"""Plotting script the net present value of the six different sceanrios."""
import pyam
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mlp

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rc('legend', fontsize=7)


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
              title="Governance\'s net present value in EUR",
              bars_order=None, cmap=cmap)

ax.set_ylabel("")

plt.xticks(rotation=45)
ax.minorticks_off()

# plt.tight_layout()

fig.savefig("net_present_value.eps", format="eps")
fig.savefig("net_present_value.png", dpi=900)
