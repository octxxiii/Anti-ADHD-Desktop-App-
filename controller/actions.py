"""
controller/actions.py

메뉴/툴바/단축키 액션 핸들러 모음
"""

def add_task_to_current_quadrant(main_window):
    """현재 포커스된 사분면에 할 일 추가 입력 포커스"""
    focused = None
    for quad in main_window.quadrant_widgets:
        if quad.hasFocus() or quad.input_field.hasFocus():
            focused = quad
            break
    if not focused:
        focused = main_window.quadrant_widgets[0] if main_window.quadrant_widgets else None
    if focused:
        focused.input_field.setFocus()

def reload_data_and_ui(main_window):
    """현재 프로젝트 데이터와 UI를 새로고침"""
    if not main_window.current_project_name:
        return
    main_window.load_project_from_file(main_window.current_project_name)
    main_window.update_quadrant_display(main_window.current_project_name)
    main_window.update_project_status_label() 