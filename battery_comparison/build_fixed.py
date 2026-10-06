"""
LEBAS - Fixed Build Script for creating standalone executable
This script properly handles tkinter and all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_packages():
    """Install all required packages."""
    print("Installing required packages...")
    print("-" * 50)
    
    packages = [
        'pyinstaller>=6.0.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'matplotlib>=3.7.0',
        'openpyxl>=3.1.0',
        'reportlab>=4.0.0',
        'scipy>=1.10.0',
        'pillow>=9.0.0',  # Required for icon support
        'python-dateutil>=2.8.2'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except Exception as e:
            print(f"⚠️ Failed to install {package}: {e}")
    print()

def build_exe():
    """Build the executable with proper configuration."""
    print("=" * 70)
    print("LEBAS - Building Standalone Executable (Fixed Version)")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    
    # Step 1: Install packages
    install_packages()
    
    # Step 2: Get Python and tkinter paths
    print("Step 2: Locating Python and tkinter...")
    print("-" * 50)
    
    import tkinter
    tkinter_path = os.path.dirname(tkinter.__file__)
    print(f"✅ Tkinter found at: {tkinter_path}")
    
    python_path = sys.executable
    print(f"✅ Python: {python_path}")
    print()
    
    # Step 3: Create .spec file
    print("Step 3: Creating PyInstaller spec file...")
    print("-" * 50)
    
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

block_cipher = None

# Get tkinter path
import tkinter
tkinter_dir = os.path.dirname(tkinter.__file__)

# Collect all needed files
datas = [
    ('dataset.csv', '.'),
    ('config.py', '.'),
    ('calculations', 'calculations'),
    ('ui', 'ui'),
    ('charts', 'charts'),
    ('services', 'services'),
    ('assets', 'assets'),
    ('reports', 'reports'),
    ('exports', 'exports'),
]

# Add tkinter files
if os.path.exists(tkinter_dir):
    for root, dirs, files in os.walk(tkinter_dir):
        for file in files:
            if file.endswith('.tcl') or file.endswith('.dll'):
                rel_path = os.path.relpath(root, tkinter_dir)
                if rel_path == '.':
                    datas.append((os.path.join(root, file), 'tkinter'))
                else:
                    datas.append((os.path.join(root, file), os.path.join('tkinter', rel_path)))

# Hidden imports for tkinter and matplotlib backends
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'tkinter.simpledialog',
    'pandas',
    'numpy',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'matplotlib.figure',
    'matplotlib.pyplot',
    'openpyxl',
    'reportlab',
    'scipy',
    'scipy.stats',
    'dateutil',
    'dateutil.parser',
]

# Collect matplotlib data files
import matplotlib
matplotlib_dir = os.path.dirname(matplotlib.__file__)
for root, dirs, files in os.walk(os.path.join(matplotlib_dir, 'mpl-data')):
    for file in files:
        rel_path = os.path.relpath(root, matplotlib_dir)
        datas.append((os.path.join(root, file), os.path.join('matplotlib', rel_path)))

# Add numpy data files
import numpy
numpy_dir = os.path.dirname(numpy.__file__)
for root, dirs, files in os.walk(numpy_dir):
    for file in files:
        if file.endswith('.pyi') or file.endswith('.pyd'):
            rel_path = os.path.relpath(root, numpy_dir)
            if rel_path == '.':
                datas.append((os.path.join(root, file), 'numpy'))
            else:
                datas.append((os.path.join(root, file), os.path.join('numpy', rel_path)))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyd = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyd,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LEBAS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
'''
    
    spec_file = project_root / 'LEBAS.spec'
    with open(spec_file, 'w') as f:
        f.write(spec_content)
    print(f"✅ Spec file created: {spec_file}")
    print()
    
    # Step 4: Build with spec file
    print("Step 4: Building executable with PyInstaller...")
    print("-" * 50)
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        str(spec_file)
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print()
        print("✅ Build successful!")
        print()
        
        # Step 5: Copy executable to root
        print("Step 5: Copying executable to root folder...")
        print("-" * 50)
        
        dist_exe = project_root / 'dist' / 'LEBAS.exe'
        root_exe = project_root / 'LEBAS.exe'
        
        if dist_exe.exists():
            shutil.copy2(dist_exe, root_exe)
            print(f"✅ Executable copied to: {root_exe}")
            
            # Check file size
            size_mb = root_exe.stat().st_size / (1024 * 1024)
            print(f"📊 File size: {size_mb:.2f} MB")
            
        else:
            print("❌ Executable not found in dist folder")
            return
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return
    
    # Step 6: Cleanup (optional)
    print()
    cleanup = input("Clean up build files? (y/n): ").lower().strip()
    if cleanup == 'y':
        print("Cleaning up...")
        for dir_name in ['build', 'dist']:
            dir_path = project_root / dir_name
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"✅ Removed {dir_name}")
        
        spec_file = project_root / 'LEBAS.spec'
        if spec_file.exists():
            spec_file.unlink()
            print("✅ Removed spec file")
    
    # Final message
    print()
    print("=" * 70)
    print("✅ BUILD COMPLETE!")
    print("=" * 70)
    print()
    print(f"📁 Executable: {root_exe}")
    print(f"📊 Size: {size_mb:.2f} MB")
    print()
    print("To run: Double-click LEBAS.exe")
    print("First run may take 10-20 seconds to start")
    print("=" * 70)


if __name__ == "__main__":
    try:
        build_exe()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please run this script as Administrator")
        input("\nPress Enter to exit...")
        