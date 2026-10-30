exec(open('style.py').read())
from km_load import load, interval_ratio
from matplotlib.gridspec import GridSpec
S1=load('sema_sglt2_b1'); S2=load('sema_sglt2_b2'); S3=load('sema_sglt2_b3'); T1=load('tirz_sglt2_b1'); T2=load('tirz_sglt2_b2'); T3=load('tirz_sglt2_b3')
P=[('Cocaine use disorder',S1,T1,'Cocaine related disorders','F14'),('Other stimulant use disorder',S1,T1,'Other stimulant related disorders','F15'),('Cannabis use disorder',S1,T1,'Cannabis related disorders','F12'),('Opioid use disorder',S1,T1,'Opioid related disorders','F11'),
   ('Nicotine dependence',S1,T1,'Nicotine dependence','F17'),('Alcohol use disorder',S1,T1,'Alcohol related disorders','F10'),('Schizophrenia',S2,T2,'Schizophrenia','F20'),('Bipolar disorder',S2,T2,'Bipolar disorder','F31'),
   ('Suicidal ideation',S2,T2,'Suicidal ideations','R45.851'),('Suicide attempt',S3,T3,'Suicide attempt','T14.91'),('Major depressive disorder, single episode',S2,T1,'Depressive episode','F32'),('Major depressive disorder, recurrent',S2,T2,'Major depressive disorder, recurrent','F33'),
   ('Anxiety disorders',S2,T2,'Other anxiety disorders','F41'),('Forearm fracture (control)',S3,T3,'Fracture of forearm',None)]
CS,CT='#0072B2','#D55E00'
fig=plt.figure(figsize=(7.2,7.2)); gs=GridSpec(4,4,figure=fig,hspace=0.62,wspace=0.42,left=0.08,right=0.985,top=0.955,bottom=0.07)
letters='abcdefghijklmnop'
for i,(title,SS,TT,key,code) in enumerate(P):
    ax=fig.add_subplot(gs[i//4,i%4])
    for D_,col,lab in [(SS,CS,'Semaglutide'),(TT,CT,'Tirzepatide')]:
        if key not in D_: continue
        t1,y1=D_[key]['c1']; t2,y2=D_[key]['c2']
        ax.plot(t2,y2,color=col,lw=0.9,ls=(0,(2.5,1.5)),alpha=0.75); ax.plot(t1,y1,color=col,lw=1.3)
    ax.set_xlim(0,1095); ax.set_xticks([0,365,730,1095]); ax.set_xticklabels(['0','1','2','3']); ax.set_ylim(bottom=0)
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4)); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v,p: f'{v:g}'))
    ax.set_title(title.replace(', ',',\n') if len(title)>30 else title,fontsize=6.4,pad=3,linespacing=1.1)
    if code:
        rs=row(COMPS[0],code); rt=row(COMPS[1],code); txt=f'HR sema {rs.cHR:.2f}'+('*' if rs.q_cal<0.05 else '')+(f' · tirz {rt.cHR:.2f}'+('*' if rt.q_cal<0.05 else '') if rt is not None else '')
        ax.text(0.03,0.95,txt,transform=ax.transAxes,fontsize=5.3,va='top',color='#3a4450')
    if i%4==0: ax.set_ylabel('Cumulative incidence (%)',fontsize=5.8)
    if i>=len(P)-4: ax.set_xlabel('Years since first prescription',fontsize=5.8)
    panel(ax,letters[i],dy=1.0)
# legend
lx=fig.add_subplot(gs[3,2:4]); lx.axis('off')
for col,lab in [(CS,'Semaglutide'),(CT,'Tirzepatide')]:
    lx.plot([],[],color=col,lw=1.3,label=lab); lx.plot([],[],color=col,lw=0.9,ls=(0,(2.5,1.5)),label=f'Matched SGLT2 inhibitor ({lab.lower()} analysis)')
lx.legend(ncol=1,frameon=False,loc='center',fontsize=6.2,handlelength=2.6,labelspacing=0.9)
finalize(fig); fig.savefig('figs/Fig4_cumulative_incidence.png',dpi=400); fig.savefig('figs/Fig4_cumulative_incidence.pdf'); plt.close(fig)
# interval ratio figure (supplementary)
rows=[]
for title,SS,TT,key,code in P:
    for lab,D_ in [('Semaglutide',SS),('Tirzepatide',TT)]:
        if key in D_: rows.append((title,lab,[r[4] for r in interval_ratio(D_[key])]))
import km_load as _K
tab=['| Outcome | Drug | 3-year cumulative incidence, drug (%) | 3-year cumulative incidence, SGLT2i (%) | 0–6 months | 6–12 months | 1–2 years | 2–3 years |','|---|---|---|---|---|---|---|---|']
for title,SS,TT,key,code in P:
    for lab,D_ in [('Semaglutide',SS),('Tirzepatide',TT)]:
        if key in D_:
            c=D_[key]; f1=np.interp(1095,*c['c1']); f2=np.interp(1095,*c['c2']); rr=[r[4] for r in interval_ratio(c)]
            tab.append(f'| {title} | {lab} | {f1:.2f} | {f2:.2f} | '+' | '.join(f'{v:.2f}' for v in rr)+' |')
open('ms/supp_table_s7.md','w').write('\n'.join(tab)+'\n')
fig,ax=plt.subplots(figsize=(5.6,7.0)); M=np.array([r[2] for r in rows]); L=np.log2(M)
im=ax.imshow(L,cmap=CM,norm=TwoSlopeNorm(0,-1.5,1.5),aspect='auto')
for i in range(len(rows)):
    for j in range(4): ax.text(j,i,f'{M[i,j]:.2f}',ha='center',va='center',fontsize=5.6,color='white' if abs(L[i,j])>0.8 else '#1f2328')
ax.set_yticks(range(len(rows))); ax.set_yticklabels([f'{r[0]} · {r[1][:4]}' for r in rows],fontsize=5.6); ax.set_xticks(range(4)); ax.set_xticklabels(['0–6 months','6–12 months','1–2 years','2–3 years'],fontsize=6); ax.xaxis.tick_top()
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0); cb=fig.colorbar(im,ax=ax,fraction=0.03,pad=0.02,ticks=np.log2([0.4,0.5,0.7,1,1.4,2,2.8])); cb.ax.set_yticklabels(['0.4','0.5','0.7','1','1.4','2','2.8']); cb.outline.set_visible(False); cb.set_label('Ratio of interval incidence (drug/SGLT2i)',fontsize=6)
plt.tight_layout(); fig.savefig('sfigs5/SFig22_interval_ratios.png',dpi=300,bbox_inches='tight'); fig.savefig('sfigs5/SFig22_interval_ratios.pdf',bbox_inches='tight'); plt.close(fig)
print('ok')
