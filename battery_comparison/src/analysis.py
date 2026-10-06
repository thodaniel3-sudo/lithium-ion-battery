"""
Battery Comparison Analysis Module

Project:
Comparative Analysis of the Performance of Lithium-Ion
and Lead-Acid Batteries for Solar System in
FUT Minna Engineering Complex

This module contains the scientific calculations used by
the application.

IMPORTANT:
The application reads experimental values from CSV files.
No experimental values are hard-coded in this module.
"""

import numpy as np
import pandas as pd


# ============================================================
# GENERAL STATISTICS
# ============================================================

def calculate_statistics(values):
    """
    Calculate basic descriptive statistics.

    Standard deviation is calculated as SAMPLE standard
    deviation using ddof=1.

    The returned dictionary contains both the scientific
    names (minimum/maximum) and compatibility aliases
    (min/max) required by the graphical interface.
    """

    series = pd.to_numeric(
        pd.Series(values),
        errors="coerce"
    ).dropna()

    if len(series) == 0:

        return {
            "count": 0,
            "mean": np.nan,
            "std": np.nan,
            "minimum": np.nan,
            "maximum": np.nan,
            "min": np.nan,
            "max": np.nan,
            "range": np.nan,
            "cv": np.nan
        }

    mean_value = series.mean()

    if len(series) > 1:
        std_value = series.std(ddof=1)
    else:
        std_value = 0.0

    minimum = series.min()
    maximum = series.max()

    data_range = maximum - minimum

    if mean_value != 0:
        coefficient_variation = (
            std_value / mean_value
        ) * 100
    else:
        coefficient_variation = 0.0

    return {
        "count": int(len(series)),

        "mean": float(mean_value),

        "std": float(std_value),

        "minimum": float(minimum),

        "maximum": float(maximum),

        # Compatibility aliases used by main.py
        "min": float(minimum),

        "max": float(maximum),

        "range": float(data_range),

        "cv": float(coefficient_variation)
    }


# ============================================================
# CHARGING EFFICIENCY ANALYSIS
# ============================================================

def analyze_charging_efficiency(df):
    """
    Analyse lithium-ion and lead-acid charging efficiency.

    Required columns:

        time_h
        lithium_ion_efficiency
        lead_acid_efficiency
    """

    required = [
        "time_h",
        "lithium_ion_efficiency",
        "lead_acid_efficiency"
    ]

    _check_columns(df, required)

    lithium = pd.to_numeric(
        df["lithium_ion_efficiency"],
        errors="coerce"
    )

    lead = pd.to_numeric(
        df["lead_acid_efficiency"],
        errors="coerce"
    )

    lithium_stats = calculate_statistics(
        lithium
    )

    lead_stats = calculate_statistics(
        lead
    )

    difference = lithium - lead

    percentage_advantage = np.where(
        lead != 0,
        ((lithium - lead) / lead) * 100,
        np.nan
    )

    result = df.copy()

    result["efficiency_difference"] = difference

    result["lithium_advantage_pct"] = (
        percentage_advantage
    )

    return {
        "data": result,

        # Original analysis structure
        "lithium_statistics": lithium_stats,
        "lead_acid_statistics": lead_stats,

        # Compatibility structure for main.py
        "lithium_ion": lithium_stats,
        "lead_acid": lead_stats,

        "mean_difference": float(
            np.nanmean(difference)
        ),

        "mean_advantage_pct": float(
            np.nanmean(percentage_advantage)
        )
    }


# ============================================================
# DISCHARGE CAPACITY ANALYSIS
# ============================================================

def analyze_discharge_capacity(df):
    """
    Analyse battery capacity retention during discharge.

    Required columns:

        time_hours
        lithium_ion_capacity
        lead_acid_capacity
    """

    required = [
        "time_hours",
        "lithium_ion_capacity",
        "lead_acid_capacity"
    ]

    _check_columns(df, required)

    lithium = pd.to_numeric(
        df["lithium_ion_capacity"],
        errors="coerce"
    )

    lead = pd.to_numeric(
        df["lead_acid_capacity"],
        errors="coerce"
    )

    lithium_stats = calculate_statistics(
        lithium
    )

    lead_stats = calculate_statistics(
        lead
    )

    difference = lithium - lead

    percentage_difference = np.where(
        lead != 0,
        ((lithium - lead) / lead) * 100,
        np.nan
    )

    result = df.copy()

    result["capacity_difference"] = difference

    result["lithium_advantage_pct"] = (
        percentage_difference
    )

    # --------------------------------------------------------
    # Remove missing values before determining initial/final
    # capacity
    # --------------------------------------------------------

    lithium_valid = lithium.dropna()

    lead_valid = lead.dropna()

    # --------------------------------------------------------
    # Initial capacity
    # --------------------------------------------------------

    if not lithium_valid.empty:
        initial_lithium = lithium_valid.iloc[0]
    else:
        initial_lithium = np.nan

    if not lead_valid.empty:
        initial_lead = lead_valid.iloc[0]
    else:
        initial_lead = np.nan

    # --------------------------------------------------------
    # Final capacity
    # --------------------------------------------------------

    if not lithium_valid.empty:
        final_lithium = lithium_valid.iloc[-1]
    else:
        final_lithium = np.nan

    if not lead_valid.empty:
        final_lead = lead_valid.iloc[-1]
    else:
        final_lead = np.nan

    # --------------------------------------------------------
    # Capacity loss
    # --------------------------------------------------------

    if not np.isnan(final_lithium):
        lithium_capacity_loss = (
            initial_lithium - final_lithium
        )
    else:
        lithium_capacity_loss = np.nan

    if not np.isnan(final_lead):
        lead_capacity_loss = (
            initial_lead - final_lead
        )
    else:
        lead_capacity_loss = np.nan

    return {
        "data": result,

        # Original analysis structure
        "lithium_statistics": lithium_stats,
        "lead_acid_statistics": lead_stats,

        # Compatibility structure for main.py
        "lithium_ion": lithium_stats,
        "lead_acid": lead_stats,

        "mean_difference": float(
            np.nanmean(difference)
        ),

        "mean_percentage_difference": float(
            np.nanmean(percentage_difference)
        ),

        "initial_lithium_capacity": float(
            initial_lithium
        ),

        "initial_lead_acid_capacity": float(
            initial_lead
        ),

        "final_lithium_capacity": float(
            final_lithium
        ),

        "final_lead_acid_capacity": float(
            final_lead
        ),

        "lithium_capacity_loss": float(
            lithium_capacity_loss
        ),

        "lead_acid_capacity_loss": float(
            lead_capacity_loss
        )
    }


# ============================================================
# DEPTH OF DISCHARGE ANALYSIS
# ============================================================

def analyze_depth_of_discharge(df):
    """
    Analyse depth of discharge over battery cycles.

    Required columns:

        cycle
        lithium_ion_dod
        lead_acid_dod
    """

    required = [
        "cycle",
        "lithium_ion_dod",
        "lead_acid_dod"
    ]

    _check_columns(df, required)

    lithium = pd.to_numeric(
        df["lithium_ion_dod"],
        errors="coerce"
    )

    lead = pd.to_numeric(
        df["lead_acid_dod"],
        errors="coerce"
    )

    lithium_stats = calculate_statistics(
        lithium
    )

    lead_stats = calculate_statistics(
        lead
    )

    difference = lithium - lead

    percentage_difference = np.where(
        lead != 0,
        ((lithium - lead) / lead) * 100,
        np.nan
    )

    result = df.copy()

    result["dod_difference"] = difference

    result["dod_difference_pct"] = (
        percentage_difference
    )

    return {
        "data": result,

        # Original analysis structure
        "lithium_statistics": lithium_stats,
        "lead_acid_statistics": lead_stats,

        # Compatibility structure for main.py
        "lithium_ion": lithium_stats,
        "lead_acid": lead_stats,

        "mean_difference": float(
            np.nanmean(difference)
        ),

        "mean_percentage_difference": float(
            np.nanmean(percentage_difference)
        )
    }


# ============================================================
# COMPARATIVE PERFORMANCE SUMMARY
# ============================================================

def create_comparative_summary(
    charging_result,
    discharge_result,
    dod_result
):
    """
    Create a summary table comparing both battery
    technologies.
    """

    charging_lithium_mean = (
        charging_result[
            "lithium_statistics"
        ]["mean"]
    )

    charging_lead_mean = (
        charging_result[
            "lead_acid_statistics"
        ]["mean"]
    )

    discharge_lithium_mean = (
        discharge_result[
            "lithium_statistics"
        ]["mean"]
    )

    discharge_lead_mean = (
        discharge_result[
            "lead_acid_statistics"
        ]["mean"]
    )

    dod_lithium_mean = (
        dod_result[
            "lithium_statistics"
        ]["mean"]
    )

    dod_lead_mean = (
        dod_result[
            "lead_acid_statistics"
        ]["mean"]
    )

    summary = pd.DataFrame({

        "Performance Parameter": [
            "Mean Charging Efficiency (%)",
            "Mean Discharge Capacity (%)",
            "Mean Depth of Discharge (%)"
        ],

        "Lithium-Ion": [
            charging_lithium_mean,
            discharge_lithium_mean,
            dod_lithium_mean
        ],

        "Lead-Acid": [
            charging_lead_mean,
            discharge_lead_mean,
            dod_lead_mean
        ]
    })

    summary["Difference"] = (
        summary["Lithium-Ion"]
        - summary["Lead-Acid"]
    )

    summary["Percentage Difference"] = np.where(
        summary["Lead-Acid"] != 0,
        (
            summary["Difference"]
            / summary["Lead-Acid"]
        ) * 100,
        np.nan
    )

    return summary


# ============================================================
# OVERALL PERFORMANCE INDICATORS
# ============================================================

def calculate_overall_indicators(
    charging_result,
    discharge_result,
    dod_result
):
    """
    Produce high-level indicators for the dashboard.
    """

    charging_lithium = (
        charging_result[
            "lithium_statistics"
        ]["mean"]
    )

    charging_lead = (
        charging_result[
            "lead_acid_statistics"
        ]["mean"]
    )

    discharge_lithium = (
        discharge_result[
            "lithium_statistics"
        ]["mean"]
    )

    discharge_lead = (
        discharge_result[
            "lead_acid_statistics"
        ]["mean"]
    )

    dod_lithium = (
        dod_result[
            "lithium_statistics"
        ]["mean"]
    )

    dod_lead = (
        dod_result[
            "lead_acid_statistics"
        ]["mean"]
    )

    return {

        "lithium_mean_charging_efficiency":
            charging_lithium,

        "lead_mean_charging_efficiency":
            charging_lead,

        "lithium_mean_discharge_capacity":
            discharge_lithium,

        "lead_mean_discharge_capacity":
            discharge_lead,

        "lithium_mean_dod":
            dod_lithium,

        "lead_mean_dod":
            dod_lead,

        "charging_efficiency_difference":
            charging_lithium - charging_lead,

        "discharge_capacity_difference":
            discharge_lithium - discharge_lead,

        "dod_difference":
            dod_lithium - dod_lead
    }


# ============================================================
# DATA QUALITY CHECK
# ============================================================

def check_analysis_data(df):
    """
    Check for missing and invalid numerical values.
    """

    report = {
        "rows": len(df),
        "missing_values": {},
        "negative_values": {},
        "valid": True
    }

    for column in df.columns:

        missing = int(
            df[column].isna().sum()
        )

        if missing > 0:

            report[
                "missing_values"
            ][column] = missing

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        negative = int(
            (df[column] < 0).sum()
        )

        if negative > 0:

            report[
                "negative_values"
            ][column] = negative

    if (
        report["missing_values"]
        or report["negative_values"]
    ):

        report["valid"] = False

    return report


# ============================================================
# INTERNAL COLUMN VALIDATION
# ============================================================

def _check_columns(
    df,
    required_columns
):
    """
    Internal function used to verify required columns.
    """

    if not isinstance(
        df,
        pd.DataFrame
    ):

        raise TypeError(
            "Input data must be a pandas DataFrame."
        )

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            "Missing required column(s): "
            + ", ".join(missing)
        )


# ============================================================
# COMPLETE ANALYSIS PIPELINE
# ============================================================

def run_complete_analysis(data):
    """
    Run the complete battery comparison analysis.

    Parameters
    ----------
    data : dict
        Dictionary containing:

            charging
            discharge
            dod

    Returns
    -------
    dict
        Complete analysis results.
    """

    if not isinstance(
        data,
        dict
    ):

        raise TypeError(
            "Data must be supplied as a dictionary."
        )

    required_datasets = [
        "charging",
        "discharge",
        "dod"
    ]

    for dataset in required_datasets:

        if dataset not in data:

            raise KeyError(
                f"Dataset '{dataset}' was not supplied."
            )

    # --------------------------------------------------------
    # Run individual analyses
    # --------------------------------------------------------

    charging_result = (
        analyze_charging_efficiency(
            data["charging"]
        )
    )

    discharge_result = (
        analyze_discharge_capacity(
            data["discharge"]
        )
    )

    dod_result = (
        analyze_depth_of_discharge(
            data["dod"]
        )
    )

    # --------------------------------------------------------
    # Comparative summary
    # --------------------------------------------------------

    summary = create_comparative_summary(
        charging_result,
        discharge_result,
        dod_result
    )

    # --------------------------------------------------------
    # Dashboard indicators
    # --------------------------------------------------------

    indicators = calculate_overall_indicators(
        charging_result,
        discharge_result,
        dod_result
    )

    # --------------------------------------------------------
    # Final analysis object
    # --------------------------------------------------------

    return {

        "charging": charging_result,

        "discharge": discharge_result,

        "dod": dod_result,

        "summary": summary,

        "indicators": indicators
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 65)

    print(
        "BATTERY COMPARISON ANALYSIS MODULE"
    )

    print("=" * 65)

    print()

    print(
        "This module contains the scientific calculations."
    )

    print()

    print(
        "Available analysis functions:"
    )

    print()

    print(
        "1. Charging efficiency analysis"
    )

    print(
        "2. Discharge capacity analysis"
    )

    print(
        "3. Depth of discharge analysis"
    )

    print(
        "4. Comparative performance analysis"
    )

    print(
        "5. Statistical analysis"
    )

    print(
        "6. Overall performance indicators"
    )

    print()

    print(
        "Analysis module loaded successfully."
    )

    print("=" * 65)