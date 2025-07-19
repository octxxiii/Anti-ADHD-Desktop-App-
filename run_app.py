#!/usr/bin/env python3
"""
Anti-ADHD PyQt6 MVVM 애플리케이션 실행 스크립트
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# PyQt6 환경 설정
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

try:
    from src.main import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Import 오류: {e}")
    print("PyQt6가 설치되어 있는지 확인하세요:")
    print("pip install PyQt6")
    sys.exit(1)
except Exception as e:
    print(f"애플리케이션 실행 오류: {e}")
    sys.exit(1)