"""
ui/settings.py 테스트
"""
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QTabWidget, QSlider, QCheckBox, QPushButton, QComboBox
from view.settings_dialog import SettingsDialog
from model.translation_model import TranslationModel

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

def test_language_switch(settings_dialog):
    """언어 전환 테스트"""
    # 일반 탭 선택
    tab_widget = settings_dialog.findChild(QTabWidget)
    tab_widget.setCurrentIndex(0)  # 일반 탭
    
    # 언어 콤보박스 찾기
    language_combo = settings_dialog.language_combo
    assert language_combo is not None
    
    # 초기 언어가 한국어인지 확인
    assert language_combo.currentData() == "ko"
    
    # 영어로 전환
    language_combo.setCurrentIndex(language_combo.findData("en"))
    
    # 영어로 전환되었는지 확인
    assert language_combo.currentData() == "en"
    assert settings_dialog.windowTitle() == "Settings"
    
    # 다시 한국어로 전환
    language_combo.setCurrentIndex(language_combo.findData("ko"))
    
    # 한국어로 전환되었는지 확인
    assert language_combo.currentData() == "ko"
    assert settings_dialog.windowTitle() == "설정"

def test_language_persistence(settings_dialog):
    """언어 설정 유지 테스트"""
    # 영어로 전환
    language_combo = settings_dialog.language_combo
    language_combo.setCurrentIndex(language_combo.findData("en"))
    settings_dialog.accept()
    
    # 새로운 설정 다이얼로그 생성
    new_dialog = SettingsDialog()
    new_dialog.show()
    
    # 언어 설정이 유지되었는지 확인
    assert new_dialog.language_combo.currentData() == "en"
    
    # 다시 한국어로 복구
    new_dialog.language_combo.setCurrentIndex(new_dialog.language_combo.findData("ko"))
    new_dialog.accept()

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