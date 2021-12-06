"""Plotting script the net present value of the six different sceanrios."""
import pyam
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mlp
import matplotlib.ticker as tkr
import numpy as np

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rc('legend', fontsize=7)

def draw_brace(ax, xspan, text):
    """Draws an annotated brace on the axes."""
    xmin, xmax = xspan
    xspan = xmax - xmin
    ax_xmin, ax_xmax = ax.get_xlim()
    xax_span = ax_xmax - ax_xmin
    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    resolution = int(xspan/xax_span*100)*2+1 # guaranteed uneven
    beta = 300./xax_span # the higher this is, the smaller the radius

    x = np.linspace(xmin, xmax, resolution)
    x_half = x[:resolution//2+1]
    y_half_brace = (1/(1.+np.exp(-beta*(x_half-x_half[0])))
                    + 1/(1.+np.exp(-beta*(x_half-x_half[-1]))))
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    y = ymin + (.05*y - .01)*yspan # adjust vertical position

    ax.autoscale(False)
    ax.plot(x, y, lw=0.75, color="black")

    ax.text((xmax+xmin)/2., ymin+.09*yspan, text, ha='center', va='bottom',
            fontsize=7, color="black",
            bbox=dict(facecolor='none', edgecolor='black', linewidth=0.,
                                 boxstyle="round,pad=0.3"))


_data_folder = Path("../../../../optimization model/result")
data = pyam.IamDataFrame(_data_folder / "scenario-results.xlsx")

fig, ax = plt.subplots()

cmap = plt.cm.jet  # define the colormap
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# force the first color entry to be grey
cmaplist[0] = (.5, .5, .5, 1.0)

# create the new map
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', ["#9B72AA", "#77ACF1", "#FFB319"], cmap.N)

data.plot.bar(ax=ax, x="scenario", stacked=True,
              title="Governance's total financial support in EUR",
              cmap=cmap,
              bars_order=None)

ax.text(x=3, y=-20000, s='$\it{Infeasible}$', rotation=90, va="top",
        ha="center")

ax.text(x=4, y=-20000, s='$\it{Infeasible}$', rotation=90, va="top",
        ha="center")

ax.set_ylabel("")
ax.set_xlabel("")

c_edge = "#161616"
leg = ax.legend(loc='lower left', framealpha=1, handlelength=1,
                handletextpad=1, borderpad=0.25, columnspacing=1,
                edgecolor=c_edge, frameon=True,
                bbox_to_anchor=(0.0125, 0.175))
leg.get_frame().set_linewidth(0.25)

group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
plt.gca().yaxis.set_major_formatter(group_thousands)

ax.set_xticklabels(labels=["DT (DH)",
                           "GD (DH)",
                           "LD (DH)",
                           "SC (HP)",
                           "GD (HP)",
                           "LD (HP)"])

ax.set_ylim([-550000, 0])
draw_brace(ax, (0, 2), 'District heating')
draw_brace(ax, (3, 5), 'Heat pump')

plt.xticks(rotation=45)
ax.minorticks_off()

# plt.tight_layout()

fig.savefig("net_present_value.eps", format="eps")
fig.savefig("net_present_value.png", dpi=900)
