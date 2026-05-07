# Generelle MR
## Beschreibe deine Änderungen
>
## User Story ID und Link
- User Story ID:
- Issue Link:
## Checklist bevor Merge Request
- [ ] Ich habe den Master Branch gepullt und in meinen Feature Branch gemerged
- [ ] Ich habe eine self-review meines Codes gemacht
- [ ] Der Code ist richtig formatiert
- [ ] Das Feature ist vollständig fertig und bereit für eine Review
- [ ] Diese MR hat als Zielbranch den develop Branch
- [ ] Ich habe alle console und debug logs entfernt
- [ ] Ich habe einen Wiki Eintrag zu diesem Feature erstellt

- [ ] Tests sind vorhanden und grün (falls zutreffend)
---
# Backend Spezifisch
## Funktionalität & API-Design
- [ ] Alle betroffenen Endpunkte entsprechen der OpenAPI-Spezifikation (`docs/swagger.yml`)
- [ ] Bei neuen oder geänderten Endpunkten wurde die OpenAPI-Spezifikation aktualisiert
- [ ] RESTful-Prinzipien sind eingehalten (korrekte HTTP-Methoden, Statuscodes, Ressourcen-Benennung)
- [ ] Hypermedia-Links sind in den Responses enthalten, wo sinnvoll (HATEOAS)
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