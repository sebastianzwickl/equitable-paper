"""Plotting script the net present value of the six different sceanrios."""
import pyam
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6
plt.rc('legend', fontsize=7)

_data_folder = Path("../../../../optimization model/result")
data = pyam.IamDataFrame(_data_folder / "heating_costs_subsidy.xlsx")

fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(2, 3)


fig_left_inv = fig.add_subplot(gs[0:2, 0])
fig_left_inv.minorticks_off()
fig_up_subsidy = fig.add_subplot(gs[0, 1:3])
fig_up_subsidy.minorticks_off()
fig_down_subsidy = fig.add_subplot(gs[1, 1:3])
fig_down_subsidy.minorticks_off()

scenarios = ('DT (DH)', 'GD (DH)', 'GD (HP)', 'LD (DH)', 'LD (HP)', 'SC (HP)')
y_pos = np.arange(len(scenarios))
value = [0, 0, 0, 0, 145, 0]

fig_left_inv.barh(y_pos, value, align='center')

fig_left_inv.set_yticks(y_pos)

fig_left_inv.set_yticklabels(list(scenarios))

fig_left_inv.set_title("Investment grant\nin "+r'$\frac{EUR}{kW}$', fontsize=8)

for _i in range(0, len(scenarios)):
    fig_left_inv.text(x=value[_i]+12.5, y=_i, s=str(value[_i]), rotation=-90,
                      va="center", ha="center")

fig_left_inv.set_xlim([0, max(value)*1.35])

energy = data.filter(variable="Heating costs subsidy")
rent = data.filter(variable="Rent charge adjustment")

energy.plot(ax=fig_up_subsidy)
fig_up_subsidy.set_title("Heating costs subsidy in "+r'$\frac{EUR}{kWh}$',
                         fontsize=8)
fig_up_subsidy.set_ylabel("")
fig_up_subsidy.set_xlabel("")
rent.plot(ax=fig_down_subsidy)
fig_down_subsidy.set_title("Rent charge adjustment in "+r'$\frac{EUR}{m^2}$',
                           fontsize=8)
fig_down_subsidy.set_ylabel("")
fig_down_subsidy.set_xlabel("")

plt.tight_layout()
fig.savefig("price_dev.eps", format="eps")
fig.savefig("price_dev.png", dpi=900)
