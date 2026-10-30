"""Check reproduced results against the numbers reported in the manuscript. Run after run_all.sh."""
import pandas as pd, sys, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'derived')
A = pd.read_csv(os.path.join(D, 'all_calibrated.csv'))

P = 'Semaglutide or tirzepatide vs SGLT2i (primary)'
expected = [  # (comparison, code, calibrated HR, lower, upper) as reported in the manuscript
    (P, 'F14', 0.41, 0.32, 0.53), (P, 'F15', 0.39, 0.31, 0.51), (P, 'T14.91', 0.39, 0.28, 0.55),
    (P, 'R45.851', 0.50, 0.39, 0.63), (P, 'F20', 0.53, 0.41, 0.69), (P, 'F12', 0.59, 0.47, 0.75),
    (P, 'F10', 0.67, 0.54, 0.84), (P, 'F31', 0.69, 0.54, 0.87), (P, 'F11', 0.70, 0.56, 0.89),
    (P, 'F17', 0.73, 0.58, 0.91), (P, 'F42', 0.73, 0.56, 0.95),
    ('Semaglutide vs SGLT2i', 'F14', 0.53, 0.43, 0.63), ('Tirzepatide vs SGLT2i', 'F14', 0.38, 0.28, 0.53),
    ('Semaglutide vs SGLT2i', 'T14.91', 0.58, 0.45, 0.74), ('Tirzepatide vs SGLT2i', 'T14.91', 0.47, 0.31, 0.71),
]
ok = 0
for cp, code, h, l, u in expected:
    r = A[(A.comparison == cp) & (A.code == code)].iloc[0]
    got = tuple(float(f'{x:.2f}') for x in (r.cHR, r.clo, r.chi)); good = got == (h, l, u); ok += good
    print(('PASS' if good else 'FAIL'), cp, code, 'expected', (h, l, u), 'got', got)
n_sig = int(((A.comparison == P) & (A.role != 'negative-control') & (A.q_cal < 0.05)).sum())
good = n_sig == 11; ok += good; print(('PASS' if good else 'FAIL'), 'primary: outcomes with FDR q<0.05 = 11, got', n_sig)
null = round(A[A.comparison == P].null_HR.iloc[0], 2); good = null == 1.17; ok += good
print(('PASS' if good else 'FAIL'), 'primary: negative-control bias HR = 1.17, got', null)
tot = len(expected) + 2
print(f'\n{ok}/{tot} checks passed'); sys.exit(0 if ok == tot else 1)
