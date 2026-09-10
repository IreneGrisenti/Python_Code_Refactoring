# Kodgranskning av order_report.py

## Sammanfattning
Skriptet skapar korrekt de tänkta rapporterna, men arkitekturen följer inte grundläggande principer för separation av ansvar, DRY-kod och tydlig felhantering.  
Koden är dessutom svår att testa automatiskt eftersom hela programmet körs vid import.

## Observationer
### Obs 1 - Hela programmet körs på modulnivå

**Observation** - Hela programflödet (inläsning, bearbetning, beräkningar och filsparning) körs direkt i modulens toppnivå.

**Konsekvens** - Att importera filen räcker för att köra hela programmet, inklusive läsa och skriva filer.  
Koden går inte att återanvända eller testa i isolerade delar.

**Förslag** - Samla programlogiken i en `main()`-funktion och kör den bakom ett main-guard.


### Obs 2 - Sökvägar är hårdkodade

**Observation** - `INPUT_FILE` och `OUTPUT_FOLDER` är hårdkodade konstanter i skriptet, och `OUTPUT_FOLDER` antas redan finnas.

**Konsekvens** - Programmet kan bara köras med exakt de sökvägarna. Det går inte att enkelt testa med tillfälliga filer, och programmet kraschar om outputmappen inte redan finns.

**Förslag** - Samla sökvägarna i en `config.py`, till exempel som standardvärden i en dataclass. På så sätt finns sökvägarna definierade på ett ställe och är enkla att hitta, men de blir samtidigt lättare att skapa ett annat objek med andra värden vid behov. Låt dessutom sparfunktioner skapa målmappen vid behov.


### Obs 3 - Statusmeddelanden använder print()

**Observation** - `print()` används för att beskriva programsteg: start, inläsning av data, sparande av dokument samt avslutning.

**Konsekvens** - `print()`-utskrifter saknar allvarlighetsnivå, kan inte enkelt konfigureras, filtreras eller skickas till en fil, och det syns inte vilken del av programmet som skrev ut meddelandet.

**Förslag** - Använd modulens `logging`, med en logger per modul och central konfiguration i programmets startpunkt.


### Obs 4 - Felhantering är otydlig och för bred

**Observation** - Valideringen kastar en generisk `Exception("Fel data")` om kolumner saknas, och hela programmet ligger i ett enda try/except Exception-block som skriver ut `"Något gick fel:"` oavsett orsak.

**Konsekvens** - Användaren får inte veta vilka kolumner som faktiskt saknas, eller vad som konkret gick fel längre ner i programmet. Felsökning blir onödigt svår.

**Förslag** - Kasta specifika, beskrivande fel (t.ex. vilka kolumner som saknas) och fånga specifika undantagstyper istället för Exception brett, så att data­fel och kodfel kan hanteras och rapporteras olika.


### Obs 5 - Skriptet blandar flera ansvarsområden

**Observation:** Samma skript hanterar filinläsning, kolumnvalidering, datarensning, beräkningar, aggregering till rapporter och filsparning, allt i samma körning utan tydlig uppdelning.

**Konsekvens:** Delarna går inte att testa eller återanvända var för sig. En liten ändring i riskerar att påverka kod långt bort i samma fil och det är svårt att förstå programmet i sin helhet.

**Förslag:** Dela upp koden i tydligt avgränsade delar, t.ex. inläsning, rensning/transformation, aggregering/rapportering och orkestrering i separata funktioner eller moduler.


### Obs 6 - Otydliga variabelnamn

**Observation:** Variabler som `result1` och `result2` namnger inte vad de faktiskt innehåller.

**Konsekvens:** Läsaren måste läsa resterande koden för att förstå vad variabeln representerar, istället för att kunna lita på namnet.

**Förslag:** Byt till namn som beskriver innehållet, t.ex. `sales_by_category` och `sales_by_region`.


### Obs 7 - Duplicerad kod i rapportgenereringen

**Observation:** `result1`, `result2` och `returns_by_category` följer samma mönster: `groupby(...).agg(...)`, beräkning av `return_rate`, sortering och sparning till CSV.  
Det som faktiskt skiljer dem åt är vilken kolumn de grupperar på, vilka kolumner som aggregeras och vilken kolumn resultatet sorteras på.

**Konsekvens:** Samma logik är skriven ut tre gånger med små variationer, vilket bryter mot DRY-principen. En ändring i hur en rapport beräknas måste göras på tre ställen och risken för att missa ett av dem är hög.

**Förslag:** Bryt ut mönstret till en återanvändbar funktion eller metod på en rapport-/summeringsklass som tar grupperingskolumn, aggregeringar och sorteringskolumn som parametrar.


### Obs 8 - Inga automatiska tester

**Observation:** Programmet har inga tester alls. Det enda sättet att kontrollera att det fungerar är att köra det manuellt och läsa utskrifterna.

**Konsekvens:** Det går inte att snabbt verifiera att en ändring inte råkar förändra beräkningarna, vilket gör framtida underhåll och refaktorering riskabelt.

**Förslag:** När logiken är uppdelad i mindre, testbara funktioner, skriv `pytest`-tester för t.ex. beräkning av ordervärde, hantering av saknade värden och att valideringen kastar rätt fel vid saknade kolumner.
