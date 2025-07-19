"""
Eisenhower Matrix Widget - 4분면 할 일 관리 위젯
"""
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, 
    QGroupBox, QListWidget, QListWidgetItem, QLineEdit, 
    QPushButton, QCheckBox, QMenu, QInputDialog, QMessageBox,
    QTextEdit, QDialog, QDialogButtonBox, QLabel, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QAction
from typing import Optional, Dict, List

from ..models.task_model import Task, Quadrant
from ..models.project_model import Project
from ..viewmodels.main_viewmodel import MainViewModel
from ..models.translation_service import tr


class TaskEditDialog(QDialog):
    """할 일 편집 다이얼로그"""
    
    def __init__(self, task: Optional[Task] = None, parent=None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle(tr("Edit Task") if task else tr("New task"))
        self.setModal(True)
        self.resize(400, 300)
        
        self._setup_ui()
        
        if task:
            self._load_task_data()
    
    def _setup_ui(self) -> None:
        """UI 설정"""
        layout = QVBoxLayout(self)
        
        # 폼 레이아웃
        form_layout = QFormLayout()
        
        # 제목
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText(tr("Enter task title"))
        form_layout.addRow(tr("Title") + ":", self.title_edit)
        
        # 설명/메모
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText(tr("Enter memo or detailed description (optional)"))
        self.description_edit.setMaximumHeight(120)
        form_layout.addRow(tr("Memo") + ":", self.description_edit)
        
        # 마감일 설정
        from PyQt6.QtWidgets import QDateTimeEdit, QCheckBox
        from PyQt6.QtCore import QDateTime
        
        due_date_layout = QHBoxLayout()
        self.due_date_checkbox = QCheckBox(tr("Set due date"))
        self.due_date_edit = QDateTimeEdit()
        self.due_date_edit.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.due_date_edit.setEnabled(False)
        self.due_date_checkbox.toggled.connect(self.due_date_edit.setEnabled)
        
        due_date_layout.addWidget(self.due_date_checkbox)
        due_date_layout.addWidget(self.due_date_edit)
        form_layout.addRow(tr("Due Date") + ":", due_date_layout)
        
        # 알림 설정
        reminder_layout = QHBoxLayout()
        self.reminder_checkbox = QCheckBox(tr("Set reminder"))
        
        from PyQt6.QtWidgets import QComboBox
        self.reminder_combo = QComboBox()
        self.reminder_combo.addItems([
            tr("1 day before"),
            tr("3 hours before"), 
            tr("1 hour before"),
            tr("30 minutes before"),
            tr("10 minutes before")
        ])
        self.reminder_combo.setEnabled(False)
        self.reminder_checkbox.toggled.connect(self.reminder_combo.setEnabled)
        
        reminder_layout.addWidget(self.reminder_checkbox)
        reminder_layout.addWidget(self.reminder_combo)
        form_layout.addRow(tr("Reminder") + ":", reminder_layout)
        
        # 우선순위 설정
        from ..models.task_model import Priority
        self.priority_combo = QComboBox()
        self.priority_combo.addItem(tr("Low"), Priority.LOW.value)
        self.priority_combo.addItem(tr("Medium"), Priority.MEDIUM.value)
        self.priority_combo.addItem(tr("High"), Priority.HIGH.value)
        form_layout.addRow(tr("Priority") + ":", self.priority_combo)
        
        layout.addLayout(form_layout)
        
        # 버튼
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def _load_task_data(self) -> None:
        """할 일 데이터 로드"""
        if self.task:
            self.title_edit.setText(self.task.title)
            self.description_edit.setPlainText(self.task.description)
            
            # 마감일 설정
            if self.task.due_date:
                self.due_date_checkbox.setChecked(True)
                from PyQt6.QtCore import QDateTime
                qt_datetime = QDateTime.fromSecsSinceEpoch(int(self.task.due_date.timestamp()))
                self.due_date_edit.setDateTime(qt_datetime)
            
            # 알림 설정
            if self.task.reminder_time:
                self.reminder_checkbox.setChecked(True)
                # 기본값으로 "마감 1시간 전" 선택
                self.reminder_combo.setCurrentIndex(2)
            
            # 우선순위 설정
            priority_index = self.priority_combo.findData(self.task.priority.value)
            if priority_index >= 0:
                self.priority_combo.setCurrentIndex(priority_index)
    
    def get_task_data(self) -> Dict:
        """할 일 데이터 반환"""
        from ..models.task_model import Priority
        from datetime import datetime, timedelta
        
        data = {
            'title': self.title_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'priority': Priority(self.priority_combo.currentData())
        }
        
        # 마감일 설정
        if self.due_date_checkbox.isChecked():
            qt_datetime = self.due_date_edit.dateTime()
            data['due_date'] = datetime.fromtimestamp(qt_datetime.toSecsSinceEpoch())
        else:
            data['due_date'] = None
        
        # 알림 설정
        if self.reminder_checkbox.isChecked() and data['due_date']:
            reminder_options = {
                0: timedelta(days=1),      # 1일 전
                1: timedelta(hours=3),     # 3시간 전
                2: timedelta(hours=1),     # 1시간 전
                3: timedelta(minutes=30),  # 30분 전
                4: timedelta(minutes=10)   # 10분 전
            }
            
            reminder_delta = reminder_options.get(self.reminder_combo.currentIndex(), timedelta(hours=1))
            data['reminder_time'] = data['due_date'] - reminder_delta
        else:
            data['reminder_time'] = None
        
        return data
    
    def accept(self) -> None:
        """확인 버튼 클릭"""
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, tr("Warning"), tr("Please enter a title"))
            self.title_edit.setFocus()
            return
        
        super().accept()


class QuadrantWidget(QWidget):
    """사분면 위젯"""
    
    task_added = pyqtSignal(str, dict)  # title, task_data
    task_updated = pyqtSignal(str, dict)  # task_id, updates
    task_deleted = pyqtSignal(str)  # task_id
    
    def __init__(self, quadrant: Quadrant, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self.quadrant = quadrant
        self.tasks: List[Task] = []
        
        self._setup_ui(title, subtitle)
    
    def _setup_ui(self, title: str, subtitle: str) -> None:
        """UI 설정"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 그룹박스
        self.group_box = QGroupBox(title)
        
        # 사분면별 색상 구분
        quadrant_colors = {
            Quadrant.URGENT_IMPORTANT: "#ffebee",          # 연한 빨강 (긴급하고 중요)
            Quadrant.NOT_URGENT_IMPORTANT: "#e8f5e8",     # 연한 초록 (중요하지만 긴급하지 않음)
            Quadrant.URGENT_NOT_IMPORTANT: "#fff3e0",     # 연한 주황 (긴급하지만 중요하지 않음)
            Quadrant.NOT_URGENT_NOT_IMPORTANT: "#f3e5f5"  # 연한 보라 (긴급하지도 중요하지도 않음)
        }
        
        border_colors = {
            Quadrant.URGENT_IMPORTANT: "#d32f2f",          # 빨강
            Quadrant.NOT_URGENT_IMPORTANT: "#388e3c",     # 초록
            Quadrant.URGENT_NOT_IMPORTANT: "#f57c00",     # 주황
            Quadrant.NOT_URGENT_NOT_IMPORTANT: "#7b1fa2"  # 보라
        }
        
        bg_color = quadrant_colors.get(self.quadrant, "#f5f5f5")
        border_color = border_colors.get(self.quadrant, "#cccccc")
        
        self.group_box.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 3px solid {border_color};
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 10px;
                background-color: {bg_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: {border_color};
                font-weight: bold;
                font-size: 13px;
            }}
        """)
        
        group_layout = QVBoxLayout(self.group_box)
        
        # 부제목
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: gray; font-size: 10px;")
        group_layout.addWidget(subtitle_label)
        
        # 입력 영역
        input_layout = QHBoxLayout()
        
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText(tr("New task"))
        self.input_edit.returnPressed.connect(self._on_add_task)
        input_layout.addWidget(self.input_edit)
        
        self.add_button = QPushButton(tr("Add"))
        self.add_button.clicked.connect(self._on_add_task)
        input_layout.addWidget(self.add_button)
        
        group_layout.addLayout(input_layout)
        
        # 할 일 목록
        self.task_list = QListWidget()
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self._show_context_menu)
        self.task_list.itemDoubleClicked.connect(self._on_edit_task)
        
        # 드래그 앤 드롭 설정
        self.task_list.setDragDropMode(QListWidget.DragDropMode.DragDrop)
        self.task_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.task_list.setAcceptDrops(True)
        
        # 드래그 시작을 위한 마우스 이벤트 처리
        self.task_list.mousePressEvent = self._mouse_press_event
        self.task_list.mouseMoveEvent = self._mouse_move_event
        self.task_list.dropEvent = self._handle_drop_event
        self.task_list.dragEnterEvent = self._drag_enter_event
        self.task_list.dragMoveEvent = self._drag_move_event
        
        # 드래그 시작 위치 저장
        self._drag_start_position = None
        
        group_layout.addWidget(self.task_list)
        
        layout.addWidget(self.group_box)
    
    def set_tasks(self, tasks: List[Task]) -> None:
        """할 일 목록 설정"""
        self.tasks = [task for task in tasks if task.quadrant == self.quadrant]
        self._update_task_list()
    
    def _update_task_list(self) -> None:
        """할 일 목록 업데이트"""
        self.task_list.clear()
        
        for task in self.tasks:
            item = QListWidgetItem()
            
            # 체크박스 생성
            checkbox = QCheckBox(task.title)
            checkbox.setChecked(task.is_completed)
            checkbox.stateChanged.connect(
                lambda state, t=task: self._on_task_completed(t, state == Qt.CheckState.Checked.value)
            )
            
            # 완료된 할 일은 스타일 변경
            if task.is_completed:
                checkbox.setStyleSheet("text-decoration: line-through; color: gray;")
            
            # 메모가 있는 경우 표시
            if task.description:
                checkbox.setText(f"{task.title} *")
            
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, checkbox)
            
            # 할 일 ID를 아이템에 저장
            item.setData(Qt.ItemDataRole.UserRole, task.id)
    
    def focus_input(self) -> None:
        """입력 필드에 포커스"""
        self.input_edit.setFocus()
    
    @pyqtSlot()
    def _on_add_task(self) -> None:
        """할 일 추가"""
        title = self.input_edit.text().strip()
        
        # 항상 확장된 다이얼로그 사용
        dialog = TaskEditDialog(parent=self)
        if title:
            dialog.title_edit.setText(title)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_task_data()
            # 확장된 데이터와 함께 시그널 발생
            self.task_added.emit(data['title'], data)
            self.input_edit.clear()
    
    @pyqtSlot(QListWidgetItem)
    def _on_edit_task(self, item: QListWidgetItem) -> None:
        """할 일 편집"""
        task_id = item.data(Qt.ItemDataRole.UserRole)
        task = next((t for t in self.tasks if t.id == task_id), None)
        
        if task:
            dialog = TaskEditDialog(task, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_task_data()
                self.task_updated.emit(task_id, data)
    
    def _on_task_completed(self, task: Task, completed: bool) -> None:
        """할 일 완료 상태 변경"""
        self.task_updated.emit(task.id, {'is_completed': completed})
    
    def _show_context_menu(self, position) -> None:
        """컨텍스트 메뉴 표시"""
        item = self.task_list.itemAt(position)
        if not item:
            return
        
        task_id = item.data(Qt.ItemDataRole.UserRole)
        task = next((t for t in self.tasks if t.id == task_id), None)
        
        if not task:
            return
        
        menu = QMenu(self)
        
        # 편집
        edit_action = QAction(tr("Edit"), self)
        edit_action.triggered.connect(lambda: self._on_edit_task(item))
        menu.addAction(edit_action)
        
        # 삭제
        delete_action = QAction(tr("Delete"), self)
        delete_action.triggered.connect(lambda: self._on_delete_task(task_id))
        menu.addAction(delete_action)
        
        menu.addSeparator()
        
        # 다른 사분면으로 이동
        move_menu = menu.addMenu(tr("Move"))
        
        quadrants = [
            (Quadrant.URGENT_IMPORTANT, tr("Urgent and Important")),
            (Quadrant.NOT_URGENT_IMPORTANT, tr("Important but Not Urgent")),
            (Quadrant.URGENT_NOT_IMPORTANT, tr("Urgent but Not Important")),
            (Quadrant.NOT_URGENT_NOT_IMPORTANT, tr("Neither Urgent nor Important"))
        ]
        
        for quadrant, name in quadrants:
            if quadrant != self.quadrant:
                action = QAction(name, self)
                action.triggered.connect(
                    lambda checked, q=quadrant: self.task_updated.emit(task_id, {'quadrant': q})
                )
                move_menu.addAction(action)
        
        menu.exec(self.task_list.mapToGlobal(position))
    
    def _on_delete_task(self, task_id: str) -> None:
        """할 일 삭제"""
        reply = QMessageBox.question(
            self, tr("Delete Task"),
            tr("Are you sure you want to delete this task?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.task_deleted.emit(task_id)
    
    def _handle_start_drag(self, supportedActions) -> None:
        """드래그 시작 이벤트 처리"""
        from PyQt6.QtCore import QMimeData
        from PyQt6.QtGui import QDrag
        
        current_item = self.task_list.currentItem()
        if current_item:
            task_id = current_item.data(Qt.ItemDataRole.UserRole)
            
            # MIME 데이터 생성
            mime_data = QMimeData()
            mime_data.setText(task_id)
            
            # 드래그 객체 생성
            drag = QDrag(self.task_list)
            drag.setMimeData(mime_data)
            
            # 드래그 실행
            drag.exec(Qt.DropAction.MoveAction)
    
    def _mouse_press_event(self, event):
        """마우스 프레스 이벤트"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_position = event.pos()
        # 원래 이벤트도 처리
        QListWidget.mousePressEvent(self.task_list, event)
    
    def _mouse_move_event(self, event):
        """마우스 이동 이벤트"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        
        if not self._drag_start_position:
            return
        
        # 드래그 거리 확인
        from PyQt6.QtWidgets import QApplication
        if ((event.pos() - self._drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
        
        # 드래그 시작
        self._start_drag()
    
    def _start_drag(self):
        """드래그 시작"""
        from PyQt6.QtCore import QMimeData
        from PyQt6.QtGui import QDrag
        
        current_item = self.task_list.currentItem()
        if not current_item:
            return
        
        task_id = current_item.data(Qt.ItemDataRole.UserRole)
        if not task_id:
            return
        
        # MIME 데이터 생성
        mime_data = QMimeData()
        mime_data.setText(task_id)
        
        # 드래그 객체 생성
        drag = QDrag(self.task_list)
        drag.setMimeData(mime_data)
        
        # 드래그 실행
        drop_action = drag.exec(Qt.DropAction.MoveAction)
    
    def _drag_enter_event(self, event):
        """드래그 진입 이벤트"""
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    
    def _drag_move_event(self, event):
        """드래그 이동 이벤트"""
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    
    def _handle_drop_event(self, event) -> None:
        """드롭 이벤트 처리"""
        if event.mimeData().hasText():
            # 드래그된 할 일의 ID 가져오기
            task_id = event.mimeData().text()
            
            # 현재 사분면으로 할 일 이동
            self.task_updated.emit(task_id, {'quadrant': self.quadrant})
            event.accept()
        else:
            event.ignore()


class EisenhowerWidget(QWidget):
    """아이젠하워 매트릭스 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._viewmodel: Optional[MainViewModel] = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """UI 설정"""
        layout = QGridLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # 4개 사분면 생성
        self.quadrant_widgets = {}
        
        # 1사분면: 긴급하고 중요
        self.quadrant_widgets[Quadrant.URGENT_IMPORTANT] = QuadrantWidget(
            Quadrant.URGENT_IMPORTANT,
            tr("Urgent and Important"),
            tr("Do it now")
        )
        layout.addWidget(self.quadrant_widgets[Quadrant.URGENT_IMPORTANT], 0, 0)
        
        # 2사분면: 중요하지만 긴급하지 않음
        self.quadrant_widgets[Quadrant.NOT_URGENT_IMPORTANT] = QuadrantWidget(
            Quadrant.NOT_URGENT_IMPORTANT,
            tr("Important but Not Urgent"),
            tr("Plan to do")
        )
        layout.addWidget(self.quadrant_widgets[Quadrant.NOT_URGENT_IMPORTANT], 0, 1)
        
        # 3사분면: 긴급하지만 중요하지 않음
        self.quadrant_widgets[Quadrant.URGENT_NOT_IMPORTANT] = QuadrantWidget(
            Quadrant.URGENT_NOT_IMPORTANT,
            tr("Urgent but Not Important"),
            tr("Delegate or do quickly")
        )
        layout.addWidget(self.quadrant_widgets[Quadrant.URGENT_NOT_IMPORTANT], 1, 0)
        
        # 4사분면: 긴급하지도 중요하지도 않음
        self.quadrant_widgets[Quadrant.NOT_URGENT_NOT_IMPORTANT] = QuadrantWidget(
            Quadrant.NOT_URGENT_NOT_IMPORTANT,
            tr("Neither Urgent nor Important"),
            tr("Don't do")
        )
        layout.addWidget(self.quadrant_widgets[Quadrant.NOT_URGENT_NOT_IMPORTANT], 1, 1)
        
        # 시그널 연결
        for widget in self.quadrant_widgets.values():
            widget.task_added.connect(self._on_task_added)
            widget.task_updated.connect(self._on_task_updated)
            widget.task_deleted.connect(self._on_task_deleted)
    
    def set_viewmodel(self, viewmodel: Optional[MainViewModel]) -> None:
        """ViewModel 설정"""
        self._viewmodel = viewmodel
        self._update_tasks()
    
    def focus_first_quadrant(self) -> None:
        """첫 번째 사분면에 포커스"""
        self.quadrant_widgets[Quadrant.URGENT_IMPORTANT].focus_input()
    
    def _update_tasks(self) -> None:
        """할 일 목록 업데이트"""
        if not self._viewmodel or not self._viewmodel.current_project:
            # 프로젝트가 없으면 모든 사분면 비우기
            for widget in self.quadrant_widgets.values():
                widget.set_tasks([])
            return
        
        # 각 사분면에 해당하는 할 일 설정
        for quadrant, widget in self.quadrant_widgets.items():
            tasks = self._viewmodel.get_tasks_by_quadrant(quadrant)
            widget.set_tasks(tasks)
    
    @pyqtSlot(str, dict)
    def _on_task_added(self, title: str, task_data: dict) -> None:
        """할 일 추가"""
        if not self._viewmodel:
            return
            
        # 어느 사분면에서 추가되었는지 확인
        sender = self.sender()
        if isinstance(sender, QuadrantWidget):
            # 기본 할 일 추가
            success = self._viewmodel.add_task(title, sender.quadrant, task_data.get('description', ''))
            
            if success and self._viewmodel.current_project:
                # 추가된 할 일을 찾아서 확장 데이터 업데이트
                added_task = None
                for task in self._viewmodel.current_project.tasks:
                    if task.title == title and task.quadrant == sender.quadrant:
                        added_task = task
                        break
                
                if added_task:
                    # 확장 데이터 업데이트
                    update_data = {}
                    if 'priority' in task_data:
                        update_data['priority'] = task_data['priority']
                    if 'due_date' in task_data:
                        update_data['due_date'] = task_data['due_date']
                    if 'reminder_time' in task_data:
                        update_data['reminder_time'] = task_data['reminder_time']
                    
                    if update_data:
                        self._viewmodel.update_task(added_task.id, **update_data)
                
                self._update_tasks()
    
    @pyqtSlot(str, dict)
    def _on_task_updated(self, task_id: str, updates: dict) -> None:
        """할 일 업데이트"""
        if not self._viewmodel:
            return
            
        success = self._viewmodel.update_task(task_id, **updates)
        if success:
            self._update_tasks()
    
    @pyqtSlot(str)
    def _on_task_deleted(self, task_id: str) -> None:
        """할 일 삭제"""
        if not self._viewmodel:
            return
            
        success = self._viewmodel.delete_task(task_id)
        if success:
            self._update_tasks()