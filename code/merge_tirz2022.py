import pandas as pd
from calib import calib
from style import NAME, DOM
ref = pd.read_csv('sema_vs_sglt2_t2d.csv')[['code', 'outcome', 'role']]
B = pd.concat([pd.read_csv(f'tirz2022_batch{i}.csv') for i in (1, 2, 3)]).drop(columns=['outcome', 'role']).merge(ref, on='code', how='left')
cols = ['outcome', 'code', 'role', 'n_c1', 'events_c1', 'n_c2', 'events_c2', 'HR', 'lo', 'hi', 'logrank_p', 'prop_p', 'batch']
B = B[cols]; B.to_csv('tirz2022_vs_sglt2.csv', index=False)
d, m, t = calib('tirz2022_vs_sglt2.csv'); o, _, _ = calib('tirz_vs_sglt2_t2d.csv')
print('null HR %.3f tau %.3f' % (m, t))
x = d[d.role != 'negative-control'].set_index('code'); y = o[o.role != 'negative-control'].set_index('code')
rows = []
for _, cs in DOM:
    for c in cs:
        if c not in x.index: continue
        a = x.loc[c]; b = y.loc[c] if c in y.index else None
        rows.append([NAME[c], f'{a.cHR:.2f} ({a.clo:.2f}–{a.chi:.2f})', '<0.001' if a.q_cal < 0.001 else f'{a.q_cal:.3f}', f'{b.cHR:.2f} ({b.clo:.2f}–{b.chi:.2f})' if b is not None else '–'])
T = pd.DataFrame(rows, columns=['Outcome', 'Tirzepatide vs SGLT2i, comparator 2022–2025: calibrated HR (95% CI)', 'q', 'Main tirzepatide analysis (comparator 2018–2025): calibrated HR (95% CI)'])
md = '| ' + ' | '.join(T.columns) + ' |\n|' + '---|' * len(T.columns) + '\n' + '\n'.join('| ' + ' | '.join(r) + ' |' for r in T.values)
open('ms/supp_table_s9.md', 'w').write(md + '\n'); print(md)
print('n pairs range', B.n_c1.min(), B.n_c1.max())
