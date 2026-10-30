import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib import font_manager as fm
plt.rcParams.update({'font.family':'Inter','font.size':7})
W,H=180,174
fig=plt.figure(figsize=(7.4,7.4*H/W)); ax=fig.add_axes([0,0,1,1]); ax.axis('off'); ax.set_xlim(0,W); ax.set_ylim(0,H)
INK='#1f2328'; MUT='#5f6670'
def card(x,y,w,h,col,tint,title,body,big=None,num=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=2.4',fc=tint,ec=col,lw=0.5,alpha=1,zorder=2))
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=2.4',fc='none',ec='white',lw=0,zorder=2))
    tx=x+4
    if num is not None:
        ax.add_patch(Circle((x+6.5,y+h-5.5),2.8,fc=col,ec='none',zorder=4)); ax.text(x+6.5,y+h-5.5,str(num),ha='center',va='center',color='white',fontsize=6.2,fontweight='bold',zorder=5); tx=x+11.5
    ax.text(tx,y+h-5.5,title,ha='left',va='center',fontsize=6.6 if w>40 else 5.6,fontweight='bold',color=INK,zorder=5)
    if big:
        ax.text(x+4,y+h-14,big,ha='left',va='center',fontsize=12 if w>40 else 10.5,fontweight='bold',color=col,zorder=5)
        ax.text(x+4,y+4.2,body,ha='left',va='center',fontsize=5.6 if w>40 else 4.8,color=MUT,zorder=5)
    else:
        ax.text(x+4,y+h-10.5,body,ha='left',va='top',fontsize=5.7,color=MUT,zorder=5,linespacing=1.45)
def harrow(x1,x2,y,col='#9aa3ad'):
    ax.add_patch(FancyArrowPatch((x1,y),(x2,y),arrowstyle='-|>,head_length=2.2,head_width=1.4',mutation_scale=1,lw=1.1,color=col,zorder=6,shrinkA=0,shrinkB=0))
def varrow(x,y1,y2,col='#9aa3ad'):
    ax.add_patch(FancyArrowPatch((x,y1),(x,y2),arrowstyle='-|>,head_length=2.2,head_width=1.4',mutation_scale=1,lw=1.1,color=col,zorder=6,shrinkA=0,shrinkB=0))
def section(y,letter,txt):
    ax.text(2,y,letter,fontsize=9,fontweight='bold',color=INK,va='center'); ax.text(7.5,y,txt,fontsize=8,fontweight='bold',color=INK,va='center')
cw,gap=52,10; xs=[2,2+cw+gap,2+2*(cw+gap)]
BL,BLt='#2a78d6','#eaf2fd'; VI,VIt='#6250d6','#efedfc'; OR,ORt='#e0602c','#fdeee6'; GR,GRt='#1baf7a','#e7f7f0'

section(169,'a','Data source and design')
yA,hA=140,23
card(xs[0],yA,cw,hA,GR,GRt,'Data source','TriNetX Global Collaborative Network\nDe-identified electronic health records\n159 healthcare organizations',num=1)
card(xs[1],yA,cw,hA,GR,GRt,'New users','First prescription, Jan 2018 – Oct 2025\nPrimary and head-to-head: from 13 May 2022\nNo prior GLP-1 drug or tirzepatide',num=2)
card(xs[2],yA,cw,hA,GR,GRt,'Propensity matching','1:1 nearest neighbour, calliper 0.1 SD\n43 terms: demographics, diagnoses,\ndrugs, BMI and HbA1c categories',num=3)
for i in range(2): harrow(xs[i]+cw+2.5,xs[i+1]-2.5,yA+hA/2)
varrow(W/2,yA-2.5,yA-7)
section(129,'b','Primary analysis and eight secondary target trials')
PK,PKt='#1f2328','#eef0f2'
ax.text(xs[0],123,'PRIMARY ANALYSIS  ·  TYPE 2 DIABETES  ·  NEW USERS MAY 2022 – OCT 2025',fontsize=5.4,color=PK,fontweight='bold',va='center')
card(2,101,W-4,19,PK,PKt,'Semaglutide or tirzepatide vs SGLT2 inhibitor','')
ax.text(6,107.5,'255,685–275,248',ha='left',va='center',fontsize=12,fontweight='bold',color=PK,zorder=5)
ax.text(6,103.6,'matched pairs',ha='left',va='center',fontsize=5.6,color=MUT,zorder=5)
ax.text(70,108.3,'485,984 semaglutide or tirzepatide and 587,364 SGLT2 inhibitor new users',ha='left',va='center',fontsize=5.7,color=MUT,zorder=5)
ax.text(70,104.3,'19 psychiatric outcomes, one FDR family; drug-specific and other comparisons secondary',ha='left',va='center',fontsize=5.7,color=MUT,zorder=5)
ax.text(xs[0],96,'SECONDARY  ·  TYPE 2 DIABETES  ·  DRUG-SPECIFIC ACTIVE COMPARATORS, 2018–2025',fontsize=5.4,color=BL,fontweight='bold',va='center')
for x,(t,n) in zip(xs,[('Semaglutide vs SGLT2 inhibitor','374,496'),('Tirzepatide vs SGLT2 inhibitor','137,440'),('Semaglutide vs DPP-4 inhibitor','275,553')]):
    card(x,71,cw,22,BL,BLt,t,'matched pairs',big=n)
ax.text(xs[0],67,'SECONDARY  ·  HEAD-TO-HEAD AND UNTREATED COMPARATORS',fontsize=5.4,color=VI,fontweight='bold',va='center')
cw4=(W-4-4*3)/5; xs4=[2+i*(cw4+3) for i in range(5)]
for x,(t,n,b) in zip(xs4,[('Tirzepatide vs semaglutide','142,681','pairs · 2022–2025'),('Semaglutide vs no drug','295,147','pairs · T2D, obesity, metformin'),('Tirzepatide vs no drug','126,768','pairs · T2D, obesity, metformin'),('Semaglutide vs no drug','185,404','pairs · obesity + OSA, no T2D'),('Tirzepatide vs no drug','135,389','pairs · obesity + OSA, no T2D')]):
    card(x,42,cw4,22,VI,VIt,t,b,big=n)
varrow(W/2,39.5,35)
section(31,'c','Outcomes, follow-up and analysis')
yC,hC=2,25
card(xs[0],yC,cw,hC,OR,ORt,'25 outcomes','19 psychiatric diagnoses in 5 domains:\nsubstance use, psychosis and bipolar,\nsuicidality, mood and anxiety, eating\nand impulse; 6 negative controls',num=4)
card(xs[1],yC,cw,hC,OR,ORt,'Follow-up','New diagnoses on days 1–1,095\nPrior cases excluded per outcome\nCox proportional hazards model\nCensoring at last record',num=5)
card(xs[2],yC,cw,hC,OR,ORt,'Bias control','Empirical calibration to the\nnegative-control null distribution\nBenjamini–Hochberg FDR\nE-values for unmeasured confounding',num=6)
for i in range(2): harrow(xs[i]+cw+2.5,xs[i+1]-2.5,yC+hC/2)
fig.savefig('figs/Fig1_design.png',dpi=300); fig.savefig('figs/Fig1_design.pdf')
