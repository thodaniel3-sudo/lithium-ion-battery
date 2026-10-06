"""
LEBAS Battery Comparison System
Data Loading Module

Project:
Comparative Analysis of the Performance of Lithium-Ion
and Lead-Acid Batteries for Solar System in FUT Minna
Engineering Complex
"""

from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CHARGING_FILE = DATA_DIR / "charging_efficiency.csv"
DISCHARGE_FILE = DATA_DIR / "discharge_capacity.csv"
DOD_FILE = DATA_DIR / "depth_of_discharge.csv"


# ============================================================
# REQUIRED COLUMNS
# ============================================================

CHARGING_COLUMNS = [
    "time_h",
    "lithium_ion_efficiency",
    "lead_acid_efficiency",
]

DISCHARGE_COLUMNS = [
    "time_hours",
    "lithium_ion_capacity",
    "lead_acid_capacity",
]

DOD_COLUMNS = [
    "cycle",
    "lithium_ion_dod",
    "lead_acid_dod",
]


# ============================================================
# GENERAL CSV LOADER
# ============================================================

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    file_path : Path or str
        Location of the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.

    ValueError
        If the CSV file is empty.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Data file not found:\n{file_path}"
        )

    try:
        df = pd.read_csv(file_path)

    except Exception as error:
        raise RuntimeError(
            f"Unable to read CSV file:\n"
            f"{file_path}\n\n"
            f"Error: {error}"
        )

    if df.empty:
        raise ValueError(
            f"The CSV file is empty:\n{file_path}"
        )

    # Remove accidental spaces from column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # Remove completely empty rows
    df = df.dropna(how="all")

    return df


# ============================================================
# COLUMN VALIDATION
# ============================================================

def validate_columns(df, required_columns, dataset_name):
    """
    Check whether a dataset contains all required columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to check.

    required_columns : list
        Required column names.

    dataset_name : str
        Human-readable dataset name.

    Returns
    -------
    bool
        True if all required columns exist.

    Raises
    ------
    ValueError
        If required columns are missing.
    """

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"{dataset_name} is missing the following "
            f"required column(s):\n\n"
            + "\n".join(
                f"- {column}"
                for column in missing_columns
            )
        )

    return True


# ============================================================
# NUMERIC COLUMN CONVERSION
# ============================================================

def convert_numeric_columns(df, columns):
    """
    Convert specified columns to numeric values.

    Invalid values are converted to NaN.
    """

    df = df.copy()

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# ============================================================
# CHARGING EFFICIENCY
# ============================================================

def load_charging_efficiency():
    """
    Load charging-efficiency experimental data.

    Returns
    -------
    pandas.DataFrame
    """

    df = load_csv(CHARGING_FILE)

    validate_columns(
        df,
        CHARGING_COLUMNS,
        "Charging efficiency dataset"
    )

    df = convert_numeric_columns(
        df,
        CHARGING_COLUMNS
    )

    return df


# ============================================================
# DISCHARGE CAPACITY
# ============================================================

def load_discharge_capacity():
    """
    Load discharge-capacity experimental data.

    Returns
    -------
    pandas.DataFrame
    """

    df = load_csv(DISCHARGE_FILE)

    validate_columns(
        df,
        DISCHARGE_COLUMNS,
        "Discharge capacity dataset"
    )

    df = convert_numeric_columns(
        df,
        DISCHARGE_COLUMNS
    )

    return df


# ============================================================
# DEPTH OF DISCHARGE
# ============================================================

def load_depth_of_discharge():
    """
    Load depth-of-discharge experimental data.

    Returns
    -------
    pandas.DataFrame
    """

    df = load_csv(DOD_FILE)

    validate_columns(
        df,
        DOD_COLUMNS,
        "Depth of discharge dataset"
    )

    df = convert_numeric_columns(
        df,
        DOD_COLUMNS
    )

    return df


# ============================================================
# LOAD ALL DATASETS
# ============================================================

def load_all_data():
    """
    Load all three battery datasets.

    Returns
    -------
    dict
        Dictionary containing the three DataFrames.
    """

    charging = load_charging_efficiency()

    discharge = load_discharge_capacity()

    dod = load_depth_of_discharge()

    return {
        "charging": charging,
        "discharge": discharge,
        "dod": dod,
    }


# ============================================================
# DATASET INFORMATION
# ============================================================

def get_dataset_information(df):
    """
    Return basic information about a dataset.
    """

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
    }


# ============================================================
# QUICK DATA CHECK
# ============================================================

def check_data_files():
    """
    Check whether all required CSV files exist.

    Returns
    -------
    dict
        File existence status.
    """

    return {
        "charging_efficiency": CHARGING_FILE.exists(),
        "discharge_capacity": DISCHARGE_FILE.exists(),
        "depth_of_discharge": DOD_FILE.exists(),
    }


# ============================================================
# TEST FUNCTION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("BATTERY COMPARISON SYSTEM")
    print("DATA LOADER TEST")
    print("=" * 60)

    print("\nChecking data files...\n")

    files = check_data_files()

    for name, exists in files.items():

        status = "FOUND" if exists else "NOT FOUND"

        print(
            f"{name:<25} : {status}"
        )

    print("\nLoading datasets...\n")

    try:

        data = load_all_data()

        for name, df in data.items():

            print(
                f"{name.upper():<15} "
                f"{len(df)} rows, "
                f"{len(df.columns)} columns"
            )

        print("\nAll datasets loaded successfully.")

    except Exception as error:

        print(
            "\nDATA LOADING ERROR:"
        )

        print(error)

    print("\n" + "=" * 60)