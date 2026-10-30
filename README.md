# GLP-1 and GIP/GLP-1 receptor agonists and the psychiatric phenome

Code and aggregate data for:

> Ssentongo P, Ssentongo AE. **Semaglutide, tirzepatide and the psychiatric phenome: a target trial emulation.** Manuscript submitted to *Nature Medicine* (2026).

This repository reproduces every derived statistic, table and figure in the manuscript from the aggregate results returned by the TriNetX platform. It contains no patient-level data.

> **Disclaimer.** This software is provided for research purposes only. It is not a medical device and must not be used to guide individual patient care.

## Overview

We emulated target trials of new users of semaglutide or tirzepatide in the TriNetX Global Collaborative Network (study 410410), using de-identified electronic health records from up to 159 healthcare organizations.

**Primary analysis.** Semaglutide or tirzepatide versus SGLT2 inhibitors in adults with type 2 diabetes, both groups new users from 13 May 2022 to 28 October 2025 (255,685–275,248 matched pairs).

**Secondary comparisons.**

| # | Comparison | Population | Matched pairs |
|---|---|---|---|
| 1 | Semaglutide vs SGLT2 inhibitors (from 2018) | Type 2 diabetes | 374,496 |
| 2 | Tirzepatide vs SGLT2 inhibitors | Type 2 diabetes | 137,440 |
| 3 | Semaglutide vs DPP-4 inhibitors | Type 2 diabetes | 275,553 |
| 4 | Tirzepatide vs semaglutide (from 13 May 2022) | Type 2 diabetes | 142,681 |
| 5 | Semaglutide vs no GLP-1 drug | Type 2 diabetes, obesity, metformin | 295,147 |
| 6 | Tirzepatide vs no GLP-1 drug | Type 2 diabetes, obesity, metformin | 120,137–126,768 |
| 7 | Semaglutide vs no anti-obesity drug | Obesity with obstructive sleep apnoea, no diabetes | 185,404 |
| 8 | Tirzepatide vs no anti-obesity drug | Obesity with obstructive sleep apnoea, no diabetes | 135,067–135,389 |

**Sensitivity analyses.** Leave-one-out and fixed-effect calibration; model-based absolute risk differences; tirzepatide versus SGLT2 inhibitors with the comparator restricted to 2022–2025 (Supplementary Table S9); and the primary analysis with extended matching on nine BMI bands, seven HbA1c bands and prior emergency, outpatient, inpatient and psychiatric care (277,115 pairs; Supplementary Table S10).

For each comparison, cohorts were 1:1 propensity-score matched on 43 baseline terms. There were 19 psychiatric outcomes and 6 negative-control outcomes, with follow-up on days 1–1,095. Hazard ratios came from Cox models in TriNetX.

The code in this repository then does the following:

1. **Empirical calibration.** Estimates systematic bias from the six negative-control outcomes (random-effects empirical null; method of moments) and calibrates every psychiatric hazard ratio, its 95% CI and its *P* value.
2. **Multiple testing.** Controls the false discovery rate across psychiatric outcomes within each comparison (Benjamini–Hochberg).
3. **E-values.** Computes them for every significant association.
4. **Covariate balance.** Computes standardized mean differences before and after matching.
5. **Cumulative incidence.** Converts Kaplan–Meier curves read from the TriNetX plots into cumulative incidence and computes interval-specific incidence ratios.
6. **Figures.** Produces all main and supplementary figures in a colour-blind-safe palette (Okabe–Ito).

```
TriNetX (cohorts, PSM, Cox)  →  data/trinetx_results/*.csv ─┐
                                 data/baseline/*.txt         ├─►  code/  ─►  data/derived/  +  figures/
                                 data/km/*.txt              ─┘
```

See **REPRODUCE_WITH_CLAUDE.md** for a step-by-step guide to reproducing the analysis, including with Claude.

## Repository structure

```
glp1-psychiatric-phenome/
├── README.md
├── LICENSE
├── requirements.txt
├── run_all.sh                     # one command to reproduce everything
├── code/
│   ├── calib.py                   # empirical calibration + BH FDR
│   ├── sens.py                    # absolute risk differences; leave-one-out and fixed-effect calibration
│   ├── merge_primary.py           # assembles the primary-analysis outcome batches
│   ├── merge_tirz2022.py          # tirzepatide sensitivity analysis (Supp Table S9)
│   ├── merge_ext.py               # extended-adjustment sensitivity analysis (Supp Table S10)
│   ├── combine.py                 # runs calibration for all comparisons, adds E-values
│   ├── table1.py                  # standardized mean differences
│   ├── km_load.py                 # Kaplan–Meier curve loader + interval incidence ratios
│   ├── style.py                   # shared figure style, palette and labels
│   ├── fig1.py                    # Fig. 1 (study design)
│   ├── mainfigs.py                # Figs 2, 3, 5 and 6
│   ├── kmfig.py                   # Fig. 4 (cumulative incidence) and Supplementary Fig. S22
│   ├── ga.py                      # graphical abstract
│   ├── ga_mech.py                 # illustrated mechanism panel
│   └── supp_figs.py               # Supplementary Figs S1–S21
├── data/
│   ├── trinetx_results/           # one CSV per comparison (Cox HRs, events, n)
│   ├── baseline/                  # baseline characteristics before/after matching
│   ├── km/                        # Kaplan–Meier curve coordinates and 3-year survival
│   └── derived/                   # outputs: all_calibrated.csv, baseline_all.csv
├── docs/
│   └── cohort_definitions.md      # cohort, outcome and covariate definitions
└── figures/
    ├── main/                      # Figs 1–6 (PNG and PDF)
    └── supplementary/             # Supplementary Figs S1–S22
```

## Data

| File | Contents |
|---|---|
| `data/trinetx_results/*.csv` | One row per outcome. Columns: `outcome, code, role, n_c1, events_c1, n_c2, events_c2, HR, lo, hi, logrank_p, prop_p, batch`. `role` is `psych`, `psych-reward` or `negative-control`; `prop_p` is the TriNetX proportionality test. |
| `data/baseline/*.txt` | Percentages or mean ± SD before and after matching, in the order drug 1 before, comparator before, drug 1 after, comparator after. |
| `data/km/*.txt` | Kaplan–Meier curve coordinates read from the TriNetX survival plots (`c1` drug, `c2` comparator). One pixel on the x axis is 1,095/389 days, and 125.5 pixels on the y axis are 100% cumulative incidence. `sends.txt` gives TriNetX-reported survival at day 1,095, which was used to check the curves. |
| `data/trinetx_results/primary_batch*.csv`, `tirz2022_batch*.csv`, `ext_batch*.csv` | Raw outcome batches for the primary analysis and the two TriNetX-based sensitivity analyses (`outcome` and `role` are filled from the reference file during merging). |
| `data/derived/sens_*.csv`, `tirz2022_vs_sglt2.csv`, `ext_primary_vs_sglt2.csv`, `supp_table_s9.md`, `supp_table_s10.md` | Absolute risk differences, calibration sensitivity and the two sensitivity analyses. |
| `data/derived/all_calibrated.csv` | All estimates with calibrated HR (`cHR, clo, chi`), FDR `q_cal`, E-values (`E, E_ci`), and the empirical null (`null_HR`, `tau`) for each comparison. |

Counts of 10 or fewer are suppressed by TriNetX and do not appear.

**Patient-level data.** These cannot be shared under TriNetX data-use agreements. Researchers at TriNetX member institutions can rebuild the cohorts from `docs/cohort_definitions.md`.

## Requirements

- Python ≥ 3.10
- `pip install -r requirements.txt` (numpy, pandas, scipy, matplotlib, openpyxl)
- Figures use the Inter font if it is installed and otherwise fall back to the Matplotlib default.

## To run

```bash
git clone https://github.com/ssentongojeddy/glp1-psychiatric-phenome.git
cd glp1-psychiatric-phenome
pip install -r requirements.txt
bash run_all.sh
```

The scripts run in a temporary `build/` folder. They write results to `data/derived/` and figures to `figures/`. A full run takes under a minute on a laptop.

## Key methods

For negative control *j* with log hazard ratio $\hat\beta_j$ and standard error $s_j$, we assume $\hat\beta_j \sim N(\mu, s_j^2+\tau^2)$. We estimate $\mu$ by the inverse-variance-weighted mean and $\tau^2$ by the method of moments. Each psychiatric estimate is then calibrated as

$$\tilde\beta=\hat\beta-\hat\mu,\qquad \tilde s=\sqrt{s^2+\hat\tau^2},\qquad p=2\{1-\Phi(|\tilde\beta|/\tilde s)\}.$$

E-values use $E=\mathrm{RR}+\sqrt{\mathrm{RR}(\mathrm{RR}-1)}$, with $\mathrm{RR}=1/\widetilde{\mathrm{HR}}$ for protective estimates. The manuscript's Methods and Supplementary Methods give full details.

## Citation

```bibtex
@article{ssentongo2026glp1psych,
  title   = {Semaglutide, tirzepatide and the psychiatric phenome: a target trial emulation},
  author  = {Ssentongo, Paddy and Ssentongo, Anna E.},
  journal = {Nature Medicine (submitted)},
  year    = {2026}
}
```

## Funding

National Institute of Mental Health (grant 11456721 to A.E.S.; MIND Study).

## License

The code is released under the MIT License (see `LICENSE`), and the aggregate data under CC BY 4.0.

## Contact

Paddy Ssentongo, MD, PhD, MPH — Penn State Health Milton S. Hershey Medical Center — pssentongo@pennstatehealth.psu.edu
