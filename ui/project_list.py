from PyQt5.QtWidgets import QListWidget, QMenu, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from viewmodel.project_list_vm import ProjectListViewModel

class ProjectListWidget(QListWidget):
    projectSelected = pyqtSignal(str)  # 프로젝트 선택 시그널

    def __init__(self, viewmodel: ProjectListViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """UI 초기화"""
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def _connect_signals(self):
        """시그널 연결"""
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.itemSelectionChanged.connect(self._on_selection_changed)
        
        # ViewModel 시그널 연결
        self.viewmodel.projectsChanged.connect(self._on_projects_changed)
        self.viewmodel.statusMessageChanged.connect(self._on_status_message)

    def _on_projects_changed(self, projects):
        """프로젝트 목록 변경 시 호출"""
        self.clear()
        for project in projects:
            self.addItem(project)

    def _on_selection_changed(self):
        """선택 변경 시 호출"""
        current_item = self.currentItem()
        if current_item:
            self.viewmodel.select_project(current_item.text())
            self.projectSelected.emit(current_item.text())
        else:
            self.viewmodel.select_project(None)
            self.projectSelected.emit("")

    def _on_status_message(self, message: str, duration: int):
        """상태 메시지 표시"""
        if hasattr(self, 'main_window') and self.main_window:
            self.main_window.statusBar().showMessage(message, duration)

    def show_context_menu(self, position):
        """컨텍스트 메뉴 표시"""
        item = self.itemAt(position)
        if not item:
            return

        menu = QMenu()
        rename_action = menu.addAction("이름 변경")
        delete_action = menu.addAction("삭제")
        
        action = menu.exec(self.mapToGlobal(position))
        
        if action == rename_action:
            self._rename_project(item)
        elif action == delete_action:
            self._delete_project(item)

    def _rename_project(self, item):
        """프로젝트 이름 변경"""
        old_name = item.text()
        new_name, ok = QInputDialog.getText(
            self, "프로젝트 이름 변경",
            "새 프로젝트 이름:",
            text=old_name
        )
        
        if ok and new_name:
            if self.viewmodel.rename_project(old_name, new_name):
                item.setText(new_name)

    def _delete_project(self, item):
        """프로젝트 삭제"""
        name = item.text()
        reply = QMessageBox.question(
            self, "프로젝트 삭제",
            f"'{name}' 프로젝트를 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.viewmodel.delete_project(name):
                self.takeItem(self.row(item))

    def add_new_project(self):
        """새 프로젝트 추가"""
        name, ok = QInputDialog.getText(self, "새 프로젝트", "프로젝트 이름:")
        if ok and name:
            if self.viewmodel.add_project(name):
                self.setCurrentItem(self.findItems(name, Qt.MatchExactly)[0]) 