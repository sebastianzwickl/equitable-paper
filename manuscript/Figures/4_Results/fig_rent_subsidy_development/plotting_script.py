"""Plotting script the net present value of the six different sceanrios."""
import pyam
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mlp

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6
plt.rc('legend', fontsize=7)

_data_folder = Path("../../../../optimization model/result")
data = pyam.IamDataFrame(_data_folder / "heating_costs_subsidy.xlsx")

fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(2, 3)

cmap = plt.cm.jet  # define the colormap
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# force the first color entry to be grey
cmaplist[0] = (.5, .5, .5, 1.0)

_c = ["#A2D2FF", "#B24080", "#2F86A6", "#FFE699", "#6ECB63", "#F2F013"]

# create the new map
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c, cmap.N)

fig_left_inv = fig.add_subplot(gs[0:2, 0])
fig_left_inv.minorticks_off()
fig_up_subsidy = fig.add_subplot(gs[0, 1:3])
fig_up_subsidy.minorticks_off()
fig_down_subsidy = fig.add_subplot(gs[1, 1:3])
fig_down_subsidy.minorticks_off()

scenarios = ('DT (DH)', 'GD (DH)', 'GD (HP)', 'LD (DH)', 'LD (HP)', 'SC (HP)')
y_pos = np.arange(len(scenarios))
value = [416, 202, 0, 112, 333, 0]

fig_left_inv.barh(y_pos, value, align='center', color=_c, linewidth=0.25,
                  edgecolor="black")

fig_left_inv.set_yticks(y_pos)

fig_left_inv.set_yticklabels(list(scenarios))

for label in fig_left_inv.yaxis.get_ticklabels():
    label.set_bbox(dict(facecolor='none', edgecolor='black', linewidth=0.1,
                        boxstyle="square,pad=0.2"))

fig_left_inv.set_title("Investment grant\nin "+r'$\frac{EUR}{kW}$', fontsize=8)

for _i in range(0, len(scenarios)):
    if value[_i] != 0:
        fig_left_inv.text(x=value[_i]+30, y=_i, s=str(value[_i]), rotation=-90,
                          va="center", ha="center", fontsize=6)
    else:
        fig_left_inv.text(x=value[_i]+50, y=_i, s='$\it{Infeasible}$',
                          rotation=0, va="center", ha="left", fontsize=6)

fig_left_inv.set_xlim([0, max(value)*1.35])

energy = data.filter(variable="Heating costs subsidy")
rent = data.filter(variable="Rent charge adjustment")

"""Adapt cmap accordingly here"""


_c1 = ["#A2D2FF", "#FFE699", "#B24080", "#6ECB63"]
cmap = mlp.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', _c1, cmap.N)


energy.plot(ax=fig_up_subsidy, color="scenario", cmap=cmap, marker="d",
            markersize=2)
fig_up_subsidy.set_title("Heating costs subsidy in "+r'$\frac{EUR}{kWh}$',
                         fontsize=8)
fig_up_subsidy.set_ylabel("")
fig_up_subsidy.set_xlabel("")
fig_up_subsidy.get_legend().remove()

rent.plot(ax=fig_down_subsidy, color="scenario", cmap=cmap)
fig_down_subsidy.set_title("Rent charge adjustment in "+r'$\frac{EUR}{m^2}$',
                           fontsize=8)
fig_down_subsidy.set_ylabel("")
fig_down_subsidy.get_legend().remove()
fig_down_subsidy.set_xlabel("")

plt.tight_layout()
fig.savefig("price_dev.eps", format="eps")
fig.savefig("price_dev.png", dpi=900)
