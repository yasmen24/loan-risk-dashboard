# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import plotly.graph_objects as go

# # # ── PAGE CONFIG ────────────────────────────────────────────────────────────────
# # st.set_page_config(page_title="Loan Risk Dashboard", page_icon="💳", layout="wide")

# # # ── GLOBAL FONT STYLE ──────────────────────────────────────────────────────────
# # st.markdown("""
# # <style>
# #     html, body, [class*="css"] {
# #         font-family: 'Segoe UI', sans-serif;
# #         font-size: 15px;
# #     }
# #     h1 { font-size: 2rem !important; }
# #     h2 { font-size: 1.6rem !important; }
# #     h3 { font-size: 1.3rem !important; }
# #     h4 { font-size: 1.1rem !important; }
# #     [data-testid="stMetricLabel"] {
# #         font-size: 14px !important;
# #         font-weight: 600 !important;
# #         color: #a0aec0 !important;
# #     }
# #     [data-testid="stMetricValue"] {
# #         font-size: 26px !important;
# #         font-weight: 700 !important;
# #     }
# #     [data-testid="stMetricDelta"] {
# #         font-size: 13px !important;
# #     }
# #     .section-label {
# #         font-size: 11px;
# #         font-weight: 700;
# #         letter-spacing: 0.12em;
# #         text-transform: uppercase;
# #         color: #718096;
# #         margin-bottom: 2px;
# #     }
# #     .section-title {
# #         font-size: 20px;
# #         font-weight: 700;
# #         color: #e8eef6;
# #         margin-bottom: 4px;
# #     }
# #     .section-desc {
# #         font-size: 13px;
# #         color: #718096;
# #         margin-bottom: 16px;
# #     }
# #     .insight-box {
# #         background: #1a202c;
# #         border-left: 3px solid #00d4aa;
# #         border-radius: 6px;
# #         padding: 10px 14px;
# #         font-size: 13px;
# #         color: #a0aec0;
# #         margin-top: 8px;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # ── LOAD DATA ──────────────────────────────────────────────────────────────────
# # @st.cache_data
# # def load_data():
# #     df = pd.read_csv("Loan_default.csv")
# #     df["LTIRatio"] = (df["LoanAmount"] / df["Income"]).round(2)

# #     def risk_tier(row):
# #         score = 0
# #         if row["DTIRatio"] > 0.5:                 score += 2
# #         if row["CreditScore"] < 580:              score += 2
# #         if row["CreditScore"] < 670:              score += 1
# #         if row["EmploymentType"] == "Unemployed": score += 3
# #         if row["EmploymentType"] == "Part-time":  score += 1
# #         if row["LTIRatio"] > 4:                   score += 2
# #         if row["HasCoSigner"] == "Yes":           score -= 1
# #         if score <= 2:   return "Low"
# #         elif score <= 5: return "Medium"
# #         else:            return "High"

# #     df["RiskTier"] = df.apply(risk_tier, axis=1)
# #     return df

# # df = load_data()

# # # ── COLORS ─────────────────────────────────────────────────────────────────────
# # PURPOSE_COLORS = {
# #     "Home":      "#00d4aa",
# #     "Auto":      "#4f9eff",
# #     "Education": "#ffc145",
# #     "Business":  "#ff6b35",
# #     "Other":     "#b06bff",
# # }
# # PURPOSE_COLORS_LIGHT = {
# #     "Home":      "rgba(0,212,170,0.3)",
# #     "Auto":      "rgba(79,158,255,0.3)",
# #     "Education": "rgba(255,193,69,0.3)",
# #     "Business":  "rgba(255,107,53,0.3)",
# #     "Other":     "rgba(176,107,255,0.3)",
# # }
# # RISK_COLORS = {
# #     "Low":    "#00d4aa",
# #     "Medium": "#ffc145",
# #     "High":   "#ff4560"
# # }
# # CHART_STYLE = dict(
# #     paper_bgcolor="#0e1117",
# #     plot_bgcolor="#0e1117",
# #     font=dict(color="#e8eef6", size=13, family="Segoe UI"),
# #     margin=dict(t=50, b=40, l=10, r=10),
# #     title_font=dict(size=15, color="#e8eef6", family="Segoe UI"),
# # )

# # # ── HEADER ─────────────────────────────────────────────────────────────────────
# # st.markdown('<p class="section-label">Loan Performance & Risk</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-title">Portfolio Intelligence Dashboard</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-desc">Monitor loan health, identify risky borrowers, and reduce defaults across your portfolio.</p>', unsafe_allow_html=True)
# # st.markdown("---")

# # # ── FILTERS ────────────────────────────────────────────────────────────────────
# # st.markdown('<p class="section-label">Filters — Select a value to update all charts below</p>', unsafe_allow_html=True)
# # f1, f2, f3 = st.columns(3)
# # with f1:
# #     purpose_filter = st.selectbox(
# #         "Loan Purpose",
# #         ["All"] + sorted(df["LoanPurpose"].unique().tolist()),
# #         help="Filter by the reason the loan was taken (Home, Auto, Business, etc.)"
# #     )
# # with f2:
# #     emp_filter = st.selectbox(
# #         "Employment Type",
# #         ["All"] + sorted(df["EmploymentType"].unique().tolist()),
# #         help="Filter by borrower employment status"
# #     )
# # with f3:
# #     risk_filter = st.selectbox(
# #         "Risk Tier",
# #         ["All", "Low", "Medium", "High"],
# #         help="Low = safe borrowers. High = borrowers most likely to default."
# #     )

# # # ── APPLY FILTERS ──────────────────────────────────────────────────────────────
# # filtered = df.copy()
# # if purpose_filter != "All":
# #     filtered = filtered[filtered["LoanPurpose"] == purpose_filter]
# # if emp_filter != "All":
# #     filtered = filtered[filtered["EmploymentType"] == emp_filter]
# # if risk_filter != "All":
# #     filtered = filtered[filtered["RiskTier"] == risk_filter]

# # # ── METRICS ────────────────────────────────────────────────────────────────────
# # total        = len(filtered)
# # defaults     = int(filtered["Default"].sum())
# # default_rate = (defaults / total * 100) if total else 0
# # avg_credit   = filtered["CreditScore"].mean()
# # avg_dti      = filtered["DTIRatio"].mean()
# # avg_lti      = filtered["LTIRatio"].mean()
# # avg_interest = filtered["InterestRate"].mean()
# # avg_loan     = filtered["LoanAmount"].mean()

# # risk_counts  = filtered["RiskTier"].value_counts()
# # low_pct      = risk_counts.get("Low", 0)    / total * 100 if total else 0
# # med_pct      = risk_counts.get("Medium", 0) / total * 100 if total else 0
# # high_pct     = risk_counts.get("High", 0)   / total * 100 if total else 0

# # st.markdown("---")

# # # ══════════════════════════════════════════════════════════════════════════════
# # # ROW 1 — KPI CARDS
# # # ══════════════════════════════════════════════════════════════════════════════
# # st.markdown('<p class="section-label">Row 1</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-title">How Bad Is It?</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-desc">Overall health of your loan portfolio based on current filters.</p>', unsafe_allow_html=True)

# # k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)

# # with k1:
# #     st.metric(
# #         "Total Loans",
# #         f"{total:,}",
# #         help="Total number of loans matching your current filters"
# #     )
# # with k2:
# #     st.metric(
# #         "Defaults",
# #         f"{defaults:,}",
# #         help="Number of loans where the borrower failed to repay"
# #     )
# # with k3:
# #     st.metric(
# #         "Default Rate",
# #         f"{default_rate:.1f}%",
# #         delta="Above 20% is critical" if default_rate > 20 else "Above 12% needs attention" if default_rate > 12 else "Healthy",
# #         delta_color="inverse" if default_rate > 12 else "normal",
# #         help="Percentage of loans that defaulted. Below 12% is healthy."
# #     )
# # with k4:
# #     st.metric(
# #         "Avg Credit Score",
# #         f"{avg_credit:.0f}",
# #         delta="Below safe line (670)" if avg_credit < 670 else "Above safe line",
# #         delta_color="inverse" if avg_credit < 670 else "normal",
# #         help="Average credit score of borrowers. Above 670 is considered safe."
# #     )
# # with k5:
# #     st.metric(
# #         "Avg DTI Ratio",
# #         f"{avg_dti:.2f}",
# #         delta="Risky if above 0.5" if avg_dti > 0.5 else "Acceptable",
# #         delta_color="inverse" if avg_dti > 0.5 else "normal",
# #         help="Debt-to-Income ratio. How much of income goes to paying debts. Above 0.5 is risky."
# #     )
# # with k6:
# #     st.metric(
# #         "Avg LTI Ratio",
# #         f"{avg_lti:.2f}",
# #         delta="Overextended if above 4" if avg_lti > 4 else "Manageable",
# #         delta_color="inverse" if avg_lti > 4 else "normal",
# #         help="Loan-to-Income ratio. Loan amount divided by annual income. Above 4 is dangerous."
# #     )
# # with k7:
# #     st.metric(
# #         "Avg Interest",
# #         f"{avg_interest:.1f}%",
# #         help="Average interest rate charged across all filtered loans"
# #     )
# # with k8:
# #     st.metric(
# #         "Avg Loan Size",
# #         f"${avg_loan:,.0f}",
# #         help="Average loan amount borrowed"
# #     )

# # st.markdown("---")

# # # ── RISK TIER PILLS ────────────────────────────────────────────────────────────
# # st.markdown('<p class="section-label">Portfolio Risk Split</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-desc">What percentage of your portfolio falls into each risk category.</p>', unsafe_allow_html=True)

# # r1, r2, r3 = st.columns(3)
# # with r1:
# #     st.metric(
# #         "Low Risk Loans",
# #         f"{low_pct:.1f}%",
# #         f"{risk_counts.get('Low', 0):,} loans — safe borrowers",
# #         help="Borrowers with strong credit, low DTI, stable employment, and manageable loan size"
# #     )
# # with r2:
# #     st.metric(
# #         "Medium Risk Loans",
# #         f"{med_pct:.1f}%",
# #         f"{risk_counts.get('Medium', 0):,} loans — needs monitoring",
# #         help="Borrowers with some risk factors. Watch these closely."
# #     )
# # with r3:
# #     st.metric(
# #         "High Risk Loans",
# #         f"{high_pct:.1f}%",
# #         f"{risk_counts.get('High', 0):,} loans — danger zone",
# #         delta_color="inverse",
# #         help="Borrowers with multiple risk factors. Most likely to default."
# #     )

# # st.markdown("---")

# # # ══════════════════════════════════════════════════════════════════════════════
# # # ROW 2 — WHICH LOAN TYPE IS THE PROBLEM?
# # # ══════════════════════════════════════════════════════════════════════════════
# # st.markdown('<p class="section-label">Row 2</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-title">Which Loan Type Is the Problem?</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-desc">Compare volume and default rate across loan purposes to find where the risk is concentrated.</p>', unsafe_allow_html=True)

# # col1, col2 = st.columns(2)

# # with col1:
# #     purpose_stats = filtered.groupby("LoanPurpose").agg(
# #         Count=("Default", "count"),
# #         Defaults=("Default", "sum")
# #     ).reset_index()
# #     purpose_stats["DefaultRate"] = (purpose_stats["Defaults"] / purpose_stats["Count"] * 100).round(1)

# #     fig1 = go.Figure()
# #     fig1.add_trace(go.Bar(
# #         x=purpose_stats["LoanPurpose"],
# #         y=purpose_stats["Count"],
# #         name="Number of Loans",
# #         marker_color=[PURPOSE_COLORS_LIGHT.get(p, "rgba(128,128,128,0.3)") for p in purpose_stats["LoanPurpose"]],
# #         yaxis="y1"
# #     ))
# #     fig1.add_trace(go.Bar(
# #         x=purpose_stats["LoanPurpose"],
# #         y=purpose_stats["DefaultRate"],
# #         name="Default Rate %",
# #         marker_color=[PURPOSE_COLORS.get(p, "#888888") for p in purpose_stats["LoanPurpose"]],
# #         yaxis="y2"
# #     ))
# #     fig1.update_layout(
# #         **CHART_STYLE,
# #         title="Loans & Default Rate by Purpose",
# #         barmode="group",
# #         yaxis=dict(title="Number of Loans", gridcolor="#1e2736", title_font=dict(size=12)),
# #         yaxis2=dict(title="Default Rate %", overlaying="y", side="right", title_font=dict(size=12)),
# #         showlegend=True,
# #         legend=dict(bgcolor="#0e1117", font=dict(size=12))
# #     )
# #     st.plotly_chart(fig1, use_container_width=True)
# #     st.markdown('<div class="insight-box">Faded bars = number of loans. Solid bars = default rate. A loan type with few loans but tall solid bars is your biggest risk per loan.</div>', unsafe_allow_html=True)

# # with col2:
# #     fc = filtered.copy()
# #     fc["DTIBucket"] = pd.cut(
# #         fc["DTIRatio"],
# #         bins=[0, 0.2, 0.35, 0.5, 0.65, 0.8, 99],
# #         labels=["<0.2", "0.2–0.35", "0.35–0.5", "0.5–0.65", "0.65–0.8", "0.8+"]
# #     )
# #     dti_stats = fc.groupby("DTIBucket", observed=True).agg(
# #         Total=("Default", "count"),
# #         Defaults=("Default", "sum")
# #     ).reset_index()
# #     dti_stats["DefaultRate"] = (dti_stats["Defaults"] / dti_stats["Total"] * 100).round(1)

# #     fig2 = go.Figure(go.Bar(
# #         x=dti_stats["DTIBucket"].astype(str),
# #         y=dti_stats["DefaultRate"],
# #         marker_color=["#00d4aa", "#00d4aa", "#ffc145", "#ffc145", "#ff4560", "#ff4560"],
# #         text=dti_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
# #         textposition="outside",
# #         textfont=dict(size=13)
# #     ))
# #     fig2.update_layout(
# #         **CHART_STYLE,
# #         title="Default Rate by DTI Bucket",
# #         yaxis=dict(title="Default Rate %", gridcolor="#1e2736"),
# #         xaxis=dict(title="DTI Ratio Range  (how much of income goes to debt payments)")
# #     )
# #     st.plotly_chart(fig2, use_container_width=True)
# #     st.markdown('<div class="insight-box">Green = safe DTI range. Yellow = watch. Red = danger. The higher the DTI the more of a borrowers income is already spent on debt before this loan.</div>', unsafe_allow_html=True)

# # st.markdown("---")

# # # ══════════════════════════════════════════════════════════════════════════════
# # # ROW 3 — WHERE ARE THE DANGEROUS LOANS?
# # # ══════════════════════════════════════════════════════════════════════════════
# # st.markdown('<p class="section-label">Row 3</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-title">Where Are the Dangerous Loans?</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-desc">Visualize exactly where defaults cluster using two key risk signals together.</p>', unsafe_allow_html=True)

# # col3, col4 = st.columns([2, 1])

# # with col3:
# #     sample = filtered.sample(min(1000, len(filtered)), random_state=42).copy()
# #     sample["LTIcapped"] = sample["LTIRatio"].clip(upper=10)
# #     sample["Status"]    = sample["Default"].map({0: "No Default", 1: "Defaulted"})

# #     fig3 = px.scatter(
# #         sample,
# #         x="DTIRatio",
# #         y="LTIcapped",
# #         color="Status",
# #         color_discrete_map={"No Default": "#00d4aa", "Defaulted": "#ff4560"},
# #         opacity=0.5,
# #         title="Danger Zone — DTI Ratio vs Loan-to-Income Ratio",
# #         labels={
# #             "DTIRatio":  "DTI Ratio  (% of income spent on debts)",
# #             "LTIcapped": "LTI Ratio  (loan size vs annual income)"
# #         },
# #     )
# #     fig3.update_traces(marker=dict(size=7))
# #     fig3.update_layout(
# #         **CHART_STYLE,
# #         showlegend=True,
# #         legend=dict(bgcolor="#0e1117", title_text="Loan Status", font=dict(size=13))
# #     )
# #     st.plotly_chart(fig3, use_container_width=True)
# #     st.markdown('<div class="insight-box">Each dot is one loan. Red = defaulted. Green = paid back. The red cluster in the top-right is your danger zone — borrowers who have high existing debt AND borrowed far more than their income supports.</div>', unsafe_allow_html=True)

# # with col4:
# #     st.markdown("#### Risk Tier Breakdown")
# #     st.markdown('<p class="section-desc">Composite score using DTI, credit score, employment, LTI, and co-signer.</p>', unsafe_allow_html=True)
# #     for tier, color in RISK_COLORS.items():
# #         count = int(risk_counts.get(tier, 0))
# #         pct   = count / total * 100 if total else 0
# #         st.markdown(f"""
# #         <div style="margin-bottom:20px">
# #             <div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:14px">
# #                 <span style="color:{color};font-weight:700">{tier} Risk</span>
# #                 <span style="color:#e8eef6">{count:,} loans &nbsp;({pct:.1f}%)</span>
# #             </div>
# #             <div style="height:12px;background:#1e2736;border-radius:6px;overflow:hidden">
# #                 <div style="height:100%;width:{pct}%;background:{color};border-radius:6px"></div>
# #             </div>
# #         </div>
# #         """, unsafe_allow_html=True)
# #     st.markdown('<div class="insight-box">If High Risk exceeds 25% of your portfolio you should tighten approval criteria immediately.</div>', unsafe_allow_html=True)

# # st.markdown("---")

# # # ══════════════════════════════════════════════════════════════════════════════
# # # ROW 4 — WHO IS THE RISKY BORROWER?
# # # ══════════════════════════════════════════════════════════════════════════════
# # st.markdown('<p class="section-label">Row 4</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-title">Who Is the Risky Borrower?</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-desc">See how credit score and employment type predict default rate in your portfolio.</p>', unsafe_allow_html=True)

# # col5, col6 = st.columns(2)

# # with col5:
# #     fc2 = filtered.copy()
# #     fc2["CreditBand"] = pd.cut(
# #         fc2["CreditScore"],
# #         bins=[300, 500, 580, 670, 740, 851],
# #         labels=["300–500", "500–580", "580–670", "670–740", "740–850"]
# #     )
# #     credit_stats = fc2.groupby("CreditBand", observed=True).agg(
# #         Total=("Default", "count"),
# #         Defaults=("Default", "sum")
# #     ).reset_index()
# #     credit_stats["DefaultRate"] = (credit_stats["Defaults"] / credit_stats["Total"] * 100).round(1)

# #     fig4 = go.Figure(go.Bar(
# #         x=credit_stats["DefaultRate"],
# #         y=credit_stats["CreditBand"].astype(str),
# #         orientation="h",
# #         marker_color=["#ff4560", "#ff4560", "#ffc145", "#00d4aa", "#00d4aa"],
# #         text=credit_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
# #         textposition="outside",
# #         textfont=dict(size=13)
# #     ))
# #     fig4.update_layout(
# #         **CHART_STYLE,
# #         title="Default Rate by Credit Score Band",
# #         xaxis=dict(title="Default Rate %", gridcolor="#1e2736"),
# #         yaxis=dict(title="Credit Score Range", tickfont=dict(size=13))
# #     )
# #     st.plotly_chart(fig4, use_container_width=True)
# #     st.markdown('<div class="insight-box">670 is the turning point. Below 670 = high risk. Above 670 = acceptable. Use this as your approval threshold.</div>', unsafe_allow_html=True)

# # with col6:
# #     emp_stats = filtered.groupby("EmploymentType").agg(
# #         Total=("Default", "count"),
# #         Defaults=("Default", "sum")
# #     ).reset_index()
# #     emp_stats["DefaultRate"] = (emp_stats["Defaults"] / emp_stats["Total"] * 100).round(1)
# #     emp_stats = emp_stats.sort_values("DefaultRate", ascending=True)

# #     fig5 = go.Figure(go.Bar(
# #         x=emp_stats["DefaultRate"],
# #         y=emp_stats["EmploymentType"],
# #         orientation="h",
# #         marker_color=["#00d4aa", "#ffc145", "#ff6b35", "#ff4560"],
# #         text=emp_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
# #         textposition="outside",
# #         textfont=dict(size=13)
# #     ))
# #     fig5.update_layout(
# #         **CHART_STYLE,
# #         title="Default Rate by Employment Type",
# #         xaxis=dict(title="Default Rate %", gridcolor="#1e2736"),
# #         yaxis=dict(title="Employment Status", tickfont=dict(size=13))
# #     )
# #     st.plotly_chart(fig5, use_container_width=True)
# #     st.markdown('<div class="insight-box">Employment is the strongest single warning sign. An unemployed borrower is roughly 3x more likely to default than a full-time borrower.</div>', unsafe_allow_html=True)

# # st.markdown("---")

# # # ══════════════════════════════════════════════════════════════════════════════
# # # ROW 5 — WHAT CAN REDUCE DEFAULTS FAST?
# # # ══════════════════════════════════════════════════════════════════════════════
# # st.markdown('<p class="section-label">Row 5</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-title">What Can Reduce Defaults Fast?</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-desc">Two actionable signals that were hidden in your data and are now surfaced for the first time.</p>', unsafe_allow_html=True)

# # col7, col8 = st.columns(2)

# # with col7:
# #     st.markdown("#### Co-Signer Impact on Default Rate")
# #     st.markdown('<p class="section-desc">Does having a co-signer actually reduce the chance of defaulting?</p>', unsafe_allow_html=True)

# #     cosigner = filtered.groupby("HasCoSigner").agg(
# #         Total=("Default", "count"),
# #         Defaults=("Default", "sum")
# #     ).reset_index()
# #     cosigner["DefaultRate"] = (cosigner["Defaults"] / cosigner["Total"] * 100).round(1)

# #     with_rate    = cosigner[cosigner["HasCoSigner"] == "Yes"]["DefaultRate"].values
# #     without_rate = cosigner[cosigner["HasCoSigner"] == "No"]["DefaultRate"].values
# #     with_val     = with_rate[0]    if len(with_rate)    else 0
# #     without_val  = without_rate[0] if len(without_rate) else 0
# #     difference   = abs(without_val - with_val)

# #     ca, cb = st.columns(2)
# #     with ca:
# #         st.metric(
# #             "With Co-Signer",
# #             f"{with_val:.1f}%",
# #             "Default Rate",
# #             help="Loans where a second person guaranteed repayment"
# #         )
# #     with cb:
# #         st.metric(
# #             "Without Co-Signer",
# #             f"{without_val:.1f}%",
# #             "Default Rate",
# #             delta_color="inverse",
# #             help="Loans where the borrower had no guarantor"
# #         )

# #     st.success(f"Requiring a co-signer cuts default risk by {difference:.1f} percentage points. Apply this rule to all High Risk borrowers.")

# # with col8:
# #     st.markdown("#### Default Rate by Education Level")
# #     st.markdown('<p class="section-desc">Does education level predict long-term repayment ability?</p>', unsafe_allow_html=True)

# #     edu_order = ["PhD", "Master's", "Bachelor's", "High School"]
# #     edu_stats = filtered.groupby("Education").agg(
# #         Total=("Default", "count"),
# #         Defaults=("Default", "sum")
# #     ).reset_index()
# #     edu_stats["DefaultRate"] = (edu_stats["Defaults"] / edu_stats["Total"] * 100).round(1)
# #     edu_stats["Education"]   = pd.Categorical(edu_stats["Education"], categories=edu_order, ordered=True)
# #     edu_stats = edu_stats.sort_values("Education")

# #     fig6 = go.Figure(go.Bar(
# #         x=edu_stats["DefaultRate"],
# #         y=edu_stats["Education"].astype(str),
# #         orientation="h",
# #         marker_color=["#00d4aa", "#00d4aa", "#ffc145", "#ff4560"],
# #         text=edu_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
# #         textposition="outside",
# #         textfont=dict(size=13)
# #     ))
# #     fig6.update_layout(
# #         **CHART_STYLE,
# #         title="Default Rate by Education Level",
# #         xaxis=dict(title="Default Rate %", gridcolor="#1e2736"),
# #         yaxis=dict(
# #             categoryorder="array",
# #             categoryarray=edu_order,
# #             tickfont=dict(size=13)
# #         )
# #     )
# #     st.plotly_chart(fig6, use_container_width=True)
# #     st.markdown('<div class="insight-box">Education signals future earning potential. A PhD borrower earning $40K today is a very different risk from a High School borrower earning $40K today.</div>', unsafe_allow_html=True)

# # st.markdown("---")

# # # ══════════════════════════════════════════════════════════════════════════════
# # # ROW 6 — BORROWER PROFILE BY LOAN TYPE
# # # ══════════════════════════════════════════════════════════════════════════════
# # st.markdown('<p class="section-label">Row 6</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-title">Borrower Profile by Loan Type</p>', unsafe_allow_html=True)
# # st.markdown('<p class="section-desc">Compare the average borrower characteristics across each loan purpose to understand who is borrowing what.</p>', unsafe_allow_html=True)

# # profile = filtered.groupby("LoanPurpose").agg(
# #     AvgLoan=("LoanAmount",    "mean"),
# #     AvgCredit=("CreditScore", "mean"),
# #     AvgInterest=("InterestRate", "mean"),
# #     AvgLTI=("LTIRatio",      "mean"),
# # ).reset_index().round(2)

# # p1, p2, p3, p4 = st.columns(4)

# # chart_configs = [
# #     (p1, "AvgLoan",     "Avg Loan Amount",              True,  "How large are the loans for each type?"),
# #     (p2, "AvgCredit",   "Avg Credit Score",             False, "Which loan type attracts stronger borrowers?"),
# #     (p3, "AvgInterest", "Avg Interest Rate (%)",        False, "Where is the bank charging more for risk?"),
# #     (p4, "AvgLTI",      "Avg Loan-to-Income Ratio",     False, "Which borrowers are most stretched vs their income?"),
# # ]

# # for col, metric, title, is_dollar, caption in chart_configs:
# #     with col:
# #         bar_colors = [PURPOSE_COLORS.get(p, "#888888") for p in profile["LoanPurpose"]]
# #         text_vals  = profile[metric].apply(lambda x: f"${x:,.0f}" if is_dollar else f"{x:.1f}")

# #         fig_p = go.Figure(go.Bar(
# #             x=profile["LoanPurpose"],
# #             y=profile[metric],
# #             marker_color=bar_colors,
# #             text=text_vals,
# #             textposition="outside",
# #             textfont=dict(size=12)
# #         ))
# #         fig_p.update_layout(
# #             **CHART_STYLE,
# #             title=title,
# #             height=300,
# #             yaxis=dict(gridcolor="#1e2736"),
# #             xaxis=dict(tickfont=dict(size=12))
# #         )
# #         st.plotly_chart(fig_p, use_container_width=True)
# #         st.markdown(f'<div class="insight-box">{caption}</div>', unsafe_allow_html=True)

# # st.markdown("---")
# # st.markdown("""
# # <div style="text-align:center;color:#4a5568;font-size:13px;padding:10px">
# #     Loan Risk Dashboard &nbsp;·&nbsp; All 18 columns used &nbsp;·&nbsp;
# #     Filters: Loan Purpose | Employment Type | Risk Tier
# # </div>
# # """, unsafe_allow_html=True)
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# # ── PAGE CONFIG ────────────────────────────────────────────────────────────────
# st.set_page_config(page_title="Loan Risk Dashboard", page_icon="💳", layout="wide")

# # ── STYLE ──────────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
#     html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
#     [data-testid="stMetricLabel"]  { font-size: 13px !important; color: #a0aec0 !important; font-weight: 600 !important; }
#     [data-testid="stMetricValue"]  { font-size: 28px !important; font-weight: 700 !important; }
#     [data-testid="stMetricDelta"]  { font-size: 12px !important; }
#     .block-title {
#         font-size: 16px;
#         font-weight: 700;
#         color: #e8eef6;
#         padding: 6px 12px;
#         background: #1a202c;
#         border-left: 4px solid #00d4aa;
#         border-radius: 4px;
#         margin-bottom: 12px;
#     }
#     .hint {
#         font-size: 12px;
#         color: #718096;
#         margin-top: 6px;
#         padding: 6px 10px;
#         background: #1a202c;
#         border-radius: 4px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ── LOAD DATA ──────────────────────────────────────────────────────────────────
# @st.cache_data
# def load_data():
#     df = pd.read_csv("Loan_default.csv")
#     df["LTIRatio"] = (df["LoanAmount"] / df["Income"]).round(2)

#     def risk_tier(row):
#         score = 0
#         if row["DTIRatio"] > 0.5:                 score += 2
#         if row["CreditScore"] < 580:              score += 2
#         if row["CreditScore"] < 670:              score += 1
#         if row["EmploymentType"] == "Unemployed": score += 3
#         if row["EmploymentType"] == "Part-time":  score += 1
#         if row["LTIRatio"] > 4:                   score += 2
#         if row["HasCoSigner"] == "Yes":           score -= 1
#         if score <= 2:   return "Low"
#         elif score <= 5: return "Medium"
#         else:            return "High"

#     df["RiskTier"] = df.apply(risk_tier, axis=1)
#     return df

# df = load_data()

# # ── COLORS ─────────────────────────────────────────────────────────────────────
# PURPOSE_COLORS = {
#     "Home": "#00d4aa", "Auto": "#4f9eff",
#     "Education": "#ffc145", "Business": "#ff6b35", "Other": "#b06bff",
# }
# PURPOSE_COLORS_LIGHT = {
#     "Home": "rgba(0,212,170,0.3)", "Auto": "rgba(79,158,255,0.3)",
#     "Education": "rgba(255,193,69,0.3)", "Business": "rgba(255,107,53,0.3)",
#     "Other": "rgba(176,107,255,0.3)",
# }
# RISK_COLORS = {"Low": "#00d4aa", "Medium": "#ffc145", "High": "#ff4560"}
# C = dict(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117",
#          font=dict(color="#e8eef6", size=13, family="Segoe UI"),
#          margin=dict(t=40, b=30, l=10, r=10),
#          title_font=dict(size=14, color="#e8eef6"))

# # ── HEADER ─────────────────────────────────────────────────────────────────────
# st.markdown("## 💳 Loan Risk Dashboard")
# st.markdown("---")

# # ── 3 FILTERS ─────────────────────────────────────────────────────────────────
# f1, f2, f3 = st.columns(3)
# with f1:
#     purpose_filter = st.selectbox("Loan Purpose", ["All"] + sorted(df["LoanPurpose"].unique().tolist()))
# with f2:
#     emp_filter = st.selectbox("Employment Type", ["All"] + sorted(df["EmploymentType"].unique().tolist()))
# with f3:
#     risk_filter = st.selectbox("Risk Tier", ["All", "Low", "Medium", "High"])

# # ── APPLY FILTERS ──────────────────────────────────────────────────────────────
# filtered = df.copy()
# if purpose_filter != "All":
#     filtered = filtered[filtered["LoanPurpose"] == purpose_filter]
# if emp_filter != "All":
#     filtered = filtered[filtered["EmploymentType"] == emp_filter]
# if risk_filter != "All":
#     filtered = filtered[filtered["RiskTier"] == risk_filter]

# # ── CALCULATIONS ───────────────────────────────────────────────────────────────
# total        = len(filtered)
# defaults     = int(filtered["Default"].sum())
# default_rate = (defaults / total * 100) if total else 0
# avg_credit   = filtered["CreditScore"].mean()
# avg_dti      = filtered["DTIRatio"].mean()
# avg_lti      = filtered["LTIRatio"].mean()
# risk_counts  = filtered["RiskTier"].value_counts()
# low_pct      = risk_counts.get("Low",    0) / total * 100 if total else 0
# med_pct      = risk_counts.get("Medium", 0) / total * 100 if total else 0
# high_pct     = risk_counts.get("High",   0) / total * 100 if total else 0

# st.markdown("---")

# # ══════════════════════════════════════════════════════════════════════════════
# # SECTION 1 — PORTFOLIO HEALTH (6 cards)
# # ══════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="block-title">📊 Portfolio Health</div>', unsafe_allow_html=True)

# k1, k2, k3, k4, k5, k6 = st.columns(6)

# with k1:
#     st.metric("Total Loans", f"{total:,}")
# with k2:
#     st.metric("Default Rate", f"{default_rate:.1f}%",
#               delta="Critical" if default_rate > 20 else "Watch" if default_rate > 12 else "Healthy",
#               delta_color="inverse" if default_rate > 12 else "normal")
# with k3:
#     st.metric("Avg Credit Score", f"{avg_credit:.0f}",
#               delta="Below 670 — risky" if avg_credit < 670 else "Above 670 — ok",
#               delta_color="inverse" if avg_credit < 670 else "normal")
# with k4:
#     st.metric("Avg DTI Ratio", f"{avg_dti:.2f}",
#               delta="Above 0.5 — risky" if avg_dti > 0.5 else "Below 0.5 — ok",
#               delta_color="inverse" if avg_dti > 0.5 else "normal")
# with k5:
#     st.metric("Avg LTI Ratio", f"{avg_lti:.2f}",
#               delta="Above 4 — overextended" if avg_lti > 4 else "Below 4 — ok",
#               delta_color="inverse" if avg_lti > 4 else "normal")
# with k6:
#     st.metric("High Risk Loans", f"{high_pct:.1f}%",
#               delta=f"{risk_counts.get('High', 0):,} loans in danger zone",
#               delta_color="inverse" if high_pct > 25 else "off")

# st.markdown("---")

# # ══════════════════════════════════════════════════════════════════════════════
# # SECTION 2 — TWO MAIN CHARTS
# # ══════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="block-title">🏦 Which Loan Type Is the Problem?</div>', unsafe_allow_html=True)

# col1, col2 = st.columns(2)

# with col1:
#     purpose_stats = filtered.groupby("LoanPurpose").agg(
#         Count=("Default", "count"),
#         Defaults=("Default", "sum")
#     ).reset_index()
#     purpose_stats["DefaultRate"] = (purpose_stats["Defaults"] / purpose_stats["Count"] * 100).round(1)

#     fig1 = go.Figure()
#     fig1.add_trace(go.Bar(
#         x=purpose_stats["LoanPurpose"], y=purpose_stats["Count"],
#         name="No. of Loans",
#         marker_color=[PURPOSE_COLORS_LIGHT.get(p, "rgba(128,128,128,0.3)") for p in purpose_stats["LoanPurpose"]],
#         yaxis="y1"
#     ))
#     fig1.add_trace(go.Bar(
#         x=purpose_stats["LoanPurpose"], y=purpose_stats["DefaultRate"],
#         name="Default Rate %",
#         marker_color=[PURPOSE_COLORS.get(p, "#888") for p in purpose_stats["LoanPurpose"]],
#         yaxis="y2"
#     ))
#     fig1.update_layout(
#         **C, title="Loans & Default Rate by Purpose", barmode="group",
#         yaxis=dict(title="No. of Loans", gridcolor="#1e2736"),
#         yaxis2=dict(title="Default Rate %", overlaying="y", side="right"),
#         showlegend=True, legend=dict(bgcolor="#0e1117")
#     )
#     st.plotly_chart(fig1, use_container_width=True)
#     st.markdown('<div class="hint">Faded bar = number of loans &nbsp;|&nbsp; Solid bar = default rate %</div>', unsafe_allow_html=True)

# with col2:
#     sample = filtered.sample(min(1000, len(filtered)), random_state=42).copy()
#     sample["LTIcapped"] = sample["LTIRatio"].clip(upper=10)
#     sample["Status"]    = sample["Default"].map({0: "No Default", 1: "Defaulted"})

#     fig2 = px.scatter(
#         sample, x="DTIRatio", y="LTIcapped", color="Status",
#         color_discrete_map={"No Default": "#00d4aa", "Defaulted": "#ff4560"},
#         opacity=0.5, title="Danger Zone — DTI vs LTI",
#         labels={"DTIRatio": "DTI Ratio", "LTIcapped": "LTI Ratio (capped at 10)"},
#     )
#     fig2.update_traces(marker=dict(size=6))
#     fig2.update_layout(**C, showlegend=True, legend=dict(bgcolor="#0e1117"))
#     st.plotly_chart(fig2, use_container_width=True)
#     st.markdown('<div class="hint">Each dot = one loan &nbsp;|&nbsp; Red dots defaulted &nbsp;|&nbsp; Top-right cluster = danger zone</div>', unsafe_allow_html=True)

# st.markdown("---")

# # ══════════════════════════════════════════════════════════════════════════════
# # SECTION 3 — WHO IS THE RISKY BORROWER?
# # ══════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="block-title">👤 Who Is the Risky Borrower?</div>', unsafe_allow_html=True)

# col3, col4 = st.columns(2)

# with col3:
#     fc2 = filtered.copy()
#     fc2["CreditBand"] = pd.cut(
#         fc2["CreditScore"],
#         bins=[300, 500, 580, 670, 740, 851],
#         labels=["300–500", "500–580", "580–670", "670–740", "740–850"]
#     )
#     credit_stats = fc2.groupby("CreditBand", observed=True).agg(
#         Total=("Default", "count"), Defaults=("Default", "sum")
#     ).reset_index()
#     credit_stats["DefaultRate"] = (credit_stats["Defaults"] / credit_stats["Total"] * 100).round(1)

#     fig3 = go.Figure(go.Bar(
#         x=credit_stats["DefaultRate"],
#         y=credit_stats["CreditBand"].astype(str),
#         orientation="h",
#         marker_color=["#ff4560", "#ff4560", "#ffc145", "#00d4aa", "#00d4aa"],
#         text=credit_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
#         textposition="outside", textfont=dict(size=13)
#     ))
#     fig3.update_layout(**C, title="Default Rate by Credit Score",
#                        xaxis=dict(title="Default Rate %", gridcolor="#1e2736"))
#     st.plotly_chart(fig3, use_container_width=True)
#     st.markdown('<div class="hint">Below 670 = high risk &nbsp;|&nbsp; Above 670 = acceptable</div>', unsafe_allow_html=True)

# with col4:
#     emp_stats = filtered.groupby("EmploymentType").agg(
#         Total=("Default", "count"), Defaults=("Default", "sum")
#     ).reset_index()
#     emp_stats["DefaultRate"] = (emp_stats["Defaults"] / emp_stats["Total"] * 100).round(1)
#     emp_stats = emp_stats.sort_values("DefaultRate", ascending=True)

#     fig4 = go.Figure(go.Bar(
#         x=emp_stats["DefaultRate"], y=emp_stats["EmploymentType"],
#         orientation="h",
#         marker_color=["#00d4aa", "#ffc145", "#ff6b35", "#ff4560"],
#         text=emp_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
#         textposition="outside", textfont=dict(size=13)
#     ))
#     fig4.update_layout(**C, title="Default Rate by Employment Type",
#                        xaxis=dict(title="Default Rate %", gridcolor="#1e2736"))
#     st.plotly_chart(fig4, use_container_width=True)
#     st.markdown('<div class="hint">Unemployed borrowers default ~3x more than full-time borrowers</div>', unsafe_allow_html=True)

# st.markdown("---")

# # ══════════════════════════════════════════════════════════════════════════════
# # SECTION 4 — TWO QUICK WINS
# # ══════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="block-title">💡 Two Quick Wins to Reduce Defaults</div>', unsafe_allow_html=True)

# col5, col6 = st.columns(2)

# with col5:
#     cosigner = filtered.groupby("HasCoSigner").agg(
#         Total=("Default", "count"), Defaults=("Default", "sum")
#     ).reset_index()
#     cosigner["DefaultRate"] = (cosigner["Defaults"] / cosigner["Total"] * 100).round(1)

#     with_val    = cosigner[cosigner["HasCoSigner"] == "Yes"]["DefaultRate"].values
#     without_val = cosigner[cosigner["HasCoSigner"] == "No"]["DefaultRate"].values
#     with_val    = with_val[0]    if len(with_val)    else 0
#     without_val = without_val[0] if len(without_val) else 0
#     diff        = abs(without_val - with_val)

#     ca, cb = st.columns(2)
#     with ca:
#         st.metric("With Co-Signer",    f"{with_val:.1f}%", "default rate")
#     with cb:
#         st.metric("Without Co-Signer", f"{without_val:.1f}%", "default rate", delta_color="inverse")

#     st.success(f"Requiring a co-signer cuts defaults by {diff:.1f} percentage points.")
#     st.markdown('<div class="hint">Require a co-signer for all High Risk borrowers</div>', unsafe_allow_html=True)

# with col6:
#     edu_order = ["PhD", "Master's", "Bachelor's", "High School"]
#     edu_stats = filtered.groupby("Education").agg(
#         Total=("Default", "count"), Defaults=("Default", "sum")
#     ).reset_index()
#     edu_stats["DefaultRate"] = (edu_stats["Defaults"] / edu_stats["Total"] * 100).round(1)
#     edu_stats["Education"]   = pd.Categorical(edu_stats["Education"], categories=edu_order, ordered=True)
#     edu_stats = edu_stats.sort_values("Education")

#     fig5 = go.Figure(go.Bar(
#         x=edu_stats["DefaultRate"],
#         y=edu_stats["Education"].astype(str),
#         orientation="h",
#         marker_color=["#00d4aa", "#00d4aa", "#ffc145", "#ff4560"],
#         text=edu_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
#         textposition="outside", textfont=dict(size=13)
#     ))
#     fig5.update_layout(
#         **C, title="Default Rate by Education Level",
#         xaxis=dict(title="Default Rate %", gridcolor="#1e2736"),
#         yaxis=dict(categoryorder="array", categoryarray=edu_order)
#     )
#     st.plotly_chart(fig5, use_container_width=True)
#     st.markdown('<div class="hint">Education signals future earning potential — not just current salary</div>', unsafe_allow_html=True)

# st.markdown("---")
# st.caption("Loan Risk Dashboard · Filters: Loan Purpose | Employment Type | Risk Tier")
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
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    [data-testid="stMetricLabel"] { font-size: 13px !important; color: #a0aec0 !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; }
    [data-testid="stMetricDelta"] { font-size: 12px !important; }
    .block-title {
        font-size: 16px; font-weight: 700; color: #e8eef6;
        padding: 6px 12px; background: #1a202c;
        border-left: 4px solid #00d4aa;
        border-radius: 4px; margin-bottom: 12px;
    }
    .hint {
        font-size: 12px; color: #718096; margin-top: 6px;
        padding: 6px 10px; background: #1a202c; border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Loan_default.csv")
    df["LTIRatio"] = (df["LoanAmount"] / df["Income"]).round(2)

    def risk_tier(row):
        score = 0
        if row["DTIRatio"] > 0.5:                 score += 2
        if row["CreditScore"] < 580:              score += 2
        if row["CreditScore"] < 670:              score += 1
        if row["EmploymentType"] == "Unemployed": score += 3
        if row["EmploymentType"] == "Part-time":  score += 1
        if row["LTIRatio"] > 4:                   score += 2
        if row["HasCoSigner"] == "Yes":           score -= 1
        if score <= 2:   return "Low"
        elif score <= 5: return "Medium"
        else:            return "High"

    df["RiskTier"] = df.apply(risk_tier, axis=1)
    return df

df = load_data()

# ── COLORS ─────────────────────────────────────────────────────────────────────
PURPOSE_COLORS = {
    "Home": "#00d4aa", "Auto": "#4f9eff",
    "Education": "#ffc145", "Business": "#ff6b35", "Other": "#b06bff",
}
RISK_COLORS = {"Low": "#00d4aa", "Medium": "#ffc145", "High": "#ff4560"}

C = dict(
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="#e8eef6", size=13, family="Segoe UI"),
    margin=dict(t=50, b=40, l=10, r=10),
    title_font=dict(size=15, color="#e8eef6"),
)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("## 💳 Loan Risk Dashboard")
st.markdown("---")

# ── FILTERS ────────────────────────────────────────────────────────────────────
f1, f2, f3 = st.columns(3)
with f1:
    purpose_filter = st.selectbox("Loan Purpose", ["All"] + sorted(df["LoanPurpose"].unique().tolist()))
with f2:
    emp_filter = st.selectbox("Employment Type", ["All"] + sorted(df["EmploymentType"].unique().tolist()))
with f3:
    risk_filter = st.selectbox("Risk Tier", ["All", "Low", "Medium", "High"])

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

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PORTFOLIO HEALTH
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="block-title">📊 Portfolio Health</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1: st.metric("Total Loans",     f"{total:,}")
with k2: st.metric("Default Rate",    f"{default_rate:.1f}%",
                   delta="Critical" if default_rate > 20 else "Watch" if default_rate > 12 else "Healthy",
                   delta_color="inverse" if default_rate > 12 else "normal")
with k3: st.metric("Avg Credit",      f"{avg_credit:.0f}",
                   delta="Risky — below 670" if avg_credit < 670 else "Safe — above 670",
                   delta_color="inverse" if avg_credit < 670 else "normal")
with k4: st.metric("Avg DTI Ratio",   f"{avg_dti:.2f}",
                   delta="Risky — above 0.5" if avg_dti > 0.5 else "Safe — below 0.5",
                   delta_color="inverse" if avg_dti > 0.5 else "normal")
with k5: st.metric("Avg LTI Ratio",   f"{avg_lti:.2f}",
                   delta="Overextended — above 4" if avg_lti > 4 else "Manageable",
                   delta_color="inverse" if avg_lti > 4 else "normal")
with k6: st.metric("High Risk Loans", f"{high_pct:.1f}%",
                   delta=f"{risk_counts.get('High', 0):,} loans in danger",
                   delta_color="inverse" if high_pct > 25 else "off")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — WHICH LOAN TYPE IS THE PROBLEM?
# NEW: Simple bar + Heatmap grid
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="block-title">🏦 Which Loan Type Is the Problem?</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # NEW: Simple clean horizontal bar — one number per loan type
    purpose_stats = filtered.groupby("LoanPurpose").agg(
        Count=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    purpose_stats["DefaultRate"] = (purpose_stats["Defaults"] / purpose_stats["Count"] * 100).round(1)
    purpose_stats = purpose_stats.sort_values("DefaultRate", ascending=True)

    bar_colors = [
        "#ff4560" if r > 20 else "#ffc145" if r > 12 else "#00d4aa"
        for r in purpose_stats["DefaultRate"]
    ]

    fig1 = go.Figure(go.Bar(
        x=purpose_stats["DefaultRate"],
        y=purpose_stats["LoanPurpose"],
        orientation="h",
        marker_color=bar_colors,
        text=[f"{r:.1f}%  ({c:,} loans)" for r, c in zip(purpose_stats["DefaultRate"], purpose_stats["Count"])],
        textposition="outside",
        textfont=dict(size=13),
    ))
    fig1.add_vline(x=12, line_dash="dash", line_color="#ffc145",
                   annotation_text="Watch (12%)", annotation_position="top right",
                   annotation_font=dict(color="#ffc145", size=11))
    fig1.add_vline(x=20, line_dash="dash", line_color="#ff4560",
                   annotation_text="Critical (20%)", annotation_position="top right",
                   annotation_font=dict(color="#ff4560", size=11))
    fig1.update_layout(
        **C,
        title="Default Rate by Loan Purpose",
        xaxis=dict(title="Default Rate %", gridcolor="#1e2736", range=[0, 40]),
        yaxis=dict(title=""),
        height=320,
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('<div class="hint">Green = healthy &nbsp;|&nbsp; Yellow = watch &nbsp;|&nbsp; Red = critical &nbsp;|&nbsp; Dashed lines show thresholds</div>', unsafe_allow_html=True)

with col2:
    fc = filtered.copy()
    # Keep the same buckets for readability
    fc["DTIBucket"] = pd.cut(fc["DTIRatio"],
        bins=[0, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0],
        labels=["Very Low", "Low", "Moderate", "High", "Very High", "Extreme"])
    fc["LTIBucket"] = pd.cut(fc["LTIRatio"].clip(upper=10),
        bins=[0, 1, 2, 4, 6, 10],
        labels=["Very Low", "Low", "Moderate", "High", "Extreme"])

    # Aggregate data
    bubble_data = fc.groupby(["DTIBucket", "LTIBucket"], observed=True).agg(
        TotalLoans=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    bubble_data["DefaultRate"] = (bubble_data["Defaults"] / bubble_data["TotalLoans"] * 100).round(1)

    # Map default rate to colors
    def color_map(rate):
        if rate > 20: return "#ff4560"    # Red = critical
        elif rate > 12: return "#ffc145"  # Yellow = watch
        else: return "#00d4aa"            # Green = safe

    bubble_data["Color"] = bubble_data["DefaultRate"].apply(color_map)

    # Bubble chart
    fig2 = px.scatter(
        bubble_data,
        x="DTIBucket",
        y="LTIBucket",
        size="TotalLoans",
        color="DefaultRate",
        color_continuous_scale=["#00d4aa", "#ffc145", "#ff4560"],
        hover_data={
            "DTIBucket": True,
            "LTIBucket": True,
            "TotalLoans": True,
            "Defaults": True,
            "DefaultRate": True,
        },
        size_max=40,
    )

    fig2.update_layout(
        **C,
        title="Loan Risk — DTI vs LTI Bubble Chart",
        xaxis=dict(title="DTI (Debt vs Income) → Higher = Risk", tickfont=dict(size=12)),
        yaxis=dict(title="LTI (Loan vs Income) ↑ Higher = Risk", tickfont=dict(size=12)),
        height=360,
        coloraxis_colorbar=dict(title="Default Rate %")
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="hint">Bubble size = number of loans &nbsp;|&nbsp; Color = default rate &nbsp;|&nbsp; Top-right bubbles = highest risk borrowers</div>', unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — WHO IS THE RISKY BORROWER?
# NEW: Line/step chart for credit + grouped vertical bars for employment
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="block-title">👤 Who Is the Risky Borrower?</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    # NEW: Step line chart — shows the drop in default rate as credit score rises
    fc2 = filtered.copy()
    fc2["CreditBand"] = pd.cut(fc2["CreditScore"],
        bins=[300, 500, 580, 670, 740, 851],
        labels=["300–500", "500–580", "580–670", "670–740", "740–850"])
    credit_stats = fc2.groupby("CreditBand", observed=True).agg(
        Total=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    credit_stats["DefaultRate"] = (credit_stats["Defaults"] / credit_stats["Total"] * 100).round(1)

    dot_colors = [
        "#ff4560" if r > 20 else "#ffc145" if r > 12 else "#00d4aa"
        for r in credit_stats["DefaultRate"]
    ]

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=credit_stats["CreditBand"].astype(str),
        y=credit_stats["DefaultRate"],
        mode="lines+markers+text",
        line=dict(color="#4f9eff", width=3, shape="spline"),
        marker=dict(size=14, color=dot_colors, line=dict(color="white", width=2)),
        text=credit_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
        textposition="top center",
        textfont=dict(size=13, color="white"),
    ))
    fig3.add_hrect(y0=0, y1=12, fillcolor="#00d4aa", opacity=0.05, line_width=0)
    fig3.add_hrect(y0=12, y1=20, fillcolor="#ffc145", opacity=0.05, line_width=0)
    fig3.add_hrect(y0=20, y1=50, fillcolor="#ff4560", opacity=0.05, line_width=0)
    fig3.add_hline(y=12, line_dash="dash", line_color="#ffc145",
                   annotation_text="Watch", annotation_font=dict(color="#ffc145", size=11))
    fig3.add_hline(y=20, line_dash="dash", line_color="#ff4560",
                   annotation_text="Critical", annotation_font=dict(color="#ff4560", size=11))
    fig3.update_layout(
        **C,
        title="Default Rate Drops as Credit Score Rises",
        xaxis=dict(title="Credit Score Band", tickfont=dict(size=12)),
        yaxis=dict(title="Default Rate %", gridcolor="#1e2736", range=[0, 50]),
        height=340,
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="hint">The line drops sharply after 670 — this is your approval threshold. Below it = high risk.</div>', unsafe_allow_html=True)

with col4:
    # NEW: Vertical bar chart with clear single color per employment type
    emp_stats = filtered.groupby("EmploymentType").agg(
        Total=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    emp_stats["DefaultRate"] = (emp_stats["Defaults"] / emp_stats["Total"] * 100).round(1)
    emp_stats = emp_stats.sort_values("DefaultRate", ascending=False)

    emp_colors = [
        "#ff4560" if r > 20 else "#ffc145" if r > 12 else "#00d4aa"
        for r in emp_stats["DefaultRate"]
    ]

    fig4 = go.Figure(go.Bar(
        x=emp_stats["EmploymentType"],
        y=emp_stats["DefaultRate"],
        marker_color=emp_colors,
        text=emp_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
        textfont=dict(size=14, color="white"),
        width=0.5,
    ))
    fig4.add_hline(y=12, line_dash="dash", line_color="#ffc145",
                   annotation_text="Watch (12%)", annotation_font=dict(color="#ffc145", size=11))
    fig4.add_hline(y=20, line_dash="dash", line_color="#ff4560",
                   annotation_text="Critical (20%)", annotation_font=dict(color="#ff4560", size=11))
    fig4.update_layout(
        **C,
        title="Default Rate by Employment Type",
        xaxis=dict(title="", tickfont=dict(size=13)),
        yaxis=dict(title="Default Rate %", gridcolor="#1e2736", range=[0, 55]),
        height=340,
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('<div class="hint">Unemployed borrowers default roughly 3x more than full-time borrowers</div>', unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — TWO QUICK WINS
# NEW: Grouped bar for co-signer + dot plot for education
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="block-title">💡 Two Quick Wins to Reduce Defaults</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    # NEW: Grouped bar — With vs Without co-signer per loan purpose
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
        name="With Co-Signer",
        x=purposes,
        y=[with_cs.get(p, 0) for p in purposes],
        marker_color="#00d4aa",
        text=[f"{with_cs.get(p,0):.1f}%" for p in purposes],
        textposition="outside",
        textfont=dict(size=12),
    ))
    fig5.add_trace(go.Bar(
        name="Without Co-Signer",
        x=purposes,
        y=[without_cs.get(p, 0) for p in purposes],
        marker_color="#ff4560",
        text=[f"{without_cs.get(p,0):.1f}%" for p in purposes],
        textposition="outside",
        textfont=dict(size=12),
    ))
    fig5.update_layout(
        **C,
        title="Co-Signer Cuts Default Rate — by Loan Purpose",
        barmode="group",
        xaxis=dict(title="", tickfont=dict(size=12)),
        yaxis=dict(title="Default Rate %", gridcolor="#1e2736", range=[0, 40]),
        legend=dict(bgcolor="#0e1117", font=dict(size=12)),
        height=360,
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('<div class="hint">Green bars are always lower than red bars — co-signer reduces risk in every loan type</div>', unsafe_allow_html=True)

with col6:
    # NEW: Dot plot — education level on a line, easy to see the gap
    edu_order = ["PhD", "Master's", "Bachelor's", "High School"]
    edu_stats = filtered.groupby("Education").agg(
        Total=("Default", "count"),
        Defaults=("Default", "sum")
    ).reset_index()
    edu_stats["DefaultRate"] = (edu_stats["Defaults"] / edu_stats["Total"] * 100).round(1)
    edu_stats["Education"]   = pd.Categorical(edu_stats["Education"], categories=edu_order, ordered=True)
    edu_stats = edu_stats.sort_values("Education")

    dot_colors = [
        "#ff4560" if r > 20 else "#ffc145" if r > 12 else "#00d4aa"
        for r in edu_stats["DefaultRate"]
    ]

    fig6 = go.Figure()
    # Connecting line
    fig6.add_trace(go.Scatter(
        x=edu_stats["Education"].astype(str),
        y=edu_stats["DefaultRate"],
        mode="lines",
        line=dict(color="#2d3748", width=3),
        showlegend=False,
    ))
    # Dots
    fig6.add_trace(go.Scatter(
        x=edu_stats["Education"].astype(str),
        y=edu_stats["DefaultRate"],
        mode="markers+text",
        marker=dict(size=22, color=dot_colors, line=dict(color="white", width=2)),
        text=edu_stats["DefaultRate"].apply(lambda x: f"{x:.1f}%"),
        textposition="top center",
        textfont=dict(size=13, color="white"),
        showlegend=False,
    ))
    # Count labels below dots
    for _, row in edu_stats.iterrows():
        fig6.add_annotation(
            x=str(row["Education"]),
            y=row["DefaultRate"] - 3.5,
            text=f"{row['Total']:,} loans",
            showarrow=False,
            font=dict(size=11, color="#718096"),
        )
    fig6.add_hrect(y0=0,  y1=12, fillcolor="#00d4aa", opacity=0.05, line_width=0)
    fig6.add_hrect(y0=12, y1=20, fillcolor="#ffc145", opacity=0.05, line_width=0)
    fig6.add_hrect(y0=20, y1=50, fillcolor="#ff4560", opacity=0.05, line_width=0)
    fig6.update_layout(
        **C,
        title="Default Rate by Education Level",
        xaxis=dict(title="", tickfont=dict(size=13)),
        yaxis=dict(title="Default Rate %", gridcolor="#1e2736", range=[0, 45]),
        height=360,
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('<div class="hint">Each dot = one education group &nbsp;|&nbsp; Green = safe &nbsp;|&nbsp; Red = high risk &nbsp;|&nbsp; Number below = loan count</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Loan Risk Dashboard · Filters: Loan Purpose | Employment Type | Risk Tier")