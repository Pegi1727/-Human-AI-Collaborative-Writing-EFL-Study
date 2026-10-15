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
Script 06 - One-way ANCOVA for Self-regulated learning (SRL) (table5).

Model: SRL_Post ~ Group + SRL_Pre  (covariate = pre-test).
Reports F test, partial eta-squared, adjusted means, and the group contrast.
Run:  python 06_ancova_srl_table5.py
"""
from scipy import stats


def ancova(df, post, pre, group_col="Group"):
    """Classic ANCOVA via OLS with treatment-coded Group; returns key stats."""
    d = df[[post, pre, group_col]].dropna().copy()
    d["Trt"] = (d[group_col] == "Experimental").astype(float)
    y = d[post].values
    n = len(d)

    X = np.column_stack([np.ones(n), d["Trt"].values, d[pre].values])
    beta, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    df_res = n - rank
    mse = (resid ** 2).sum() / df_res
    cov = mse * np.linalg.inv(X.T @ X)

    # Reduced model (covariate only) for the F test of Group
    X0 = np.column_stack([np.ones(n), d[pre].values])
    b0, _, _, _ = np.linalg.lstsq(X0, y, rcond=None)
    sse_full = (resid ** 2).sum()
    sse_red = ((y - X0 @ b0) ** 2).sum()
    F = (sse_red - sse_full) / mse
    p_F = 1 - stats.f.cdf(F, 1, df_res)

    se_trt = np.sqrt(cov[1, 1])
    t_trt = beta[1] / se_trt
    p_trt = 2 * (1 - stats.t.cdf(abs(t_trt), df_res))

    ss_group = sse_red - sse_full
    eta_sq = ss_group / (ss_group + sse_full)   # partial eta-squared

    gm = d[pre].mean()
    adj = {g: beta[0] + beta[1] * (1.0 if g == "Experimental" else 0.0) + beta[2] * gm
           for g in ["Experimental", "Control"]}
    return dict(F=F, df_res=df_res, p=p_F, t=t_trt, p_t=p_trt,
                beta_trt=beta[1], se_trt=se_trt, eta_sq=eta_sq,
                adj_means=adj, grand_mean_cov=gm, n=n)


def main():
    df = ensure_writing_100(load_data())
    res = ancova(df, "SRL_Post", "SRL_Pre")
    out_df = pd.DataFrame([{
        "Comparison": "Self-regulated learning (SRL)",
        "F(1, %d)" % res["df_res"]: round(res["F"], 2),
        "p": round(res["p"], 4),
        "partial_eta_sq": round(res["eta_sq"], 3),
        "Mean_Diff_Exp_Ctrl": round(res["beta_trt"], 2),
        "SE_Diff": round(res["se_trt"], 2),
        "AdjMean_Exp": round(res["adj_means"]["Experimental"], 2),
        "AdjMean_Ctrl": round(res["adj_means"]["Control"], 2),
    }])
    out_dir = make_output_dir()
    out = os.path.join(out_dir, "table5_ancova.csv")
    out_df.to_csv(out, index=False)
    print("[OK] Saved:", out)
    print(out_df.to_string(index=False))
    size = "large" if res["eta_sq"] >= .14 else "medium" if res["eta_sq"] >= .06 else "small"
    print(f"\nInterpretation: Group effect p = {res['p']:.4f}; "
          f"partial eta-squared = {res['eta_sq']:.3f} ({size} effect).")


if __name__ == "__main__":
    main()

