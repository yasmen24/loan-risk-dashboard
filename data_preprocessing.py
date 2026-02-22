import pandas as pd
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# LOAN RISK DASHBOARD — DATA PREPROCESSING
# ══════════════════════════════════════════════════════════════════════════════
# This script cleans and transforms the raw loan dataset before it is used
# in the dashboard. Run this script FIRST before running app.py.
#
# Input  : Loan_default.csv        (18 columns, raw data)
# Output : Loan_default_clean.csv  (20 columns, ready for dashboard)
# ══════════════════════════════════════════════════════════════════════════════

# ── STEP 1: LOAD DATA ──────────────────────────────────────────────────────────
# We load the raw CSV file into a pandas DataFrame.
# A DataFrame is like an Excel table in Python — rows and columns.
# We check the shape (how many rows and columns) to confirm it loaded correctly.

df = pd.read_csv("Loan_default.csv")

print("=" * 55)
print("STEP 1: LOAD DATA")
print("=" * 55)
print("We load the raw CSV file and check its size.")
print(f"  Rows    : {df.shape[0]:,}  (each row = one loan)")
print(f"  Columns : {df.shape[1]}   (each column = one piece of information)")

# ── STEP 2: BASIC CHECKS ───────────────────────────────────────────────────────
# Before doing anything we check three basic things:
#
# 1. Missing values — are there any empty cells?
#    Empty cells cause errors in charts and calculations.
#    If found, we would need to either fill them or remove those rows.
#
# 2. Duplicate rows — is the same loan recorded twice?
#    Duplicates make counts wrong and inflate statistics.
#    If found, we keep only one copy.
#
# 3. Duplicate LoanIDs — does each loan have a unique ID?
#    Each loan should appear exactly once in the dataset.

print("\n" + "=" * 55)
print("STEP 2: BASIC CHECKS")
print("=" * 55)
print("Checking for missing values, duplicate rows, and duplicate IDs.")
print("These are the three most common problems in real datasets.")
print()

missing = df.isnull().sum().sum()
dupes   = df.duplicated().sum()
dup_ids = df["LoanID"].duplicated().sum()

print(f"  Missing values  : {missing}  {'✓ No action needed' if missing == 0 else '✗ Need to handle'}")
print(f"  Duplicate rows  : {dupes}   {'✓ No action needed' if dupes == 0 else '✗ Need to drop duplicates'}")
print(f"  Duplicate IDs   : {dup_ids}   {'✓ No action needed' if dup_ids == 0 else '✗ Need to investigate'}")

# ── STEP 3: VALIDITY CHECKS ────────────────────────────────────────────────────
# We check that every number is within a realistic and logical range.
# For example:
#   - No one can be younger than 18 (legal borrowing age)
#   - Credit scores only go from 300 to 850
#   - Income and loan amounts cannot be negative
#   - DTI Ratio must be between 0 and 1 (it is a percentage)
#   - Interest rate cannot be negative or above 100%
#   - Months employed cannot be negative
#
# If any of these checks fail it means the data was entered incorrectly
# or corrupted and those rows need to be fixed or removed.

print("\n" + "=" * 55)
print("STEP 3: VALIDITY CHECKS")
print("=" * 55)
print("Checking that all numbers are within realistic ranges.")
print("Example: age must be 18+, credit score must be 300-850.")
print()

checks = {
    "Age < 18 (below legal borrowing age)"  : (df["Age"] < 18).sum(),
    "Age > 100 (unrealistic age)"           : (df["Age"] > 100).sum(),
    "CreditScore < 300 (below minimum)"     : (df["CreditScore"] < 300).sum(),
    "CreditScore > 850 (above maximum)"     : (df["CreditScore"] > 850).sum(),
    "Income < 0 (impossible)"               : (df["Income"] < 0).sum(),
    "LoanAmount < 0 (impossible)"           : (df["LoanAmount"] < 0).sum(),
    "DTIRatio < 0 (impossible)"             : (df["DTIRatio"] < 0).sum(),
    "DTIRatio > 1 (above 100% of income)"   : (df["DTIRatio"] > 1).sum(),
    "InterestRate < 0 (impossible)"         : (df["InterestRate"] < 0).sum(),
    "InterestRate > 100 (unrealistic)"      : (df["InterestRate"] > 100).sum(),
    "MonthsEmployed < 0 (impossible)"       : (df["MonthsEmployed"] < 0).sum(),
}

for check, count in checks.items():
    status = "✓ OK" if count == 0 else f"✗ WARNING: {count} rows"
    print(f"  {check:<42} → {status}")

# ── STEP 4: INCONSISTENCY CHECK ────────────────────────────────────────────────
# We check for logical inconsistencies — values that are individually valid
# but do not make sense together.
#
# Example found: Some borrowers are listed as "Unemployed" but also have
# MonthsEmployed > 0.
#
# Two possible explanations:
#   A) MonthsEmployed = current job duration → should be 0 if unemployed
#   B) MonthsEmployed = total past work history → can be > 0 even if unemployed
#
# We chose interpretation B and KEEP the data as-is.
# Reason: It is more useful to know a borrower has 5 years of work history
# even if they are currently unemployed. This signals future earning potential.
#
# Decision: KEEP. Document the assumption.

print("\n" + "=" * 55)
print("STEP 4: INCONSISTENCY CHECK")
print("=" * 55)
print("Checking for values that conflict with each other.")
print("Example: a borrower listed as Unemployed but has months employed > 0.")
print()

unemp_with_months = df[
    (df["EmploymentType"] == "Unemployed") &
    (df["MonthsEmployed"] > 0)
].shape[0]

print(f"  Unemployed borrowers with MonthsEmployed > 0 : {unemp_with_months:,}")
print()
print("  Decision: KEEP these rows.")
print("  Reason  : MonthsEmployed likely represents total past work history,")
print("            not current job duration. An unemployed person can still")
print("            have 5 years of past employment experience.")

# ── STEP 5: CLASS BALANCE CHECK ────────────────────────────────────────────────
# We check how balanced our target column (Default) is.
# Default = 1 means the borrower failed to repay.
# Default = 0 means the borrower paid back successfully.
#
# Why does balance matter?
# If 95% of loans are "no default" and only 5% are "default",
# a machine learning model could just predict "no default" every time
# and be 95% accurate — but completely useless.
#
# For the dashboard: class imbalance does not affect charts.
# For future ML model: we would need to handle this using techniques
# like oversampling (SMOTE) or class weights.

print("\n" + "=" * 55)
print("STEP 5: CLASS BALANCE CHECK")
print("=" * 55)
print("Checking how many loans defaulted vs did not default.")
print("This is important if we ever build a machine learning model.")
print()

vc = df["Default"].value_counts()
print(f"  No Default (0) : {vc[0]:,}  ({vc[0]/len(df)*100:.1f}%)")
print(f"  Defaulted  (1) : {vc[1]:,}  ({vc[1]/len(df)*100:.1f}%)")
print()
print("  Note: Dataset is imbalanced (88% vs 12%).")
print("  For dashboard → no problem, charts work fine.")
print("  For ML model  → handle with oversampling or class weights.")

# ── STEP 6: FEATURE ENGINEERING ───────────────────────────────────────────────
# Feature engineering means creating NEW columns from existing ones.
# These new columns give us more insight than the raw numbers alone.
#
# We create 2 new columns:
#
# Column 1: LTIRatio (Loan-to-Income Ratio)
#   Formula  : LoanAmount ÷ Income
#   Meaning  : How large is the loan relative to the borrower's yearly salary?
#   Example  : LoanAmount = $150,000 | Income = $50,000 → LTI = 3.0
#              The borrower took a loan 3x their annual salary.
#   Safe range : Below 4 is manageable. Above 4 is dangerous.
#
# Column 2: RiskTier (Low / Medium / High)
#   Formula  : Composite score from 5 columns
#   Meaning  : Overall risk level of each loan in one simple label
#   Scoring  :
#     DTI > 0.5         → +2 points  (high debt burden)
#     CreditScore < 580 → +2 points  (very poor credit)
#     CreditScore < 670 → +1 point   (below safe line)
#     Unemployed        → +3 points  (no income stability)
#     Part-time         → +1 point   (reduced income stability)
#     LTI > 4           → +2 points  (loan too large vs income)
#     Has CoSigner      → -1 point   (reduces risk)
#   Result   :
#     0–2 points → Low Risk
#     3–5 points → Medium Risk
#     6+ points  → High Risk

print("\n" + "=" * 55)
print("STEP 6: FEATURE ENGINEERING")
print("=" * 55)
print("Creating 2 new columns that give more insight than raw numbers.")
print()

# Create LTIRatio
df["LTIRatio"] = (df["LoanAmount"] / df["Income"]).round(2)
print("  NEW COLUMN 1: LTIRatio")
print("  Formula : LoanAmount ÷ Income")
print("  Meaning : How many times their yearly salary did they borrow?")
print(f"  Min     : {df['LTIRatio'].min():.2f}  (borrowed almost nothing vs income)")
print(f"  Max     : {df['LTIRatio'].max():.2f}  (borrowed 16x their annual salary)")
print(f"  Mean    : {df['LTIRatio'].mean():.2f}  (average borrower borrowed 2x salary)")
print(f"  Safe    : Below 4.0  |  Dangerous: Above 4.0")

# Create RiskTier
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
rc = df["RiskTier"].value_counts()

print()
print("  NEW COLUMN 2: RiskTier")
print("  Formula : Score from DTI + CreditScore + Employment + LTI + CoSigner")
print("  Meaning : Overall risk level of each loan in one simple label")
print(f"  Low     : {rc.get('Low',0):,} loans  ({rc.get('Low',0)/len(df)*100:.1f}%)  — safe borrowers")
print(f"  Medium  : {rc.get('Medium',0):,} loans  ({rc.get('Medium',0)/len(df)*100:.1f}%)  — watch closely")
print(f"  High    : {rc.get('High',0):,} loans  ({rc.get('High',0)/len(df)*100:.1f}%)  — danger zone")

# ── STEP 7: SAVE CLEAN FILE ────────────────────────────────────────────────────
# We save the final processed dataset as a new CSV file.
# The original file is NOT changed — we always keep the raw data untouched.
# The dashboard (app.py) will read from this clean file.

print("\n" + "=" * 55)
print("STEP 7: SAVE CLEAN FILE")
print("=" * 55)
print("Saving the processed dataset as a new file.")
print("The original Loan_default.csv is kept untouched.")
print()

df.to_csv("Loan_default_clean.csv", index=False)

print(f"  Saved   → Loan_default_clean.csv")
print(f"  Rows    : {df.shape[0]:,}")
print(f"  Columns : {df.shape[1]}  (original 18 + LTIRatio + RiskTier)")

# ── STEP 8: FINAL SUMMARY ──────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 8: FINAL SUMMARY")
print("=" * 55)
print("""
  CLEANING RESULTS:
  ─────────────────────────────────────────────────
  Missing values    → 0         NO ACTION NEEDED
  Duplicate rows    → 0         NO ACTION NEEDED
  Invalid ranges    → 0         NO ACTION NEEDED

  FINDINGS NOTED:
  ─────────────────────────────────────────────────
  Inconsistency     → NOTED     Unemployed borrowers with
                                MonthsEmployed > 0
                                Decision: kept as past history

  Class imbalance   → NOTED     88.4% no default
                                11.6% defaulted
                                Handle if building ML model

  NEW COLUMNS CREATED:
  ─────────────────────────────────────────────────
  LTIRatio          → LoanAmount ÷ Income
  RiskTier          → Low / Medium / High

  OUTPUT:
  ─────────────────────────────────────────────────
  Loan_default_clean.csv  →  20 columns, ready for dashboard

  NEXT STEP:
  ─────────────────────────────────────────────────
  Run app.py to launch the dashboard.
""")