from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


OUT_DIR = Path(__file__).resolve().parent


PALETTE = {
    "signal": "#2F8F8C",
    "signal_dark": "#1F6663",
    "signal_soft": "#DCEEEE",
    "neutral_dark": "#303030",
    "neutral_mid": "#6A6A6A",
    "neutral_light": "#D8D8D8",
    "neutral_soft": "#F4F4F4",
}


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "Nimbus Roman", "DejaVu Serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 9.0,
        "axes.linewidth": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
    }
)


def save_pub(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT_DIR / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(OUT_DIR / f"{stem}.pdf", bbox_inches="tight")


def make_result_ladder() -> None:
    data = [
        {"setting": "Mixed-source matrix", "denom": "230", "empty": 29, "single": 38, "portfolio": 57, "oracle": 58},
        {"setting": "Retrieved-only anchor", "denom": "230", "empty": 29, "single": 35, "portfolio": 52, "oracle": 52},
        {"setting": "Frozen fresh holdout", "denom": "432", "empty": 30, "single": 54, "portfolio": 67, "oracle": 68},
    ]
    for row in data:
        row["single_pct"] = 100 * row["single"] / row["oracle"]
        row["portfolio_pct"] = 100 * row["portfolio"] / row["oracle"]

    with (OUT_DIR / "result_ladder_source.csv").open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "setting",
                "denom",
                "empty",
                "single",
                "portfolio",
                "oracle",
                "single_pct",
                "portfolio_pct",
            ],
        )
        writer.writeheader()
        writer.writerows(data)

    fig, ax = plt.subplots(figsize=(6.65, 2.65))
    y_base = [4.8, 2.55, 0.3]
    bar_h = 0.36

    ax.set_xlim(-1.5, 112)
    ax.set_ylim(-0.65, 5.75)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#E8E8E8", lw=0.7)

    for row, y in zip(data, y_base):
        single = row["single_pct"]
        portfolio = row["portfolio_pct"]

        ax.text(
            -1.0,
            y + 0.46,
            f"{row['setting']} ({row['denom']} goals)",
            ha="left",
            va="center",
            fontsize=9.2,
            color=PALETTE["neutral_dark"],
        )

        ax.barh(y + 0.08, single, height=bar_h, color=PALETTE["neutral_light"], edgecolor="none")
        ax.barh(y - 0.38, portfolio, height=bar_h, color=PALETTE["signal"], edgecolor="none")
        ax.plot([100, 100], [y - 0.68, y + 0.36], color=PALETTE["neutral_dark"], lw=0.8)

        ax.text(
            max(2, single - 2.2),
            y + 0.08,
            f"single {row['single']}/{row['oracle']} ({single:.0f}%)",
            ha="right" if single > 38 else "left",
            va="center",
            fontsize=8.3,
            color=PALETTE["neutral_dark"],
        )
        ax.text(
            min(portfolio - 2.2, 97.8),
            y - 0.38,
            f"portfolio {row['portfolio']}/{row['oracle']} ({portfolio:.0f}%)",
            ha="right",
            va="center",
            fontsize=8.3,
            color="white",
        )
        ax.text(
            101.5,
            y - 0.15,
            f"oracle\n{row['oracle']}",
            ha="left",
            va="center",
            fontsize=8.0,
            linespacing=0.95,
            color=PALETTE["neutral_dark"],
        )

    ax.set_yticks([])
    ax.set_xticks([0, 50, 100])
    ax.set_xticklabels(["0", "50%", "100%"])
    ax.set_xlabel("Fraction of tested-action oracle recovered", labelpad=3)
    ax.tick_params(axis="x", length=0, pad=2)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(PALETTE["neutral_light"])

    save_pub(fig, "result_ladder")
    plt.close(fig)


def main() -> None:
    make_result_ladder()


if __name__ == "__main__":
    main()
