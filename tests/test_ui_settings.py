"""
ui/settings.py 테스트
"""
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from ui.settings import SettingsDialog

@pytest.fixture
def settings_dialog(qapp):
    """SettingsDialog fixture"""
    dialog = SettingsDialog()
    dialog.show()
    return dialog

def test_initial_state(settings_dialog):
    """초기 상태 테스트"""
    assert settings_dialog.windowTitle() == "설정"
    assert settings_dialog.isVisible()
    
    # 탭이 존재하는지 확인
    tab_widget = settings_dialog.findChild(QTabWidget)
    assert tab_widget is not None
    assert tab_widget.count() > 0

def test_opacity_slider(settings_dialog):
    """투명도 슬라이더 테스트"""
    # 투명도 탭 선택
    tab_widget = settings_dialog.findChild(QTabWidget)
    tab_widget.setCurrentIndex(0)  # 투명도 탭
    
    # 슬라이더 값 변경
    slider = settings_dialog.findChild(QSlider)
    slider.setValue(50)
    
    # 값이 변경되었는지 확인
    assert slider.value() == 50

def test_auto_save_checkbox(settings_dialog):
    """자동 저장 체크박스 테스트"""
    # 데이터 관리 탭 선택
    tab_widget = settings_dialog.findChild(QTabWidget)
    tab_widget.setCurrentIndex(1)  # 데이터 관리 탭
    
    # 체크박스 상태 변경
    checkbox = settings_dialog.findChild(QCheckBox, "auto_save_checkbox")
    QTest.mouseClick(checkbox, Qt.LeftButton)
    
    # 상태가 변경되었는지 확인
    assert checkbox.isChecked()

def test_save_button(settings_dialog):
    """저장 버튼 테스트"""
    # 데이터 관리 탭 선택
    tab_widget = settings_dialog.findChild(QTabWidget)
    tab_widget.setCurrentIndex(1)
    
    # 저장 버튼 클릭
    save_button = settings_dialog.findChild(QPushButton, "save_button")
    QTest.mouseClick(save_button, Qt.LeftButton)
    
    # 다이얼로그가 닫혔는지 확인
    assert not settings_dialog.isVisible() 