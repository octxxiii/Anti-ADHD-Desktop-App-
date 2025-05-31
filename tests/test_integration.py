"""
통합 테스트
"""
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from ui.main_window import MainWindow
from core.data import save_data, load_data

@pytest.fixture
def main_window_with_data(qapp, temp_data_dir, sample_todo_data):
    """데이터가 있는 MainWindow fixture"""
    # 샘플 데이터 저장
    data_file = temp_data_dir / "test_data.json"
    save_data(sample_todo_data, data_file)
    
    # MainWindow 생성 및 데이터 로드
    window = MainWindow()
    window.load_data(data_file)
    window.show()
    return window

def test_add_and_save_todo(main_window_with_data, temp_data_dir):
    """할 일 추가 및 저장 테스트"""
    # 1사분면에 할 일 추가
    quadrant1 = main_window_with_data.findChild(EisenhowerQuadrantWidget, "quadrant1")
    input_field = quadrant1.findChild(QLineEdit)
    QTest.keyClicks(input_field, "새로운 할 일")
    QTest.keyClick(input_field, Qt.Key_Return)
    
    # 저장
    main_window_with_data.save_data(temp_data_dir / "saved_data.json")
    
    # 저장된 데이터 확인
    loaded_data = load_data(temp_data_dir / "saved_data.json")
    assert "새로운 할 일" in [todo["text"] for todo in loaded_data["quadrant1"]]

def test_check_and_auto_save(main_window_with_data, temp_data_dir):
    """할 일 체크 및 자동 저장 테스트"""
    # 자동 저장 활성화
    settings_dialog = main_window_with_data.show_settings()
    auto_save_checkbox = settings_dialog.findChild(QCheckBox, "auto_save_checkbox")
    if not auto_save_checkbox.isChecked():
        QTest.mouseClick(auto_save_checkbox, Qt.LeftButton)
    
    # 할 일 체크
    quadrant1 = main_window_with_data.findChild(EisenhowerQuadrantWidget, "quadrant1")
    todo_list = quadrant1.findChild(QListWidget)
    item = todo_list.item(0)
    checkbox = todo_list.itemWidget(item).findChild(QCheckBox)
    QTest.mouseClick(checkbox, Qt.LeftButton)
    
    # 자동 저장 대기
    QTest.qWait(1000)  # 1초 대기
    
    # 저장된 데이터 확인
    loaded_data = load_data(temp_data_dir / "auto_save.json")
    assert loaded_data["quadrant1"][0]["done"] is True

def test_full_workflow(main_window_with_data, temp_data_dir):
    """전체 워크플로우 테스트"""
    # 1. 할 일 추가
    quadrant1 = main_window_with_data.findChild(EisenhowerQuadrantWidget, "quadrant1")
    input_field = quadrant1.findChild(QLineEdit)
    QTest.keyClicks(input_field, "중요한 할 일")
    QTest.keyClick(input_field, Qt.Key_Return)
    
    # 2. 할 일 체크
    todo_list = quadrant1.findChild(QListWidget)
    item = todo_list.item(0)
    checkbox = todo_list.itemWidget(item).findChild(QCheckBox)
    QTest.mouseClick(checkbox, Qt.LeftButton)
    
    # 3. 투명도 조절
    opacity_button = main_window_with_data.findChild(QToolButton, "opacity_button")
    QTest.mouseClick(opacity_button, Qt.LeftButton)
    popup = qapp.activePopupWidget()
    slider = popup.findChild(QSlider)
    slider.setValue(50)
    
    # 4. 항상 위 설정
    pin_button = main_window_with_data.findChild(QToolButton, "pin_button")
    QTest.mouseClick(pin_button, Qt.LeftButton)
    
    # 5. 저장
    main_window_with_data.save_data(temp_data_dir / "workflow_data.json")
    
    # 6. 데이터 확인
    loaded_data = load_data(temp_data_dir / "workflow_data.json")
    assert "중요한 할 일" in [todo["text"] for todo in loaded_data["quadrant1"]]
    assert loaded_data["quadrant1"][0]["done"] is True 