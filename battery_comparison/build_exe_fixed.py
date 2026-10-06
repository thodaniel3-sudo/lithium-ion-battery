"""
build_exe_fixed.py - Build standalone EXE for PV Soiling Analyzer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_files():
    """Check if required files exist"""
    required_files = ['main.py']
    optional_files = ['core.py', 'database.py', 'ui.py', 'visualization.py', 'reports.py']
    
    print("📁 Checking files...")
    for f in required_files:
        if os.path.exists(f):
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} - MISSING!")
            return False
    
    print("\n📁 Optional files found:")
    for f in optional_files:
        if os.path.exists(f):
            print(f"  ✅ {f}")
        else:
            print(f"  ⚠️  {f} - not found (will use main.py only)")
    
    return True

def create_folders():
    """Create required folders"""
    print("\n📁 Creating folders...")
    for folder in ['data', 'reports']:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"  ✅ Created {folder}/")
        else:
            print(f"  ✅ {folder}/ exists")
    
    # Create sample data if needed
    if not os.path.exists('data/pv_soiling.db'):
        print("  📝 Creating sample database...")
        try:
            from database import Database
            db = Database()
            print("  ✅ Database created")
        except:
            print("  ⚠️  Could not create database (will be created on first run)")

def build_exe():
    """Build the EXE file"""
    print("=" * 60)
    print("  BUILDING PV SOILING ANALYZER EXE")
    print("=" * 60)
    print()
    
    # Check files
    if not check_files():
        print("\n❌ Missing required files!")
        print("   Make sure you're in the correct folder.")
        print("   Required: main.py")
        return False
    
    # Create folders
    create_folders()
    
    print("\n🔨 Building EXE...")
    print("   This may take 3-5 minutes...")
    print()
    
    # Build command with only main.py
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
        '--hidden-import', 'pandas',
        '--hidden-import', 'numpy',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'reportlab',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'plotly',
        '--hidden-import', 'seaborn',
        '--collect-all', 'matplotlib',
        '--collect-all', 'pyqt5',
        '--exclude-module', 'tkinter',
        'main.py'
    ]
    
    # Run the build
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print("\n✅ BUILD SUCCESSFUL!")
        copy_to_folder()
        return True
    else:
        print("\n❌ Build failed!")
        print("   Check the error messages above.")
        return False

def copy_to_folder():
    """Copy the EXE to a folder on Desktop"""
    try:
        desktop = Path.home() / 'Desktop'
        exe_folder = desktop / 'PV_Soiling_Analyzer_App'
        exe_folder.mkdir(exist_ok=True)
        
        src_exe = Path('dist/PVSoilingAnalyzer.exe')
        dst_exe = exe_folder / 'PVSoilingAnalyzer.exe'
        
        if src_exe.exists():
            shutil.copy2(src_exe, dst_exe)
            print(f"\n📁 EXE copied to: {dst_exe}")
            
            # Copy folders
            for folder in ['data', 'reports']:
                src = Path(folder)
                dst = exe_folder / folder
                if src.exists():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    print(f"📁 Copied {folder}/")
            
            # Create run script
            run_bat = exe_folder / 'run_app.bat'
            with open(run_bat, 'w') as f:
                f.write("""@echo off
title PV Soiling Analyzer
echo ============================================
echo  PV Soiling Analyzer
echo  Federal University of Technology, Minna
echo ============================================
echo.
echo Starting application...
start "" "PVSoilingAnalyzer.exe"
echo.
echo Application started!
pause
""")
            print("📝 Created: run_app.bat")
            
            print("\n" + "=" * 60)
            print("✅ APPLICATION READY!")
            print("=" * 60)
            print(f"\n📍 Location: {exe_folder}")
            print("\n🚀 To run: Double-click PVSoilingAnalyzer.exe")
            
            # Open folder
            os.startfile(exe_folder)
            
        else:
            print("⚠️  EXE not found in dist/")
            
    except Exception as e:
        print(f"⚠️  Error: {e}")

def main():
    """Main function"""
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found!")
        print(f"   Current folder: {os.getcwd()}")
        print("   Make sure you're in the right folder.")
        return
    
    # Build
    build_exe()

if __name__ == "__main__":
    main()