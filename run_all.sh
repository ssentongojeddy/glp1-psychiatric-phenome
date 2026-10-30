#!/usr/bin/env bash
# Reproduce all derived statistics and figures from the aggregate TriNetX outputs.
# Usage: bash run_all.sh   (requires Python >= 3.10 and the packages in requirements.txt)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
B="$ROOT/build"; mkdir -p "$B/figs" "$B/sfigs5" "$B/ms"
cp "$ROOT"/code/*.py "$B/"
cp "$ROOT"/data/trinetx_results/*.csv "$B/"
rm -rf "$B/baseline" "$B/km"; cp -r "$ROOT/data/baseline" "$B/baseline"; cp -r "$ROOT/data/km" "$B/km"
cd "$B"
python3 combine.py          # empirical calibration, FDR and E-values -> all6_calibrated.csv
python3 table1.py           # standardized mean differences -> baseline_all.csv
python3 sens.py             # absolute risk differences and calibration sensitivity
python3 merge_tirz2022.py   # tirzepatide vs SGLT2i, comparator restricted to 2022-2025 (Supp Table S9)
python3 merge_ext.py        # primary analysis with extended adjustment (Supp Table S10)
python3 fig1.py             # Fig. 1 study design
python3 mainfigs.py         # Figs 2, 3, 5 and 6
python3 kmfig.py            # Fig. 4 cumulative incidence and Supplementary Fig. S22
python3 ga.py               # graphical abstract
python3 supp_figs.py        # Supplementary Figs S1-S21
cp all6_calibrated.csv "$ROOT/data/derived/all_calibrated.csv"; cp ms/supp_table_s7.md "$ROOT/data/derived/interval_ratios_table.md"; cp baseline_all.csv "$ROOT/data/derived/baseline_all.csv"; cp sens_absolute_risk.csv sens_calibration.csv tirz2022_vs_sglt2.csv ext_primary_vs_sglt2.csv "$ROOT/data/derived/"; cp ms/supp_table_s9.md ms/supp_table_s10.md "$ROOT/data/derived/"
cp figs/* "$ROOT/figures/main/"; cp sfigs5/* "$ROOT/figures/supplementary/"
echo "Done. Outputs in data/derived and figures/."
python3 "$ROOT/code/verify.py"
