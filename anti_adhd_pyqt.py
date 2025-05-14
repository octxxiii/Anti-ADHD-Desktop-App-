from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter, QListWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLineEdit, QPushButton, QAction, QMenu, QGridLayout, QTextEdit, QInputDialog,
    QMessageBox, QFileDialog, QListWidgetItem, QDialog, QLabel, QCheckBox, QSlider, QStyle, QSizePolicy,
    QTabWidget, QFormLayout, QToolButton, QFrame
)
from PyQt5.QtCore import Qt, QSettings, QUrl, QPoint, QSize
from PyQt5.QtGui import QIcon, QDesktopServices, QPainter, QPen, QColor, QPixmap, QCursor
import sys
import os
import json
import zipfile
import shutil

# --- 유틸리티 함수 ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- 설정 대화상자 클래스 ---
class SettingsDialog(QDialog):
    def __init__(self, current_data_dir, settings_file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("애플리케이션 설정")
        self.setModal(True)
        self.main_window_ref = parent
        self.current_data_dir = current_data_dir
        self.new_data_dir = current_data_dir
        self.settings_file_path = settings_file_path
        self.settings = QSettings(self.settings_file_path, QSettings.IniFormat)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # "일반" 탭 생성 및 UI 구성
        self.general_tab = QWidget()
        self.tab_widget.addTab(self.general_tab, "일반")
        self.setup_general_tab()

        # "정보" 탭 생성 및 UI 구성
        self.info_tab = QWidget()
        self.tab_widget.addTab(self.info_tab, "정보")
        self.setup_info_tab()

        # 하단 버튼 레이아웃 ("닫기" 버튼만)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.close_button = QPushButton("닫기")
        self.close_button.clicked.connect(self.accept_settings)
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)
        button_layout.setContentsMargins(0, 10, 0, 0)

        self.setLayout(main_layout)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

    def setup_general_tab(self):
        layout = QVBoxLayout(self.general_tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # 데이터 경로 설정 그룹 (기존 UI 재활용)
        data_dir_group = QGroupBox("데이터 저장 경로")
        data_dir_group_layout = QVBoxLayout()
        data_dir_group_layout.setSpacing(8)
        data_dir_group_layout.setContentsMargins(10, 5, 10, 10)

        path_input_layout = QHBoxLayout()
        self.data_dir_label = QLabel("현재 경로:")
        self.data_dir_edit = QLineEdit(self.current_data_dir)
        self.data_dir_edit.setReadOnly(True)
        self.browse_button = QPushButton("폴더 변경...")
        self.browse_button.clicked.connect(self.browse_data_directory)
        path_input_layout.addWidget(self.data_dir_label)
        path_input_layout.addWidget(self.data_dir_edit, 1)
        path_input_layout.addWidget(self.browse_button)
        data_dir_group_layout.addLayout(path_input_layout)

        path_notice_label = QLabel("경로 변경 후 프로그램을 재시작해야 적용됩니다.")
        path_notice_label.setStyleSheet("font-size: 9pt; color: gray;")
        data_dir_group_layout.addWidget(path_notice_label, 0, Qt.AlignTop)
        data_dir_group.setLayout(data_dir_group_layout)
        layout.addWidget(data_dir_group)

        # 자동 저장 그룹
        auto_save_group = QGroupBox("자동 저장")
        auto_save_layout = QVBoxLayout()
        auto_save_layout.setContentsMargins(10, 5, 10, 10)
        self.auto_save_checkbox = QCheckBox("애플리케이션 상태 자동 저장")
        self.auto_save_checkbox.setChecked(self.settings.value("general/autoSaveEnabled", True, type=bool))
        self.auto_save_checkbox.stateChanged.connect(self._on_auto_save_changed)
        auto_save_layout.addWidget(self.auto_save_checkbox)
        auto_save_group.setLayout(auto_save_layout)
        layout.addWidget(auto_save_group)

        # 업데이트 그룹
        update_group = QGroupBox("업데이트")
        update_layout = QVBoxLayout()
        update_layout.setContentsMargins(10, 5, 10, 10)
        self.check_updates_checkbox = QCheckBox("시작 시 업데이트 자동 확인")
        self.check_updates_checkbox.setChecked(self.settings.value("general/checkUpdatesOnStart", True, type=bool))
        self.check_updates_checkbox.stateChanged.connect(self._on_check_updates_changed)
        self.check_now_button = QPushButton("지금 업데이트 확인")
        self.check_now_button.clicked.connect(self.perform_update_check)
        update_layout.addWidget(self.check_updates_checkbox)
        update_layout.addWidget(self.check_now_button, 0, Qt.AlignLeft)
        update_group.setLayout(update_layout)
        layout.addWidget(update_group)

        # 데이터 관리 그룹
        data_management_group = QGroupBox("데이터 관리")
        data_management_layout = QHBoxLayout()
        data_management_layout.setSpacing(10)
        data_management_layout.setContentsMargins(10, 10, 10, 10)
        self.backup_data_button = QPushButton("데이터 백업...")
        self.restore_data_button = QPushButton("데이터 복원...")
        self.reset_data_button = QPushButton("데이터 초기화...")
        
        self.backup_data_button.clicked.connect(self.backup_data)
        self.restore_data_button.clicked.connect(self.restore_data)
        self.reset_data_button.clicked.connect(self.reset_data)

        data_management_layout.addWidget(self.backup_data_button)
        data_management_layout.addWidget(self.restore_data_button)
        data_management_layout.addWidget(self.reset_data_button)
        data_management_layout.addStretch()
        data_management_group.setLayout(data_management_layout)
        layout.addWidget(data_management_group)

        layout.addStretch()

    def setup_info_tab(self):
        layout = QVBoxLayout(self.info_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # 프로그램 정보 섹션
        info_group_box = QGroupBox("프로그램 정보")
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(10, 5, 10, 10)

        app_name_label = QLabel("Anti-ADHD")
        font = app_name_label.font()
        font.setPointSize(16)
        font.setBold(True)
        app_name_label.setFont(font)
        form_layout.addRow(QLabel("이름:"), app_name_label)
        form_layout.addRow(QLabel("버전:"), QLabel("1.0.1 (PyQt)")) # 버전 업데이트 예시
        form_layout.addRow(QLabel("개발자:"), QLabel("octaxii & Gemini"))
        
        github_link = QLabel("<a href=\"https://github.com/octaxii/Anti-ADHD\">GitHub 저장소</a>")
        github_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        github_link.setOpenExternalLinks(True)
        form_layout.addRow(QLabel("GitHub:"), github_link)
        info_group_box.setLayout(form_layout)
        layout.addWidget(info_group_box)

        # 라이선스 정보 섹션
        license_group_box = QGroupBox("라이선스")
        license_layout = QVBoxLayout()
        license_layout.setContentsMargins(10, 5, 10, 10)
        self.license_text_edit = QTextEdit()
        self.license_text_edit.setReadOnly(True)
        mit_license_text = """
MIT License

Copyright (c) 2024 octaxii

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        self.license_text_edit.setText(mit_license_text.strip())
        license_layout.addWidget(self.license_text_edit)
        license_group_box.setLayout(license_layout)
        layout.addWidget(license_group_box)
        layout.addStretch()

    def browse_data_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "데이터 저장 폴더 선택", self.new_data_dir)
        if directory and directory != self.current_data_dir:
            self.new_data_dir = directory
            self.data_dir_edit.setText(self.new_data_dir)
            # 경로 변경 시 즉시 알림은 여기서 하지 않고, "닫기" 누를 때 accept_settings에서 처리

    def _on_auto_save_changed(self, state):
        self.settings.setValue("general/autoSaveEnabled", self.auto_save_checkbox.isChecked())
        self.settings.sync()
        if self.main_window_ref: # MainWindow에 즉시 반영 (선택적)
            self.main_window_ref.auto_save_enabled = self.auto_save_checkbox.isChecked()

    def _on_check_updates_changed(self, state):
        self.settings.setValue("general/checkUpdatesOnStart", self.check_updates_checkbox.isChecked())
        self.settings.sync()

    def accept_settings(self):
        # 데이터 경로 변경 사항이 있다면 저장하고 알림
        if self.new_data_dir != self.current_data_dir:
            self.settings.setValue("dataDir", self.new_data_dir)
            self.current_data_dir = self.new_data_dir # 현재 대화상자 내의 current_data_dir도 업데이트
            if self.main_window_ref: # MainWindow의 data_dir은 재시작 후 반영됨을 명심
                 pass # MainWindow의 data_dir을 직접 바꾸는 것은 재시작 전에는 의미가 적을 수 있음
            QMessageBox.information(self, "설정 변경",
                                    f"데이터 저장 경로가 다음으로 설정되었습니다:\\n'{self.new_data_dir}'\\n\\n애플리케이션을 재시작해야 변경 사항이 완전히 적용됩니다.")
        
        # 체크박스 값들은 이미 stateChanged 시그널에서 즉시 저장되었음
        # self.settings.sync() # 각 시그널 핸들러에서 이미 호출됨
        self.accept() # QDialog.Accepted 상태로 다이얼로그 닫기

    def perform_update_check(self):
        QMessageBox.information(self, "업데이트 확인", "업데이트 확인 기능은 아직 구현되지 않았습니다.")

    def backup_data(self):
        # 현재 활성화된 데이터 디렉토리 사용 (MainWindow의 data_dir)
        # SettingsDialog 생성 시 current_data_dir로 전달받음
        source_dir = self.current_data_dir 
        if not os.path.isdir(source_dir):
            QMessageBox.warning(self, "백업 오류", f"데이터 디렉토리를 찾을 수 없습니다: {source_dir}")
            return

        # 백업 파일명 제안 (예: anti_adhd_backup_YYYYMMDD_HHMMSS.zip)
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        suggested_filename = f"anti_adhd_backup_{timestamp}.zip"

        file_path, _ = QFileDialog.getSaveFileName(self, "데이터 백업 파일 저장", suggested_filename, "ZIP 파일 (*.zip)")

        if not file_path:
            return # 사용자가 취소

        try:
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for foldername, subfolders, filenames in os.walk(source_dir):
                    for filename in filenames:
                        if filename.startswith("project_") and filename.endswith(".json"):
                            abs_path = os.path.join(foldername, filename)
                            # zip 파일 내에서는 source_dir 다음 경로만 유지 (상대 경로)
                            rel_path = os.path.relpath(abs_path, source_dir)
                            zf.write(abs_path, rel_path)
            QMessageBox.information(self, "백업 성공", f"데이터가 다음 파일로 성공적으로 백업되었습니다:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "백업 실패", f"데이터 백업 중 오류가 발생했습니다:\n{e}")

    def restore_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "데이터 백업 파일 선택", "", "ZIP 파일 (*.zip)")
        if not file_path:
            return

        if not zipfile.is_zipfile(file_path):
            QMessageBox.warning(self, "복원 오류", "선택한 파일이 유효한 ZIP 파일이 아닙니다.")
            return

        # 사용자에게 데이터 덮어쓰기 경고
        reply = QMessageBox.question(self, "데이터 복원 확인",
                                     f"데이터를 복원하시겠습니까?\n현재 '{self.current_data_dir}' 디렉토리의 프로젝트 파일들이 복원된 데이터로 대체됩니다. 이 작업은 되돌릴 수 없습니다.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # 복원 대상 디렉토리 (MainWindow의 data_dir 사용)
        target_dir = self.current_data_dir
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except OSError as e:
                QMessageBox.critical(self, "복원 오류", f"데이터 디렉토리 생성 실패: {target_dir}\n{e}")
                return
        
        # 기존 project_*.json 파일들을 먼저 삭제 (또는 백업)
        # 여기서는 간단하게 삭제하는 것으로 처리합니다.
        cleaned_count = 0
        for item in os.listdir(target_dir):
            if item.startswith("project_") and item.endswith(".json"):
                try:
                    os.remove(os.path.join(target_dir, item))
                    cleaned_count += 1
                except OSError as e:
                    QMessageBox.warning(self, "복원 준비 오류", f"기존 프로젝트 파일 '{item}' 삭제 실패: {e}")
                    # 실패해도 계속 진행할지, 중단할지 결정 필요. 여기서는 계속 진행.
        if cleaned_count > 0:
            print(f"{cleaned_count}개의 기존 프로젝트 파일을 삭제했습니다.")

        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                # zip 파일 내의 모든 project_*.json 파일만 압축 해제
                project_files_in_zip = [name for name in zf.namelist() if name.startswith("project_") and name.endswith(".json")]
                if not project_files_in_zip:
                    QMessageBox.warning(self, "복원 오류", "선택한 ZIP 파일에 유효한 프로젝트 데이터(project_*.json)가 없습니다.")
                    return

                zf.extractall(target_dir, members=project_files_in_zip)
            
            QMessageBox.information(self, "복원 성공", "데이터가 성공적으로 복원되었습니다. 애플리케이션 데이터를 새로고침합니다.")
            
            if self.main_window_ref and hasattr(self.main_window_ref, 'reload_data_and_ui'):
                self.main_window_ref.reload_data_and_ui()

        except zipfile.BadZipFile:
            QMessageBox.critical(self, "복원 실패", "ZIP 파일이 손상되었거나 잘못된 형식입니다.")
        except Exception as e:
            QMessageBox.critical(self, "복원 실패", f"데이터 복원 중 오류가 발생했습니다:\n{e}")

    def reset_data(self):
        reply = QMessageBox.question(self, "데이터 초기화 확인",
                                     f"정말로 모든 프로젝트 데이터를 초기화하시겠습니까?\n'{self.current_data_dir}' 디렉토리의 모든 project_*.json 파일이 삭제되며, 이 작업은 되돌릴 수 없습니다.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        target_dir = self.current_data_dir
        if not os.path.isdir(target_dir):
            QMessageBox.information(self, "데이터 초기화", "데이터 디렉토리가 이미 존재하지 않습니다. 초기화할 데이터가 없습니다.")
            # 이 경우에도 UI는 새로고침하여 빈 상태를 반영할 수 있도록 함
            if self.main_window_ref and hasattr(self.main_window_ref, 'reload_data_and_ui'):
                self.main_window_ref.reload_data_and_ui()
            return

        deleted_count = 0
        errors = []
        for item in os.listdir(target_dir):
            if item.startswith("project_") and item.endswith(".json"):
                file_path_to_delete = os.path.join(target_dir, item)
                try:
                    os.remove(file_path_to_delete)
                    deleted_count += 1
                except OSError as e:
                    errors.append(f"'{item}' 삭제 실패: {e}")
        
        if errors:
            error_message = "\n".join(errors)
            QMessageBox.warning(self, "초기화 중 오류", f"일부 프로젝트 파일 삭제 중 오류가 발생했습니다:\n{error_message}")
        else:
            QMessageBox.information(self, "데이터 초기화 성공", f"{deleted_count}개의 프로젝트 파일이 성공적으로 삭제되었습니다. 애플리케이션 데이터를 새로고침합니다.")

        if self.main_window_ref and hasattr(self.main_window_ref, 'reload_data_and_ui'):
            self.main_window_ref.reload_data_and_ui()

class QuadrantWidget(QGroupBox):
    def __init__(self, title, main_window_ref):
        super().__init__(title)
        self.main_window = main_window_ref
        self.list_widget = QListWidget()
        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(24)
        self.add_button = QPushButton("추가")

        input_layout = QHBoxLayout()
        input_layout.setSpacing(5)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 15, 10, 10)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_task)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if not (event.modifiers() & Qt.ShiftModifier): # Shift 키가 눌리지 않았을 때만
                self.add_task()
                event.accept() # 이벤트 처리됨, 기본 동작(줄바꿈) 방지
                return
        super().keyPressEvent(event) # 그 외의 경우는 기본 이벤트 처리

    def add_task(self):
        task_text = self.input_field.toPlainText().strip()
        if task_text and self.main_window.current_project_name:
            project_data = self.main_window.projects_data.get(self.main_window.current_project_name)
            if project_data:
                quadrant_index = self.main_window.quadrant_widgets.index(self)
                
                if "tasks" not in project_data:
                    project_data["tasks"] = [[], [], [], []]

                if task_text not in project_data["tasks"][quadrant_index]:
                     project_data["tasks"][quadrant_index].append(task_text)
                
                self.main_window.update_quadrant_display(self.main_window.current_project_name)
                self.input_field.clear()
                # 자동 저장 로직 적용
                if self.main_window.auto_save_enabled:
                    self.main_window.save_project_to_file(self.main_window.current_project_name)

    def clear_tasks(self):
        self.list_widget.clear()

    def load_tasks(self, tasks_list):
        self.clear_tasks()
        for task_text in tasks_list:
            item = QListWidgetItem(task_text)
            self.list_widget.addItem(item)

# --- 투명도 조절 팝업 위젯 --- #
class OpacityPopup(QWidget):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.main_window = parent_window
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(240, 240, 240, 0.95); /* 반투명 배경 */
                border: 1px solid #c0c0c0;
                border-radius: 6px;
            }
        """)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(20)
        self.slider.setMaximum(100)
        self.slider.setValue(int(self.main_window.window_opacity * 100))
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.value_label = QLabel(f"{self.slider.value()}%")
        self.value_label.setAlignment(Qt.AlignCenter)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("투명도:"))
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.value_label)
        layout.addLayout(slider_layout)
        self.setFixedSize(220, 60) # 팝업 크기 고정

    def slider_value_changed(self, value):
        self.value_label.setText(f"{value}%")
        self.main_window.set_window_opacity(value / 100.0)

    def show_at(self, pos):
        self.move(pos)
        self.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_file = "anti_adhd_settings.ini"
        self.data_dir = "anti_adhd_data"
        self.always_on_top = False
        self.window_opacity = 1.0
        self.auto_save_enabled = True # 자동 저장 기본값, load_settings에서 덮어씀

        self.init_ui()
        self.load_settings()

        self.projects_data = {}
        self.current_project_name = None
        
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir)
            except OSError as e:
                QMessageBox.critical(self, "오류", f"데이터 디렉토리 생성 실패: {self.data_dir}\\n{e}")
        
        self.load_all_projects()
        self.select_initial_project()

    def init_ui(self):
        self.setWindowTitle("Anti-ADHD (PyQt)")

        # --- 파일 메뉴 구성 --- #
        menubar = self.menuBar()
        file_menu = menubar.addMenu("파일")

        new_project_action = QAction("새 프로젝트 만들기", self)
        new_project_action.triggered.connect(self.add_new_project)
        file_menu.addAction(new_project_action)

        import_project_action = QAction("프로젝트 가져오기...", self)
        import_project_action.triggered.connect(self.import_project_file)
        file_menu.addAction(import_project_action)
        
        file_menu.addSeparator()

        save_project_action = QAction("현재 프로젝트 저장", self)
        save_project_action.setShortcut(Qt.CTRL + Qt.Key_S) # 단축키 예시
        save_project_action.triggered.connect(self.save_current_project)
        file_menu.addAction(save_project_action)

        save_project_as_action = QAction("현재 프로젝트 다른 이름으로 저장...", self)
        save_project_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_project_as_action)

        file_menu.addSeparator()

        settings_main_action = QAction("설정...", self) 
        settings_main_action.triggered.connect(self.open_settings_dialog)
        file_menu.addAction(settings_main_action)

        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # --- 툴바 구성 (기존 코드 유지) --- #
        self.toolbar = self.addToolBar("메인 툴바")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setIconSize(QSize(20, 20)) 
        
        # 사이드바 토글 액션 (기존 정의된 액션 사용, 아이콘/툴큐은 update_sidebar_toggle_icon에서 설정)
        # toggle_sidebar_icon = self.style().standardIcon(QStyle.SP_ToolBarHorizontalExtensionButton) # 이전
        # self.toggle_sidebar_action = QAction(toggle_sidebar_icon, "사이드바 토글", self) # 이전
        self.toggle_sidebar_action = QAction(self) # 아이콘 등은 아래 update_sidebar_toggle_icon()에서 설정
        self.toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        self.toolbar.addAction(self.toggle_sidebar_action)

        self.toolbar.addSeparator()

        # 항상 위에 고정 액션
        self.always_on_top_action = QAction(self)
        self.always_on_top_action.setCheckable(True)
        self.update_always_on_top_icon() # 아이콘 및 초기 상태 설정
        self.always_on_top_action.triggered.connect(self.toggle_always_on_top)
        self.toolbar.addAction(self.always_on_top_action)

        # 투명도 조절 액션 (팝업 방식)
        # 임시 아이콘 생성 (물방울 모양 - QPainter 사용)
        opacity_icon = QIcon(self.create_opacity_icon(Qt.black)) # 아이콘 색상
        self.opacity_action = QAction(opacity_icon, "투명도 조절", self)
        self.opacity_action.setToolTip("창 투명도 조절")
        self.opacity_action.triggered.connect(self.show_opacity_popup)
        self.toolbar.addAction(self.opacity_action)
        self.opacity_popup = None # 팝업 인스턴스 저장용

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # 설정 액션 아이콘 변경
        settings_toolbar_icon = self.style().standardIcon(QStyle.SP_FileDialogDetailedView) 
        self.settings_toolbar_action = QAction(settings_toolbar_icon, "설정", self)
        self.settings_toolbar_action.setToolTip("애플리케이션 설정 열기")
        self.settings_toolbar_action.triggered.connect(self.open_settings_dialog)
        self.toolbar.addAction(self.settings_toolbar_action)

        # --- 나머지 UI 구성 (사이드바, 4분면 등) --- #
        # self.sidebar = QListWidget() # 이전 QListWidget 사이드바
        # self.sidebar.setFixedWidth(220) 
        # self.sidebar.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.sidebar.customContextMenuRequested.connect(self.show_project_context_menu)
        # self.sidebar.currentItemChanged.connect(self.on_project_selection_changed)

        # 사이드바를 QFrame으로 변경하고 내부에 QListWidget(project_list) 배치
        self.sidebar = QFrame() 
        self.sidebar.setFrameShape(QFrame.StyledPanel)
        self.sidebar.setFixedWidth(200) # 폭은 200으로 유지

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.project_list_label = QLabel("프로젝트 목록:") 
        self.sidebar_layout.addWidget(self.project_list_label)

        self.project_list = QListWidget() # 실제 프로젝트 목록 위젯
        self.project_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_list.customContextMenuRequested.connect(self.show_project_context_menu)
        self.project_list.currentItemChanged.connect(self.on_project_selection_changed)
        self.sidebar_layout.addWidget(self.project_list)
        
        # 사이드바 내부 프레임 여백: (left, top, right, bottom)
        self.sidebar_layout.setContentsMargins(8, 8, 0, 8) # 우측 여백을 0으로 수정
        self.sidebar_layout.setSpacing(5) # 사이드바 내부 라벨과 리스트 간 간격

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10) # 4분면 사이의 간격
        grid_layout.setContentsMargins(0,0,0,0) # 4분면 그룹 전체의 여백을 0으로 설정
        categories = [
            "긴급하고 중요한 일", "긴급하지 않지만 중요한 일",
            "긴급하지만 중요하지 않은 일", "긴급하지도 중요하지도 않은 일"
        ]
        self.quadrant_widgets = []
        for i, cat_name in enumerate(categories):
            quad_widget = QuadrantWidget(cat_name, self)
            grid_layout.addWidget(quad_widget, i // 2, i % 2)
            self.quadrant_widgets.append(quad_widget)

        main_content_widget = QWidget()
        main_content_widget.setLayout(grid_layout)

        # --- QSplitter ---
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.sidebar) # QFrame인 sidebar를 splitter에 추가
        self.splitter.addWidget(main_content_widget)
        self.splitter.setStretchFactor(1, 1) 
        self.splitter.setHandleWidth(0) # 스플리터 핸들 너비 조정 (기본값보다 작게)
        self.setCentralWidget(self.splitter)

        self.update_sidebar_toggle_icon() # init_ui 마지막에 호출하여 초기 아이콘 설정

    def create_opacity_icon(self, color):
        icon_size = self.toolbar.iconSize() # 툴바 아이콘 크기 참조
        pixmap = QPixmap(icon_size) # 참조한 크기로 QPixmap 생성
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        # 아이콘 내부 여백을 고려하여 그림 크기 조정 (예: 전체 크기의 70-80%)
        padding = int(icon_size.width() * 0.15)
        draw_rect = pixmap.rect().adjusted(padding, padding, -padding, -padding)
        painter.setPen(QPen(color, 1.5 if icon_size.width() > 16 else 1)) # 선 두께도 크기에 따라 조정
        painter.drawEllipse(draw_rect) 
        painter.end()
        return QIcon(pixmap)

    def show_opacity_popup(self):
        # 이전 팝업이 있다면 닫아서 WA_DeleteOnClose에 의해 삭제되도록 함
        if self.opacity_popup is not None:
            try:
                # self.opacity_popup이 이미 C++ 레벨에서 삭제되었지만
                # Python 참조가 남아있는 경우를 대비하여 try-except 사용
                if self.opacity_popup.isVisible():
                    self.opacity_popup.close()
            except RuntimeError: # 이미 삭제된 객체에 접근하려 할 때
                pass # 특별히 할 작업 없음
            self.opacity_popup = None # 이전 참조 정리

        # 팝업을 새로 생성하고 표시
        button = self.toolbar.widgetForAction(self.opacity_action)
        if button:
            point = button.mapToGlobal(QPoint(0, button.height()))
            self.opacity_popup = OpacityPopup(self)
            self.opacity_popup.show_at(point)
        else: 
            cursor_pos = QCursor.pos() # QCursor를 사용하려면 QtGui에서 import 필요
            self.opacity_popup = OpacityPopup(self)
            self.opacity_popup.show_at(cursor_pos)

    def show_project_context_menu(self, position):
        menu = QMenu()
        add_action = menu.addAction("새 프로젝트 추가")
        rename_action = menu.addAction("이름 변경")
        delete_action = menu.addAction("프로젝트 삭제")
        # delete_file_action = menu.addAction("프로젝트 파일 삭제") # 추후 추가

        action = menu.exec_(self.sidebar.mapToGlobal(position))

        if action == add_action:
            self.add_new_project()
        elif action == rename_action:
            self.rename_selected_project()
        elif action == delete_action:
            self.delete_selected_project()

    def add_new_project(self):
        text, ok = QInputDialog.getText(self, "새 프로젝트", "프로젝트 이름:")
        if ok and text.strip():
            project_name = text.strip()
            if project_name not in self.projects_data:
                self.projects_data[project_name] = {"tasks": [[], [], [], []]} 
                self.project_list.addItem(project_name)
                self.project_list.setCurrentRow(self.project_list.count() - 1) 
                # 새 프로젝트는 자동 저장 여부와 관계없이 기본 파일 생성 (중요)
                self.save_project_to_file(project_name) 
            else:
                QMessageBox.warning(self, "중복 오류", "이미 존재하는 프로젝트 이름입니다.")
        # self.update_quadrant_display(self.current_project_name) # setCurrentRow에서 on_project_selection_changed 호출로 처리

    def rename_selected_project(self):
        current_item = self.project_list.currentItem()
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
            # self.current_project_name = new_name_stripped # on_project_selection_changed가 처리
            
            old_file_path = os.path.join(self.data_dir, f"project_{old_name}.json")
            new_file_path = os.path.join(self.data_dir, f"project_{new_name_stripped}.json")
            if os.path.exists(old_file_path):
                try:
                    os.rename(old_file_path, new_file_path)
                except OSError as e:
                     QMessageBox.critical(self, "파일 오류", f"프로젝트 파일 이름 변경 실패: {e}")
            
            # 자동 저장 로직 적용 (내용 변경은 없지만, 파일 이름 변경 후 일관성을 위해 저장)
            if self.auto_save_enabled:
                self.save_project_to_file(new_name_stripped) 
            # 현재 선택된 프로젝트 이름은 on_project_selection_changed에 의해 업데이트되므로,
            # 해당 콜백 내에서 update_quadrant_display가 호출됨.

    def delete_selected_project(self):
        current_item = self.project_list.currentItem()
        if not current_item:
            return

        project_name = current_item.text()
        reply = QMessageBox.question(self, "프로젝트 삭제", 
                                     f"'{project_name}' 프로젝트를 삭제하시겠습니까?\n(데이터와 해당 프로젝트 파일 모두 삭제됩니다!)",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            row = self.project_list.row(current_item)
            self.project_list.takeItem(row) 
            if project_name in self.projects_data:
                del self.projects_data[project_name] 
            
            file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    QMessageBox.critical(self, "파일 오류", f"프로젝트 파일 삭제 실패: {e}")

            if self.project_list.count() > 0:
                 new_row = max(0, row -1)
                 if new_row < self.project_list.count(): # Ensure new_row is a valid index
                    self.project_list.setCurrentRow(new_row)
                 else: #Fallback if new_row is out of bounds (e.g. last item deleted)
                    self.project_list.setCurrentRow(self.project_list.count() -1 if self.project_list.count() > 0 else -1)
            else:
                 self.current_project_name = None 
                 self.clear_all_quadrants()
            # 삭제 작업은 자동 저장과 직접적 연관은 적음. on_project_selection_changed가 후속 처리.

    def on_project_selection_changed(self, current_item, previous_item):
        # 이전 프로젝트 저장 (자동 저장 옵션에 따라)
        if previous_item and previous_item.text() in self.projects_data:
            if self.auto_save_enabled:
                self.save_project_to_file(previous_item.text())

        if current_item:
            self.current_project_name = current_item.text()
            self.update_quadrant_display(self.current_project_name)
        else:
            self.current_project_name = None
            self.clear_all_quadrants()

    def save_project_to_file(self, project_name):
        if project_name and project_name in self.projects_data:
            file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.projects_data[project_name], f, ensure_ascii=False, indent=4)
            except IOError as e:
                QMessageBox.critical(self, "저장 오류", f"프로젝트 '{project_name}' 저장 실패: {e}")

    def load_project_from_file(self, project_name):
        file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                QMessageBox.critical(self, "로드 오류", f"프로젝트 '{project_name}' 로드 실패: {e}")
        return {"tasks": [[], [], [], []]} # 파일 없거나 오류 시 기본값

    def load_all_projects(self):
        self.project_list.clear()
        self.projects_data.clear()
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        for filename in os.listdir(self.data_dir):
            if filename.startswith("project_") and filename.endswith(".json"):
                project_name = filename[8:-5] # "project_" 와 ".json" 제거
                self.projects_data[project_name] = self.load_project_from_file(project_name)
                self.project_list.addItem(project_name)
    
    def select_initial_project(self):
        if self.project_list.count() > 0:
            self.project_list.setCurrentRow(0)
        else:
            # 기본 프로젝트가 없으면 하나 생성
            default_project_name = "기본 프로젝트"
            self.projects_data[default_project_name] = {"tasks": [[], [], [], []]}
            self.project_list.addItem(default_project_name)
            self.project_list.setCurrentRow(0)
            self.save_project_to_file(default_project_name)


    def update_quadrant_display(self, project_name):
        if project_name and project_name in self.projects_data:
            project_content = self.projects_data[project_name]
            tasks_by_quadrant = project_content.get("tasks", [[], [], [], []])
            for i, quad_widget in enumerate(self.quadrant_widgets):
                if i < len(tasks_by_quadrant):
                    quad_widget.load_tasks(tasks_by_quadrant[i])
                else:
                    quad_widget.clear_tasks() # 데이터가 부족할 경우 대비
        else:
            self.clear_all_quadrants()

    def clear_all_quadrants(self):
        for quad_widget in self.quadrant_widgets:
            quad_widget.clear_tasks()
            
    def toggle_sidebar(self):
        if hasattr(self, 'sidebar'):
            self.sidebar.setVisible(not self.sidebar.isVisible())
            self.update_sidebar_toggle_icon()

    def set_always_on_top(self, enabled):
        self.always_on_top = enabled
        if enabled:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.update_always_on_top_icon() # 아이콘 및 툴큐 업데이트
        self.show() # 플래그 변경 후 show() 호출 필수

    def toggle_always_on_top(self):
        # QAction의 checked 상태가 이미 변경된 후 호출됨
        self.set_always_on_top(self.always_on_top_action.isChecked())

    def update_always_on_top_icon(self):
        if not hasattr(self, 'always_on_top_action'): # 초기화 중 오류 방지
            return
        if self.always_on_top_action.isChecked(): 
            # "고정됨" 상태 아이콘: SP_DialogYesButton 또는 핀 모양 아이콘
            icon = self.style().standardIcon(QStyle.SP_DialogYesButton) 
            self.always_on_top_action.setIcon(icon)
            self.always_on_top_action.setToolTip("창 고정 해제 (Always on Top 비활성화)")
        else:
            # "고정 안됨" 상태 아이콘: SP_DialogNoButton 또는 빈 핀 모양 아이콘
            icon = self.style().standardIcon(QStyle.SP_DialogNoButton) 
            self.always_on_top_action.setIcon(icon)
            self.always_on_top_action.setToolTip("창 항상 위에 고정 (Always on Top 활성화)")

    def set_window_opacity(self, opacity):
        self.window_opacity = opacity 
        super().setWindowOpacity(opacity)
        # OpacityPopup이 열려있다면 슬라이더 값도 동기화 (선택적, 이미 popup 내부에서 처리 중)
        # if self.opacity_popup and self.opacity_popup.isVisible():
        #    self.opacity_popup.slider.setValue(int(opacity * 100))

    def load_settings(self):
        settings = QSettings(self.settings_file, QSettings.IniFormat)
        self.restoreGeometry(settings.value("geometry", self.saveGeometry()))
        sidebar_visible = settings.value("sidebarVisible", True, type=bool)
        if hasattr(self, 'sidebar'): 
            self.sidebar.setVisible(sidebar_visible)
            self.update_sidebar_toggle_icon() # settings 로드 후 아이콘 상태 업데이트
        
        self.data_dir = settings.value("dataDir", self.data_dir)
        
        self.always_on_top = settings.value("alwaysOnTop", False, type=bool)
        if hasattr(self, 'always_on_top_action'): 
            self.always_on_top_action.setChecked(self.always_on_top) 
        self.update_always_on_top_icon() # 아이콘 업데이트
        if self.always_on_top_action.isChecked(): # 실제 창 상태도 반영
             self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
             self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        # self.show() # init_ui 마지막이나 MainWindow.show() 에서 한 번에 처리
        
        self.window_opacity = settings.value("windowOpacity", 1.0, type=float)
        self.set_window_opacity(self.window_opacity) # 창 투명도 설정
        # 툴바 슬라이더가 없어졌으므로 관련 코드 제거

        self.auto_save_enabled = settings.value("general/autoSaveEnabled", True, type=bool)
    
    def save_settings(self):
        settings = QSettings(self.settings_file, QSettings.IniFormat)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("sidebarVisible", self.sidebar.isVisible())
        settings.setValue("dataDir", self.data_dir) # 현재 사용 중인 data_dir을 저장
        settings.setValue("alwaysOnTop", self.always_on_top)
        settings.setValue("windowOpacity", self.window_opacity)
        # 자동 저장 설정은 SettingsDialog에서 직접 QSettings에 저장함
        # settings.setValue("general/autoSaveEnabled", self.auto_save_enabled) # MainWindow에서 관리 시 필요

    def open_settings_dialog(self):
        dialog = SettingsDialog(current_data_dir=self.data_dir, 
                                settings_file_path=self.settings_file,
                                parent=self)
        if dialog.exec_() == QDialog.Accepted:
            # 설정 대화상자에서 "확인"(실제로는 "닫기" 후 accept())을 누르면 
            # SettingsDialog 내부의 accept_settings 메서드에서 QSettings에 필요한 값들이 저장됩니다.
            # (예: 데이터 디렉토리 변경, 자동 저장 활성화 여부 등)
            # MainWindow의 always_on_top이나 window_opacity 값은 SettingsDialog에서 직접 제어하지 않으므로,
            # 여기서 dialog 객체로부터 해당 값을 읽어올 필요가 없습니다.
            # 이 값들은 MainWindow의 툴바 액션과 save_settings/load_settings를 통해 관리됩니다.
            
            # 아래 두 줄이 AttributeError의 원인이므로 삭제합니다.
            # self.always_on_top = dialog.always_on_top_checkbox.isChecked()
            # self.window_opacity = dialog.opacity_slider.value() / 100.0
            
            # SettingsDialog에서 auto_save_enabled가 변경되었다면, MainWindow의 상태도 업데이트될 수 있도록
            # SettingsDialog의 _on_auto_save_changed에서 self.main_window_ref.auto_save_enabled를 업데이트합니다.
            # 여기서는 추가 작업이 필요 없습니다.
            pass

    # --- 신규 파일 작업 메서드 --- #
    def import_project_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "프로젝트 파일 가져오기", "", "JSON 파일 (*.json);;모든 파일 (*)", options=options)
        
        if not file_path:
            return # 사용자가 취소

        try:
            # 1. 파일 내용 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # 기본 JSON 구조 검증 및 보정
            if not isinstance(imported_data, dict):
                QMessageBox.warning(self, "가져오기 오류", "선택한 파일의 최상위 데이터가 딕셔너리 형식이 아닙니다.")
                return
            
            tasks_data = imported_data.get("tasks")
            if not isinstance(tasks_data, list) or len(tasks_data) != 4:
                # tasks가 없거나, 리스트가 아니거나, 4개의 quadrant 구조가 아니면 기본 구조라도 만들어줌
                # 사용자의 데이터를 최대한 보존하되, 앱 구조에 맞게끔 최소한으로 조정
                corrected_tasks = [[], [], [], []]
                if isinstance(tasks_data, list): # 일부 데이터가 리스트 형태로 있다면 최대한 활용
                    for i in range(min(len(tasks_data), 4)):
                        if isinstance(tasks_data[i], list):
                            corrected_tasks[i] = tasks_data[i]
                imported_data["tasks"] = corrected_tasks
                # 필요하다면 사용자에게 구조가 수정되었음을 알릴 수 있음

        except json.JSONDecodeError:
            QMessageBox.warning(self, "가져오기 오류", "선택한 파일이 유효한 JSON 형식이 아닙니다.")
            return
        except Exception as e:
            QMessageBox.critical(self, "가져오기 오류", f"파일을 읽는 중 오류가 발생했습니다: {e}")
            return

        # 2. 가져올 프로젝트 이름 결정
        original_filename = os.path.basename(file_path)
        potential_project_name = ""
        if original_filename.startswith("project_") and original_filename.endswith(".json"):
            potential_project_name = original_filename[8:-5]
        else:
            potential_project_name, _ = os.path.splitext(original_filename)

        new_project_name = potential_project_name.strip()
        if not new_project_name: # 이름이 비었으면 기본 이름 사용
            new_project_name = "가져온_프로젝트"

        # 중복 이름 처리
        name_suffix = 1
        final_project_name = new_project_name
        while final_project_name in self.projects_data:
            final_project_name = f"{new_project_name}_{name_suffix}"
            name_suffix += 1
        
        text, ok = QInputDialog.getText(self, "프로젝트 이름 확인", "가져올 프로젝트의 이름을 입력하세요:", text=final_project_name)
        if ok and text.strip():
            final_project_name = text.strip()
            if final_project_name in self.projects_data:
                QMessageBox.warning(self, "이름 중복", f"프로젝트 이름 '{final_project_name}'은(는) 이미 존재합니다. 가져오기를 취소합니다.")
                return
        elif not ok: 
            return
        
        new_project_file_path = os.path.join(self.data_dir, f"project_{final_project_name}.json")
        try:
            with open(new_project_file_path, 'w', encoding='utf-8') as f:
                json.dump(imported_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "가져오기 오류", f"가져온 프로젝트를 저장하는 중 오류가 발생했습니다: {e}")
            return

        self.projects_data[final_project_name] = imported_data
        self.project_list.addItem(final_project_name)

        items = self.project_list.findItems(final_project_name, Qt.MatchExactly)
        if items:
            self.project_list.setCurrentItem(items[0]) 
        
        QMessageBox.information(self, "가져오기 성공", f"프로젝트 '{final_project_name}'(으)로 성공적으로 가져왔습니다.")

    def save_current_project(self):
        if self.current_project_name:
            self.save_project_to_file(self.current_project_name)
            # 사용자에게 저장되었음을 알리는 피드백 (선택적)
            # self.statusBar().showMessage(f"'{self.current_project_name}' 저장됨", 2000)
        else:
            QMessageBox.information(self, "알림", "저장할 프로젝트가 선택되지 않았습니다.")

    def save_project_as(self):
        if not self.current_project_name:
            QMessageBox.information(self, "알림", "'다른 이름으로 저장'할 프로젝트가 선택되지 않았습니다.")
            return

        current_project_data = self.projects_data.get(self.current_project_name)
        if not current_project_data:
            QMessageBox.warning(self, "오류", f"현재 프로젝트 '{self.current_project_name}'의 데이터를 찾을 수 없습니다.")
            return

        # 새 프로젝트 이름 제안 시 현재 이름 기반 (예: "현재프로젝트명_복사본")
        suggested_new_name = f"{self.current_project_name}_복사본"
        
        options = QFileDialog.Options()
        # 파일 다이얼로그에서 실제 파일 저장은 하지 않고, 이름과 경로만 얻음
        # 실제 저장은 save_project_to_file 내부에서 일어남
        new_file_path, _ = QFileDialog.getSaveFileName(self, 
                                                       "프로젝트 다른 이름으로 저장", 
                                                       os.path.join(self.data_dir, f"project_{suggested_new_name}.json"), 
                                                       "JSON 파일 (*.json)", 
                                                       options=options)
        if not new_file_path:
            return # 사용자가 취소

        # 파일 경로에서 새 프로젝트 이름 추출 (project_ 접두사와 .json 확장자 고려)
        new_project_filename = os.path.basename(new_file_path)
        if new_project_filename.startswith("project_") and new_project_filename.endswith(".json"):
            new_project_name = new_project_filename[8:-5]
        else:
            # 기본 이름 지정 방식이 아니면, 사용자에게 경고하거나 다른 방식의 이름 추출 필요
            # 여기서는 단순하게 파일명(확장자제거)을 프로젝트 이름으로 사용 시도
            new_project_name, _ = os.path.splitext(new_project_filename)
            # 추가적인 이름 정제 로직이 필요할 수 있음 (예: 공백, 특수문자 처리)
            if not new_project_name.strip():
                QMessageBox.warning(self, "오류", "올바른 새 프로젝트 이름을 파일명에서 추출할 수 없습니다.")
                return
        
        new_project_name = new_project_name.strip()

        if new_project_name == self.current_project_name or new_project_name in self.projects_data:
            QMessageBox.warning(self, "중복 오류", f"프로젝트 이름 '{new_project_name}'은(는) 이미 존재합니다. 다른 이름을 사용해주세요.")
            return

        # 데이터 복사 및 새 이름으로 저장
        self.projects_data[new_project_name] = json.loads(json.dumps(current_project_data)) # 깊은 복사
        self.save_project_to_file(new_project_name) # 새 이름으로 파일 저장

        # 사이드바 업데이트 및 새 프로젝트 선택
        self.project_list.addItem(new_project_name)
        # QListWidget에서 텍스트로 아이템 찾기 (더 견고한 방법은 QListWidgetItem을 직접 관리하는 것)
        items = self.project_list.findItems(new_project_name, Qt.MatchExactly)
        if items:
            self.project_list.setCurrentItem(items[0])
        # self.current_project_name은 on_project_selection_changed에 의해 업데이트됨
        QMessageBox.information(self, "성공", f"프로젝트가 '{new_project_name}'(으)로 저장되었습니다.")

    def reload_data_and_ui(self):
        """
        데이터 디렉토리 변경(복원, 초기화 등) 후 프로젝트 데이터와 UI를 새로고침합니다.
        """
        # 1. 현재 로드된 프로젝트 데이터 및 사이드바 초기화
        self.projects_data.clear()
        self.project_list.clear()
        self.current_project_name = None # 현재 선택된 프로젝트 없음으로 설정
        self.clear_all_quadrants() # 4분면 클리어

        # 2. 데이터 디렉토리에서 모든 프로젝트 다시 로드
        # 데이터 디렉토리가 존재하지 않을 경우를 대비 (예: 초기화 직후)
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir)
            except OSError as e:
                QMessageBox.critical(self, "오류", f"데이터 디렉토리 생성 실패: {self.data_dir}\\n{e}")
                return # 디렉토리 생성 실패 시 더 이상 진행 불가

        self.load_all_projects() # 사이드바도 채워짐

        # 3. 초기 프로젝트 선택 또는 기본 프로젝트 생성 (기존 로직 활용)
        self.select_initial_project()
        
        # select_initial_project 내에서 current_project_name 설정 및 update_quadrant_display 호출됨
        # 만약 select_initial_project 후에도 current_project_name이 None이면 (예: 프로젝트가 전혀 없는 초기 상태)
        # clear_all_quadrants는 이미 위에서 호출되었으므로 추가 작업 불필요.

    def closeEvent(self, event):
        # 애플리케이션 종료 시 현재 프로젝트는 자동 저장 여부와 관계없이 항상 저장
        if self.current_project_name and self.current_project_name in self.projects_data:
            self.save_project_to_file(self.current_project_name)
        self.save_settings() 
        super().closeEvent(event)

    def update_sidebar_toggle_icon(self): # 아이콘 및 툴큐 업데이트
        if hasattr(self, 'sidebar') and hasattr(self, 'toggle_sidebar_action'):
            if self.sidebar.isVisible():
                self.toggle_sidebar_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
                self.toggle_sidebar_action.setToolTip("사이드바 숨기기")
            else:
                self.toggle_sidebar_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
                self.toggle_sidebar_action.setToolTip("사이드바 보이기")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 조너선 아이브 스타일 가미된 스타일시트 적용
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0; /* 밝은 회색 배경 */
        }
        QWidget {
            font-family: "SF Pro Display", "Helvetica Neue", "Arial", sans-serif; /* macOS 스타일 폰트 우선, 없으면 기본 산세리프 */
            color: #333; /* 기본 텍스트 색상 */
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            margin-top: 6px;
            background-color: #f9f9f9;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left; /* 제목 위치 */
            padding: 0 5px 0 5px;
            color: #555;
        }
        QListWidget {
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            background-color: #ffffff;
        }
        QListWidget::item {
            padding: 5px;
        }
        QListWidget::item:selected {
            background-color: #007aff; /* Apple Blue 강조색 */
            color: white;
        }
        QTextEdit, QLineEdit {
            border: 1px solid #c0c0c0;
            border-radius: 4px;
            padding: 5px;
            background-color: #ffffff;
            selection-background-color: #007aff;
            selection-color: white;
        }
        QTextEdit:focus, QLineEdit:focus {
            border: 1px solid #007aff; /* 포커스 시 강조 */
        }
        QPushButton {
            background-color: #fdfdfd;
            border: 1px solid #c0c0c0;
            border-radius: 4px;
            padding: 5px 10px;
            min-height: 20px; /* 버튼 최소 높이 */
        }
        QPushButton:hover {
            background-color: #e8e8e8;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        QPushButton:disabled {
            background-color: #f5f5f5;
            color: #a0a0a0;
        }
        QToolBar {
            background-color: #e8e8e8; /* 툴바 배경 */
            border: none;
            padding: 2px;
        }
        QToolButton { /* 툴바 안의 버튼 스타일링 */
            padding: 3px;
            margin: 2px;
            border-radius: 3px;
        }
        QToolButton:hover {
            background-color: #d8d8d8;
        }
        QToolButton:pressed {
            background-color: #c8c8c8;
        }
        QSplitter::handle {
            background-color: #d0d0d0;
            width: 1px; /* 핸들 두께 줄임 */
        }
        QSplitter::handle:horizontal {
            height: 1px;
        }
        QMenu {
            background-color: #ffffff;
            border: 1px solid #c0c0c0;
        }
        QMenu::item {
            padding: 5px 20px;
        }
        QMenu::item:selected {
            background-color: #007aff;
            color: white;
        }
        QDialog {
            background-color: #f0f0f0;
        }
        QLabel {
             background-color: transparent; /* 그룹박스 배경색 상속 안받도록 */
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        QCheckBox::indicator:unchecked {
            image: url(icon_checkbox_unchecked.png); /* 비선택 시 아이콘 (경로 설정 필요) */
        }
        QCheckBox::indicator:checked {
            image: url(icon_checkbox_checked.png); /* 선택 시 아이콘 (경로 설정 필요) */
        }
        QSlider::groove:horizontal {
            border: 1px solid #bbb;
            background: white;
            height: 8px;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #007aff;
            border: 1px solid #007aff;
            width: 16px;
            margin: -4px 0; /* 핸들이 그루브 중앙에 오도록 */
            border-radius: 8px;
        }
    """)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_()) 