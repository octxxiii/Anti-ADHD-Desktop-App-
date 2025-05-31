"""
build.py

- pyinstaller로 실행 파일 빌드
- mkdocs build로 문서 빌드
- requirements.txt freeze
- 사용법: python scripts/build.py [--docs|--app|--all]
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_icon():
    """Create application icon"""
    subprocess.run([sys.executable, "scripts/create_icon.py"], check=True)

def build_executable():
    """Build executable using PyInstaller"""
    # Clean dist directory
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Build executable
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=app_icon.ico",
        "--name=anti_adhd",
        "main.py"
    ], check=True)
    
    # Create zip archive
    shutil.make_archive("dist/anti_adhd", "zip", "dist", "anti_adhd.exe")

def build_docs():
    subprocess.run(['mkdocs', 'build'], check=True)

def freeze_requirements():
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        subprocess.run(['pip', 'freeze'], stdout=f, check=True)

def main():
    """Main build function"""
    # Create icon
    create_icon()
    
    # Build executable
    build_executable()
    
    print("Build completed successfully!")

if __name__ == '__main__':
    main() 