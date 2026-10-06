"""
build_exe.py - Complete Build Script for PV Soiling Analyzer
Converts Python application to standalone EXE
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import time

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_color(text, color=Colors.RESET):
    print(f"{color}{text}{Colors.RESET}")

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print_color("✅ PyInstaller is installed", Colors.GREEN)
        return True
    except ImportError:
        print_color("❌ PyInstaller is NOT installed", Colors.RED)
        print_color("   Installing PyInstaller...", Colors.YELLOW)
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print_color("✅ PyInstaller installed successfully!", Colors.GREEN)
        return True

def clean_build():
    """Clean previous build files"""
    print_color("\n🧹 Cleaning previous builds...", Colors.YELLOW)
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print_color(f"  ✅ Removed {dir_name}/", Colors.GREEN)
    
    # Remove .spec files
    for file in Path('.').glob('*.spec'):
        file.unlink()
        print_color(f"  ✅ Removed {file.name}", Colors.GREEN)
    
    print_color("✅ Clean complete!\n", Colors.GREEN)

def get_project_files():
    """Get all Python files in the project"""
    project_files = [
        'main.py',
        'core.py', 
        'database.py',
        'ui.py',
        'visualization.py',
        'reports.py',
        'requirements.txt'
    ]
    
    missing = []
    for file in project_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print_color(f"⚠️  Missing files: {', '.join(missing)}", Colors.YELLOW)
        return False
    
    print_color("✅ All project files found", Colors.GREEN)
    return True

def build_exe():
    """Build the EXE file using PyInstaller"""
    print_color("=" * 60, Colors.CYAN)
    print_color("  BUILDING PV SOILING ANALYZER EXE", Colors.CYAN)
    print_color("=" * 60, Colors.CYAN)
    print()
    
    # Step 1: Check PyInstaller
    print_color("[1/5] Checking PyInstaller...", Colors.BLUE)
    check_pyinstaller()
    print()
    
    # Step 2: Check project files
    print_color("[2/5] Checking project files...", Colors.BLUE)
    if not get_project_files():
        print_color("❌ Missing required files. Build cancelled.", Colors.RED)
        return False
    print()
    
    # Step 3: Clean previous builds
    print_color("[3/5] Cleaning previous builds...", Colors.BLUE)
    clean_build()
    
    # Step 4: Build the EXE
    print_color("[4/5] Building EXE...", Colors.BLUE)
    print_color("   This may take 3-5 minutes. Please wait...", Colors.YELLOW)
    print()
    
    # Get absolute paths
    project_dir = Path(__file__).parent.absolute()
    data_dir = project_dir / 'data'
    reports_dir = project_dir / 'reports'
    
    # Create directories if they don't exist
    data_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    # Build command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'PVSoilingAnalyzer',
        '--add-data', f'{data_dir}{os.pathsep}data',
        '--add-data', f'{reports_dir}{os.pathsep}reports',
        '--hidden-import', 'PyQt5',
        '--hidden-import', 'PyQt5.QtWidgets',
        '--hidden-import', 'PyQt5.QtCore',
        '--hidden-import', 'PyQt5.QtGui',
        '--hidden-import', 'matplotlib',
        '--hidden-import', 'matplotlib.backends.backend_qt5agg',
        '--hidden-import', 'matplotlib.pyplot',
        '--hidden-import', 'matplotlib.figure',
        '--hidden-import', 'pandas',
        '--hidden-import', 'numpy',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'reportlab',
        '--hidden-import', 'reportlab.platypus',
        '--hidden-import', 'reportlab.lib',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'plotly',
        '--hidden-import', 'seaborn',
        '--hidden-import', 'core',
        '--hidden-import', 'database',
        '--hidden-import', 'ui',
        '--hidden-import', 'visualization',
        '--hidden-import', 'reports',
        '--collect-all', 'matplotlib',
        '--collect-all', 'pyqt5',
        '--collect-all', 'numpy',
        '--collect-data', 'matplotlib',
        '--exclude-module', 'tkinter',
        '--exclude-module', 'tcl',
        '--exclude-module', 'test',
        '--exclude-module', 'distutils',
        'main.py'
    ]
    
    # Run the build
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            print_color("\n✅ BUILD SUCCESSFUL!", Colors.GREEN)
            print_color("[5/5] Copying files...", Colors.BLUE)
            
            # Step 5: Copy to output folder
            copy_to_exe_folder()
            return True
        else:
            print_color("\n❌ Build failed!", Colors.RED)
            return False
            
    except Exception as e:
        print_color(f"\n❌ Build error: {e}", Colors.RED)
        return False

def copy_to_exe_folder():
    """Copy the EXE to a dedicated folder with supporting files"""
    try:
        # Create output folder on Desktop
        desktop = Path.home() / 'Desktop'
        exe_folder = desktop / 'PV_Soiling_Analyzer_App'
        
        # If folder exists, rename old one
        if exe_folder.exists():
            backup_folder = desktop / f'PV_Soiling_Analyzer_App_Backup_{time.strftime("%Y%m%d_%H%M%S")}'
            shutil.move(str(exe_folder), str(backup_folder))
            print_color(f"📁 Previous version backed up to: {backup_folder.name}", Colors.YELLOW)
        
        exe_folder.mkdir(exist_ok=True)
        
        # Copy EXE
        src_exe = Path('dist/PVSoilingAnalyzer.exe')
        dst_exe = exe_folder / 'PVSoilingAnalyzer.exe'
        
        if src_exe.exists():
            shutil.copy2(src_exe, dst_exe)
            print_color(f"\n📁 EXE copied to: {dst_exe}", Colors.GREEN)
            
            # Copy data and reports folders
            for folder in ['data', 'reports']:
                src_folder = Path(folder)
                dst_folder = exe_folder / folder
                if src_folder.exists():
                    if dst_folder.exists():
                        shutil.rmtree(dst_folder)
                    shutil.copytree(src_folder, dst_folder)
                    print_color(f"📁 Copied {folder}/ to app folder", Colors.GREEN)
            
            # Create README file
            create_readme(exe_folder)
            
            # Create run script
            create_run_script(exe_folder)
            
            # Create uninstall script
            create_uninstall_script(exe_folder)
            
            print_color("\n" + "=" * 60, Colors.CYAN)
            print_color("✅ APPLICATION READY FOR USE!", Colors.GREEN)
            print_color("=" * 60, Colors.CYAN)
            print_color(f"\n📍 Location: {exe_folder}", Colors.CYAN)
            print_color("\n📋 To run the application:", Colors.YELLOW)
            print_color(f"   1. Open: {exe_folder}", Colors.WHITE)
            print_color("   2. Double-click: PVSoilingAnalyzer.exe", Colors.WHITE)
            print_color("   3. Or double-click: run_app.bat", Colors.WHITE)
            print_color("\n📁 You can share this entire folder with others.", Colors.CYAN)
            print_color("   No Python installation needed!", Colors.CYAN)
            print_color("\n" + "=" * 60, Colors.CYAN)
            
            # Open the folder
            os.startfile(exe_folder)
            
        else:
            print_color("⚠️  EXE not found in dist/", Colors.RED)
            
    except Exception as e:
        print_color(f"⚠️  Error copying to folder: {e}", Colors.RED)

def create_readme(folder):
    """Create README file"""
    readme_path = folder / 'README.txt'
    with open(readme_path, 'w') as f:
        f.write("""
============================================================
  PV SOILING ANALYZER - STANDALONE APPLICATION
  Federal University of Technology, Minna
  Department of Materials and Metallurgical Engineering
============================================================

📁 LOCATION: This folder contains the standalone EXE

📄 FILES:
  - PVSoilingAnalyzer.exe  (Main application)
  - data/                  (Database folder)
  - reports/               (Generated reports)
  - run_app.bat            (Quick launch script)
  - README.txt             (This file)

🚀 HOW TO RUN:
  Double-click PVSoilingAnalyzer.exe

  OR

  Double-click run_app.bat

📋 FEATURES:
  ✓ Machine Design Calculations
  ✓ Experiment Management
  ✓ Results Tracking
  ✓ PDF/Excel Report Generation
  ✓ Data Visualization
  ✓ Graph Generation
  ✓ Detailed Calculations

⚠️  REQUIREMENTS:
  - Windows 7 or later
  - No Python installation needed!

🔧 TROUBLESHOOTING:
  If the application doesn't start:
  1. Make sure all files are in the same folder
  2. Check that data/ and reports/ folders exist
  3. Try running as Administrator

📊 PROJECT DETAILS:
  Assessment of Dust Accumulation on Photovoltaic
  Panel Performance in Minna, Niger State, Nigeria

📧 CONTACT:
  Department of Materials and Metallurgical Engineering
  Federal University of Technology, Minna

============================================================
""")
    print_color("📝 Created: README.txt", Colors.GREEN)

def create_run_script(folder):
    """Create batch file to run the EXE"""
    run_bat = folder / 'run_app.bat'
    with open(run_bat, 'w') as f:
        f.write("""@echo off
title PV Soiling Analyzer
color 0A

echo ============================================
echo    PV SOILING ANALYZER
echo    Federal University of Technology, Minna
echo    Department of Materials and Metallurgical Engineering
echo ============================================
echo.
echo Starting application...
echo.

start "" "PVSoilingAnalyzer.exe"

echo Application started!
echo.
echo ============================================
echo To close the application, close the main window.
echo ============================================
echo.
pause
""")
    print_color("📝 Created: run_app.bat", Colors.GREEN)

def create_uninstall_script(folder):
    """Create uninstall script"""
    uninstall_bat = folder / 'uninstall.bat'
    with open(uninstall_bat, 'w') as f:
        f.write("""@echo off
title Uninstall PV Soiling Analyzer
color 0C

echo ============================================
echo    UNINSTALL PV SOILING ANALYZER
echo ============================================
echo.
echo This will delete all files in this folder.
echo.

set /p confirm="Are you sure? (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo Deleting files...
    cd ..
    rmdir /s /q "%~dp0"
    echo.
    echo ✅ Uninstall complete!
) else (
    echo.
    echo ❌ Uninstall cancelled.
)

echo.
pause
""")
    print_color("📝 Created: uninstall.bat", Colors.GREEN)

def main():
    """Main function"""
    # Check if running with admin privileges
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    if not is_admin:
        print_color("⚠️  Not running as administrator.", Colors.YELLOW)
        print_color("   Some functions may require admin privileges.", Colors.YELLOW)
    
    # Build the EXE
    success = build_exe()
    
    if success:
        print_color("\n🎉 Build completed successfully!", Colors.GREEN)
    else:
        print_color("\n❌ Build failed. Please check the errors above.", Colors.RED)
        print_color("\nTry running manually:", Colors.YELLOW)
        print_color("   python -m PyInstaller --onefile --windowed --name PVSoilingAnalyzer main.py", Colors.WHITE)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()