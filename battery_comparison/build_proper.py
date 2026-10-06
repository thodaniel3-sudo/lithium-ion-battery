"""
build_proper.py - Complete Working Build System for PV Soiling Analyzer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_all():
    """Clean all build files"""
    print("🧹 Cleaning previous builds...")
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  ✅ Removed {folder}/")
    
    # Remove spec files
    for file in Path('.').glob('*.spec'):
        file.unlink()
        print(f"  ✅ Removed {file.name}")
    print()

def create_folders():
    """Create required folders"""
    print("📁 Creating folders...")
    folders = ['data', 'reports']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"  ✅ Created {folder}/")
        else:
            print(f"  ✅ {folder}/ exists")
    
    # Create empty database if needed
    db_path = Path('data/pv_soiling.db')
    if not db_path.exists():
        db_path.touch()
        print("  ✅ Created data/pv_soiling.db")
    print()

def create_requirements():
    """Create requirements file"""
    with open('requirements.txt', 'w') as f:
        f.write("""PyQt5==5.15.9
matplotlib==3.7.2
pandas==2.0.3
numpy==1.24.3
openpyxl==3.1.2
reportlab==4.0.4
sqlalchemy==2.0.19
plotly==5.15.0
seaborn==0.12.2
""")
    print("✅ Created requirements.txt")

def check_files():
    """Check if all required files exist"""
    required = ['main.py', 'core.py', 'database.py', 'ui.py', 
                'visualization.py', 'reports.py']
    missing = []
    
    print("📁 Checking files...")
    for file in required:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size} bytes)")
        else:
            print(f"  ❌ {file} - MISSING!")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
        print("   Please make sure all files are in this folder.")
        return False
    return True

def fix_main_py():
    """Fix main.py to properly handle imports"""
    if not os.path.exists('main.py'):
        return
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add proper error handling for imports
    if 'try:' not in content:
        fixed_content = '''"""
main.py - Entry point for PV Soiling Analyzer
"""

import sys
import os
import traceback

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        print("=" * 60)
        print("  PV SOILING ANALYZER")
        print("  Federal University of Technology, Minna")
        print("=" * 60)
        print()
        
        from ui import run_app
        run_app()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\\nPlease make sure all files are in the same folder.")
        print("\\nRequired files:")
        print("  - main.py, core.py, database.py, ui.py")
        print("  - visualization.py, reports.py")
        input("\\nPress Enter to exit...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        input("\\nPress Enter to exit...")

if __name__ == "__main__":
    main()
'''
        with open('main.py', 'w') as f:
            f.write(fixed_content)
        print("✅ Fixed main.py")

def build_exe():
    """Build the EXE file"""
    print("=" * 60)
    print("  BUILDING PV SOILING ANALYZER EXE")
    print("=" * 60)
    print()
    
    # Clean previous builds
    clean_all()
    
    # Create folders
    create_folders()
    
    # Check files
    if not check_files():
        print("\n❌ Build cancelled - missing files!")
        return False
    
    # Fix main.py
    fix_main_py()
    
    print("\n🔨 Building EXE...")
    print("   This may take 3-5 minutes...")
    print("   DO NOT INTERRUPT THE PROCESS!")
    print()
    
    # Build command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'PVSoilingAnalyzer',
        '--add-data', f'data{os.pathsep}data',
        '--add-data', f'reports{os.pathsep}reports',
        '--hidden-import', 'PyQt5',
        '--hidden-import', 'PyQt5.QtWidgets',
        '--hidden-import', 'PyQt5.QtCore',
        '--hidden-import', 'PyQt5.QtGui',
        '--hidden-import', 'matplotlib',
        '--hidden-import', 'matplotlib.backends.backend_qt5agg',
        '--hidden-import', 'matplotlib.pyplot',
        '--hidden-import', 'pandas',
        '--hidden-import', 'numpy',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'reportlab',
        '--hidden-import', 'reportlab.platypus',
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
        '--exclude-module', 'tkinter',
        '--exclude-module', 'tcl',
        '--exclude-module', 'test',
        '--exclude-module', 'distutils',
        'main.py'
    ]
    
    # Run the build
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ BUILD SUCCESSFUL!")
        print("=" * 60)
        copy_to_desktop()
        return True
    else:
        print("\n❌ Build failed!")
        print("   Check the error messages above.")
        return False

def copy_to_desktop():
    """Copy EXE to Desktop"""
    try:
        desktop = Path.home() / 'Desktop'
        exe_folder = desktop / 'PV_Soiling_Analyzer_App'
        
        # Remove old folder
        if exe_folder.exists():
            shutil.rmtree(exe_folder)
            print("  ✅ Removed old folder")
        
        exe_folder.mkdir()
        print(f"  ✅ Created folder: {exe_folder}")
        
        # Copy EXE
        src_exe = Path('dist/PVSoilingAnalyzer.exe')
        if src_exe.exists():
            shutil.copy2(src_exe, exe_folder / 'PVSoilingAnalyzer.exe')
            print(f"  ✅ Copied PVSoilingAnalyzer.exe")
        
        # Copy folders
        for folder in ['data', 'reports']:
            src = Path(folder)
            dst = exe_folder / folder
            if src.exists():
                shutil.copytree(src, dst)
                print(f"  ✅ Copied {folder}/")
        
        # Create run script
        with open(exe_folder / 'run_app.bat', 'w') as f:
            f.write('''@echo off
title PV Soiling Analyzer
color 0A
echo ============================================
echo    PV SOILING ANALYZER
echo    Federal University of Technology, Minna
echo ============================================
echo.
echo Starting application...
echo.
start "" "PVSoilingAnalyzer.exe"
echo.
echo Application started!
echo.
pause
''')
        print("  ✅ Created run_app.bat")
        
        # Create README
        with open(exe_folder / 'README.txt', 'w') as f:
            f.write('''
============================================================
  PV SOILING ANALYZER - STANDALONE APPLICATION
  Federal University of Technology, Minna
============================================================

📁 LOCATION: This folder contains the standalone EXE

🚀 HOW TO RUN:
  Double-click PVSoilingAnalyzer.exe

📋 FEATURES:
  ✓ Machine Design Calculations
  ✓ Experiment Management
  ✓ Results Tracking
  ✓ PDF/Excel Report Generation
  ✓ Data Visualization
  ✓ Graph Generation

⚠️  REQUIREMENTS:
  - Windows 7 or later
  - No Python installation needed!

============================================================
''')
        print("  ✅ Created README.txt")
        
        print("\n" + "=" * 60)
        print("✅ APPLICATION READY FOR USE!")
        print("=" * 60)
        print(f"\n📍 Location: {exe_folder}")
        print("\n🚀 To run: Double-click PVSoilingAnalyzer.exe")
        print("   OR: Double-click run_app.bat")
        print("\n📁 You can share this entire folder.")
        print("   No Python installation needed!")
        print("\n" + "=" * 60)
        
        # Open folder
        os.startfile(exe_folder)
        
    except Exception as e:
        print(f"⚠️  Error copying: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("  PV SOILING ANALYZER - BUILD TOOL")
    print("  Federal University of Technology, Minna")
    print("=" * 60)
    print()
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller is installed")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed")
    
    # Create requirements
    create_requirements()
    
    # Build
    build_exe()

if __name__ == "__main__":
    main()