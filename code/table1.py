import numpy as np, pandas as pd, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/baseline')
files=[('primary','Semaglutide or tirzepatide vs SGLT2i (primary)'),('sema_sglt2','Semaglutide vs SGLT2i'),('tirz_sglt2','Tirzepatide vs SGLT2i'),('sema_dpp4','Semaglutide vs DPP-4i'),('tirz_sema','Tirzepatide vs semaglutide'),('sema_nodrug','Semaglutide vs no drug (T2D)'),('tirz_nodrug','Tirzepatide vs no drug (T2D)'),('obes','Semaglutide vs no drug (obesity+OSA)'),('tirz_obes','Tirzepatide vs no drug (obesity+OSA)')]
out=[]
for f,lab in files:
    for line in open(f+'.txt'):
        k,v=line.strip().split('|',1); v=v.strip('|').split(';')
        if k=='N':
            out.append(dict(comp=lab,var='N',b1=v[0],b2=v[1],a1=v[2],a2=v[3],smd_b='',smd_a='')); continue
        if '±' in v[0]:
            m=[tuple(map(float,x.split('±'))) for x in v]
            smd=lambda x,y:(x[0]-y[0])/np.sqrt((x[1]**2+y[1]**2)/2)
            fmt=lambda x:f'{x[0]:.1f} ({x[1]:.1f})'
            out.append(dict(comp=lab,var=k+', mean (SD)',b1=fmt(m[0]),b2=fmt(m[1]),a1=fmt(m[2]),a2=fmt(m[3]),smd_b=f'{abs(smd(m[0],m[1])):.2f}',smd_a=f'{abs(smd(m[2],m[3])):.2f}'))
        else:
            p=[float(x.strip('%'))/100 for x in v]
            smd=lambda x,y:(x-y)/np.sqrt((x*(1-x)+y*(1-y))/2)
            out.append(dict(comp=lab,var=k+', %',b1=f'{p[0]*100:.1f}',b2=f'{p[1]*100:.1f}',a1=f'{p[2]*100:.1f}',a2=f'{p[3]*100:.1f}',smd_b=f'{abs(smd(p[0],p[1])):.2f}',smd_a=f'{abs(smd(p[2],p[3])):.2f}'))
d=pd.DataFrame(out); d.to_csv('../baseline_all.csv',index=False)
x=d[d.smd_a!='']; x=x.assign(s=x.smd_a.astype(float))
print(x.groupby('comp').s.max()); print(x[x.s>0.1][['comp','var','a1','a2','smd_a']])
