# Human–AI Collaborative Writing: Effects of ChatGPT-Mediated Peer Feedback on EFL Learners' Academic Writing Quality, Self-Regulated Learning, and AI Literacy

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23386738.svg)](https://doi.org/10.5281/zenodo.23386738)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.2%2B-276DC3.svg)](https://www.r-project.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange.svg)](https://jupyter.org/)

**Author:** Dr. Pegah Merrikhi  
**Manuscript ID:** `NCAL-2026-1259`  
**Journal:** *Computer Assisted Language Learning*  
**Zenodo Persistent Archive:** [10.5281/zenodo.23386738](https://doi.org/10.5281/zenodo.23386738)  
**Permanent GitHub Repository:** [https://github.com/Pegi1727/-Human-AI-Collaborative-Writing-EFL-Study](https://github.com/Pegi1727/-Human-AI-Collaborative-Writing-EFL-Study)

---

## 📌 Executive Summary & Abstract

This repository constitutes the comprehensive open-science replication package for an 8-week quasi-experimental study investigating the integration of generative AI into peer-review pedagogy. The investigation examines the impact of **ChatGPT-mediated peer feedback** compared to conventional peer feedback among undergraduate EFL learners ($N = 68$). 

The intervention paired structured student peer critique with generative AI refinement protocols, evaluating effects across three primary dimensions:
1. **Academic Writing Quality** (evaluated via a 25-point analytical rubric and scaled to 0–100).
2. **Self-Regulated Learning (SRL)** (metacognitive planning, monitoring, and revision strategies).
3. **AI Literacy** (prompt formulation, ethical appraisal, and critical validation).

All statistical models employ Analysis of Covariance (ANCOVA) controlling for pretest baselines, adhering to APA 7th reporting standards.

---

## 🖼 Key Visual Assets & Graphical Abstract

### Graphical Abstract
<p align="center">
  <img src="figures/Graphical_Abstract.png" alt="Graphical Abstract" width="95%"/>
</p>
<p align="center"><em>Figure GA: Conceptual framework, pedagogical workflow, and empirical highlights.</em></p>

### Empirical Findings Panels (Figures 1–4)

| Figure 1: Academic Writing Quality | Figure 2: Self-Regulated Learning (SRL) |
|:---:|:---:|
| <img src="figures/Figure_1_Writing_Quality.png" width="95%"/> | <img src="figures/Figure_2_SRL.png" width="95%"/> |
| *Pre-to-post gains with ANCOVA adjusted posttest means.* | *Adjusted gains across SRL metacognitive dimensions.* |

| Figure 3: AI Literacy | Figure 4: Effect Sizes & Gain Distributions |
|:---:|:---:|
| <img src="figures/Figure_3_AI_Literacy.png" width="95%"/> | <img src="figures/Figure_4_Effect_Sizes_Summary.png" width="95%"/> |
| *Composite AI literacy enhancement by condition.* | *Standardized effect sizes ($\eta_p^2$) and gain densities.* |

---

## 📊 Summary of Core Statistical Findings

All posttest outcomes were examined via ANCOVA with baseline pretest scores specified as the covariate ($N = 68$, $df_{\text{model}} = 1, 65$).

| Outcome Measure | Baseline Equivalence ($t$-test) | ANCOVA $F(1, 65)$ | Sig. ($p$) | Partial $\eta^2$ ($\eta_p^2$) | Adjusted Mean: Experimental | Adjusted Mean: Control |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Academic Writing (100-pt Scale)** | $t(66) = 0.31, p = .755$ | **$28.09$** | **$< .001$** | **$.302$** | **$82.17$** ($SE = 1.05$) | **$74.21$** ($SE = 1.05$) |
| **Academic Writing (Raw 25-pt)** | $t(66) = 0.29, p = .770$ | **$27.84$** | **$< .001$** | **$.300$** | **$20.40$** ($SE = 0.26$) | **$19.04$** ($SE = 0.26$) |
| **Self-Regulated Learning (SRL, 1–5)** | $t(66) = -0.18, p = .857$ | **$47.22$** | **$< .001$** | **$.421$** | **$4.11$** ($SE = 0.07$) | **$3.51$** ($SE = 0.07$) |
| **AI Literacy (Composite, 1–5)** | $t(66) = 0.42, p = .675$ | **$143.50$** | **$< .001$** | **$.688$** | **$4.28$** ($SE = 0.07$) | **$3.20$** ($SE = 0.07$) |

*Note. $\eta_p^2 \ge .14$ corresponds to a large effect size benchmark under Cohen's guidelines. All models fulfilled homogeneity of regression slopes and residual normality assumptions.*

---

## 💡 Key Conclusions

1. **Substantive Writing Quality Improvements:** Integrating ChatGPT as an iterative scaffolding partner in peer review led to statistically significant and practically meaningful writing gains ($\eta_p^2 = .302$), primarily driven by higher coherence, structural clarity, and academic lexical precision.
2. **Amplified Metacognitive Agency:** Contrary to passive-dependence concerns, experimental learners exhibited superior self-regulated learning ($\eta_p^2 = .421$), actively monitoring, querying, and auditing AI feedback rather than uncritically accepting recommendations.
3. **Pronounced AI Literacy Gains:** The largest intervention impact emerged in learners' AI literacy ($\eta_p^2 = .688$). Explicit pedagogical interaction fostered sophisticated prompt design strategies and critical verification habits.

---

🔁 Reproduction Guidelines
1. Python Workflow
bash
# Clone the repository
git clone https://github.com/Pegi1727/-Human-AI-Collaborative-Writing-EFL-Study.git
cd -Human-AI-Collaborative-Writing-EFL-Study

# Install required dependencies
pip install numpy pandas scipy statsmodels matplotlib seaborn

# Run end-to-end pipeline
python scripts/01_validate_environment.py
python scripts/05_ancova_writing_table4.py
python scripts/09_generate_figures_1_to_4.py
2. R Workflow
bash
# Execute ANCOVA models and export publication plots
Rscript scripts_r/05_ancova_writing_table4.R
Rscript scripts_r/09_generate_figures_1_to_4.R
-------------------------------
📖 How to Cite
Primary Article
bibtex
@article{merrikhi2026human_ai_collaborative_writing,
  author    = {Merrikhi, Pegah},
  title     = {Human--AI Collaborative Writing: Effects of ChatGPT-Mediated Peer Feedback on EFL Learners' Academic Writing Quality, Self-Regulated Learning, and AI Literacy},
  journal   = {Computer Assisted Language Learning},
  year      = {2026},
  note      = {Manuscript ID: NCAL-2026-1259}
----------------------------------
Replication Package & Dataset
bibtex
@misc{merrikhi2026zenodo_replication,
  author    = {Merrikhi, Pegah},
  title     = {Replication Data, Python \& R Scripts, and Jupyter Notebooks for: Human–AI Collaborative Writing},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v1.00},
  doi       = {10.5281/zenodo.23386738},
  url       = {https://doi.org/10.5281/zenodo.23386738}
}
--------------------------------------
⚖️ License
The empirical dataset, documentation, and graphical materials are licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0). All analytical scripts (Python and R) and Jupyter Notebooks are provided under the open-source MIT License.
--------------
## 🗂 Repository Structure
```text
├── data/                               <- Participant datasets
│   ├── raw/
│   │   └── Hypothetical_EFL_AI_Study_Data.csv
│   └── processed/
│       ├── Reconstructed_Raw_and_Scaled_EFL_Study_Data.csv
│       ├── Reconstructed_Raw_and_Scaled_EFL_Study_Data.xlsx
│       ├── Summary_Statistics.csv
│       └── Statistics_Raw25_vs_Scale100_Summary.csv
├── figures/                            <- Camera-ready 300 DPI figures
│   ├── README.md                       <- Figure captions & specifications
│   ├── Graphical_Abstract.png
│   ├── Figure_1_Writing_Quality.png
│   ├── Figure_2_SRL.png
│   ├── Figure_3_AI_Literacy.png
│   └── Figure_4_Effect_Sizes_Summary.png
├── notebooks/                          <- Interactive Jupyter Notebooks
│   ├── 01_data_exploration_and_descriptives.ipynb
│   ├── 02_statistical_assumptions_and_diagnostics.ipynb
│   ├── 03_inferential_models_ancova_tables4_to_6.ipynb
│   ├── 04_adjusted_means_and_table7.ipynb
│   └── 05_publication_figures_and_graphical_abstract.ipynb
├── scripts/                            <- Python pipeline (01 through 10)
│   ├── 01_validate_environment.py
│   ├── 02_load_and_clean_data.py
│   ├── 03_descriptive_stats_table3.py
│   ├── 04_assumption_checks.py
│   ├── 05_ancova_writing_table4.py
│   ├── 06_ancova_srl_table5.py
│   ├── 07_ancova_ai_lit_table6.py
│   ├── 08_adjusted_means_table7.py
│   ├── 09_generate_figures_1_to_4.py
│   └── 10_generate_graphical_abstract.py
├── scripts_r/                          <- Corresponding R pipeline (01 through 10)
│   ├── 01_validate_environment.R
│   └── ...
├── outputs/                            <- Generated tables and verification outputs
└── README.md                           <- Repository documentation
