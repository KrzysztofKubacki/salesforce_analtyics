# Salespeople Performance Dashboard (Streamlit, Hellwig, TOPSIS, z-score)

##  Cel biznesowy
Firma chce porównywać handlowców w wielu KPI jednocześnie i szybko wskazać
- kto dowozi wynik (oraz w czym),
- gdzie są najsłabsze punkty (osobaregionmetryka),
- jakie działania naprawcze wdrożyć.

##  Rozwiązanie
Interaktywny dashboard w Streamlit z metodami wielokryterialnej oceny
- z-score – normalizacja KPI,
- Wskaźnik Hellwiga – odległość od „wzorca idealnego”,
- TOPSIS – preferencja bliżej wzorca, dalej od anty-wzorca.

Dodatkowo generowane są rekomendacje per handlowiec (na podstawie silnychsłabych KPI).

---

##  Najważniejsze widoki i ich wartość

1) Regional heatmap (średni z-score per region & KPI)  
    Szybko pokazuje w których metrykach region jest mocnysłaby.  
   „Zielone” – powyżej średniej, „czerwone” – poniżej.  
   Plik `screenshots02_regional_heatmap.png`

2) Heatmap all salespeople vs all metrics  
    Macierz kompetencji – który handlowiec w których KPI odstaje (na plusminus).  
   Idealna do targetowania szkoleń czy celowanych działań.  
   Plik `screenshots05_salespeople_heatmap.png`

3) Radar chart (profil jednego handlowca)  
    Jedno spojrzenie na profil KPI wybranej osoby. Widać natychmiast, co ciągnie wynik w górę, a co w dół.  
   Plik `screenshots06_radar_chart.png`

4) Rankingi (Hellwig  TOPSIS)  
    Transparentny, „sprawiedliwy” ranking wielokryterialny – nie faworyzuje pojedynczego KPI.  
   Plik `screenshots03_SR_ranking.png`

5) Rekomendacje per handlowiec  
    Automatyczne wskazówki „co robić dalej” mocnesłabe strony + konkretne akcje.  
   Plik `screenshots07_recommendations.png`

(Dla kompletności w repo są też `01_raw_data.png`, `04_scatter.png`.)

---

## Struktura repo
```bash
streamlit-salespeople
├── app.py
├── requirements.txt
├── README.md
├── sample_data
│ └── salespeople_performance_sample.xlsx
└── screenshots
├── 01_raw_data.png
├── 02_regional_heatmap.png
├── 03_SR_ranking.png
├── 04_scatter.png
├── 05_salespeople_heatmap.png
├── 06_radar_chart.png
└── 07_recommendations.png
```

---

## Dane – oczekiwane kolumny
Minimalny zestaw (kolumny tekstowe dowolne, reszta numeryczna)
- `SalespersonID` (np. S001)  
- `Region`, `Month`  
- `VisitsPlanned`, `VisitsMade`, `NewClients`, `Revenue`, `SalesTarget`, `Orders made`  
- `ResponseTimeDays`, `CustomerSatisfaction`, `ComplaintCount`, `Return value`

Aplikacja wylicza dodatkowe KPI  
`Visit Achievement %`, `Revenue Achievement`, `Complaint Rate`, `Refund Rate`, `Conversion Rate`, `Average Order Value`.

Format wejścia CSV lub XLSX (możesz wskazać arkusz).  
Separator CSV wykrywany automatycznie (`,` lub `;`).

---

## Uruchomienie

# 1) (opcjonalnie) środowisko wirtualne
```bash
python -m venv .venv
# Windows
.venvScriptsactivate
# macOSLinux
source .venvbinactivate
```
# 2) zależności
```bash
pip install -r requirements.txt
```
# 3) start aplikacji
```bash
streamlit run app.py
```
Po starcie wczytaj swój plik w panelu bocznym („Upload Excel or CSV with raw data”).

## Ustawienia metodyczne (w kodzie)

Stymulantydestymulanty (np. ResponseTimeDays, Complaint Rate, Refund Rate są odwracane w z-score).

Wzorzecantywzorzec – skrajne wartości po standaryzacji.

Progi do rekomendacji (domyślnie ≥ +1,0 mocna strona; ≤ −1,0 słaba).

## Dlaczego to działa

Normalizacja z-score usuwa różnice skali KPI.

HellwigTOPSIS analizują wiele kryteriów naraz, więc ranking jest stabilniejszy niż „pojedyncza metryka”.

Heatmapy i radar ułatwiają przełożenie liczb na decyzje (szkolenia, cele, coaching, routing wizyt).

---

### Autor

Projekt stworzony jako portfolio / CV project – Krzysztof Kubacki