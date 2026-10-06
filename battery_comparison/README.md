# Battery Comparison Analysis System

## Comparative Analysis of the Performance of Lithium-Ion and Lead-Acid Batteries for a Solar System in FUT Minna Engineering Complex

---

## 1. Project Description

The Battery Comparison Analysis System is a Python-based analytical application developed to support the comparative evaluation of lithium-ion and lead-acid batteries used in a solar-system context.

The system processes battery performance data and provides:

- Data loading and validation
- Statistical analysis
- Charging efficiency analysis
- Discharge capacity analysis
- Depth of discharge analysis
- Comparative performance analysis
- Interactive graphical visualization
- Data exploration
- Automated PDF report generation

The application is designed to provide a structured computational platform for analyzing battery-performance data obtained during the research.

---

## 2. Project Objective

The main objective of the system is to provide a reliable computational method for comparing the performance of lithium-ion and lead-acid batteries using selected performance indicators.

The investigated indicators are:

1. Charging efficiency
2. Discharge capacity
3. Depth of discharge

---

## 3. Project Structure

```text
battery_comparison/
│
├── data/
│   ├── charging_efficiency.csv
│   ├── discharge_capacity.csv
│   └── depth_of_discharge.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── analysis.py
│   ├── visualization.py
│   └── report_generator.py
│
├── outputs/
│   ├── charts/
│   └── battery_comparison_report.pdf
│
├── main.py
├── requirements.txt
└── README.md