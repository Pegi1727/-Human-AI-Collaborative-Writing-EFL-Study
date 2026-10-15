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
Script 10 - Graphical abstract (300 DPI).

A single three-panel summary figure showing pre->post mean trajectories
(+/- SE) for Experimental vs Control on Writing, SRL, and AI-literacy.

Run:  python 10_generate_graphical_abstract.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")
PALETTE = {"Experimental": "#1f77b4", "Control": "#d62728"}
CONSTRUCTS = [("Writing", "Writing_Pre", "Writing_Post", "Score (0-100)"),
              ("SRL", "SRL_Pre", "SRL_Post", "Score (1-5)"),
              ("AI literacy", "AI_Pre", "AI_Post", "Score (1-5)")]


def main():
    df = ensure_writing_100(load_data())
    out_dir = make_output_dir("outputs")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (name, pre, post, ylab) in zip(axes, CONSTRUCTS):
        for g in ["Experimental", "Control"]:
            d = df[df["Group"] == g]
            pre_m, post_m = d[pre].mean(), d[post].mean()
            pre_se, post_se = d[pre].sem(), d[post].sem()
            ax.errorbar([0, 1], [pre_m, post_m], yerr=[pre_se, post_se],
                        marker="o", ms=9, capsize=5, lw=2.5,
                        color=PALETTE[g], label=g)
            ax.annotate("", xy=(1, post_m), xytext=(0, pre_m),
                        arrowprops=dict(arrowstyle="->", color=PALETTE[g],
                                        alpha=.35, lw=2))
        ax.set_xticks([0, 1]); ax.set_xticklabels(["Pre", "Post"])
        ax.set_title(name); ax.set_ylabel(ylab)
        ax.legend(frameon=False, fontsize=11)
    fig.suptitle("Effects of AI-assisted instruction on EFL writing, SRL, and AI literacy\n(NCAL-2026-1259)",
                 fontsize=16, y=1.04)
    fig.tight_layout()
    path = os.path.join(out_dir, "graphical_abstract.png")
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("[OK] Graphical abstract saved:", path)


if __name__ == "__main__":
    main()

