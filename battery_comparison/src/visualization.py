"""
Battery Comparison System
Visualization Module

Project:
Comparative Analysis of the Performance of Lithium-Ion
and Lead-Acid Batteries for Solar System in
FUT Minna Engineering Complex

This module creates professional research-quality charts.

All chart data comes from the CSV datasets through the
analysis pipeline. No experimental values are hard-coded.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# CHART DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHART_DIR = BASE_DIR / "outputs" / "charts"

CHART_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# GENERAL CHART SETTINGS
# ============================================================

FIGURE_DPI = 200

FIGURE_SIZE = (11, 6)

FONT_SIZE_TITLE = 16
FONT_SIZE_LABEL = 12
FONT_SIZE_TICK = 10
FONT_SIZE_LEGEND = 10


# ============================================================
# SAVE CHART
# ============================================================

def _save_chart(fig, filename):
    """
    Save a matplotlib figure to the project's chart folder.
    """

    path = CHART_DIR / filename

    fig.savefig(
        path,
        dpi=FIGURE_DPI,
        bbox_inches="tight"
    )

    return path


# ============================================================
# DISCHARGE CAPACITY CHART
# ============================================================

def plot_discharge_capacity(
    df,
    save=True,
    filename="discharge_capacity.png"
):
    """
    Create a comparison of battery capacity retention
    against discharge time.

    Parameters
    ----------
    df : pandas.DataFrame
        Discharge dataset.

    save : bool
        Whether to save the chart.

    filename : str
        Output filename.

    Returns
    -------
    matplotlib.figure.Figure
    """

    required = [
        "time_hours",
        "lithium_ion_capacity",
        "lead_acid_capacity"
    ]

    _check_columns(df, required)

    time = df["time_hours"]

    lithium = df["lithium_ion_capacity"]

    lead = df["lead_acid_capacity"]

    fig, ax = plt.subplots(
        figsize=FIGURE_SIZE
    )

    ax.plot(
        time,
        lithium,
        marker="o",
        linewidth=2.5,
        markersize=7,
        label="Lithium-Ion"
    )

    ax.plot(
        time,
        lead,
        marker="s",
        linewidth=2.5,
        markersize=7,
        label="Lead-Acid"
    )

    ax.set_title(
        "Battery Capacity Retention During Discharge",
        fontsize=FONT_SIZE_TITLE,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        "Discharge Time (hours)",
        fontsize=FONT_SIZE_LABEL
    )

    ax.set_ylabel(
        "Remaining Capacity (%)",
        fontsize=FONT_SIZE_LABEL
    )

    ax.tick_params(
        axis="both",
        labelsize=FONT_SIZE_TICK
    )

    ax.set_ylim(
        0,
        105
    )

    ax.grid(
        True,
        alpha=0.25
    )

    ax.legend(
        fontsize=FONT_SIZE_LEGEND,
        frameon=True
    )

    fig.tight_layout()

    if save:
        _save_chart(
            fig,
            filename
        )

    return fig


# ============================================================
# CHARGING EFFICIENCY CHART
# ============================================================

def plot_charging_efficiency(
    df,
    save=True,
    filename="charging_efficiency.png"
):
    """
    Create a comparison of charging efficiency against time.
    """

    required = [
        "time_h",
        "lithium_ion_efficiency",
        "lead_acid_efficiency"
    ]

    _check_columns(df, required)

    time = df["time_h"]

    lithium = df[
        "lithium_ion_efficiency"
    ]

    lead = df[
        "lead_acid_efficiency"
    ]

    fig, ax = plt.subplots(
        figsize=FIGURE_SIZE
    )

    ax.plot(
        time,
        lithium,
        marker="o",
        linewidth=2.5,
        markersize=7,
        label="Lithium-Ion"
    )

    ax.plot(
        time,
        lead,
        marker="s",
        linewidth=2.5,
        markersize=7,
        label="Lead-Acid"
    )

    ax.set_title(
        "Charging Efficiency Comparison",
        fontsize=FONT_SIZE_TITLE,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        "Charging Time (hours)",
        fontsize=FONT_SIZE_LABEL
    )

    ax.set_ylabel(
        "Charging Efficiency (%)",
        fontsize=FONT_SIZE_LABEL
    )

    ax.tick_params(
        axis="both",
        labelsize=FONT_SIZE_TICK
    )

    ax.set_ylim(
        0,
        100
    )

    ax.grid(
        True,
        alpha=0.25
    )

    ax.legend(
        fontsize=FONT_SIZE_LEGEND,
        frameon=True
    )

    fig.tight_layout()

    if save:
        _save_chart(
            fig,
            filename
        )

    return fig


# ============================================================
# DEPTH OF DISCHARGE CHART
# ============================================================

def plot_depth_of_discharge(
    df,
    save=True,
    filename="depth_of_discharge.png"
):
    """
    Create a comparison of depth of discharge against cycle.
    """

    required = [
        "cycle",
        "lithium_ion_dod",
        "lead_acid_dod"
    ]

    _check_columns(df, required)

    cycles = df["cycle"]

    lithium = df[
        "lithium_ion_dod"
    ]

    lead = df[
        "lead_acid_dod"
    ]

    fig, ax = plt.subplots(
        figsize=FIGURE_SIZE
    )

    ax.plot(
        cycles,
        lithium,
        marker="o",
        linewidth=2.5,
        markersize=7,
        label="Lithium-Ion"
    )

    ax.plot(
        cycles,
        lead,
        marker="s",
        linewidth=2.5,
        markersize=7,
        label="Lead-Acid"
    )

    ax.set_title(
        "Depth of Discharge Across Battery Cycles",
        fontsize=FONT_SIZE_TITLE,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        "Cycle Number",
        fontsize=FONT_SIZE_LABEL
    )

    ax.set_ylabel(
        "Depth of Discharge (%)",
        fontsize=FONT_SIZE_LABEL
    )

    ax.tick_params(
        axis="both",
        labelsize=FONT_SIZE_TICK
    )

    ax.set_ylim(
        0,
        100
    )

    ax.grid(
        True,
        alpha=0.25
    )

    ax.legend(
        fontsize=FONT_SIZE_LEGEND,
        frameon=True
    )

    fig.tight_layout()

    if save:
        _save_chart(
            fig,
            filename
        )

    return fig


# ============================================================
# COMPARATIVE PERFORMANCE CHART
# ============================================================

def plot_comparative_performance(
    summary_df,
    save=True,
    filename="comparative_performance.png"
):
    """
    Create an overall comparison of lithium-ion and
    lead-acid battery performance.

    Expected columns:

        Performance Parameter
        Lithium-Ion
        Lead-Acid
    """

    required = [
        "Performance Parameter",
        "Lithium-Ion",
        "Lead-Acid"
    ]

    _check_columns(
        summary_df,
        required
    )

    parameters = summary_df[
        "Performance Parameter"
    ].tolist()

    lithium = summary_df[
        "Lithium-Ion"
    ].to_numpy()

    lead = summary_df[
        "Lead-Acid"
    ].to_numpy()

    x = np.arange(
        len(parameters)
    )

    width = 0.35

    fig, ax = plt.subplots(
        figsize=(12, 6.5)
    )

    ax.bar(
        x - width / 2,
        lithium,
        width,
        label="Lithium-Ion"
    )

    ax.bar(
        x + width / 2,
        lead,
        width,
        label="Lead-Acid"
    )

    ax.set_title(
        "Comparative Battery Performance",
        fontsize=FONT_SIZE_TITLE,
        fontweight="bold",
        pad=15
    )

    ax.set_ylabel(
        "Performance Value (%)",
        fontsize=FONT_SIZE_LABEL
    )

    ax.set_xticks(
        x
    )

    ax.set_xticklabels(
        parameters,
        rotation=15,
        ha="right"
    )

    ax.tick_params(
        axis="both",
        labelsize=FONT_SIZE_TICK
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )

    ax.legend(
        fontsize=FONT_SIZE_LEGEND,
        frameon=True
    )

    fig.tight_layout()

    if save:
        _save_chart(
            fig,
            filename
        )

    return fig


# ============================================================
# BATTERY PERFORMANCE DIFFERENCE CHART
# ============================================================

def plot_performance_difference(
    summary_df,
    save=True,
    filename="performance_difference.png"
):
    """
    Display the difference between lithium-ion and
    lead-acid performance.

    Difference =
        Lithium-Ion value - Lead-Acid value
    """

    required = [
        "Performance Parameter",
        "Difference"
    ]

    _check_columns(
        summary_df,
        required
    )

    parameters = summary_df[
        "Performance Parameter"
    ].tolist()

    differences = summary_df[
        "Difference"
    ].to_numpy()

    x = np.arange(
        len(parameters)
    )

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    ax.bar(
        x,
        differences
    )

    ax.axhline(
        y=0,
        linewidth=1
    )

    ax.set_title(
        "Lithium-Ion Performance Difference Relative to Lead-Acid",
        fontsize=FONT_SIZE_TITLE,
        fontweight="bold",
        pad=15
    )

    ax.set_ylabel(
        "Difference (percentage points)",
        fontsize=FONT_SIZE_LABEL
    )

    ax.set_xticks(
        x
    )

    ax.set_xticklabels(
        parameters,
        rotation=15,
        ha="right"
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )

    fig.tight_layout()

    if save:
        _save_chart(
            fig,
            filename
        )

    return fig


# ============================================================
# DASHBOARD PERFORMANCE CHART
# ============================================================

def plot_dashboard_summary(
    indicators,
    save=True,
    filename="dashboard_summary.png"
):
    """
    Create a compact dashboard-style summary chart.

    Parameters
    ----------
    indicators : dict
        Output from calculate_overall_indicators().
    """

    categories = [
        "Charging Efficiency",
        "Discharge Capacity",
        "Depth of Discharge"
    ]

    lithium_values = [
        indicators[
            "lithium_mean_charging_efficiency"
        ],

        indicators[
            "lithium_mean_discharge_capacity"
        ],

        indicators[
            "lithium_mean_dod"
        ]
    ]

    lead_values = [
        indicators[
            "lead_mean_charging_efficiency"
        ],

        indicators[
            "lead_mean_discharge_capacity"
        ],

        indicators[
            "lead_mean_dod"
        ]
    ]

    x = np.arange(
        len(categories)
    )

    width = 0.35

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    ax.bar(
        x - width / 2,
        lithium_values,
        width,
        label="Lithium-Ion"
    )

    ax.bar(
        x + width / 2,
        lead_values,
        width,
        label="Lead-Acid"
    )

    ax.set_title(
        "Battery Performance Overview",
        fontsize=FONT_SIZE_TITLE,
        fontweight="bold",
        pad=15
    )

    ax.set_ylabel(
        "Mean Value (%)",
        fontsize=FONT_SIZE_LABEL
    )

    ax.set_xticks(
        x
    )

    ax.set_xticklabels(
        categories
    )

    ax.set_ylim(
        0,
        100
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )

    ax.legend(
        fontsize=FONT_SIZE_LEGEND,
        frameon=True
    )

    fig.tight_layout()

    if save:
        _save_chart(
            fig,
            filename
        )

    return fig


# ============================================================
# GENERATE ALL CHARTS
# ============================================================

def generate_all_charts(analysis_results):
    """
    Generate every chart used by the application.

    Parameters
    ----------
    analysis_results : dict
        Output generated by run_complete_analysis().

    Returns
    -------
    dict
        Paths of generated charts.
    """

    generated = {}

    # --------------------------------------------------------
    # Discharge
    # --------------------------------------------------------

    discharge_df = analysis_results[
        "discharge"
    ]["data"]

    discharge_fig = plot_discharge_capacity(
        discharge_df
    )

    generated[
        "discharge_capacity"
    ] = CHART_DIR / "discharge_capacity.png"

    plt.close(
        discharge_fig
    )

    # --------------------------------------------------------
    # Charging
    # --------------------------------------------------------

    charging_df = analysis_results[
        "charging"
    ]["data"]

    charging_fig = plot_charging_efficiency(
        charging_df
    )

    generated[
        "charging_efficiency"
    ] = CHART_DIR / "charging_efficiency.png"

    plt.close(
        charging_fig
    )

    # --------------------------------------------------------
    # Depth of discharge
    # --------------------------------------------------------

    dod_df = analysis_results[
        "dod"
    ]["data"]

    dod_fig = plot_depth_of_discharge(
        dod_df
    )

    generated[
        "depth_of_discharge"
    ] = CHART_DIR / "depth_of_discharge.png"

    plt.close(
        dod_fig
    )

    # --------------------------------------------------------
    # Overall comparison
    # --------------------------------------------------------

    summary_df = analysis_results[
        "summary"
    ]

    comparison_fig = plot_comparative_performance(
        summary_df
    )

    generated[
        "comparative_performance"
    ] = CHART_DIR / "comparative_performance.png"

    plt.close(
        comparison_fig
    )

    # --------------------------------------------------------
    # Difference
    # --------------------------------------------------------

    difference_fig = plot_performance_difference(
        summary_df
    )

    generated[
        "performance_difference"
    ] = CHART_DIR / "performance_difference.png"

    plt.close(
        difference_fig
    )

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    indicators = analysis_results[
        "indicators"
    ]

    dashboard_fig = plot_dashboard_summary(
        indicators
    )

    generated[
        "dashboard_summary"
    ] = CHART_DIR / "dashboard_summary.png"

    plt.close(
        dashboard_fig
    )

    return generated


# ============================================================
# INTERNAL COLUMN CHECK
# ============================================================

def _check_columns(df, required_columns):
    """
    Verify that all required columns exist.
    """

    if df is None:
        raise ValueError(
            "The supplied dataset is None."
        )

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            "The visualization dataset is missing "
            "the following column(s): "
            + ", ".join(missing)
        )


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("BATTERY COMPARISON SYSTEM")
    print("VISUALIZATION MODULE")
    print("=" * 65)

    print()
    print("Chart directory:")
    print(CHART_DIR)

    print()
    print("Available visualization functions:")
    print()
    print("1. plot_discharge_capacity()")
    print("2. plot_charging_efficiency()")
    print("3. plot_depth_of_discharge()")
    print("4. plot_comparative_performance()")
    print("5. plot_performance_difference()")
    print("6. plot_dashboard_summary()")
    print("7. generate_all_charts()")

    print()
    print("Visualization module loaded successfully.")

    print("=" * 65)