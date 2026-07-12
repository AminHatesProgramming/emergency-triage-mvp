# -*- coding: utf-8 -*-
"""Regenerate final management charts with honest forecast/evidence labels."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "docs" / "artifacts"
POSTER = ROOT / "poster-assets"


def save_burndown() -> None:
    df = pd.read_csv(ART / "burndown-data.csv")
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.plot(df["day"], df["ideal_remaining_story_points"], "--", color="#60717e", linewidth=2, label="Ideal")
    ax.plot(df["day"], df["actual_remaining_story_points"], marker="o", color="#087f8c", linewidth=2.6, label="Actual")
    ax.fill_between(df["day"], df["actual_remaining_story_points"], alpha=0.10, color="#087f8c")
    ax.set(title="Final Sprint Burndown", xlabel="Sprint day", ylabel="Remaining story points")
    ax.set_xticks(df["day"])
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(POSTER / "burndown-chart.png", dpi=220)
    fig.savefig(ART / "burndown-final.png", dpi=220)
    fig.savefig(ART / "burndown.svg")
    plt.close(fig)


def save_velocity() -> None:
    df = pd.read_csv(ART / "velocity-data.csv")
    x = range(len(df))
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    ax.bar([i - 0.18 for i in x], df["planned_story_points"], width=0.36, color="#a8bbc2", label="Planned")
    ax.bar([i + 0.18 for i in x], df["completed_story_points"], width=0.36, color="#157a55", label="Completed")
    ax.set(title="Sprint Velocity", ylabel="Story points")
    ax.set_xticks(list(x), df["sprint"], rotation=18, ha="right")
    ax.grid(axis="y", alpha=0.2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(POSTER / "sprint-velocity.png", dpi=220)
    fig.savefig(ART / "velocity-final.png", dpi=220)
    fig.savefig(ART / "velocity.svg")
    plt.close(fig)


def save_user_forecast() -> None:
    df = pd.read_csv(ART / "user-acquisition-data.csv")
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    ax.plot(df["period"], df["forecast_cumulative_testers"], marker="o", color="#575bc3", linewidth=2.6, label="Pilot forecast")
    ax.scatter([df["period"].iloc[-1]], [df["verified_specialist_feedback"].iloc[-1]], s=110, color="#c43b3b", zorder=5, label="Verified specialist feedback (9)")
    ax.annotate("9 confirmed triage-nurse feedback items\n(not clinical validation)",
                (len(df) - 1, 9), xytext=(-190, 28), textcoords="offset points",
                arrowprops={"arrowstyle": "->", "color": "#c43b3b"}, fontsize=9)
    ax.set(title="Pilot User Acquisition Forecast vs. Verified Evidence", ylabel="Cumulative people")
    ax.set_ylim(0, 78)
    ax.tick_params(axis="x", rotation=18)
    ax.grid(alpha=0.2)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(POSTER / "user-acquisition-forecast.png", dpi=220)
    fig.savefig(ART / "user-acquisition-final.png", dpi=220)
    fig.savefig(ART / "user-acquisition.svg")
    plt.close(fig)


def save_stakeholder_engagement() -> None:
    labels = ["Triage nurses\nconfirmed feedback", "Payambaran Hospital\nmeeting request", "Salamat Fardaye Tehran\nmeeting request"]
    values = [9, 1, 1]
    colors = ["#157a55", "#b8770a", "#b8770a"]
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    bars = ax.bar(labels, values, color=colors, width=0.58)
    ax.bar_label(bars, labels=["9 confirmed", "awaiting response", "awaiting response"], padding=5, fontsize=9)
    ax.set(title="Stakeholder Engagement Evidence", ylabel="Recorded interactions / feedback items", ylim=(0, 11))
    ax.grid(axis="y", alpha=0.18)
    ax.text(0.5, -0.22, "No hospital partnership or clinical validation is claimed.", transform=ax.transAxes, ha="center", color="#60717e", fontsize=9)
    fig.tight_layout()
    fig.savefig(POSTER / "stakeholder-engagement.png", dpi=220, bbox_inches="tight")
    fig.savefig(ART / "stakeholder-engagement.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    POSTER.mkdir(parents=True, exist_ok=True)
    save_burndown()
    save_velocity()
    save_user_forecast()
    save_stakeholder_engagement()
    print("Updated final management charts.")


if __name__ == "__main__":
    main()
