"""
ui/eisenhower.py 테스트
"""
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from ui.eisenhower import EisenhowerQuadrantWidget

@pytest.fixture
def eisenhower_widget(qapp):
    """EisenhowerQuadrantWidget fixture"""
    widget = EisenhowerQuadrantWidget()
    widget.show()
    return widget

def test_initial_state(eisenhower_widget):
    """초기 상태 테스트"""
    assert eisenhower_widget.windowTitle() == "아이젠하워 매트릭스"
    assert eisenhower_widget.isVisible()
    
    # 4개의 분면이 존재하는지 확인
    quadrants = eisenhower_widget.findChildren(EisenhowerQuadrantWidget)
    assert len(quadrants) == 4

def test_add_todo(eisenhower_widget):
    """할 일 추가 테스트"""
    # 1사분면에 할 일 추가
    quadrant1 = eisenhower_widget.findChild(EisenhowerQuadrantWidget, "quadrant1")
    input_field = quadrant1.findChild(QLineEdit)
    
    QTest.keyClicks(input_field, "새로운 할 일")
    QTest.keyClick(input_field, Qt.Key_Return)
    
    # 할 일이 추가되었는지 확인
    todo_list = quadrant1.findChild(QListWidget)
    assert todo_list.count() == 1
    assert todo_list.item(0).text() == "새로운 할 일"

def test_check_todo(eisenhower_widget):
    """할 일 체크 테스트"""
    # 할 일 추가
    quadrant1 = eisenhower_widget.findChild(EisenhowerQuadrantWidget, "quadrant1")
    input_field = quadrant1.findChild(QLineEdit)
    QTest.keyClicks(input_field, "체크할 할 일")
    QTest.keyClick(input_field, Qt.Key_Return)
    
    # 체크박스 클릭
    todo_list = quadrant1.findChild(QListWidget)
    item = todo_list.item(0)
    checkbox = todo_list.itemWidget(item).findChild(QCheckBox)
    QTest.mouseClick(checkbox, Qt.LeftButton)
    
    # 체크 상태 확인
    assert checkbox.isChecked()

def test_delete_todo(eisenhower_widget):
    """할 일 삭제 테스트"""
    # 할 일 추가
    quadrant1 = eisenhower_widget.findChild(EisenhowerQuadrantWidget, "quadrant1")
    input_field = quadrant1.findChild(QLineEdit)
    QTest.keyClicks(input_field, "삭제할 할 일")
    QTest.keyClick(input_field, Qt.Key_Return)
    
    # 우클릭 메뉴에서 삭제 선택
    todo_list = quadrant1.findChild(QListWidget)
    item = todo_list.item(0)
    QTest.mouseClick(todo_list.viewport(), Qt.RightButton, pos=todo_list.visualItemRect(item).center())
    
    # 삭제 메뉴 항목 클릭
    menu = qapp.activePopupWidget()
    delete_action = menu.findChild(QAction, "delete_action")
    QTest.mouseClick(menu, Qt.LeftButton, pos=menu.actionGeometry(delete_action).center())
    
    # 할 일이 삭제되었는지 확인
    assert todo_list.count() == 0 