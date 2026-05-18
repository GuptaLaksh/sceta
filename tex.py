import matplotlib.pyplot as plt

A = 6  # Want figures to be A6
plt.rc('figure', figsize=[46.82 * .5**(.5 * A), 33.11 * .5**(.5 * A)])
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# There seems to be some problem with LaTex printing. The first plot never prints according to the required dpi, hence here I print a *not-associated-to-this-study* plot.

plt.rcParams['figure.dpi'] = 70 # display 
plt.rcParams['savefig.dpi'] = 300 # when saving figures

fig = plt.figure(figsize=(5,5))

plt.scatter(1, 1, color = 'deeppink', marker = 's', s=10, edgecolors='none')
fig.canvas.draw()
plt.close(fig)