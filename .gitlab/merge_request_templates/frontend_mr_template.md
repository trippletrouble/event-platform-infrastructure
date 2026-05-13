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

### Perceivable (Wahrnehmbar):
- [ ] Ich habe alle Medien(Audios, Videos) auf verständliche subtitles geprüft
- [ ] Animationen: Pausierbar und durch prefers-reducedmotion steuerbar?
- [ ] Labels: Ich habe alle Formularfelder auf sichtbare Labels geprüft !
- [ ] Layout & Informationshierarchie: Ich habe sicher gestellt das Layout responsive interagiert →Inhalte müssen bei 200 % und 400% Zoom nutzbar bleiben (WCAG 1.4.4, Level AA) →Kein horizontales Scrollen bei Viewport-Breite von 320 CSS-Pixel (WCAG 1.4.10, Level AA) → Touch-Targets: mindestens 44×44px (WCAG 2.5.8)

- [ ] Layout & Informationshierarchie: Eine Seite/Ein Abschnitt hat eine klare Hauptaufgabe
- [ ] Layout & Informationshierarchie: Meine Visuelle Hierarchie unterstützt die semantische Hierarchie
- [ ] Layout & Informationshierarchie: Ich hab Abstände und Gruppierungen als Hilfe zur Orientierung designt
- [ ] Color: Ich habe Text und UI-Elemente auf Ausreichender Kontrast geprüft

- [ ] Color: Ich habe sichergestellt das es keine Informationen gibt die nur durch Farbe vermittelt werden
- [ ] Fonts/Text: Ich hab die Typografie auf Skalierbarkeit getestet (wie bei layout 200%-400%)
- [ ] Fonts/Text: Verwendete Fonts sind Serifenlos
- [ ] Fonts/Text: Erkennbarkeit  der Verwendete Fonts ist sichergestellt: Wie klar und unterscheidbar sind einzelne Buchstaben und Zahlen
- [ ] Fonts/Text:Verwendete Fonts sind nicht Kursiv
- [ ] Fonts/Text: KEINE LANGEN TEXTE WIE DIESER
- [ ] Fonts/Text: Kein Blocksatz sondern linksbündig ( besser lesbar)
- [ ] Fonts/Text: Ich habe Semantische Hervorhebung (fett, kursiv) gezielt und sparsam eingesetzt
- [ ] Fonts/Text: Bei Links der Text ist der Informationsträger “Zur Anmeldung”!  
“Hier klicken” => nicht das ist nicht eindeutig
- [ ] Fonts/Text: Lesbarkeit der Verwendete Fonts ist sichergestellt: Wie flüssig und einfach ist der gesamte Text zu lesen
- [ ] Images: Ich habe alle Images auf einen aussagekräftigen Alt-Text geprüft
- [ ] Images: Ich habe für alle Images passende Fallback implementiert
### Bedienbarkeit (Operable):
- [ ] Ich habe meine anwendung auf Vollständige Tastaturbedienung geprüft alle Funktionen sind erreichbar ohne Maus
- [ ] Die Fokus Reihenfolge der Tastaturbedienung folgt der visuellen und inhaltlichen Logik
- [ ] Bei der Tastaturbedienung sind kein „Tastatur-Fallen" in Menüs, Dialogen oder Widgets implementiert 
- [ ] Bei der Tastaturbedienung sind Skip-Link und Landmarken für schnellere Navigation implementiert 
- [ ] Bei Tastaturbedienung ist Sichtbarer Fokusabstand auf allen interaktiven Elementen gegeben → Fokus-Indikator: mindestens 2px breit, Kontrast 3:1 gegen Hintergrund (WCAG 2.4.13)
- [ ] Alle implementierte Klick-/Touchflächen erfüllen die ausreichende größe (mindestens 44×44px)
- [ ] Ich habe keine unnötigen Zeitlimits oder Auto-Weiterleitungen implementiert
### Verständlichkeit (Understandable):
- [ ] Es wurde einfache und direkte Sprache verwendet
- [ ] Die Überschriftenhierarchie ist klar und konsistent 
- [ ] Es wurde eindeutige Beschriftungen und keine vagen Beschriftungen/Platzhalter verwendet
- [ ] Konsistentes Verhalten: Gleiche Aktionen → gleiche Muster

### Fehlermeldungen
- [ ] Ich habe präzise, verständliche Fehlermeldungen mit Lösungshinweisen implementiert 
- [ ] Wo ist der Fehler? Fehlertext nah am Feld, Feld visuell hervorheben
- [ ] Was ist der Fehler? (Konkret benennenz.B. „Ungültige Eingabe" ohne weiteren Kontext ist nicht ausreichend)
- [ ] Wie lässt er sich beheben? (Handlungsanweisung geben)
- [ ] !!! Aria-Attribute einsetzen ARIA erklärt dem Screenreader(wichtig bei komplexen UI-Elementen): „Das hier ist ein Menü", „Dieser Button ist gerade geöffnet", „Dieses Feld ist Pflichtfeld"
- [ ] Bei mehreren Fehlern in einem Formular → Fehlerzusammenfassung am Formularanfang mit Ankerlinks zu den Feldern
- [ ] Statusmeldungen (Erfolg/Fehler) Screenreader
- [ ] Live-Validierung dezent und nicht übermäßigaggressiv (Fehlermeldungen anzeigen so dass sie helfen, ohne zu nerven oder zu stressen)
### Robustheit (Robust):
- [ ] Semantische Struktur als Grundlage für Assistive Technologien implementieren Semantische Rolle = Ist das ein Button, ein Link, eine Überschrift?

