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
Script 01 - Validate environment.

Checks Python version, required libraries, working directory, presence of the
data file, and basic data integrity for study NCAL-2026-1259.
Run:  python 01_validate_environment.py
"""


def main():
    print("=" * 60)
    print("ENVIRONMENT VALIDATION - NCAL-2026-1259")
    print("=" * 60)

    print(f"Python version : {sys.version.split()[0]}")
    assert sys.version_info >= (3, 8), "Python >= 3.8 required."

    import scipy, matplotlib, seaborn
    print(f"numpy      : {np.__version__}")
    print(f"pandas     : {pd.__version__}")
    print(f"scipy      : {scipy.__version__}")
    print(f"matplotlib : {matplotlib.__version__}")
    print(f"seaborn    : {seaborn.__version__}")

    print(f"Working dir: {os.getcwd()}")
    find_data_file(verbose=False)

    df = load_data()
    assert set(EXPECTED_COLUMNS).issubset(df.columns)
    assert set(df["Group"].unique()) == {"Experimental", "Control"}, \
        "Group must contain exactly 'Experimental' and 'Control'."
    n_per_group = df.groupby("Group").size().to_dict()
    print(f"Per-group N: {n_per_group}")
    assert all(v >= 2 for v in n_per_group.values()), "Need >= 2 participants per group."

    report = df[EXPECTED_COLUMNS].isna().sum()
    print("\nMissing values per column:")
    print(report.to_string())
    if report.sum() > 0:
        print("[WARN] Missing values detected - downstream scripts drop them pairwise.")

    print("\n[OK] Environment and data validated successfully.")


if __name__ == "__main__":
    main()

