import pandas as pd
from calib import calib
ref = pd.read_csv('sema_vs_sglt2_t2d.csv')[['code', 'outcome', 'role']]
B = pd.concat([pd.read_csv(f'primary_batch{i}.csv') for i in (1, 2, 3)])
B = B.drop(columns=['outcome', 'role']).merge(ref, on='code', how='left')
assert len(B) == 25 and B.role.notna().all(), B
cols = ['outcome', 'code', 'role', 'n_c1', 'events_c1', 'n_c2', 'events_c2', 'HR', 'lo', 'hi', 'logrank_p', 'prop_p', 'batch']
B = B.set_index('code').loc[ref.code].reset_index()[cols]
B.to_csv('primary_glp1class_vs_sglt2.csv', index=False)
d, m, t = calib('primary_glp1class_vs_sglt2.csv')
print('null HR %.3f tau %.3f' % (m, t))
print(d[d.role != 'negative-control'].sort_values('cHR')[['outcome', 'events_c1', 'events_c2', 'HR', 'cHR', 'clo', 'chi', 'q_cal']].round(3).to_string(index=False))
