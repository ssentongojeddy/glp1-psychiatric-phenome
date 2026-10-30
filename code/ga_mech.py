# Illustrated mechanism panel for the graphical abstract (sagittal brain, neurons, NAc synapse inset)
import numpy as np
from scipy.interpolate import splprep, splev
from matplotlib.patches import Polygon, Circle, Ellipse, PathPatch, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe

def smooth(pts, closed=True, n=400):
    p = np.array(pts, float)
    if closed: p = np.vstack([p, p[:1]])
    k = min(3, len(p) - 1)
    tck, _ = splprep([p[:, 0], p[:, 1]], s=0, per=closed, k=k)
    x, y = splev(np.linspace(0, 1, n), tck)
    return np.c_[x, y]

def curve(ax, pts, col, lw=1.0, alpha=1, z=5, ls='-', n=200):
    c = smooth(pts, closed=False, n=n)
    ax.plot(c[:, 0], c[:, 1], color=col, lw=lw, alpha=alpha, zorder=z, solid_capstyle='round', ls=ls)
    return c

def arrowhead(ax, c, col, size=1.3, z=6, alpha=1):
    p, q = c[-6], c[-1]; d = (q - p) / np.linalg.norm(q - p); nrm = np.array([-d[1], d[0]])
    tri = [q + d * 0.2, q - d * size + nrm * size * 0.55, q - d * size - nrm * size * 0.55]
    ax.add_patch(Polygon(tri, closed=True, fc=col, ec='none', zorder=z, alpha=alpha))

def neuron(ax, soma, col, tint, r=1.5, dend_seed=0, z=7):
    rng = np.random.default_rng(dend_seed)
    for k in range(5):
        a = rng.uniform(0, 2 * np.pi); L = rng.uniform(2.2, 3.6)
        p0 = np.array(soma) + r * 0.8 * np.array([np.cos(a), np.sin(a)])
        p1 = p0 + L * 0.55 * np.array([np.cos(a + 0.3), np.sin(a + 0.3)])
        p2 = p0 + L * np.array([np.cos(a - 0.15), np.sin(a - 0.15)])
        curve(ax, [p0, p1, p2], col, lw=0.7, z=z - 1)
        for s in (-1, 1):
            b = p1 + 0.9 * np.array([np.cos(a + s * 0.9), np.sin(a + s * 0.9)])
            ax.plot([p1[0], b[0]], [p1[1], b[1]], color=col, lw=0.5, zorder=z - 1, solid_capstyle='round')
    ax.add_patch(Circle(soma, r, fc=tint, ec=col, lw=0.9, zorder=z))
    ax.add_patch(Circle(soma, r * 0.42, fc=col, ec='none', zorder=z + 1, alpha=0.85))

def terminals(ax, end, col, ang, z=7):
    for da in (-0.7, 0, 0.7):
        a = ang + da; q = np.array(end) + 1.5 * np.array([np.cos(a), np.sin(a)])
        ax.plot([end[0], q[0]], [end[1], q[1]], color=col, lw=0.6, zorder=z)
        ax.add_patch(Circle(q, 0.42, fc=col, ec='white', lw=0.3, zorder=z + 1))

def receptor(ax, xy, ang=90, s=1.0, col='#E69F00', z=9):
    a = np.deg2rad(ang); d = np.array([np.cos(a), np.sin(a)]); n = np.array([-d[1], d[0]])
    base = np.array(xy); top = base + d * 0.9 * s
    ax.plot(*zip(base, top), color=col, lw=1.0 * s, zorder=z, solid_capstyle='round')
    for sg in (-1, 1):
        t = top + d * 0.55 * s + n * sg * 0.45 * s
        ax.plot(*zip(top, t), color=col, lw=1.0 * s, zorder=z, solid_capstyle='round')

def peptide(ax, start, ang, col='#E69F00', nb=6, r=0.42, z=10):
    a = np.deg2rad(ang)
    for i in range(nb):
        off = 0.35 * np.sin(i * 1.3)
        p = np.array(start) + i * 0.78 * np.array([np.cos(a), np.sin(a)]) + off * np.array([-np.sin(a), np.cos(a)])
        ax.add_patch(Circle(p, r, fc=col if i % 2 == 0 else '#f6c26b', ec='white', lw=0.25, zorder=z))

def draw(ax, X0=2, Y0=14, INK='#1f2328', MUT='#5f6670'):
    BLUE = '#0072B2'; GREEN = '#009E73'; ORA = '#E69F00'; PUR = '#CC79A7'; VERM = '#D55E00'
    ox, oy = X0 + 2, Y0 + 24.5
    T = lambda x, y: (ox + x, oy + y)
    # ---- brain (sagittal, facing left)
    cer = smooth([T(2.5, 22), T(4, 31), T(10, 38), T(20, 42.5), T(32, 43), T(43, 40), T(50.5, 34), T(54, 26), T(53, 19.5), T(49.5, 15.5),
                  T(43, 14.5), T(37, 13.5), T(32, 10.5), T(24, 7.5), T(16, 8), T(11, 11), T(8.5, 15), T(4.5, 17.5)])
    ax.add_patch(Polygon(cer, closed=True, fc='#f7eff1', ec='#b99aa5', lw=0.9, zorder=2))
    # sulci
    for pts in [[T(12, 36), T(17, 33), T(16, 28)], [T(24, 41), T(26, 35), T(30, 31)], [T(36, 41.5), T(36, 35), T(40, 30)],
                [T(45, 37), T(44, 31), T(48, 26)], [T(8, 27), T(13, 24), T(19, 25)], [T(28, 26), T(34, 24), T(40, 25.5)],
                [T(20, 14), T(27, 16), T(34, 15.5)], [T(46, 22), T(49, 20), T(51, 22.5)]]:
        curve(ax, pts, '#d9c3cb', lw=0.6, z=3)
    # corpus callosum hint
    curve(ax, [T(14, 24), T(24, 31), T(36, 31), T(44, 25)], '#e5d3d9', lw=2.2, z=3)
    # cerebellum
    cb = smooth([T(42.5, 14), T(48, 15.5), T(54, 13.5), T(56.5, 9), T(54, 4.5), T(47.5, 3.5), T(42.5, 6.5)])
    ax.add_patch(Polygon(cb, closed=True, fc='#f1e6ea', ec='#b99aa5', lw=0.8, zorder=2))
    for k in range(4):
        curve(ax, [T(44 + k * 0.4, 12.5 - k * 2.2), T(49, 13 - k * 2.4), T(54.5 - k * 0.3, 11.5 - k * 2.2)], '#d9c3cb', lw=0.5, z=3)
    # brainstem
    bs = smooth([T(36, 15), T(41.5, 14.5), T(43, 9), T(42.5, 0), T(39.5, -5), T(36.5, -4.5), T(37.5, 2), T(35.5, 9)])
    ax.add_patch(Polygon(bs, closed=True, fc='#efe3e8', ec='#b99aa5', lw=0.8, zorder=2.5))
    # ---- region glows
    REG = {'PFC': T(8.5, 30), 'NAc': T(16.5, 17.5), 'VTA': T(36.5, 15.5), 'NTS': T(40.0, -0.5)}
    for k, (xy, c) in {'NAc': (REG['NAc'], BLUE), 'VTA': (REG['VTA'], BLUE), 'NTS': (REG['NTS'], GREEN)}.items():
        for rr, al in [(3.6, 0.10), (2.6, 0.16), (1.7, 0.22)]:
            ax.add_patch(Ellipse(xy, rr * 2.2, rr * 1.6, fc=c, ec='none', alpha=al, zorder=4))
    ax.add_patch(Ellipse(REG['PFC'], 6, 4.5, fc=BLUE, ec='none', alpha=0.07, zorder=4))
    # ---- NTS GLP-1 neuron -> VTA and NAc
    neuron(ax, REG['NTS'], GREEN, '#d9f0e7', r=1.2, dend_seed=3)
    c = curve(ax, [REG['NTS'], T(38.5, 5), T(37, 10), T(36.5, 13.0)], GREEN, lw=0.9, z=6); arrowhead(ax, c, GREEN, 1.1)
    c = curve(ax, [REG['NTS'], T(36.5, 3), T(28, 8), T(19.5, 14.8)], GREEN, lw=0.9, z=6, alpha=0.85); arrowhead(ax, c, GREEN, 1.1, alpha=0.85)
    # ---- VTA dopamine neuron -> NAc (mesolimbic) and PFC (mesocortical)
    neuron(ax, REG['VTA'], BLUE, '#dcebf6', r=1.5, dend_seed=7)
    c = curve(ax, [REG['VTA'], T(30, 21.5), T(23, 21), T(18.6, 18.6)], BLUE, lw=1.4, z=6)
    terminals(ax, c[-1], BLUE, np.arctan2(*(c[-1] - c[-8])[::-1]))
    c2 = curve(ax, [REG['VTA'], T(30, 25), T(20, 31.5), T(11, 30.5)], BLUE, lw=0.8, z=6, alpha=0.45)
    terminals(ax, c2[-1], '#7fb3d6', np.arctan2(*(c2[-1] - c2[-8])[::-1]))
    # receptors on regions
    for xy, ang in [(T(15.0, 15.5), 250), (T(35.0, 13.5), 250), (T(41.6, -2.2), 300)]:
        receptor(ax, xy, ang, 0.8)
    # ---- drug entering from circulation
    peptide(ax, T(-1.5, 3.5), 25); peptide(ax, T(2, 0), 18, nb=5)
    ax.text(*T(-1.5, -1.8), 'Semaglutide · tirzepatide', fontsize=5.6, fontweight='bold', color='#8a4b00', va='center', zorder=11)
    c = curve(ax, [T(6.5, 6.5), T(11, 10), T(14.4, 14.3)], ORA, lw=1.0, z=8); arrowhead(ax, c, ORA, 1.2)
    c = curve(ax, [T(7.5, 3), T(20, 4.5), T(33.6, 12.3)], ORA, lw=1.0, z=8, alpha=0.9); arrowhead(ax, c, ORA, 1.2, alpha=0.9)
    # ---- labels with leaders
    def lab(txt, xy, txy, col, ha='left', sub=None):
        ax.annotate('', xy=xy, xytext=txy, arrowprops=dict(arrowstyle='-', lw=0.4, color='#8995a1', shrinkA=0, shrinkB=1.5), zorder=12)
        ax.text(*txy, txt, fontsize=5.6, fontweight='bold', color=col, ha=ha, va='center', zorder=12,
                path_effects=[pe.withStroke(linewidth=2, foreground='white')])
        if sub: ax.text(txy[0], txy[1] - 2.6, sub, fontsize=4.7, color=MUT, ha=ha, va='center', zorder=12, path_effects=[pe.withStroke(linewidth=2, foreground='white')])
    lab('Prefrontal cortex', T(8, 31.5), T(-1, 39.5), '#3a6f99')
    lab('Nucleus accumbens', T(15.5, 19.5), T(2, 26.0), BLUE, sub='reward valuation')
    lab('VTA', T(38.5, 16.8), T(44.5, 22.5), BLUE, sub='dopamine neurons')
    lab('NTS', T(41.5, 0.5), T(46.5, -3.5), GREEN, sub='GLP-1 neurons')
    # pathway tag
    ax.text(*T(26.5, 17.6), 'dopamine', fontsize=4.8, color=BLUE, style='italic', ha='center', rotation=0, zorder=12,
            path_effects=[pe.withStroke(linewidth=1.8, foreground='#f7eff1')])
    # ---- synapse inset
    cx, cy, R = X0 + 76.5, Y0 + 49.0, 12.5
    nac = np.array(REG['NAc'])
    for s in (1, -1):
        ang = np.arctan2(cy - nac[1], cx - nac[0]) + s * np.pi / 2
        p = nac + 3.0 * np.array([np.cos(ang), np.sin(ang)]); q = np.array([cx, cy]) + R * np.array([np.cos(ang), np.sin(ang)])
        ax.plot([p[0], q[0]], [p[1], q[1]], color='#b8c4d0', lw=0.5, zorder=1.5, ls=(0, (2, 1.5)))
    ax.add_patch(Circle(nac, 3.0, fc='none', ec='#8fa3b6', lw=0.6, zorder=5, ls=(0, (2, 1.5))))
    ax.add_patch(Circle((cx, cy), R, fc='white', ec='#8fa3b6', lw=0.9, zorder=13))
    clip = Circle((cx, cy), R - 0.15, transform=ax.transData)
    # presynaptic terminal
    pre = smooth([(cx - 9, cy + 13), (cx - 7.5, cy + 4), (cx - 3, cy + 0.8), (cx + 3, cy + 0.8), (cx + 7.5, cy + 4), (cx + 9, cy + 13)], closed=False)
    pre = np.vstack([pre, [(cx + 9, cy + 14), (cx - 9, cy + 14)]])
    P1 = Polygon(pre, closed=True, fc='#dcebf6', ec=BLUE, lw=0.9, zorder=14); ax.add_patch(P1); P1.set_clip_path(clip)
    rng = np.random.default_rng(2)
    pts = []
    while len(pts) < 10:
        vx, vy = cx + rng.uniform(-5.5, 5.5), cy + rng.uniform(3.8, 9.2)
        if any((vx - px) ** 2 + (vy - py) ** 2 < 2.1 ** 2 for px, py in pts): continue
        pts.append((vx, vy))
    for vx, vy in pts:
        v = Circle((vx, vy), 0.85, fc='white', ec=BLUE, lw=0.5, zorder=15); ax.add_patch(v)
        for _ in range(3):
            d = Circle((vx + rng.uniform(-0.4, 0.4), vy + rng.uniform(-0.4, 0.4)), 0.13, fc=BLUE, ec='none', zorder=16); ax.add_patch(d)
    # GLP-1R on terminal with drug bound
    for gx in (cx - 6.2, cx + 6.4):
        gy = cy + 3.2 if gx < cx else cy + 3.4
        ang = 215 if gx < cx else 325
        receptor(ax, (gx, gy), ang, 1.0, z=17)
        a = np.deg2rad(ang); tip = np.array([gx, gy]) + 1.9 * np.array([np.cos(a), np.sin(a)])
        peptide(ax, tip + np.array([-0.3, -0.2]), ang - 90 if gx < cx else ang + 90, nb=4, r=0.36, z=18)
    # released dopamine (sparse) in cleft
    for (dx, dy) in [(-1.8, -0.6), (0.6, -1.2), (2.1, -0.4), (-0.4, -2.0)]:
        ax.add_patch(Circle((cx + dx, cy + dy), 0.22, fc=BLUE, ec='none', zorder=16))
    # postsynaptic MSN
    post = smooth([(cx - 11, cy - 4.5), (cx - 5, cy - 3.2), (cx, cy - 3.0), (cx + 5, cy - 3.2), (cx + 11, cy - 4.5)], closed=False)
    post = np.vstack([post, [(cx + 11, cy - 14), (cx - 11, cy - 14)]])
    P2 = Polygon(post, closed=True, fc='#efe3ee', ec='#8e5c86', lw=0.9, zorder=14); ax.add_patch(P2); P2.set_clip_path(clip)
    for k, dx in enumerate((-3.6, -1.2, 1.2, 3.6)):
        ax.add_patch(Polygon([(cx + dx - 0.35, cy - 3.1), (cx + dx + 0.35, cy - 3.1), (cx + dx + 0.35, cy - 2.2), (cx + dx - 0.35, cy - 2.2)], closed=True, fc='#8e5c86', ec='none', zorder=16))
    # inset text
    ax.text(cx, cy + R + 2.0, 'Nucleus accumbens synapse', fontsize=5.6, fontweight='bold', color=INK, ha='center', va='center', zorder=20)
    ax.text(cx, cy + 10.6, 'dopamine terminal', fontsize=4.6, color=BLUE, ha='center', va='center', zorder=20, path_effects=[pe.withStroke(linewidth=1.6, foreground='#dcebf6')])
    ax.text(cx, cy - 8.2, 'medium spiny neuron', fontsize=4.6, color='#7a4a72', ha='center', va='center', zorder=20, path_effects=[pe.withStroke(linewidth=1.6, foreground='#efe3ee')])
    ax.text(cx, cy - 10.5, 'dopamine receptors', fontsize=4.2, color='#7a4a72', ha='center', va='center', zorder=20, path_effects=[pe.withStroke(linewidth=1.6, foreground='#efe3ee')])
    ax.annotate('GLP-1R +\nagonist', xy=(cx - 7.6, cy + 1.8), xytext=(cx - R - 3.6, cy + 6.0), fontsize=4.6, color='#8a4b00', ha='center', va='center', zorder=21,
                arrowprops=dict(arrowstyle='-', lw=0.4, color='#8995a1', shrinkA=1, shrinkB=0))
    ax.text(cx, cy - R - 3.4, 'agonist binds GLP-1R on the terminal:\nless dopamine is released', fontsize=4.8, color=INK, ha='center', va='center', zorder=21)
    # ---- consequence flow (arrows, no boxes)
    fy = Y0 + 12.5
    steps = [('GLP-1R activation', ORA), ('↓ drug-evoked\ndopamine surge', BLUE), ('↓ reward and\ncraving', BLUE), ('↓ substance use\ndisorders', GREEN)]
    xs = [X0 + 10, X0 + 33, X0 + 56, X0 + 80]
    for i, ((t, col), x) in enumerate(zip(steps, xs)):
        ax.text(x, fy, t, fontsize=5.4, fontweight='bold', color=col, ha='center', va='center', linespacing=1.2)
        if i < len(xs) - 1:
            a = FancyArrowPatch((x + 9.5, fy), (xs[i + 1] - 9.5, fy), arrowstyle='-|>,head_length=1.8,head_width=1.1', mutation_scale=1, lw=1.0, color='#8995a1', shrinkA=0, shrinkB=0)
            ax.add_patch(a)
    hy = Y0 + 4.0
    for (xa, xt, t) in [(X0 + 33, X0 + 26, 'psychosis and bipolar disorder?'), (X0 + 56, X0 + 62, 'suicidality?')]:
        a = FancyArrowPatch((xa, fy - 3.6), (xt + (6 if xt < xa else 0), hy + 1.7), arrowstyle='-|>,head_length=1.5,head_width=0.9', mutation_scale=1, lw=0.8, color=PUR, linestyle=(0, (3, 2)), shrinkA=0, shrinkB=0)
        ax.add_patch(a)
        ax.text(xt, hy, t, fontsize=5.0, color='#9b4f86', ha='left', va='center', style='italic')
    ax.text(X0 + 4, hy, 'Hypothesised:', fontsize=5.0, color=MUT, ha='left', va='center')
