# 💳 Loan Risk Dashboard

---

## 📌 Project Overview

Credit default is one of the most consequential risks a lending institution faces. A single percentage point increase in the default rate can wipe out significant portfolio value, yet many lenders still rely on intuition or siloed reports to make approval decisions. Traditionally, understanding loan risk required analysts to spend considerable time manually gathering data from disparate sources, cross-referencing borrower records, and running reports that were often outdated by the time they reached decision-makers. This slow, fragmented process is not just inefficient — it is dangerous. Delayed or incomplete risk analysis can lead to catastrophic outcomes, including mass defaults across an unmonitored segment, cascading portfolio losses, and in severe cases, institutional insolvency. This project set out to address that gap by answering a deceptively simple question: *who defaults, and why — and how quickly can we see it?*

The Loan Risk Dashboard is an interactive, real-time analytical tool built to give loan officers, risk analysts, and portfolio managers a clear, evidence-based view of default risk across their loan book. By replacing slow manual analysis with an always-current visual interface, it eliminates the lag between when risk emerges and when it is detected. Rather than presenting raw numbers in isolation, the dashboard surfaces the relationships between borrower characteristics — credit score, income ratios, employment status, education level, and co-signer presence — and actual default outcomes. The goal is not just to describe the past but to give decision-makers the pattern recognition they need to act before a manageable problem becomes a catastrophic one.

---

## 🗂️ Data Source

The dataset was sourced from Kaggle — specifically the [Loan Default dataset](https://www.kaggle.com/datasets/nikhil1e9/loan-default/data) published by Nikhil1e9. It contains individual-level borrower records covering financial attributes such as credit score, debt-to-income ratio, and loan amount, as well as demographic information including employment type, education level, and co-signer status. Each record also includes the loan purpose and a binary default outcome indicating whether the loan was repaid or defaulted on. Before being used in the dashboard, the data was cleaned and transformed in a separate `data_preprocessing.py` script — where two additional features were engineered: `LTIRatio` (loan amount divided by annual income) and `RiskTier` (a composite Low/Medium/High risk classification) — and saved as `Loan_default_clean.csv`.

---

## 🔬 Steps & Methodology

The project moved through five clear stages to go from raw data to a working dashboard.

**Data Cleaning** — The raw dataset came in clean: no missing values, no duplicate rows, and no duplicate IDs, so no records needed to be removed or filled in. All numerical fields were validated against realistic ranges — credit scores between 300 and 850, ages between 18 and 100, and all financial values above zero. One inconsistency was found: 63,292 borrowers were marked as unemployed but had employment history recorded. These were kept, as the field likely captures past work experience rather than current job status.

**Transformation** — Two new columns were created to make the data more useful for analysis. `LTIRatio` (Loan-to-Income) divides the loan amount by the borrower's annual income, showing how much they borrowed relative to what they earn — values above 4.0 are considered dangerous. `RiskTier` combines five factors (DTI, credit score, employment type, LTI, and co-signer presence) into a single Low, Medium, or High risk label for each borrower. The final clean file contains 255,347 rows and 20 columns.

**Analysis Approach** — Default rate was used as the single consistent metric across all charts, defined as the percentage of loans that ended in default within each group. Two threshold lines — 12% (Watch) and 20% (Critical) — appear on every chart so comparisons are always meaningful and immediate.

**Tool Selection** — Python was used throughout. Pandas handled all data loading and aggregation, Streamlit powered the web application, and Plotly was chosen for all charts due to its interactivity and precise layout control. The preprocessing logic was kept in a separate script (`data_preprocessing.py`) to keep the dashboard code clean.

**Design Decisions** — The entire dashboard follows one rule: a user should understand the risk within seconds of opening it. Every chart uses the same three-colour system — green for healthy, amber for watch, red for critical. Three filters at the top (loan purpose, employment type, risk tier) let users instantly narrow the view to any segment they care about.

---

## 📸 Dashboard Screenshots

<img width="2874" height="1264" alt="image" src="https://github.com/user-attachments/assets/0b5914bd-9e85-4c02-b99c-b469172f930f" />
<img width="2874" height="1264" alt="image" src="https://github.com/user-attachments/assets/eb63b7be-0470-4995-af4a-7f6b89ffbccd" />

---

## 🖌️ Design Screenshots

<img width="1000" height="1087" alt="image" src="https://github.com/user-attachments/assets/34c5cbe4-d72d-4f2f-b73a-befaf1861145" />


---

## 💡 Key Insights

The dashboard reveals four insights that any lender should act on.

**1. Credit score is your best filter.** The data is clear — borrowers below 580 default at nearly three times the rate of those above 670. The decline is steep, consistent, and holds across every loan type. A minimum credit score threshold of 670 is the single most impactful change a lender can make to reduce portfolio risk.

**2. Unemployed borrowers carry outsized risk.** Regardless of loan purpose or amount, unemployed borrowers default roughly three times more than full-time employees. Approving loans for unemployed applicants without additional safeguards is one of the clearest risk exposures in the portfolio.

**3. A co-signer is a simple safety net.** Across every loan category — home, auto, education, business — loans with a co-signer consistently default less, often by 5 to 8 percentage points. It costs nothing to require one, and the data shows it works every time.

**4. Watch borrowers who are stretched on both ratios.** When a borrower has both a high Debt-to-Income ratio and a high Loan-to-Income ratio, they are under pressure from two directions at once — too much existing debt and too large a new loan relative to their income. This combination produces the highest default rates in the entire dataset and should always trigger a manual review.

---

## 🔗 Live Dashboard Link

🔗 [View Live Dashboard](https://loan-risk-dashboard-kh6ffmvnedqvuokl4m63ux.streamlit.app/#loan-risk-dashboard)

---

## ⚠️ Assumptions & Limitations

Several assumptions underpin the analysis. The binary `Default` column is treated as a clean, verified outcome label — no attempt was made to audit or validate individual records, so any labeling errors in the source data propagate directly into the default rates shown. The risk tier thresholds (12% and 20%) were chosen based on common industry benchmarks rather than derived statistically from this specific dataset, which means they may not be optimally calibrated for every lender's risk appetite.

The dataset does not include a time dimension, so it is not possible to assess whether default patterns have shifted over time or whether the portfolio has seasonal characteristics. Similarly, the data does not capture loan officer behavior, regional economic conditions, or macroeconomic context — all of which influence default rates in practice. The dashboard is best interpreted as a diagnostic tool for understanding structural risk drivers within the existing portfolio, not as a predictive model for future defaults.
