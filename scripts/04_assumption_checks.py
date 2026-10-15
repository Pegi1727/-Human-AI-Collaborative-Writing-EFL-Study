# ---------------------------------------------------------------
# Study: NCAL-2026-1259 (Computer Assisted Language Learning)
# EFL writing / SRL / AI-literacy study: Experimental vs Control
# ---------------------------------------------------------------
import os, sys
import numpy as np
import pandas as pd

DATA_CANDIDATES = [
    "data/raw/Hypothetical_EFL_AI_Study_Data.csv",
    "data/Hypothetical_EFL_AI_Study_Data.csv",
    "Hypothetical_EFL_AI_Study_Data.csv",
    "/mnt/data/Hypothetical_EFL_AI_Study_Data.csv",
]

EXPECTED_COLUMNS = ["ID", "Group",
                    "Writing_Pre", "Writing_Post",
                    "SRL_Pre", "SRL_Post",
                    "AI_Pre", "AI_Post"]


def find_data_file(verbose=True):
    """Return the first existing data-file path among standard candidates."""
    for path in DATA_CANDIDATES:
        if os.path.exists(path):
            if verbose:
                print(f"[INFO] Data file found: {path}")
            return path
    raise FileNotFoundError("Data file not found. Looked in: " + ", ".join(DATA_CANDIDATES))


def load_data(path=None):
    """Load the study data and validate required columns."""
    path = path or find_data_file()
    df = pd.read_csv(path)
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")
    df["Group"] = df["Group"].astype(str).str.strip().str.capitalize()
    print(f"[INFO] Loaded {len(df)} rows; groups:")
    print(df["Group"].value_counts())
    return df


def ensure_writing_100(df):
    """Support both 25-point raw rubric scores and 100-point scores.

    If Writing values look like a raw 25-point rubric (max <= 25), rescale x4.
    Otherwise treat them as 100-point scores and use them directly.
    """
    df = df.copy()
    for col in ["Writing_Pre", "Writing_Post"]:
        if df[col].max() <= 25:
            print(f"[INFO] {col} appears to be a raw 25-point rubric score -> rescaled (x4) to 100.")
            df[col] = df[col] * 4
        else:
            print(f"[INFO] {col} treated as a 100-point score (used directly).")
    return df


def make_output_dir(name="outputs"):
    os.makedirs(name, exist_ok=True)
    return name


"""
Script 04 - ANCOVA assumption checks.

Per outcome (Writing_Post, SRL_Post, AI_Post) with its pre-test covariate:
  1. Normality: Shapiro-Wilk per group on post scores.
  2. Homogeneity of variance: Levene's test.
  3. Homogeneity of regression slopes: compares per-group slopes; Fisher-z
     test on the correlation difference as an interaction proxy.
  4. Linearity: Pearson r between covariate and outcome per group.

Run:  python 04_assumption_checks.py
"""
from scipy import stats


def main():
    df = ensure_writing_100(load_data())
    pairs = [("Writing_Post", "Writing_Pre"),
             ("SRL_Post", "SRL_Pre"),
             ("AI_Post", "AI_Pre")]
    rows = []
    for post, pre in pairs:
        e = df[df["Group"] == "Experimental"]
        c = df[df["Group"] == "Control"]
        sw_e = stats.shapiro(e[post].dropna())
        sw_c = stats.shapiro(c[post].dropna())
        lev = stats.levene(e[post].dropna(), c[post].dropna(), center="mean")

        def slope_r(g):
            r, _ = stats.pearsonr(g[pre], g[post])
            b = r * g[post].std(ddof=1) / g[pre].std(ddof=1)
            return b, r

        b_e, r_e = slope_r(e)
        b_c, r_c = slope_r(c)
        z = (np.arctanh(r_e) - np.arctanh(r_c)) / np.sqrt(1/(len(e)-3) + 1/(len(c)-3))
        p_slope = 2 * (1 - stats.norm.cdf(abs(z)))
        rows.append({"Outcome": post, "Covariate": pre,
                     "Shapiro_E_W": round(sw_e.statistic, 3), "Shapiro_E_p": round(sw_e.pvalue, 3),
                     "Shapiro_C_W": round(sw_c.statistic, 3), "Shapiro_C_p": round(sw_c.pvalue, 3),
                     "Levene_F": round(lev.statistic, 3), "Levene_p": round(lev.pvalue, 3),
                     "Slope_E": round(b_e, 3), "Slope_C": round(b_c, 3),
                     "SlopeHomog_p": round(p_slope, 3),
                     "r_E": round(r_e, 3), "r_C": round(r_c, 3)})
    checks = pd.DataFrame(rows)
    out_dir = make_output_dir()
    out = os.path.join(out_dir, "assumption_checks.csv")
    checks.to_csv(out, index=False)
    print("[OK] Assumption checks saved to:", out)
    print(checks.to_string(index=False))
    print("\nGuidance: p > .05 for Shapiro / Levene / SlopeHomog indicates the assumption holds.")


if __name__ == "__main__":
    main()

