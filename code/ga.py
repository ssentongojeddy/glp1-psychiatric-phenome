import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse
plt.rcParams.update({'font.family':'Inter','font.size':7})
A=pd.read_csv('all6_calibrated.csv')
INK='#1f2328'; MUT='#5f6670'; BLUE='#0072B2'; VERM='#D55E00'; GREEN='#009E73'; SKY='#56B4E9'; ORA='#E69F00'; PUR='#CC79A7'
W,H=200,112
fig=plt.figure(figsize=(7.4,7.4*H/W)); ax=fig.add_axes([0,0,1,1]); ax.axis('off'); ax.set_xlim(0,W); ax.set_ylim(0,H)
def box(x,y,w,h,fc,ec,r=2.2,lw=0.6,z=1):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',fc=fc,ec=ec,lw=lw,zorder=z))
def arrow(p,q,col=MUT,lw=1.0,rad=0.0,z=4,ls='-'):
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>,head_length=2.0,head_width=1.2',mutation_scale=1,lw=lw,color=col,zorder=z,connectionstyle=f'arc3,rad={rad}',shrinkA=0,shrinkB=0,linestyle=ls))
# ---------- title band
box(2,96,W-4,14,'#eaf2fd','#eaf2fd',r=2.5)
ax.text(6,106,'Semaglutide, tirzepatide and the psychiatric phenome',fontsize=10.5,fontweight='bold',color=INK,va='center')
ax.text(6,100.2,'Primary analysis plus 8 secondary target trials in TriNetX  ·  new users  ·  19 psychiatric outcomes over 3 years  ·  calibrated to 6 negative controls',fontsize=5.9,color='#2f4a6b',va='center')
# ---------- left: proposed mechanism (illustrated)
box(2,14,92,79,'white','#d8dee6',r=2.5)
ax.text(6,88.5,'Proposed mechanism',fontsize=7.6,fontweight='bold',color=INK,va='center')
ax.text(6,84.3,'GLP-1 signalling in the mesolimbic dopamine reward pathway (mainly rodent studies)',fontsize=5.4,color=MUT,va='center')
import ga_mech; ga_mech.draw(ax,X0=2,Y0=14)
# ---------- right: findings (data)
box(98,14,100,79,'white','#d8dee6',r=2.5)
ax.text(102,88.5,'Primary analysis, type 2 diabetes',fontsize=7.6,fontweight='bold',color=INK,va='center')
ax.text(102,84.3,'Semaglutide or tirzepatide vs SGLT2 inhibitor, 2022–2025: calibrated HR (95% CI)',fontsize=5.4,color=MUT,va='center')
groups=[('Lower risk',GREEN,[('F14','Cocaine use disorder'),('F15','Other stimulant use disorder'),('F12','Cannabis use disorder'),('F11','Opioid use disorder'),('F17','Nicotine dependence'),('F20','Schizophrenia'),('F31','Bipolar disorder'),('R45.851','Suicidal ideation'),('T14.91','Suicide attempt')]),
        ('No significant association',MUT,[('F32','Major depressive disorder, single episode'),('F33','Major depressive disorder, recurrent'),('F41','Anxiety disorders'),('G47.0','Insomnia')])]
# axis mapping: log HR 0.25..2.5 -> x 140..192
x0,x1=141,193; lo,hi=np.log(0.28),np.log(2.6)
X=lambda v: x0+(np.log(v)-lo)/(hi-lo)*(x1-x0)
y=80.0; step=3.85; rows=[]
for gname,gcol,items in groups:
    ax.text(102,y,gname,fontsize=5.6,fontweight='bold',color=gcol,va='center'); y-=step*0.95
    for code,lab in items:
        rows.append(y); ax.text(104,y,lab,fontsize=5.3,color=INK,va='center')
        for k,(cp,col,dy) in enumerate([('Semaglutide or tirzepatide vs SGLT2i (primary)',INK,0.0)]):
            r=A[(A.comparison==cp)&(A.code==code)].iloc[0]; sig=r.q_cal<0.05
            ax.plot([X(max(r.clo,0.28)),X(min(r.chi,2.6))],[y+dy]*2,color=col,lw=0.8,solid_capstyle='round',zorder=3)
            ax.text(x1+0.5,y,f'{r.cHR:.2f}',fontsize=4.9,va='center',color=MUT)
            ax.plot(X(r.cHR),y+dy,'o',ms=2.6,color=col,mfc=col if sig else 'white',mew=0.7,zorder=4)
        y-=step
    y-=step*0.35
ytop,ybot=81.5,y+step*0.6
ax.plot([X(1)]*2,[ybot,ytop],color='#3a4450',lw=0.6,ls=(0,(3,2)),zorder=2)
for v in (0.3,0.5,1,2):
    ax.plot([X(v)]*2,[ybot,ybot-1],color='#3a4450',lw=0.6); ax.text(X(v),ybot-3,f'{v:g}',fontsize=5,ha='center',va='center',color=MUT)
ax.plot([x0,x1],[ybot,ybot],color='#3a4450',lw=0.6)
# legend
ly=17.2
for k,(lab,col) in enumerate([('255,685–275,248 matched pairs',INK)]):
    xx=104+k*28; ax.plot(xx,ly,'o',ms=3,color=col); ax.text(xx+2.2,ly,lab,fontsize=5.2,va='center',color=INK)
ax.plot(160,ly,'o',ms=3,color=MUT,mfc='white',mew=0.8); ax.text(162.2,ly,'open: FDR q ≥ 0.05',fontsize=5.2,va='center',color=INK)
# ---------- bottom takeaway
box(2,2,W-4,9.5,'#fdf1e8','#fdf1e8',r=2.5)
ax.text(W/2,8.4,'Findings replicated for each drug separately, against DPP-4 inhibitors and untreated patients, and partly in obesity; tirzepatide and semaglutide did not differ significantly.',fontsize=5.7,color=INK,ha='center',va='center')
ax.text(W/2,4.6,'Observational associations: randomized trials in stimulant use disorder, early psychosis and suicide prevention are warranted.',fontsize=5.7,color='#8a3b12',ha='center',va='center',fontweight='bold')
fig.savefig('figs/Graphical_abstract.png',dpi=400); fig.savefig('figs/Graphical_abstract.pdf')
print('ok')
