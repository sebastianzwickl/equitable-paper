"""Plotting script the net present value of the six different sceanrios."""
import pyam
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mlp
import matplotlib.ticker as tkr

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 5
plt.rcParams['ytick.labelsize'] = 5
plt.rc('legend', fontsize=5)


fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(2, 2)

cmap = plt.cm.jet
cmaplist = [cmap(i) for i in range(cmap.N)]
cmaplist[0] = (.5, .5, .5, 1.0)

_c = ["#77ACF1", "#D7E9F7", "#FFB319"]
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c, cmap.N)

fig_left_up = fig.add_subplot(gs[0, 0])
fig_left_up.minorticks_off()
fig_left_down = fig.add_subplot(gs[1, 0])
fig_left_down.minorticks_off()
fig_right_up = fig.add_subplot(gs[0, 1])
fig_right_up.minorticks_off()
fig_right_down = fig.add_subplot(gs[1, 1])
fig_right_down.minorticks_off()


"""Plot landlord's revenues in EUR (Upper left) """
data = pyam.IamDataFrame("(a).xlsx")

_c = ["#99A799", "#D7E9F7"]
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c, cmap.N)

data.plot.bar(stacked=True, ax=fig_left_up, title=None, legend=False,
              cmap=cmap, edgecolor="black", linewidth=0.25)
fig_left_up.set_xlabel("")
fig_left_up.set_ylabel("")
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
fig_left_up.yaxis.set_major_formatter(group_thousands)
fig_left_up.set_title("Governance's total costs in EUR", fontsize=6, y=0.95)
fig_left_up.tick_params("x", labelrotation=0)
fig_left_up.set_xticklabels(labels=["0\%", "10\%", "20\%", "30\%"])
fig_left_up.tick_params(axis='x', which='both', top=False)
fig_left_up.text(x=0, y=450000, s='Infeasible', color="black",
        style='italic', rotation=0, va="center", ha="left", fontsize=4,
                  bbox=dict(facecolor='none', edgecolor='black', linewidth=0.25,
                                        boxstyle="round,pad=0.3"))
fig_left_up.set_ylim([0, 510000])

fig_left_up.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(0, 250000), xycoords='data',
    xytext=(.5, 415000), textcoords='data',
    arrowprops=dict(headlength=3.5,
                    headwidth=1,
                    width=0.025,
                    linewidth=0.5,
                    connectionstyle="arc3,rad=.1",
                    color="black", zorder=-10))


fig_left_up.text(x=0.175, y=75000, s=r'$145\frac{kWh}{m^2 yr}$', color="black",
        rotation=90, va="bottom", ha="center", fontsize=4.5,
                  bbox=dict(facecolor='none', edgecolor='#595260', linewidth=0.,
                                        boxstyle="round,pad=0.3"))

fig_left_up.text(x=1.175, y=75000, s=r'$130\frac{kWh}{m^2 yr}$', color="black",
        rotation=90, va="bottom", ha="center", fontsize=4.5,
                  bbox=dict(facecolor='none', edgecolor='white', linewidth=0.,
                                        boxstyle="round,pad=0.3"))

fig_left_up.text(x=2.175, y=75000, s=r'$115\frac{kWh}{m^2 yr}$', color="black",
        rotation=90, va="bottom", ha="center", fontsize=4.5,
                  bbox=dict(facecolor='none', edgecolor='white', linewidth=0.,
                                        boxstyle="round,pad=0.3"))

fig_left_up.text(x=3.175, y=75000, s=r'$100\frac{kWh}{m^2 yr}$', color="black",
                 rotation=90, va="bottom", ha="center", fontsize=4.5,
                 bbox=dict(
                     facecolor='none', edgecolor='white', linewidth=0.,
                     boxstyle="round,pad=0.3"))
fig_left_up.tick_params(axis='y',  which='both', right=False)

""" FIGURE (b) """
_c = ["#77ACF1", "#864879", "#3F3351"]
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c, cmap.N)

data = pyam.IamDataFrame("(b).xlsx")
data.plot.bar(stacked=True, ax=fig_right_up, title=None, legend=False,
              cmap=cmap, linewidth=0., edgecolor="black")
fig_right_up.set_xlabel("")
fig_right_up.set_ylabel("")
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
fig_right_up.yaxis.set_major_formatter(group_thousands)
fig_right_up.set_title("Investment grant in EUR", fontsize=6, y=0.95)
fig_right_up.tick_params(axis='x',  which='both', top=False)

fig_right_up.text(x=1, y=33500, s=r'29\% of investm.', color="black",
                  rotation=90, va="center", ha="center", fontsize=5)

fig_right_up.text(x=2, y=33500, s=r'2\% of investm.', color="black",
                  rotation=90, va="center", ha="center", fontsize=5)

fig_right_up.text(x=3, y=33500, s=r'3\% of investm.', color="black",
                  rotation=90, va="center", ha="center", fontsize=5)


fig_right_up.set_xticklabels(labels=["0\%", "10\%", "20\%", "30\%"])
fig_right_up.tick_params("x", labelrotation=0)
fig_right_up.tick_params(axis='y',  which='both', right=False)



"""FIGURE (c)"""
data = pyam.IamDataFrame("(c).xlsx")
data.plot(ax=fig_left_down, title=None, legend=False, color="#3F3351",
          marker="d", markersize=0)
Lines = fig_left_down.get_lines()

Lines[1].set_linestyle("dashed")
Lines[2].set_linestyle("dotted")

fig_left_down.set_xlabel("")
fig_left_down.set_ylabel("")
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
fig_left_down.yaxis.set_major_formatter(group_thousands)
fig_left_down.set_title("Subsidy payment in EUR/unit", fontsize=6, y=0.95)
fig_left_down.tick_params("x", labelrotation=0)
fig_left_down.set_ylim([0, 5200])
# fig_left_down.set_yticks(ticks=[0, 1000, 2000, 3000, 4000])
Legend = fig_left_down.legend(loc="upper right", frameon=True, framealpha=1,
                              edgecolor="black")
Legend.get_frame().set_linewidth(0.25)

Legend.get_texts()[0].set_text(r'$10\%$')
Legend.get_texts()[1].set_text(r'$20\%$')
Legend.get_texts()[2].set_text(r'$30\%$')

fig_left_down.tick_params(axis='x',  which='both', top=False)
labels = [2025, 2030, 2035, 2040]
fig_left_down.set_xticks(ticks=labels)
# fig_left_down.tick_params(axis='y',  which='both', right=False)

"""FIGURE (d)"""

_c = ["#FFB319", "#C8C6C6"]
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c, cmap.N)

data = pyam.IamDataFrame("(d).xlsx")
data.plot(ax=fig_right_down, title=None, legend=False, color="#FFB319")
fig_right_down.set_xlabel("")
fig_right_down.set_ylabel("")
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
fig_right_down.yaxis.set_major_formatter(group_thousands)
fig_right_down.set_title("Rent revenues in EUR",
                         fontsize=6, y=0.95)
fig_right_down.tick_params("x", labelrotation=0)

Lines = fig_right_down.get_lines()

Lines[1].set_linestyle("dashed")
Lines[2].set_linestyle("dotted")


Legend = fig_right_down.legend(loc="lower right", frameon=True, framealpha=1,
                              edgecolor="black")
Legend.get_frame().set_linewidth(0.25)

Legend.get_texts()[0].set_text(r'$10\%$')
Legend.get_texts()[1].set_text(r'$20\%$')
Legend.get_texts()[2].set_text(r'$30\%$')

fig_right_down.set_ylim([0, 47500])

fig_right_down.tick_params(axis='x',  which='both', top=False)
fig_right_down.set_xticks(ticks=labels)
# fig_right_down.tick_params(axis='y',  which='both', right=False)

plt.tight_layout()
fig.savefig("retrofitting.eps", format="eps")
fig.savefig("retrofitting.png", dpi=900)
