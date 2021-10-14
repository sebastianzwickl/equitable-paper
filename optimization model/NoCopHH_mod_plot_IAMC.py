import pyam as py
import matplotlib.pyplot as plt
import os


def plot_results(res_dir):

    # Plot Day-Ahead, Future (Base) and CO2 Price
    plt.style.use("ggplot")

    fig, ax = plt.subplots()
    df = py.IamDataFrame("IAMC_inputs.xlsx")
    df.plot(
        color="variable",
        title="Electricity prices in EUR/MWh, $CO_2$ price in EUR/t",
        marker="d",
        markersize=5,
        ax=ax,
    )
    plt.xlabel("Time in h")
    plt.ylabel("")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    legend = plt.legend(fontsize=12)
    legend.get_texts()[0].set_text("$CO_2$")
    legend.get_texts()[1].set_text("Day-Ahead (EPEX)")
    legend.get_texts()[2].set_text("Future contract (EEX)")

    plt.tight_layout()
    fig.savefig(os.path.join(res_dir, "Prices.png"), dpi=500)

    # Plot Results
    fig, ax = plt.subplots()
    df = py.IamDataFrame(os.path.join(res_dir, "IAMC_hourly.xlsx"))
    df.plot(
        color="variable",
        title="Hydropower plant resource allocation in MWh",
        marker="d",
        markersize=5,
        ax=ax,
        cmap="Dark2",
    )
    plt.xlabel("Time in h")
    plt.ylabel("")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.title("Hydropower plant resource allocation in MWh", fontsize=14)
    plt.tight_layout()
    fig.savefig(os.path.join(res_dir, "Ressource allocation.png"), dpi=500)

    # Plot supply/generation
    fig = plt.figure(constrained_layout=False)
    plt.style.use("ggplot")
    gs = fig.add_gridspec(2, 1)
    fig_leader = fig.add_subplot(gs[0, :])
    fig_follower = fig.add_subplot(gs[1, :])

    df = py.IamDataFrame(os.path.join(res_dir, "IAMC_supply.xlsx"))
    data_leader = df.filter(variable=["Future contract", "Day-Ahead"])
    data_leader.plot.stack(
        stack="variable",
        title="Hydropower electricty production",
        total=True,
        ax=fig_leader,
        cmap="Set3",
    )
    fig_leader.set_xlabel("Time in h")
    lines = fig_leader.get_lines()
    lines[0].set_linewidth(2)
    fig_leader.set_title("Hydropower electricty production", fontsize=12)

    data_leader = df.filter(variable=["Conventional"])
    data_leader.plot.stack(
        stack="variable",
        title="Energy demand provision\n(transportation firm)",
        total=True,
        ax=fig_follower,
        cmap="PiYG",
    )
    fig_follower.set_xlabel("Time in h")
    lines = fig_follower.get_lines()
    lines[0].set_linewidth(2)
    fig_follower.set_title(
        "Energy demand provision\n(transportation firm)", fontsize=12
    )

    plt.tight_layout()
    fig.savefig(os.path.join(res_dir, "Energy service provision.png"), dpi=500)
