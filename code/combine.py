import pandas as pd, numpy as np
from calib import calib
F=[('primary_glp1class_vs_sglt2.csv','Semaglutide or tirzepatide vs SGLT2i (primary)'),('sema_vs_sglt2_t2d.csv','Semaglutide vs SGLT2i'),('tirz_vs_sglt2_t2d.csv','Tirzepatide vs SGLT2i'),('sema_vs_dpp4_t2d.csv','Semaglutide vs DPP-4i'),('tirz_vs_sema_t2d.csv','Tirzepatide vs semaglutide'),('sema_vs_nodrug_t2d.csv','Semaglutide vs no drug (T2D)'),('tirz_vs_nodrug_t2d.csv','Tirzepatide vs no drug (T2D)'),('obes_sema_vs_nodrug.csv','Semaglutide vs no drug (obesity+OSA)'),('obes_tirz_vs_nodrug.csv','Tirzepatide vs no drug (obesity+OSA)')]
def ev(hr,lo,hi):
    # E-value for HR (rare outcome approx -> treat as RR)
    if hr<1: hr,ci=1/hr,(1/hi if hi<1 else 1)
    else: ci=lo if lo>1 else 1
    e=lambda r: r+np.sqrt(r*(r-1)) if r>1 else 1
    return e(hr),e(ci)
rows=[]
for f,lab in F:
    d,mu,tau=calib(f); d['comparison']=lab; d['null_HR']=mu; d['tau']=tau
    e=[ev(r.cHR,r.clo,r.chi) for r in d.itertuples()]; d['E']=[x[0] for x in e]; d['E_ci']=[x[1] for x in e]
    rows.append(d)
A=pd.concat(rows); A.to_csv('all6_calibrated.csv',index=False)
print(A.groupby('comparison')[['null_HR','tau']].first())
