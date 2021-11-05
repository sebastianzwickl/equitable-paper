import matplotlib.pyplot as plt
import pyam
import matplotlib.ticker as tkr

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rc('legend', fontsize=7)

fig, ax = plt.subplots()

# args = dict(
#     model="WITCH-GLOBIOM 4.4",
#     scenario="CD-LINKS_NPi2020_1000",
#     region="World",
# )

data = pyam.IamDataFrame("cop_sens_an.xlsx")

format_args = dict(color="#89B5AF", linestyle="solid", marker="*",
                   label="Objective function value", linewidth=1, markersize=5)

data_1 = data.filter(variable="Objective function value")


ax2 = ax.twinx()
format_args = dict(color="#161616", linestyle="--", marker="d",
                    label="Energy demand", linewidth=0.25, markersize=2)

data_2 = data.filter(variable="Energy demand")
data_2.plot(x="year", ax=ax2, legend=False, title=None, **format_args,
            zorder=0)

format_args = dict(color="#89B5AF", linestyle="solid", marker="*",
                   label="Objective function value", linewidth=1, markersize=5)
data_1.plot(x="year", ax=ax, legend=False, title=None, **format_args, zorder=10)

data = data_2._data

for index, value in enumerate(data):
    if value != 100 and value != 115:
        ax2.text(x=index+2025+0.25, y=value*1.01, s=str(value), va="center",
                 ha="center", fontsize=5,
                 bbox=dict(facecolor='none', edgecolor='black',
                           linewidth=0.5, boxstyle="round,pad=0.2"))
    else:
        if value == 115:
            ax2.text(x=index+2025-0.25, y=value*0.99, s=str(value),
                     va="center", ha="center", fontsize=5,
                     bbox=dict(facecolor='none', edgecolor='black',
                               linewidth=0.5, boxstyle="round,pad=0.2"))

ax2.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(2027.875, 92.5), xycoords='data',
    xytext=(2026, 100), textcoords='data',
    arrowprops=dict(headlength=4.5, 
                    headwidth=1.5,
                    width=0.05,
                    linewidth=0.5,
                    connectionstyle="arc3,rad=.1",
                    color="#C85C5C"))
ax2.text(x=2025, y=106,
         s="Energy justice constraint\n(high overnight investment costs\nfor the building owner)",
         fontsize=7, va="center", multialignment="center", color="#C85C5C")




ax.set_ylabel("Governance's NPV in EUR")
ax2.set_ylabel("Energy demand in "+r'$\frac{kWh}{m^2 yr}$')

ax2.set_ylim([90, 150])

ax.set_xlabel("Coefficient of Performance (COP)")
# ax.legend(loc=4)
# ax2.legend(loc=1)
# ax2.set_ylim(0, 2)
# ax.set_title("Primary energy mix and temperature")

group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)).replace(',', ' '))
ax.yaxis.set_major_formatter(group_thousands)

plt.xticks(rotation=0)
ax.set_xticks([2025, 2026, 2027, 2028])
ax.set_xticklabels(labels=['2.35', '2.5', "3.0", "3.5"])

# plt.tight_layout()

fig.savefig("renovation.eps", format="eps")
fig.savefig("renovation.png", dpi=900)
