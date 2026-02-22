import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Loan Risk Dashboard", page_icon="💳", layout="wide")

# ── STYLE ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #071a0f !important;
    }
    .stApp {
        background: radial-gradient(ellipse at top left, #0d2b18 0%, #071a0f 50%, #030f08 100%);
        background-attachment: fixed;
    }
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        background: transparent;
    }
    /* Collapse default Streamlit gaps */
    .element-container { margin-bottom: 0 !important; }
    [data-testid="stVerticalBlock"] > div { gap: 0 !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0.75rem !important; }
    .element-container:has(hr) {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Metrics */
    [data-testid="stMetricLabel"] { font-size: 13px !important; color: #52a871 !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #d4f5e2 !important; }
    [data-testid="stMetricDelta"] { font-size: 12px !important; }
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #0d2b18, #0a2014);
        border: 1px solid #1a4d2e;
        border-radius: 10px;
        padding: 14px 16px 10px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        transition: border-color 0.2s ease;
    }
    [data-testid="metric-container"]:hover { border-color: #39d98a; }

    /* Section titles */
    .block-title {
        font-size: 16px; font-weight: 700; color: #d4f5e2;
        padding: 6px 12px;
        background: linear-gradient(90deg, #0d2b18, #071a0f);
        border-left: 4px solid #39d98a;
        border-radius: 4px; margin-bottom: 12px;
    }

    /* Hint boxes */
    .hint {
        font-size: 12px; color: #3a7a55; margin-top: 6px;
        padding: 6px 10px;
        background: #071a0f;
        border: 1px solid #122b1c;
        border-radius: 4px;
    }

    /* Dividers */
    hr { border-color: #122b1c !important; margin: 0.3rem 0 !important; }

    /* Selectboxes */
    [data-testid="stSelectbox"] > div > div {
        background: #0d2b18 !important;
        border: 1px solid #1a4d2e !important;
        border-radius: 8px !important;
        color: #d4f5e2 !important;
    }
    [data-testid="stSelectbox"] label { color: #52a871 !important; font-size: 13px !important; }

    /* Caption & scrollbar */
    .stCaption { color: #2a5c3c !important; font-size: 11px !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #071a0f; }
    ::-webkit-scrollbar-thumb { background: #1a4d2e; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #39d98a; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Loan_default_clean.csv")
    return df

df = load_data()

# ── COLORS ─────────────────────────────────────────────────────────────────────
PURPOSE_COLORS = {
    "Home": "#39d98a", "Auto": "#5bc8f5",
    "Education": "#f5c542", "Business": "#f0954a", "Other": "#a07af0",
}
RISK_COLORS = {"Low": "#39d98a", "Medium": "#f5c542", "High": "#f05454"}

SAFE = "#39d98a"
MID  = "#f5c542"
HIGH = "#f05454"

C = dict(
    paper_bgcolor="#0a2014",
    plot_bgcolor="#071a0f",
    font=dict(color="#d4f5e2", size=13, family="Segoe UI"),
    margin=dict(t=40, b=20, l=10, r=10),
    title_font=dict(size=15, color="#d4f5e2"),
)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("## 💳 Loan Risk Dashboard")

# ── FILTERS ────────────────────────────────────────────────────────────────────
f1, f2, f3 = st.columns(3)
with f1:
    purpose_filter = st.selectbox(
        "Loan Purpose",
        ["All"] + sorted(df["LoanPurpose"].unique().tolist()),
        help="Filter all charts by the reason the loan was taken. Example: select 'Business' to see only business loans."
    )
with f2:
    emp_filter = st.selectbox(
        "Employment Type",
        ["All"] + sorted(df["EmploymentType"].unique().tolist()),
        help="Filter by the borrower's job status. Unemployed borrowers have the highest default rate."
    )
with f3:
    risk_filter = st.selectbox(
        "Risk Tier",
        ["All", "Low", "Medium", "High"],
        help="Low = safe borrowers (score 0–2). Medium = some risk factors (score 3–5). High = multiple red flags (score 6+)."
    )

# ── APPLY FILTERS ──────────────────────────────────────────────────────────────
filtered = df.copy()
if purpose_filter != "All":
    filtered = filtered[filtered["LoanPurpose"] == purpose_filter]
if emp_filter != "All":
    filtered = filtered[filtered["EmploymentType"] == emp_filter]
if risk_filter != "All":
    filtered = filtered[filtered["RiskTier"] == risk_filter]

# ── CALCULATIONS ───────────────────────────────────────────────────────────────
total        = len(filtered)
defaults     = int(filtered["Default"].sum())
default_rate = (defaults / total * 100) if total else 0
avg_credit   = filtered["CreditScore"].mean()
avg_dti      = filtered["DTIRatio"].mean()
avg_lti      = filtered["LTIRatio"].mean()
risk_counts  = filtered["RiskTier"].value_counts()
high_pct     = risk_counts.get("High", 0) / total * 100 if total else 0

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PORTFOLIO HEALTH
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="block-title">📊 Portfolio Health</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.metric("Total Loans", f"{total:,}",
              help="Total number of loans in the current filtered view.")
with k2:
    st.metric("Default Rate", f"{default_rate:.1f}%",
              delta="Critical" if default_rate > 20 else "Watch" if default_rate > 12 else "Healthy",
              delta_color="inverse" if default_rate > 12 else "normal",
              help="How many loans failed out of 100. Below 12% = healthy. Above 12% = watch. Above 20% = critical.")
with k3:
    st.metric("Avg Credit Score", f"{avg_credit:.0f}",
              delta="Risky — below 670" if avg_credit < 670 else "Safe — above 670",
              delta_color="inverse" if avg_credit < 670 else "normal",
              help="Average credit score. Scale is 300–850. The safe line is 670 — below it default rates rise sharply.")
with k4:
    st.metric("Avg DTI Ratio", f"{avg_dti:.2f}",
              delta="Risky — above 0.5" if avg_dti > 0.5 else "Safe — below 0.5",
              delta_color="inverse" if avg_dti > 0.5 else "normal",
              help="DTI = Debt-to-Income. How much of monthly income already goes to debt payments. Above 0.5 is dangerous.")
with k5:
    st.metric("Avg LTI Ratio", f"{avg_lti:.2f}",
              delta="Overextended — above 4" if avg_lti > 4 else "Manageable",
              delta_color="inverse" if avg_lti > 4 else "normal",
              help="LTI = Loan-to-Income. Loan amount divided by annual income. Above 4 means borrower is very stretched.")
with k6:
    st.metric("High Risk Loans", f"{high_pct:.1f}%",
              delta=f"{risk_counts.get('High', 0):,} loans in danger",
              delta_color="inverse" if high_pct > 25 else "off",
              help="Percentage scored as High Risk using DTI + Credit Score + Employment + LTI + Co-Signer. Above 25% is serious.")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — WHICH LOAN TYPE IS THE PROBLEM?
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="block-title">🏦 Which Loan Type Is the Problem?</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    purpose_stats = filtered.groupby("LoanPurpose").agg(
        Count=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    purpose_stats["DefaultRate"] = (purpose_stats["Defaults"] / purpose_stats["Count"] * 100).round(1)
    purpose_stats = purpose_stats.sort_values("DefaultRate", ascending=True)

    bar_colors = [HIGH if r > 20 else MID if r > 12 else SAFE for r in purpose_stats["DefaultRate"]]

    fig1 = go.Figure(go.Bar(
        x=purpose_stats["DefaultRate"],
        y=purpose_stats["LoanPurpose"],
        orientation="h",
        marker_color=bar_colors,
        marker_line=dict(width=0),
        text=[f"{r:.1f}%  ({c:,} loans)" for r, c in zip(purpose_stats["DefaultRate"], purpose_stats["Count"])],
        textposition="outside",
        textfont=dict(size=13, color="#d4f5e2"),
    ))
    fig1.add_vline(x=12, line_dash="dash", line_color=MID,
                   annotation_text="Watch (12%)", annotation_position="top right",
                   annotation_font=dict(color=MID, size=11))
    fig1.add_vline(x=20, line_dash="dash", line_color=HIGH,
                   annotation_text="Critical (20%)", annotation_position="top right",
                   annotation_font=dict(color=HIGH, size=11))
    fig1.update_layout(
        **C, title="Default Rate by Loan Purpose",
        xaxis=dict(title="Default Rate %", gridcolor="#122b1c", range=[0, 40]),
        yaxis=dict(title=""), height=320,
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('<div class="hint">Green = healthy &nbsp;|&nbsp; Amber = watch &nbsp;|&nbsp; Red = critical &nbsp;|&nbsp; Dashed lines show thresholds</div>', unsafe_allow_html=True)

with col2:
    fc = filtered.copy()
    fc["DTIBucket"] = pd.cut(fc["DTIRatio"],
        bins=[0, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0],
        labels=["Very Low", "Low", "Moderate", "High", "Very High", "Extreme"])
    fc["LTIBucket"] = pd.cut(fc["LTIRatio"].clip(upper=10),
        bins=[0, 1, 2, 4, 6, 10],
        labels=["Very Low", "Low", "Moderate", "High", "Extreme"])

    bubble_data = fc.groupby(["DTIBucket", "LTIBucket"], observed=True).agg(
        TotalLoans=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    bubble_data["DefaultRate"] = (bubble_data["Defaults"] / bubble_data["TotalLoans"] * 100).round(1)

    fig2 = px.scatter(
        bubble_data, x="DTIBucket", y="LTIBucket",
        size="TotalLoans", color="DefaultRate",
        color_continuous_scale=[SAFE, MID, HIGH],
        hover_data={"DTIBucket": True, "LTIBucket": True,
                    "TotalLoans": True, "Defaults": True, "DefaultRate": True},
        size_max=40,
    )
    fig2.update_layout(
        **C, title="Loan Risk Bubble — DTI vs LTI",
        xaxis=dict(title="DTI Level (Debt vs Income)  →  Higher = More Risk", tickfont=dict(size=12), gridcolor="#122b1c"),
        yaxis=dict(title="LTI Level (Loan vs Income)  ↑  Higher = More Risk", tickfont=dict(size=12), gridcolor="#122b1c"),
        height=360, coloraxis_colorbar=dict(title="Default %")
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="hint">Bubble size = number of loans &nbsp;|&nbsp; Color = default rate &nbsp;|&nbsp; Top-right = highest risk group</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — WHO IS THE RISKY BORROWER?
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="block-title">👤 Who Is the Risky Borrower?</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    fc2 = filtered.copy()
    fc2["CreditBand"] = pd.cut(fc2["CreditScore"],
        bins=[300, 500, 580, 670, 740, 851],
        labels=["300–500", "500–580", "580–670", "670–740", "740–850"])
    credit_stats = fc2.groupby("CreditBand", observed=True).agg(
        Total=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    credit_stats["DefaultRate"] = (credit_stats["Defaults"] / credit_stats["Total"] * 100).round(1)

    dot_colors = [HIGH if r > 20 else MID if r > 12 else SAFE for r in credit_stats["DefaultRate"]]

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=credit_stats["CreditBand"].astype(str),
        y=credit_stats["DefaultRate"],
        mode="lines+markers+text",
        line=dict(color="#1a5e35", width=3, shape="spline"),
        marker=dict(size=14, color=dot_colors, line=dict(color="white", width=2)),
        text=credit_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
        textposition="top center",
        textfont=dict(size=13, color="#d4f5e2"),
    ))
    fig3.add_hrect(y0=0,  y1=12, fillcolor=SAFE, opacity=0.05, line_width=0)
    fig3.add_hrect(y0=12, y1=20, fillcolor=MID,  opacity=0.05, line_width=0)
    fig3.add_hrect(y0=20, y1=50, fillcolor=HIGH,  opacity=0.05, line_width=0)
    fig3.add_hline(y=12, line_dash="dash", line_color=MID,
                   annotation_text="Watch", annotation_font=dict(color=MID, size=11))
    fig3.add_hline(y=20, line_dash="dash", line_color=HIGH,
                   annotation_text="Critical", annotation_font=dict(color=HIGH, size=11))
    fig3.update_layout(
        **C, title="Default Rate Drops as Credit Score Rises",
        xaxis=dict(title="Credit Score Band", tickfont=dict(size=12), gridcolor="#122b1c"),
        yaxis=dict(title="Default Rate %", gridcolor="#122b1c", range=[0, 50]),
        height=340,
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="hint">The line drops sharply after 670 — this is your approval threshold. Below it = high risk.</div>', unsafe_allow_html=True)

with col4:
    emp_stats = filtered.groupby("EmploymentType").agg(
        Total=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    emp_stats["DefaultRate"] = (emp_stats["Defaults"] / emp_stats["Total"] * 100).round(1)
    emp_stats = emp_stats.sort_values("DefaultRate", ascending=False)

    emp_colors = [HIGH if r > 20 else MID if r > 12 else SAFE for r in emp_stats["DefaultRate"]]

    fig4 = go.Figure(go.Bar(
        x=emp_stats["EmploymentType"],
        y=emp_stats["DefaultRate"],
        marker_color=emp_colors,
        marker_line=dict(width=0),
        text=emp_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
        textfont=dict(size=14, color="#d4f5e2"),
        width=0.5,
    ))
    fig4.add_hline(y=12, line_dash="dash", line_color=MID,
                   annotation_text="Watch (12%)", annotation_font=dict(color=MID, size=11))
    fig4.add_hline(y=20, line_dash="dash", line_color=HIGH,
                   annotation_text="Critical (20%)", annotation_font=dict(color=HIGH, size=11))
    fig4.update_layout(
        **C, title="Default Rate by Employment Type",
        xaxis=dict(title="", tickfont=dict(size=13), gridcolor="#122b1c"),
        yaxis=dict(title="Default Rate %", gridcolor="#122b1c", range=[0, 55]),
        height=340,
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('<div class="hint">Unemployed borrowers default roughly 3x more than full-time borrowers</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — TWO QUICK WINS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="block-title">💡 Two Quick Wins to Reduce Defaults</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    cs = filtered.groupby(["LoanPurpose", "HasCoSigner"]).agg(
        Total=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    cs["DefaultRate"] = (cs["Defaults"] / cs["Total"] * 100).round(1)

    with_cs    = cs[cs["HasCoSigner"] == "Yes"].set_index("LoanPurpose")["DefaultRate"]
    without_cs = cs[cs["HasCoSigner"] == "No"].set_index("LoanPurpose")["DefaultRate"]
    purposes   = sorted(filtered["LoanPurpose"].unique())

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        name="With Co-Signer", x=purposes,
        y=[with_cs.get(p, 0) for p in purposes],
        marker_color=SAFE, marker_line=dict(width=0),
        text=[f"{with_cs.get(p,0):.1f}%" for p in purposes],
        textposition="outside", textfont=dict(size=12, color="#d4f5e2"),
    ))
    fig5.add_trace(go.Bar(
        name="Without Co-Signer", x=purposes,
        y=[without_cs.get(p, 0) for p in purposes],
        marker_color=HIGH, marker_line=dict(width=0),
        text=[f"{without_cs.get(p,0):.1f}%" for p in purposes],
        textposition="outside", textfont=dict(size=12, color="#d4f5e2"),
    ))
    fig5.update_layout(
        **C, title="Co-Signer Cuts Default Rate — by Loan Purpose",
        barmode="group",
        xaxis=dict(title="", tickfont=dict(size=12), gridcolor="#122b1c"),
        yaxis=dict(title="Default Rate %", gridcolor="#122b1c", range=[0, 40]),
        legend=dict(bgcolor="#0a2014", font=dict(size=12), bordercolor="#1a4d2e", borderwidth=1),
        height=360,
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('<div class="hint">Green bars are always lower than red bars — co-signer reduces risk in every loan type</div>', unsafe_allow_html=True)

with col6:
    edu_order = ["PhD", "Master's", "Bachelor's", "High School"]
    edu_stats = filtered.groupby("Education").agg(
        Total=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    edu_stats["DefaultRate"] = (edu_stats["Defaults"] / edu_stats["Total"] * 100).round(1)
    edu_stats["Education"]   = pd.Categorical(edu_stats["Education"], categories=edu_order, ordered=True)
    edu_stats = edu_stats.sort_values("Education")

    dot_colors = [HIGH if r > 20 else MID if r > 12 else SAFE for r in edu_stats["DefaultRate"]]

    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=edu_stats["Education"].astype(str), y=edu_stats["DefaultRate"],
        mode="lines", line=dict(color="#1a4d2e", width=3), showlegend=False,
    ))
    fig6.add_trace(go.Scatter(
        x=edu_stats["Education"].astype(str), y=edu_stats["DefaultRate"],
        mode="markers+text",
        marker=dict(size=22, color=dot_colors, line=dict(color="white", width=2)),
        text=edu_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
        textposition="top center", textfont=dict(size=13, color="#d4f5e2"),
        showlegend=False,
    ))
    for _, row in edu_stats.iterrows():
        fig6.add_annotation(
            x=str(row["Education"]), y=row["DefaultRate"] - 3.5,
            text=f"{row['Total']:,} loans", showarrow=False,
            font=dict(size=11, color="#3a7a55"),
        )
    fig6.add_hrect(y0=0,  y1=12, fillcolor=SAFE, opacity=0.05, line_width=0)
    fig6.add_hrect(y0=12, y1=20, fillcolor=MID,  opacity=0.05, line_width=0)
    fig6.add_hrect(y0=20, y1=50, fillcolor=HIGH,  opacity=0.05, line_width=0)
    fig6.update_layout(
        **C, title="Default Rate by Education Level",
        xaxis=dict(title="", tickfont=dict(size=13), gridcolor="#122b1c"),
        yaxis=dict(title="Default Rate %", gridcolor="#122b1c", range=[0, 45]),
        height=360,
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('<div class="hint">Each dot = one education group &nbsp;|&nbsp; Green = safe &nbsp;|&nbsp; Red = high risk &nbsp;|&nbsp; Number below = loan count</div>', unsafe_allow_html=True)

st.caption("Loan Risk Dashboard · Source: Loan_default_clean.csv · Preprocessed by data_preprocessing.py")
