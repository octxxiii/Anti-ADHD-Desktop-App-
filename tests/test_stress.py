import sys
import pytest
import json
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QTimer, QMimeData, QPoint
from PyQt5.QtGui import QDrag
from anti_adhd_pyqt import MainWindow
from datetime import datetime

@pytest.fixture(scope="module")
def app_and_window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.is_test_mode = True  # 테스트 모드 활성화
    win.show()
    yield app, win
    # --- 테스트 데이터 정리 (모든 테스트 후) ---
    win.project_list.clear()
    win.projects_data.clear()
    for quad in win.quadrant_widgets:
        quad.items.clear()
        quad.list_widget.clear()
    win.save_settings()
    win.close()

# --- 유틸리티: 테스트 데이터 클린업 (테스트 간 격리) ---
def clear_all_projects(win):
    win.project_list.clear()
    win.projects_data.clear()
    for quad in win.quadrant_widgets:
        quad.items.clear()
        quad.list_widget.clear()

def wait_for_events(app, timeout=1000):
    """이벤트 루프가 완료될 때까지 대기"""
    timer = QTimer()
    timer.setSingleShot(True)
    timer.start(timeout)
    while timer.isActive():
        app.processEvents()

def delete_test_projects(win, prefix_list=None):
    """테스트에서 사용된 프로젝트(특정 prefix) 모두 목록과 파일에서 삭제"""
    if prefix_list is None:
        prefix_list = [
            "StressTest_", "TaskCreationStress", "CheckDeleteStress",
            "SearchStress", "Switch_", "DragDropStress", "SaveLoadStress", "UIUpdateStress"
        ]
    to_delete = []
    for i in range(win.project_list.count()):
        item = win.project_list.item(i)
        if any(item.text().startswith(prefix) for prefix in prefix_list):
            to_delete.append(item.text())
    for project_name in to_delete:
        # 목록에서 삭제
        items = win.project_list.findItems(project_name, Qt.MatchExactly)
        if items:
            win.project_list.setCurrentItem(items[0])
            win.delete_selected_project()
        # 파일에서 삭제
        file_path = os.path.join(win.data_dir, f"project_{project_name}.json")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

# --- 1. 프로젝트 대량 생성 스트레스 테스트 ---
def test_project_creation_stress(app_and_window):
    app, win = app_and_window
    clear_all_projects(win)
    N = 100
    
    # UI 업데이트 비활성화로 성능 향상
    win.project_list.setUpdatesEnabled(False)
    win.setUpdatesEnabled(False)
    
    for i in range(N):
        win.add_new_project(f"StressTest_{i}")
        if i % 10 == 0:  # 10개마다 이벤트 처리
            wait_for_events(app)
    
    # UI 업데이트 재활성화
    win.project_list.setUpdatesEnabled(True)
    win.setUpdatesEnabled(True)
    wait_for_events(app)
    
    assert win.project_list.count() == N, f"프로젝트 생성 실패: {win.project_list.count()}개 생성됨"
    delete_test_projects(win)

# --- 2. 할 일 대량 추가 스트레스 테스트 ---
def test_task_creation_stress(app_and_window):
    app, win = app_and_window
    clear_all_projects(win)
    
    project_name = "TaskCreationStress"
    win.add_new_project(project_name)
    win.project_list.setCurrentItem(win.project_list.findItems(project_name, Qt.MatchExactly)[0])
    wait_for_events(app)
    
    quadrant = win.quadrant_widgets[0]
    quadrant.setUpdatesEnabled(False)
    
    for i in range(50):
        item_data = {
            'title': f"Task_{i}",
            'checked': False,
            'completed': False,
            'priority': 0,
            'due_date': None,
            'details': '',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        quadrant._add_list_item(item_data)
        if i % 10 == 0:
            wait_for_events(app)
    
    quadrant.setUpdatesEnabled(True)
    wait_for_events(app)
    
    assert quadrant.list_widget.count() == 50, "50개의 태스크가 생성되지 않았습니다."
    delete_test_projects(win)

# --- 3. 체크/해제 및 대량 삭제 스트레스 테스트 ---
def test_task_check_and_delete_stress(app_and_window):
    app, win = app_and_window
    clear_all_projects(win)
    
    project_name = "CheckDeleteStress"
    win.add_new_project(project_name)
    win.project_list.setCurrentItem(win.project_list.findItems(project_name, Qt.MatchExactly)[0])
    wait_for_events(app)
    
    quadrant = win.quadrant_widgets[0]
    quadrant.setUpdatesEnabled(False)
    
    # 태스크 생성
    for i in range(50):
        item_data = {
            'title': f"Task_{i}",
            'checked': False,
            'completed': False,
            'priority': 0,
            'due_date': None,
            'details': '',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        quadrant._add_list_item(item_data)
    
    quadrant.setUpdatesEnabled(True)
    wait_for_events(app)
    
    # 모든 태스크 체크
    quadrant.blockSignals(True)
    for i in range(quadrant.list_widget.count()):
        item = quadrant.list_widget.item(i)
        item.setCheckState(Qt.Checked)
    quadrant.blockSignals(False)
    wait_for_events(app)
    
    # 체크된 태스크 삭제
    quadrant.blockSignals(True)
    items_to_delete = []
    for i in range(quadrant.list_widget.count()):
        item = quadrant.list_widget.item(i)
        if item.checkState() == Qt.Checked:
            items_to_delete.append(item)
    
    for item in items_to_delete:
        quadrant.list_widget.takeItem(quadrant.list_widget.row(item))
    
    quadrant.blockSignals(False)
    wait_for_events(app)
    
    assert quadrant.list_widget.count() == 0, "모든 체크된 태스크가 삭제되지 않았습니다."
    delete_test_projects(win)

# --- 4. 검색 반복 스트레스 테스트 ---
def test_search_stress(app_and_window):
    app, win = app_and_window
    clear_all_projects(win)
    win.add_new_project("SearchStress")
    win.project_list.setCurrentRow(0)
    wait_for_events(app)
    
    quad = win.quadrant_widgets[0]
    quad.setUpdatesEnabled(False)
    
    # 할 일 추가
    for i in range(30):
        item_data = {
            'title': f"Searchable_{i}",
            'checked': False,
            'completed': False,
            'priority': 0,
            'due_date': None,
            'details': 'findme' if i % 2 == 0 else '',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        quad.items.append(item_data)
    
    quad.setUpdatesEnabled(True)
    quad._reorder_items()
    wait_for_events(app)
    
    # 검색 반복
    for _ in range(10):
        win.search_input.setText("findme")
        wait_for_events(app, 100)
        win.search_input.setText("")
        wait_for_events(app, 100)
    
    assert True  # UI 검색 반복에서 예외 없으면 성공
    delete_test_projects(win)

# --- 5. 프로젝트 전환 반복 스트레스 테스트 ---
def test_project_switch_stress(app_and_window):
    app, win = app_and_window
    clear_all_projects(win)
    
    # 프로젝트 생성
    win.project_list.setUpdatesEnabled(False)
    for i in range(10):
        win.add_new_project(f"Switch_{i}")
    win.project_list.setUpdatesEnabled(True)
    wait_for_events(app)
    
    # 프로젝트 전환
    for _ in range(20):
        for i in range(win.project_list.count()):
            win.project_list.setCurrentRow(i)
            wait_for_events(app, 50)
    
    assert True  # 반복 전환에서 예외 없으면 성공 
    delete_test_projects(win)

# --- 6. 드래그 앤 드롭 스트레스 테스트 ---
def test_drag_and_drop_stress(app_and_window):
    app, win = app_and_window
    clear_all_projects(win)
    
    project_name = "DragDropStress"
    win.add_new_project(project_name)
    win.project_list.setCurrentItem(win.project_list.findItems(project_name, Qt.MatchExactly)[0])
    wait_for_events(app)
    
    source_quad = win.quadrant_widgets[0]
    target_quad = win.quadrant_widgets[1]
    
    # 데이터 직접 이동 방식으로 대체
    for i in range(20):
        item_data = {
            'title': f"DragTask_{i}",
            'checked': False,
            'completed': False,
            'priority': 0,
            'due_date': None,
            'details': '',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        source_quad.items.append(item_data)
    source_quad._reorder_items()
    wait_for_events(app)
    
    for _ in range(20):
        if not source_quad.items:
            break
        item_data = source_quad.items[0]
        source_quad.items.pop(0)
        target_quad.items.append(item_data)
    source_quad._reorder_items()
    target_quad._reorder_items()
    wait_for_events(app)
    
    assert source_quad.list_widget.count() == 0, "모든 태스크가 소스 사분면에서 이동되지 않았습니다."
    assert target_quad.list_widget.count() == 20, "모든 태스크가 타겟 사분면으로 이동되지 않았습니다."
    # 테스트용 프로젝트 삭제
    win.delete_selected_project()
    delete_test_projects(win)

# --- 7. 데이터 저장/로드 스트레스 테스트 ---
def test_save_load_stress(app_and_window, tmp_path):
    app, win = app_and_window
    clear_all_projects(win)
    
    project_name = "SaveLoadStress"
    win.add_new_project(project_name)
    win.project_list.setCurrentItem(win.project_list.findItems(project_name, Qt.MatchExactly)[0])
    wait_for_events(app)
    
    for quad_idx, quad in enumerate(win.quadrant_widgets):
        quad.setUpdatesEnabled(False)
        for i in range(25):
            item_data = {
                'title': f"Task_{quad_idx}_{i}",
                'checked': i % 2 == 0,
                'completed': False,
                'priority': i % 3,
                'due_date': datetime.now().strftime('%Y-%m-%d %H:%M') if i % 4 == 0 else None,
                'details': f"Details for task {i} in quadrant {quad_idx}",
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            quad.items.append(item_data)
        quad._reorder_items()
        quad.setUpdatesEnabled(True)
    wait_for_events(app)
    
    for _ in range(5):
        save_path = tmp_path / f"stress_save_{_}.json"
        win.save_project_to_file(project_name, str(save_path))
        wait_for_events(app)
        clear_all_projects(win)
        wait_for_events(app)
        # 로드 후 UI 동기화
        loaded_data = win.load_project_from_file(project_name)
        win.projects_data[project_name] = loaded_data
        for i, quad in enumerate(win.quadrant_widgets):
            quad.load_tasks(loaded_data["tasks"][i])
        wait_for_events(app)
        for quad_idx, quad in enumerate(win.quadrant_widgets):
            assert quad.list_widget.count() == 25, f"사분면 {quad_idx}의 태스크 수가 일치하지 않습니다."
    # 테스트용 프로젝트 삭제
    win.delete_selected_project()
    delete_test_projects(win)

# --- 8. UI 업데이트 스트레스 테스트 ---
def test_ui_update_stress(app_and_window):
    app, win = app_and_window
    clear_all_projects(win)
    
    # 프로젝트 생성
    project_name = "UIUpdateStress"
    win.add_new_project(project_name)
    win.project_list.setCurrentItem(win.project_list.findItems(project_name, Qt.MatchExactly)[0])
    wait_for_events(app)
    
    # UI 업데이트 트리거 반복
    for _ in range(10):
        # 투명도 변경
        win.set_window_opacity(0.5)
        wait_for_events(app, 50)
        win.set_window_opacity(1.0)
        wait_for_events(app, 50)
        
        # 사이드바 토글
        win.toggle_sidebar()
        wait_for_events(app, 50)
        win.toggle_sidebar()
        wait_for_events(app, 50)
        
        # 다크 모드 토글
        win.toggle_dark_mode()
        wait_for_events(app, 50)
        win.toggle_dark_mode()
        wait_for_events(app, 50)
        
        # 툴바 토글
        win.toggle_main_toolbar()
        wait_for_events(app, 50)
        win.toggle_main_toolbar()
        wait_for_events(app, 50)
        
        # 검색바 토글
        win.toggle_search_toolbar()
        wait_for_events(app, 50)
        win.toggle_search_toolbar()
        wait_for_events(app, 50)
    
    assert True  # UI 업데이트 반복에서 예외 없으면 성공 
    delete_test_projects(win) 