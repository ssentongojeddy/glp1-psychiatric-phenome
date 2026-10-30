exec(open('style.py').read())
from matplotlib.gridspec import GridSpec
codes=[c for _,cs in DOM for c in cs]
def ypos():
    y=0; Y={}; heads=[]
    for dom,cs in DOM:
        heads.append((y,dom)); y-=0.9
        for c in cs: Y[c]=y; y-=1
        y-=0.35
    return Y,heads,y
Y,HEADS,YMIN=ypos()
def forest(ax,comps,cols,xl=(0.22,3.6),labels=True):
    off=np.linspace(-0.26,0.26,len(comps)) if len(comps)>1 else [0]
    for i,(h,dom) in enumerate(HEADS):
        nxt=HEADS[i+1][0] if i+1<len(HEADS) else YMIN
        if i%2==0: ax.axhspan(nxt+0.2,h+0.2,color='#f2f5f9',zorder=0,lw=0)
        ax.text(xl[0]*1.04,h-0.25,dom,fontsize=6,fontweight='bold',color='#3a4450',va='center',zorder=5,bbox=dict(fc='#f2f5f9' if i%2==0 else 'white',ec='none',pad=0.6))
    for c in codes:
        for k,(cp,col) in enumerate(zip(comps,cols)):
            r=row(cp,c)
            if r is None: continue
            yy=Y[c]+off[k]; sig=r.q_cal<0.05
            ax.plot([max(r.clo,xl[0]),min(r.chi,xl[1])],[yy,yy],color=col,lw=0.9,solid_capstyle='round',zorder=2)
            ax.plot(r.cHR,yy,marker='o',ms=3.3,color=col,mfc=col if sig else 'white',mew=0.9,zorder=3)
    ax.axvline(1,color='#3a4450',lw=0.6,ls=(0,(3,2)),zorder=1)
    logx(ax,[0.25,0.5,1,2,3]); ax.set_xlim(*xl); ax.set_ylim(YMIN+0.4,0.6)
    ax.set_yticks([Y[c] for c in codes]); ax.set_yticklabels([NAME[c] for c in codes] if labels else []); ax.tick_params(axis='y',length=0)
    ax.spines['left'].set_visible(False)
# ---------------- Fig 2
fig=plt.figure(figsize=(7.2,8.6)); gs=GridSpec(2,3,figure=fig,height_ratios=[3.1,1],width_ratios=[1.25,0.75,0.95],hspace=0.36,wspace=0.14,left=0.255,right=0.98,top=0.95,bottom=0.06)
a=fig.add_subplot(gs[0,0:2]); b=fig.add_subplot(gs[0,2])
_A=[PRIM,COMPS[0],COMPS[1]]; _AC=[C[8],C[0],C[1]]
forest(a,_A[::-1],_AC[::-1]); a.set_xlabel('Calibrated hazard ratio (95% CI)'); panel(a,'a',-0.3)
a.set_title('Primary analysis and drug-specific comparisons with SGLT2 inhibitors, type 2 diabetes',fontsize=6.6)
for k in range(3): a.plot([],[],'o-',color=_AC[k],ms=3.3,lw=0.9,label=['Semaglutide or tirzepatide (primary)','Semaglutide','Tirzepatide'][k])
a.plot([],[],'o',color='#3a4450',mfc='white',ms=3.3,label='q ≥ 0.05'); a.legend(frameon=False,loc='upper left',bbox_to_anchor=(0.0,-0.075),ncol=4,handlelength=1.6,columnspacing=1.0)
forest(b,[COMPS[3]],[C[3]],xl=(0.22,2.6),labels=False); logx(b,[0.25,0.5,1,2]); b.set_xlim(0.22,2.6); b.set_xlabel('Calibrated HR (95% CI)')
b.set_title('Tirzepatide vs semaglutide',fontsize=6.6); panel(b,'b',-0.02)
for c in codes:
    r=row(COMPS[3],c)
    if r is not None: b.text(2.55,Y[c],f'{r.cHR:.2f}',fontsize=5.4,ha='right',va='center',color='#5c6f82')
# c: crude risks dumbbell key outcomes
c_ax=fig.add_subplot(gs[1,0:2]); key=['F14','F15','F12','F11','F17','F10','F20','F31','R45.851','T14.91']
xs=np.arange(len(key))
for j,(cp,col,dx) in enumerate([(COMPS[0],C[0],-0.18),(COMPS[1],C[1],0.18)]):
    for i,cc in enumerate(key):
        r=row(cp,cc); a1=r.events_c1/r.n_c1*1000; a2=r.events_c2/r.n_c2*1000
        c_ax.plot([i+dx,i+dx],[a2,a1],color=col,lw=1.6,alpha=0.35); c_ax.plot(i+dx,a2,'o',ms=3.2,color='#aab4bf'); c_ax.plot(i+dx,a1,'o',ms=3.6,color=col)
c_ax.set_yscale('log'); c_ax.set_xticks(xs); c_ax.set_xticklabels([NAME[k].replace(' use disorder','').replace('Other stimulant','Stimulant').replace('Nicotine dependence','Nicotine').replace(' disorder','') for k in key],rotation=35,ha='right')
c_ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g')); c_ax.set_ylabel('New diagnoses per 1,000\n(crude, 3 years)')
c_ax.plot([],[],'o',color=C[0],label='Semaglutide'); c_ax.plot([],[],'o',color=C[1],label='Tirzepatide'); c_ax.plot([],[],'o',color='#aab4bf',label='SGLT2 inhibitor')
c_ax.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(0.5,1.16)); panel(c_ax,'c',-0.05,1.04)
# d: concordance
d_ax=fig.add_subplot(gs[1,2]); P=A[A.role!='negative-control']
x=P[P.comparison==COMPS[0]].set_index('code'); y=P[P.comparison==COMPS[2]].set_index('code'); ix=x.index.intersection(y.index)
d_ax.errorbar(x.cHR[ix],y.cHR[ix],xerr=[x.cHR[ix]-x.clo[ix],x.chi[ix]-x.cHR[ix]],yerr=[y.cHR[ix]-y.clo[ix],y.chi[ix]-y.cHR[ix]],fmt='none',ecolor='#c9d3de',lw=0.6,zorder=1)
d_ax.scatter(x.cHR[ix],y.cHR[ix],s=14,color=C[2],edgecolor='white',lw=0.4,zorder=3)
d_ax.set_xscale('log'); d_ax.set_yscale('log'); lim=[0.35,3]; d_ax.plot(lim,lim,ls=':',color='#8995a1',lw=0.7); d_ax.set_xlim(lim); d_ax.set_ylim(lim)
for t in (d_ax.xaxis,d_ax.yaxis): t.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g')); t.set_minor_formatter(matplotlib.ticker.NullFormatter())
d_ax.set_xticks([0.5,1,2]); d_ax.set_yticks([0.5,1,2]); r_=np.corrcoef(np.log(x.cHR[ix]),np.log(y.cHR[ix]))[0,1]
d_ax.text(0.38,2.3,f'r = {r_:.2f}',fontsize=6); d_ax.set_xlabel('HR, semaglutide vs SGLT2i'); d_ax.set_ylabel('HR, semaglutide vs DPP-4i'); panel(d_ax,'d',-0.3,1.04)
finalize(fig); fig.savefig('figs/Fig2_forest_T2D.png',dpi=400); fig.savefig('figs/Fig2_forest_T2D.pdf'); plt.close(fig)
# ---------------- Fig 3
HC=[PRIM]+[c for c in COMPS[:8] if c in set(A.comparison)]; HS=[SHORT[COMPS.index(c)] for c in HC]; HCOL=[C[COMPS.index(c)] for c in HC]; nC=len(HC)
fig=plt.figure(figsize=(7.2,9.4)); gs=GridSpec(2,2,figure=fig,height_ratios=[2.9,1],width_ratios=[1,1.15],wspace=0.55,hspace=0.2,left=0.24,right=0.97,top=0.93,bottom=0.06)
h=fig.add_subplot(gs[0,:])
M=np.array([[row(cp,c).cHR if row(cp,c) is not None else np.nan for cp in HC] for c in codes]); Q=np.array([[row(cp,c).q_cal if row(cp,c) is not None else np.nan for cp in HC] for c in codes])
L=np.log2(M); im=h.imshow(L,cmap=CM,norm=TwoSlopeNorm(0,-1.5,1.5),aspect='auto')
for i in range(len(codes)):
    for j in range(nC):
        if np.isnan(M[i,j]): h.text(j,i,'–',ha='center',va='center',fontsize=6,color='#8995a1'); continue
        s_=Q[i,j]<0.05; h.text(j,i,f'{M[i,j]:.2f}',ha='center',va='center',fontsize=6,color='white' if abs(L[i,j])>0.75 else '#1f2328',fontweight='bold' if s_ else 'normal')
        if s_: h.add_patch(plt.Rectangle((j-0.47,i-0.47),0.94,0.94,fill=False,ec='#1f2328',lw=0.7))
h.set_yticks(range(len(codes))); h.set_yticklabels([NAME[c] for c in codes]); h.set_xticks(range(nC)); h.set_xticklabels(['Primary:\nsema or tirz\nvs SGLT2i' if c==PRIM else SHORT[COMPS.index(c)].replace(' vs ','\nvs ') for c in HC],fontsize=5.6,linespacing=1.05); h.xaxis.tick_top()
for j,(lab,col) in enumerate(zip(h.get_xticklabels(),HCOL)): lab.set_color(col); lab.set_fontweight('bold')
k=0
for dom,cs in DOM[:-1]: k+=len(cs); h.axhline(k-0.5,color='white',lw=2.4)
for s_ in h.spines.values(): s_.set_visible(False)
h.tick_params(length=0); panel(h,'a',-0.33,1.06)
cax=h.inset_axes([0.0,-0.045,0.42,0.012]); cb=fig.colorbar(im,cax=cax,orientation='horizontal',ticks=np.log2([0.4,0.5,0.7,1,1.4,2,2.8])); cb.ax.set_xticklabels(['0.4','0.5','0.7','1','1.4','2','2.8'],fontsize=5.6); cb.outline.set_visible(False)
h.text(0.44,-0.04,'Calibrated HR · boxed and bold: FDR q < 0.05 · –, count suppressed',transform=h.transAxes,fontsize=5.8,color='#3a4450',va='center')
bx=fig.add_subplot(gs[1,0]); P=A[A.role!='negative-control']
lo=[((P.comparison==cp)&(P.q_cal<0.05)&(P.cHR<1)).sum() for cp in HC]; hi=[((P.comparison==cp)&(P.q_cal<0.05)&(P.cHR>1)).sum() for cp in HC]
yy=np.arange(nC)[::-1]; bx.barh(yy,lo,color=HCOL,height=0.62); bx.barh(yy,[-v for v in hi],color='#a993d8',height=0.62)
for i in range(nC):
    bx.text(lo[i]+0.25,yy[i],str(lo[i]),va='center',fontsize=5.8)
    if hi[i]: bx.text(-hi[i]-0.25,yy[i],str(hi[i]),va='center',ha='right',fontsize=5.8)
bx.axvline(0,color='#3a4450',lw=0.6); bx.set_yticks(yy); bx.set_yticklabels([s.replace('\n',' ') for s in HS],fontsize=5.8); bx.tick_params(axis='y',length=0); bx.spines['left'].set_visible(False)
if max(hi)>0:
    bx.set_xlim(-4,12.5); bx.set_xticks([-2,0,4,8,12]); bx.set_xticklabels(['2','0','4','8','12'])
    bx.text(-0.5,nC-0.35,'higher',ha='right',fontsize=5.8,color='#6a4bb3'); bx.text(0.5,nC-0.35,'lower risk',fontsize=5.8,color=C[0])
else:
    bx.set_xlim(0,12.5); bx.set_xticks([0,4,8,12])
bx.set_xlabel('Outcomes with significantly lower risk (FDR q < 0.05)'); panel(bx,'b',-0.62,1.02)
vx=fig.add_subplot(gs[1,1])
for k_,cp in enumerate(HC):
    d=P[P.comparison==cp]; vx.scatter(np.log2(d.cHR),-np.log10(d.q_cal.clip(lower=1e-12)),s=11,color=HCOL[k_],alpha=0.9,edgecolor='white',lw=0.3)
vx.axhline(-np.log10(0.05),color='#6a4bb3',lw=0.6,ls=(0,(3,2))); vx.axvline(0,color='#3a4450',lw=0.5)
_pl=[]
for _,r in P[(P.q_cal<1e-6)&(P.cHR<1)].sort_values('q_cal').drop_duplicates('code').head(4).iterrows():
    _x,_y=np.log2(r.cHR),-np.log10(r.q_cal)
    while any(abs(_y-py)<0.45 and abs(_x-px)<1.2 for px,py in _pl): _y-=0.5
    _pl.append((_x,_y)); vx.annotate(NAME[r.code].replace(' use disorder','').replace('Other stimulant','Stimulant'),(np.log2(r.cHR),-np.log10(r.q_cal)),xytext=(_x+0.12,_y),fontsize=5,color='#3a4450',va='center',arrowprops=dict(arrowstyle='-',lw=0.3,color='#8995a1',shrinkA=0,shrinkB=1.5))
vx.set_xticks(np.log2([0.35,0.5,0.7,1,1.4,2,2.8])); vx.set_xticklabels(['0.35','0.5','0.7','1','1.4','2','2.8']); vx.set_xlabel('Calibrated HR'); vx.set_ylabel('−log$_{10}$ FDR q')
panel(vx,'c',-0.18,1.02)
finalize(fig); fig.savefig('figs/Fig3_heatmap.png',dpi=400); fig.savefig('figs/Fig3_heatmap.pdf'); plt.close(fig)
# ---------------- Fig 5 untreated comparators
HC=[c for c in COMPS if c in set(A.comparison)]
UC=[c for c in HC if 'no drug' in c]; UCOL=[C[COMPS.index(c)] for c in UC]
fig=plt.figure(figsize=(7.2,8.2)); gs=GridSpec(2,2,figure=fig,height_ratios=[3.1,1],width_ratios=[1,1],hspace=0.3,wspace=0.35,left=0.255,right=0.98,top=0.945,bottom=0.06)
a=fig.add_subplot(gs[0,:]); forest(a,UC,UCOL,xl=(0.2,3.6)); a.set_xlabel('Calibrated HR (95% CI)'); panel(a,'a',dy=1.04)
for k_,cp in enumerate(UC): a.plot([],[],'o-',color=UCOL[k_],ms=3.3,lw=0.9,label=cp.replace('(obesity+OSA)','(obesity with sleep apnoea, no T2D)'))
a.legend(frameon=False,loc='lower center',bbox_to_anchor=(0.45,1.02),ncol=2,fontsize=5.6,handlelength=1.6)
for j,(act,unt,col,lab) in enumerate([(COMPS[0],COMPS[4],C[0],'Semaglutide'),(COMPS[1],COMPS[5],C[1],'Tirzepatide')]):
    ax=fig.add_subplot(gs[1,j]); P=A[A.role!='negative-control']
    x=P[P.comparison==act].set_index('code'); y=P[P.comparison==unt].set_index('code'); ix=x.index.intersection(y.index)
    ax.errorbar(x.cHR[ix],y.cHR[ix],xerr=[x.cHR[ix]-x.clo[ix],x.chi[ix]-x.cHR[ix]],yerr=[y.cHR[ix]-y.clo[ix],y.chi[ix]-y.cHR[ix]],fmt='none',ecolor='#c9d3de',lw=0.6,zorder=1)
    ax.scatter(x.cHR[ix],y.cHR[ix],s=14,color=col,edgecolor='white',lw=0.4,zorder=3)
    ax.set_xscale('log'); ax.set_yscale('log'); lim=[0.3,3]; ax.plot(lim,lim,ls=':',color='#8995a1',lw=0.7); ax.set_xlim(lim); ax.set_ylim(lim)
    for t in (ax.xaxis,ax.yaxis): t.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g')); t.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xticks([0.5,1,2]); ax.set_yticks([0.5,1,2]); r_=np.corrcoef(np.log(x.cHR[ix]),np.log(y.cHR[ix]))[0,1]
    ax.text(0.33,2.3,f'r = {r_:.2f}',fontsize=6); ax.set_xlabel(f'HR, {lab.lower()} vs SGLT2i'); ax.set_ylabel(f'HR, {lab.lower()} vs no drug'); ax.set_title(f'{lab}: active vs untreated comparator',fontsize=6.6)
    panel(ax,'bc'[j])
finalize(fig); fig.savefig('figs/Fig5_untreated.png',dpi=400); fig.savefig('figs/Fig5_untreated.pdf'); plt.close(fig)
# ---------------- Fig 6 bias and robustness
HC=[PRIM]+[c for c in COMPS[:8] if c in set(A.comparison)]
fig=plt.figure(figsize=(7.2,9.6)); nC=len(HC)
outer=GridSpec(3,1,figure=fig,height_ratios=[1.35,1,1],hspace=0.5,left=0.15,right=0.98,top=0.955,bottom=0.05)
from matplotlib.gridspec import GridSpecFromSubplotSpec as SGS
g0=SGS(2,5,subplot_spec=outer[0],hspace=0.75,wspace=0.12)
for k_,cp in enumerate(HC):
    ax=fig.add_subplot(g0[k_//5,k_%5]); d=A[(A.comparison==cp)&(A.role=='negative-control')].set_index('code').loc[NC]
    mu=d.null_HR.iloc[0]; tau=d.tau.iloc[0]; col=C[COMPS.index(cp)]
    ax.axvspan(np.exp(np.log(mu)-1.96*tau),np.exp(np.log(mu)+1.96*tau),color=col,alpha=0.12,lw=0)
    for i,c in enumerate(NC):
        r=d.loc[c]; ax.plot([r.lo,r.hi],[-i,-i],color=col,lw=0.9); ax.plot(r.HR,-i,'o',ms=2.8,color=col)
    ax.axvline(1,color='#3a4450',lw=0.5,ls=(0,(3,2))); ax.axvline(mu,color='#1f2328',lw=1)
    logx(ax,[0.7,1,1.4]); ax.set_xlim(0.6,1.6); ax.set_yticks(-np.arange(6)); ax.set_yticklabels([NAME[c] for c in NC] if k_%5==0 else [],fontsize=5.4); ax.tick_params(axis='y',length=0); ax.spines['left'].set_visible(False)
    ax.set_title(SHORT[COMPS.index(cp)].replace('\n',' '),fontsize=5.8,fontweight='bold',color=col,pad=9); ax.text(0.0,1.01,f'bias {mu:.2f} · τ {tau:.2f}',transform=ax.transAxes,fontsize=5,color='#5c6f82',va='bottom')
    if k_==0: panel(ax,'a',dy=1.12)
    if k_>=4: ax.set_xlabel('Uncalibrated HR',fontsize=5.8)
g1=SGS(1,2,subplot_spec=outer[1],wspace=0.55,width_ratios=[1,1.15])
bx=fig.add_subplot(g1[0]); P=A[A.role!='negative-control']
for cp in HC:
    d=P[P.comparison==cp]; bx.scatter(d.HR,d.cHR,s=8,color=C[COMPS.index(cp)],alpha=0.85,edgecolor='white',lw=0.3)
lim=[0.33,2.8]; bx.plot(lim,lim,ls=':',color='#8995a1',lw=0.7); bx.set_xscale('log'); bx.set_yscale('log'); bx.set_xlim(lim); bx.set_ylim(lim)
for t in (bx.xaxis,bx.yaxis): t.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g')); t.set_minor_formatter(matplotlib.ticker.NullFormatter())
bx.set_xticks([0.5,1,2]); bx.set_yticks([0.5,1,2]); bx.axhline(1,color='#3a4450',lw=0.4,ls=(0,(3,2))); bx.axvline(1,color='#3a4450',lw=0.4,ls=(0,(3,2)))
sr=((P.hi<1)|(P.lo>1)); sc=P.q_cal<0.05
bx.text(0.36,2.3,f'Significant before calibration: {int(sr.sum())}\nafter calibration: {int(sc.sum())} (lost {int((sr&~sc).sum())}, gained {int((~sr&sc).sum())})',fontsize=5.2,va='top',color='#3a4450',bbox=dict(fc='white',ec='none',pad=1.2),zorder=5)
bx.set_xlabel('Uncalibrated HR'); bx.set_ylabel('Calibrated HR'); bx.set_title('Effect of calibration, all comparisons',fontsize=6.6); panel(bx,'b')
cx=fig.add_subplot(g1[1]); keyo=['F14','F15','F12','F11','F17','F10','F20','F31','R45.851','T14.91','F32']
for i,c in enumerate(keyo):
    if i%2==0: cx.axhspan(-i-0.45,-i+0.45,color='#f2f5f9',lw=0,zorder=0)
    for k_,cp in enumerate(HC):
        r=row(cp,c)
        if r is None or not (r.q_cal<0.05 and r.cHR<1): continue
        yy=-i+0.08*(k_-(len(HC)-1)/2); col=C[COMPS.index(cp)]
        cx.plot([r.E_ci,r.E],[yy]*2,color=col,lw=0.9,alpha=0.6); cx.plot(r.E,yy,'o',ms=2.6,color=col)
cx.set_yticks(-np.arange(len(keyo))); cx.set_yticklabels([NAME[c] for c in keyo],fontsize=5.6); cx.tick_params(axis='y',length=0); cx.spines['left'].set_visible(False)
cx.set_xlim(1,5.4); cx.set_ylim(-len(keyo)+0.5,0.5); cx.set_xlabel('E-value (line to CI-limit E-value)');
for cp in HC:
    if any((row(cp,c) is not None) and row(cp,c).q_cal<0.05 and row(cp,c).cHR<1 for c in keyo): cx.plot([],[],'o',ms=3,color=C[COMPS.index(cp)],label=SHORT[COMPS.index(cp)].replace('\n',' '))
cx.legend(frameon=False,fontsize=5,ncol=3,loc='upper center',bbox_to_anchor=(0.4,-0.2),handletextpad=0.2,columnspacing=0.8)
cx.set_title('Robustness to unmeasured confounding',fontsize=6.6); panel(cx,'c')
g2=SGS(1,2,subplot_spec=outer[2],wspace=0.85,width_ratios=[1,1])
dx=fig.add_subplot(g2[0]); d=B[(B.comp==PRIM)&(B['var']!='N')].copy(); d['sb']=d.smd_b.astype(float); d['sa']=d.smd_a.astype(float); d=d.sort_values('sb'); yy=np.arange(len(d))
for y_,(b_,a_) in zip(yy,zip(d.sb,d.sa)): dx.plot([a_,b_],[y_,y_],color='#d8dee6',lw=1.2)
dx.scatter(d.sb,yy,s=9,facecolor='white',edgecolor='#8995a1',lw=0.7,label='Before matching',zorder=3); dx.scatter(d.sa,yy,s=9,color=C[8],label='After matching',zorder=4)
dx.axvline(0.1,color='#D55E00',lw=0.6,ls=(0,(3,2))); dx.set_yticks(yy); dx.set_yticklabels(d['var'].str.replace(', %','').str.replace(', mean (SD)',' (mean)').str.replace('Anxiety and stress-related disorders','Anxiety/stress disorders').str.replace('Childhood-onset behavioural disorders','Childhood-onset disorders').str.replace('Age at Index','Age'),fontsize=5); dx.tick_params(axis='y',length=0); dx.spines['left'].set_visible(False)
dx.set_xlabel('Absolute SMD'); dx.legend(frameon=False,fontsize=5.2,loc='lower right'); dx.set_title('Covariate balance, primary analysis',fontsize=6.6); panel(dx,'d')
ex=fig.add_subplot(g2[1]); key=['F14','F15','F12','F11','F17','F10','F20','F31','R45.851','T14.91']
S_=pd.read_csv('sens_absolute_risk.csv')
for j,(cp,col,off,lab) in enumerate([(PRIM,C[8],0.0,'Semaglutide or tirzepatide')]):
    s_=S_[S_.comparison==cp].set_index('code').loc[key]; yy=np.arange(len(key))[::-1]
    ex.errorbar(s_.RDm,yy,xerr=[s_.RDm-s_.RDm_lo,s_.RDm_hi-s_.RDm],fmt='o',ms=3.2,color=col,ecolor=col,elinewidth=0.9,capsize=0)
ex.axvline(0,color='#3a4450',lw=0.6); ex.set_yticks(np.arange(len(key))[::-1]); ex.set_yticklabels([NAME[k] for k in key],fontsize=5.6); ex.tick_params(axis='y',length=0); ex.spines['left'].set_visible(False)
ex.set_xlim(-14.5,1); ex.set_xticks([-12,-8,-4,0]); ex.set_xticklabels(['−12','−8','−4','0'])
ex.set_xlabel('Difference per 1,000 vs SGLT2i, 3 years (95% CI)'); ex.set_title('Absolute differences, primary analysis',fontsize=6.6); panel(ex,'e')
finalize(fig); fig.savefig('figs/Fig6_bias_robustness.png',dpi=400); fig.savefig('figs/Fig6_bias_robustness.pdf'); plt.close(fig)
print('ok')
