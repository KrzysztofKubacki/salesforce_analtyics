import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config("Salespeople Analysis Dashboard", layout="wide")
st.title("Salespeople Performance Dashboard (Hellwig, TOPSIS, z-score)")

# --- KPI LABELS & RECOMMENDATIONS ---
KPI_LABELS = {
    "VisitsMade": "Visits Made",
    "NewClients": "New Clients",
    "Revenue": "Revenue",
    "Orders made": "Orders Made",
    "ResponseTimeDays": "Response Time (days)",
    "CustomerSatisfaction": "Customer Satisfaction",
    "Visit Achievement %": "Visit Achievement (%)",
    "Revenue Achievement": "Revenue Achievement",
    "Complaint Rate": "Complaint Rate",
    "Refund Rate": "Refund Rate",
    "Conversion Rate": "Conversion Rate",
    "Average Order Value": "Average Order Value"
}

WEAK_ACTIONS = {
    "VisitsMade": "Increase the number of visits, especially to key clients.",
    "NewClients": "Focus on active acquisition of new clients.",
    "Revenue": "Aim for higher value sales and upselling.",
    "Orders made": "Follow up more to close more deals.",
    "ResponseTimeDays": "Speed up your response time to clients.",
    "CustomerSatisfaction": "Improve communication and after-sales service.",
    "Visit Achievement %": "Plan and execute visits according to schedule.",
    "Revenue Achievement": "Analyze the sales plan and look for ways to meet/exceed it.",
    "Complaint Rate": "Analyze and eliminate the sources of complaints.",
    "Refund Rate": "Identify reasons for refunds and work to minimize them.",
    "Conversion Rate": "Improve effectiveness of sales conversations.",
    "Average Order Value": "Encourage clients to buy higher value products/services."
}

STRONG_ACTIONS = {
    "VisitsMade": "Optimize your routing to increase visit efficiency.",
    "NewClients": "Leverage referral programs and maintain high acquisition rates.",
    "Revenue": "Consider cross-selling and upselling.",
    "Orders made": "Maintain a high close rate.",
    "ResponseTimeDays": "Keep up the fast response – you set a great example.",
    "CustomerSatisfaction": "Collect positive references and testimonials.",
    "Visit Achievement %": "Optimize routes to save time and costs.",
    "Revenue Achievement": "Set new, ambitious sales targets.",
    "Complaint Rate": "Share your best practices for minimizing complaints.",
    "Refund Rate": "Share your approach to reducing refunds.",
    "Conversion Rate": "Share your effective sales techniques with the team.",
    "Average Order Value": "Test upselling for even better results."
}

def calculate_metrics(df):
    agg_dict = {
        'VisitsPlanned': 'sum',
        'VisitsMade': 'sum',
        'NewClients': 'sum',
        'Revenue': 'sum',
        'SalesTarget': 'sum',
        'Orders made': 'sum',
        'ResponseTimeDays': 'sum',
        'CustomerSatisfaction': 'sum',
        'ComplaintCount': 'sum',
        'Return value': 'sum',
        'Region': 'first',
        'Month': 'first'
    }
    agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}
    df_agg = df.groupby('SalespersonID').agg(agg_dict).reset_index()
    # Calculated metrics
    df_agg['Visit Achievement %'] = df_agg['VisitsMade'] / df_agg['VisitsPlanned']
    df_agg['Revenue Achievement'] = df_agg['Revenue'] / df_agg['SalesTarget']
    df_agg['Complaint Rate'] = df_agg['ComplaintCount'] / df_agg['Orders made']
    df_agg['Refund Rate'] = df_agg['Return value'] / df_agg['Revenue']
    df_agg['Conversion Rate'] = df_agg['NewClients'] / df_agg['VisitsMade']
    df_agg['Average Order Value'] = df_agg['Revenue'] / df_agg['Orders made']
    return df_agg

def standardize(df, columns, stimulants):
    scaler = StandardScaler()
    X = scaler.fit_transform(df[columns])
    X = pd.DataFrame(X, columns=columns)
    # Reverse z-score for destimulants
    for col, stim in zip(columns, stimulants):
        if not stim:
            X[col] = -X[col]
    return X

def hellwig_score(df_z, pattern):
    d = np.sqrt(((df_z - pattern) ** 2).sum(axis=1))
    return 1 / (1 + d)

def topsis_score(df_z, pattern, antipattern):
    D_plus = np.sqrt(((df_z - pattern) ** 2).sum(axis=1))
    D_minus = np.sqrt(((df_z - antipattern) ** 2).sum(axis=1))
    return D_minus / (D_plus + D_minus)

def get_recommendations(df_zscore, columns, good=1.0, bad=-1.0):
    recommendations = []
    for idx, row in df_zscore.iterrows():
        sr = row['SalespersonID']
        rec = f"**{sr}**\n"
        strong, weak, actions = [], [], []
        for col in columns:
            label = KPI_LABELS.get(col, col)
            if row[col] >= good:
                strong.append(label)
                actions.append(f"- **{label}**: {STRONG_ACTIONS.get(col, '')}")
            elif row[col] <= bad:
                weak.append(label)
                actions.append(f"- **{label}**: {WEAK_ACTIONS.get(col, '')}")
        if not strong:
            strong.append("No clear strengths")
        if not weak:
            weak.append("No clear weaknesses")
        rec += f"- **Strengths:** {', '.join(strong)}\n"
        rec += f"- **Weaknesses:** {', '.join(weak)}\n"
        rec += f"- **Recommended actions:**\n"
        rec += "\n".join(actions) if actions else "No specific recommendations – keep up the current good work."
        recommendations.append(rec)
    return recommendations

# --- DATA UPLOAD ---
uploaded = st.sidebar.file_uploader("Upload Excel or CSV with raw data", type=["xlsx", "csv"])
if uploaded is not None:
    # Choose sheet if Excel
    if uploaded.name.endswith('.xlsx'):
        xls = pd.ExcelFile(uploaded)
        sheet = st.sidebar.selectbox("Select sheet", xls.sheet_names)
        df_raw = pd.read_excel(xls, sheet)
    else:
        import csv
        first = uploaded.read().decode("utf-8-sig").splitlines()[0]
        sep = ';' if first.count(';') > first.count(',') else ','
        uploaded.seek(0)
        df_raw = pd.read_csv(uploaded, sep=sep, decimal=',', encoding="utf-8")
    st.markdown("#### Raw data preview")
    st.dataframe(df_raw.head(10))

    num_cols = [col for col in df_raw.columns if col not in ['SalespersonID', 'Region', 'Month']]
    for col in num_cols:
        df_raw[col] = pd.to_numeric(df_raw[col].astype(str).str.replace(",", ".", regex=False), errors="coerce")

    # --- METRICS & STIMULANTS ---
    columns = [
        'VisitsMade', 'NewClients', 'Revenue', 'Orders made', 'ResponseTimeDays',
        'CustomerSatisfaction', 'Visit Achievement %', 'Revenue Achievement',
        'Complaint Rate', 'Refund Rate', 'Conversion Rate', 'Average Order Value'
    ]
    stimulants = [
        True, True, True, True,  # VisitsMade, NewClients, Revenue, Orders made
        False, True, True, True, # ResponseTimeDays, CustomerSatisfaction, Visit Ach., Revenue Ach.
        False, False, True, True # Complaint Rate, Refund Rate, Conversion, AOV
    ]

    # --- AGGREGATION & METRICS ---
    df_agg = calculate_metrics(df_raw)
    st.markdown("#### Aggregated metrics per salesperson")
    st.dataframe(df_agg)

    # --- Z-SCORE ---
    df_z = standardize(df_agg, columns, stimulants)
    df_z['SalespersonID'] = df_agg['SalespersonID']
    for col in ['Region', 'Month']:
        if col in df_agg.columns:
            df_z[col] = df_agg[col]

    pattern = df_z[columns].max()
    antipattern = df_z[columns].min()
    df_z['Hellwig_score'] = hellwig_score(df_z[columns], pattern)
    df_z['TOPSIS_score'] = topsis_score(df_z[columns], pattern, antipattern)
    df_z['Hellwig_rank'] = df_z['Hellwig_score'].rank(ascending=False, method='min')
    df_z['TOPSIS_rank'] = df_z['TOPSIS_score'].rank(ascending=False, method='min')

    # --- REGIONAL HEATMAP (GENERAL OVERVIEW) ---
    st.markdown("### Regional analysis (mean z-score per region & metric)")
    if 'Region' in df_z.columns:
        df_region = df_z.groupby("Region")[columns].mean().T
        fig_region, ax_region = plt.subplots(figsize=(12, 4))
        sns.heatmap(df_region, annot=True, center=0, cmap="RdYlGn", ax=ax_region)
        plt.ylabel("Metric")
        plt.xlabel("Region")
        st.pyplot(fig_region)

    # --- BAR CHARTS (Hellwig & TOPSIS ranking) ---
    st.markdown("### Salesperson rankings")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ranking (Hellwig score)")
        fig = px.bar(
            df_z.sort_values('Hellwig_score', ascending=False),
            x="SalespersonID", y="Hellwig_score", color="Hellwig_score"
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Ranking (TOPSIS score)")
        fig = px.bar(
            df_z.sort_values('TOPSIS_score', ascending=False),
            x="SalespersonID", y="TOPSIS_score", color="TOPSIS_score"
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- SCATTER PLOT (any metrics) ---
    st.markdown("### Explore: scatter plot (select any 2 metrics)")
    met1 = st.selectbox("X axis", columns, index=0, key="scatter_x")
    met2 = st.selectbox("Y axis", columns, index=1, key="scatter_y")
    fig3 = px.scatter(
        df_z, x=met1, y=met2, hover_name="SalespersonID", color="Hellwig_score"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # --- HEATMAP Z-SCORE: ALL SALESPEOPLE ---
    st.markdown("### Heatmap: all salespeople vs all metrics")
    fig2, ax = plt.subplots(figsize=(15, 6))
    sns.heatmap(df_z.set_index('SalespersonID')[columns], annot=False, center=0, cmap="RdYlGn", ax=ax)
    st.pyplot(fig2)

    # --- RADAR CHART (single salesperson) ---
    st.markdown("### Radar chart (select salesperson)")
    sr_ids = df_z['SalespersonID'].unique()
    sel_sr = st.selectbox("Select SalespersonID", sr_ids)
    radar_data = df_z.set_index('SalespersonID').loc[sel_sr, columns]
    radar_labels = [KPI_LABELS.get(col, col) for col in columns]
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=radar_data.values,
        theta=radar_labels,
        fill='toself',
        name=sel_sr
    ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[-2.5, 2.5])),
        showlegend=True,
        title=f"Z-score profile: {sel_sr}"
    )
    st.plotly_chart(radar_fig, use_container_width=True)

    # --- RECOMMENDATIONS ---
    st.markdown("### Salesperson recommendations")
    recs = get_recommendations(df_z, columns)
    for rec in recs:
        st.markdown(rec)
else:
    st.info("Upload an Excel or CSV file with salesperson data.")
