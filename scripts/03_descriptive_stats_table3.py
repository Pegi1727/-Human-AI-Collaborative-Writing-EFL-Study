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
Script 03 - Descriptive statistics (Table 3).

Produces N, Mean, SD, SE, Min, Max and 95% CI per group for Writing, SRL,
and AI-literacy (pre/post), saved as a publication-ready CSV.

Run:  python 03_descriptive_stats_table3.py
"""


def describe_group(g):
    rows = []
    for col in ["Writing_Pre", "Writing_Post", "SRL_Pre", "SRL_Post", "AI_Pre", "AI_Post"]:
        x = g[col].dropna()
        mean, sd = x.mean(), x.std(ddof=1)
        se = sd / np.sqrt(len(x))
        ci = 1.96 * se
        rows.append({"Variable": col, "N": len(x), "Mean": round(mean, 2),
                     "SD": round(sd, 2), "SE": round(se, 2),
                     "Min": round(x.min(), 2), "Max": round(x.max(), 2),
                     "CI95_low": round(mean - ci, 2), "CI95_high": round(mean + ci, 2)})
    return pd.DataFrame(rows)


def main():
    df = ensure_writing_100(load_data())
    tables = []
    for grp in ["Experimental", "Control"]:
        t = describe_group(df[df["Group"] == grp])
        t.insert(0, "Group", grp)
        tables.append(t)
    table3 = pd.concat(tables, ignore_index=True)

    out_dir = make_output_dir()
    out = os.path.join(out_dir, "table3_descriptive_statistics.csv")
    table3.to_csv(out, index=False)
    print("[OK] Table 3 saved to:", out)
    print(table3.to_string(index=False))


if __name__ == "__main__":
    main()

