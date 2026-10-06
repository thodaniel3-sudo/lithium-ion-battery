"""
BATTERY COMPARISON ANALYSIS SYSTEM

Project:
Comparative Analysis of the Performance of Lithium-Ion
and Lead-Acid Batteries for a Solar System in
FUT Minna Engineering Complex

Main Application

This application connects:

    CSV Data
        ↓
    Data Loading
        ↓
    Statistical Analysis
        ↓
    Interactive Dashboard
        ↓
    Charts
        ↓
    PDF Report

IMPORTANT:
The application does not invent experimental data.
All numerical values are obtained from the CSV files
inside the data folder.
"""

# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.data_loader import load_all_data
from src.analysis import run_complete_analysis

from src.visualization import (
    plot_discharge_capacity,
    plot_charging_efficiency,
    plot_depth_of_discharge,
    plot_comparative_performance,
)

from src.report_generator import generate_report


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "outputs"

CHART_DIR = OUTPUT_DIR / "charts"

REPORT_PATH = OUTPUT_DIR / "battery_comparison_report.pdf"


# ============================================================
# APPLICATION INFORMATION
# ============================================================

APP_TITLE = "Battery Comparison Analysis System"

PROJECT_TITLE = (
    "Comparative Analysis of the Performance of "
    "Lithium-Ion and Lead-Acid Batteries for a Solar "
    "System in FUT Minna Engineering Complex"
)


# ============================================================
# COLOUR PALETTE
# ============================================================

BG_COLOR = "#F4F7F5"
SIDEBAR_COLOR = "#12372A"
SIDEBAR_HOVER = "#1B4D3E"

PRIMARY_COLOR = "#176B4D"
PRIMARY_DARK = "#0F4A35"

CARD_COLOR = "#FFFFFF"

TEXT_COLOR = "#1C2B25"
SECONDARY_TEXT = "#68756F"

BORDER_COLOR = "#DDE5E0"

SUCCESS_COLOR = "#238636"
WARNING_COLOR = "#B7791F"
DANGER_COLOR = "#C0392B"

WHITE = "#FFFFFF"


# ============================================================
# MAIN APPLICATION CLASS
# ============================================================

class BatteryComparisonApp(tk.Tk):
    """
    Main graphical user interface for the battery comparison
    analysis system.
    """

    def __init__(self):

        super().__init__()

        # ----------------------------------------------------
        # WINDOW CONFIGURATION
        # ----------------------------------------------------

        self.title(APP_TITLE)

        self.geometry("1400x850")

        self.minsize(
            1100,
            700
        )

        self.configure(
            bg=BG_COLOR
        )

        # ----------------------------------------------------
        # APPLICATION STATE
        # ----------------------------------------------------

        self.data = None

        self.analysis = None

        self.current_page = "dashboard"

        self.current_figure = None

        self.current_canvas = None

        # ----------------------------------------------------
        # CREATE OUTPUT DIRECTORIES
        # ----------------------------------------------------

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        CHART_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------
        # CONFIGURE TKINTER STYLES
        # ----------------------------------------------------

        self.configure_styles()

        # ----------------------------------------------------
        # BUILD APPLICATION
        # ----------------------------------------------------

        self.create_layout()

        # ----------------------------------------------------
        # LOAD DATA
        # ----------------------------------------------------

        self.load_application_data()

    # ========================================================
    # STYLE CONFIGURATION
    # ========================================================

    def configure_styles(self):

        style = ttk.Style(
            self
        )

        try:
            style.theme_use(
                "clam"
            )
        except tk.TclError:
            pass

        # ----------------------------------------------------
        # General frame
        # ----------------------------------------------------

        style.configure(
            "App.TFrame",
            background=BG_COLOR
        )

        style.configure(
            "Card.TFrame",
            background=CARD_COLOR
        )

        # ----------------------------------------------------
        # Labels
        # ----------------------------------------------------

        style.configure(
            "Title.TLabel",
            background=BG_COLOR,
            foreground=TEXT_COLOR,
            font=(
                "Segoe UI",
                20,
                "bold"
            )
        )

        style.configure(
            "Subtitle.TLabel",
            background=BG_COLOR,
            foreground=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                10
            )
        )

        style.configure(
            "CardTitle.TLabel",
            background=CARD_COLOR,
            foreground=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        )

        style.configure(
            "CardValue.TLabel",
            background=CARD_COLOR,
            foreground=TEXT_COLOR,
            font=(
                "Segoe UI",
                22,
                "bold"
            )
        )

        style.configure(
            "Section.TLabel",
            background=BG_COLOR,
            foreground=TEXT_COLOR,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        )

        style.configure(
            "Body.TLabel",
            background=BG_COLOR,
            foreground=TEXT_COLOR,
            font=(
                "Segoe UI",
                10
            )
        )

        # ----------------------------------------------------
        # Treeview
        # ----------------------------------------------------

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT_COLOR,
            fieldbackground=WHITE,
            rowheight=32,
            font=(
                "Segoe UI",
                9
            )
        )

        style.configure(
            "Treeview.Heading",
            background=SIDEBAR_COLOR,
            foreground=WHITE,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            padding=8
        )

        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    "#DCEDE5"
                )
            ],
            foreground=[
                (
                    "selected",
                    TEXT_COLOR
                )
            ]
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        style.configure(
            "Primary.TButton",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            padding=10
        )

        style.configure(
            "Secondary.TButton",
            font=(
                "Segoe UI",
                9
            ),
            padding=8
        )

    # ========================================================
    # APPLICATION LAYOUT
    # ========================================================

    def create_layout(self):

        # ----------------------------------------------------
        # Main container
        # ----------------------------------------------------

        self.main_container = tk.Frame(
            self,
            bg=BG_COLOR
        )

        self.main_container.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------

        self.sidebar = tk.Frame(
            self.main_container,
            bg=SIDEBAR_COLOR,
            width=245
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )

        # ----------------------------------------------------
        # Content area
        # ----------------------------------------------------

        self.content_area = tk.Frame(
            self.main_container,
            bg=BG_COLOR
        )

        self.content_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()

        self.create_header()

        self.page_container = tk.Frame(
            self.content_area,
            bg=BG_COLOR
        )

        self.page_container.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 25)
        )

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        # ----------------------------------------------------
        # Logo / brand
        # ----------------------------------------------------

        brand_frame = tk.Frame(
            self.sidebar,
            bg=SIDEBAR_COLOR
        )

        brand_frame.pack(
            fill="x",
            padx=22,
            pady=(28, 35)
        )

        logo = tk.Label(
            brand_frame,
            text="BC",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            width=3,
            height=1
        )

        logo.pack(
            side="left",
            padx=(0, 12)
        )

        brand_text = tk.Frame(
            brand_frame,
            bg=SIDEBAR_COLOR
        )

        brand_text.pack(
            side="left"
        )

        tk.Label(
            brand_text,
            text="BATTERY",
            bg=SIDEBAR_COLOR,
            fg=WHITE,
            font=(
                "Segoe UI",
                12,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            brand_text,
            text="COMPARISON",
            bg=SIDEBAR_COLOR,
            fg="#AFC8BC",
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # Navigation title
        # ----------------------------------------------------

        tk.Label(
            self.sidebar,
            text="ANALYSIS",
            bg=SIDEBAR_COLOR,
            fg="#8EAA9E",
            font=(
                "Segoe UI",
                8,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        # ----------------------------------------------------
        # Navigation buttons
        # ----------------------------------------------------

        self.nav_buttons = {}

        navigation = [
            (
                "dashboard",
                "⌂",
                "Dashboard"
            ),

            (
                "charging",
                "⚡",
                "Charging Efficiency"
            ),

            (
                "discharge",
                "↘",
                "Discharge Capacity"
            ),

            (
                "dod",
                "◈",
                "Depth of Discharge"
            ),

            (
                "comparison",
                "⇄",
                "Comparison"
            ),

            (
                "data",
                "▦",
                "Data Explorer"
            ),

            (
                "report",
                "▤",
                "Reports"
            ),
        ]

        for page_id, icon, label in navigation:

            button = tk.Button(
                self.sidebar,
                text=f"  {icon}   {label}",
                bg=SIDEBAR_COLOR,
                fg="#D9E7E0",
                activebackground=SIDEBAR_HOVER,
                activeforeground=WHITE,
                bd=0,
                relief="flat",
                anchor="w",
                font=(
                    "Segoe UI",
                    10
                ),
                padx=18,
                pady=13,
                cursor="hand2",
                command=lambda p=page_id: self.show_page(p)
            )

            button.pack(
                fill="x",
                padx=12,
                pady=2
            )

            self.nav_buttons[
                page_id
            ] = button

        # ----------------------------------------------------
        # Bottom status
        # ----------------------------------------------------

        bottom = tk.Frame(
            self.sidebar,
            bg=SIDEBAR_COLOR
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=22,
            pady=22
        )

        tk.Frame(
            bottom,
            bg="#2B5949",
            height=1
        ).pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            bottom,
            text="●  SYSTEM READY",
            bg=SIDEBAR_COLOR,
            fg="#78C69E",
            font=(
                "Segoe UI",
                8,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            bottom,
            text="FUT Minna Engineering Complex",
            bg=SIDEBAR_COLOR,
            fg="#8EAA9E",
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.content_area,
            bg=BG_COLOR,
            height=82
        )

        header.pack(
            fill="x",
            padx=28,
            pady=(20, 0)
        )

        header.pack_propagate(
            False
        )

        left = tk.Frame(
            header,
            bg=BG_COLOR
        )

        left.pack(
            side="left",
            fill="y"
        )

        self.page_title = tk.Label(
            left,
            text="Battery Performance Dashboard",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(
                "Segoe UI",
                20,
                "bold"
            )
        )

        self.page_title.pack(
            anchor="w"
        )

        self.page_subtitle = tk.Label(
            left,
            text="Comparative analysis of lithium-ion and lead-acid batteries",
            bg=BG_COLOR,
            fg=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                9
            )
        )

        self.page_subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

        right = tk.Frame(
            header,
            bg=BG_COLOR
        )

        right.pack(
            side="right",
            fill="y"
        )

        tk.Button(
            right,
            text="↻  Refresh Data",
            bg=WHITE,
            fg=TEXT_COLOR,
            activebackground="#EAF1ED",
            bd=1,
            relief="solid",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.refresh_data
        ).pack(
            side="left",
            padx=(0, 8),
            pady=10
        )

        tk.Button(
            right,
            text="▤  Generate Report",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            activebackground=PRIMARY_DARK,
            activeforeground=WHITE,
            bd=0,
            relief="flat",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            padx=14,
            pady=9,
            cursor="hand2",
            command=self.generate_pdf_report
        ).pack(
            side="left",
            pady=10
        )

    # ========================================================
    # LOAD APPLICATION DATA
    # ========================================================

    def load_application_data(self):

        try:

            self.data = load_all_data()

            self.analysis = run_complete_analysis(
                self.data
            )

            self.show_page(
                "dashboard"
            )

        except Exception as error:

            messagebox.showerror(
                "Data Loading Error",
                "The application could not load the project data.\n\n"
                f"{error}"
            )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_data(self):

        try:

            self.data = load_all_data()

            self.analysis = run_complete_analysis(
                self.data
            )

            self.show_page(
                self.current_page
            )

            messagebox.showinfo(
                "Data Refreshed",
                "The battery datasets have been reloaded successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Refresh Error",
                str(error)
            )

    # ========================================================
    # PAGE MANAGEMENT
    # ========================================================

    def clear_page(self):

        for widget in self.page_container.winfo_children():

            widget.destroy()

        if self.current_canvas is not None:

            try:
                self.current_canvas.get_tk_widget().destroy()
            except Exception:
                pass

            self.current_canvas = None

        self.current_figure = None

    # ========================================================
    # SHOW PAGE
    # ========================================================

    def show_page(
        self,
        page
    ):

        if self.analysis is None:
            return

        self.current_page = page

        self.clear_page()

        # ----------------------------------------------------
        # Navigation state
        # ----------------------------------------------------

        for page_id, button in self.nav_buttons.items():

            if page_id == page:

                button.configure(
                    bg=PRIMARY_COLOR,
                    fg=WHITE
                )

            else:

                button.configure(
                    bg=SIDEBAR_COLOR,
                    fg="#D9E7E0"
                )

        # ----------------------------------------------------
        # Page titles
        # ----------------------------------------------------

        titles = {

            "dashboard": (
                "Battery Performance Dashboard",
                "Overview of the supplied battery performance data"
            ),

            "charging": (
                "Charging Efficiency",
                "Analysis of charging efficiency over time"
            ),

            "discharge": (
                "Discharge Capacity",
                "Comparison of capacity retention during discharge"
            ),

            "dod": (
                "Depth of Discharge",
                "Cycle-based depth of discharge comparison"
            ),

            "comparison": (
                "Performance Comparison",
                "Comparative summary of the three performance indicators"
            ),

            "data": (
                "Data Explorer",
                "Inspect the datasets currently being analyzed"
            ),

            "report": (
                "Reports",
                "Generate and manage the analytical PDF report"
            ),
        }

        title, subtitle = titles.get(
            page,
            titles["dashboard"]
        )

        self.page_title.configure(
            text=title
        )

        self.page_subtitle.configure(
            text=subtitle
        )

        # ----------------------------------------------------
        # Display selected page
        # ----------------------------------------------------

        if page == "dashboard":

            self.build_dashboard()

        elif page == "charging":

            self.build_charging_page()

        elif page == "discharge":

            self.build_discharge_page()

        elif page == "dod":

            self.build_dod_page()

        elif page == "comparison":

            self.build_comparison_page()

        elif page == "data":

            self.build_data_page()

        elif page == "report":

            self.build_report_page()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def build_dashboard(self):

        indicators = self.analysis[
            "indicators"
        ]

        # ----------------------------------------------------
        # KPI area
        # ----------------------------------------------------

        kpi_frame = tk.Frame(
            self.page_container,
            bg=BG_COLOR
        )

        kpi_frame.pack(
            fill="x",
            pady=(5, 18)
        )

        kpis = [

            (
                "DATA POINTS",
                str(
                    len(
                        self.data["charging"]
                    )
                ),
                "records in charging dataset"
            ),

            (
                "LI-ION CHARGING",
                f"{indicators['lithium_mean_charging_efficiency']:.2f}%",
                "mean charging efficiency"
            ),

            (
                "LEAD-ACID CHARGING",
                f"{indicators['lead_mean_charging_efficiency']:.2f}%",
                "mean charging efficiency"
            ),

            (
                "CAPACITY ADVANTAGE",
                f"{indicators['lithium_mean_discharge_capacity'] - indicators['lead_mean_discharge_capacity']:.2f}",
                "percentage-point difference"
            ),
        ]

        for index, (
            title,
            value,
            description
        ) in enumerate(kpis):

            kpi_frame.columnconfigure(
                index,
                weight=1
            )

            card = tk.Frame(
                kpi_frame,
                bg=CARD_COLOR,
                highlightbackground=BORDER_COLOR,
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=6
            )

            tk.Label(
                card,
                text=title,
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT,
                font=(
                    "Segoe UI",
                    8,
                    "bold"
                )
            ).pack(
                anchor="w",
                padx=18,
                pady=(16, 3)
            )

            tk.Label(
                card,
                text=value,
                bg=CARD_COLOR,
                fg=TEXT_COLOR,
                font=(
                    "Segoe UI",
                    20,
                    "bold"
                )
            ).pack(
                anchor="w",
                padx=18
            )

            tk.Label(
                card,
                text=description,
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT,
                font=(
                    "Segoe UI",
                    8
                )
            ).pack(
                anchor="w",
                padx=18,
                pady=(2, 16)
            )

        # ----------------------------------------------------
        # Chart area
        # ----------------------------------------------------

        chart_card = tk.Frame(
            self.page_container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        chart_card.pack(
            fill="both",
            expand=True
        )

        chart_header = tk.Frame(
            chart_card,
            bg=CARD_COLOR
        )

        chart_header.pack(
            fill="x",
            padx=20,
            pady=(16, 8)
        )

        tk.Label(
            chart_header,
            text="Performance Overview",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            side="left"
        )

        tk.Label(
            chart_header,
            text="Mean performance indicators",
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            side="right"
        )

        summary = self.analysis[
            "summary"
        ].copy()

        self.display_matplotlib_chart(
            chart_card,
            plot_comparative_performance,
            summary,
            padx=15,
            pady=(0, 15)
        )

    # ========================================================
    # CHARGING PAGE
    # ========================================================

    def build_charging_page(self):

        result = self.analysis[
            "charging"
        ]

        self.build_analysis_page(
            title="Charging Efficiency Analysis",
            description=(
                "Comparison of charging-efficiency values "
                "recorded over time."
            ),
            dataframe=self.data[
                "charging"
            ],
            chart_function=plot_charging_efficiency,
            stats=result
        )

    # ========================================================
    # DISCHARGE PAGE
    # ========================================================

    def build_discharge_page(self):

        result = self.analysis[
            "discharge"
        ]

        self.build_analysis_page(
            title="Discharge Capacity Analysis",
            description=(
                "Comparison of remaining battery capacity "
                "during discharge."
            ),
            dataframe=self.data[
                "discharge"
            ],
            chart_function=plot_discharge_capacity,
            stats=result
        )

    # ========================================================
    # DOD PAGE
    # ========================================================

    def build_dod_page(self):

        result = self.analysis[
            "dod"
        ]

        self.build_analysis_page(
            title="Depth of Discharge Analysis",
            description=(
                "Comparison of depth of discharge across "
                "the supplied battery cycles."
            ),
            dataframe=self.data[
                "dod"
            ],
            chart_function=plot_depth_of_discharge,
            stats=result
        )

    # ========================================================
    # GENERIC ANALYSIS PAGE
    # ========================================================

    def build_analysis_page(
        self,
        title,
        description,
        dataframe,
        chart_function,
        stats
    ):

        # ----------------------------------------------------
        # Main split
        # ----------------------------------------------------

        top = tk.Frame(
            self.page_container,
            bg=BG_COLOR
        )

        top.pack(
            fill="x",
            pady=(5, 12)
        )

        tk.Label(
            top,
            text=title,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            top,
            text=description,
            bg=BG_COLOR,
            fg=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ----------------------------------------------------
        # Chart
        # ----------------------------------------------------

        chart_card = tk.Frame(
            self.page_container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        chart_card.pack(
            fill="both",
            expand=True,
            pady=(0, 12)
        )

        self.display_matplotlib_chart(
            chart_card,
            chart_function,
            dataframe,
            padx=15,
            pady=10
        )

        # ----------------------------------------------------
        # Statistics card
        # ----------------------------------------------------

        stats_card = tk.Frame(
            self.page_container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        stats_card.pack(
            fill="x"
        )

        tk.Label(
            stats_card,
            text="Statistical Summary",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=(
                "Segoe UI",
                11,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(12, 8)
        )

        self.create_statistics_table(
            stats_card,
            stats
        )

    # ========================================================
    # STATISTICS TABLE
    # ========================================================

    def create_statistics_table(
        self,
        parent,
        stats
    ):

        columns = [
            "Battery",
            "Mean",
            "Std. Dev.",
            "Minimum",
            "Maximum",
            "Range",
            "CV (%)"
        ]

        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=2
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                anchor="center",
                width=120
            )

        tree.column(
            "Battery",
            width=150
        )

        for battery_name, key in [
            (
                "Lithium-Ion",
                "lithium_ion"
            ),
            (
                "Lead-Acid",
                "lead_acid"
            )
        ]:

            values = stats[
                key
            ]

            tree.insert(
                "",
                "end",
                values=[
                    battery_name,
                    f"{values['mean']:.2f}",
                    f"{values['std']:.2f}",
                    f"{values['min']:.2f}",
                    f"{values['max']:.2f}",
                    f"{values['range']:.2f}",
                    f"{values['cv']:.2f}",
                ]
            )

        tree.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

    # ========================================================
    # COMPARISON PAGE
    # ========================================================

    def build_comparison_page(self):

        summary = self.analysis[
            "summary"
        ].copy()

        indicators = self.analysis[
            "indicators"
        ]

        # ----------------------------------------------------
        # Summary cards
        # ----------------------------------------------------

        cards = tk.Frame(
            self.page_container,
            bg=BG_COLOR
        )

        cards.pack(
            fill="x",
            pady=(5, 15)
        )

        comparisons = [

            (
                "CHARGING",
                indicators[
                    "lithium_mean_charging_efficiency"
                ] -
                indicators[
                    "lead_mean_charging_efficiency"
                ]
            ),

            (
                "DISCHARGE CAPACITY",
                indicators[
                    "lithium_mean_discharge_capacity"
                ] -
                indicators[
                    "lead_mean_discharge_capacity"
                ]
            ),

            (
                "DEPTH OF DISCHARGE",
                indicators[
                    "lithium_mean_dod"
                ] -
                indicators[
                    "lead_mean_dod"
                ]
            )
        ]

        for index, (
            label,
            difference
        ) in enumerate(comparisons):

            cards.columnconfigure(
                index,
                weight=1
            )

            card = tk.Frame(
                cards,
                bg=CARD_COLOR,
                highlightbackground=BORDER_COLOR,
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=6
            )

            tk.Label(
                card,
                text=label,
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT,
                font=(
                    "Segoe UI",
                    8,
                    "bold"
                )
            ).pack(
                anchor="w",
                padx=18,
                pady=(15, 3)
            )

            sign = "+" if difference >= 0 else ""

            tk.Label(
                card,
                text=f"{sign}{difference:.2f}",
                bg=CARD_COLOR,
                fg=(
                    SUCCESS_COLOR
                    if difference >= 0
                    else DANGER_COLOR
                ),
                font=(
                    "Segoe UI",
                    21,
                    "bold"
                )
            ).pack(
                anchor="w",
                padx=18
            )

            tk.Label(
                card,
                text="Li-ion minus lead-acid",
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT,
                font=(
                    "Segoe UI",
                    8
                )
            ).pack(
                anchor="w",
                padx=18,
                pady=(0, 15)
            )

        # ----------------------------------------------------
        # Table
        # ----------------------------------------------------

        table_card = tk.Frame(
            self.page_container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        table_card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            table_card,
            text="Comparative Results",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=(
                "Segoe UI",
                12,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 10)
        )

        self.create_comparison_table(
            table_card,
            summary
        )

        # ----------------------------------------------------
        # Chart
        # ----------------------------------------------------

        chart_card = tk.Frame(
            self.page_container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        chart_card.pack(
            fill="both",
            expand=True
        )

        self.display_matplotlib_chart(
            chart_card,
            plot_comparative_performance,
            summary,
            padx=15,
            pady=10
        )

    # ========================================================
    # COMPARISON TABLE
    # ========================================================

    def create_comparison_table(
        self,
        parent,
        summary
    ):

        columns = list(
            summary.columns
        )

        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=4
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                anchor="center",
                width=150
            )

        for _, row in summary.iterrows():

            values = []

            for value in row:

                if isinstance(
                    value,
                    (int, float)
                ):

                    values.append(
                        f"{value:.2f}"
                    )

                else:

                    values.append(
                        str(value)
                    )

            tree.insert(
                "",
                "end",
                values=values
            )

        tree.pack(
            fill="x",
            padx=18,
            pady=(0, 18)
        )

    # ========================================================
    # DATA EXPLORER
    # ========================================================

    def build_data_page(self):

        notebook = ttk.Notebook(
            self.page_container
        )

        notebook.pack(
            fill="both",
            expand=True,
            pady=5
        )

        datasets = [
            (
                "Charging Efficiency",
                self.data[
                    "charging"
                ]
            ),

            (
                "Discharge Capacity",
                self.data[
                    "discharge"
                ]
            ),

            (
                "Depth of Discharge",
                self.data[
                    "dod"
                ]
            )
        ]

        for title, dataframe in datasets:

            frame = tk.Frame(
                notebook,
                bg=CARD_COLOR
            )

            notebook.add(
                frame,
                text=title
            )

            self.create_data_table(
                frame,
                dataframe
            )

    # ========================================================
    # DATA TABLE
    # ========================================================

    def create_data_table(
        self,
        parent,
        dataframe
    ):

        outer = tk.Frame(
            parent,
            bg=CARD_COLOR
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        columns = list(
            dataframe.columns
        )

        tree = ttk.Treeview(
            outer,
            columns=columns,
            show="headings"
        )

        vertical = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=tree.yview
        )

        horizontal = ttk.Scrollbar(
            outer,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical.set,
            xscrollcommand=horizontal.set
        )

        vertical.pack(
            side="right",
            fill="y"
        )

        horizontal.pack(
            side="bottom",
            fill="x"
        )

        tree.pack(
            fill="both",
            expand=True
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                anchor="center",
                width=180
            )

        for _, row in dataframe.iterrows():

            values = []

            for value in row:

                if pd.isna(value):

                    values.append("")

                elif isinstance(
                    value,
                    float
                ):

                    values.append(
                        f"{value:.2f}"
                    )

                else:

                    values.append(
                        str(value)
                    )

            tree.insert(
                "",
                "end",
                values=values
            )

    # ========================================================
    # REPORT PAGE
    # ========================================================

    def build_report_page(self):

        container = tk.Frame(
            self.page_container,
            bg=BG_COLOR
        )

        container.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Report card
        # ----------------------------------------------------

        card = tk.Frame(
            container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=10
        )

        tk.Label(
            card,
            text="Analytical Report",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=(
                "Segoe UI",
                16,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            card,
            text=PROJECT_TITLE,
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                9
            ),
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        status_frame = tk.Frame(
            card,
            bg="#F1F6F3"
        )

        status_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        tk.Label(
            status_frame,
            text="PDF REPORT",
            bg="#F1F6F3",
            fg=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                8,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        tk.Label(
            status_frame,
            text=str(REPORT_PATH),
            bg="#F1F6F3",
            fg=TEXT_COLOR,
            font=(
                "Consolas",
                9
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        # ----------------------------------------------------
        # Generate button
        # ----------------------------------------------------

        tk.Button(
            card,
            text="▤  Generate PDF Report",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            activebackground=PRIMARY_DARK,
            activeforeground=WHITE,
            bd=0,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.generate_pdf_report
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

        # ----------------------------------------------------
        # Report contents
        # ----------------------------------------------------

        contents = tk.Frame(
            container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        contents.pack(
            fill="both",
            expand=True,
            pady=(5, 0)
        )

        tk.Label(
            contents,
            text="Report Contents",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=(
                "Segoe UI",
                12,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 12)
        )

        report_items = [
            "Project title and study location",
            "Introduction and analytical methodology",
            "Key performance indicators",
            "Charging efficiency analysis",
            "Discharge capacity analysis",
            "Depth of discharge analysis",
            "Comparative performance table",
            "Performance charts",
            "Discussion of calculated results",
            "Data-based conclusion",
        ]

        for item in report_items:

            tk.Label(
                contents,
                text=f"✓  {item}",
                bg=CARD_COLOR,
                fg=TEXT_COLOR,
                font=(
                    "Segoe UI",
                    9
                )
            ).pack(
                anchor="w",
                padx=30,
                pady=4
            )

    # ========================================================
    # MATPLOTLIB EMBEDDING
    # ========================================================

    def display_matplotlib_chart(
        self,
        parent,
        chart_function,
        dataframe,
        padx=10,
        pady=10
    ):

        try:

            figure = chart_function(
                dataframe,
                save=False
            )

            self.current_figure = figure

            canvas = FigureCanvasTkAgg(
                figure,
                master=parent
            )

            canvas.draw()

            widget = canvas.get_tk_widget()

            widget.pack(
                fill="both",
                expand=True,
                padx=padx,
                pady=pady
            )

            self.current_canvas = canvas

        except Exception as error:

            error_label = tk.Label(
                parent,
                text=(
                    "Unable to display chart.\n\n"
                    f"{error}"
                ),
                bg=CARD_COLOR,
                fg=DANGER_COLOR,
                font=(
                    "Segoe UI",
                    10
                )
            )

            error_label.pack(
                expand=True
            )

    # ========================================================
    # GENERATE PDF
    # ========================================================

    def generate_pdf_report(self):

        if self.analysis is None:

            messagebox.showwarning(
                "No Analysis",
                "There is no analysis data available yet."
            )

            return

        try:

            # ------------------------------------------------
            # Generate charts required by report
            # ------------------------------------------------

            from src.visualization import (
                generate_all_charts
            )

            generate_all_charts(
                self.analysis
            )

            # ------------------------------------------------
            # Generate PDF
            # ------------------------------------------------

            report = generate_report(
                self.analysis,
                output_path=REPORT_PATH,
                data_source_label=(
                    "Project CSV Dataset"
                )
            )

            messagebox.showinfo(
                "Report Generated",
                "The analytical PDF report was generated successfully.\n\n"
                f"Location:\n{report}"
            )

            self.show_page(
                "report"
            )

        except Exception as error:

            messagebox.showerror(
                "Report Generation Error",
                "The report could not be generated.\n\n"
                f"{error}"
            )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():

    app = BatteryComparisonApp()

    app.mainloop()


if __name__ == "__main__":

    main()