"""
Anti-ADHD PyQt6 MVVM Application
메인 애플리케이션 진입점
"""
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QTranslator, QLocale
from PyQt6.QtGui import QIcon

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.views.main_window import MainWindow
from src.viewmodels.main_viewmodel import MainViewModel


class AntiADHDApplication(QApplication):
    """Anti-ADHD 애플리케이션 클래스"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # 애플리케이션 정보 설정
        self.setApplicationName("Anti-ADHD")
        self.setApplicationVersion("2.0.0")
        self.setOrganizationName("octaxii")
        self.setOrganizationDomain("github.com/octaxii")
        
        # 고해상도 디스플레이 지원 (PyQt6에서는 기본적으로 활성화됨)
        # PyQt6에서는 AA_EnableHighDpiScaling이 제거되었음
        
        # 애플리케이션 아이콘 설정
        self._setup_icon()
        
        # 스타일 설정
        self._setup_style()
        
        # 메인 윈도우 생성
        self.main_window = None
        self._create_main_window()
    
    def _setup_icon(self):
        """애플리케이션 아이콘 설정"""
        icon_path = project_root / "icon1.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
    
    def _setup_style(self):
        """애플리케이션 스타일 설정"""
        # 기본 스타일시트 적용
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QPushButton {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 8px 16px;
            text-align: center;
            font-size: 14px;
            border-radius: 4px;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        
        QLineEdit {
            border: 2px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            font-size: 14px;
        }
        
        QLineEdit:focus {
            border-color: #4CAF50;
        }
        
        QListWidget {
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
        }
        
        QListWidget::item {
            padding: 5px;
            border-bottom: 1px solid #eee;
        }
        
        QListWidget::item:selected {
            background-color: #e3f2fd;
        }
        
        QListWidget::item:hover {
            background-color: #f5f5f5;
        }
        
        QCheckBox {
            spacing: 5px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 2px solid #cccccc;
            border-radius: 3px;
            background-color: white;
        }
        
        QCheckBox::indicator:checked {
            border: 2px solid #4CAF50;
            border-radius: 3px;
            background-color: #4CAF50;
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
        }
        
        QMenuBar {
            background-color: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        
        QMenuBar::item {
            padding: 8px 12px;
            background-color: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #e9ecef;
        }
        
        QToolBar {
            background-color: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            spacing: 3px;
        }
        
        QStatusBar {
            background-color: #f8f9fa;
            border-top: 1px solid #dee2e6;
        }
        """
        
        self.setStyleSheet(style)
    
    def _create_main_window(self):
        """메인 윈도우 생성"""
        try:
            self.main_window = MainWindow()
            self.main_window.show()
        except Exception as e:
            QMessageBox.critical(
                None, 
                "애플리케이션 오류", 
                f"애플리케이션을 시작할 수 없습니다:\n{str(e)}"
            )
            sys.exit(1)
    
    def run(self):
        """애플리케이션 실행"""
        return self.exec()


def main():
    """메인 함수"""
    # 환경 변수 설정 (고해상도 디스플레이 지원)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    
    try:
        # 애플리케이션 생성 및 실행
        app = AntiADHDApplication(sys.argv)
        
        # 예외 처리 핸들러 설정
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            error_msg = f"예상치 못한 오류가 발생했습니다:\n{exc_type.__name__}: {exc_value}"
            QMessageBox.critical(None, "오류", error_msg)
        
        sys.excepthook = handle_exception
        
        # 애플리케이션 실행
        exit_code = app.run()
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"애플리케이션 시작 실패: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()