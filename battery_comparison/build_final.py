"""
build_final.py - Complete Build Script for PV Soiling Analyzer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_folders():
    """Create required folders"""
    print("\n📁 Creating folders...")
    folders = ['data', 'reports', 'dist', 'build']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"  ✅ Created {folder}/")
        else:
            print(f"  ✅ {folder}/ exists")
    
    # Create a simple database file if it doesn't exist
    if not os.path.exists('data/pv_soiling.db'):
        with open('data/pv_soiling.db', 'w') as f:
            f.write("")  # Create empty file
        print("  ✅ Created data/pv_soiling.db")

def create_simple_main():
    """Create a simple main.py if the real one doesn't exist"""
    if os.path.exists('main.py'):
        print("  ✅ main.py exists")
        return True
    
    print("  📝 Creating main.py...")
    with open('main.py', 'w') as f:
        f.write('''
"""
PV Soiling Analyzer - Main Entry Point
"""

import sys
import os

def main():
    print("=" * 60)
    print("  PV SOILING ANALYZER")
    print("  Federal University of Technology, Minna")
    print("=" * 60)
    print()
    print("✅ Application is running!")
    print("   This is a test build.")
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
''')
    print("  ✅ Created main.py")
    return True

def build_exe():
    """Build the EXE file"""
    print("=" * 60)
    print("  BUILDING PV SOILING ANALYZER EXE")
    print("=" * 60)
    print()
    
    # Create folders
    create_folders()
    
    # Create main.py if needed
    create_simple_main()
    
    print("\n🔨 Building EXE...")
    print("   This may take 3-5 minutes...")
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
        '--hidden-import', 'matplotlib',
        '--hidden-import', 'pandas',
        '--hidden-import', 'numpy',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'reportlab',
        '--hidden-import', 'openpyxl',
        '--collect-all', 'matplotlib',
        '--exclude-module', 'tkinter',
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
        
        # Remove old folder if exists
        if exe_folder.exists():
            shutil.rmtree(exe_folder)
        
        exe_folder.mkdir()
        
        # Copy EXE
        src_exe = Path('dist/PVSoilingAnalyzer.exe')
        if src_exe.exists():
            shutil.copy2(src_exe, exe_folder / 'PVSoilingAnalyzer.exe')
            print(f"\n📁 EXE copied to: {exe_folder}")
            
            # Copy folders
            for folder in ['data', 'reports']:
                src = Path(folder)
                dst = exe_folder / folder
                if src.exists():
                    shutil.copytree(src, dst)
                    print(f"📁 Copied {folder}/")
            
            # Create run script
            with open(exe_folder / 'run_app.bat', 'w') as f:
                f.write('''@echo off
title PV Soiling Analyzer
echo ============================================
echo  PV Soiling Analyzer
echo  Federal University of Technology, Minna
echo ============================================
echo.
echo Starting application...
start "" "PVSoilingAnalyzer.exe"
echo.
pause
''')
            
            print("\n" + "=" * 60)
            print("✅ APPLICATION READY!")
            print("=" * 60)
            print(f"\n📍 Location: {exe_folder}")
            print("\n🚀 Double-click: PVSoilingAnalyzer.exe")
            
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
    
    # Build
    build_exe()

if __name__ == "__main__":
    main()