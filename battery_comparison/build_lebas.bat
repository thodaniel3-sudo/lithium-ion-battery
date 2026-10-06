

@echo off
echo ============================================================
echo LEBAS - Building Standalone Executable
echo ============================================================
echo.

cd /d "%~dp0"

echo Step 1: Installing required packages...
echo ----------------------------------------
pip install pyinstaller pandas numpy matplotlib openpyxl reportlab scipy pillow

echo.
echo Step 2: Building executable...
echo ----------------------------------------
pyinstaller --onefile --name LEBAS --add-data "dataset.csv;." --add-data "config.py;." --add-data "calculations;calculations" --add-data "ui;ui" --add-data "charts;charts" --add-data "services;services" --add-data "assets;assets" --add-data "reports;reports" --add-data "exports;exports" --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import tkinter.messagebox --hidden-import tkinter.filedialog --hidden-import tkinter.simpledialog --hidden-import pandas --hidden-import numpy --hidden-import matplotlib --hidden-import matplotlib.backends.backend_tkagg --hidden-import matplotlib.figure --hidden-import matplotlib.pyplot --hidden-import openpyxl --hidden-import reportlab --hidden-import scipy --hidden-import scipy.stats --collect-all matplotlib --collect-all numpy --collect-all pandas main.py

echo.
if exist "dist\LEBAS.exe" (
    echo Step 3: Copying executable to root folder...
    echo ----------------------------------------
    copy "dist\LEBAS.exe" "LEBAS.exe"
    echo.
    echo ============================================================
    echo BUILD SUCCESSFUL!
    echo ============================================================
    echo.
    echo Your executable is at: %CD%\LEBAS.exe
    echo File size: 
    dir "LEBAS.exe" | find "LEBAS.exe"
    echo.
    echo You can now run LEBAS.exe by double-clicking it.
    echo First run may take 10-20 seconds to start.
) else (
    echo.
    echo ============================================================
    echo BUILD FAILED!
    echo ============================================================
    echo The executable was not created. Check the error messages above.
)

echo.
pause