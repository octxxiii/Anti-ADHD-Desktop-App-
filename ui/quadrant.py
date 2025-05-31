from PyQt5.QtWidgets import QFrame, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QMenu, QInputDialog, QTextEdit, QCheckBox, QDateTimeEdit, QGridLayout, QApplication, QCalendarWidget, QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QDateTime
from PyQt5.QtGui import QColor, QFont, QIcon
from datetime import datetime
from typing import Optional
from viewmodel.quadrant_vm import EisenhowerQuadrantViewModel

class EisenhowerQuadrantWidget(QFrame):
    def __init__(self, color, keyword, description, icon=None, viewmodel: EisenhowerQuadrantViewModel = None, parent=None):
        super().__init__(parent)
        self.color = color
        self.keyword = keyword
        self.description = description
        self.icon = icon
        self.viewmodel = viewmodel
        self._init_widgets()
        self._setup_styles(color)
        self._setup_layout()
        self._connect_signals()
        self._refresh_list()

    def _init_widgets(self):
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("할 일을 입력하세요...")
        self.add_button = QPushButton("추가")
        self.list_widget = QListWidget()

    def _setup_styles(self, color):
        self.setStyleSheet(f"""
            QFrame {{
                background: #fff;
                border-radius: 14px;
                border: 2px solid {color};
            }}
            QLabel {{
                color: {color};
                font-family: 'Segoe UI', 'Noto Sans KR', Arial, sans-serif;
                font-size: 11px;
                font-weight: bold;
                background: transparent;
                border: none;
            }}
        """)

    def _setup_layout(self):
        title_layout = QHBoxLayout()
        title_label = QLabel(self.keyword)
        title_label.setStyleSheet(f"font-size: 10.5pt; font-weight: bold; color: {self.color}; margin-bottom: 0px;")
        if self.icon:
            icon_label = QLabel()
            if isinstance(self.icon, QIcon):
                icon_label.setPixmap(self.icon.pixmap(15, 15))
            elif isinstance(self.icon, str):
                icon_label.setText(self.icon)
                icon_label.setAlignment(Qt.AlignCenter)
                icon_label.setStyleSheet("font-size: 13pt; margin-right: 2px;")
            title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.setSpacing(4)
        title_layout.setContentsMargins(2, 2, 2, 0)
        desc_label = QLabel(self.description)
        desc_label.setStyleSheet("font-size: 8.5pt; color: #666; margin-bottom: 2px;")
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(1, 1, 1, 1)
        input_layout.setSpacing(2)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(2)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(desc_label)
        main_layout.addWidget(self.list_widget, stretch=1)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

    def _connect_signals(self):
        self.add_button.clicked.connect(self.on_add_task)
        self.input_field.returnPressed.connect(self.on_add_task)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.list_widget.itemChanged.connect(self._on_item_changed)
        if self.viewmodel:
            self.viewmodel.tasksChanged.connect(self._refresh_list)

    def _refresh_list(self, *args):
        self.list_widget.clear()
        if not self.viewmodel:
            return
        for task in self.viewmodel.tasks:
            self._add_list_item(task)

    def on_add_task(self):
        title = self.input_field.text().strip()
        if not title:
            return
        if any(t.title == title for t in self.viewmodel.tasks):
            QMessageBox.warning(self, "중복", "이미 존재하는 제목입니다.")
            return
        self.viewmodel.add_task(title)
        self.input_field.clear()
        self.input_field.setFocus()

    def _add_list_item(self, task, idx=None):
        item = QListWidgetItem(task.title)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked if getattr(task, 'checked', False) else Qt.Unchecked)
        if idx is not None:
            self.list_widget.insertItem(idx, item)
        else:
            self.list_widget.addItem(item)
        if getattr(task, 'details', None):
            item.setToolTip(task.details)

    def _on_item_changed(self, item):
        idx = self.list_widget.row(item)
        if not self.viewmodel or idx < 0 or idx >= len(self.viewmodel.tasks):
            return
        task = self.viewmodel.tasks[idx]
        checked = (item.checkState() == Qt.Checked)
        if task.checked != checked:
            self.viewmodel.check_task(task.id, checked)

    def on_item_double_clicked(self, item):
        idx = self.list_widget.row(item)
        if not self.viewmodel or idx < 0 or idx >= len(self.viewmodel.tasks):
            return
        self.edit_task_dialog(idx)

    def show_context_menu(self, position):
        item = self.list_widget.itemAt(position)
        if not item:
            return
        idx = self.list_widget.row(item)
        menu = QMenu()
        edit_action = menu.addAction("수정")
        delete_action = menu.addAction("삭제")
        action = menu.exec(self.list_widget.mapToGlobal(position))
        if action == edit_action:
            self.edit_task_dialog(idx)
        elif action == delete_action:
            self.delete_task(idx)

    def edit_task_dialog(self, idx):
        task = self.viewmodel.tasks[idx]
        new_title, ok = QInputDialog.getText(self, "항목 수정", "제목:", text=task.title)
        if ok and new_title and new_title != task.title:
            task.title = new_title
            self.viewmodel.update_task(task)

    def delete_task(self, idx):
        if not self.viewmodel or idx < 0 or idx >= len(self.viewmodel.tasks):
            return
        task = self.viewmodel.tasks[idx]
        self.viewmodel.remove_task(task.id)

    def clear_tasks(self):
        if self.viewmodel:
            self.viewmodel.clear_tasks()

    def load_tasks(self, tasks):
        # MVVM 구조에서는 ViewModel이 직접 관리하므로 필요시만 사용
        self._refresh_list() 