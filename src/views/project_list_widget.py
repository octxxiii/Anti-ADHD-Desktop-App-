"""
Project List Widget - 프로젝트 목록 위젯
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QPushButton, QLabel, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List

from ..models.project_model import Project
from ..models.translation_service import tr


class ProjectListWidget(QWidget):
    """프로젝트 목록 위젯"""
    
    # 시그널 정의
    project_selected = pyqtSignal(str)  # project_id
    project_create_requested = pyqtSignal()
    project_rename_requested = pyqtSignal(str)  # project_id
    project_delete_requested = pyqtSignal(str)  # project_id
    project_move_up_requested = pyqtSignal(str)  # project_id
    project_move_down_requested = pyqtSignal(str)  # project_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._projects: List[Project] = []
        self._current_project_id: str = ""
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UI 설정"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 제목
        title_label = QLabel(tr("Projects"))
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 16px; 
                color: #333;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title_label)
        
        # 새 프로젝트 버튼
        self.new_project_btn = QPushButton("+ " + tr("New Project"))
        self.new_project_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.new_project_btn.clicked.connect(self._on_new_project_clicked)
        layout.addWidget(self.new_project_btn)
        
        # 프로젝트 목록
        self.project_list = QListWidget()
        self.project_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                outline: none;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)
        self.project_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.project_list.customContextMenuRequested.connect(self._show_context_menu)
        self.project_list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.project_list)
        
        # 통계 정보 (선택사항)
        self.stats_label = QLabel("프로젝트: 0개")
        self.stats_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.stats_label)
    
    def set_projects(self, projects: List[Project]) -> None:
        """프로젝트 목록 설정"""
        self._projects = projects
        self._update_project_list()
    
    def set_current_project(self, project: Project) -> None:
        """현재 프로젝트 설정"""
        if project:
            self._current_project_id = project.id
            self._update_selection()
    
    def _update_project_list(self) -> None:
        """프로젝트 목록 업데이트"""
        self.project_list.clear()
        
        for project in self._projects:
            item = QListWidgetItem()
            
            # 프로젝트 정보 표시
            task_count = len(project.tasks)
            completed_count = len(project.get_completed_tasks())
            
            if task_count > 0:
                completion_rate = int((completed_count / task_count) * 100)
                item_text = f"{project.name}\n{completed_count}/{task_count} ({completion_rate}%)"
            else:
                item_text = f"{project.name}\n{tr('No tasks')}"
            
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, project.id)
            
            self.project_list.addItem(item)
        
        # 통계 업데이트
        self.stats_label.setText(f"{tr('Projects')}: {len(self._projects)}")
        
        # 현재 선택 복원
        self._update_selection()
    
    def _update_selection(self) -> None:
        """현재 선택 업데이트"""
        if not self._current_project_id:
            return
            
        for i in range(self.project_list.count()):
            item = self.project_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == self._current_project_id:
                self.project_list.setCurrentItem(item)
                break
    
    def _on_new_project_clicked(self) -> None:
        """새 프로젝트 버튼 클릭"""
        self.project_create_requested.emit()
    
    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        """프로젝트 항목 클릭"""
        project_id = item.data(Qt.ItemDataRole.UserRole)
        if project_id:
            self._current_project_id = project_id
            self.project_selected.emit(project_id)
    
    def _get_project_index(self, project_id: str) -> int:
        """프로젝트 인덱스 반환"""
        for i, project in enumerate(self._projects):
            if project.id == project_id:
                return i
        return -1
    
    def _show_context_menu(self, position) -> None:
        """컨텍스트 메뉴 표시"""
        item = self.project_list.itemAt(position)
        if not item:
            return
        
        project_id = item.data(Qt.ItemDataRole.UserRole)
        if not project_id:
            return
        
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)
        
        # 순서 변경
        current_index = self._get_project_index(project_id)
        
        if current_index > 0:
            move_up_action = menu.addAction("↑ " + tr("Move Up"))
            move_up_action.triggered.connect(lambda: self.project_move_up_requested.emit(project_id))
        
        if current_index < len(self._projects) - 1:
            move_down_action = menu.addAction("↓ " + tr("Move Down"))
            move_down_action.triggered.connect(lambda: self.project_move_down_requested.emit(project_id))
        
        if current_index > 0 or current_index < len(self._projects) - 1:
            menu.addSeparator()
        
        # 이름 변경
        rename_action = menu.addAction(tr("Rename Project"))
        rename_action.triggered.connect(lambda: self.project_rename_requested.emit(project_id))
        
        menu.addSeparator()
        
        # 삭제
        delete_action = menu.addAction(tr("Delete Project"))
        delete_action.triggered.connect(lambda: self.project_delete_requested.emit(project_id))
        
        # 메뉴 표시
        menu.exec(self.project_list.mapToGlobal(position))