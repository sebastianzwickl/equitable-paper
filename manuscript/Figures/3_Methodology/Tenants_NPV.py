"""Plotting the model validation."""
import matplotlib.pyplot as plt

plt.style.use(['science'])

plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8

plt.rc('legend', fontsize=7)

labels = ["Conventional", "Alternative"]


width = 0.5
fig, ax = plt.subplots()

ax.minorticks_off()

ax.bar(labels, [-184898, -184898], width, label='Energy and rent charge',
       bottom=[0], color='#C6B4CE')


ax.bar(labels, [0, 13750], width, label='Heating costs subsidy',
       bottom=[0, -184898-13750], color="#9B72AA")


ax.legend(loc="lower right")
plt.xticks(rotation=0)

# ax.annotate("",
#             xy=(11, -5000), xycoords='data',
#             xytext=(7.5, -7500), textcoords='data',
#             arrowprops=dict(arrowstyle="->",
#                             connectionstyle="arc3",
#                             linewidth=0.5),
#             )

# ax.text(x=9.5, y=-7000, s=r'$\frac{4}{5}$',
#         fontsize=8, rotation=30, va="center",
#         ha="center")

# ax.text(x=0.75, y=-12436.5, s=r'$\frac{1}{5}$', fontsize=8, rotation=0,
#         va="center",
#         ha="center")

ax.text(x=1, y=-191773, s=r'$+13750$', fontsize=10, rotation=0,
        va="center",
        ha="center",
        color="black"
        )


ax.plot([0.25, 0.75], 2*[-184898], linestyle="dashed", color="#716F81",
        linewidth=0.35)

ax.annotate("",
            xy=(1, -198648), xycoords='data',
            xytext=(1, -193500), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3",
                            linewidth=0.5,
                            color="black"),
            zorder=1,
            )

ax.annotate("",
            xy=(1, -184898), xycoords='data',
            xytext=(1, -184898+(193500-198648)), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3",
                            linewidth=0.5,
                            color="black"),
            zorder=1,
            )

# ax.annotate("",
#             xy=(2.5, -0), xycoords='data',
#             xytext=(2.5, -4500), textcoords='data',
#             arrowprops=dict(arrowstyle="->",
#                             connectionstyle="arc3",
#                             linewidth=0.5,
#                             color="#716F81"),
#             zorder=-100
#             )

ax.set_ylim([-200000, -150000])
ax.set_xlim([-0.5, 1.5])
leg = ax.get_legend()
leg._loc = 3
ax.set_title("Tenant\'s net present value in EUR", fontsize=10)
fig.savefig("Validate-Tenant.eps", format="eps")
fig.savefig("Validate-Tenant.png", dpi=900)
plt.show()
