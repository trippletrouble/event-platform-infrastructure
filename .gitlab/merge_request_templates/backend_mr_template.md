## Beschreibung der Änderungen
>
>
## User Story ID und Link
- User Story ID:
- Issue Link:
## Checkliste vor dem Review
- [ ] Ich habe den `master`-Branch in meinen `feature`-Branch gemerged
- [ ] Ich habe ein Self-Review meines Codes durchgeführt
- [ ] Der Code ist korrekt formatiert
- [ ] Das Feature ist vollständig implementiert und bereit für das Review
- [ ] Diese MR zielt auf den `develop`-Branch
- [ ] Ich habe sämtlichen Debug-Code und Console-Logs entfernt
- [ ] Ich habe einen Wiki-Eintrag zu diesem Feature erstellt

- [ ] Bei Kernfeatures habe ich ausführliche Tests geschrieben (falls zutreffend)
- [ ] Die hinzugefügten Tests sind erfolgreich (falls zutreffend)

## Funktionalität & API-Design
- [ ] Das Feature ist vollständig implementiert und funktionsfähig
- [ ] Alle betroffenen Endpunkte entsprechen der OpenAPI-Spezifikation (`swagger.yml`)
- [ ] Bei neuen oder geänderten Endpunkten wurde die OpenAPI-Spezifikation aktualisiert
- [ ] RESTful-Prinzipien sind eingehalten (korrekte HTTP-Methoden, Statuscodes, Ressourcen-Benennung)
- [ ] Hypermedia-Links sind in den Responses enthalten, wo sinnvoll (HATEOAS)
- [ ] Caching-Header (`Cache-Control`, `ETag`) sind gesetzt, wo anwendbar
- [ ] Eingabevalidierung ist für alle Endpunkte implementiert (DTOs mit class-validator o.Ä.)
- [ ] Fehlerresponses folgen einem einheitlichen Format (`ErrorResponseDto`)

## Authentifizierung & Autorisierung
- [ ] Geschützte Endpunkte prüfen die Authentifizierung (OAuth / Session)
- [ ] Rollenbasierte Zugriffskontrolle ist korrekt umgesetzt (Admin vs. Company)
- [ ] Unautorisierte Zugriffe werden mit `401`/`403` korrekt abgewiesen

## Datenbank
- [ ] Prisma-Schema-Änderungen sind via Migration eingecheckt (`prisma migrate`)
- [ ] Neue Relations haben explizite `onDelete`-Regeln
- [ ] FK-Spalten haben `@@index`-Direktiven für Query-Performance
- [ ] Seed-Daten sind aktualisiert, falls das Schema sich geändert hat
- [ ] Alle Datenbankänderungen sind im Wiki dokumentiert

## Tests
- [ ] Unit-Tests für die Service-Logik sind vorhanden und grün
- [ ] Integrationstests für neue/geänderte Endpunkte sind vorhanden und grün
- [ ] Edge Cases und Fehlerfälle sind abgedeckt (ungültige Eingaben, fehlende Rechte, nicht gefundene Ressourcen)
- [ ] Alle bestehenden Tests sind weiterhin grün

## Dokumentation
- [ ] Wiki-Eintrag für das Feature ist erstellt oder aktualisiert
- [ ] Komplexe Logik ist im Code kommentiert (Warum, nicht Was)