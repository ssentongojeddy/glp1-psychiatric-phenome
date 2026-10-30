import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'Inter','font.size':7.5,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#555','xtick.color':'#333','ytick.color':'#333'})
exec(open('style.py').read().split('A=pd.read_csv')[0])
A=pd.read_csv('all6_calibrated.csv'); B=pd.read_csv('baseline_all.csv')
DOM=[('Substance use',['F10','F11','F12','F14','F15','F17']),('Psychosis and bipolar',['F20','F31']),('Suicidality',['R45.851','T14.91']),('Depression, anxiety, stress, sleep',['F32','F33','F41','F43','G47.0']),('Eating, impulse and compulsive',['F50.2','F50.0','F63.0','F42']),('Negative controls',['L60.0','H60','J30','D22','S52','H52'])]
NAME={'F10':'Alcohol use disorder','F11':'Opioid use disorder','F12':'Cannabis use disorder','F14':'Cocaine use disorder','F15':'Other stimulant use disorder','F17':'Nicotine dependence','F20':'Schizophrenia','F31':'Bipolar disorder','R45.851':'Suicidal ideation','T14.91':'Suicide attempt','F32':'Major depressive disorder, single episode','F33':'Major depressive disorder, recurrent','F41':'Anxiety disorders','F43':'Stress-related and adjustment disorders','G47.0':'Insomnia','F50.2':'Bulimia nervosa','F50.0':'Anorexia nervosa','F63.0':'Pathological gambling','F42':'Obsessive-compulsive disorder','L60.0':'Ingrowing nail','H60':'Otitis externa','J30':'Allergic rhinitis','D22':'Melanocytic naevi','S52':'Forearm fracture','H52':'Refraction disorders'}
DOMX=DOM
COMPS=[c for c in COMPS if c in set(A.comparison)]
n=0
def save(fig,name):
    global n; n+=1; fig.savefig(f'sfigs5/SFig{n:02d}_{name}.png',dpi=250,bbox_inches='tight'); fig.savefig(f'sfigs5/SFig{n:02d}_{name}.pdf',bbox_inches='tight'); plt.close(fig)
lg=lambda ax: (ax.set_xscale('log'), ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()))
# 1-6 raw vs calibrated forest per comparison
for k,cp in enumerate(COMPS):
    d=A[A.comparison==cp].set_index('code')
    fig,ax=plt.subplots(figsize=(6.6,7.2)); y=0; ticks=[];labs=[]
    for dom,codes in DOM:
        ax.text(0.22,y-0.1,dom,fontweight='bold',fontsize=7.2,va='bottom'); y-=0.9
        for c in codes:
            if c in d.index:
                r=d.loc[c]
                ax.plot([r.lo,r.hi],[y+0.17]*2,color='#9aa3ad',lw=1); ax.plot(r.HR,y+0.17,'s',ms=3.2,color='#9aa3ad')
                if r.role!='negative-control':
                    sig=r.q_cal<0.05; ax.plot([max(r.clo,0.2),min(r.chi,4)],[y-0.17]*2,color=C[k],lw=1.2); ax.plot(r.cHR,y-0.17,'o',ms=3.8,color=C[k],mfc=C[k] if sig else 'white')
                    ax.text(4.6,y,f'{r.cHR:.2f} ({r.clo:.2f}–{r.chi:.2f})'+('*' if sig else ''),fontsize=6.4,va='center',color='#333')
                else: ax.text(4.6,y,f'{r.HR:.2f} ({r.lo:.2f}–{r.hi:.2f})',fontsize=6.4,va='center',color='#777')
            ticks.append(y); labs.append(NAME[c]); y-=1
        y-=0.3
    ax.axvline(1,color='#444',lw=0.7,ls='--'); lg(ax); ax.set_xlim(0.2,4); ax.set_xticks([0.25,0.5,1,2,4]); ax.set_xticklabels(['0.25','0.5','1','2','4'])
    ax.set_yticks(ticks); ax.set_yticklabels(labs); ax.tick_params(axis='y',length=0); ax.set_ylim(y+0.3,0.8)
    ax.plot([],[],'s-',color='#9aa3ad',label='Uncalibrated HR'); ax.plot([],[],'o-',color=C[k],label='Calibrated HR'); ax.legend(frameon=False,loc='lower right',fontsize=6.5)
    ax.set_xlabel('Hazard ratio (95% CI), log scale'); ax.set_title(cp+': uncalibrated and calibrated estimates',loc='left',fontweight='bold',fontsize=8.5)
    ax.text(4.6,0.7,'Calibrated HR (95% CI)',fontsize=6.4,fontweight='bold')
    save(fig,f'forest_{k+1}')
# 7 negative controls with CI
nr=int(np.ceil(len(COMPS)/4)); fig,axs=plt.subplots(nr,4,figsize=(7.4,2.5*nr+0.4),sharex=True)
for k,(cp,ax) in enumerate(zip(COMPS,axs.flat)):
    d=A[(A.comparison==cp)&(A.role=='negative-control')].set_index('code').loc[NC].reset_index()
    mu=d.null_HR.iloc[0]; tau=d.tau.iloc[0]; col=C[COMPS.index(cp)] if cp in COMPS else C[k]
    ax.axvspan(np.exp(np.log(mu)-1.96*tau),np.exp(np.log(mu)+1.96*tau),color=col,alpha=0.10,lw=0)
    for i,r in d.iterrows(): ax.plot([r.lo,r.hi],[-i,-i],color=col,lw=1.1); ax.plot(r.HR,-i,'o',ms=3.2,color=col)
    ax.axvline(1,color='#444',lw=0.6,ls=(0,(3,2))); ax.axvline(mu,color='#222',lw=1.1)
    ax.set_yticks(-np.arange(len(d))); ax.set_yticklabels([NAME[c] for c in d.code] if k%4==0 else []); ax.tick_params(axis='y',length=0)
    lg(ax); ax.set_xlim(0.55,1.65); ax.set_xticks([0.7,1,1.4]); ax.set_xticklabels(['0.7','1','1.4']); ax.set_ylim(-len(d)+0.4,0.6)
    ax.set_title(SHORT[COMPS.index(cp)].replace('\n',' ')+f'\nbias HR {mu:.2f} · τ {tau:.2f}',fontsize=6.4,loc='left',color='#222')
for ax in list(axs.flat)[len(COMPS):]: ax.axis('off')
fig.supxlabel('Uncalibrated HR (95% CI)',fontsize=7.5); plt.tight_layout(); save(fig,'negative_controls_CI')
# 8-13 Love plots
for k,cp in enumerate(COMPS):
    d=B[(B.comp==cp)&(B['var']!='N')].copy(); d['sb']=d.smd_b.astype(float); d['sa']=d.smd_a.astype(float); d=d.sort_values('sb')
    fig,ax=plt.subplots(figsize=(5.2,5.0)); y=np.arange(len(d))
    for yy,(b,a) in zip(y,zip(d.sb,d.sa)): ax.plot([a,b],[yy,yy],color='#d8dee6',lw=1.5,zorder=1)
    ax.scatter(d.sb,y,s=18,facecolor='white',edgecolor='#9aa3ad',label='Before matching',zorder=2); ax.scatter(d.sa,y,s=18,color=C[k],label='After matching',zorder=3)
    ax.axvline(0.1,color='#c23b6b',lw=0.8,ls='--'); ax.text(0.105,len(d)-0.6,'0.1',color='#c23b6b',fontsize=6.5)
    ax.set_yticks(y); ax.set_yticklabels(d['var'].str.replace(', %','').str.replace(', mean (SD)',' (mean)')); ax.tick_params(axis='y',length=0)
    ax.set_xlabel('Absolute standardized mean difference'); ax.set_title(cp+': covariate balance',loc='left',fontweight='bold',fontsize=8.5); ax.legend(frameon=False,loc='lower right',fontsize=6.5)
    save(fig,f'balance_{k+1}')
# 14 volcano
P=A[A.role!='negative-control'].copy()
fig,ax=plt.subplots(figsize=(7.2,4.6))
for k,cp in enumerate(COMPS):
    d=P[P.comparison==cp]; ax.scatter(np.log2(d.cHR),-np.log10(d.q_cal.clip(lower=1e-12)),s=18,color=C[k],alpha=0.9,label=cp,edgecolor='white',lw=0.4)
pl=[]
lab=P[(P.q_cal<0.05)].assign(lq=-np.log10(P.q_cal)).sort_values('lq',ascending=False).drop_duplicates('code').head(7)
for _,r in lab.iterrows():
    x,y=np.log2(r.cHR),r.lq; ty=y; tx=x+(0.18 if r.cHR<1 else -0.18)
    while any(abs(ty-py)<0.45 and abs(tx-px)<1.0 for px,py in pl): ty-=0.5
    pl.append((tx,ty)); ax.annotate(NAME[r.code].replace(' use disorder','').replace('Other stimulant','Stimulant'),(x,y),xytext=(tx,ty),fontsize=5.6,color='#333',va='center',ha='left' if r.cHR<1 else 'right',arrowprops=dict(arrowstyle='-',lw=0.35,color='#8995a1',shrinkA=0,shrinkB=2))
ax.axhline(-np.log10(0.05),color='#c23b6b',lw=0.8,ls=(0,(3,2))); ax.axvline(0,color='#444',lw=0.6)
ax.set_xticks(np.log2([0.35,0.5,0.7,1,1.4,2,2.8])); ax.set_xticklabels(['0.35','0.5','0.7','1','1.4','2','2.8'])
ax.set_xlabel('Calibrated hazard ratio (log scale)'); ax.set_ylabel('−log$_{10}$ FDR q'); ax.legend(frameon=False,fontsize=6,loc='upper left',bbox_to_anchor=(1.01,1.0)); ax.set_title(f'All psychiatric estimates across {len(COMPS)} comparisons',loc='left',fontweight='bold',fontsize=8.5)
plt.tight_layout()
save(fig,'volcano')
# 15 concordance
fig,axs=plt.subplots(1,3,figsize=(7.4,2.8))
base=P[P.comparison==COMPS[0]].set_index('code').cHR
for ax,(j,cp) in zip(axs,[(2,COMPS[2]),(1,COMPS[1]),(4,COMPS[4])]):
    o=P[P.comparison==cp].set_index('code').cHR; ix=base.index.intersection(o.index)
    ax.scatter(base[ix],o[ix],s=16,color=C[j]); ax.set_xscale('log'); ax.set_yscale('log'); lim=[0.3,2.8]; ax.plot(lim,lim,ls=':',color='#999'); ax.set_xlim(lim); ax.set_ylim(lim)
    for t in (ax.xaxis,ax.yaxis): t.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f')); t.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xticks([0.5,1,2]); ax.set_yticks([0.5,1,2]); r=np.corrcoef(np.log(base[ix]),np.log(o[ix]))[0,1]
    ax.text(0.32,2.2,f'r = {r:.2f}',fontsize=7); ax.set_xlabel('Semaglutide vs SGLT2i, HR'); ax.set_ylabel(cp+', HR',fontsize=7)
plt.tight_layout(); save(fig,'concordance')
# 16 crude risks
fig,axs=plt.subplots(1,2,figsize=(7.4,4.8),sharey=True)
codes=[c for _,cs in DOM[:-1] for c in cs]
for ax,(k,cp) in zip(axs,[(0,COMPS[0]),(1,COMPS[1])]):
    d=P[P.comparison==cp].set_index('code')
    for i,c in enumerate(codes):
        if c not in d.index: continue
        r=d.loc[c]; a=r.events_c1/r.n_c1*1000; b=r.events_c2/r.n_c2*1000
        ax.plot([a,b],[-i,-i],color='#d8dee6',lw=2); ax.plot(b,-i,'o',color='#9aa3ad',ms=4); ax.plot(a,-i,'o',color=C[k],ms=4)
    ax.set_xscale('log'); ax.set_xlim(0.05,120); ax.set_yticks(-np.arange(len(codes))); ax.set_yticklabels([NAME[c] for c in codes]); ax.tick_params(axis='y',length=0)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g')); ax.set_xlabel('New diagnoses per 1,000 (crude, log scale)'); ax.set_title(cp,loc='left',fontweight='bold',fontsize=8)
    ax.plot([],[],'o',color=C[k],label=cp.split(' vs')[0]); ax.plot([],[],'o',color='#9aa3ad',label='SGLT2 inhibitor'); ax.legend(frameon=False,fontsize=6.5,loc='lower right')
plt.tight_layout(); save(fig,'crude_risks')
# 17 E-values
S=P[(P.q_cal<0.05)&(P.cHR<1)].copy(); S['lab']=S.code.map(NAME)
S=S.sort_values(['comparison','E']); nrow=len(S)+2*S.comparison.nunique()
fig,ax=plt.subplots(figsize=(6.4,0.16*nrow+0.9)); y=0; ticks=[];labs=[]
for k,cp in enumerate(COMPS):
    d=S[S.comparison==cp].sort_values('E',ascending=False)
    if not len(d): continue
    ax.text(1.03,y,cp,fontsize=6.6,fontweight='bold',color=C[k],va='center'); y-=1
    for _,r in d.iterrows():
        ax.barh(y,r.E-1,left=1,height=0.7,color=C[k],alpha=0.35,lw=0); ax.barh(y,r.E_ci-1,left=1,height=0.7,color=C[k],lw=0); ticks.append(y); labs.append(r.lab); y-=1
    y-=0.7
ax.set_yticks(ticks); ax.set_yticklabels(labs,fontsize=6); ax.tick_params(axis='y',length=0); ax.set_ylim(y+0.4,1)
ax.set_xlim(1,max(5.5,S.E.max()*1.05)); ax.set_xlabel('E-value (dark: CI limit; light: point estimate)')
ax.set_title('E-values for significant inverse associations',loc='left',fontweight='bold',fontsize=8.5); plt.tight_layout()
save(fig,'evalues')
print(n)
