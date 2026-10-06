@echo off
title PV Soiling Analyzer - Build EXE
color 0A

echo ============================================================
echo   PV SOILING ANALYZER - BUILD EXE
echo   Federal University of Technology, Minna
echo ============================================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python.
    pause
    exit /b 1
)
echo ✅ Python OK
echo.

echo [2/4] Installing PyInstaller...
python -m pip install pyinstaller --quiet
echo ✅ PyInstaller installed
echo.

echo [3/4] Building EXE...
echo This may take 3-5 minutes...
echo.

python -m PyInstaller --onefile --windowed --name PVSoilingAnalyzer --add-data "data;data" --add-data "reports;reports" --hidden-import PyQt5 --hidden-import PyQt5.QtWidgets --hidden-import PyQt5.QtCore --hidden-import PyQt5.QtGui --hidden-import matplotlib --hidden-import matplotlib.backends.backend_qt5agg --hidden-import pandas --hidden-import numpy --hidden-import sqlalchemy --hidden-import reportlab --hidden-import reportlab.platypus --hidden-import openpyxl --hidden-import plotly --hidden-import seaborn --hidden-import core --hidden-import database --hidden-import ui --hidden-import visualization --hidden-import reports --collect-all matplotlib --collect-all pyqt5 --exclude-module tkinter main.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Copying files...
mkdir "%USERPROFILE%\Desktop\PV_Soiling_Analyzer_App" 2>nul
copy "dist\PVSoilingAnalyzer.exe" "%USERPROFILE%\Desktop\PV_Soiling_Analyzer_App\"
xcopy "data" "%USERPROFILE%\Desktop\PV_Soiling_Analyzer_App\data\" /E /I /Y >nul
xcopy "reports" "%USERPROFILE%\Desktop\PV_Soiling_Analyzer_App\reports\" /E /I /Y >nul

echo.
echo ============================================================
echo ✅ BUILD COMPLETE!
echo ============================================================
echo.
echo 📁 EXE Location:
echo    %USERPROFILE%\Desktop\PV_Soiling_Analyzer_App\
echo.
echo 🚀 To run:
echo    Double-click PVSoilingAnalyzer.exe
echo.
pause