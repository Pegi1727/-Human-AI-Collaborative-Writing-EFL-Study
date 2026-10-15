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
Script 08 - Adjusted means and 95% CIs (Table 7).

ANCOVA-adjusted group means for all three outcomes, evaluated at the grand
mean of each covariate, with standard errors and 95% CIs.

Run:  python 08_adjusted_means_table7.py
"""
from scipy import stats


def adjusted_means(df, post, pre):
    d = df[[post, pre, "Group"]].dropna().copy()
    d["Trt"] = (d["Group"] == "Experimental").astype(float)
    n = len(d)
    X = np.column_stack([np.ones(n), d["Trt"], d[pre]])
    y = d[post].values
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    mse = (resid ** 2).sum() / (n - 3)
    cov = mse * np.linalg.inv(X.T @ X)
    gm = d[pre].mean()
    rows = []
    tcrit = stats.t.ppf(0.975, n - 3)
    for g, trt in [("Experimental", 1.0), ("Control", 0.0)]:
        mean = beta[0] + beta[1] * trt + beta[2] * gm
        x0 = np.array([1.0, trt, gm])
        se = float(np.sqrt(x0 @ cov @ x0))
        rows.append({"Outcome": post, "Group": g, "Covariate": pre,
                     "Covariate_grand_mean": round(gm, 2),
                     "Adjusted_Mean": round(mean, 2), "SE": round(se, 2),
                     "CI95_low": round(mean - tcrit * se, 2),
                     "CI95_high": round(mean + tcrit * se, 2)})
    return rows


def main():
    df = ensure_writing_100(load_data())
    rows = []
    for post, pre in [("Writing_Post", "Writing_Pre"),
                      ("SRL_Post", "SRL_Pre"),
                      ("AI_Post", "AI_Pre")]:
        rows.extend(adjusted_means(df, post, pre))
    table7 = pd.DataFrame(rows)
    out_dir = make_output_dir()
    out = os.path.join(out_dir, "table7_adjusted_means.csv")
    table7.to_csv(out, index=False)
    print("[OK] Table 7 saved to:", out)
    print(table7.to_string(index=False))


if __name__ == "__main__":
    main()

