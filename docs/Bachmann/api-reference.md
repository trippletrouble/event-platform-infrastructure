# API-Referenz

Kompakte Übersicht aller REST-Endpoints.
Die **autoritative, self-descriptive Spezifikation** ist die live generierte OpenAPI-Doku:

- **Swagger UI:** `GET /api` (Backend, z. B. `http://localhost:3100/api`)
- **Committed Spec:** `backend/docs/swagger-v3.yml`

Verwandt: `docs/architecture-and-rest-review.md`, `docs/rest-design-decisions.md`.

---

## Konventionen

- **Auth:** `JWT` = gültiges Access-Token (Cookie oder `Authorization: Bearer`) nötig.
- **Public:** kein Token nötig.
- **Admin:** nur Rolle `ADMIN` (`RolesGuard`).
- **Ticket-Shop:** Admin **oder** verifizierte Company (`TicketShopAccessGuard`).
- **ETag:** Antwort trägt `ETag` + `Cache-Control` (Conditional GET via `If-None-Match`).
- **If-Match:** Write mit Optimistic-Concurrency-Prüfung (`412` bei veraltetem Stand).
- Datenformat: durchgängig `JSON`.

---

## Auth — `/auth`

| Methode | Pfad | Auth | Zweck | Caching |
|---|---|---|---|---|
| GET | `/auth/oauth` | Public | Login starten (Redirect zu Keycloak) | — |
| GET | `/auth/oauth/callback` | Public | OAuth-Callback, Token-Tausch, Cookies setzen | — |
| POST | `/auth/logout` | Public | Session beenden, Token-Revocation | — |
| GET | `/auth/session` | JWT | Aktueller Session-User (+ `_links`) | **ETag**, private |
| GET | `/auth/me` | JWT | User inkl. Company | **ETag**, private |

## Companies — `/companies`

| Methode | Pfad | Auth | Zweck | Caching |
|---|---|---|---|---|
| POST | `/companies` | JWT | Company registrieren | — |
| GET | `/companies/:id` | Public | Company abrufen (+ `_links`) | **ETag**, public |
| PATCH | `/companies/:id` | JWT (Owner) | Company aktualisieren | **If-Match → 412** |
| PATCH | `/companies/members/:id` | JWT (Owner) | Mitglieder entfernen | — |
| POST | `/companies/:id/image` | JWT | Logo hochladen (JPEG/PNG, max 5 MB) | — |
| POST | `/companies/:id/logo-upload-url` | JWT | Presigned Upload-URL anfordern | — |
| DELETE | `/companies/:id/image` | JWT | Logo löschen | — |

## Events — `/events` (Controller `@Public`)

| Methode | Pfad | Auth | Zweck | Caching |
|---|---|---|---|---|
| GET | `/events/infos` | Public | Nächstes/aktuelles Event | **ETag**, public 1 h |
| GET | `/events/exhibitors` | Public | Aussteller eines Events | **ETag**, public 1 h |

## Bookings — `/bookings` (`TicketShopAccessGuard`)

| Methode | Pfad | Auth | Zweck | Caching |
|---|---|---|---|---|
| GET | `/bookings` | Ticket-Shop | Verfügbare Tiers (`?eventId=`) | **ETag** |
| POST | `/bookings` | Ticket-Shop | Tier buchen (Guard gegen Doppelkauf) | — |
| GET | `/bookings/:id` | Ticket-Shop | Buchung abrufen | **ETag** |
| POST | `/bookings/:id/upgrade` | Ticket-Shop | Standplatz upgraden | — |
| PATCH | `/bookings` | Ticket-Shop | Buchung stornieren (`cancel`-Link) | — |

## Payments — `/payments`

| Methode | Pfad | Auth | Zweck | Caching |
|---|---|---|---|---|
| POST | `/payments/checkout` | JWT | Checkout-Session (Stripe/PayPal) | `no-store` |
| POST | `/payments/webhook` | Public* | Stripe-Webhook (signaturgeprüft) | `no-store` |
| POST | `/payments/webhook/paypal` | Public* | PayPal-Webhook (signaturgeprüft) | `no-store` |

\* Public im Sinne von "kein JWT", aber durch Webhook-Signatur abgesichert.

## Invitations — `/invitations`

| Methode | Pfad | Auth | Zweck | Caching |
|---|---|---|---|---|
| PATCH | `/invitations/renew` | JWT | Invite-Code der eigenen Company erneuern | — |
| PATCH | `/invitations/:invitationCode` | JWT | Einladung einlösen (Company beitreten) | — |

## Admin — `/admin` (`@Roles(ADMIN)`)

| Methode | Pfad | Zweck | Caching |
|---|---|---|---|
| GET | `/admin` | Nutzerliste (Admin-Einstieg) | **ETag**, private |
| GET | `/admin/users` | Nutzerliste (paginiert) | **ETag**, private |
| PATCH | `/admin/promote/:userId` | User zum Admin befördern | — |
| PATCH | `/admin/demote/:id` | Admin herabstufen | — |
| GET | `/admin/companies` | Firmenliste (paginiert, Filter) | **ETag**, private |
| GET | `/admin/companies/:companyId` | Firmendetail + Buchungshistorie | **ETag**, private |
| PATCH | `/admin/companies/:companyId` | Sponsor-/Verifizierungsstatus | — |
| DELETE | `/admin/companies/:companyId` | Company löschen | — |
| GET | `/admin/dashboard` | KPI-Dashboard | **ETag**, private |
| GET | `/admin/events` | Events (paginiert) | **ETag**, private |
| POST | `/admin/events` | Event anlegen | — |
| GET | `/admin/events/:eventId` | Event-Detail | **ETag**, private |
| PATCH | `/admin/events/:eventId` | Event aktualisieren | — |
| DELETE | `/admin/events/:eventId` | Event löschen | — |
| GET | `/admin/exhibitors` | Aussteller (paginiert, Suche) | — |
| PATCH | `/admin/exhibitors/:companyId` | Aussteller-Logistik/-Status | — |

---

## Fehler-Codes (einheitlich)

| Code | Bedeutung |
|---|---|
| `400` | Malformed Request (z. B. ungültiges JSON) |
| `401` | Fehlendes/abgelaufenes Token |
| `403` | Authentifiziert, aber keine Berechtigung |
| `404` | Resource nicht gefunden |
| `409` | Konflikt (z. B. ausgebucht, Duplikat, Doppelkauf) |
| `412` | Precondition Failed (veralteter `If-Match`) |
| `422` | Validierungsfehler (mit `details[]`) |

> `500` wird bewusst nicht nach außen gegeben (siehe `rest-design-decisions.md`, §1).