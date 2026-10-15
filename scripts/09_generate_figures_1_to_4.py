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
Script 09 - Figures 1-4 (300 DPI).

  Figure 1: Pre/Post group means for Writing (bars + SE error bars).
  Figure 2: Pre/Post group means for SRL and AI-literacy.
  Figure 3: Gain-score distributions by construct and group (boxplots).
  Figure 4: Writing Pre vs Post scatter with per-group regression lines.

Run:  python 09_generate_figures_1_to_4.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="paper")
PALETTE = {"Experimental": "#1f77b4", "Control": "#d62728"}


def save(fig, path):
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("[OK] Figure saved:", path)


def main():
    df = ensure_writing_100(load_data())
    out_dir = make_output_dir(os.path.join("outputs", "figures"))
    long = df.melt(id_vars=["ID", "Group"],
                   value_vars=["Writing_Pre", "Writing_Post", "SRL_Pre", "SRL_Post",
                               "AI_Pre", "AI_Post"],
                   var_name="Measure", value_name="Score")
    long["Time"] = long["Measure"].str.split("_").str[1]
    long["Construct"] = long["Measure"].str.split("_").str[0]

    # ---- Figure 1: Writing ------------------------------------------------
    fig, ax = plt.subplots(figsize=(6, 4))
    sub = long[long["Construct"] == "Writing"]
    m = sub.groupby(["Group", "Time"])["Score"].agg(["mean", "sem"]).reset_index()
    w = 0.35
    for i, g in enumerate(["Experimental", "Control"]):
        d = m[m["Group"] == g].set_index("Time").loc[["Pre", "Post"]]
        ax.bar(np.arange(2) + (i - .5) * w, d["mean"], width=w, yerr=d["sem"],
               capsize=4, color=PALETTE[g], alpha=.85, label=g)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Pre", "Post"])
    ax.set_ylabel("Writing score (0-100)")
    ax.set_title("Figure 1. Writing achievement by group and time")
    ax.legend(frameon=False)
    save(fig, os.path.join(out_dir, "figure1_writing_means.png"))

    # ---- Figure 2: SRL & AI literacy -------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, constr in zip(axes, ["SRL", "AI"]):
        sub = long[long["Construct"] == constr]
        m = sub.groupby(["Group", "Time"])["Score"].agg(["mean", "sem"]).reset_index()
        for i, g in enumerate(["Experimental", "Control"]):
            d = m[m["Group"] == g].set_index("Time").loc[["Pre", "Post"]]
            ax.bar(np.arange(2) + (i - .5) * w, d["mean"], width=w, yerr=d["sem"],
                   capsize=4, color=PALETTE[g], alpha=.85, label=g)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["Pre", "Post"])
        ax.set_title(constr); ax.legend(frameon=False)
    fig.suptitle("Figure 2. SRL and AI-literacy by group and time")
    save(fig, os.path.join(out_dir, "figure2_srl_ai_means.png"))

    # ---- Figure 3: Gain scores --------------------------------------------
    gains = pd.DataFrame({
        "Group": np.tile(df["Group"], 3),
        "Construct": (["Writing"] * len(df)) + (["SRL"] * len(df)) + (["AI"] * len(df)),
        "Gain": np.concatenate([df["Writing_Post"] - df["Writing_Pre"],
                                df["SRL_Post"] - df["SRL_Pre"],
                                df["AI_Post"] - df["AI_Pre"]]),
    })
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=gains, x="Construct", y="Gain", hue="Group", ax=ax,
                palette=PALETTE)
    ax.axhline(0, ls="--", c="grey", lw=1)
    ax.set_title("Figure 3. Gain scores by construct and group")
    save(fig, os.path.join(out_dir, "figure3_gain_scores.png"))

    # ---- Figure 4: Writing pre/post scatter --------------------------------
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.scatterplot(data=df, x="Writing_Pre", y="Writing_Post", hue="Group",
                    palette=PALETTE, ax=ax, s=45)
    for g in ["Experimental", "Control"]:
        d = df[df["Group"] == g].dropna(subset=["Writing_Pre", "Writing_Post"])
        b, a = np.polyfit(d["Writing_Pre"], d["Writing_Post"], 1)
        xs = np.linspace(d["Writing_Pre"].min(), d["Writing_Pre"].max(), 50)
        ax.plot(xs, a + b * xs, color=PALETTE[g], lw=2)
    ax.set_title("Figure 4. Writing pre- vs post-test with regression lines")
    save(fig, os.path.join(out_dir, "figure4_writing_scatter.png"))


if __name__ == "__main__":
    main()

