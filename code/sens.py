"""Absolute risk differences and calibration sensitivity (no new TriNetX data needed)."""
import pandas as pd, numpy as np, sys
from scipy.stats import norm
from calib import bh
from combine import F
from style import NAME

def calib_variant(d, mode='re', drop=None):
    d = d.copy(); d['b'] = np.log(d.HR); d['se'] = (np.log(d.hi) - np.log(d.lo)) / (2 * 1.96)
    nc = d[d.role == 'negative-control']
    if drop is not None: nc = nc[nc.code != drop]
    w = 1 / nc.se**2; mu = np.sum(w * nc.b) / np.sum(w)
    Q = np.sum(w * (nc.b - mu)**2)
    tau2 = 0.0 if mode == 'fe' else max(0, (Q - (len(nc) - 1)) / (np.sum(w) - np.sum(w**2) / np.sum(w)))
    d['cb'] = d.b - mu; d['cse'] = np.sqrt(d.se**2 + tau2)
    d['cHR'] = np.exp(d.cb); d['clo'] = np.exp(d.cb - 1.96 * d.cse); d['chi'] = np.exp(d.cb + 1.96 * d.cse)
    d['cp'] = 2 * norm.sf(abs(d.cb / d.cse)); ps = d.role != 'negative-control'
    d.loc[ps, 'q'] = bh(d.loc[ps, 'cp'])
    return d

files = F + ([('primary_glp1class_vs_sglt2.csv', 'Semaglutide or tirzepatide vs SGLT2i (primary)')] if len(sys.argv) > 1 else [])
ard, cal = [], []
for f, lab in files:
    d = pd.read_csv(f)
    # absolute risk difference per 1,000 over 3 years (cumulative risk, Wald 95% CI)
    p1 = d.events_c1 / d.n_c1; p2 = d.events_c2 / d.n_c2
    rd = (p1 - p2) * 1000; se = np.sqrt(p1 * (1 - p1) / d.n_c1 + p2 * (1 - p2) / d.n_c2) * 1000
    ard.append(pd.DataFrame({'comparison': lab, 'code': d.code, 'outcome': d.code.map(NAME).fillna(d.outcome), 'role': d.role,
                             'risk1_per1000': p1 * 1000, 'risk2_per1000': p2 * 1000, 'RD': rd, 'RD_lo': rd - 1.96 * se, 'RD_hi': rd + 1.96 * se}))
    base = calib_variant(d, 're'); fe = calib_variant(d, 'fe')
    # model-based RD: comparator 3-year risk x (calibrated HR - 1); robust to unequal follow-up
    ard[-1]['cHR'] = base.cHR.values; ard[-1]['RDm'] = p2.values * 1000 * (base.cHR.values - 1)
    ard[-1]['RDm_lo'] = p2.values * 1000 * (base.clo.values - 1); ard[-1]['RDm_hi'] = p2.values * 1000 * (base.chi.values - 1)
    ard[-1]['q_cal'] = base.q.values
    ps = base.role != 'negative-control'
    loo = [calib_variant(d, 're', drop=c) for c in d[d.role == 'negative-control'].code]
    for i in base[ps].index:
        hrs = [x.loc[i, 'cHR'] for x in loo]; nsig = sum(x.loc[i, 'q'] < 0.05 for x in loo)
        cal.append({'comparison': lab, 'code': base.loc[i, 'code'], 'outcome': NAME.get(base.loc[i, 'code'], base.loc[i, 'outcome']),
                    'cHR_RE': base.loc[i, 'cHR'], 'q_RE': base.loc[i, 'q'], 'cHR_FE': fe.loc[i, 'cHR'], 'clo_FE': fe.loc[i, 'clo'], 'chi_FE': fe.loc[i, 'chi'], 'q_FE': fe.loc[i, 'q'],
                    'LOO_min': min(hrs), 'LOO_max': max(hrs), 'LOO_sig_of_6': nsig, 'sig_RE': base.loc[i, 'q'] < 0.05})
A = pd.concat(ard); A.to_csv('sens_absolute_risk.csv', index=False)
C = pd.DataFrame(cal); C.to_csv('sens_calibration.csv', index=False)
# summary
s = C.groupby('comparison').agg(n_sig_RE=('sig_RE', 'sum'), n_sig_FE=('q_FE', lambda x: (x < 0.05).sum()),
                                 robust_all6=('LOO_sig_of_6', lambda x: (x == 6).sum()))
print(s.to_string())
flip = C[C.sig_RE & (C.LOO_sig_of_6 < 6)]
print('\nsignificant under RE but lost in >=1 leave-one-out:\n', flip[['comparison', 'outcome', 'cHR_RE', 'LOO_min', 'LOO_max', 'LOO_sig_of_6']].round(3).to_string(index=False))
