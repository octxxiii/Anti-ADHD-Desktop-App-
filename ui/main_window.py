from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QListWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLineEdit, QPushButton, QAction, QMenu, QGridLayout, QTextEdit,
    QMessageBox, QFileDialog, QListWidgetItem, QLabel, QCheckBox, QSlider,
    QStyle, QSizePolicy, QTabWidget, QFormLayout, QToolButton, QFrame,
    QStatusBar, QShortcut, QDateTimeEdit, QAbstractItemView, QCalendarWidget,
    QInputDialog, QDialog, QToolBar
)
from PyQt5.QtCore import Qt, QSettings, QUrl, QPoint, QSize, QTimer, QDateTime
from PyQt5.QtGui import QIcon, QDesktopServices, QPainter, QPen, QColor, QPixmap, QCursor, QFont
import os
import json
import zipfile
import shutil
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List

from ui.quadrant import EisenhowerQuadrantWidget
from ui.project_list import ProjectListWidget
from ui.settings_dialog import SettingsDialog
from ui.opacity_popup import OpacityPopup
from core.constants import QT_CONST, QSETTINGS_INIFMT
from core.utils import resource_path
from core.data import (
    save_project_to_file as core_save_project_to_file,
    load_project_from_file as core_load_project_from_file,
    list_project_files as core_list_project_files,
    backup_project_file as core_backup_project_file,
    restore_project_file as core_restore_project_file
)
from controller.actions import add_task_to_current_quadrant, reload_data_and_ui
from controller.backup import backup_data, restore_from_backup

from viewmodel.quadrant_vm import EisenhowerQuadrantViewModel
from usecase.todo_usecase import TodoUseCase
from model.repository import FileTodoRepository
from usecase.project_usecase import ProjectUseCase
from viewmodel.project_list_vm import ProjectListViewModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anti-ADHD")
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        
        # 기본 설정
        self.settings = QSettings("anti_adhd_settings.ini", QSETTINGS_INIFMT)
        self.data_dir = self.settings.value("dataDir", os.path.join(os.path.expanduser("~"), "anti_adhd_data"))
        self.current_project_name = None
        self.projects_data = {}
        self.quadrant_widgets = []
        self.window_opacity = 1.0
        self.auto_save_enabled = True
        self.dark_mode = False
        
        # Repository, UseCase 초기화
        self.repository = FileTodoRepository(self.data_dir)
        self.todo_usecase = TodoUseCase(self.repository)
        self.project_usecase = ProjectUseCase(self.repository)
        
        # ViewModel 초기화
        self.project_list_vm = ProjectListViewModel(self.project_usecase)
        
        # UI 초기화
        self.init_ui()
        self.setup_shortcuts()
        
        # 프로젝트 로드
        self.load_all_projects()
        self.select_initial_project()
        
        # 자동 저장 타이머
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self._auto_backup)
        self.auto_save_timer.start(300000)  # 5분마다
        
        # 리마인더 체크 타이머
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_due_reminders)
        self.reminder_timer.start(60000)  # 1분마다
        
        # 창 크기/위치 복원
        self.restore_geometry()
        
    def init_ui(self):
        """UI 초기화"""
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Repository, UseCase 초기화
        self.repository = FileTodoRepository(self.data_dir)
        self.todo_usecase = TodoUseCase(self.repository)
        self.project_usecase = ProjectUseCase(self.repository)
        
        # ViewModel 초기화
        self.project_list_vm = ProjectListViewModel(self.project_usecase)
        
        # 사이드바 (프로젝트 리스트)
        self.sidebar = ProjectListWidget(self.project_list_vm)
        self.sidebar.setMaximumWidth(200)
        self.sidebar.setMinimumWidth(150)
        self.sidebar.projectSelected.connect(self.on_project_selection_changed)
        self.sidebar.main_window = self  # 상태 메시지 표시를 위해 참조 유지
        
        # 메인 영역 (사분면)
        main_area = QWidget()
        main_area_layout = QGridLayout(main_area)
        main_area_layout.setSpacing(10)
        
        # 사분면 위젯 생성
        quadrant_configs = [
            ("#FF5252", "긴급하고 중요함", "즉시 처리해야 할 일", "⚡"),
            ("#FFD740", "중요하지만 긴급하지 않음", "계획적으로 처리할 일", "📅"),
            ("#69F0AE", "긴급하지만 중요하지 않음", "위임하거나 최소화할 일", "↗️"),
            ("#40C4FF", "긴급하지도 중요하지도 않음", "제거하거나 나중에 할 일", "⏳")
        ]
        
        self.quadrant_widgets = []
        for i, (color, keyword, description, icon) in enumerate(quadrant_configs):
            # ViewModel 생성
            viewmodel = EisenhowerQuadrantViewModel(
                todo_usecase=self.todo_usecase,
                project_name=self.current_project_name or "",
                quadrant_idx=i
            )
            
            # 위젯 생성 및 ViewModel 주입
            widget = EisenhowerQuadrantWidget(
                color=color,
                keyword=keyword,
                description=description,
                icon=icon,
                viewmodel=viewmodel
            )
            widget.main_window = self  # 상태 메시지 표시를 위해 참조 유지
            self.quadrant_widgets.append(widget)
            
            # 레이아웃에 추가
            row = i // 2
            col = i % 2
            main_area_layout.addWidget(widget, row, col)
        
        # 레이아웃 설정
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(main_area)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)
        
        # 상태바 설정
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.project_status_label = QLabel()
        self.statusBar.addPermanentWidget(self.project_status_label)
        
        # 메뉴바 설정
        self.setup_menubar()
        
        # 툴바 설정
        self.setup_toolbars()
        
        # 창 크기 설정
        self.resize(1200, 800)
        
    def setup_shortcuts(self):
        """단축키 설정"""
        # 새 프로젝트
        new_project_shortcut = QShortcut(Qt.CTRL + Qt.Key_N, self)
        new_project_shortcut.activated.connect(self.add_new_project)
        
        # 저장
        save_shortcut = QShortcut(Qt.CTRL + Qt.Key_S, self)
        save_shortcut.activated.connect(self.save_current_project)
        
        # 새 할 일
        new_task_shortcut = QShortcut(Qt.CTRL + Qt.Key_B, self)
        new_task_shortcut.activated.connect(lambda: add_task_to_current_quadrant(self))
        
        # 검색
        search_shortcut = QShortcut(Qt.CTRL + Qt.Key_F, self)
        search_shortcut.activated.connect(lambda: self.search_toolbar.show())
        
        # 실행 취소
        undo_shortcut = QShortcut(Qt.CTRL + Qt.Key_Z, self)
        undo_shortcut.activated.connect(lambda: reload_data_and_ui(self))
        
    def restore_geometry(self):
        """창 크기/위치 복원"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            # 기본 크기/위치
            screen = QDesktopServices.screenGeometry(self)
            self.resize(1200, 800)
            self.move(
                (screen.width() - self.width()) // 2,
                (screen.height() - self.height()) // 2
            ) 

    def setup_menubar(self):
        """메뉴바 설정"""
        menubar = self.menuBar()
        
        # 파일 메뉴
        file_menu = menubar.addMenu("파일")
        
        new_project_action = QAction("새 프로젝트", self)
        new_project_action.setShortcut("Ctrl+N")
        new_project_action.triggered.connect(self.add_new_project)
        file_menu.addAction(new_project_action)
        
        save_action = QAction("저장", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_current_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("다른 이름으로 저장", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        import_action = QAction("프로젝트 가져오기", self)
        import_action.triggered.connect(self.import_project_file)
        file_menu.addAction(import_action)
        
        export_action = QAction("프로젝트 내보내기", self)
        export_action.triggered.connect(self.save_project_as)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction("설정", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("종료", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 편집 메뉴
        edit_menu = menubar.addMenu("편집")
        
        add_task_action = QAction("새 할 일", self)
        add_task_action.setShortcut("Ctrl+B")
        add_task_action.triggered.connect(lambda: add_task_to_current_quadrant(self))
        edit_menu.addAction(add_task_action)
        
        edit_menu.addSeparator()
        
        undo_action = QAction("실행 취소", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(lambda: reload_data_and_ui(self))
        edit_menu.addAction(undo_action)
        
        # 보기 메뉴
        view_menu = menubar.addMenu("보기")
        
        toggle_sidebar_action = QAction("사이드바", self)
        toggle_sidebar_action.setCheckable(True)
        toggle_sidebar_action.setChecked(True)
        toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(toggle_sidebar_action)
        
        toggle_toolbar_action = QAction("메인 툴바", self)
        toggle_toolbar_action.setCheckable(True)
        toggle_toolbar_action.setChecked(True)
        toggle_toolbar_action.triggered.connect(self.toggle_main_toolbar)
        view_menu.addAction(toggle_toolbar_action)
        
        toggle_search_action = QAction("검색 툴바", self)
        toggle_search_action.setCheckable(True)
        toggle_search_action.setChecked(True)
        toggle_search_action.triggered.connect(self.toggle_search_toolbar)
        view_menu.addAction(toggle_search_action)
        
        view_menu.addSeparator()
        
        always_on_top_action = QAction("항상 위", self)
        always_on_top_action.setCheckable(True)
        always_on_top_action.triggered.connect(self.toggle_always_on_top)
        view_menu.addAction(always_on_top_action)
        
        dark_mode_action = QAction("다크 모드", self)
        dark_mode_action.setCheckable(True)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(dark_mode_action)
        
        # 도구 메뉴
        tools_menu = menubar.addMenu("도구")
        
        search_action = QAction("검색", self)
        search_action.setShortcut("Ctrl+F")
        search_action.triggered.connect(lambda: self.search_toolbar.show())
        tools_menu.addAction(search_action)
        
        statistics_action = QAction("통계", self)
        statistics_action.triggered.connect(self.show_task_statistics)
        tools_menu.addAction(statistics_action)
        
        export_report_action = QAction("보고서 내보내기", self)
        export_report_action.triggered.connect(self.export_task_report)
        tools_menu.addAction(export_report_action)
        
        tools_menu.addSeparator()
        
        backup_action = QAction("백업", self)
        backup_action.triggered.connect(lambda: backup_data(self))
        tools_menu.addAction(backup_action)
        
        restore_action = QAction("복원", self)
        restore_action.triggered.connect(lambda: restore_from_backup(self))
        tools_menu.addAction(restore_action)
        
        # 도움말 메뉴
        help_menu = menubar.addMenu("도움말")
        
        about_action = QAction("정보", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
    def setup_toolbars(self):
        """메인 툴바 복원: 프로젝트 리스트 Show/Hide, Always on Top, 투명도, 설정 버튼 순"""
        self.main_toolbar = self.addToolBar("메인")
        self.main_toolbar.setMovable(False)

        # 1. 프로젝트 리스트 Show/Hide 버튼
        sidebar_btn = QToolButton()
        sidebar_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        sidebar_btn.setToolTip("프로젝트 리스트 표시/숨김")
        sidebar_btn.clicked.connect(self.toggle_sidebar)
        self.main_toolbar.addWidget(sidebar_btn)

        # 2. Always on Top 버튼
        on_top_btn = QToolButton()
        on_top_btn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarShadeButton))
        on_top_btn.setToolTip("항상 위 (Always on Top)")
        on_top_btn.setCheckable(True)
        on_top_btn.setChecked(self.windowFlags() & Qt.WindowStaysOnTopHint)
        on_top_btn.clicked.connect(self.toggle_always_on_top)
        self.main_toolbar.addWidget(on_top_btn)

        # 3. 투명도 조절 버튼
        opacity_btn = QToolButton()
        opacity_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        opacity_btn.setToolTip("창 투명도 조절")
        opacity_btn.clicked.connect(self.show_opacity_popup)
        self.main_toolbar.addWidget(opacity_btn)

        # 4. 설정 버튼
        settings_btn = QToolButton()
        settings_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        settings_btn.setToolTip("설정")
        settings_btn.clicked.connect(self.open_settings_dialog)
        self.main_toolbar.addWidget(settings_btn)

    def setup_search(self):
        """검색 기능 설정"""
        self.search_toolbar = QToolBar("검색")
        self.search_toolbar.setMovable(False)
        self.addToolBar(Qt.BottomToolBarArea, self.search_toolbar)
        
        # 검색 입력 필드
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색어 입력...")
        self.search_input.returnPressed.connect(self.filter_tasks)
        self.search_toolbar.addWidget(self.search_input)
        
        # 검색 버튼
        search_btn = QToolButton()
        search_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        search_btn.setToolTip("검색")
        search_btn.clicked.connect(self.filter_tasks)
        self.search_toolbar.addWidget(search_btn)
        
        # 초기화 버튼
        clear_btn = QToolButton()
        clear_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        clear_btn.setToolTip("검색 초기화")
        clear_btn.clicked.connect(self.clear_search)
        self.search_toolbar.addWidget(clear_btn)
        
    def filter_tasks(self):
        """할 일 검색"""
        search_text = self.search_input.text().lower()
        if not search_text:
            self.clear_search()
            return
        # 현재 프로젝트의 모든 할 일 검색
        if not self.current_project_name:
            return
        project_data = self.project_list_vm.get_project_info(self.current_project_name)
        found_tasks = []
        for quadrant_idx, quadrant in enumerate(project_data["quadrants"]):
            for task_idx, task in enumerate(quadrant):
                title = (task.get("title") or "").lower()
                details = (task.get("details") or "").lower()
                if (search_text in title or search_text in details):
                    found_tasks.append((quadrant_idx, task_idx, task))
        if not found_tasks:
            QMessageBox.information(self, "검색 결과", "검색 결과가 없습니다.")
            return
        # 검색 결과 표시
        result_dialog = QDialog(self)
        result_dialog.setWindowTitle("검색 결과")
        result_dialog.setMinimumSize(400, 300)
        layout = QVBoxLayout(result_dialog)
        # 결과 리스트
        result_list = QListWidget()
        for quadrant_idx, task_idx, task in found_tasks:
            quadrant_names = ["긴급하고 중요함", "중요하지만 긴급하지 않음",
                            "긴급하지만 중요하지 않음", "긴급하지도 중요하지도 않음"]
            item_text = f"[{quadrant_names[quadrant_idx]}] {task.get('title', '')}"
            if task.get("details"):
                item_text += f"\n{task['details']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, (quadrant_idx, task_idx))
            result_list.addItem(item)
        layout.addWidget(result_list)
        # 버튼
        button_layout = QHBoxLayout()
        open_btn = QPushButton("열기")
        open_btn.clicked.connect(lambda: self._open_search_result(result_list.currentItem(), result_dialog))
        button_layout.addWidget(open_btn)
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(result_dialog.close)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        result_dialog.exec_()

    def _open_search_result(self, item, dialog):
        """검색 결과 항목 열기"""
        if not item:
            return
            
        quadrant_idx, task_idx = item.data(Qt.UserRole)
        dialog.close()
        
        # 해당 사분면으로 이동
        self.quadrant_widgets[quadrant_idx].setFocus()
        
        # 해당 항목 선택
        quadrant = self.quadrant_widgets[quadrant_idx]
        quadrant.list_widget.setCurrentRow(task_idx)
        
    def clear_search(self):
        """검색 초기화"""
        self.search_input.clear()
        for quadrant in self.quadrant_widgets:
            quadrant.list_widget.clearSelection()
            
    def show_task_statistics(self):
        """할 일 통계 표시 (MVVM 구조)"""
        if not self.current_project_name:
            QMessageBox.information(self, "통계", "프로젝트를 선택해주세요.")
            return
        info = self.project_list_vm.get_project_info(self.current_project_name)
        quadrants = info.get("quadrants", [[], [], [], []])
        total_tasks = sum(len(q) for q in quadrants)
        completed_tasks = sum(
            sum(1 for task in q if task.get("checked", False)) for q in quadrants
        )
        # 통계 다이얼로그
        dialog = QDialog(self)
        dialog.setWindowTitle("할 일 통계")
        dialog.setMinimumSize(400, 300)
        layout = QVBoxLayout(dialog)
        summary = QLabel(
            f"총 할 일: {total_tasks}개\n"
            f"완료된 할 일: {completed_tasks}개\n"
            f"완료율: {(completed_tasks/total_tasks*100 if total_tasks > 0 else 0):.1f}%"
        )
        layout.addWidget(summary)
        quadrant_names = ["긴급하고 중요함", "중요하지만 긴급하지 않음",
                         "긴급하지만 중요하지 않음", "긴급하지도 중요하지도 않음"]
        for i, name in enumerate(quadrant_names):
            stats = QLabel(
                f"{name}:\n"
                f"  총 {len(quadrants[i])}개 중 {sum(1 for t in quadrants[i] if t.get('checked', False))}개 완료\n"
                f"  완료율: {(sum(1 for t in quadrants[i] if t.get('checked', False))/len(quadrants[i])*100 if len(quadrants[i]) > 0 else 0):.1f}%"
            )
            layout.addWidget(stats)
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        dialog.exec_()

    def export_task_report(self):
        """할 일 보고서 내보내기 (MVVM 구조)"""
        if not self.current_project_name:
            QMessageBox.information(self, "보고서", "프로젝트를 선택해주세요.")
            return
        info = self.project_list_vm.get_project_info(self.current_project_name)
        quadrants = info.get("quadrants", [[], [], [], []])
        file_path, _ = QFileDialog.getSaveFileName(
            self, "보고서 저장",
            os.path.join(self.data_dir, f"{self.current_project_name}_report.txt"),
            "Text Files (*.txt)"
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"프로젝트: {self.current_project_name}\n")
                f.write(f"생성일: {info.get('created_at', '')}\n")
                f.write(f"최종 수정일: {info.get('updated_at', '')}\n\n")
                quadrant_names = ["긴급하고 중요함", "중요하지만 긴급하지 않음",
                                "긴급하지만 중요하지 않음", "긴급하지도 중요하지도 않음"]
                for i, name in enumerate(quadrant_names):
                    f.write(f"=== {name} ===\n")
                    tasks = quadrants[i]
                    if not tasks:
                        f.write("  할 일 없음\n")
                    else:
                        for task in tasks:
                            status = "✓" if task.get("checked", False) else "□"
                            f.write(f"{status} {task['title']}\n")
                            if task.get("details"):
                                f.write(f"    {task['details']}\n")
                            if task.get("due_date"):
                                f.write(f"    마감일: {task['due_date']}\n")
                            f.write("\n")
                    f.write("\n")
            QMessageBox.information(self, "보고서", "보고서가 저장되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"보고서 저장 중 오류가 발생했습니다:\n{str(e)}")
        
    def toggle_main_toolbar(self):
        """메인 툴바 토글"""
        self.main_toolbar.setVisible(not self.main_toolbar.isVisible())
        
    def toggle_search_toolbar(self):
        """검색 툴바 토글"""
        self.search_toolbar.setVisible(not self.search_toolbar.isVisible())
        
    def show_about_dialog(self):
        """정보 다이얼로그 표시"""
        QMessageBox.about(self, "Anti-ADHD 정보",
            "Anti-ADHD v1.0\n\n"
            "아이젠하워 매트릭스를 활용한 할 일 관리 프로그램\n\n"
            "© 2024 Anti-ADHD Team") 

    def add_new_project(self):
        """새 프로젝트 추가 (MVVM 구조, anti_adhd_pyqt.py의 피드백/예외처 통합)"""
        text, ok = QInputDialog.getText(self, "새 프로젝트", "프로젝트 이름:")
        if ok and text.strip():
            project_name = text.strip()
            if project_name not in self.projects_data:
                self.statusBar.showMessage(f"새 프로젝트 '{project_name}' 생성 중...")
                self.projects_data[project_name] = {"quadrants": [[], [], [], []]}
                item = QListWidgetItem(project_name)
                self.sidebar.addItem(item)
                self.sidebar.setCurrentItem(item)
                self.save_project_to_file(project_name)
                self.statusBar.showMessage(f"새 프로젝트 '{project_name}' 생성 완료", 3000)
            else:
                QMessageBox.warning(self, "중복 오류", "이미 존재하는 프로젝트 이름입니다.")

    def rename_selected_project(self):
        """선택된 프로젝트 이름 변경 (MVVM 구조, anti_adhd_pyqt.py의 피드백/예외처 통합)"""
        current_item = self.sidebar.currentItem()
        if not current_item:
            return
        old_name = current_item.text()
        new_name, ok = QInputDialog.getText(self, "이름 변경", f"'{old_name}'의 새 이름:", text=old_name)
        if ok and new_name.strip() and new_name.strip() != old_name:
            new_name_stripped = new_name.strip()
            if new_name_stripped in self.projects_data:
                QMessageBox.warning(self, "중복 오류", "이미 존재하는 프로젝트 이름입니다.")
                return
            self.projects_data[new_name_stripped] = self.projects_data.pop(old_name)
            current_item.setText(new_name_stripped)
            # 파일 이름 변경 (anti_adhd_pyqt.py 참고)
            old_file_path = os.path.join(self.data_dir, f"project_{old_name}.json")
            new_file_path = os.path.join(self.data_dir, f"project_{new_name_stripped}.json")
            if os.path.exists(old_file_path):
                try:
                    os.rename(old_file_path, new_file_path)
                except OSError as e:
                    QMessageBox.critical(self, "파일 오류", f"프로젝트 파일 이름 변경 실패: {e}")
            if self.auto_save_enabled:
                self.save_project_to_file(new_name_stripped)
            self.statusBar.showMessage(f"프로젝트 이름이 '{old_name}'에서 '{new_name_stripped}'(으)로 변경되었습니다.", 3000)

    def delete_selected_project(self):
        """선택된 프로젝트 삭제 (MVVM 구조, anti_adhd_pyqt.py의 피드백/예외처 통합)"""
        current_item = self.sidebar.currentItem()
        if not current_item:
            return
        project_name = current_item.text()
        reply = QMessageBox.question(self, "프로젝트 삭제", f"'{project_name}' 프로젝트를 삭제하시겠습니까?\n(데이터와 해당 프로젝트 파일 모두 삭제됩니다!)", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            row = self.sidebar.row(current_item)
            self.sidebar.takeItem(row)
            if project_name in self.projects_data:
                del self.projects_data[project_name]
            file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    QMessageBox.critical(self, "파일 오류", f"프로젝트 파일 삭제 실패: {e}")
            if self.sidebar.count() > 0:
                new_row = max(0, row - 1)
                if new_row < self.sidebar.count():
                    self.sidebar.setCurrentRow(new_row)
                else:
                    self.sidebar.setCurrentRow(self.sidebar.count() - 1 if self.sidebar.count() > 0 else -1)
            else:
                self.current_project_name = None
                self.clear_all_quadrants()
            self.statusBar.showMessage(f"'{project_name}' 프로젝트가 삭제되었습니다.", 3000)

    def load_all_projects(self):
        """프로젝트 전체 로드 (MVVM 구조)"""
        # ViewModel이 알아서 로드함
        self.project_list_vm._load_projects()

    def save_project_to_file(self, project_name):
        """프로젝트 저장 (MVVM 구조, anti_adhd_pyqt.py의 데이터 구조 보정/방어코드/피드백 통합)"""
        try:
            info = self.project_list_vm.get_project_info(project_name)
            # 데이터 구조 보정 (anti_adhd_pyqt.py 참고)
            if "quadrants" not in info or not isinstance(info["quadrants"], list) or len(info["quadrants"]) != 4:
                info["quadrants"] = [[], [], [], []]
            for quadrant in info["quadrants"]:
                if not isinstance(quadrant, list):
                    quadrant = []
                for i, item in enumerate(quadrant):
                    if not isinstance(item, dict):
                        current_time = datetime.now().isoformat()
                        quadrant[i] = {
                            "title": str(item),
                            "details": "",
                            "checked": False,
                            "due_date": None,
                            "reminders": [],
                            "created_at": current_time,
                            "modified_at": current_time
                        }
                    else:
                        # 필수 필드 확인 및 추가
                        if "title" not in item:
                            item["title"] = ""
                        if "details" not in item:
                            item["details"] = ""
                        if "checked" not in item:
                            item["checked"] = False
                        if "due_date" not in item:
                            item["due_date"] = None
                        if "reminders" not in item:
                            item["reminders"] = []
                        if "created_at" not in item:
                            item["created_at"] = datetime.now().isoformat()
                        if "modified_at" not in item:
                            item["modified_at"] = datetime.now().isoformat()
            self.project_usecase.save_project(project_name, info)
            self.statusBar.showMessage(f"'{project_name}' 저장 완료", 2000)
        except Exception as e:
            self.statusBar.showMessage(f"'{project_name}' 저장 중 오류: {e}", 4000)

    def load_project_from_file(self, project_name):
        """프로젝트 로드 (MVVM 구조)"""
        # ViewModel이 알아서 로드함
        pass

    def select_initial_project(self):
        """초기 프로젝트 선택"""
        if self.sidebar.count() > 0:
            self.sidebar.setCurrentRow(0)
            
    def update_quadrant_display(self, project_name):
        """프로젝트의 사분면 표시 업데이트 (MVVM 구조)"""
        if not project_name:
            return
        # 각 사분면 ViewModel의 _load_tasks()만 호출
        for widget in self.quadrant_widgets:
            widget.viewmodel.project_name = project_name
            widget.viewmodel._load_tasks()

    def clear_all_quadrants(self):
        """모든 사분면 초기화 (MVVM 구조)"""
        for widget in self.quadrant_widgets:
            widget.viewmodel.clear_tasks()
            
    def update_project_status_label(self):
        """프로젝트 상태 레이블 업데이트 (MVVM 구조)"""
        if not self.current_project_name:
            self.project_status_label.setText("프로젝트 없음")
            return
        info = self.project_list_vm.get_project_info(self.current_project_name)
        quadrants = info.get("quadrants", [[], [], [], []])
        total_tasks = sum(len(q) for q in quadrants)
        completed_tasks = sum(
            sum(1 for task in q if task.get("checked", False)) for q in quadrants
        )
        status_text = f"프로젝트: {self.current_project_name} | "
        status_text += f"할 일: {total_tasks}개 | "
        status_text += f"완료: {completed_tasks}개"
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            status_text += f" ({completion_rate:.1f}%)"
        self.project_status_label.setText(status_text)

    def load_settings(self):
        """설정 로드"""
        # 데이터 디렉토리
        self.data_dir = self.settings.value("dataDir", os.path.join(os.path.expanduser("~"), "anti_adhd_data"))
        
        # 자동 저장
        self.auto_save_enabled = self.settings.value("autoSave", True, type=bool)
        
        # 다크 모드
        self.dark_mode = self.settings.value("darkMode", False, type=bool)
        self.apply_theme()
        
        # 항상 위
        always_on_top = self.settings.value("alwaysOnTop", False, type=bool)
        self.set_always_on_top(always_on_top)
        
        # 창 투명도
        opacity = self.settings.value("windowOpacity", 1.0, type=float)
        self.set_window_opacity(opacity)
        
        # 창 크기/위치
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
            
    def save_settings(self):
        """설정 저장"""
        self.settings.setValue("dataDir", self.data_dir)
        self.settings.setValue("autoSave", self.auto_save_enabled)
        self.settings.setValue("darkMode", self.dark_mode)
        self.settings.setValue("alwaysOnTop", self.windowFlags() & Qt.WindowStaysOnTopHint)
        self.settings.setValue("windowOpacity", self.window_opacity)
        self.settings.setValue("geometry", self.saveGeometry())
        
    def open_settings_dialog(self):
        """설정 다이얼로그 표시"""
        dialog = SettingsDialog(self.data_dir, self.settings.fileName(), self)
        if dialog.exec_() == QDialog.Accepted:
            # 설정 변경 사항 적용
            self.data_dir = dialog.data_dir
            self.auto_save_enabled = dialog.auto_save_checkbox.isChecked()
            
            # 데이터 디렉토리 변경 시 프로젝트 다시 로드
            if dialog.data_dir_changed:
                self.projects_data.clear()
                self.sidebar.clear()
                self.load_all_projects()
                self.select_initial_project()
                
            # 설정 저장
            self.save_settings()
            
    def set_always_on_top(self, enabled):
        """항상 위 설정"""
        if enabled:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
        
    def toggle_always_on_top(self):
        """항상 위 토글"""
        self.set_always_on_top(self.windowFlags() & Qt.WindowStaysOnTopHint)
        self.update_always_on_top_icon()
        
    def update_always_on_top_icon(self):
        """항상 위 아이콘 업데이트"""
        is_on_top = self.windowFlags() & Qt.WindowStaysOnTopHint
        icon = self.style().standardIcon(
            QStyle.SP_ArrowUp if is_on_top else QStyle.SP_ArrowDown
        )
        self.findChild(QAction, "always_on_top_action").setIcon(icon)
        
    def set_window_opacity(self, opacity):
        """창 투명도 설정"""
        self.window_opacity = max(0.1, min(1.0, opacity))
        self.setWindowOpacity(self.window_opacity)
        
    def setup_dark_mode(self):
        """다크 모드 설정"""
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow, QDialog {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMenuBar {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMenuBar::item:selected {
                    background-color: #3b3b3b;
                }
                QMenu {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMenu::item:selected {
                    background-color: #3b3b3b;
                }
                QToolBar {
                    background-color: #2b2b2b;
                    border: none;
                }
                QStatusBar {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QLineEdit, QTextEdit {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #4b4b4b;
                }
                QPushButton {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #4b4b4b;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #4b4b4b;
                }
                QListWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    border: 1px solid #4b4b4b;
                }
                QListWidget::item:selected {
                    background-color: #3b3b3b;
                }
                QListWidget::item:hover {
                    background-color: #4b4b4b;
                }
            """)
        else:
            self.setStyleSheet("")
            
    def toggle_dark_mode(self):
        """다크 모드 토글"""
        self.dark_mode = not self.dark_mode
        self.setup_dark_mode()
        self.save_settings()
        
    def apply_theme(self):
        """테마 적용"""
        self.setup_dark_mode()
        # 추가 테마 설정이 있다면 여기에 구현 

    def check_due_reminders(self):
        """마감일 리마인더 체크"""
        if not self.current_project_name:
            return
            
        project_data = self.projects_data[self.current_project_name]
        now = datetime.now()
        
        for quadrant in project_data["quadrants"]:
            for task in quadrant:
                if not task.get("due_date"):
                    continue
                    
                try:
                    due_date = datetime.fromisoformat(task["due_date"])
                    time_diff = due_date - now
                    
                    # 마감 1시간 전
                    if timedelta(hours=0) <= time_diff <= timedelta(hours=1):
                        self.show_reminder_popup(task["title"], due_date, minutes=60)
                        
                    # 마감 30분 전
                    elif timedelta(minutes=0) <= time_diff <= timedelta(minutes=30):
                        self.show_reminder_popup(task["title"], due_date, minutes=30)
                        
                    # 마감 10분 전
                    elif timedelta(minutes=0) <= time_diff <= timedelta(minutes=10):
                        self.show_reminder_popup(task["title"], due_date, minutes=10)
                        
                    # 마감 지남
                    elif time_diff < timedelta(minutes=0):
                        self.show_reminder_popup(task["title"], due_date, overdue=True)
                        
                except Exception:
                    continue
                    
    def show_reminder_popup(self, title, due_dt, minutes=None, overdue=False):
        """리마인더 팝업 표시"""
        msg = QMessageBox(self)
        msg.setWindowTitle("할 일 리마인더")
        
        if overdue:
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"마감이 지난 할 일이 있습니다!")
            msg.setInformativeText(f"'{title}'\n마감일: {due_dt.strftime('%Y-%m-%d %H:%M')}")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"마감 {minutes}분 전입니다!")
            msg.setInformativeText(f"'{title}'\n마감일: {due_dt.strftime('%Y-%m-%d %H:%M')}")
            
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def _auto_backup(self):
        if not self.auto_save_enabled or not self.current_project_name:
            return
        try:
            backup_dir = os.path.join(self.data_dir, "backups")
            core_backup_project_file(self.data_dir, self.current_project_name, backup_dir)
            self._cleanup_old_backups()
        except Exception as e:
            print(f"자동 백업 중 오류 발생: {str(e)}")
            
    def _cleanup_old_backups(self):
        """오래된 백업 파일 정리"""
        backup_dir = os.path.join(self.data_dir, "backups")
        if not os.path.exists(backup_dir):
            return
            
        # 백업 파일 목록
        backup_files = []
        for file_name in os.listdir(backup_dir):
            if file_name.endswith(".json"):
                file_path = os.path.join(backup_dir, file_name)
                backup_files.append((file_path, os.path.getmtime(file_path)))
                
        # 수정일 기준 정렬
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # 최근 10개만 유지
        for file_path, _ in backup_files[10:]:
            try:
                os.remove(file_path)
            except Exception:
                continue
                
    def toggle_sidebar(self):
        """사이드바(ProjectListWidget) 표시/숨김 토글"""
        visible = not self.sidebar.isVisible()
        self.sidebar.setVisible(visible)
        # 메뉴 액션 체크 상태 동기화
        menubar = self.menuBar()
        file_menu = menubar.findChild(QMenu, "파일")
        view_menu = None
        for action in menubar.actions():
            if action.text() == "보기":
                view_menu = action.menu()
                break
        if view_menu:
            for action in view_menu.actions():
                if action.text() == "사이드바":
                    action.setChecked(visible)
                    break 

    def closeEvent(self, event):
        """창 닫기 이벤트"""
        # 현재 프로젝트 저장
        if self.current_project_name:
            self.save_project_to_file(self.current_project_name)
            
        # 설정 저장
        self.save_settings()
        
        event.accept() 

    def save_current_project(self):
        """현재 선택된 프로젝트를 저장"""
        if self.current_project_name:
            self.save_project_to_file(self.current_project_name)
        else:
            QMessageBox.information(self, "저장", "저장할 프로젝트가 없습니다.") 

    def save_project_as(self):
        """현재 프로젝트를 다른 이름으로 저장"""
        if not self.current_project_name:
            QMessageBox.information(self, "다른 이름으로 저장", "저장할 프로젝트가 없습니다.")
            return
        new_name, ok = QInputDialog.getText(self, "다른 이름으로 저장", "새 프로젝트 이름:")
        if not ok or not new_name:
            return
        if new_name in self.projects_data:
            QMessageBox.warning(self, "경고", "이미 존재하는 프로젝트 이름입니다.")
            return
        # 데이터 복사 및 저장
        import copy
        new_data = copy.deepcopy(self.projects_data[self.current_project_name])
        new_data["created_at"] = datetime.now().isoformat()
        new_data["updated_at"] = datetime.now().isoformat()
        self.projects_data[new_name] = new_data
        self.save_project_to_file(new_name)
        # UI에 새 프로젝트 추가
        item = QListWidgetItem(new_name)
        self.sidebar.addItem(item)
        self.sidebar.setCurrentItem(item)
        self.current_project_name = new_name
        self.update_project_status_label()
        QMessageBox.information(self, "다른 이름으로 저장", f"프로젝트가 '{new_name}'(으)로 저장되었습니다.") 

    def import_project_file(self):
        """외부 JSON 파일을 프로젝트로 가져오기"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "프로젝트 파일 가져오기", self.data_dir, "JSON Files (*.json)"
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 프로젝트 이름 결정
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            name, ok = QInputDialog.getText(self, "프로젝트 이름", "가져올 프로젝트 이름:", text=base_name)
            if not ok or not name:
                return
            if name in self.projects_data:
                QMessageBox.warning(self, "경고", "이미 존재하는 프로젝트 이름입니다.")
                return
            # 데이터 저장 및 UI 반영
            data["created_at"] = datetime.now().isoformat()
            data["updated_at"] = datetime.now().isoformat()
            self.projects_data[name] = data
            self.save_project_to_file(name)
            item = QListWidgetItem(name)
            self.sidebar.addItem(item)
            self.sidebar.setCurrentItem(item)
            self.current_project_name = name
            self.update_project_status_label()
            QMessageBox.information(self, "가져오기", f"프로젝트 '{name}'이(가) 성공적으로 가져와졌습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"가져오기 중 오류가 발생했습니다:\n{str(e)}") 

    def on_project_selection_changed(self, project_name: str):
        """프로젝트 선택 변경 시 호출 (MVVM 구조, anti_adhd_pyqt.py의 피드백/방어코드/상태바 메시지 통합)"""
        # 이전 프로젝트 저장 (자동 저장 옵션에 따라)
        if self.current_project_name and self.auto_save_enabled:
            try:
                self.save_project_to_file(self.current_project_name)
                self.statusBar.showMessage(f"'{self.current_project_name}' 저장 완료", 2000)
            except Exception as e:
                self.statusBar.showMessage(f"'{self.current_project_name}' 저장 중 오류: {e}", 4000)
        self.current_project_name = project_name
        if project_name:
            for widget in self.quadrant_widgets:
                widget.viewmodel.project_name = project_name
                widget.viewmodel._load_tasks()
            self.statusBar.showMessage(f"'{project_name}' 프로젝트로 전환", 2000)
        else:
            for widget in self.quadrant_widgets:
                widget.viewmodel.project_name = ""
                widget.viewmodel.clear_tasks()
            self.statusBar.showMessage("프로젝트 없음", 2000)
        self.update_project_status_label() 

    def show_opacity_popup(self):
        """창 투명도 조절 팝업"""
        value, ok = QInputDialog.getDouble(self, "창 투명도", "0.1~1.0 사이의 값을 입력하세요:", value=self.window_opacity, min=0.1, max=1.0, decimals=2)
        if ok:
            self.set_window_opacity(value) 