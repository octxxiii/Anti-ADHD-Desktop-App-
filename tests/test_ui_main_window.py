"""
ui/main_window.py 테스트
"""
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from ui.main_window import MainWindow

@pytest.fixture
def main_window(qapp):
    """MainWindow fixture"""
    window = MainWindow()
    window.show()
    return window

def test_initial_state(main_window):
    """초기 상태 테스트"""
    assert main_window.windowTitle() == "Anti-ADHD"
    assert main_window.isVisible()
    
    # 주요 위젯 존재 확인
    assert main_window.findChild(QToolBar) is not None
    assert main_window.findChild(QStatusBar) is not None

def test_settings_dialog(main_window):
    """설정 다이얼로그 테스트"""
    # 설정 버튼 클릭
    settings_button = main_window.findChild(QToolButton, "settings_button")
    QTest.mouseClick(settings_button, Qt.LeftButton)
    
    # 설정 다이얼로그가 열렸는지 확인
    dialog = qapp.activeWindow()
    assert isinstance(dialog, SettingsDialog)
    assert dialog.isVisible()

def test_opacity_popup(main_window):
    """투명도 팝업 테스트"""
    # 투명도 버튼 클릭
    opacity_button = main_window.findChild(QToolButton, "opacity_button")
    QTest.mouseClick(opacity_button, Qt.LeftButton)
    
    # 투명도 팝업이 표시되었는지 확인
    popup = qapp.activePopupWidget()
    assert isinstance(popup, OpacityPopup)
    assert popup.isVisible()

def test_always_on_top(main_window):
    """항상 위 설정 테스트"""
    # 항상 위 버튼 클릭
    pin_button = main_window.findChild(QToolButton, "pin_button")
    QTest.mouseClick(pin_button, Qt.LeftButton)
    
    # 창이 항상 위로 설정되었는지 확인
    assert main_window.windowFlags() & Qt.WindowStaysOnTopHint

def test_menu_actions(main_window):
    """메뉴 동작 테스트"""
    # 파일 메뉴 열기
    file_menu = main_window.menuBar().findChild(QMenu, "file_menu")
    file_menu.triggered.emit(file_menu.actions()[0])  # 새로 만들기
    
    # 새 프로젝트 다이얼로그가 표시되었는지 확인
    dialog = qapp.activeWindow()
    assert isinstance(dialog, QDialog)
    assert dialog.isVisible() 