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

_data_folder = Path("../../../../optimization model/result")
data = pyam.IamDataFrame(_data_folder / "heating_costs_subsidy.xlsx")

fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(2, 2)

cmap = plt.cm.jet  # define the colormap
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# force the first color entry to be grey
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
data.plot.bar(stacked=True, ax=fig_left_up, title=None, legend=False,
              cmap=cmap)
fig_left_up.set_xlabel("")
fig_left_up.set_ylabel("")
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
fig_left_up.yaxis.set_major_formatter(group_thousands)
fig_left_up.set_title("Landlord's cash flow in EUR", fontsize=6, y=0.95)
fig_left_up.tick_params("x", labelrotation=0)
fig_left_up.legend(loc="upper right", handlelength=1)
fig_left_up.tick_params(axis='x', which='both', top=False)
val = [0, 5, 10, 15]
fig_left_up.set_xticks(ticks=val)
fig_left_up.set_yticks(ticks=[-50000, -25000,0,25000,50000])
fig_left_up.tick_params(axis='y',  which='both', right=False)

"""Plot tenant's revenues in EUR (Upper right) """
_c = ["#E9A6A6", "#864879", "#3F3351"]
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c, cmap.N)

data = pyam.IamDataFrame("(b).xlsx")
data.plot.bar(stacked=True, ax=fig_right_up, title=None, legend=False,
              cmap=cmap)
fig_right_up.set_xlabel("")
fig_right_up.set_ylabel("")
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
fig_right_up.yaxis.set_major_formatter(group_thousands)
fig_right_up.set_title("Tenant's cash flow in EUR", fontsize=6, y=0.95)
fig_right_up.tick_params("x", labelrotation=0)
fig_right_up.set_ylim([-10000, 7500])
fig_right_up.legend(loc="upper right", handlelength=1)
fig_right_up.tick_params(axis='x',  which='both', top=False)
val = [0, 5, 10, 15]
fig_right_up.set_xticks(ticks=val)
fig_right_up.tick_params(axis='y',  which='both', right=False)


"""Plot landlord's net present value in EUR (lower left) """
data = pyam.IamDataFrame("(c).xlsx")
data.plot(ax=fig_left_down, title=None, legend=False, color="#678983",
          marker="d", markersize=1)
fig_left_down.set_xlabel("")
fig_left_down.set_ylabel("")
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
fig_left_down.yaxis.set_major_formatter(group_thousands)
fig_left_down.set_title("Landlord's NPV in EUR", fontsize=6, y=0.95)
fig_left_down.tick_params("x", labelrotation=0)
fig_left_down.legend(loc="upper right")
fig_left_down.tick_params(axis='x',  which='both', top=False)
labels = [2025, 2030, 2035, 2040]
fig_left_down.set_xticks(ticks=labels)

"""Plot tenant's net present value in EUR (lower right) """

_c = ["#678983", "#C8C6C6"]
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c, cmap.N)

data = pyam.IamDataFrame("(d).xlsx")
data.plot(ax=fig_right_down, title=None, legend=False, color="variable",
          cmap=cmap)
fig_right_down.set_xlabel("")
fig_right_down.set_ylabel("")
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
fig_right_down.yaxis.set_major_formatter(group_thousands)
fig_right_down.set_title("Tenant's NPV in EUR",
                         fontsize=6, y=0.95)
fig_right_down.tick_params("x", labelrotation=0)

Lines = fig_right_down.get_lines()
Lines[1].set_linestyle("dashed")


fig_right_down.legend(loc="lower left", handletextpad=0.4, handlelength=1.5,
                      fontsize=5)
fig_right_down.tick_params(axis='x',  which='both', top=False)
labels = [2025, 2030, 2035, 2040]
fig_right_down.set_xticks(ticks=labels)

plt.tight_layout()
fig.savefig("detail.eps", format="eps")
fig.savefig("detail.png", dpi=900)
