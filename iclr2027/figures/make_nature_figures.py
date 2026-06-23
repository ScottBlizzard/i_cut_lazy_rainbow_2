from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches


OUT_DIR = Path(__file__).resolve().parent


PALETTE = {
    "signal": "#2F8F8C",
    "signal_soft": "#DCEEEE",
    "signal_mid": "#8EC7C3",
    "neutral_dark": "#303030",
    "neutral_mid": "#777777",
    "neutral_light": "#D8D8D8",
    "neutral_soft": "#F4F4F4",
}


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 7
plt.rcParams["axes.linewidth"] = 0.7
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["legend.frameon"] = False


def save_pub(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT_DIR / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(OUT_DIR / f"{stem}.pdf", bbox_inches="tight")


def add_round_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    *,
    facecolor: str,
    edgecolor: str,
    linewidth: float = 0.8,
    fontsize: float = 7,
    color: str = PALETTE["neutral_dark"],
) -> patches.FancyBboxPatch:
    box = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.08,rounding_size=0.07",
        linewidth=linewidth,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        linespacing=1.05,
    )
    return box


def arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], *, color: str) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle="-|>",
            lw=0.8,
            color=color,
            shrinkA=0,
            shrinkB=0,
            mutation_scale=8,
        ),
    )


def make_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(6.55, 1.25))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.axis("off")

    y_top = 2.05
    box_w = 1.95
    box_h = 0.55
    xs = [0.25, 3.0, 5.75, 8.65]
    labels = [
        "Goal g\ncandidate names",
        "Shared baseline\nempty Hammer",
        "ACE compiler\ntyped allocation",
        "Lean kernel\nverified outcome",
    ]
    faces = [PALETTE["neutral_soft"], PALETTE["neutral_soft"], PALETTE["signal_soft"], PALETTE["neutral_soft"]]
    edges = ["#B0B0B0", "#B0B0B0", PALETTE["signal"], "#B0B0B0"]
    boxes = [
        add_round_box(ax, (x, y_top), box_w, box_h, label, facecolor=face, edgecolor=edge)
        for x, label, face, edge in zip(xs, labels, faces, edges)
    ]

    for left, right in zip(boxes[:-1], boxes[1:]):
        y = y_top + box_h / 2
        arrow(ax, (left.get_x() + left.get_width() + 0.12, y), (right.get_x() - 0.12, y), color=PALETTE["neutral_mid"])

    route_y = 0.85
    channel_labels = [
        ("Hammer", "facts"),
        ("HammerCore", "inputs"),
        ("Simp", "lemmas"),
        ("Local", "facts"),
        ("Aesop", "facts/simps"),
    ]
    channel_x0 = 1.2
    channel_w = 1.72
    gap = 0.18
    channel_boxes = []
    for i, (head, sub) in enumerate(channel_labels):
        x = channel_x0 + i * (channel_w + gap)
        channel_boxes.append(
            add_round_box(
                ax,
                (x, route_y),
                channel_w,
                0.48,
                f"{head}\n{sub}",
                facecolor="#EEF7F7",
                edgecolor=PALETTE["signal"],
                linewidth=0.65,
                fontsize=6.4,
            )
        )

    compiler = boxes[2]
    arrow(
        ax,
        (compiler.get_x() + compiler.get_width() / 2, y_top - 0.04),
        (compiler.get_x() + compiler.get_width() / 2, route_y + 0.56),
        color=PALETTE["signal"],
    )
    ax.text(
        6,
        0.28,
        "same candidate names; different executable Lean interfaces; fixed retry budget",
        ha="center",
        va="center",
        color=PALETTE["neutral_mid"],
        fontsize=6.4,
    )

    save_pub(fig, "ace_pipeline")
    plt.close(fig)


def make_result_ladder() -> None:
    data = [
        {"setting": "Mixed-source 230", "single": 38, "portfolio": 57, "oracle": 58},
        {"setting": "Retrieved-only 230", "single": 35, "portfolio": 52, "oracle": 52},
        {"setting": "Fresh holdout 432", "single": 54, "portfolio": 67, "oracle": 68},
    ]
    with (OUT_DIR / "result_ladder_source.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["setting", "single", "portfolio", "oracle"])
        writer.writeheader()
        writer.writerows(data)

    fig, ax = plt.subplots(figsize=(6.55, 1.45))
    y_positions = [2.0, 1.0, 0.0]
    bar_h = 0.18

    for row, y in zip(data, y_positions):
        single = row["single"] / row["oracle"]
        portfolio = row["portfolio"] / row["oracle"]
        ax.barh(y + bar_h / 1.7, single, height=bar_h, color=PALETTE["neutral_light"], edgecolor="none")
        ax.barh(y - bar_h / 1.7, portfolio, height=bar_h, color=PALETTE["signal_mid"], edgecolor="none")
        ax.plot([1, 1], [y - 0.31, y + 0.31], color=PALETTE["neutral_dark"], lw=0.8)
        ax.text(single + 0.018, y + bar_h / 1.7, str(row["single"]), va="center", ha="left", fontsize=6.8)
        ax.text(
            min(portfolio - 0.018, 0.965),
            y - bar_h / 1.7,
            str(row["portfolio"]),
            va="center",
            ha="right",
            fontsize=6.8,
            color=PALETTE["signal"],
        )
        ax.text(1.08, y, str(row["oracle"]), va="center", ha="left", fontsize=6.8, color=PALETTE["neutral_dark"])

    ax.set_yticks(y_positions)
    ax.set_yticklabels([row["setting"] for row in data])
    ax.set_xlim(0, 1.18)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(["0", "50%", "100%"])
    ax.set_xlabel("Verified goals / tested-action oracle", labelpad=2)
    ax.tick_params(axis="both", length=0, pad=2)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(PALETTE["neutral_light"])
    ax.grid(axis="x", color="#E8E8E8", lw=0.6)
    ax.set_axisbelow(True)

    ax.text(0.02, 2.55, "strongest single", color=PALETTE["neutral_mid"], ha="left", va="center", fontsize=6.8)
    ax.text(0.46, 2.55, "fixed portfolio", color=PALETTE["signal"], ha="left", va="center", fontsize=6.8)
    ax.text(1.08, 2.55, "oracle", color=PALETTE["neutral_dark"], ha="left", va="center", fontsize=6.8)

    save_pub(fig, "result_ladder")
    plt.close(fig)


def main() -> None:
    make_pipeline()
    make_result_ladder()


if __name__ == "__main__":
    main()
