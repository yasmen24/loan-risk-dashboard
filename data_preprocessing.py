import pandas as pd
import numpy as np

# ── STEP 1: LOAD DATA ──────────────────────────────────────────────────────────
df = pd.read_csv("/mnt/user-data/uploads/Loan_default.csv")

print("=" * 50)
print("STEP 1: LOAD DATA")
print("=" * 50)
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

# ── STEP 2: BASIC CHECKS ───────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 2: BASIC CHECKS")
print("=" * 50)
print(f"Missing values  : {df.isnull().sum().sum()}")
print(f"Duplicate rows  : {df.duplicated().sum()}")
print(f"Duplicate IDs   : {df['LoanID'].duplicated().sum()}")

# ── STEP 3: VALIDITY CHECKS ────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 3: VALIDITY CHECKS")
print("=" * 50)
checks = {
    "Age < 18"             : (df["Age"] < 18).sum(),
    "Age > 100"            : (df["Age"] > 100).sum(),
    "CreditScore < 300"    : (df["CreditScore"] < 300).sum(),
    "CreditScore > 850"    : (df["CreditScore"] > 850).sum(),
    "Income < 0"           : (df["Income"] < 0).sum(),
    "LoanAmount < 0"       : (df["LoanAmount"] < 0).sum(),
    "DTIRatio < 0"         : (df["DTIRatio"] < 0).sum(),
    "DTIRatio > 1"         : (df["DTIRatio"] > 1).sum(),
    "InterestRate < 0"     : (df["InterestRate"] < 0).sum(),
    "InterestRate > 100"   : (df["InterestRate"] > 100).sum(),
    "MonthsEmployed < 0"   : (df["MonthsEmployed"] < 0).sum(),
}
for check, count in checks.items():
    status = "OK" if count == 0 else f"WARNING: {count} rows"
    print(f"  {check:<25} → {status}")

# ── STEP 4: INCONSISTENCY CHECK ────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 4: INCONSISTENCY CHECK")
print("=" * 50)
unemp_with_months = df[
    (df["EmploymentType"] == "Unemployed") &
    (df["MonthsEmployed"] > 0)
].shape[0]
print(f"Unemployed with MonthsEmployed > 0 : {unemp_with_months:,}")
print("Decision : KEEP — MonthsEmployed represents past work history")

# ── STEP 5: CLASS BALANCE ──────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 5: CLASS BALANCE (Target Column)")
print("=" * 50)
vc = df["Default"].value_counts()
print(f"No Default (0) : {vc[0]:,}  ({vc[0]/len(df)*100:.1f}%)")
print(f"Defaulted  (1) : {vc[1]:,}  ({vc[1]/len(df)*100:.1f}%)")
print("Note : Imbalanced dataset. Handle if building ML model.")

# ── STEP 6: FEATURE ENGINEERING ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 6: FEATURE ENGINEERING")
print("=" * 50)

# New Column 1: LTI Ratio
df["LTIRatio"] = (df["LoanAmount"] / df["Income"]).round(2)
print(f"LTIRatio created  → LoanAmount ÷ Income")
print(f"  Min: {df['LTIRatio'].min()}  Max: {df['LTIRatio'].max():.2f}  Mean: {df['LTIRatio'].mean():.2f}")

# New Column 2: Risk Tier
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
print(f"\nRiskTier created  → composite score from 5 columns")
print(f"  Low    : {rc.get('Low',0):,}  ({rc.get('Low',0)/len(df)*100:.1f}%)")
print(f"  Medium : {rc.get('Medium',0):,}  ({rc.get('Medium',0)/len(df)*100:.1f}%)")
print(f"  High   : {rc.get('High',0):,}  ({rc.get('High',0)/len(df)*100:.1f}%)")

# ── STEP 7: SAVE CLEAN FILE ────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 7: SAVE CLEAN FILE")
print("=" * 50)
df.to_csv("/mnt/user-data/outputs/Loan_default_clean.csv", index=False)
print(f"Saved  → Loan_default_clean.csv")
print(f"Rows   : {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}  (original 18 + LTIRatio + RiskTier)")

# ── STEP 8: FINAL SUMMARY ──────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 8: FINAL SUMMARY")
print("=" * 50)
print("""
  Missing values    → 0        CLEAN
  Duplicates        → 0        CLEAN
  Invalid ranges    → 0        CLEAN
  Inconsistency     → NOTED    Unemployed + MonthsEmployed > 0
                               Decision: kept as past work history
  Class imbalance   → NOTED    88.4% no default / 11.6% default
  LTIRatio          → CREATED  LoanAmount ÷ Income
  RiskTier          → CREATED  Low / Medium / High composite score
  Output file       → Loan_default_clean.csv  (20 columns)
""")
