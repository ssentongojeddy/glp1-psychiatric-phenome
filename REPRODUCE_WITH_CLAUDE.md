# Reproducing the analysis with Claude

This folder lets you reproduce every number, table and figure in
*Semaglutide, tirzepatide and the psychiatric phenome: a target trial emulation*
from the aggregate results that TriNetX returned. No patient-level data are included or needed.

There are two levels of reproduction.

| Level | What it checks | What you need | Time |
|---|---|---|---|
| **A. Re-run the analysis** (recommended) | Calibration, FDR, E-values, absolute risks, sensitivity analyses, every table and figure | This zip and Claude | 5 minutes |
| **B. Re-query TriNetX** | That the cohorts and hazard ratios themselves come out the same | TriNetX access to study 410410 plus Claude with a browser | Several hours |

---

## Level A: re-run everything from the TriNetX outputs

1. Open Claude (claude.ai or the desktop app) and start a new chat.
2. Attach this zip file (`glp1-psychiatric-phenome_reproduce.zip`).
3. Paste this prompt:

> I've attached the analysis package for our Nature Medicine manuscript on semaglutide, tirzepatide and psychiatric outcomes. Please unzip it (or clone it from https://github.com/ssentongojeddy/glp1-psychiatric-phenome), read `README.md` and `REPRODUCE_WITH_CLAUDE.md`, install the packages in `requirements.txt`, and run `bash run_all.sh`. Then:
> 1. Report the output of `code/verify.py` (it should say 17/17 checks passed).
> 2. Show me the calibrated hazard ratios (95% CI) and FDR q for all 19 outcomes in the primary analysis (semaglutide or tirzepatide vs SGLT2 inhibitors), from `data/derived/all_calibrated.csv`.
> 3. Compare them with Extended Data Table 2 in the manuscript PDF, if attached, and list any number that differs.
> 4. Show me the regenerated Figure 2 and Figure 3 from `figures/main/`.
> 5. Explain in plain language what `code/calib.py` does to each hazard ratio.

4. Optionally, attach the manuscript PDF so Claude can compare numbers directly.

**What success looks like:**

- `17/17 checks passed`.
- Primary analysis: 11 of 19 outcomes with FDR q < 0.05, and negative-control bias HR 1.17.
- Examples: cocaine use disorder 0.41 (0.32–0.53); schizophrenia 0.53 (0.41–0.69); suicide attempt 0.39 (0.28–0.55).
- Figures in `figures/main/` match the manuscript.

### What `run_all.sh` does

| Step | Script | Output |
|---|---|---|
| 1 | `combine.py` → `calib.py` | Empirical calibration to six negative controls (random-effects null), Benjamini–Hochberg FDR and E-values for the primary analysis and all eight secondary comparisons → `data/derived/all_calibrated.csv` |
| 2 | `table1.py` | Standardized mean differences before and after matching → `baseline_all.csv` |
| 3 | `sens.py` | Model-based absolute risk differences per 1,000; leave-one-out and fixed-effect calibration |
| 4 | `merge_tirz2022.py` | Tirzepatide vs SGLT2 inhibitors with the comparator restricted to 2022–2025 (Supplementary Table S9) |
| 5 | `merge_ext.py` | Primary analysis with extended matching on BMI and HbA1c bands and prior healthcare use (Supplementary Table S10) |
| 6 | `fig1.py`, `mainfigs.py`, `kmfig.py`, `ga.py`, `supp_figs.py` | Figures 1–6, the graphical abstract and Supplementary Figures S1–S22 |
| 7 | `verify.py` | Compares key results with the manuscript |

---

## Level B: re-query TriNetX (optional, for full independent verification)

TriNetX returns only aggregate results and re-runs propensity matching each time, so a re-run gives very similar but not identical counts. Healthcare organizations also go online and offline, and new data arrive.

1. **Access.** Paddy shares TriNetX study 410410 ("GLP-1 and GIP/GLP-1 receptor agonists and the psychiatric phenome: discovery study (Nature Medicine)") with your account.
2. **Definitions.** All cohort queries, outcome codes, the 43 matching covariates and the extended-adjustment covariates are in `docs/cohort_definitions.md`. Primary-analysis cohort queries: 15334422 (semaglutide or tirzepatide, 13 May 2022 – 28 Oct 2025) and 15334477 (SGLT2 inhibitors, same period).
3. **Analysis settings.** In TriNetX Advanced Analytics → Compare Outcomes:
   - index event = first qualifying prescription
   - 1:1 propensity matching, calliper 0.1 SD
   - outcome window day 1 to day 1,095
   - "exclude patients with outcomes prior to the window" ticked
   - Kaplan–Meier with log-rank and hazard ratio
   - outcomes run in batches of up to 10
4. **Using Claude.** Claude can drive TriNetX through its browser if your Claude desktop app has the built-in browser and you are signed in to TriNetX. You enter your own password; Claude should not handle it.
5. **Compare.** Put your exported hazard ratios in the same CSV format as `data/trinetx_results/*.csv`, re-run `run_all.sh`, and compare.

A suggested prompt for Level B:

> Using the definitions in `docs/cohort_definitions.md`, open TriNetX study 410410 in the browser (I am signed in), open the analysis "PRIMARY T2D: semaglutide or tirzepatide vs SGLT2i (2022-2025)", re-run the outcome batches, and record each outcome's patients, events, hazard ratio and 95% CI in the format of `data/trinetx_results/primary_glp1class_vs_sglt2.csv`. Then re-run the calibration and compare with the original results.

---

## Contents of this package

```
glp1-psychiatric-phenome/
├── REPRODUCE_WITH_CLAUDE.md    ← this guide
├── README.md                   ← full description of code and data
├── run_all.sh                  ← one command reproduces everything
├── requirements.txt
├── code/                       ← analysis and figure scripts, plus verify.py
├── data/trinetx_results/       ← aggregate TriNetX outputs (one CSV per comparison or batch)
├── data/baseline/              ← baseline characteristics before and after matching
├── data/km/                    ← Kaplan–Meier curve coordinates
├── data/derived/               ← outputs (regenerated by run_all.sh)
├── docs/cohort_definitions.md  ← cohorts, codes, covariates, TriNetX query IDs
├── figures/                    ← main and supplementary figures
```

Questions: Paddy Ssentongo, pssentongo@pennstatehealth.psu.edu
