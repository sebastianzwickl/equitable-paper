"""Plotting the model validation."""
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rc('legend', fontsize=7)

color_grants = "#77ACF1"
color_inv = "#D7E9F7"
color_rev = "#FFB319"

plt.minorticks_off()

labels = []
for i in range(2025, 2041, 1):
    labels.append(str(i))

men_means = [2627]
_null = 15*[0]
io = men_means + _null
i1 = men_means + _null
i1[0] = -13750+2627

revenues = [600, 588.2352941, 576.7012687, 565.3934007, 815.1642501,
            799.1806374, 783.5104288, 768.1474792, 753.0857639, 738.3193764,
            723.8425259, 709.6495352, 695.7348384, 682.0929788, 668.7186067,
            655.6064772]

width = 0.5
fig, ax = plt.subplots()

ax.minorticks_off()

ax.bar(labels, i1, width, label='Overnight investment costs',
       bottom=[0], color=color_inv)

bottom_values = []
bottom_values.append(-13750+2627)

for i in range(1, len(revenues)):
    val = bottom_values[i-1]
    bottom_values.append(val+revenues[i-1])

ax.bar(labels, io, width, label='Investment grants', bottom=[-13750],
       color=color_grants)

ax.bar(labels,
       revenues,
       width,
       label='Rent-charge related revenues', bottom=bottom_values,
       color=color_rev)

ax.plot([-0.25, 0.25], 2*[-13750], linewidth=1, linestyle="solid",
        color="black")

ax.plot([-0.25, 0.25], 2*[-13750+2627], linewidth=1, linestyle="solid",
        color="black")

for index, value in enumerate(bottom_values):
    if index != len(bottom_values)-1:
        ax.plot([index+0.25, index+0.75],
                [bottom_values[index+1], bottom_values[index+1]],
                linewidth=0.35, color="black", linestyle="dotted")

ax.plot([15+0.25, 15+0.75], [0, 0], linewidth=0.35, color="black",
        linestyle="dotted")

ax.legend(loc="lower right")
plt.xticks(rotation=90)

ax.annotate("",
            xy=(11, -5000), xycoords='data',
            xytext=(7.5, -7500), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3",
                            linewidth=0.5,
                            color="#716F81"),
            )

ax.text(x=9.75, y=-7250, s=r'$\frac{4}{5}$',
        fontsize=13, rotation=30, va="center",
        ha="center",
        color="#716F81")

ax.text(x=0.75, y=-12436.5, s=r'$\frac{1}{5}$', fontsize=13, rotation=0,
        va="center",
        ha="center",
        color="#716F81")

ax.text(x=2.5, y=-6750, s=r'+13,750', fontsize=10, rotation=0,
        va="center",
        ha="center",
        color="black"
        )


ax.plot([0.75, 3], 2*[-13750], linestyle="dashed", color="#716F81",
        linewidth=0.5)
ax.plot([2, 14.25], 2*[0], linestyle="dashed", color="#716F81", linewidth=0.5)

ax.annotate("",
            xy=(2.5, -13750), xycoords='data',
            xytext=(2.5, -11000), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3",
                            linewidth=0.5,
                            color="black"),
            zorder=-100,
            )

ax.annotate("",
            xy=(2.5, -0), xycoords='data',
            xytext=(2.5, -4500), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3",
                            linewidth=0.5,
                            color="black"),
            zorder=-100
            )

ax.set_ylim([-15000, 1000])
ax.set_xlim([-1, 16])
leg = ax.get_legend()
leg._loc = 4
group_thousands = tkr.FuncFormatter(lambda x, pos: '{:0,d}'.format(
    int(x)))

ax.yaxis.set_major_formatter(group_thousands)
ax.set_title("Property owner\'s net present value in EUR", fontsize=10)
fig.savefig("Validate-Landlord.eps", format="eps")
fig.savefig("Validate-Landlord.png", dpi=900)
