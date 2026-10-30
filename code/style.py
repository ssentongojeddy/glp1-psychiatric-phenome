import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
plt.rcParams.update({'font.family':'Inter','font.size':6.5,'axes.titlesize':7,'axes.labelsize':6.5,'xtick.labelsize':6,'ytick.labelsize':6,
 'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#3a4450','axes.linewidth':0.6,'xtick.major.width':0.6,'ytick.major.width':0.6,
 'xtick.color':'#3a4450','ytick.color':'#3a4450','axes.labelcolor':'#1f2328','legend.fontsize':6,'pdf.fonttype':42})
COMPS=['Semaglutide vs SGLT2i','Tirzepatide vs SGLT2i','Semaglutide vs DPP-4i','Tirzepatide vs semaglutide','Semaglutide vs no drug (T2D)','Tirzepatide vs no drug (T2D)','Semaglutide vs no drug (obesity+OSA)','Tirzepatide vs no drug (obesity+OSA)']
SHORT=['Sema vs SGLT2i','Tirz vs SGLT2i','Sema vs DPP-4i','Tirz vs sema','Sema vs no drug\n(T2D)','Tirz vs no drug\n(T2D)','Sema vs no drug\n(obesity)','Tirz vs no drug\n(obesity)']
C=['#0072B2','#D55E00','#009E73','#CC79A7','#56B4E9','#E69F00','#999999','#882255']   # Okabe-Ito colour-blind-safe palette
PRIM='Semaglutide or tirzepatide vs SGLT2i (primary)'
COMPS.append(PRIM); SHORT.append('Sema or tirz\nvs SGLT2i (primary)'); C.append('#1f2328')
CM=LinearSegmentedColormap.from_list('cb_div',['#053061','#2166ac','#4393c3','#92c5de','#f7f7f7','#fdb863','#e08214','#b35806','#7f3b08'])  # blue-orange, colour-blind safe
DOM=[('Substance use',['F10','F11','F12','F14','F15','F17']),('Psychosis and bipolar',['F20','F31']),('Suicidality',['R45.851','T14.91']),('Depression, anxiety, stress, sleep',['F32','F33','F41','F43','G47.0']),('Eating, impulse, compulsive',['F50.2','F50.0','F63.0','F42'])]
NC=['L60.0','H60','J30','D22','S52','H52']
NAME={'F10':'Alcohol use disorder','F11':'Opioid use disorder','F12':'Cannabis use disorder','F14':'Cocaine use disorder','F15':'Other stimulant use disorder','F17':'Nicotine dependence','F20':'Schizophrenia','F31':'Bipolar disorder','R45.851':'Suicidal ideation','T14.91':'Suicide attempt','F32':'Major depressive disorder, single episode','F33':'Major depressive disorder, recurrent','F41':'Anxiety disorders','F43':'Stress-related and adjustment disorders','G47.0':'Insomnia','F50.2':'Bulimia nervosa','F50.0':'Anorexia nervosa','F63.0':'Pathological gambling','F42':'Obsessive-compulsive disorder','L60.0':'Ingrowing nail','H60':'Otitis externa','J30':'Allergic rhinitis','D22':'Melanocytic naevi','S52':'Forearm fracture','H52':'Refraction disorders'}
A=pd.read_csv('all6_calibrated.csv'); B=pd.read_csv('baseline_all.csv')
def row(cp,c):
    d=A[(A.comparison==cp)&(A.code==c)]; return d.iloc[0] if len(d) else None
_PANELS=[]
def panel(ax,l,dx=None,dy=1.02): _PANELS.append((ax,l,dy))
def finalize(fig):
    fig.canvas.draw(); r=fig.canvas.get_renderer(); W,H=fig.get_size_inches()*fig.dpi
    for ax,l,dy in [p for p in _PANELS if p[0].figure is fig]:
        tb=ax.get_tightbbox(r); pos=ax.get_position()
        fig.text(max(tb.x0/W-0.005,0.003),pos.y1+(dy-1)*pos.height+0.012,l,fontsize=9,fontweight='bold',va='bottom',ha='left')
def logx(ax,ticks):
    ax.set_xscale('log'); ax.set_xticks(ticks); ax.set_xticklabels([f'{t:g}' for t in ticks]); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
