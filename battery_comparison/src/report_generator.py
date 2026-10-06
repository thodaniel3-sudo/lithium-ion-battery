"""
Battery Comparison System
Report Generation Module

Project:
Comparative Analysis of the Performance of Lithium-Ion
and Lead-Acid Batteries for Solar System in
FUT Minna Engineering Complex

This module generates a professional research report
from the supplied battery analysis results.

IMPORTANT:
The program does not invent experimental results.
The values used in the report come directly from the
CSV datasets supplied to the application.
"""

from pathlib import Path
from datetime import datetime

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
)

from .data_loader import BASE_DIR


# ============================================================
# PROJECT INFORMATION
# ============================================================

PROJECT_TITLE = (
    "Comparative Analysis of the Performance of "
    "Lithium-Ion and Lead-Acid Batteries for a Solar "
    "System in FUT Minna Engineering Complex"
)

OUTPUT_DIR = BASE_DIR / "outputs"

REPORT_DIR = OUTPUT_DIR

CHART_DIR = OUTPUT_DIR / "charts"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# REPORT FILE
# ============================================================

DEFAULT_REPORT_PATH = (
    REPORT_DIR / "battery_comparison_report.pdf"
)


# ============================================================
# REPORT STYLES
# ============================================================

def create_report_styles():
    """
    Create the styles used throughout the PDF report.
    """

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ProjectTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SubHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyResearch",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            alignment=TA_LEFT,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableText",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CenterText",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
        )
    )

    return styles


# ============================================================
# PAGE NUMBER
# ============================================================

def add_page_number(canvas, document):
    """
    Add page number and report footer.
    """

    canvas.saveState()

    page_width, page_height = A4

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.drawCentredString(
        page_width / 2,
        1.0 * cm,
        f"Page {document.page}"
    )

    canvas.drawString(
        1.5 * cm,
        1.0 * cm,
        "Battery Comparison Analysis System"
    )

    canvas.restoreState()


# ============================================================
# NUMBER FORMATTER
# ============================================================

def format_number(value, decimals=2):
    """
    Safely format numerical values.
    """

    try:
        return f"{float(value):.{decimals}f}"

    except (
        TypeError,
        ValueError
    ):
        return str(value)


# ============================================================
# DATAFRAME TO REPORT TABLE
# ============================================================

def dataframe_to_table(
    df,
    decimal_places=2
):
    """
    Convert a pandas DataFrame into a ReportLab table.
    """

    if df is None or df.empty:
        return Table(
            [["No data available"]]
        )

    headers = list(df.columns)

    table_data = [
        [
            Paragraph(
                str(header),
                ParagraphStyle(
                    "HeaderTemp",
                    fontName="Helvetica-Bold",
                    fontSize=8,
                    alignment=TA_CENTER,
                )
            )
            for header in headers
        ]
    ]

    for _, row in df.iterrows():

        formatted_row = []

        for value in row:

            if isinstance(
                value,
                (int, float)
            ):
                value = format_number(
                    value,
                    decimal_places
                )

            formatted_row.append(
                Paragraph(
                    str(value),
                    ParagraphStyle(
                        "CellTemp",
                        fontName="Helvetica",
                        fontSize=8,
                        alignment=TA_CENTER,
                    )
                )
            )

        table_data.append(
            formatted_row
        )

    table = Table(
        table_data,
        repeatRows=1,
        hAlign="CENTER"
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#163A2D")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F2F5F3")
                    ]
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
            ]
        )
    )

    return table


# ============================================================
# KPI TABLE
# ============================================================

def create_kpi_table(
    indicators
):
    """
    Create a summary table of key performance indicators.
    """

    rows = [
        [
            "Performance Indicator",
            "Lithium-Ion",
            "Lead-Acid",
        ],

        [
            "Mean Charging Efficiency (%)",
            format_number(
                indicators[
                    "lithium_mean_charging_efficiency"
                ]
            ),
            format_number(
                indicators[
                    "lead_mean_charging_efficiency"
                ]
            ),
        ],

        [
            "Mean Discharge Capacity (%)",
            format_number(
                indicators[
                    "lithium_mean_discharge_capacity"
                ]
            ),
            format_number(
                indicators[
                    "lead_mean_discharge_capacity"
                ]
            ),
        ],

        [
            "Mean Depth of Discharge (%)",
            format_number(
                indicators[
                    "lithium_mean_dod"
                ]
            ),
            format_number(
                indicators[
                    "lead_mean_dod"
                ]
            ),
        ],
    ]

    table = Table(
        rows,
        colWidths=[
            8.5 * cm,
            4 * cm,
            4 * cm,
        ],
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#163A2D")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F2F5F3")
                    ]
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
            ]
        )
    )

    return table


# ============================================================
# REPORT INTRODUCTION
# ============================================================

def build_introduction(styles):
    """
    Create the introduction section.
    """

    story = []

    story.append(
        Paragraph(
            "1. Introduction",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "Energy storage is an important component of solar "
            "energy systems because batteries provide the means "
            "for storing electrical energy generated during "
            "periods of solar availability and supplying power "
            "when solar generation is insufficient.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            "This analysis provides a comparative assessment "
            "of lithium-ion and lead-acid battery performance "
            "using the supplied charging efficiency, discharge "
            "capacity and depth of discharge datasets.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            "The purpose of the application is to provide a "
            "consistent computational framework for examining "
            "the supplied battery performance data and "
            "presenting the results in tables and graphical form.",
            styles["BodyResearch"]
        )
    )

    return story


# ============================================================
# METHODOLOGY
# ============================================================

def build_methodology(styles):
    """
    Create the methodology section.
    """

    story = []

    story.append(
        Paragraph(
            "2. Methodology",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "The analysis system reads three comma-separated "
            "value (CSV) datasets. The datasets represent "
            "charging efficiency, discharge capacity and "
            "depth of discharge for lithium-ion and lead-acid "
            "batteries.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            "The data are processed using descriptive statistical "
            "analysis. For each battery type, the system "
            "calculates the number of observations, mean, "
            "standard deviation, minimum value, maximum value, "
            "range and coefficient of variation where applicable.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            "The comparative analysis also determines the "
            "difference between the lithium-ion and lead-acid "
            "values for corresponding observations.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            "<b>Data integrity note:</b> The report uses only "
            "the values contained in the project's CSV files. "
            "No additional experimental observations are "
            "generated by the software.",
            styles["BodyResearch"]
        )
    )

    return story


# ============================================================
# CHARGING SECTION
# ============================================================

def build_charging_section(
    styles,
    charging_result
):
    """
    Create charging efficiency results.
    """

    story = []

    story.append(
        Paragraph(
            "3. Charging Efficiency Analysis",
            styles["SectionHeading"]
        )
    )

    lithium_stats = charging_result[
        "lithium_ion"
    ]

    lead_stats = charging_result[
        "lead_acid"
    ]

    story.append(
        Paragraph(
            "The supplied charging-efficiency dataset was "
            "examined to determine the central tendency and "
            "variation of the recorded values for both battery "
            "types.",
            styles["BodyResearch"]
        )
    )

    stats_df = pd.DataFrame(
        [
            {
                "Battery Type": "Lithium-Ion",
                "Mean (%)": lithium_stats["mean"],
                "SD": lithium_stats["std"],
                "Minimum (%)": lithium_stats["min"],
                "Maximum (%)": lithium_stats["max"],
            },

            {
                "Battery Type": "Lead-Acid",
                "Mean (%)": lead_stats["mean"],
                "SD": lead_stats["std"],
                "Minimum (%)": lead_stats["min"],
                "Maximum (%)": lead_stats["max"],
            }
        ]
    )

    story.append(
        dataframe_to_table(
            stats_df
        )
    )

    story.append(
        Spacer(
            1,
            0.4 * cm
        )
    )

    chart_path = (
        CHART_DIR /
        "charging_efficiency.png"
    )

    if chart_path.exists():

        story.append(
            Image(
                str(chart_path),
                width=16 * cm,
                height=8.5 * cm
            )
        )

    return story


# ============================================================
# DISCHARGE SECTION
# ============================================================

def build_discharge_section(
    styles,
    discharge_result
):
    """
    Create discharge capacity results.
    """

    story = []

    story.append(
        Paragraph(
            "4. Discharge Capacity Analysis",
            styles["SectionHeading"]
        )
    )

    lithium_stats = discharge_result[
        "lithium_ion"
    ]

    lead_stats = discharge_result[
        "lead_acid"
    ]

    stats_df = pd.DataFrame(
        [
            {
                "Battery Type": "Lithium-Ion",
                "Mean (%)": lithium_stats["mean"],
                "SD": lithium_stats["std"],
                "Minimum (%)": lithium_stats["min"],
                "Maximum (%)": lithium_stats["max"],
            },

            {
                "Battery Type": "Lead-Acid",
                "Mean (%)": lead_stats["mean"],
                "SD": lead_stats["std"],
                "Minimum (%)": lead_stats["min"],
                "Maximum (%)": lead_stats["max"],
            }
        ]
    )

    story.append(
        Paragraph(
            "Discharge capacity values are presented as the "
            "percentage capacity values supplied in the dataset. "
            "The analysis therefore treats these values as "
            "percentage-based capacity measurements rather than "
            "absolute ampere-hour capacity.",
            styles["BodyResearch"]
        )
    )

    story.append(
        dataframe_to_table(
            stats_df
        )
    )

    story.append(
        Spacer(
            1,
            0.4 * cm
        )
    )

    chart_path = (
        CHART_DIR /
        "discharge_capacity.png"
    )

    if chart_path.exists():

        story.append(
            Image(
                str(chart_path),
                width=16 * cm,
                height=8.5 * cm
            )
        )

    return story


# ============================================================
# DOD SECTION
# ============================================================

def build_dod_section(
    styles,
    dod_result
):
    """
    Create depth of discharge results.
    """

    story = []

    story.append(
        Paragraph(
            "5. Depth of Discharge Analysis",
            styles["SectionHeading"]
        )
    )

    lithium_stats = dod_result[
        "lithium_ion"
    ]

    lead_stats = dod_result[
        "lead_acid"
    ]

    stats_df = pd.DataFrame(
        [
            {
                "Battery Type": "Lithium-Ion",
                "Mean (%)": lithium_stats["mean"],
                "SD": lithium_stats["std"],
                "Minimum (%)": lithium_stats["min"],
                "Maximum (%)": lithium_stats["max"],
            },

            {
                "Battery Type": "Lead-Acid",
                "Mean (%)": lead_stats["mean"],
                "SD": lead_stats["std"],
                "Minimum (%)": lead_stats["min"],
                "Maximum (%)": lead_stats["max"],
            }
        ]
    )

    story.append(
        Paragraph(
            "The depth-of-discharge dataset was examined across "
            "the supplied battery cycles. The values are reported "
            "as percentages in accordance with the supplied data.",
            styles["BodyResearch"]
        )
    )

    story.append(
        dataframe_to_table(
            stats_df
        )
    )

    story.append(
        Spacer(
            1,
            0.4 * cm
        )
    )

    chart_path = (
        CHART_DIR /
        "depth_of_discharge.png"
    )

    if chart_path.exists():

        story.append(
            Image(
                str(chart_path),
                width=16 * cm,
                height=8.5 * cm
            )
        )

    return story


# ============================================================
# COMPARISON SECTION
# ============================================================

def build_comparison_section(
    styles,
    analysis_results
):
    """
    Create the comparative results section.
    """

    story = []

    story.append(
        Paragraph(
            "6. Comparative Analysis",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "The following table summarizes the mean values "
            "obtained for the three investigated performance "
            "parameters.",
            styles["BodyResearch"]
        )
    )

    summary_df = analysis_results[
        "summary"
    ].copy()

    display_df = summary_df.copy()

    numeric_columns = [
        "Lithium-Ion",
        "Lead-Acid",
        "Difference",
        "Percentage Difference"
    ]

    for column in numeric_columns:

        if column in display_df.columns:

            display_df[column] = display_df[
                column
            ].apply(
                lambda x: format_number(
                    x,
                    2
                )
            )

    story.append(
        dataframe_to_table(
            display_df
        )
    )

    story.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    chart_path = (
        CHART_DIR /
        "comparative_performance.png"
    )

    if chart_path.exists():

        story.append(
            Image(
                str(chart_path),
                width=16 * cm,
                height=8.5 * cm
            )
        )

    story.append(
        PageBreak()
    )

    difference_path = (
        CHART_DIR /
        "performance_difference.png"
    )

    if difference_path.exists():

        story.append(
            Paragraph(
                "Comparative Difference",
                styles["SubHeading"]
            )
        )

        story.append(
            Image(
                str(difference_path),
                width=16 * cm,
                height=8.5 * cm
            )
        )

    return story


# ============================================================
# DISCUSSION
# ============================================================

def build_discussion(
    styles,
    analysis_results
):
    """
    Create a discussion based strictly on calculated results.
    """

    story = []

    story.append(
        Paragraph(
            "7. Discussion of Results",
            styles["SectionHeading"]
        )
    )

    indicators = analysis_results[
        "indicators"
    ]

    li_charge = indicators[
        "lithium_mean_charging_efficiency"
    ]

    lead_charge = indicators[
        "lead_mean_charging_efficiency"
    ]

    li_discharge = indicators[
        "lithium_mean_discharge_capacity"
    ]

    lead_discharge = indicators[
        "lead_mean_discharge_capacity"
    ]

    li_dod = indicators[
        "lithium_mean_dod"
    ]

    lead_dod = indicators[
        "lead_mean_dod"
    ]

    charge_difference = (
        li_charge -
        lead_charge
    )

    discharge_difference = (
        li_discharge -
        lead_discharge
    )

    dod_difference = (
        li_dod -
        lead_dod
    )

    story.append(
        Paragraph(
            f"The mean charging-efficiency value for the "
            f"lithium-ion battery was "
            f"<b>{format_number(li_charge)}%</b>, compared with "
            f"<b>{format_number(lead_charge)}%</b> for the "
            f"lead-acid battery. The corresponding difference "
            f"was {format_number(charge_difference)} percentage "
            f"points.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            f"For the supplied discharge-capacity observations, "
            f"the mean lithium-ion value was "
            f"<b>{format_number(li_discharge)}%</b>, while the "
            f"lead-acid value was "
            f"<b>{format_number(lead_discharge)}%</b>. The "
            f"difference between the means was "
            f"{format_number(discharge_difference)} percentage "
            f"points.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            f"The mean depth-of-discharge values were "
            f"<b>{format_number(li_dod)}%</b> for lithium-ion "
            f"and <b>{format_number(lead_dod)}%</b> for "
            f"lead-acid, giving a difference of "
            f"{format_number(dod_difference)} percentage "
            f"points.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            "<b>Interpretation note:</b> A higher depth of "
            "discharge is not automatically equivalent to "
            "better overall battery performance. Depth of "
            "discharge should be interpreted together with "
            "battery life, cycle life, operating conditions "
            "and the specific experimental procedure.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            "The numerical conclusions in this report are "
            "limited to the supplied dataset. They should not "
            "be presented as measured field performance unless "
            "the supplied values correspond to the actual "
            "experimental measurements obtained by the researcher.",
            styles["BodyResearch"]
        )
    )

    return story


# ============================================================
# CONCLUSION
# ============================================================

def build_conclusion(
    styles,
    analysis_results
):
    """
    Create a data-based conclusion.
    """

    story = []

    story.append(
        Paragraph(
            "8. Conclusion",
            styles["SectionHeading"]
        )
    )

    indicators = analysis_results[
        "indicators"
    ]

    li_charge = indicators[
        "lithium_mean_charging_efficiency"
    ]

    lead_charge = indicators[
        "lead_mean_charging_efficiency"
    ]

    li_discharge = indicators[
        "lithium_mean_discharge_capacity"
    ]

    lead_discharge = indicators[
        "lead_mean_discharge_capacity"
    ]

    story.append(
        Paragraph(
            f"Based on the supplied dataset, the lithium-ion "
            f"battery recorded a mean charging-efficiency value "
            f"of {format_number(li_charge)}%, while the "
            f"lead-acid battery recorded {format_number(lead_charge)}%.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            f"The mean discharge-capacity values were "
            f"{format_number(li_discharge)}% for lithium-ion "
            f"and {format_number(lead_discharge)}% for "
            f"lead-acid under the supplied observations.",
            styles["BodyResearch"]
        )
    )

    story.append(
        Paragraph(
            "The analysis therefore provides a quantitative "
            "basis for comparing the two battery technologies "
            "using the selected performance indicators. "
            "However, final engineering conclusions should "
            "consider the actual experimental conditions, "
            "battery specifications and measurement procedures "
            "used during the research.",
            styles["BodyResearch"]
        )
    )

    return story


# ============================================================
# REPORT METADATA
# ============================================================

def build_cover_page(
    styles,
    data_source_label="Supplied Project Dataset"
):
    """
    Create the report cover page.
    """

    story = []

    story.append(
        Spacer(
            1,
            3 * cm
        )
    )

    story.append(
        Paragraph(
            "BATTERY COMPARISON ANALYSIS SYSTEM",
            styles["SectionHeading"]
        )
    )

    story.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    story.append(
        Paragraph(
            PROJECT_TITLE,
            styles["ProjectTitle"]
        )
    )

    story.append(
        Spacer(
            1,
            1 * cm
        )
    )

    story.append(
        Paragraph(
            "<b>Study Location:</b><br/>"
            "FUT Minna Engineering Complex",
            styles["CenterText"]
        )
    )

    story.append(
        Spacer(
            1,
            0.7 * cm
        )
    )

    story.append(
        Paragraph(
            f"<b>Data Source:</b><br/>{data_source_label}",
            styles["CenterText"]
        )
    )

    story.append(
        Spacer(
            1,
            0.7 * cm
        )
    )

    story.append(
        Paragraph(
            f"<b>Report Generated:</b><br/>"
            f"{datetime.now().strftime('%d %B %Y, %H:%M')}",
            styles["CenterText"]
        )
    )

    story.append(
        Spacer(
            1,
            2 * cm
        )
    )

    story.append(
        Paragraph(
            "Automated Analytical Report",
            styles["CenterText"]
        )
    )

    story.append(
        PageBreak()
    )

    return story


# ============================================================
# MAIN REPORT FUNCTION
# ============================================================

def generate_report(
    analysis_results,
    output_path=None,
    data_source_label="Supplied Project Dataset"
):
    """
    Generate the complete PDF report.

    Parameters
    ----------
    analysis_results : dict
        Results returned by run_complete_analysis().

    output_path : str or Path, optional
        Destination of generated PDF.

    data_source_label : str
        Label identifying the dataset.

    Returns
    -------
    Path
        Generated report path.
    """

    if output_path is None:

        output_path = (
            DEFAULT_REPORT_PATH
        )

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    styles = create_report_styles()

    story = []

    # --------------------------------------------------------
    # Cover
    # --------------------------------------------------------

    story.extend(
        build_cover_page(
            styles,
            data_source_label
        )
    )

    # --------------------------------------------------------
    # Introduction
    # --------------------------------------------------------

    story.extend(
        build_introduction(
            styles
        )
    )

    # --------------------------------------------------------
    # Methodology
    # --------------------------------------------------------

    story.extend(
        build_methodology(
            styles
        )
    )

    # --------------------------------------------------------
    # Key indicators
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Key Performance Indicators",
            styles["SubHeading"]
        )
    )

    story.append(
        create_kpi_table(
            analysis_results[
                "indicators"
            ]
        )
    )

    story.append(
        Spacer(
            1,
            0.6 * cm
        )
    )

    # --------------------------------------------------------
    # Charging
    # --------------------------------------------------------

    story.extend(
        build_charging_section(
            styles,
            analysis_results[
                "charging"
            ]
        )
    )

    story.append(
        PageBreak()
    )

    # --------------------------------------------------------
    # Discharge
    # --------------------------------------------------------

    story.extend(
        build_discharge_section(
            styles,
            analysis_results[
                "discharge"
            ]
        )
    )

    story.append(
        PageBreak()
    )

    # --------------------------------------------------------
    # DOD
    # --------------------------------------------------------

    story.extend(
        build_dod_section(
            styles,
            analysis_results[
                "dod"
            ]
        )
    )

    story.append(
        PageBreak()
    )

    # --------------------------------------------------------
    # Comparison
    # --------------------------------------------------------

    story.extend(
        build_comparison_section(
            styles,
            analysis_results
        )
    )

    # --------------------------------------------------------
    # Discussion
    # --------------------------------------------------------

    story.extend(
        build_discussion(
            styles,
            analysis_results
        )
    )

    # --------------------------------------------------------
    # Conclusion
    # --------------------------------------------------------

    story.extend(
        build_conclusion(
            styles,
            analysis_results
        )
    )

    # --------------------------------------------------------
    # Build PDF
    # --------------------------------------------------------

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.7 * cm,
        title=PROJECT_TITLE,
        author="Battery Comparison Analysis System",
    )

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return output_path


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("BATTERY COMPARISON SYSTEM")
    print("REPORT GENERATOR MODULE")
    print("=" * 65)

    print()
    print("Report output directory:")
    print(REPORT_DIR)

    print()
    print(
        "Default report:"
    )

    print(
        DEFAULT_REPORT_PATH
    )

    print()
    print(
        "Report generator module loaded successfully."
    )

    print()
    print(
        "The PDF will be generated automatically when "
        "generate_report() is called by the main application."
    )

    print("=" * 65)