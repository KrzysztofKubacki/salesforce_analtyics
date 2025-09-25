# Salespeople Performance Dashboard (Streamlit, Hellwig, TOPSIS, z-score)

---

## Business Objective

The company needs to compare salespeople across multiple KPIs simultaneously and quickly identify:  
- who delivers results (and in which areas),  
- where the weakest points are (person × region × metric),  
- which corrective actions should be taken.  

---

## Solution

An interactive dashboard built in **Streamlit** with multi-criteria evaluation methods:  
- **z-score** – KPI normalization  
- **Hellwig’s method** – distance from the “ideal benchmark”  
- **TOPSIS** – preference closer to the ideal, farther from the anti-ideal  

Additionally, recommendations are generated per salesperson (based on strong and weak KPIs).  

---

## Key Views & Business Value

1. **Regional heatmap (average z-score per region & KPI)**  
   Highlights which KPIs a region is strong or weak in.  
   “Green” = above average, “red” = below.  
   File: `screenshots/02_regional_heatmap.png`  

2. **Heatmap – all salespeople vs all metrics**  
   Competence matrix showing which salesperson excels or underperforms in each KPI.  
   Useful for targeting training and corrective actions.  
   File: `screenshots/05_salespeople_heatmap.png`  

3. **Radar chart (individual profile)**  
   One view of a salesperson’s KPI profile – instantly shows strengths and weaknesses.  
   File: `screenshots/06_radar_chart.png`  

4. **Rankings (Hellwig + TOPSIS)**  
   Transparent, “fair” multi-criteria ranking – avoids bias toward a single KPI.  
   File: `screenshots/03_SR_ranking.png`  

5. **Recommendations per salesperson**  
   Automatic suggestions on “what to do next” – strengths, weaknesses, and concrete actions.  
   File: `screenshots/07_recommendations.png`  

(For completeness, the repo also contains `01_raw_data.png` and `04_scatter.png`.)  

---

## Repository Structure
```bash
streamlit-salespeople
├── app.py
├── requirements.txt
├── README.md
├── sample_data
│   └── salespeople_performance_sample.xlsx
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

## Data – Expected Columns
Minimum dataset (text columns flexible, others numeric):
- SalespersonID (e.g., S001)
- Region, Month
- VisitsPlanned, VisitsMade, NewClients, Revenue, SalesTarget, OrdersMade
- ResponseTimeDays, CustomerSatisfaction, ComplaintCount, ReturnValue
Additional KPIs are calculated automatically:
- Visit Achievement %, Revenue Achievement, Complaint Rate,
- Refund Rate, Conversion Rate, Average Order Value.

Input format: CSV or XLSX (Excel sheet can be specified).
CSV delimiter is detected automatically (, or ;).

---

## How to Run

# 1) (optional) Virtual envoirnment
```bash
python -m venv .venv
# Windows
.venvScriptsactivate
# macOSLinux
source .venvbinactivate
```
# 2) Install dependencies
```bash
pip install -r requirements.txt
```
# 3) start the app
```bash
streamlit run app.py
```

After launch, upload your file in the sidebar panel (“Upload Excel or CSV with raw data”).

## Methodological Settings (in code)
- Stimulants vs destimulants &rarr; e.g., ResponseTimeDays, ComplaintRate, and RefundRate are reversed in z-score.
- Benchmark vs anti-benchmark &rarr; extreme standardized values.
- Recommendation thresholds &rarr; default: ≥ +1.0 = strong; ≤ −1.0 = weak.

## Why it Works

- z-score normalization eliminates differences in KPI scale.
- Hellwig + TOPSIS evaluate many criteria simultaneously, producing more stable rankings than “single-metric” comparisons.
- Heatmaps and radar charts translate numbers into actionable insights (training, goals, coaching, visit routing).

---

## Author

Project created as a portfolio / CV project – Krzysztof Kubacki
