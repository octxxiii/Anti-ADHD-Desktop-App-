"""
Main Window View - PyQt6 기반 메인 윈도우
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QToolBar, QStatusBar, QMessageBox, QFileDialog,
    QInputDialog, QProgressBar, QLabel, QListWidget, QListWidgetItem,
    QPushButton
)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from typing import Optional

from .base_view import BaseView
from .eisenhower_widget import EisenhowerWidget
from .project_list_widget import ProjectListWidget
from .settings_dialog import SettingsDialog
from ..viewmodels.main_viewmodel import MainViewModel
from ..models.task_model import Quadrant
from ..models.translation_service import tr, set_language, Language


class MainWindow(QMainWindow, BaseView[MainViewModel]):
    """메인 윈도우"""
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        BaseView.__init__(self, parent=parent)
        
        self._setup_ui()
        self._setup_menus()
        self._setup_toolbar()
        self._setup_statusbar()
        
        # ViewModel 생성 및 설정
        viewmodel = MainViewModel()
        self.set_viewmodel(viewmodel)
    
    def _setup_ui(self) -> None:
        """UI 초기화"""
        self.setWindowTitle("Anti-ADHD - Eisenhower Matrix")
        self.setMinimumSize(800, 600)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 스플리터
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # 프로젝트 리스트 위젯
        self.project_list_widget = ProjectListWidget()
        self.splitter.addWidget(self.project_list_widget)
        
        # 아이젠하워 매트릭스 위젯
        self.eisenhower_widget = EisenhowerWidget()
        self.splitter.addWidget(self.eisenhower_widget)
        
        # 스플리터 비율 설정
        self.splitter.setSizes([250, 550])
        
        # 위젯 연결
        self.project_list_widget.project_selected.connect(self._on_project_selected)
        self.project_list_widget.project_create_requested.connect(self._on_create_project)
        self.project_list_widget.project_delete_requested.connect(self._on_delete_project)
        self.project_list_widget.project_rename_requested.connect(self._on_rename_project)
        self.project_list_widget.project_move_up_requested.connect(self._on_move_project_up)
        self.project_list_widget.project_move_down_requested.connect(self._on_move_project_down)
    
    def _setup_menus(self) -> None:
        """메뉴 설정"""
        # 기존 메뉴바 클리어
        self.menuBar().clear()
        
        menubar = self.menuBar()
        
        # 파일 메뉴
        file_menu = menubar.addMenu(tr("File") + "(&F)")
        
        self.new_project_action = QAction(tr("New Project") + "(&N)", self)
        self.new_project_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_project_action.triggered.connect(self._on_create_project)
        file_menu.addAction(self.new_project_action)
        
        file_menu.addSeparator()
        
        self.import_project_action = QAction(tr("Import Project") + "(&I)", self)
        self.import_project_action.triggered.connect(self._on_import_project)
        file_menu.addAction(self.import_project_action)
        
        self.export_project_action = QAction(tr("Export Project") + "(&E)", self)
        self.export_project_action.triggered.connect(self._on_export_project)
        file_menu.addAction(self.export_project_action)
        
        file_menu.addSeparator()
        
        self.exit_action = QAction(tr("Exit") + "(&X)", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)
        file_menu.addAction(self.exit_action)
        
        # 편집 메뉴
        edit_menu = menubar.addMenu(tr("Edit") + "(&E)")
        
        self.add_task_action = QAction(tr("Add Task") + "(&A)", self)
        self.add_task_action.setShortcut(QKeySequence("Ctrl+T"))
        self.add_task_action.triggered.connect(self._on_add_task_shortcut)
        edit_menu.addAction(self.add_task_action)
        
        # 보기 메뉴
        view_menu = menubar.addMenu(tr("View") + "(&V)")
        
        self.toggle_sidebar_action = QAction(tr("Show Sidebar") + "(&S)", self)
        self.toggle_sidebar_action.setCheckable(True)
        self.toggle_sidebar_action.setChecked(True)
        self.toggle_sidebar_action.triggered.connect(self._on_toggle_sidebar)
        view_menu.addAction(self.toggle_sidebar_action)
        
        self.toggle_toolbar_action = QAction(tr("Show Toolbar") + "(&T)", self)
        self.toggle_toolbar_action.setCheckable(True)
        self.toggle_toolbar_action.setChecked(True)
        self.toggle_toolbar_action.triggered.connect(self._on_toggle_toolbar)
        view_menu.addAction(self.toggle_toolbar_action)
        
        self.toggle_statusbar_action = QAction(tr("Show Statusbar") + "(&B)", self)
        self.toggle_statusbar_action.setCheckable(True)
        self.toggle_statusbar_action.setChecked(True)
        self.toggle_statusbar_action.triggered.connect(self._on_toggle_statusbar)
        view_menu.addAction(self.toggle_statusbar_action)
        
        view_menu.addSeparator()
        
        self.always_on_top_action = QAction(tr("Always on Top") + "(&O)", self)
        self.always_on_top_action.setCheckable(True)
        self.always_on_top_action.triggered.connect(self._on_toggle_always_on_top)
        view_menu.addAction(self.always_on_top_action)
        
        # 도구 메뉴
        tools_menu = menubar.addMenu(tr("Tools") + "(&T)")
        
        self.settings_action = QAction(tr("Settings") + "(&S)", self)
        self.settings_action.triggered.connect(self._on_show_settings)
        tools_menu.addAction(self.settings_action)
        
        tools_menu.addSeparator()
        
        self.statistics_action = QAction(tr("Statistics") + "(&T)", self)
        self.statistics_action.triggered.connect(self._on_show_statistics)
        tools_menu.addAction(self.statistics_action)
        
        # 도움말 메뉴
        help_menu = menubar.addMenu(tr("Help") + "(&H)")
        
        self.about_action = QAction(tr("About") + "(&A)", self)
        self.about_action.triggered.connect(self._on_show_about)
        help_menu.addAction(self.about_action)
    
    def _setup_toolbar(self) -> None:
        """툴바 설정"""
        # 기존 툴바 모두 제거
        for toolbar in self.findChildren(QToolBar):
            self.removeToolBar(toolbar)
        
        # 툴바를 생성하지 않음 (메뉴만 사용)
    
    def _setup_statusbar(self) -> None:
        """상태바 설정"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 상태 레이블
        self.status_label = QLabel("준비")
        self.status_bar.addWidget(self.status_label)
        
        # 프로그레스 바 (로딩 시 표시)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 프로젝트 정보 레이블
        self.project_info_label = QLabel()
        self.status_bar.addPermanentWidget(self.project_info_label)
    
    def _setup_shortcuts(self) -> None:
        """단축키 설정"""
        # 이미 메뉴에서 설정됨
        pass
    
    def _connect_viewmodel(self) -> None:
        """ViewModel 연결"""
        super()._connect_viewmodel()
        
        if self._viewmodel:
            self._viewmodel.projects_changed.connect(self._on_projects_changed)
            self._viewmodel.current_project_changed.connect(self._on_current_project_changed)
            self._viewmodel.settings_changed.connect(self._on_settings_changed)
            self._viewmodel.auto_save_triggered.connect(self._on_auto_save_triggered)
    
    def _update_from_viewmodel(self) -> None:
        """ViewModel에서 UI 업데이트"""
        if not self._viewmodel:
            return
        
        # 프로젝트 목록 업데이트
        self.project_list_widget.set_projects(self._viewmodel.projects)
        
        # 현재 프로젝트 업데이트
        if self._viewmodel.current_project:
            self.project_list_widget.set_current_project(self._viewmodel.current_project)
            self.eisenhower_widget.set_viewmodel(self._viewmodel)
            self._update_project_info()
        
        # 설정 적용
        self._apply_settings()
    
    def _apply_settings(self) -> None:
        """설정 적용"""
        if not self._viewmodel:
            return
        
        settings = self._viewmodel.settings
        
        # 창 설정
        window_settings = settings.window_settings
        self.setWindowOpacity(window_settings.opacity)
        
        # 항상 위 설정
        flags = self.windowFlags()
        if window_settings.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()  # 플래그 변경 후 다시 표시
        
        # UI 요소 표시/숨김
        self.project_list_widget.setVisible(settings.sidebar_visible)
        # 툴바는 제거되었으므로 설정하지 않음
        self.status_bar.setVisible(settings.statusbar_visible)
        
        # 메뉴 체크 상태 업데이트
        self.toggle_sidebar_action.setChecked(settings.sidebar_visible)
        self.toggle_toolbar_action.setChecked(settings.toolbar_visible)
        self.toggle_statusbar_action.setChecked(settings.statusbar_visible)
        self.always_on_top_action.setChecked(window_settings.always_on_top)
    
    def _update_project_info(self) -> None:
        """프로젝트 정보 업데이트"""
        if not self._viewmodel or not self._viewmodel.current_project:
            self.project_info_label.setText("")
            return
        
        project = self._viewmodel.current_project
        stats = self._viewmodel.get_project_statistics()
        
        info_text = f"{project.name} | 할 일: {stats.get('total_tasks', 0)} | 완료: {stats.get('completed_tasks', 0)}"
        self.project_info_label.setText(info_text)
    
    # Slots
    @pyqtSlot()
    def _on_projects_changed(self) -> None:
        """프로젝트 목록 변경"""
        if self._viewmodel:
            self.project_list_widget.set_projects(self._viewmodel.projects)
    
    @pyqtSlot()
    def _on_current_project_changed(self) -> None:
        """현재 프로젝트 변경"""
        if self._viewmodel and self._viewmodel.current_project:
            self.project_list_widget.set_current_project(self._viewmodel.current_project)
            self.eisenhower_widget.set_viewmodel(self._viewmodel)
            self._update_project_info()
            # 프로젝트 목록도 업데이트 (퍼센티지 반영)
            self.project_list_widget.set_projects(self._viewmodel.projects)
    
    @pyqtSlot()
    def _on_settings_changed(self) -> None:
        """설정 변경"""
        self._apply_settings()
    
    @pyqtSlot()
    def _on_auto_save_triggered(self) -> None:
        """자동 저장 실행"""
        self.status_label.setText("자동 저장됨")
        QTimer.singleShot(2000, lambda: self.status_label.setText("준비"))
    
    @pyqtSlot(str)
    def _on_project_selected(self, project_id: str) -> None:
        """프로젝트 선택"""
        if self._viewmodel:
            self._viewmodel.set_current_project_by_id(project_id)
    
    @pyqtSlot()
    def _on_create_project(self) -> None:
        """프로젝트 생성"""
        name, ok = QInputDialog.getText(self, "새 프로젝트", "프로젝트 이름:")
        if ok and name.strip():
            if self._viewmodel:
                success = self._viewmodel.create_project(name.strip())
                if success:
                    self.status_label.setText("프로젝트가 생성되었습니다")
                    QTimer.singleShot(2000, lambda: self.status_label.setText("준비"))
    
    @pyqtSlot(str)
    def _on_delete_project(self, project_id: str) -> None:
        """프로젝트 삭제"""
        reply = QMessageBox.question(
            self, "프로젝트 삭제", 
            "정말로 이 프로젝트를 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes and self._viewmodel:
            success = self._viewmodel.delete_project(project_id)
            if success:
                self.status_label.setText("프로젝트가 삭제되었습니다")
                QTimer.singleShot(2000, lambda: self.status_label.setText("준비"))
    
    @pyqtSlot(str)
    def _on_rename_project(self, project_id: str) -> None:
        """프로젝트 이름 변경"""
        if not self._viewmodel:
            return
        
        # 현재 이름 가져오기
        project = next((p for p in self._viewmodel.projects if p.id == project_id), None)
        if not project:
            return
        
        new_name, ok = QInputDialog.getText(
            self, tr("Rename Project"), 
            tr("New name") + ":", text=project.name
        )
        
        if ok and new_name.strip():
            success = self._viewmodel.rename_project(project_id, new_name.strip())
            if success:
                self.status_label.setText(tr("Project renamed"))
                QTimer.singleShot(2000, lambda: self.status_label.setText(tr("Ready")))
    
    @pyqtSlot(str)
    def _on_move_project_up(self, project_id: str) -> None:
        """프로젝트 위로 이동"""
        if self._viewmodel:
            success = self._viewmodel.move_project_up(project_id)
            if success:
                self.status_label.setText(tr("Project moved up"))
                QTimer.singleShot(2000, lambda: self.status_label.setText(tr("Ready")))
    
    @pyqtSlot(str)
    def _on_move_project_down(self, project_id: str) -> None:
        """프로젝트 아래로 이동"""
        if self._viewmodel:
            success = self._viewmodel.move_project_down(project_id)
            if success:
                self.status_label.setText(tr("Project moved down"))
                QTimer.singleShot(2000, lambda: self.status_label.setText(tr("Ready")))
    
    @pyqtSlot(str, str, str)
    def _on_task_added(self, quadrant_str: str, title: str, description: str) -> None:
        """할 일 추가"""
        if not self._viewmodel:
            return
        
        try:
            quadrant = Quadrant(quadrant_str)
            success = self._viewmodel.add_task(title, quadrant, description)
            if success:
                self._update_project_info()
        except ValueError:
            self._on_error_occurred(f"잘못된 사분면: {quadrant_str}")
    
    @pyqtSlot(str, dict)
    def _on_task_updated(self, task_id: str, updates: dict) -> None:
        """할 일 업데이트"""
        if self._viewmodel:
            success = self._viewmodel.update_task(task_id, **updates)
            if success:
                self._update_project_info()
                # 프로젝트 목록 퍼센티지 업데이트
                self.project_list_widget.set_projects(self._viewmodel.projects)
    
    @pyqtSlot(str)
    def _on_task_deleted(self, task_id: str) -> None:
        """할 일 삭제"""
        if self._viewmodel:
            success = self._viewmodel.delete_task(task_id)
            if success:
                self._update_project_info()
                # 프로젝트 목록 퍼센티지 업데이트
                self.project_list_widget.set_projects(self._viewmodel.projects)
    
    @pyqtSlot()
    def _on_add_task_shortcut(self) -> None:
        """할 일 추가 단축키"""
        # 기본적으로 첫 번째 사분면에 추가
        self.eisenhower_widget.focus_first_quadrant()
    
    @pyqtSlot()
    def _on_toggle_sidebar(self) -> None:
        """사이드바 토글"""
        if self._viewmodel:
            visible = not self._viewmodel.settings.sidebar_visible
            self._viewmodel.update_settings(sidebar_visible=visible)
    
    @pyqtSlot()
    def _on_toggle_toolbar(self) -> None:
        """툴바 토글"""
        if self._viewmodel:
            visible = not self._viewmodel.settings.toolbar_visible
            self._viewmodel.update_settings(toolbar_visible=visible)
    
    @pyqtSlot()
    def _on_toggle_statusbar(self) -> None:
        """상태바 토글"""
        if self._viewmodel:
            visible = not self._viewmodel.settings.statusbar_visible
            self._viewmodel.update_settings(statusbar_visible=visible)
    
    @pyqtSlot()
    def _on_toggle_always_on_top(self) -> None:
        """항상 위 토글"""
        if self._viewmodel:
            always_on_top = not self._viewmodel.settings.window_settings.always_on_top
            self._viewmodel.update_settings(window_settings={'always_on_top': always_on_top})
    
    @pyqtSlot()
    def _on_show_settings(self) -> None:
        """설정 다이얼로그 표시"""
        if self._viewmodel:
            dialog = SettingsDialog(self._viewmodel.settings, self)
            
            # 설정 변경 시그널 연결
            dialog.settings_changed.connect(self._on_settings_dialog_changed)
            
            dialog.exec()
    
    @pyqtSlot(dict)
    def _on_settings_dialog_changed(self, changes: dict) -> None:
        """설정 다이얼로그에서 설정 변경됨"""
        try:
            if self._viewmodel:
                # ViewModel의 설정 업데이트
                success = self._viewmodel.update_settings(**changes)
                if success:
                    # 메뉴 다시 생성 (언어 변경 반영)
                    self._setup_menus()
                    # 설정 적용
                    self._apply_settings()
                else:
                    QMessageBox.warning(self, "경고", "일부 설정이 저장되지 않았습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"설정 적용 중 오류가 발생했습니다:\n{str(e)}")
    
    @pyqtSlot()
    def _on_show_statistics(self) -> None:
        """통계 다이얼로그 표시"""
        if not self._viewmodel or not self._viewmodel.current_project:
            QMessageBox.information(self, tr("Statistics"), tr("Please select a project first."))
            return
        
        stats = self._viewmodel.get_project_statistics()
        
        message = f"""{tr("Project")}: {self._viewmodel.current_project.name}

{tr("Total tasks")}: {stats['total_tasks']}
{tr("Completed tasks")}: {stats['completed_tasks']}
{tr("Pending tasks")}: {stats['pending_tasks']}
{tr("Completion rate")}: {stats['completion_rate']:.1f}%

{tr("Quadrant Statistics")}:
• {tr("Urgent and Important")}: {stats['quadrant_stats']['urgent_important']['total']}
• {tr("Important but Not Urgent")}: {stats['quadrant_stats']['not_urgent_important']['total']}
• {tr("Urgent but Not Important")}: {stats['quadrant_stats']['urgent_not_important']['total']}
• {tr("Neither Urgent nor Important")}: {stats['quadrant_stats']['not_urgent_not_important']['total']}"""
        
        QMessageBox.information(self, tr("Project Statistics"), message)
    
    @pyqtSlot()
    def _on_show_about(self) -> None:
        """정보 다이얼로그 표시"""
        QMessageBox.about(
            self, tr("About Anti-ADHD"),
            f"""Anti-ADHD v2.0
            
{tr("Eisenhower Matrix Task Management Tool for ADHD")}

{tr("Developer")}: octaxii
{tr("License")}: MIT License
GitHub: https://github.com/octaxii/Anti-ADHD"""
        )
    
    @pyqtSlot()
    def _on_import_project(self) -> None:
        """프로젝트 가져오기"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "프로젝트 가져오기", "", "JSON 파일 (*.json)"
        )
        
        if file_path and self._viewmodel:
            success = self._viewmodel.import_project(file_path)
            if success:
                self.status_label.setText("프로젝트를 가져왔습니다")
                QTimer.singleShot(2000, lambda: self.status_label.setText("준비"))
    
    @pyqtSlot()
    def _on_export_project(self) -> None:
        """프로젝트 내보내기"""
        if not self._viewmodel or not self._viewmodel.current_project:
            QMessageBox.information(self, "내보내기", "내보낼 프로젝트를 먼저 선택해주세요.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "프로젝트 내보내기", 
            f"{self._viewmodel.current_project.name}.json",
            "JSON 파일 (*.json)"
        )
        
        if file_path:
            success = self._viewmodel.export_project(self._viewmodel.current_project.id, file_path)
            if success:
                self.status_label.setText("프로젝트를 내보냈습니다")
                QTimer.singleShot(2000, lambda: self.status_label.setText("준비"))
    
    def _on_loading_changed(self, is_loading: bool) -> None:
        """로딩 상태 변경"""
        self.progress_bar.setVisible(is_loading)
        if is_loading:
            self.progress_bar.setRange(0, 0)  # 무한 프로그레스
            self.status_label.setText("처리 중...")
        else:
            self.status_label.setText("준비")
    
    def _on_error_occurred(self, message: str) -> None:
        """에러 발생"""
        QMessageBox.critical(self, "오류", message)
        self.status_label.setText("오류 발생")
        QTimer.singleShot(3000, lambda: self.status_label.setText("준비"))