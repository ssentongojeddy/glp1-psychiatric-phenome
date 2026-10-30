import pandas as pd, numpy as np, sys
from scipy.stats import norm
def bh(p):
    p=np.asarray(p); n=len(p); o=np.argsort(p); q=p[o]*n/np.arange(1,n+1); q=np.minimum.accumulate(q[::-1])[::-1]; r=np.empty(n); r[o]=np.minimum(q,1); return r
def calib(f):
    d=pd.read_csv(f); d['b']=np.log(d.HR); d['se']=(np.log(d.hi)-np.log(d.lo))/(2*1.96)
    nc=d[d.role=='negative-control']; w=1/nc.se**2; mu=np.sum(w*nc.b)/np.sum(w)
    Q=np.sum(w*(nc.b-mu)**2); tau2=max(0,(Q-(len(nc)-1))/(np.sum(w)-np.sum(w**2)/np.sum(w)))
    d['cb']=d.b-mu; d['cse']=np.sqrt(d.se**2+tau2)
    d['cHR']=np.exp(d.cb); d['clo']=np.exp(d.cb-1.96*d.cse); d['chi']=np.exp(d.cb+1.96*d.cse)
    d['cp']=2*norm.sf(abs(d.cb/d.cse)); ps=d.role!='negative-control'
    d.loc[ps,'q_cal']=bh(d.loc[ps,'cp'])
    return d, np.exp(mu), np.sqrt(tau2)
if __name__=='__main__':
    for f in sys.argv[1:]:
        d,m,t=calib(f); print(f,'null HR %.3f tau %.3f'%(m,t))
        print(d[d.role!='negative-control'].sort_values('cHR')[['outcome','HR','cHR','clo','chi','q_cal']].round(3).to_string(index=False))
