# Zero-shot-Lauf 01 – Auswertung

## Forschungsfrage

How did the Sun's flare activity change between February 2021 and
February 2026, and did strong flares become a larger share of all
flares over time?

## Technisches Ergebnis

- Der von Qwen erzeugte Python-Code konnte in Docker ausgeführt werden.
- Docker lief ohne Netzwerkzugriff.
- Arbeitsspeicher und CPU wurden begrenzt.
- Die Terminalausgabe wurde unter `runs/zero_shot_01_docker.log` gespeichert.
- Das Diagramm wurde unter `outputs/zero_shot_01/strong_flare_percentage.png` gespeichert.

## Ausgabe

- Flares im gefilterten Datensatz: 32.456
- Flares im Februar 2021: 6
- Flares im Februar 2026: 736
- Erkannte starke Flares: 0

## Erkannter fachlicher Fehler

Qwen prüft die Flare-Klasse mit:

`value.upper() in ["M", "X"]`

Die CSV enthält jedoch Werte wie `M1.4` und `X1.0`. Deshalb werden
M- und X-Flares nicht erkannt. Eine spätere korrigierte Version muss
prüfen, ob der Wert mit `M` oder `X` beginnt.

## Fazit

Die technische Ausführung war erfolgreich, aber das Ergebnis ist
fachlich falsch. Der Zero-shot-Lauf zeigt, dass ausführbarer Code
nicht automatisch eine korrekte Datenanalyse bedeutet.

## Vergleich mit der eigenen pandas-EDA

Die manuelle EDA enthält insgesamt 33.076 Flares.

Dabei wurden folgende Klassen erkannt:

- A: 120
- B: 4.027
- C: 26.723
- M: 2.092
- X: 114

Damit enthält der Datensatz 2.206 starke Flares:

`2.092 M-Flares + 114 X-Flares = 2.206 starke Flares`

Der Zero-shot-Code meldete dagegen 0 starke Flares. Ursache ist,
dass er nur nach den exakten Werten `M` und `X` sucht. Die tatsächlichen
Werte enthalten zusätzlich eine Stärke, beispielsweise `M1.4` oder `X1.0`.

Außerdem verwendet die manuelle EDA bei fehlenden gemessenen GOES-Klassen
die Spalte `goes_estimated_mean_class`. Der Zero-shot-Code entfernt diese
620 Zeilen vollständig.

Die technische Ausführung der Baseline war erfolgreich, das fachliche
Ergebnis war jedoch falsch.