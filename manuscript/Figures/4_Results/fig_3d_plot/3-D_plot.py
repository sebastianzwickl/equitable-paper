import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transforms

c_case_D = "#8236CB"
c_case_0 = "black"
c_case_B = "#57837B"
c_case_C = "#185ADB"
c_case_A = "#FFAA4C"

def plt_sphere(list_center, list_radius):
    for c, r in zip(list_center, list_radius):    
        ax = fig.gca(projection='3d')

        u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
        x = r*np.cos(u)*np.sin(v)
        y = r*np.sin(u)*np.sin(v)
        z = r*np.cos(v)
    
        ax.plot_surface(x-c[0], y-c[1], z-c[2], color=np.random.choice(['g','b']), alpha=0.5*np.random.random()+0.5)



plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 5
plt.rcParams['ytick.labelsize'] = 5
plt.rc('legend', fontsize=4)
plt.rcParams['grid.color'] = "#E1E5EA"
plt.rcParams['grid.linewidth'] = 0.2


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# FIRST LINE
f_line_x = np.linspace(0, 1/3, 1000)
f_line_y = np.linspace(0, 1/3, 1000)
f_line_z = np.linspace(0, 1/3, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, color=c_case_A, linewidth=0.25,
          linestyle="solid")

f_line_x = np.linspace(0, 0, 1000)
f_line_y = np.linspace(0, 1, 1000)
f_line_z = np.linspace(0, 0, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, color=c_case_C, linewidth=0.25,
          linestyle="solid")

f_line_x = np.linspace(0, 1/2, 1000)
f_line_y = np.linspace(0, 1/2, 1000)
f_line_z = np.linspace(0, 0, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, color=c_case_B, linewidth=0.25,
          linestyle="solid")

f_line_x = np.linspace(0, 1/2, 1000)
f_line_y = np.linspace(0, 0, 1000)
f_line_z = np.linspace(0, 1/2, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, color=c_case_D, linewidth=0.25,
          linestyle="solid")


f_line_x = np.linspace(1/3, 1/3, 1000)
f_line_y = np.linspace(0, 1/3, 1000)
f_line_z = np.linspace(0, 0, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, 'gray', linestyle="dotted",
          linewidth=0.35)

f_line_x = np.linspace(1/3, 1/3, 1000)
f_line_y = np.linspace(1/3, 1/3, 1000)
f_line_z = np.linspace(0, 1/3, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, 'gray', linestyle="dotted",
          linewidth=0.35)

f_line_x = np.linspace(0, 1/3, 1000)
f_line_y = np.linspace(0, 0, 1000)
f_line_z = np.linspace(0, 0, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, 'gray', linestyle="dotted",
          linewidth=0.35)

f_line_x = np.linspace(0, 0, 1000)
f_line_y = np.linspace(0, 0, 1000)
f_line_z = np.linspace(0, 1, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, color=c_case_0, linewidth=0.25,
          linestyle="solid")

ax.plot3D(0, 0, 1, marker="d", markersize=2)

f_line_x = np.linspace(1/3, 1/2, 1000)
f_line_y = np.linspace(0, 0, 1000)
f_line_z = np.linspace(0, 0, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, 'gray', linestyle="dotted",
          linewidth=0.35)

f_line_x = np.linspace(1/2, 1/2, 1000)
f_line_y = np.linspace(0, 1/2, 1000)
f_line_z = np.linspace(0, 0, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, 'gray', linestyle="dotted",
          linewidth=0.35)

f_line_x = np.linspace(1/2, 1/2, 1000)
f_line_y = np.linspace(0, 0, 1000)
f_line_z = np.linspace(0, 1/2, 1000)
ax.plot3D(f_line_x, f_line_y, f_line_z, 'gray', linestyle="dotted",
          linewidth=0.35)

ax.text(-0.325, 0.15, 1, s='Ref. value', fontsize=5, zdir=None, color=c_case_0,
        bbox=dict(facecolor='white', edgecolor=c_case_0, linewidth=0.1,
                  boxstyle="round,pad=0.3"))

ax.text(.15, 1, 0.1, s=r'$-49\%$', fontsize=5, zdir=None, color=c_case_C,
        bbox=dict(facecolor='white', edgecolor=c_case_C, linewidth=0.25,
                  boxstyle="round,pad=0.3"))

ax.text(.65, 0.5, 0.1, s=r'$-34\%$', fontsize=5, zdir=None, color=c_case_B,
        bbox=dict(facecolor='white', edgecolor=c_case_B, linewidth=0.25,
                  boxstyle="round,pad=0.3"))

ax.text(-0.02, 1/3, 1/3, s=r'$-25\%$', fontsize=5, zdir=None, color=c_case_A,
        bbox=dict(facecolor='white', edgecolor=c_case_A, linewidth=0.25,
                  boxstyle="round,pad=0.3"))

ax.text(0.25, 0, 0.15, s=r'$-6\%$', fontsize=5, zdir=None, color=c_case_D,
        bbox=dict(facecolor='white', edgecolor=c_case_D, linewidth=0.25,
                  boxstyle="round,pad=0.3"))

# zdirs = ('x', None)
# xs = (0.5, 0)
# ys = (0.5, 0)
# zs = (0.5, 0)

# for zdir, x, y, z in zip(zdirs, xs, ys, zs):
#     label = '(%d, %d, %d), dir=%s' % (x, y, z, zdir)
#     ax.text(x, y, z, label, zdir)
    
ax.set_zlabel("Governance's share $(g)$", fontsize=5, labelpad=-10)
ax.set_xlabel("Tenant's share $(t)$", fontsize=5, labelpad=-10)
ax.set_ylabel("Landlord's share $(l)$", fontsize=5, labelpad=-10)

ax.set_xticks(ticks=[0, 1/3, 0.5, 2/3, 0.915])
ax.set_xticklabels(
    labels=[r'$0$', r'$\frac{1}{3}$', r'$\frac{1}{2}$', r'$\frac{2}{3}$', r'$1$'])
ax.set_yticks(ticks=[0, 1/3, 0.5, 2/3, 1])
ax.set_yticklabels(
    labels=[r'$0$', r'$\frac{1}{3}$', r'$\frac{1}{2}$', r'$\frac{2}{3}$', r'$1$'],
    ha="center", va="center")

ax.set_zticks(ticks=[0, 1/3, 0.5, 2/3, 1])
ax.set_zticklabels(
    labels=[r'$0$', r'$\frac{1}{3}$', r'$\frac{1}{2}$', r'$\frac{2}{3}$', r'$1$'])

offset = matplotlib.transforms.ScaledTranslation(1, 0, fig.dpi_scale_trans)

for label in ax.yaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)

ax.tick_params(axis='y', which='major', pad=-4)
ax.tick_params(axis='x', which='major', pad=-6)
ax.tick_params(axis='z', which='major', pad=-4)




from matplotlib.lines import Line2D
_patches = []
# _line = Line2D([1], [2], label = "Minimum",color="black")
# _patches.extend([_line])
# _line = Line2D([0], [0], label = "Heat",color="black", linewidth=6)
# _patches.extend([_line])
line4 = Line2D(range(1), range(1), color="white", marker='o',markersize=4,
               markerfacecolor=c_case_0, label='GD (DH) ($t$=0, $l$=0, $g$=1)')
_patches.extend([line4])

line4 = Line2D(range(1), range(1), color="white", marker='o',markersize=4,
               markerfacecolor=c_case_A, label=r'Case A $(\frac{1}{3}, \frac{1}{3}, \frac{1}{3})$')
_patches.extend([line4])
line4 = Line2D(range(1), range(1), color="white", marker='o',markersize=4,
               markerfacecolor=c_case_B, label=r'Case B $(\frac{1}{2}, \frac{1}{2}, 0)$')
_patches.extend([line4])
line4 = Line2D(range(1), range(1), color="white", marker='o',markersize=4,
               markerfacecolor=c_case_C, label='Case C $(0, 1, 0)$')
_patches.extend([line4])
line4 = Line2D(range(1), range(1), color="white", marker='o',markersize=4,
               markerfacecolor=c_case_D, label=r'Case D $(\frac{1}{2}, 0, \frac{1}{2})$')
_patches.extend([line4])
leg = ax.legend(handles=_patches, loc='lower center', bbox_to_anchor=(0.625, 0.65), ncol=1, edgecolor="black", frameon=True, framealpha=1)
leg.get_frame().set_linewidth(0.25)

ax.set_title(
    "Rel. change of objective value in \% of GD (DH)\nfor varying allocation of "+"CO$_2$"+"-related opportunity costs", fontsize=8, y=1.02)



ax.scatter(0, 0, 1, s=200, color=c_case_0)
ax.scatter(1/3, 1/3, 1/3, s=151, color=c_case_A)
ax.scatter(1/2, 1/2, 0, s=133, color=c_case_B)
ax.scatter(0, 1, 0, s=102, color=c_case_C)
ax.scatter(1/2, 0, 1/2, s=188, color=c_case_D)

ax.set_zlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlim(0, 1)
# plt.tight_layout()
fig.savefig("3d.png", dpi=900)
fig.savefig("3d.eps", format="eps")