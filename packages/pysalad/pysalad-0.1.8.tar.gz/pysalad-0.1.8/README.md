[<img src="https://img.shields.io/pypi/v/pysalad">](https://pypi.org/project/pysalad/)
<img src="https://img.shields.io/badge/python-3.9-blue">
<img src="https://img.shields.io/badge/license-MIT-green">

# pysalad🥗🐍     

Ein kleines Tool um über die Kommandozeile auf den [HBT](https://www.hbt.de)-Salat zuzugreifen



# How-to

## Install
````bash
pip install pysalad
````

### Salatbuchungen eines Tages anzeigen
````bash
pysalad show day # alle Buchungen von Heute zeigen
pysalad show yesterday # alle Buchungen von Gestern zeigen
pysalad show tomorrow # alle Buchungen von Morgen zeigen
pysalad show day 2021-01-01 # alle Buchungen vom ersten Januar zeigen
````

### Salatbuchungen einer Woche anzeigen
````bash
pysalad show week # alle Buchungen der aktuellen Woche zeigen
pysalad show week 2021-01-01 # alle Buchungen der ersten Januar Woche zeigen
````

### Salatbuchungen eines Monats anzeigen
````bash
pysalad show month # alle Buchungen des aktuellen Monats zeigen
pysalad show month 2021-01-01 # alle Buchungen für Januar 2021 zeigen
````

### Eigenen Vertrag in Salat anzeigen
````bash
pysalad show contract
````

### Eigenen Daten anzeigen
````bash
pysalad show employee
````

### Aufträge auf die man buchen kann
````bash
pysalad show orders
````

### Neue Buchung erstellen
````bash
pysalad report <Kommentar> <Dauer> <Auftrag> # Arbeitszeit für Heute buchen
pysalad report <Kommentar> <Dauer> <Auftrag> <Datum> # Arbeitszeit an einem bestimmten Tag buchen
````

oder ohne Parameter (die Werte müssen dann per Eingabeaufforderung eingegeben werden):

````bash
pysalad report
````

### Buchung Templates

#### Template erstellen

````bash
pysalad --template <Template> --template-duration <Dauer> config save # Dauer im Template speichern
pysalad --template <Template> --template-comment <Kommentar> config save # Kommentar im Template speichern
pysalad --template <Template> --template-order <Auftrag> config save # Auftrag im Template speichern
````

Kommentare können auch Attribute enthalten, die dann beim Erstellen der Buchung per Eingabeaufforderung
eingegeben werden müssen:

````
JIRA-{Ticketnummer} {Kommentar:Standardkommentar}
````


#### Template buchen

Nach dem Erstellen kann mit einem Template gebucht werden:

````bash
pysalad report <Template> # Arbeitszeit mit Template für Heute buchen
````

#### Jira Kommentare

Bei Salat Buchungen mit einem Template kann zusätzlich ein Kommentar in einen Jira Task erstellt werden.
Der Kommentarinhalt und die Jira Task Nummer werden im Template gespeichert:

````bash
pysalad --template <Template> --template-jira-issue <Issue> config save # Jira Issue im Template speichern
pysalad --template <Template> --template-jira-comment <Kommentar> config save # Jira Kommentar im Template speichern
````

Damit pysalad auf Jira zugreifen kann, sollte der Benutzername, ein Personal Access Token (PAT) und
die Jira URL zur Konfiguration hinzugefügt werden:

````bash
pysalad --jira-user <Username> config save # Jira Benutzername speichern
pysalad --jira-token <Personal Access Token> config save # Jira Token speichern
````

Werte, die nicht in der Konfigurationsdatei gespeichert sind, können beim Buchen über die Eingabeaufforderung 
eingegeben werden!

#### Beispiel Templates

````
order = GF2020.02
comment = Daily
duration = 0.5
````

````
order = GF2020.01
comment = GFA-3983 {Kommentar}
jira_issue = GFA-3983
jira_comment = {duration}h {Kommentar}
````

````
order = Wartung & Support
comment = {Kommentar:Betriebsueberwachung}
duration = 0.5
````

### Einstellungen speichern
````bash
pysalad --url <URL> config save # URL speichern
pysalad --user <Mitarbeiterkürzel> config save # eigenes Mitarbeiterkürzel speichern
pysalad --password <Passwort> config save # eigenes Passwort speichern
pysalad --order <Text> config save # mein am häufigsten genutzten Unterauftrag speichern
````

Werte, die nicht in der Konfigurationsdatei gespeichert sind, können beim Buchen über die Eingabeaufforderung
eingegeben werden!

### Einstellungen anzeigen
````bash
pysalad config show
````

Wenn die Einstellungen gespeichert sind, kann man zum Beispiel auf seinen häufigsten Unterauftrag buchen mit:
````bash
pysalad report <Kommentar> <Dauer>
````
