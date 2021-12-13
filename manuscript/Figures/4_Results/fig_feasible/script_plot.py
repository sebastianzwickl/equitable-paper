"""Plotting script the net present value of the six different sceanrios."""
import pyam
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mlp
import matplotlib.ticker as tkr
import matplotlib.patches as mpatches

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6
plt.rc('legend', fontsize=6)

box_color= "#444444"

data = pyam.IamDataFrame("mappe2.xlsx")

fig = plt.figure()
ax = fig.add_subplot(111)
c_edge = "#334257"


cmap = plt.cm.jet  # define the colormap
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# force the first color entry to be grey
cmaplist[0] = (.5, .5, .5, 1.0)

_c = ["#2F86A6", "#81B214", "#FF8303"]
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c, cmap.N)

data.plot(ax=ax, title=None, legend=False,
          marker="|", markersize=2, cmap=cmap, color="scenario")


ax.plot([2032, 2032], [30000, 93533*0.985], linestyle="solid",
        color=box_color, linewidth=0.2)
ax.plot([2030, 2032], [30000, 30000], linestyle="solid",
        color=box_color, linewidth=0.2, zorder=-1)
ax.text(x=2025.25, y=30000,
        s="Feasibility limit $(s_l=70\%)$\nObj. value = 93.5kEUR",
        fontsize=6, va="center", ha="left", color=box_color,
        multialignment="left", linespacing=1.5,
        bbox=dict(facecolor='white', edgecolor=box_color, linewidth=0.25,
                              boxstyle="round,pad=0.3"))


ax.plot([2031, 2031], [70000, 89877*0.985], linestyle="solid",
        color=box_color, linewidth=0.2)
ax.plot([2030, 2031], [70000, 70000], linestyle="solid",
        color=box_color, linewidth=0.2, zorder=-1)
ax.text(x=2029.5, y=173000,
        s="Feasibility limit $(s_l=100\%)$\nObj. value = 99.4kEUR",
        fontsize=6, va="center", ha="left", color=box_color,
        multialignment="left", linespacing=1.5,
        bbox=dict(facecolor='white', edgecolor=box_color, linewidth=0.25,
                              boxstyle="round,pad=0.3"))


ax.plot([2035, 2035], [173000, 99419*0.985], linestyle="solid",
        color=box_color, linewidth=0.2)
ax.plot([2030.5, 2035], [173000, 173000], linestyle="solid",
        color=box_color, linewidth=0.2, zorder=-1)



ax.text(x=2025.25, y=70000,
        s="Feasibility limit $(s_l=60\%)$\nObj. value = 89.8kEUR",
        fontsize=6, va="center", ha="left", color=box_color,
        multialignment="left", linespacing=1.5,
        bbox=dict(facecolor='white', edgecolor=box_color, linewidth=0.25,
                              boxstyle="round,pad=0.3"))






# ax.plot([2031, 2031], [0, 89877], linestyle="dashed", color="#99A799")
ax.set_xticks([2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035])
ax.set_xticklabels(labels=["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"])
ax.set_ylabel("")
ax.set_xlabel("Property owner's share in costs of inaction $(s_l)$", fontsize=8)



ax.set_title("Objective value in EUR for varying property owner's interest rates",
                         fontsize=8)

ax.set_ylim([0, 220000])
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)))

ax.yaxis.set_major_formatter(group_thousands)

ax.tick_params(axis='x',  which='both', top=False)
ax.tick_params(axis='y',  which='both', right=False)

leg = ax.legend(loc='upper right', framealpha=1, handlelength=1,
                handletextpad=1, borderpad=0.25, columnspacing=1,
                edgecolor=None, frameon=False, ncol=3, facecolor=None)
leg.get_frame().set_linewidth(0.25)

leg.get_texts()[0].set_text(r'$i_l=10\%$')
leg.get_texts()[1].set_text(r'$i_l=5\%$')
leg.get_texts()[2].set_text(r'$i_l=3\%$')

ellipse = mpatches.Ellipse(xy=(2033.75, 50000), width=2.5, height=30000,
                           facecolor="white", linewidth=0.5, edgecolor="black",
                           linestyle="dashed")
ax.add_patch(ellipse)
ax.text(x=2033.75, y=50000, s=r'Infeasible', color="black", va="center",
        ha="center", fontsize=7)

ax.plot([2031, 2032, 2035], [89877, 93533, 99419], color="black",
        linestyle="dashed", zorder=-100, linewidth=0.5)

# ax.text(x=2032.25, y=20000, s=r'$\longleftarrow$ Decreaseing $i_l$ extends infeasible', fontsize=4)

# ax.plot([2031, 2032], [89877, 93533], linestyle="dashed",
#         color="red", linewidth=1, zorder=-1)
ax.minorticks_off()
plt.tight_layout()
fig.savefig("feasible.eps", format="eps")
fig.savefig("feasible.png", dpi=900)