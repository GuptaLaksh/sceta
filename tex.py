import matplotlib.pyplot as plt
 
A = 6  # Want figures to be A6
plt.rc('figure', figsize=[46.82 * .5**(.5 * A), 33.11 * .5**(.5 * A)])
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
 
# Custom LaTeX preamble
latex_preamble = r"""
\usepackage{mathptmx}
\DeclareMathAlphabet{\mathcal}{OMS}{cmsy}{m}{n}
\usepackage[scaled=1]{helvet}
\usepackage{courier}
\usepackage{microtype}
\usepackage{sectsty}
\allsectionsfont{\scshape}
\linespread{1.0}
"""

plt.rcParams['text.latex.preamble'] = latex_preamble 
plt.rcParams['figure.dpi']=100
plt.rcParams['savefig.dpi'] = 300 # when saving figures
plt.tight_layout()
fig = plt.figure(figsize=(5,5))

plt.scatter(1, 1, color = 'deeppink', marker = 's', s=10, edgecolors='none')
fig.canvas.draw()
plt.close(fig)