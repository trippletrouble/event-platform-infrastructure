# Implementation Plan: ETags & Automatic HATEOAS Link Usage (Frontend)

Audience: a coding agent implementing the frontend side. The backend already emits
ETags on GET responses and `_links` on (almost) every resource. The goal is to make
the **frontend** consume both consistently and automatically.

---

## ✅ Status — implemented (2026-07-08)

The gaps and the critical caveat have been addressed. Delivered:

**Backend (the caveat — real `If-Match`/412 enforcement):**
- `backend/src/common/util/etag.util.ts` — shared `computeEtag(body)` (now the single
  source used by the read interceptor) and `assertIfMatch(ifMatch, currentRepresentation)`
  which throws `412 PreconditionFailed` on a stale ETag, is a no-op when no `If-Match` is
  sent, and honors `If-Match: *`. Unit-tested in `etag.util.spec.ts`.
- `CacheHeaderInterceptor` refactored to use `computeEtag`.
- `CompaniesService.getResource(id)` centralizes the exact `GET /companies/:id`
  representation so the read ETag and the write precondition hash identical bytes.
- `PATCH /companies/:id` now enforces `If-Match` via `assertIfMatch` (the company edit
  form's write path — the real edit-collision case). Documented with a 412 response.
  Controller spec covers match / stale-412 / no-header cases.

**Frontend (the ETag gap):**
- `api.ts`: fixed the **304 fall-through** (unconditional refetch on cache miss instead
  of a spurious error); **auto-attaches `If-Match`** on writes from the cached GET ETag
  (explicit `etag` still wins) making concurrency automatic; **always invalidates** the
  GET cache after a successful write (no longer gated on a write-response ETag); honors
  `cache: 'no-store'` to bypass conditional GET + caching. New tests cover each.

**Frontend (the HATEOAS gap — helper layer + typing):**
- `link-helpers.ts`: added `hasLink`, `follow`, and a typed `MissingLinkError` (lists
  available rels; lets UIs distinguish "action withheld" from transport failure), plus
  `href` **origin normalization** so absolute backend links don't double-prefix. Tested.
- Reconciled `Links` typing: deleted the array-shaped `LinksDto`/`HateoasLinkDto`,
  standardized every DTO on `Links = Record<string, HateoasLink>`.
- `CompanyProfile.tsx`: catches `isConflictError` (412) → shows a conflict message and
  refetches so the user reapplies against current data.

**Verification:** backend `256/256` pass; the affected frontend suites (`api`,
`link-helpers`, `CompanyProfile`) pass `69/69`. 8 pre-existing frontend suites fail
identically on the clean tree (unrelated German-copy/`api.types` export drift) — not
touched here.

**Deliberately left as mechanical follow-up** (bounded, low-risk, no new mechanism):
1. Extend `assertIfMatch` to the other mutable resources (admin company update, events,
   bookings) — same three-line pattern: load the GET representation, `assertIfMatch`,
   then mutate. Each needs its GET representation centralized like `getResource`.
2. Migrate remaining services from hardcoded URLs to `follow(parentLinks, rel)` where the
   backend already emits actionable rels (bookings `payment`/`cancel`/`upgrade`, events
   `tiers`). Use `hasLink` to conditionally render the corresponding action controls.

The rest of this document is the original analysis and the full rollout design.

---

## 0. Current state (verified in the codebase)

### What the backend actually does
- **ETag generation (read side):** `backend/src/common/interceptors/cache-header.interceptor.ts`
  hashes the serialized GET body (MD5), sets the `ETag` header, and returns `304` when the
  request's `If-None-Match` matches. **Only fires on endpoints decorated with `@HttpCache(...)`**
  (`if (!options) return next.handle()`). There are **17 `@HttpCache` usages across 8 controllers**.
  Endpoints without the decorator send **no** ETag.
- **HATEOAS:** `_links: { <rel>: { href, method } }` (HAL-style object, not an array) is emitted
  broadly — companies, bookings, events, invitations, admin controllers, paginated lists, `auth/me`, etc.
- **⚠️ `If-Match` / `412` is NOT implemented on the backend.** The interceptor returns early for
  every non-GET request. No controller or guard validates `If-Match` or throws `PreconditionFailed`.
  So **write-side optimistic concurrency does not currently work end-to-end** — see §4.

### What the frontend already has (infrastructure exists, usage does not)
- `frontend/src/services/api.ts`
  - `apiFetchWithMeta<T>()` already: sends `If-None-Match` from an in-memory cache on GET, handles
    `304` by returning the cached body, stores `{etag, body}` per `GET:<path>` on 200, invalidates
    the base path on writes, and accepts an `etag` option that becomes `If-Match` on non-GET.
  - `apiClient.{get,post,put,patch,delete}` wrappers. `put/patch/delete` accept an optional `etag`
    argument, but **no caller ever passes it**.
  - `isConflictError(e)` → checks `statusCode === 412`. **Never called anywhere.**
- `frontend/src/services/etag-cache.ts` — module-level in-memory `Map` cache.
- `frontend/src/services/link-helpers.ts` — `getLink(links, rel)` and `followLink<T>(link, body)`.
- `frontend/src/types/common.types.ts` — `HateoasLink` / `Links` types.
- 10 frontend DTOs already declare `_links?: Links`.

### The actual gaps
1. **HATEOAS is barely used.** Only `payment.service.ts` (and a few `*ByLink` helpers in
   `booking.service.ts`) call `followLink`. Every other service **hardcodes URLs** (`/companies/${id}`,
   `/companies/${id}/logo-upload-url`, `/bookings/${id}/upgrade`, …) instead of following links from
   the resource that was already fetched. There is no discipline and no shared consumption pattern.
2. **ETag GET caching is only half-wired.** `apiFetchWithMeta` handles it, but (a) it only helps on
   `@HttpCache` endpoints, and (b) there is a **304 fall-through bug** (see §2.1).
3. **ETag write concurrency is dead code.** The `etag`/`If-Match`/`412` plumbing exists but is never
   exercised, and the backend wouldn't honor it anyway.

---

## 1. Goals & scope

**In scope (frontend, backend already supports):**
- A. Make **ETag GET revalidation** correct and robust everywhere it applies (§2).
- B. Make **HATEOAS link-following** the default consumption pattern for related/derived resources,
  with a clean, testable helper layer and DTO typing (§3).

**Conditionally in scope (needs a backend decision):**
- C. **Optimistic-concurrency writes** via `If-Match`/`412`. The frontend plumbing is ready, but the
  backend does not enforce it. Either (a) descope until the backend adds `If-Match` validation, or
  (b) do it as a coordinated FE+BE change. See §4 — **do not silently ship a fake concurrency guard.**

**Out of scope:** replacing the hand-rolled fetch layer with React Query/SWR; changing the backend
HAL shape; persistent (localStorage) ETag caching.

---

## 2. Workstream A — ETag GET revalidation

### 2.1 Fix the `304` fall-through bug (blocking, do first)
In `api.ts`, `apiFetchWithMeta`, the `304` branch only returns when the cache has an entry:

```ts
if (res.status === 304) {
  const cached = etagCache.get(`GET:${path}`);
  if (cached) return { data: cached.body as T, etag: cached.etag };
  // ← falls through here on cache miss
}
```

On a cache miss (e.g. cache cleared after the conditional request was sent), execution falls into the
`!res.ok` block and **throws `ApiError(304, …)`** — a spurious error. Fix: if a `304` arrives with no
cached body, treat it as a cache-coherence failure and **re-fetch unconditionally** (strip
`If-None-Match` and retry once), or throw a clear typed error. Recommended: retry once without the
conditional header.

Add a regression test in `frontend/src/__tests__/services/api.test.ts`:
`304 + empty cache → performs unconditional refetch and returns fresh body`.

### 2.2 Confirm/enable the cache key includes the full path + query
`GET:${path}` is used as the key and `path` includes the query string (e.g.
`/admin/companies?page=1&limit=20`). Good. But **write invalidation** uses only
`path.split('?')[0]` (base path), so a `PATCH /companies/5` invalidates `GET:/companies/5` but **not**
`GET:/companies/5?include=bookings` or list endpoints like `GET:/admin/companies?page=1`. Decide the
invalidation policy:
- Minimum: keep base-path invalidation but **also** clear list/collection keys related to the mutated
  resource. Add an `invalidatePrefix(prefix)` method to `EtagCache` and call it for known collections.
- Document that stale list caches are acceptable because collection GETs are also ETag-revalidated on
  next fetch (the server 200s with a new ETag if data changed). Given the backend re-hashes the body,
  **a changed collection will not 304**, so stale reads self-heal on next request. This makes
  aggressive invalidation optional — note it and keep it simple.

### 2.3 Make GET caching opt-out-able per call
Some GETs must always be fresh (e.g. polling, auth checks). Add an option to `ApiFetchOptions`
like `cache?: 'revalidate' | 'no-store'` (default `'revalidate'`). When `'no-store'`, skip
`If-None-Match` and skip storing the response. Wire `apiClient.get` to accept it.

### 2.4 Tests
- `If-None-Match` sent when a cached ETag exists; not sent otherwise.
- `304` returns cached body without re-parsing.
- Response ETag stored on `200`.
- `cache: 'no-store'` bypasses both.

---

## 3. Workstream B — Automatic HATEOAS link usage

### 3.1 Principle
Once a resource has been fetched, **derived actions/relations must be taken from that resource's
`_links`**, not by reconstructing URLs. New URL strings should only be hardcoded for **entry-point**
requests (the first fetch of a root collection/resource) — everything reachable from a response
should be followed via `_links`.

### 3.2 Harden the link-helper layer (`link-helpers.ts`)
Current `followLink` drops the ETag/meta and ignores query/caching options. Extend it:

```ts
export function getLink(links: Links | undefined, rel: string): HateoasLink {
  const link = links?.[rel];
  if (!link) throw new MissingLinkError(rel, links);
  return link;
}

export function hasLink(links: Links | undefined, rel: string): boolean {
  return Boolean(links?.[rel]);
}

export function followLink<T>(link: HateoasLink, body?: unknown): Promise<T> { /* existing switch */ }

// convenience: resolve + follow in one call
export function follow<T>(links: Links | undefined, rel: string, body?: unknown): Promise<T> {
  return followLink<T>(getLink(links, rel), body);
}
```

- Add a typed `MissingLinkError extends Error` (include the rel and the available rels in the message)
  so UIs can distinguish "server didn't offer this action" from a transport error. This matters because
  HATEOAS lets the server **withhold** links the current user isn't allowed to use — the UI should
  hide the corresponding control when the link is absent (`hasLink`), not attempt and fail.
- Keep `method` optional and default to `GET` (already done).
- **Base-URL note:** `_links.href` values are server-relative paths (e.g. `/companies/5`). `apiClient`
  prepends `BASE_URL`. Verify every emitted `href` is root-relative and does **not** already include the
  API prefix/origin; if any controller emits absolute URLs, normalize in `followLink` (strip origin).

### 3.3 Standardize DTO `_links` typing
- All response DTOs that the backend decorates with links must declare `_links?: Links` (HAL object),
  **not** the legacy `LinksDto { hateoasLinks: HateoasLinkDto[] }` array shape.
  `frontend/src/types/dto/links.dto.ts` currently defines the array shape and is inconsistent with the
  actual server payload. **Reconcile:** delete/deprecate `LinksDto`/`HateoasLinkDto` array types and
  standardize on `Links = Record<string, HateoasLink>` from `common.types.ts`. Update the ~10 DTOs to
  use `_links?: Links`.
- Cross-check against the real payloads (see `backend/swagger.yml` and the controller examples) to get
  the **rel names** right per resource (`self`, `payment`, `cancel`, `tiers`, `upgrade`, `members`,
  `logo-upload-url`, list `next`/`prev`, …). Produce a short **rel catalog** table in this doc's PR
  description mapping resource → available rels → method, derived from the controllers under
  `backend/src/**/*.controller.ts` and `bookings.service.ts` / `invitations.service.ts`.

### 3.4 Migrate services to follow links (incrementally, per resource)
For each service, keep **one** hardcoded entry point and convert the rest to `follow(...)`. Concretely:

- **company.service.ts**
  - `getCompany(id)` stays a hardcoded entry point (returns `_links`).
  - `getLogoUploadUrl` → `follow(company._links, 'logo-upload-url', {...})` when a company is already
    in hand; keep an id-based fallback for cold calls.
  - `updateCompany` / `removeCompanyMembers` → prefer `follow(company._links, 'self'|'update'|'remove-members', body)`
    if the backend exposes those rels; otherwise leave hardcoded and note the missing rel for backend.
- **booking.service.ts** — already has `getTiersByLink`, `cancelBookingByLink`. Make the
  `...ByLink` variants the primary API and have components pass the parent resource's `_links`.
  `upgradeBooking` → `follow(booking._links, 'upgrade', data)`.
- **payment.service.ts** — already correct (`createCheckoutByLink`). Make it the default; keep
  `createCheckout` only as the cold entry point.
- **event.service.ts, invitation.service.ts, user.service.ts, dashboard.service.ts** — same treatment:
  audit each function, replace derived-URL calls with `follow(parentLinks, rel)`.

Signature convention: link-following functions take the **parent resource or its `_links`** plus a body,
never re-derive ids into URLs.

### 3.5 Update hooks & components to thread `_links`
Hooks (`useCompany`, `useEvent`, `useEvents`, `useTiers`, `useExhibitors`, …) currently discard nothing
special but components call id-based service functions. Migrate the write/derived flows:
- Store the fetched resource (including `_links`) in hook state (already happens — `_links` rides along
  on the DTO).
- In components that trigger actions (e.g. `app/admin/companies/[id]/page.tsx` sponsor toggle / delete,
  booking cancel/upgrade, checkout), pass `resource._links` into the `...ByLink` service call.
- **Conditionally render action controls** based on `hasLink(resource._links, rel)` so the UI reflects
  server-granted capabilities (hides buttons the current user can't use).

### 3.6 Tests
- `getLink`/`hasLink`/`follow` happy path + `MissingLinkError` with available-rels message.
- `followLink` dispatches to the correct verb and forwards the body.
- Service-level: with a mocked resource containing `_links`, the derived call hits the href from the
  link (assert the request URL), not a reconstructed string.
- Component-level: action button hidden when the rel is absent.
- Existing tests to keep green: `link-helpers.test.ts`, `api.test.ts`, `company.service.test.ts`,
  `useEvents.test.ts` and the MSW handlers in `__tests__/mocks/handlers.ts` (update handlers to return
  `_links` and ETags where relevant).

---

## 4. Workstream C — Optimistic-concurrency writes (`If-Match` / `412`)

**This cannot be completed frontend-only.** The plumbing exists (`apiClient.put/patch/delete(…, etag)`
→ `If-Match`; `isConflictError` → 412) but **no backend endpoint validates `If-Match` or returns 412.**

Decision required (pick one; raise with the maintainer):

- **Option C1 — Descope now (recommended default).** Leave the FE `etag`/`If-Match`/`isConflictError`
  plumbing in place but unused, and file a backend task: "Add `If-Match` precondition validation to
  mutating endpoints, returning `412 Precondition Failed` when the stored ETag differs." Do not wire the
  UI to a guard that the server ignores.

- **Option C2 — Coordinated FE+BE.** If backend work is in scope:
  1. Backend: on decorated mutating routes, compare `If-Match` against the current resource ETag
     (reuse the same hashing as the read interceptor) and throw `PreconditionFailedException` (412) on
     mismatch. Require `If-Match` where you want it enforced.
  2. Frontend: capture the ETag from the last GET (`apiFetchWithMeta` already returns it, and the cache
     stores it). Thread it into the write: `apiClient.patch(path, body, retry, etagCache.get('GET:'+path)?.etag)`.
     Add a service convenience that pulls the current cached ETag automatically.
  3. Frontend UX: catch `isConflictError(e)` in the mutation handler → show a "someone else changed this,
     reload" prompt, refetch (which revalidates via ETag), and let the user retry.
  4. Tests: 412 path surfaces the conflict UI; successful write clears/updates the cached ETag.

**Whichever option:** if descoped, add a short comment on `isConflictError` and the `etag` params in
`api.ts` noting they are reserved for the backend `If-Match` work so they aren't deleted as dead code.

---

## 5. Suggested execution order (PR-sized steps)

1. **A-fix:** §2.1 304 bug + tests. (Small, blocking, standalone.)
2. **A-polish:** §2.3 `no-store` option + §2.2 invalidation policy decision + tests.
3. **B-types:** §3.3 reconcile `Links` typing across DTOs; delete the array-shaped `LinksDto`.
4. **B-helpers:** §3.2 harden `link-helpers` (`hasLink`, `follow`, `MissingLinkError`) + tests.
5. **B-catalog:** §3.3 produce the resource→rel catalog from the controllers (reference artifact).
6. **B-migrate:** §3.4/§3.5 convert services + hooks + components resource-by-resource, one PR per
   resource (company, booking, payment already partial, event, invitation, admin). Keep tests green.
7. **C:** §4 — decide C1 vs C2; if C1, file the backend ticket and annotate the reserved code.

## 6. Acceptance criteria
- No spurious errors on `304`; conditional GETs demonstrably reduce payload (assert `If-None-Match`
  sent and cached body returned in tests).
- Derived/related actions across migrated resources go through `_links` (asserted by request-URL tests),
  with only documented entry points hardcoded.
- Action controls hide when the corresponding link is absent.
- `Links` typing is uniform (`Record<string, HateoasLink>`); no remaining `hateoasLinks[]` array usage.
- Write-concurrency (§4) is either fully working end-to-end (C2) or explicitly descoped with a filed
  backend ticket and annotated reserved code (C1) — never a UI wired to an unenforced guard.

## 7. Key files
- Read layer: `frontend/src/services/api.ts`, `frontend/src/services/etag-cache.ts`
- HATEOAS: `frontend/src/services/link-helpers.ts`, `frontend/src/types/common.types.ts`,
  `frontend/src/types/dto/*.ts`
- Services to migrate: `frontend/src/services/{company,booking,payment,event,invitation,user,dashboard}.service.ts`
- Hooks/components: `frontend/src/hooks/*`, `frontend/src/app/**/*.tsx`, `frontend/src/components/**`
- Tests/mocks: `frontend/src/__tests__/services/{api,link-helpers}.test.ts`,
  `frontend/src/__tests__/mocks/handlers.ts`
- Backend reference (do not edit unless doing C2): `backend/src/common/interceptors/cache-header.interceptor.ts`,
  `backend/src/**/*.controller.ts`, `backend/swagger.yml`