import numpy as np, glob, os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'km')
DAYS_PER_PX=1095/389.0; PX_PER_UNIT=125.5
def load(name):
    out={}
    for line in open(f'{D}/{name}.txt'):
        parts=line.strip().split('#'); nm=parts[0]; cur={}
        for p in parts[1:]:
            tag,pts=p.split('@',1); tag='c1' if tag.startswith('c1') or tag.startswith('135') else 'c2'
            xy=np.array([[float(a) for a in q.split(',')] for q in pts.split()])
            cur[tag]=(xy[:,0]*DAYS_PER_PX, xy[:,1]/PX_PER_UNIT*100)  # days, cumulative %
        out[nm]=cur
    return out
def interval_ratio(cur,cuts=(0,180,365,730,1095)):
    res=[]
    for a,b in zip(cuts[:-1],cuts[1:]):
        f=lambda t,c: np.interp(t,*cur[c])
        d1=f(b,'c1')-f(a,'c1'); d2=f(b,'c2')-f(a,'c2'); res.append((a,b,d1,d2,d1/d2 if d2>0 else np.nan))
    return res
if __name__=='__main__':
    for nm,f in [('Cocaine related disorders','sema_sglt2_b1'),('Suicidal ideations','sema_sglt2_b2'),('Schizophrenia','sema_sglt2_b2')]:
        print(f,nm); 
        for a,b,d1,d2,r in interval_ratio(load(f)[nm]): print(f'  {a}-{b}d: drug {d1:.3f}% comparator {d2:.3f}% ratio {r:.2f}')
