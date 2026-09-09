## 1. Vilka var de viktigaste problemen i originalkoden?
Dem viktigaste probem var att hela programmet kördes direkt på modulnivå, vilket gjorde koden svår att testa och återanvända.  
Skriptet blandade flera ansvarsområden, innehöll duplicerad kod och saknade automatiska tester.


## 2. Vilka förändringar tycker du förbättrade programmet mest?
Den största förbättringen var att följa separation of concerns genom att dela upp koden i separata moduler med ett tydligt ansvar.  
Uppdelningen gjorde det möjligt att skriva riktade tester som hjälpte mig upptäcka och förbättra faktiska beteenden i koden. Några exempel på detta är att negativa värden hanteras nu som ogiltiga och fylls med samma standardvärden som saknade värden, samt att en tom dataframe kastar ett ValueError istället för att tyst passera igenom.


## 3. Varför valde du den projektstruktur du använde?
Jag fokuserade på att separera ansvarsområdena i det ursprungliga skriptet för att skapa moduler med tydliga uppgifter:  
`file_handler.py` för att läsa in och spara data, `validation.py` för att rensa och validera den, `processing.py` för att transformera och aggregera den till rapporter, samt `pipeline.py` för att orkestrera dessa steg tillsammans, med `main.py` som startpunkt.  
Jag använde centraliserad loggning så att meddelanden från varje modul kunde konfigureras och följas konsekvent från ett och samma ställe.    
Slutligen strukturerade jag `src/order_report` som ett installerbart paket (med en `pyproject.toml`), vilket höll en tydlig separation mellan källkod och tester, och gjorde det möjligt att importera modulerna på ett rent sätt istället för att förlita sig på relativa sökvägs-lösningar.


## 4. Var använde du OOP/dataclass och varför passade det där?
Jag använde en dataclass (`ReportConfig`) i `config.py` eftersom den bara behövde lagra filsökvägsdata, inte beteende. Jag gjorde den `frozen=True` för att den skulle passa väl som konfiguration: sökvägarna är oföränderliga och kan inte oavsiktligt ändras medan pipelinen körs.


## 5. Vilka viktiga beteenden skyddar dina automatiska tester, och vilken nytta ger testerna om programmet förändras i framtiden?
Mina tester skyddar de viktigaste beräkningarna och felhanteringen i projektet:  
att `order_value` och `discounted_value` beräknas korrekt,  
att sammanfattningarna per kategori och region stämmer,  
att `validate_order_data` fyller i saknade eller ogiltiga värden med rätt standardvärden,  
att programmet kastar tydliga fel vid tom data, saknade kolumner eller ogiltiga inmatningar.  
Nyttan är att jag i framtiden kan ändra eller refaktorera koden och snabbt se om en ändring råkar förändra ett resultat eller ett felbeteende jag inte avsett utan att behöva testa allt manuellt igen.


## 6. Vad var svårast?
Det svåraste var testerna, att förstå vad som faktiskt behövde testas och att stoppa mig själv från att testa varje liten detalj.


## 7. Vad hade du velat förbättra ytterligare om du haft mer tid?
Om jag hade haft mer tid hade jag velat förbättra valideringslogiken, till exempel genom att göra gränsvärdena konfigurerbara.  
Jag hade också velat lägga till radnivå-rapportering, så att man kan se exakt vilka rader eller `order_id` som fick sina värden ersatta med standardvärden. Det skulle göra det lättare att upptäcka systematiska datakvalitetsproblem i källdatan.