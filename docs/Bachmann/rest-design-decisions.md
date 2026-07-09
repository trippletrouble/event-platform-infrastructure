# REST-Design-Entscheidungen

Kurze Begründung der wichtigsten Design-Entscheidungen der API.
Ziel: nachvollziehbar machen, *warum* etwas so gebaut ist — nicht nur *dass*.

Verweise: `docs/architecture-and-rest-review.md`, `docs/api-reference.md`.

---

## 1. Keine `500`-Fehler nach außen

- **Entscheidung:** Fehler werden auf Domänen-Codes gemappt (`400/401/403/404/409/412/422`).
- **Warum:**
  - `500` ist für Clients nicht handhabbar (keine Aktion ableitbar).
  - Klare Codes machen das Verhalten testbar und dokumentierbar.
- **Wie:** NestJS-Exceptions (`NotFoundException`, `ConflictException`, …) + globale `ValidationPipe`.
- **Trade-off:** erfordert Disziplin bei der Fehlerbehandlung im Service-Layer.

## 2. HAL-`_links` statt fest kodierter URLs

- **Entscheidung:** Responses tragen `_links` (HAL-Stil: `{ rel: { href, method } }`).
- **Warum:**
  - RMM-Level 3: Clients folgen Links statt URLs zu raten.
  - **Zustandsabhängige Links** (z. B. `cancel` nur bei stornierbaren Buchungen) verlagern Berechtigungs-Logik auf den Server.
  - UI kann Controls ausblenden, wenn der Server die Aktion nicht anbietet.
- **Trade-off:** noch nicht auf jedem Endpoint; `href`s teils absolut/relativ (Client normalisiert).

## 3. ETags statt `Last-Modified`

- **Entscheidung:** starker `ETag` = quoted MD5 des JSON-Body.
- **Warum:**
  - Genauer als Zeitstempel (erkennt jede inhaltliche Änderung, keine 1-Sekunden-Granularität).
  - Ein Token dient **doppelt**: Read-Revalidation (`If-None-Match`) *und* Write-Concurrency (`If-Match`).
- **Wie:** globaler `CacheHeaderInterceptor` + `computeEtag` (`etag.util.ts`).
- **Trade-off:** MD5 über den Body kostet CPU; akzeptabel bei kleinen Payloads.

## 4. `@HttpCache`-Decorator statt globalem Caching

- **Entscheidung:** Caching ist **opt-in pro Route** über `@HttpCache(...)`.
- **Warum:**
  - Explizit statt implizit — nur bewusst markierte GETs cachen.
  - Sensible Endpoints setzen `noStore` (z. B. Payments).
  - `scope`/`max-age`/`Vary` pro Route steuerbar (`private` + `Vary: Authorization` für User-Daten).
- **Trade-off:** Entwickler müssen den Decorator aktiv setzen.

## 5. Optimistic Concurrency (`If-Match` → `412`)

- **Entscheidung:** Writes können mit `If-Match` gegen den aktuellen ETag geprüft werden.
- **Warum:**
  - Verhindert **Lost Updates** bei parallelem Editieren (zwei Admins, dieselbe Company).
  - Kein Locking nötig — der Client trägt den zuletzt gesehenen Stand.
- **Wie:** `assertIfMatch` (`etag.util.ts`); aktiv in `PATCH /companies/:id`.
- **Trade-off:** aktuell nur auf einer Route erzwungen; Rollout auf weitere Mutations dokumentiert.

## 6. Stateless JWT statt Server-Session

- **Entscheidung:** kein Session-Store; Identität steckt im Keycloak-JWT.
- **Warum:**
  - Horizontale Skalierung ohne Sticky-Sessions.
  - Standard-konform (OIDC), Signaturprüfung gegen **Remote-JWKS**.
- **Wie:** `JwtAuthGuard` + `jose.jwtVerify` (Issuer + `azp` + Clock-Tolerance).
- **Trade-off:** Token-Widerruf greift erst nach Ablauf; deshalb explizite Revocation beim Logout.

## 7. Token in `httpOnly`-Cookies (nicht im JS-Zugriff)

- **Entscheidung:** access/refresh/id-Token als `httpOnly`, `sameSite=lax`, prod `secure`.
- **Warum:**
  - Schutz gegen **XSS-Token-Diebstahl** (kein Zugriff aus JavaScript).
  - `sameSite=lax` mindert CSRF; zusätzlich `state`-Check im OAuth-Callback.
- **Trade-off:** Cross-Domain-Setup braucht korrekte Cookie-Domain-Ableitung.

## 8. Separater `image-service` für Object-Storage

- **Entscheidung:** MinIO nur über einen eigenen Microservice erreichbar.
- **Warum:**
  - **Layered System**: Business-Logik kennt kein S3/MinIO-Detail.
  - Presigned-URL-Erzeugung + Bucket-Management gekapselt.
- **Trade-off:** ein Netzwerk-Hop mehr; dafür klare Verantwortlichkeiten.

## 9. Repository-Pattern über Prisma

- **Entscheidung:** Controller/Services nutzen Interfaces, nicht Prisma direkt.
- **Warum:**
  - Persistenz austauschbar/mockbar → einfache Unit-Tests.
  - Transaktionen (z. B. Slot-Dekrement bei Buchung) an einer Stelle gekapselt.
- **Trade-off:** etwas mehr Boilerplate (Interface + Implementierung).

## 10. Webhook-Signaturen server-seitig verifizieren

- **Entscheidung:** Stripe- und PayPal-Webhooks werden signaturgeprüft.
- **Warum:**
  - Zahlungsbestätigung darf nicht fälschbar sein.
  - Stripe: Raw Body + `Stripe-Signature`. PayPal: Verifikation über die PayPal-API.
- **Wie:** `payments.service.ts` (`handleWebhook`, `handlePayPalWebhook`).
- **Trade-off:** Raw-Body-Handling nötig (`rawBody: true` in `main.ts`).