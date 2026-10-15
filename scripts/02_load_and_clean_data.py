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
Script 02 - Load and clean data.

Loads the raw CSV, validates columns/groups, harmonises the 25-vs-100 point
writing scale, removes duplicates and impossible values, adds gain scores,
and saves a clean analysis-ready CSV.

Run:  python 02_load_and_clean_data.py
"""


def main():
    df = load_data()

    n0 = len(df)
    df = df.drop_duplicates(subset="ID").reset_index(drop=True)
    if len(df) < n0:
        print(f"[INFO] Removed {n0 - len(df)} duplicate ID rows.")

    for col in EXPECTED_COLUMNS[2:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["SRL_Pre", "SRL_Post", "AI_Pre", "AI_Post"]:
        bad = df[col].notna() & ((df[col] < 1) | (df[col] > 5))
        if bad.sum():
            print(f"[WARN] {bad.sum()} value(s) of {col} outside 1-5 range -> set to NaN.")
            df.loc[bad, col] = np.nan

    df = ensure_writing_100(df)

    df["Writing_Gain"] = df["Writing_Post"] - df["Writing_Pre"]
    df["SRL_Gain"] = df["SRL_Post"] - df["SRL_Pre"]
    df["AI_Gain"] = df["AI_Post"] - df["AI_Pre"]

    out_dir = make_output_dir()
    out_csv = os.path.join(out_dir, "clean_data.csv")
    df.to_csv(out_csv, index=False)
    print(f"\n[OK] Clean data saved to: {out_csv}")
    print(df.describe().T.round(2).to_string())
    return df


if __name__ == "__main__":
    main()

