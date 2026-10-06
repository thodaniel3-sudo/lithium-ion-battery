"""
LEBAS - Simple Fixed Build Script
This is a simplified version that should work without errors
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build():
    print("=" * 70)
    print("LEBAS - Simple Build (Fixed)")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    
    # Install required packages
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pyinstaller'], check=False)
    
    # Install tkinter if needed (on Windows it comes with Python)
    print()
    print("Building executable with PyInstaller...")
    print("-" * 50)
    
    # Simple build command with all necessary options
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name', 'LEBAS',
        '--add-data', f'dataset.csv;.',
        '--add-data', f'config.py;.',
        '--add-data', f'calculations;calculations',
        '--add-data', f'ui;ui',
        '--add-data', f'charts;charts',
        '--add-data', f'services;services',
        '--add-data', f'assets;assets',
        '--add-data', f'reports;reports',
        '--add-data', f'exports;exports',
        '--hidden-import', 'tkinter',
        '--hidden-import', 'tkinter.ttk',
        '--hidden-import', 'tkinter.messagebox',
        '--hidden-import', 'tkinter.filedialog',
        '--hidden-import', 'tkinter.simpledialog',
        '--hidden-import', 'pandas',
        '--hidden-import', 'numpy',
        '--hidden-import', 'matplotlib',
        '--hidden-import', 'matplotlib.backends.backend_tkagg',
        '--hidden-import', 'matplotlib.figure',
        '--hidden-import', 'matplotlib.pyplot',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'reportlab',
        '--hidden-import', 'scipy',
        '--collect-all', 'matplotlib',
        '--collect-all', 'numpy',
        '--collect-all', 'pandas',
        '--collect-data', 'matplotlib',
        '--collect-data', 'openpyxl',
        '--collect-data', 'reportlab',
        '--runtime-tmpdir', 'tmp',
        'main.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=False)
        
        if result.returncode == 0:
            print()
            print("✅ Build successful!")
            
            # Copy to root
            dist_exe = project_root / 'dist' / 'LEBAS.exe'
            root_exe = project_root / 'LEBAS.exe'
            
            if dist_exe.exists():
                shutil.copy2(dist_exe, root_exe)
                size_mb = root_exe.stat().st_size / (1024 * 1024)
                print(f"✅ Executable copied to: {root_exe}")
                print(f"📊 File size: {size_mb:.2f} MB")
                print()
                print("=" * 70)
                print("BUILD COMPLETE!")
                print("=" * 70)
                print()
                print(f"Run: {root_exe}")
            else:
                print("❌ Could not find built executable")
        else:
            print("❌ Build failed")
            print("Try running as Administrator or check error messages above")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    build()