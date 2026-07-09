# Shared API Client Module

> **Scope:** Covers the enhanced API client introduced in `frontend/src/services/api.ts` within the `infrastructure` repo, including typed HTTP method helpers, error normalisation, and configurable retry logic.

| | |
|---|---|
| **Last updated** | 2026-06-17 |
| **Creator** | @nico |
| **Last Updated By** | @nico |
| **Related US** | `US-A0.9` |
| **Status** | Draft |

---

## Overview

The frontend service communicates with the backend exclusively through a central `apiFetch<T>()` wrapper in `src/services/api.ts`. US-A0.9 evolves this wrapper into a more robust shared API client: it adds structured error normalisation so all error responses share a consistent shape, automatic retry logic for transient failures, and a typed `apiClient` convenience object exposing per-method helpers (`get`, `post`, `put`, `patch`, `delete`). All existing service consumers (`auth.service.ts`, `booking.service.ts`, `payment.service.ts`) continue to work without changes because the new retry parameter is optional.

---

## Error Normalisation

Previously, the `!res.ok` error path parsed the JSON response body inline and fell back to a plain string on failure. The enhanced client extracts this into a dedicated `parseErrorResponse(res)` helper that always returns a well-formed `ErrorResponseDto` — even when the upstream response body is HTML (e.g. a 502 from a reverse proxy). This means callers can always rely on `ApiError.errorBody` having `statusCode`, `message`, and `error` fields.

---

## Retry Logic

`apiFetch<T>()` accepts an optional third parameter `retryConfig: Partial<RetryConfig> | false`. When omitted, the default config applies:

| Field | Default | Description |
|---|---|---|
| `maxRetries` | `2` | Maximum number of retry attempts after the first failure |
| `baseDelayMs` | `500` | Base delay in milliseconds; multiplied linearly by attempt number |
| `retryableStatuses` | `[408, 429, 500, 502, 503, 504]` | HTTP status codes that trigger a retry |

Retries use linear backoff (`baseDelayMs × attempt`). Network errors (where `fetch()` itself throws) are always retried since they are transient by nature. A `401` response is never retried — it redirects to `/login` immediately. Passing `false` as `retryConfig` disables retries entirely for that call.

---

## HTTP Method Helpers

`apiClient` is a typed object exported alongside `apiFetch`. It covers the standard HTTP verbs:

```ts
apiClient.get<T>(path, retryConfig?)
apiClient.post<T>(path, body?, retryConfig?)
apiClient.put<T>(path, body?, retryConfig?)
apiClient.patch<T>(path, body?, retryConfig?)
apiClient.delete<T>(path, retryConfig?)
```

`GET` inherits the default retry config. Mutation methods (`POST`, `PUT`, `PATCH`, `DELETE`) default to `retryConfig: false` to avoid accidental double-submission of non-idempotent requests. Callers can override in either direction by passing an explicit config.

---

## Key Files

- `src/services/api.ts` — core client: `apiFetch`, `apiClient`, `ApiError`, `parseErrorResponse`
- `src/types/common.types.ts` — exports the `RetryConfig` interface
- `src/__tests__/services/api.test.ts` — unit tests covering all retry, error, and method-helper scenarios
- `src/__tests__/mocks/handlers.ts` — MSW handlers extended for retry and error test cases

---

## Commands

```bash
# Run the API client unit tests
npx jest src/__tests__/services/api.test.ts

# Type-check the whole frontend
npx tsc --noEmit
```

---

## Related

- [Frontend CI/CD Pipeline](./Frontend-CI-CD-Pipeline.md)
- `US-A0.9.1` — typed fetch wrapper with auth headers
- `US-A0.9.2` — error normalisation and retry logic