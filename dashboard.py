import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Telecom Analytics Dashboard",
    page_icon="📡",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

df = pd.read_excel("data/telecom_data_1200_rows.xlsx")

df["Connection_Date"] = pd.to_datetime(df["Connection_Date"])

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📡 AI Telecom Analytics")

district = st.sidebar.selectbox(
    "Select District",
    ["All"] + sorted(df["District"].unique().tolist())
)

status = st.sidebar.selectbox(
    "Select Status",
    ["All"] + sorted(df["Status"].unique().tolist())
)

if district != "All":
    df = df[df["District"] == district]

if status != "All":
    df = df[df["Status"] == status]

# ---------------- TITLE ---------------- #

st.title("📡 AI Telecom Analytics Dashboard")
st.markdown("### Smart Telecom Connection & Disconnection Analysis")

# ---------------- KPI SECTION ---------------- #

total_connections = len(df)

active_connections = len(
    df[df["Status"] == "Active"]
)

disconnected_connections = len(
    df[df["Status"] == "Disconnected"]
)

total_revenue = df["Monthly_Bill"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Connections",
    total_connections
)

c2.metric(
    "Active Connections",
    active_connections
)

c3.metric(
    "Disconnected",
    disconnected_connections
)

c4.metric(
    "Revenue",
    f"₹{total_revenue:,.0f}"
)

st.divider()

# ---------------- NETWORK HEALTH ---------------- #

st.subheader("📶 Network Health Score")

signal_map = {
    "Excellent": 5,
    "Good": 4,
    "Average": 3,
    "Poor": 2,
    "Very Poor": 1
}

temp_df = df.copy()

if temp_df["Signal_Strength"].dtype == object:
    temp_df["Signal_Score"] = (
        temp_df["Signal_Strength"]
        .map(signal_map)
        .fillna(3)
    )
else:
    temp_df["Signal_Score"] = temp_df["Signal_Strength"]

temp_df["Signal_Score"] = pd.to_numeric(
    temp_df["Signal_Score"],
    errors="coerce"
)

avg_signal = temp_df["Signal_Score"].mean()

if pd.isna(avg_signal):
    avg_signal = 0
avg_complaints = temp_df["Complaint_Count"].mean()

health_score = max(
    0,
    min(
        100,
        round((avg_signal * 20) - (avg_complaints * 5))
    )
)

st.progress(health_score / 100)

st.metric(
    "Network Health",
    f"{health_score}%"
)

# ---------------- AREA ANALYSIS ---------------- #

st.subheader("📍 Area-wise Connections")

area_count = (
    df["Area"]
    .value_counts()
    .reset_index()
)

area_count.columns = [
    "Area",
    "Connections"
]

fig_area = px.bar(
    area_count,
    x="Area",
    y="Connections",
    color="Connections"
)

st.plotly_chart(
    fig_area,
    width="stretch"
)

# ---------------- DISTRICT ANALYSIS ---------------- #

st.subheader("🏙 District-wise Connections")

district_count = (
    df["District"]
    .value_counts()
    .reset_index()
)

district_count.columns = [
    "District",
    "Connections"
]

fig_district = px.bar(
    district_count,
    x="District",
    y="Connections",
    color="Connections"
)

st.plotly_chart(
    fig_district,
    width="stretch"
)

# ---------------- DISCONNECTION ANALYSIS ---------------- #

st.subheader("❌ Disconnection Analysis")

disc_df = df[
    df["Status"] == "Disconnected"
]

if len(disc_df) > 0:

    reason_count = (
        disc_df["Disconnection_Reason"]
        .value_counts()
        .reset_index()
    )

    reason_count.columns = [
        "Reason",
        "Count"
    ]

    fig_reason = px.pie(
        reason_count,
        names="Reason",
        values="Count"
    )

    st.plotly_chart(
        fig_reason,
        width="stretch"
    )

# ---------------- CONNECTION TYPE ---------------- #

st.subheader("📡 Connection Type")

fig_type = px.pie(
    df,
    names="Connection_Type"
)

st.plotly_chart(
    fig_type,
    width="stretch"
)

# ---------------- PAYMENT STATUS ---------------- #

st.subheader("💰 Payment Status")

fig_payment = px.pie(
    df,
    names="Payment_Status"
)

st.plotly_chart(
    fig_payment,
    width="stretch"
)

# ---------------- SIGNAL ANALYSIS ---------------- #

st.subheader("📶 Signal Strength")

signal_count = (
    df["Signal_Strength"]
    .value_counts()
    .reset_index()
)

signal_count.columns = [
    "Signal",
    "Count"
]

fig_signal = px.bar(
    signal_count,
    x="Signal",
    y="Count",
    color="Signal"
)

st.plotly_chart(
    fig_signal,
    width="stretch"
)

# ---------------- COMPLAINT ANALYSIS ---------------- #

st.subheader("🚨 Complaint Analysis")

fig_complaint = px.histogram(
    df,
    x="Complaint_Count",
    nbins=10
)

st.plotly_chart(
    fig_complaint,
    width="stretch"
)

# ---------------- REVENUE ANALYSIS ---------------- #

st.subheader("💵 Revenue by Area")

revenue_area = (
    df.groupby("Area")["Monthly_Bill"]
    .sum()
    .reset_index()
)

fig_revenue = px.bar(
    revenue_area,
    x="Area",
    y="Monthly_Bill",
    color="Monthly_Bill"
)

st.plotly_chart(
    fig_revenue,
    width="stretch"
)

# ---------------- DISTRICT REVENUE ---------------- #

st.subheader("🏆 District Revenue Ranking")

district_revenue = (
    df.groupby("District")["Monthly_Bill"]
    .sum()
    .reset_index()
)

fig_dist_rev = px.bar(
    district_revenue,
    x="District",
    y="Monthly_Bill",
    color="Monthly_Bill"
)

st.plotly_chart(
    fig_dist_rev,
    width="stretch"
)

# ---------------- CONNECTION TREND ---------------- #

st.subheader("📈 Monthly Connection Trend")

monthly_connections = (
    df.groupby(
        df["Connection_Date"]
        .dt.to_period("M")
    )
    .size()
    .reset_index(name="Connections")
)

monthly_connections["Connection_Date"] = (
    monthly_connections["Connection_Date"]
    .astype(str)
)

fig_trend = px.line(
    monthly_connections,
    x="Connection_Date",
    y="Connections",
    markers=True
)

st.plotly_chart(
    fig_trend,
    width="stretch"
)

# ---------------- CUSTOMER RISK ---------------- #

st.subheader("🤖 Customer Risk Analysis")

risk_df = df[
    df["Complaint_Count"] >= 3
]

st.metric(
    "High Risk Customers",
    len(risk_df)
)

st.dataframe(
    risk_df[
        [
            "Customer_ID",
            "Area",
            "Complaint_Count",
            "Signal_Strength",
            "Payment_Status"
        ]
    ],
    width="stretch"
)

# ---------------- MAP ---------------- #

st.subheader("🗺 Telecom Connection Map")

map_df = df[
    ["Latitude", "Longitude"]
].copy()

map_df.columns = [
    "latitude",
    "longitude"
]

st.map(map_df)

# ---------------- TOP PROBLEM AREAS ---------------- #

st.subheader("⚠ Top Complaint Areas")

problem_areas = (
    df.groupby("Area")
    ["Complaint_Count"]
    .sum()
    .reset_index()
    .sort_values(
        by="Complaint_Count",
        ascending=False
    )
)

st.dataframe(
    problem_areas.head(10),
    width="stretch"
)

# ---------------- EXECUTIVE SUMMARY ---------------- #

st.subheader("📊 Executive Summary")

top_area = (
    df["Area"]
    .value_counts()
    .idxmax()
)

worst_area = (
    df.groupby("Area")
    ["Complaint_Count"]
    .sum()
    .idxmax()
)

st.info(
    f"""
Top Connection Area : {top_area}

Highest Complaint Area : {worst_area}

Total Revenue : ₹{total_revenue:,.0f}

Total Customers : {len(df)}
"""
)

# ---------------- DATASET ---------------- #

st.subheader("📄 Telecom Dataset")

st.dataframe(
    df,
    width="stretch"
)

# ---------------- FOOTER ---------------- #

st.divider()

st.markdown(
    "### 🚀 Developed by Arun"
)

st.markdown(
    "AI Telecom Analytics Dashboard"
)
