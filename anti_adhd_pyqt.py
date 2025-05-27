from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter, QListWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLineEdit, QPushButton, QAction, QMenu, QGridLayout, QTextEdit, QInputDialog,
    QMessageBox, QFileDialog, QListWidgetItem, QDialog, QLabel, QCheckBox, QSlider, QStyle, QSizePolicy,
    QTabWidget, QFormLayout, QToolButton, QFrame, QStatusBar, QShortcut, QDateTimeEdit, QAbstractItemView
)
from PyQt5.QtCore import Qt, QSettings, QUrl, QPoint, QSize, QTimer, QDateTime, QCoreApplication
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QIcon, QDesktopServices, QPainter, QPen, QColor, QPixmap, QCursor, QFont
import sys
import os
import json
import zipfile
import shutil
import time
from datetime import datetime, timedelta
from typing import Optional

# --- Qt 및 PyQt5 상수 대체값 정의 (파일 상단에 추가) ---
QT_CONST = {
    'AlignRight': 0x0002,
    'AlignLeft': 0x0001,
    'AlignTop': 0x0004,
    'AlignCenter': 0x0084,
    'TextBrowserInteraction': 0x0001,
    'ScrollBarAlwaysOff': 1,
    'ScrollBarAsNeeded': 1,
    'PointingHandCursor': 13,
    'CustomContextMenu': 2,
    'UserRole': 32,
    'ItemIsUserCheckable': 0x0100,
    'Checked': 2,
    'Unchecked': 0,
    'CTRL': 0x04000000,
    'SHIFT': 0x02000000,
    'Key_N': 0x4e,
    'Key_S': 0x53,
    'Key_R': 0x52,
    'Key_Delete': 0x01000007,
    'Key_B': 0x42,
    'Key_Return': 0x01000004,
    'Key_Up': 0x01000013,
    'Key_Down': 0x01000015,
    'Key_Comma': 0x2c,
    'Key_Z': 0x5a,
    'Key_F': 0x46,
    'Key_Escape': 0x01000000,
    'ControlModifier': 0x04000000,
    'NoToolBarArea': 0,
    'PreventContextMenu': 4,
    'Horizontal': 1,
    'WindowStaysOnTopHint': 0x00040000,
    'Popup': 0x80000000,
    'FramelessWindowHint': 0x00000800,
    'NoDropShadowWindowHint': 0x40000000,
    'WA_TranslucentBackground': 120,
    'WA_DeleteOnClose': 55,
    'transparent': 0,
    'MatchExactly': 0,
}
QSETTINGS_INIFMT = 1
QFORMLAYOUT_WRAPALLROWS = 2

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
        self.settings = QSettings(self.settings_file_path, QSETTINGS_INIFMT)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabBar::tab { min-width: 80px; min-height: 24px; font-size: 10.5pt; padding: 4px 10px; } QTabBar::tab:selected { font-weight: bold; color: #1565c0; }")
        main_layout.addWidget(self.tab_widget)

        # "일반" 탭 생성 및 UI 구성
        self.general_tab = QWidget()
        self.tab_widget.addTab(self.general_tab, "일반")
        self.setup_general_tab()

        # "정보" 탭 생성 및 UI 구성
        self.info_tab = QWidget()
        self.tab_widget.addTab(self.info_tab, "정보")
        self.setup_info_tab()

        # 하단 버튼 레이아웃 (닫기 버튼)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.close_button = QPushButton("닫기")
        self.close_button.setMinimumWidth(80)
        self.close_button.setMaximumWidth(140)
        self.close_button.setStyleSheet("QPushButton { font-size: 10pt; padding: 6px 0; border-radius: 6px; background: #1565c0; color: white; font-weight: bold; } QPushButton:hover { background: #1976d2; }")
        self.close_button.clicked.connect(self.accept_settings)
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)
        button_layout.setContentsMargins(0, 12, 0, 0)

        self.setLayout(main_layout)
        self.setMinimumWidth(420)
        self.setMinimumHeight(340)
        self.setMaximumWidth(700)

    def setup_general_tab(self):
        layout = QVBoxLayout(self.general_tab)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        # 데이터 경로 설정 그룹
        data_dir_group = QGroupBox("데이터 저장 경로")
        data_dir_group.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 8px; background: #fafbfc; }")
        data_dir_group_layout = QVBoxLayout()
        data_dir_group_layout.setSpacing(6)
        data_dir_group_layout.setContentsMargins(10, 6, 10, 10)

        path_input_layout = QHBoxLayout()
        self.data_dir_label = QLabel("현재 경로:")
        self.data_dir_label.setStyleSheet("font-size: 9.5pt; color: #666;")
        self.data_dir_edit = QLineEdit(self.current_data_dir)
        self.data_dir_edit.setReadOnly(True)
        self.browse_button = QPushButton("폴더 변경…")
        self.browse_button.setMinimumWidth(80)
        self.browse_button.setMaximumWidth(140)
        self.browse_button.setStyleSheet("QPushButton { font-size: 9.5pt; padding: 3px 0; border-radius: 5px; background: #e3f2fd; color: #1565c0; } QPushButton:hover { background: #bbdefb; }")
        self.browse_button.clicked.connect(self.browse_data_directory)
        path_input_layout.addWidget(self.data_dir_label)
        path_input_layout.addWidget(self.data_dir_edit, 1)
        path_input_layout.addWidget(self.browse_button)
        data_dir_group_layout.addLayout(path_input_layout)
        path_notice_label = QLabel("경로 변경 후 프로그램을 재시작해야 적용됩니다.")
        path_notice_label.setStyleSheet("font-size: 8.5pt; color: #aaa;")
        data_dir_group_layout.addWidget(path_notice_label, 0x0004)
        data_dir_group.setLayout(data_dir_group_layout)
        layout.addWidget(data_dir_group)

        # 자동 저장 그룹
        auto_save_group = QGroupBox("자동 저장")
        auto_save_group.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 8px; background: #fafbfc; }")
        auto_save_layout = QVBoxLayout()
        auto_save_layout.setContentsMargins(10, 6, 10, 10)
        self.auto_save_checkbox = QCheckBox("애플리케이션 상태 자동 저장")
        self.auto_save_checkbox.setChecked(self.settings.value("general/autoSaveEnabled", True, type=bool))
        self.auto_save_checkbox.setStyleSheet("font-size: 9.5pt;")
        self.auto_save_checkbox.stateChanged.connect(self._on_auto_save_changed)
        auto_save_layout.addWidget(self.auto_save_checkbox)
        auto_save_group.setLayout(auto_save_layout)
        layout.addWidget(auto_save_group)

        # 업데이트 그룹
        update_group = QGroupBox("업데이트")
        update_group.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 8px; background: #fafbfc; }")
        update_layout = QVBoxLayout()
        update_layout.setContentsMargins(10, 6, 10, 10)
        self.check_updates_checkbox = QCheckBox("시작 시 업데이트 자동 확인")
        self.check_updates_checkbox.setChecked(self.settings.value("general/checkUpdatesOnStart", True, type=bool))
        self.check_updates_checkbox.setStyleSheet("font-size: 9.5pt;")
        self.check_updates_checkbox.stateChanged.connect(self._on_check_updates_changed)
        self.check_now_button = QPushButton("지금 업데이트 확인")
        self.check_now_button.setMinimumWidth(80)
        self.check_now_button.setMaximumWidth(140)
        self.check_now_button.setStyleSheet("QPushButton { font-size: 9.5pt; padding: 3px 0; border-radius: 5px; background: #e3f2fd; color: #1565c0; } QPushButton:hover { background: #bbdefb; }")
        self.check_now_button.clicked.connect(self.perform_update_check)
        update_layout.addWidget(self.check_updates_checkbox)
        update_layout.addWidget(self.check_now_button, 0x0001)
        update_group.setLayout(update_layout)
        layout.addWidget(update_group)

        # 데이터 관리 그룹
        data_management_group = QGroupBox("데이터 관리")
        data_management_group.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 8px; background: #fafbfc; }")
        data_management_layout = QHBoxLayout()
        data_management_layout.setSpacing(8)
        data_management_layout.setContentsMargins(10, 8, 10, 10)
        self.backup_data_button = QPushButton("데이터 백업…")
        self.restore_data_button = QPushButton("데이터 복원…")
        self.reset_data_button = QPushButton("데이터 초기화…")
        for btn in [self.backup_data_button, self.restore_data_button, self.reset_data_button]:
            btn.setMinimumWidth(80)
            btn.setMaximumWidth(140)
            btn.setStyleSheet("QPushButton { font-size: 9.5pt; padding: 5px 0; border-radius: 6px; background: #fff3e0; color: #e65100; font-weight: bold; } QPushButton:hover { background: #ffe0b2; }")
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
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        # 프로그램 정보 섹션
        info_group_box = QGroupBox("프로그램 정보")
        info_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 8px; background: #fafbfc; }")
        form_layout = QFormLayout()
        # form_layout.setLabelAlignment(0x0002)  # Qt.AlignRight (Enum 오류 방지)
        # form_layout.setRowWrapPolicy(2)  # QFormLayout.WrapAllRows (Enum 오류 방지)
        form_layout.setSpacing(8)
        form_layout.setContentsMargins(10, 6, 10, 10)
        app_name_label = QLabel("Anti-ADHD")
        font = app_name_label.font()
        font.setPointSize(13)
        font.setBold(True)
        app_name_label.setFont(font)
        app_name_label.setStyleSheet("color: #1565c0;")
        form_layout.addRow(QLabel("이름:"), app_name_label)
        form_layout.addRow(QLabel("버전:"), QLabel("1.0.1"))
        form_layout.addRow(QLabel("개발자:"), QLabel("octaxii"))
        github_link = QLabel("<a href=\"https://github.com/octaxii/Anti-ADHD\">GitHub 저장소</a>")
        # github_link.setTextInteractionFlags(0x0001)  # Qt.TextBrowserInteraction (Enum 오류 방지)
        github_link.setOpenExternalLinks(True)
        form_layout.addRow(QLabel("GitHub:"), github_link)
        info_group_box.setLayout(form_layout)
        layout.addWidget(info_group_box)
        # 라이선스 정보 섹션
        license_group_box = QGroupBox("라이선스")
        license_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 8px; background: #fafbfc; }")
        license_layout = QVBoxLayout()
        license_layout.setContentsMargins(10, 6, 10, 10)
        self.license_text_edit = QTextEdit()
        self.license_text_edit.setReadOnly(True)
        self.license_text_edit.setStyleSheet("font-size: 8.5pt; background: #f8f9fa; color: #333; border-radius: 6px; padding: 6px;")
        mit_license_text = """
MIT License

Copyright (c) 2024 octaxii

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
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

class ProjectListWidget(QListWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self.main_window.adjust_sidebar_width)

class EisenhowerQuadrantWidget(QFrame):
    def __init__(self, color, keyword, description, icon=None, main_window_ref=None):
        super().__init__()
        self.main_window = main_window_ref
        self.color = color
        self.keyword = keyword
        self.description = description
        self.icon = icon
        self.setObjectName("eisenhowerQuadrant")
        
        # 캐시 초기화
        self._due_date_cache = {}
        self._item_cache = {}
        self._last_update = 0
        self._update_interval = 1000  # 1초마다 업데이트
        
        # 색상 계산 (한 번만)
        from PyQt5.QtGui import QColor
        base = QColor(color)
        light = base.lighter(170).name()
        dark = base.darker(130).name()
        border = base.darker(120).name()
        
        # 위젯 생성
        self._init_widgets()
        self._setup_styles(color, light, dark, border)
        self._setup_layout()
        self._connect_signals()
        
        # 초기화
        self.notified_set = set()
        self.items = []
        
        # 애니메이션 설정
        self._setup_animations()
        
    def _init_widgets(self):
        """위젯 초기화"""
        self.list_widget = QListWidget()
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("할 일 제목을 입력하세요...")
        self.input_field.setClearButtonEnabled(True)
        
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(24, 24)
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setToolTip("할 일 추가")
        
    def _setup_styles(self, color, light, dark, border):
        """스타일 설정 (리스트 영역 최대화, 아이템 높이 최소화)"""
        pastel = {
            '#d32f2f': '#ffdde0',
            '#f57c00': '#ffe5c2',
            '#388e3c': '#d6f5d6',
            '#757575': '#e0e0e0',
        }
        pastel_border = {
            '#d32f2f': '#e57373',
            '#f57c00': '#ffb74d',
            '#388e3c': '#81c784',
            '#757575': '#bdbdbd',
        }
        pastel_dark = {
            '#d32f2f': '#c62828',
            '#f57c00': '#ef6c00',
            '#388e3c': '#2e7d32',
            '#757575': '#616161',
        }
        pastel_light = pastel.get(color, light)
        pastel_border_c = pastel_border.get(color, border)
        pastel_dark_c = pastel_dark.get(color, dark)
        # 메인 프레임 스타일
        self.setStyleSheet(f"""
            QFrame#eisenhowerQuadrant {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {pastel_light}, stop:1 white);
                border-radius: 14px;
                border: 2px solid {pastel_border_c};
            }}
        """)
        # 리스트 위젯 스타일 (아이템 높이/여백 최소화)
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border-radius: 8px;
                border: none;
                margin: 2px 2px 0 2px;
                padding: 2px;
                font-size: 10pt;
                font-family: 'Segoe UI', 'Noto Sans KR', 'Pretendard', Arial, sans-serif;
            }}
            QListWidget::item {{
                padding: 3px 8px;
                border-radius: 5px;
                margin-bottom: 2px;
                font-size: 9.5pt;
                color: #333;
                background: rgba(255,255,255,0.7);
            }}
            QListWidget::item:selected, QListWidget::item:focus {{
                background: {pastel_border_c};
                color: #fff;
                outline: 2px solid #1976d2;
            }}
            QListWidget::item:hover {{
                background: #f3f6fa;
            }}
        """)
        # 입력 필드 스타일 (높이 최소화)
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background: #fff;
                border: 2px solid {pastel_border_c};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 9.5pt;
                font-family: 'Segoe UI', 'Noto Sans KR', 'Pretendard', Arial, sans-serif;
                color: #222;
                margin-right: 4px;
                min-height: 22px;
                max-height: 26px;
            }}
            QLineEdit:focus {{
                border: 2px solid {pastel_dark_c};
                background: #f8fbff;
            }}
        """)
        # 추가 버튼 스타일 (높이 최소화)
        self.add_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {pastel_border_c}, stop:1 {pastel_dark_c});
                color: #fff;
                border-radius: 6px;
                padding: 4px 12px;
                font-weight: 600;
                font-size: 9.5pt;
                font-family: 'Segoe UI', 'Noto Sans KR', 'Pretendard', Arial, sans-serif;
                border: none;
                min-height: 22px;
                max-height: 26px;
            }}
            QPushButton:hover {{
                background: {pastel_dark_c};
                color: #fff;
            }}
        """)
        
    def _setup_layout(self):
        """레이아웃 설정 (여백/간격 최소화)"""
        title_layout = QHBoxLayout()
        title_label = QLabel(self.keyword)
        title_label.setStyleSheet(f"font-size: 10.5pt; font-weight: bold; color: {self.color}; margin-bottom: 0px;")
        if self.icon:
            icon_label = QLabel()
            icon_label.setPixmap(self.icon.pixmap(15, 15))
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
        """시그널 연결"""
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.add_button.clicked.connect(self.add_task)
        self.input_field.returnPressed.connect(self.add_task)
        
    def _setup_animations(self):
        """애니메이션 설정"""
        self._fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self._fade_animation.setDuration(150)
        
    def _animate_add(self, item):
        """항목 추가 애니메이션"""
        item.setOpacity(0)
        self._fade_animation.setStartValue(0)
        self._fade_animation.setEndValue(1)
        self._fade_animation.start()
        
    def add_task(self) -> None:
        """입력창에서 할 일 추가"""
        title = self.input_field.text().strip()
        if not title:
            return
            
        # 중복 체크
        if any(item["title"] == title for item in self.items):
            if self.main_window:
                self.main_window.statusBar().showMessage("이미 존재하는 제목입니다.", 2000)
            self.input_field.clear()
            self.input_field.setFocus()
            return
        item_data = {
            "title": title,
            "details": "",
            "checked": False,
            "due_date": None,
            "reminders": []
        }
        if "due_date" not in item_data:
            item_data["due_date"] = None
        if "reminders" not in item_data:
            item_data["reminders"] = []
        self.items.append(item_data)
        self._add_list_item(item_data, idx=len(self.items)-1)
        self.input_field.clear()
        self.input_field.setFocus()
        if self.main_window:
            self.main_window.statusBar().showMessage("항목이 추가되었습니다.", 1500)

    def _add_list_item(self, item_data: dict, idx: Optional[int] = None) -> None:
        """리스트에 아이템 추가 및 표시 동기화."""
        item = QListWidgetItem()
        if idx is None:
            idx = len(self.items) - 1
        self._update_list_item(item, idx)
        item.setData(Qt.UserRole, item_data)
        self.list_widget.addItem(item)

    def _update_list_item(self, item: QListWidgetItem, idx: int) -> None:
        """리스트 아이템의 텍스트/툴팁/체크박스 상태를 동기화."""
        if idx < 0 or idx >= len(self.items):
            return
        item_data = self.items[idx]
        ICON_MEMO = "📝"
        ICON_DUE = "⏰"
        icons = []
        if item_data.get("details") and item_data["details"].strip():
            icons.append(ICON_MEMO)
        if item_data.get("due_date") and str(item_data["due_date"]).strip():
            icons.append(ICON_DUE)
        dday_str = ""
        due_date_cache = getattr(self, '_due_date_cache', None)
        if due_date_cache is None:
            due_date_cache = {}
            self._due_date_cache = due_date_cache
        due_key = item_data.get("due_date")
        if due_key and due_key in due_date_cache:
            dday_str = due_date_cache[due_key]
        elif item_data.get("due_date") and str(item_data["due_date"]).strip():
            try:
                due_dt = datetime.strptime(item_data["due_date"], "%Y-%m-%d %H:%M")
                now = datetime.now()
                due_date_only = due_dt.date()
                today = now.date()
                delta_days = (due_date_only - today).days
                if delta_days == 0:
                    dday_str = "[D-DAY]"
                elif delta_days > 0:
                    dday_str = f"[D-{delta_days}일]"
                else:
                    dday_str = f"[D+{abs(delta_days)}일]"
                due_date_cache[due_key] = dday_str
            except:
                pass
        title = item_data["title"]
        display_title = title
        if len(display_title) > 30:
            display_title = display_title[:30] + "..."
        prefix = []
        if dday_str:
            prefix.append(dday_str)
        if icons:
            prefix.append(' '.join(icons))
        if prefix:
            display_title = f"{' '.join(prefix)} {display_title}"
        item.setText(display_title)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked if item_data["checked"] else Qt.Unchecked)
        tooltip = []
        tooltip.append(f"제목: {title}")
        if item_data.get("details"):
            tooltip.append(f"세부내용: {item_data['details']}")
        if item_data.get("due_date"):
            tooltip.append(f"마감일: {item_data['due_date']}")
        if item_data.get("reminders"):
            reminder_str = ', '.join([
                f"{m//60}시간 전" if m >= 60 else f"{m}분 전" for m in item_data["reminders"]
            ])
            tooltip.append(f"알림: {reminder_str}")
        item.setToolTip("\n".join(tooltip))

    def on_item_double_clicked(self, item) -> None:
        idx = self.list_widget.row(item)
        if idx < 0 or idx >= len(self.items):
            return
        self.edit_task_dialog(idx, item)

    def show_context_menu(self, position) -> None:
        item = self.list_widget.itemAt(position)
        if not item:
            return
        idx = self.list_widget.row(item)
        if idx < 0 or idx >= len(self.items):
            return
        menu = QMenu()
        edit_action = menu.addAction("수정")
        delete_action = menu.addAction("삭제")
        menu.addSeparator()
        toggle_action = menu.addAction("완료 표시" if item.checkState() == Qt.Unchecked else "완료 해제")
        action = menu.exec_(self.list_widget.mapToGlobal(position))
        if not action:
            return
        if action == edit_action:
            self.edit_task_dialog(idx, item)
        elif action == delete_action:
            if idx < len(self.items):
                self.items.pop(idx)
            self.list_widget.takeItem(idx)
            if self.main_window:
                self.main_window.statusBar().showMessage("항목이 삭제되었습니다.", 1500)
        elif action == toggle_action:
            if idx < len(self.items):
                checked = not self.items[idx]["checked"]
                self.items[idx]["checked"] = checked
                item.setCheckState(Qt.Checked if checked else Qt.Unchecked)
                msg = "완료됨" if checked else "미완료로 변경됨"
                if self.main_window:
                    self.main_window.statusBar().showMessage(msg, 2000)

    def edit_task_dialog(self, idx, item):
        from PyQt5.QtWidgets import QDateTimeEdit, QCheckBox, QGridLayout
        from PyQt5.QtCore import QDateTime
        dialog = QDialog(self)
        dialog.setWindowTitle("항목 수정")
        layout = QVBoxLayout(dialog)
        title_edit = QLineEdit(self.items[idx]["title"])
        details_edit = QTextEdit(self.items[idx]["details"])
        layout.addWidget(QLabel("제목:"))
        layout.addWidget(title_edit)
        layout.addWidget(QLabel("세부 내용:"))
        layout.addWidget(details_edit)
        # 마감일
        due_label = QLabel("마감일:")
        due_edit = QDateTimeEdit()
        due_edit.setCalendarPopup(True)
        due_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        due_none_cb = QCheckBox("마감일 없음")
        if self.items[idx].get("due_date"):
            due_edit.setDateTime(QDateTime.fromString(self.items[idx]["due_date"], "yyyy-MM-dd HH:mm"))
            due_none_cb.setChecked(False)
            due_edit.setEnabled(True)
        else:
            due_edit.setDateTime(QDateTime.currentDateTime())
            due_none_cb.setChecked(True)
            due_edit.setEnabled(False)
        def on_due_none_changed(state):
            due_edit.setEnabled(not due_none_cb.isChecked())
        due_none_cb.stateChanged.connect(on_due_none_changed)
        layout.addWidget(due_label)
        layout.addWidget(due_edit)
        layout.addWidget(due_none_cb)
        # 알림 시점
        reminder_label = QLabel("알림 시점:")
        reminder_grid = QGridLayout()
        reminder_options = [
            ("1일 전", 24*60),
            ("3시간 전", 180),
            ("1시간 전", 60),
            ("30분 전", 30),
            ("10분 전", 10)
        ]
        reminder_checks = []
        for i, (label, minutes) in enumerate(reminder_options):
            cb = QCheckBox(label)
            if minutes in self.items[idx].get("reminders", []):
                cb.setChecked(True)
            reminder_checks.append((cb, minutes))
            reminder_grid.addWidget(cb, i // 3, i % 3)
        layout.addWidget(reminder_label)
        layout.addLayout(reminder_grid)
        # 버튼
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("확인")
        cancel_btn = QPushButton("취소")
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        if dialog.exec_() == QDialog.Accepted:
            new_title = title_edit.text().strip()
            new_details = details_edit.toPlainText().strip()
            if due_none_cb.isChecked():
                due_dt = None
            else:
                due_dt = due_edit.dateTime().toString("yyyy-MM-dd HH:mm")
            reminders = [minutes for cb, minutes in reminder_checks if cb.isChecked()]
            if new_title:
                self.items[idx]["title"] = new_title
                self.items[idx]["details"] = new_details
                self.items[idx]["due_date"] = due_dt
                self.items[idx]["reminders"] = reminders
                # 데이터 구조 보정
                if "due_date" not in self.items[idx]:
                    self.items[idx]["due_date"] = None
                if "reminders" not in self.items[idx]:
                    self.items[idx]["reminders"] = []
                self._update_list_item(item, idx)

    def clear_tasks(self):
        self.items = []
        self.list_widget.clear()

    def load_tasks(self, tasks_list):
        self.clear_tasks()
        items_to_add = []
        for item_data in tasks_list:
            if isinstance(item_data, str):
                item_data = {"title": item_data, "details": "", "checked": False, "due_date": None, "reminders": []}
            else:
                if "due_date" not in item_data:
                    item_data["due_date"] = None
                if "reminders" not in item_data:
                    item_data["reminders"] = []
            self.items.append(item_data)
            items_to_add.append(item_data)
        n = len(items_to_add)
        if n > 1:
            self.list_widget.setUpdatesEnabled(False)
        for i, item_data in enumerate(items_to_add):
            self._add_list_item(item_data, idx=i)
        if n > 1:
            self.list_widget.setUpdatesEnabled(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_file = "anti_adhd_settings.ini"
        self.data_dir = "anti_adhd_data"
        self.always_on_top = False
        self.window_opacity = 1.0
        self.auto_save_enabled = True
        self.project_status_label = None  # 상태바 프로젝트명 라벨 미리 선언
        
        # 캐시 관련 속성 초기화
        self._project_cache = {}
        self._cache_timer = QTimer()
        self._cache_timer.setInterval(30000)  # 30초마다 캐시 정리
        self._cache_timer.timeout.connect(self._cleanup_cache)
        self._cache_timer.start()

        self.init_ui()
        self.load_settings()

        self.projects_data = {}
        self.current_project_name = None
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir)
            except OSError as e:
                QMessageBox.critical(self, "오류", f"데이터 디렉토리 생성 실패: {self.data_dir}\n{e}")
        self.load_all_projects()
        self.select_initial_project()
        self.force_adjust_sidebar_width()

        self.project_list.model().rowsInserted.connect(lambda *_: QTimer.singleShot(0, self.adjust_sidebar_width))
        self.project_list.model().rowsRemoved.connect(lambda *_: QTimer.singleShot(0, self.adjust_sidebar_width))
        self.project_list.model().dataChanged.connect(lambda *_: QTimer.singleShot(0, self.adjust_sidebar_width))

        # 상태 표시줄 추가
        self.statusBar().showMessage("준비")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: #f5f5f5;
                border-top: 1px solid #d0d0d0;
                padding: 2px;
            }
            QStatusBar QLabel {
                padding: 2px 8px;
                color: #666;
            }
        """)
        # --- 프로젝트명 상태바 표시용 라벨 추가 ---
        self.project_status_label = QLabel()
        self.project_status_label.setStyleSheet("color: #1976d2; font-weight: bold; padding-right: 16px;")
        self.statusBar().addPermanentWidget(self.project_status_label)
        self.update_project_status_label()
        
        # 자동 백업 설정
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.last_backup_time = 0
        self.backup_interval = 300  # 5분마다 백업
        
        # 백업 디렉토리 생성
        if not os.path.exists(self.backup_dir):
            try:
                os.makedirs(self.backup_dir)
            except OSError as e:
                QMessageBox.warning(self, "백업 경고", 
                    f"백업 디렉토리를 생성할 수 없습니다: {e}\n자동 백업이 비활성화됩니다.")
                self.backup_interval = 0
        
        # 백업 타이머 설정
        self.backup_timer = QTimer()
        self.backup_timer.timeout.connect(self._auto_backup)
        if self.backup_interval > 0:
            self.backup_timer.start(self.backup_interval * 1000)
            
        # 단축키 설정
        self.setup_shortcuts()
        
        # 다크 모드 설정
        self.dark_mode = False
        self.setup_dark_mode()
        
        # 검색 기능 초기화
        self.setup_search()

    def setup_shortcuts(self):
        """키보드 단축키 설정"""
        # 프로젝트 관련
        QShortcut(Qt.CTRL + Qt.Key_N, self, self.add_new_project)
        QShortcut(Qt.CTRL + Qt.Key_S, self, self.save_current_project)
        QShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_S, self, self.save_project_as)
        QShortcut(Qt.CTRL + Qt.Key_R, self, self.rename_selected_project)
        QShortcut(Qt.Key_Delete, self, self.delete_selected_project)
        
        # 사이드바 관련
        QShortcut(Qt.CTRL + Qt.Key_B, self, self.toggle_sidebar)
        
        # 항목 관련
        QShortcut(Qt.CTRL + Qt.Key_Return, self, self.add_task_to_current_quadrant)
        QShortcut(Qt.CTRL + Qt.Key_Up, self, self.move_selected_task_up)
        QShortcut(Qt.CTRL + Qt.Key_Down, self, self.move_selected_task_down)
        
        # 기타
        QShortcut(Qt.CTRL + Qt.Key_Comma, self, self.open_settings_dialog)
        QShortcut(Qt.CTRL + Qt.Key_Z, self, self.restore_from_backup)
        
        QShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_B, self, self.toggle_main_toolbar)
        QShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_F, self, self.toggle_search_toolbar)
        
    def add_task_to_current_quadrant(self):
        """현재 선택된 사분면에 새 항목 추가"""
        if not self.current_project_name:
            return
            
        # 현재 포커스된 위젯 찾기
        focused_widget = QApplication.focusWidget()
        for i, quad in enumerate(self.quadrant_widgets):
            if quad.input_field == focused_widget:
                quad.add_task()
                return
                
        # 포커스된 위젯이 없으면 첫 번째 사분면에 추가
        self.quadrant_widgets[0].input_field.setFocus()
        self.quadrant_widgets[0].add_task()
        
    def move_selected_task_up(self):
        """선택된 항목을 위로 이동"""
        focused_widget = QApplication.focusWidget()
        for quad in self.quadrant_widgets:
            if quad.list_widget == focused_widget:
                current_row = quad.list_widget.currentRow()
                if current_row > 0:
                    # 데이터 이동
                    quad.items[current_row], quad.items[current_row-1] = \
                        quad.items[current_row-1], quad.items[current_row]
                    
                    # UI 업데이트
                    item = quad.list_widget.takeItem(current_row)
                    quad.list_widget.insertItem(current_row-1, item)
                    quad.list_widget.setCurrentRow(current_row-1)
                return
                
    def move_selected_task_down(self):
        """선택된 항목을 아래로 이동"""
        focused_widget = QApplication.focusWidget()
        for quad in self.quadrant_widgets:
            if quad.list_widget == focused_widget:
                current_row = quad.list_widget.currentRow()
                if current_row < quad.list_widget.count() - 1:
                    # 데이터 이동
                    quad.items[current_row], quad.items[current_row+1] = \
                        quad.items[current_row+1], quad.items[current_row]
                    
                    # UI 업데이트
                    item = quad.list_widget.takeItem(current_row)
                    quad.list_widget.insertItem(current_row+1, item)
                    quad.list_widget.setCurrentRow(current_row+1)
                return
                
    def keyPressEvent(self, event):
        """전역 키 이벤트 처리"""
        # ESC 키로 검색 초기화
        if event.key() == Qt.Key_Escape:
            if self.search_input.hasFocus():
                self.clear_search()
                return
            # 기존 ESC 키 동작
            focused_widget = QApplication.focusWidget()
            if isinstance(focused_widget, QLineEdit):
                focused_widget.clearFocus()
                return
                
        # CTRL + F로 검색창 포커스
        if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.search_input.setFocus()
            self.search_input.selectAll()
            return
            
        super().keyPressEvent(event)

    def _cleanup_cache(self):
        """오래된 캐시 데이터 정리"""
        current_time = time.time()
        to_remove = []
        for project_name, cache_data in self._project_cache.items():
            if current_time - cache_data['last_access'] > 300:  # 5분 이상 미접근
                to_remove.append(project_name)
        
        for project_name in to_remove:
            del self._project_cache[project_name]
            
    def _get_project_data(self, project_name):
        """프로젝트 데이터를 캐시에서 가져오거나 파일에서 로드"""
        if project_name in self._project_cache:
            self._project_cache[project_name]['last_access'] = time.time()
            return self._project_cache[project_name]['data']
            
        data = self.load_project_from_file(project_name)
        self._project_cache[project_name] = {
            'data': data,
            'last_access': time.time()
        }
        return data
        
    def force_adjust_sidebar_width(self):
        self.adjust_sidebar_width()
        QApplication.processEvents()
        QTimer.singleShot(0, self.adjust_sidebar_width)
        QTimer.singleShot(50, self.adjust_sidebar_width)
        QTimer.singleShot(200, self.adjust_sidebar_width)
        QTimer.singleShot(500, self.adjust_sidebar_width)

    def adjust_sidebar_width(self):
        min_width = 100
        max_width = 300
        QApplication.processEvents()
        max_width_item = min_width
        for i in range(self.project_list.count()):
            rect = self.project_list.visualItemRect(self.project_list.item(i))
            if rect.width() > max_width_item:
                max_width_item = rect.width()
        width = min(max(min_width, max_width_item + 32), max_width)
        self.sidebar.setFixedWidth(width)

    def init_ui(self):
        self.setWindowTitle("Anti-ADHD (Eisenhower Matrix)")
        # --- 디자인 토큰 ---
        PRIMARY = "#1976d2"
        ACCENT = "#ff9800"
        ERROR = "#d32f2f"
        BG = "#f8f9fa"
        BORDER = "#e0e0e0"
        FONT = "'Segoe UI', 'Noto Sans KR', 'Pretendard', Arial, sans-serif"
        # --- 메뉴바 (기존 코드 유지) ---
        menubar = self.menuBar()
        # 파일 메뉴
        file_menu = menubar.addMenu("파일")
        new_project_action = QAction("새 프로젝트 만들기", self)
        new_project_action.triggered.connect(self.add_new_project)
        file_menu.addAction(new_project_action)
        import_project_action = QAction("프로젝트 가져오기...", self)
        import_project_action.triggered.connect(self.import_project_file)
        file_menu.addAction(import_project_action)
        file_menu.addSeparator()
        save_project_action = QAction("현재 프로젝트 저장", self)
        save_project_action.setShortcut("Ctrl+S")
        save_project_action.triggered.connect(self.save_current_project)
        file_menu.addAction(save_project_action)
        save_project_as_action = QAction("현재 프로젝트 다른 이름으로 저장...", self)
        save_project_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_project_as_action)
        file_menu.addSeparator()
        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        # 보기 메뉴
        view_menu = menubar.addMenu("보기")
        self.toggle_toolbar_action = QAction("메인 툴바 보이기", self)
        self.toggle_toolbar_action.setCheckable(True)
        self.toggle_toolbar_action.setChecked(True)
        self.toggle_toolbar_action.setShortcut("Ctrl+Shift+B")
        self.toggle_toolbar_action.setToolTip("메인 툴바 보이기/숨기기 (Ctrl+Shift+B)")
        self.toggle_toolbar_action.triggered.connect(self.toggle_main_toolbar)
        view_menu.addAction(self.toggle_toolbar_action)
        self.toggle_searchbar_action = QAction("검색 툴바 보이기", self)
        self.toggle_searchbar_action.setCheckable(True)
        self.toggle_searchbar_action.setChecked(True)
        self.toggle_searchbar_action.setShortcut("Ctrl+Shift+F")
        self.toggle_searchbar_action.setToolTip("검색 툴바 보이기/숨기기 (Ctrl+Shift+F)")
        self.toggle_searchbar_action.triggered.connect(self.toggle_search_toolbar)
        view_menu.addAction(self.toggle_searchbar_action)
        # 통계 메뉴 (중복 없이 한 번만)
        stats_menu = menubar.addMenu("통계")
        show_stats_action = QAction("작업 통계 보기", self)
        show_stats_action.triggered.connect(self.show_task_statistics)
        stats_menu.addAction(show_stats_action)
        export_report_action = QAction("보고서 내보내기...", self)
        export_report_action.triggered.connect(self.export_task_report)
        stats_menu.addAction(export_report_action)
        # 설정 메뉴
        settings_menu = menubar.addMenu("설정")
        settings_main_action = QAction("설정 열기...", self)
        settings_main_action.triggered.connect(self.open_settings_dialog)
        settings_menu.addAction(settings_main_action)
        # 도움말 메뉴
        help_menu = menubar.addMenu("도움말")
        about_action = QAction("프로그램 정보", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "정보", "ANTI-ADHD\nEisenhower Matrix 기반 생산성 도구"))
        help_menu.addAction(about_action)
        # --- 툴바(아이콘만, 좌측 정렬, 우측 여백 완전 제거) ---
        self.toolbar = self.addToolBar("메인 툴바")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setIconSize(QSize(20, 20))
        self.toolbar.setStyleSheet(f"""
            QToolBar {{
                background: {BG};
                border-bottom: 1.5px solid {BORDER};
                padding: 0 0 0 0;
                spacing: 0px;
                min-height: 32px;
                margin: 0;
            }}
            QToolButton {{
                padding: 3px 4px;
                border-radius: 5px;
                background: transparent;
                color: {PRIMARY};
            }}
            QToolButton:checked {{
                background: #e3f0ff;
            }}
            QToolButton:hover {{
                background: #e8e8e8;
            }}
            QToolButton:focus {{
                outline: 2px solid {PRIMARY};
                background: #e3f0ff;
            }}
        """)
        # opacity_icon은 툴바 생성 후에 만들어야 함
        opacity_icon = QIcon(self.create_opacity_icon(QColor("black")))
        self.opacity_action = QAction(opacity_icon, "", self)
        self.opacity_action.setToolTip("창 투명도 조절")
        self.opacity_action.triggered.connect(self.show_opacity_popup)
        self.opacity_popup = None
        # --- 툴바 액션 인스턴스 생성 및 설정 (addAction보다 먼저) ---
        self.toggle_sidebar_action = QAction(self)
        self.toggle_sidebar_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.toggle_sidebar_action.setToolTip("프로젝트 목록 보이기/숨기기")
        self.toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        self.dark_mode_action = QAction(self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.dark_mode_action.setToolTip("다크 모드 전환")
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.always_on_top_action = QAction(self)
        self.always_on_top_action.setCheckable(True)
        self.update_always_on_top_icon()
        self.always_on_top_action.triggered.connect(self.toggle_always_on_top)
        settings_toolbar_icon = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        self.settings_toolbar_action = QAction(settings_toolbar_icon, "", self)
        self.settings_toolbar_action.setToolTip("애플리케이션 설정 열기")
        self.settings_toolbar_action.triggered.connect(self.open_settings_dialog)
        # --- 툴바 액션 좌측 정렬 (spacer 제거) ---
        self.toolbar.addAction(self.toggle_sidebar_action)
        self.toolbar.addAction(self.dark_mode_action)
        self.toolbar.addAction(self.opacity_action)
        self.toolbar.addAction(self.always_on_top_action)
        self.toolbar.addAction(self.settings_toolbar_action)
        # --- 검색 툴바(한 번만 생성) ---
        self.search_toolbar = self.addToolBar("검색")
        self.search_toolbar.setObjectName("search")
        self.search_toolbar.setAllowedAreas(Qt.NoToolBarArea)
        self.search_toolbar.setFloatable(False)
        self.search_toolbar.setMovable(False)
        self.search_toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.search_toolbar.setIconSize(QSize(18, 18))
        self.search_toolbar.setStyleSheet(f"""
            QToolBar {{
                background: {BG};
                border-bottom: 1px solid {BORDER};
                padding: 4px 8px;
                spacing: 4px;
                min-height: 32px;
            }}
        """)

        # --- 사이드바 생성 및 스타일 ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFrameShape(QFrame.StyledPanel)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(8, 8, 8, 8)
        self.sidebar_layout.setSpacing(4)
        self.project_list_label = QLabel("프로젝트 목록:")
        self.project_list_label.setStyleSheet(f"font-size: 10pt; color: {PRIMARY}; font-family: {FONT}; margin-bottom: 2px;")
        self.sidebar_layout.addWidget(self.project_list_label)
        self.project_list = ProjectListWidget(self)
        self.project_list.setContextMenuPolicy(2)  # Qt.CustomContextMenu = 2
        self.project_list.customContextMenuRequested.connect(self.show_project_context_menu)
        self.project_list.currentItemChanged.connect(self.on_project_selection_changed)
        self.project_list.setHorizontalScrollBarPolicy(1)  # Qt.ScrollBarAlwaysOff = 1
        self.project_list.setWordWrap(False)
        self.project_list.setUniformItemSizes(True)
        self.project_list.setStyleSheet(f"""
            QListWidget {{
                background: #fff;
                border: 1px solid {BORDER};
                border-radius: 7px;
                font-family: {FONT};
                font-size: 9.5pt;
                padding: 2px;
            }}
            QListWidget::item {{
                padding: 4px 8px;
                border-radius: 5px;
                margin-bottom: 2px;
            }}
            QListWidget::item:selected, QListWidget::item:focus {{
                background: {PRIMARY};
                color: #fff;
                outline: 2px solid {ACCENT};
            }}
            QListWidget::item:hover {{
                background: #f3f6fa;
            }}
        """)
        self.sidebar_layout.addWidget(self.project_list)
        self.sidebar_layout.addStretch()
        self.sidebar.setFixedWidth(148)
        # --- 검색바 스타일 개선 ---
        self.search_toolbar = self.addToolBar("검색")
        self.search_toolbar.setObjectName("search")
        self.search_toolbar.setAllowedAreas(Qt.NoToolBarArea)
        self.search_toolbar.setFloatable(False)
        self.search_toolbar.setMovable(False)
        self.search_toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.search_toolbar.setIconSize(QSize(18, 18))
        self.search_toolbar.setStyleSheet(f"""
            QToolBar {{
                background: {BG};
                border-bottom: 1px solid {BORDER};
                padding: 4px 8px;
                spacing: 4px;
                min-height: 32px;
            }}
        """)
        
        # --- 컴팩트한 툴바(메뉴바) 구성 --- #
        self.toolbar = self.addToolBar("메인 툴바")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setIconSize(QSize(18, 18))
        self.toolbar.setStyleSheet("QToolBar { spacing: 0px; margin: 0; padding: 0; min-height: 28px; background: #f5f6fa; border: none; } QToolButton { margin: 0 2px; padding: 2px; border-radius: 4px; background: transparent; } QToolButton:checked { background: #e3f0ff; } QToolButton:hover { background: #e8e8e8; }")

        # spacer로 오른쪽 정렬
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # --- 나머지 UI 구성 (사이드바, 4분면 등) --- #
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFrameShape(QFrame.StyledPanel)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.project_list_label = QLabel("프로젝트 목록:")
        self.sidebar_layout.addWidget(self.project_list_label)
        self.project_list = ProjectListWidget(self)
        self.project_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_list.customContextMenuRequested.connect(self.show_project_context_menu)
        self.project_list.currentItemChanged.connect(self.on_project_selection_changed)
        self.project_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.project_list.setWordWrap(False)
        self.project_list.setUniformItemSizes(True)
        self.sidebar_layout.addWidget(self.project_list)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.project_list.setContentsMargins(0, 0, 0, 0)
        self.project_list_label.setContentsMargins(0, 0, 0, 0)
        # [제프 딘] 사이드바 폭 완전 고정 (동적 조정 코드 제거)
        self.sidebar.setFixedWidth(140)

        # Eisenhower Matrix 색상/키워드/설명/아이콘 (한글화)
        quadrant_info = [
            ("#d32f2f", "중요·긴급", "즉시 처리", self.style().standardIcon(QStyle.SP_DialogApplyButton)),
            ("#f57c00", "중요", "계획/우선순위", self.style().standardIcon(QStyle.SP_BrowserReload)),
            ("#388e3c", "긴급", "위임/빠른 처리", self.style().standardIcon(QStyle.SP_ArrowRight)),
            ("#757575", "중요 아님·긴급 아님", "삭제/미루기", self.style().standardIcon(QStyle.SP_TrashIcon)),
        ]
        # 3x3 그리드로 확장하여 축 라벨이 사분면 바깥에 위치하도록
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        grid_layout.setContentsMargins(16, 16, 16, 16)
        self.quadrant_widgets = []
        for i, (color, keyword, desc, icon) in enumerate(quadrant_info):
            quad_widget = EisenhowerQuadrantWidget(color, keyword, desc, icon, self)
            row = 1 + (i // 2)
            col = 1 + (i % 2)
            grid_layout.addWidget(quad_widget, row, col)
            self.quadrant_widgets.append(quad_widget)

        main_content_widget = QWidget()
        main_content_widget.setLayout(grid_layout)
        main_content_widget.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(main_content_widget)
        self.splitter.setStretchFactor(1, 1)
        # QSplitter 핸들 완전 비활성화
        self.splitter.setHandleWidth(0)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        self.splitter.setStyleSheet("QSplitter { border: none; margin: 0; padding: 0; }")
        self.setCentralWidget(self.splitter)
        self.update_sidebar_toggle_icon()
        # 스타일시트는 기존과 동일하게 유지 또는 필요시 추가

        # 메인 툴바 우클릭 메뉴 및 옵션 완전 비활성화
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.setAllowedAreas(Qt.NoToolBarArea)
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

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
                self.statusBar().showMessage(f"새 프로젝트 '{project_name}' 생성 중...")
                QApplication.processEvents()
                
                self.projects_data[project_name] = {"tasks": [[], [], [], []]}
                self.project_list.addItem(project_name)
                self.project_list.setCurrentRow(self.project_list.count() - 1)
                self.save_project_to_file(project_name)
                self.adjust_sidebar_width()
                
                self.statusBar().showMessage(f"새 프로젝트 '{project_name}' 생성 완료", 3000)
            else:
                QMessageBox.warning(self, "중복 오류", "이미 존재하는 프로젝트 이름입니다.")

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
            old_file_path = os.path.join(self.data_dir, f"project_{old_name}.json")
            new_file_path = os.path.join(self.data_dir, f"project_{new_name_stripped}.json")
            if os.path.exists(old_file_path):
                try:
                    os.rename(old_file_path, new_file_path)
                except OSError as e:
                    QMessageBox.critical(self, "파일 오류", f"프로젝트 파일 이름 변경 실패: {e}")
            if self.auto_save_enabled:
                self.save_project_to_file(new_name_stripped)
            self.adjust_sidebar_width()

    def delete_selected_project(self):
        current_item = self.project_list.currentItem()
        if not current_item:
            return
        project_name = current_item.text()
        reply = QMessageBox.question(self, "프로젝트 삭제", f"'{project_name}' 프로젝트를 삭제하시겠습니까?\n(데이터와 해당 프로젝트 파일 모두 삭제됩니다!)", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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
                new_row = max(0, row - 1)
                if new_row < self.project_list.count():
                    self.project_list.setCurrentRow(new_row)
                else:
                    self.project_list.setCurrentRow(self.project_list.count() - 1 if self.project_list.count() > 0 else -1)
            else:
                self.current_project_name = None
                self.clear_all_quadrants()
            self.adjust_sidebar_width()

    def on_project_selection_changed(self, current_item, previous_item):
        # 이전 프로젝트 저장 (자동 저장 옵션에 따라)
        if previous_item and previous_item.text() in self.projects_data:
            if self.auto_save_enabled:
                self.save_project_to_file(previous_item.text())

        if current_item:
            self.current_project_name = current_item.text()
            # 캐시된 데이터 사용
            project_data = self._get_project_data(self.current_project_name)
            self.update_quadrant_display(self.current_project_name)
            self.update_project_status_label()  # 상태바 프로젝트명 갱신
        else:
            self.current_project_name = None
            self.clear_all_quadrants()
            self.update_project_status_label()

    def save_project_to_file(self, project_name):
        if not project_name or project_name not in self.projects_data:
            return
        self.statusBar().showMessage(f"'{project_name}' 저장 중...")
        QApplication.processEvents()
        file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
        try:
            # --- 마감일/알림 필드 보장: 모든 항목에 due_date, reminders 필드가 반드시 포함되도록 ---
            project = self.projects_data[project_name]
            for i, quadrant in enumerate(project.get("tasks", [])):
                for j, item in enumerate(quadrant):
                    if not isinstance(item, dict):
                        # 문자열 등 dict가 아니면 마이그레이션
                        item = {"title": str(item), "details": "", "checked": False, "due_date": None, "reminders": []}
                        quadrant[j] = item
                    if "due_date" not in item:
                        item["due_date"] = None
                    if "reminders" not in item:
                        item["reminders"] = []
            # 임시 파일에 먼저 저장
            temp_file_path = file_path + '.tmp'
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.projects_data[project_name], f, ensure_ascii=False, indent=4)
            # 저장 성공 시 기존 파일 교체
            if os.path.exists(file_path):
                os.replace(temp_file_path, file_path)
            else:
                os.rename(temp_file_path, file_path)
            # 캐시 업데이트
            self._project_cache[project_name] = {
                'data': self.projects_data[project_name],
                'last_access': time.time()
            }
        except (IOError, OSError) as e:
            QMessageBox.critical(self, "저장 오류", 
                f"프로젝트 '{project_name}' 저장 중 오류가 발생했습니다:\n{e}\n\n"
                "임시 파일이 남아있을 수 있습니다. 프로그램을 다시 시작해주세요.")
            try:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            except:
                pass
        self.statusBar().showMessage(f"'{project_name}' 저장 완료", 3000)
        
    def load_project_from_file(self, project_name):
        self.statusBar().showMessage(f"'{project_name}' 로드 중...")
        QApplication.processEvents()
        
        file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
        if not os.path.exists(file_path):
            return {"tasks": [[], [], [], []]}
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 데이터 구조 검증 및 보정
            if not isinstance(data, dict):
                raise ValueError("프로젝트 데이터가 올바른 형식이 아닙니다.")
                
            if "tasks" not in data:
                data["tasks"] = [[], [], [], []]
            elif not isinstance(data["tasks"], list) or len(data["tasks"]) != 4:
                # tasks 배열이 올바르지 않으면 기본값으로 초기화
                data["tasks"] = [[], [], [], []]
                
            self.statusBar().showMessage(f"'{project_name}' 로드 완료", 3000)
            return data
            
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "로드 오류", 
                f"프로젝트 '{project_name}' 파일이 손상되었습니다:\n{e}\n\n"
                "프로젝트를 백업에서 복원하거나 새로 만들어주세요.")
            return {"tasks": [[], [], [], []]}
            
        except Exception as e:
            QMessageBox.critical(self, "로드 오류", 
                f"프로젝트 '{project_name}' 로드 중 오류가 발생했습니다:\n{e}")
            return {"tasks": [[], [], [], []]}

    def load_all_projects(self):
        self.project_list.clear()
        self.projects_data.clear()
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        for filename in os.listdir(self.data_dir):
            if filename.startswith("project_") and filename.endswith(".json"):
                project_name = filename[8:-5]
                project_data = self.load_project_from_file(project_name)
                if "completed" not in project_data:
                    project_data["completed"] = []
                    for tasks in project_data.get("tasks", [[], [], [], []]):
                        project_data["completed"].append([False] * len(tasks))
                self.projects_data[project_name] = project_data
                self.project_list.addItem(project_name)
        self.adjust_sidebar_width()

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
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
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
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
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
                QMessageBox.critical(self, "오류", f"데이터 디렉토리 생성 실패: {self.data_dir}\n{e}")
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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 사이드바 폭 조정 코드 없음 (고정 폭)

    def _auto_backup(self):
        """자동 백업 수행"""
        current_time = time.time()
        if current_time - self.last_backup_time < self.backup_interval:
            return
            
        if not self.current_project_name:
            return
            
        try:
            # 백업 파일명 생성 (타임스탬프 포함)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{self.current_project_name}_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # 현재 프로젝트 데이터 백업
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.projects_data[self.current_project_name], f, 
                         ensure_ascii=False, indent=4)
            
            # 오래된 백업 파일 정리 (최근 10개만 유지)
            self._cleanup_old_backups()
            
            self.last_backup_time = current_time
            
        except Exception as e:
            print(f"자동 백업 실패: {e}")  # 사용자에게는 알리지 않음
            
    def _cleanup_old_backups(self):
        """오래된 백업 파일 정리"""
        try:
            # 현재 프로젝트의 백업 파일만 필터링
            backup_files = [f for f in os.listdir(self.backup_dir) 
                          if f.startswith(f"backup_{self.current_project_name}_")]
            
            # 타임스탬프로 정렬
            backup_files.sort(reverse=True)
            
            # 최근 10개를 제외한 나머지 삭제
            for old_file in backup_files[10:]:
                try:
                    os.remove(os.path.join(self.backup_dir, old_file))
                except:
                    pass
                    
        except Exception as e:
            print(f"백업 파일 정리 실패: {e}")
            
    def restore_from_backup(self):
        """백업에서 복원"""
        if not self.current_project_name:
            QMessageBox.information(self, "복원", "복원할 프로젝트를 선택해주세요.")
            return
            
        try:
            # 현재 프로젝트의 백업 파일 목록 가져오기
            backup_files = [f for f in os.listdir(self.backup_dir) 
                          if f.startswith(f"backup_{self.current_project_name}_")]
            
            if not backup_files:
                QMessageBox.information(self, "복원", "사용 가능한 백업이 없습니다.")
                return
                
            # 백업 파일 선택 다이얼로그
            backup_files.sort(reverse=True)  # 최신순 정렬
            backup_list = QListWidget()
            for backup in backup_files:
                # 파일명에서 타임스탬프 추출하여 보기 좋게 표시
                timestamp = backup.split('_')[-1].replace('.json', '')
                date_str = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}"
                backup_list.addItem(date_str)
                
            dialog = QDialog(self)
            dialog.setWindowTitle("백업에서 복원")
            layout = QVBoxLayout(dialog)
            
            layout.addWidget(QLabel("복원할 백업을 선택하세요:"))
            layout.addWidget(backup_list)
            
            buttons = QHBoxLayout()
            restore_btn = QPushButton("복원")
            cancel_btn = QPushButton("취소")
            buttons.addWidget(restore_btn)
            buttons.addWidget(cancel_btn)
            layout.addLayout(buttons)
            
            restore_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)
            
            if dialog.exec_() == QDialog.Accepted and backup_list.currentRow() >= 0:
                selected_backup = backup_files[backup_list.currentRow()]
                backup_path = os.path.join(self.backup_dir, selected_backup)
                
                # 백업 데이터 로드
                with open(backup_path, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                    
                # 현재 데이터 백업
                self.save_project_to_file(self.current_project_name)
                
                # 백업 데이터로 복원
                self.projects_data[self.current_project_name] = backup_data
                self.update_quadrant_display(self.current_project_name)
                
                QMessageBox.information(self, "복원 완료", 
                    f"프로젝트가 {selected_backup} 백업에서 복원되었습니다.")
                
        except Exception as e:
            QMessageBox.critical(self, "복원 오류", 
                f"백업에서 복원하는 중 오류가 발생했습니다:\n{e}")

    def setup_dark_mode(self):
        """다크 모드 설정"""
        # 이미 다크 모드 액션이 있으면 중복 추가 방지
        if hasattr(self, 'dark_mode_action'):
            return
        self.dark_mode_action = QAction(self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.dark_mode_action.setToolTip("다크 모드 전환")
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.toolbar.addAction(self.dark_mode_action)
        
        # 초기 다크 모드 상태 설정
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
        self.dark_mode = settings.value("darkMode", False, type=bool)
        self.dark_mode_action.setChecked(self.dark_mode)
        self.apply_theme()
        
    def toggle_dark_mode(self):
        """다크 모드 전환"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        
        # 설정 저장
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
        settings.setValue("darkMode", self.dark_mode)
        
    def apply_theme(self):
        """현재 테마 적용"""
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QWidget {
                    font-family: "Segoe UI", "SF Pro Display", "Helvetica Neue", "Arial", sans-serif;
                    color: #e0e0e0;
                }
                QGroupBox {
                    font-weight: 600;
                    border: 1px solid #404040;
                    border-radius: 8px;
                    margin-top: 8px;
                    background-color: #2d2d2d;
                    padding: 12px;
                }
                QGroupBox::title {
                    color: #e0e0e0;
                }
                QListWidget {
                    border: 1px solid #404040;
                    border-radius: 6px;
                    background-color: #2d2d2d;
                    padding: 4px;
                }
                QListWidget::item {
                    padding: 6px;
                    border-radius: 4px;
                    margin: 2px 0;
                }
                QListWidget::item:selected {
                    background-color: #0d47a1;
                    color: white;
                }
                QListWidget::item:hover {
                    background-color: #404040;
                }
                QTextEdit, QLineEdit {
                    border: 1px solid #404040;
                    border-radius: 6px;
                    padding: 6px;
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    selection-background-color: #0d47a1;
                    selection-color: white;
                }
                QTextEdit:focus, QLineEdit:focus {
                    border: 1px solid #0d47a1;
                }
                QPushButton {
                    background-color: #2d2d2d;
                    border: 1px solid #404040;
                    border-radius: 6px;
                    padding: 6px 12px;
                    min-height: 24px;
                    font-weight: 500;
                    color: #e0e0e0;
                }
                QPushButton:hover {
                    background-color: #404040;
                    border-color: #0d47a1;
                }
                QPushButton:pressed {
                    background-color: #505050;
                }
                QPushButton:disabled {
                    background-color: #2d2d2d;
                    color: #808080;
                }
                QToolBar {
                    background-color: #2d2d2d;
                    border-bottom: 1px solid #404040;
                    padding: 4px;
                    spacing: 4px;
                }
                QToolButton {
                    padding: 4px;
                    border-radius: 4px;
                    background: transparent;
                    color: #e0e0e0;
                }
                QToolButton:hover {
                    background-color: #404040;
                }
                QToolButton:pressed {
                    background-color: #505050;
                }
                QMenu {
                    background-color: #2d2d2d;
                    border: 1px solid #404040;
                    border-radius: 6px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 6px 24px;
                    border-radius: 4px;
                    color: #e0e0e0;
                }
                QMenu::item:selected {
                    background-color: #0d47a1;
                    color: white;
                }
                QDialog {
                    background-color: #1e1e1e;
                }
                QLabel {
                    background-color: transparent;
                    color: #e0e0e0;
                }
                QCheckBox {
                    spacing: 8px;
                    color: #e0e0e0;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border: 1px solid #404040;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                }
                QCheckBox::indicator:checked {
                    background-color: #0d47a1;
                    border-color: #0d47a1;
                }
                QCheckBox::indicator:hover {
                    border-color: #0d47a1;
                }
                QSlider::groove:horizontal {
                    border: 1px solid #404040;
                    background: #2d2d2d;
                    height: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #0d47a1;
                    border: none;
                    width: 16px;
                    margin: -4px 0;
                    border-radius: 8px;
                }
                QSlider::handle:horizontal:hover {
                    background: #1565c0;
                }
                QStatusBar {
                    background-color: #2d2d2d;
                    border-top: 1px solid #404040;
                    padding: 4px;
                }
                QStatusBar QLabel {
                    padding: 2px 8px;
                    color: #808080;
                }
                QToolBar#search {
                    background-color: #2d2d2d;
                    border-bottom: 1px solid #404040;
                }
                QToolBar#search QLineEdit {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #404040;
                    border-radius: 4px;
                    padding: 4px;
                }
                QToolBar#search QLineEdit:focus {
                    border: 1px solid #0d47a1;
                }
                QToolBar#search QLabel {
                    color: #e0e0e0;
                }
            """)
            # 검색 툴바 및 자식 위젯 직접 스타일 적용
            if hasattr(self, 'search_toolbar'):
                self.search_toolbar.setStyleSheet("QToolBar { background: #2d2d2d; border-bottom: 1px solid #404040; }")
            if hasattr(self, 'search_input'):
                self.search_input.setStyleSheet("QLineEdit { background: #2d2d2d; color: #e0e0e0; border: 1px solid #404040; border-radius: 4px; } QLineEdit:focus { border: 1px solid #0d47a1; }")
            if hasattr(self, 'search_options'):
                self.search_options.setStyleSheet("QToolButton { color: #e0e0e0; background: #2d2d2d; } QToolButton:hover { background: #404040; }")
            if hasattr(self, 'search_result_label'):
                self.search_result_label.setStyleSheet("color: #e0e0e0; padding: 0 8px;")
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f8f9fa;
                }
                QWidget {
                    font-family: "Segoe UI", "SF Pro Display", "Helvetica Neue", "Arial", sans-serif;
                    color: #2c3e50;
                }
                QGroupBox {
                    font-weight: 600;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    margin-top: 8px;
                    background-color: #ffffff;
                    padding: 12px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 8px;
                    color: #34495e;
                }
                QListWidget {
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    background-color: #ffffff;
                    padding: 4px;
                }
                QListWidget::item {
                    padding: 6px;
                    border-radius: 4px;
                    margin: 2px 0;
                }
                QListWidget::item:selected {
                    background-color: #3498db;
                    color: white;
                }
                QListWidget::item:hover {
                    background-color: #f0f0f0;
                }
                QTextEdit, QLineEdit {
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    padding: 6px;
                    background-color: #ffffff;
                    selection-background-color: #3498db;
                    selection-color: white;
                }
                QTextEdit:focus, QLineEdit:focus {
                    border: 1px solid #3498db;
                    background-color: #ffffff;
                }
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    padding: 6px 12px;
                    min-height: 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #f8f9fa;
                    border-color: #3498db;
                }
                QPushButton:pressed {
                    background-color: #e9ecef;
                }
                QPushButton:disabled {
                    background-color: #f8f9fa;
                    color: #adb5bd;
                }
                QToolBar {
                    background-color: #ffffff;
                    border-bottom: 1px solid #e0e0e0;
                    padding: 4px;
                    spacing: 4px;
                }
                QToolButton {
                    padding: 4px;
                    border-radius: 4px;
                    background: transparent;
                    color: #2c3e50;
                }
                QToolButton:hover {
                    background-color: #f8f9fa;
                }
                QToolButton:pressed {
                    background-color: #e9ecef;
                }
                QMenu {
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 6px 24px;
                    border-radius: 4px;
                }
                QMenu::item:selected {
                    background-color: #3498db;
                    color: white;
                }
                QDialog {
                    background-color: #f8f9fa;
                }
                QLabel {
                    background-color: transparent;
                }
                QCheckBox {
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    background-color: #ffffff;
                }
                QCheckBox::indicator:checked {
                    background-color: #3498db;
                    border-color: #3498db;
                }
                QCheckBox::indicator:hover {
                    border-color: #3498db;
                }
                QSlider::groove:horizontal {
                    border: 1px solid #e0e0e0;
                    background: #ffffff;
                    height: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #3498db;
                    border: none;
                    width: 16px;
                    margin: -4px 0;
                    border-radius: 8px;
                }
                QSlider::handle:horizontal:hover {
                    background: #2980b9;
                }
                QStatusBar {
                    background-color: #ffffff;
                    border-top: 1px solid #e0e0e0;
                    padding: 4px;
                }
                QStatusBar QLabel {
                    padding: 2px 8px;
                    color: #666;
                }
                QToolBar#search {
                    background-color: #ffffff;
                    border-bottom: 1px solid #e0e0e0;
                }
                QToolBar#search QLineEdit {
                    background-color: #ffffff;
                    color: #2c3e50;
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    padding: 4px;
                }
                QToolBar#search QLineEdit:focus {
                    border: 1px solid #3498db;
                }
                QToolBar#search QLabel {
                    color: #2c3e50;
                }
            """)
            # 검색 툴바 및 자식 위젯 직접 스타일 적용
            if hasattr(self, 'search_toolbar'):
                self.search_toolbar.setStyleSheet("QToolBar { background: #ffffff; border-bottom: 1px solid #e0e0e0; }")
            if hasattr(self, 'search_input'):
                self.search_input.setStyleSheet("QLineEdit { background: #ffffff; color: #2c3e50; border: 1px solid #e0e0e0; border-radius: 4px; } QLineEdit:focus { border: 1px solid #3498db; }")
            if hasattr(self, 'search_options'):
                self.search_options.setStyleSheet("QToolButton { color: #2c3e50; background: #ffffff; } QToolButton:hover { background: #f8f9fa; }")
            if hasattr(self, 'search_result_label'):
                self.search_result_label.setStyleSheet("color: #2c3e50; padding: 0 8px;")

    def setup_search(self):
        """검색 기능 설정"""
        self.search_toolbar = self.addToolBar("검색")
        self.search_toolbar.setObjectName("search")
        self.search_toolbar.setAllowedAreas(Qt.NoToolBarArea)
        self.search_toolbar.setFloatable(False)
        self.search_toolbar.setMovable(False)
        self.search_toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.search_toolbar.setIconSize(QSize(18, 18))
        # 검색 입력 필드
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("작업 검색...")
        self.search_input.setMinimumWidth(200)
        self.search_input.textChanged.connect(self.filter_tasks)
        self.search_toolbar.addWidget(self.search_input)
        # 검색 옵션
        self.search_options = QToolButton()
        self.search_options.setPopupMode(QToolButton.InstantPopup)
        self.search_options.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.search_options.setToolTip("검색 옵션")
        search_menu = QMenu()
        self.search_title_action = QAction("제목으로 검색", self)
        self.search_title_action.setCheckable(True)
        self.search_title_action.setChecked(True)
        self.search_details_action = QAction("세부 내용으로 검색", self)
        self.search_details_action.setCheckable(True)
        self.search_details_action.setChecked(True)
        self.search_completed_action = QAction("완료된 작업 포함", self)
        self.search_completed_action.setCheckable(True)
        self.search_completed_action.setChecked(True)
        search_menu.addAction(self.search_title_action)
        search_menu.addAction(self.search_details_action)
        search_menu.addAction(self.search_completed_action)
        self.search_options.setMenu(search_menu)
        self.search_toolbar.addWidget(self.search_options)
        # 검색 옵션 변경 시 필터링 다시 실행
        self.search_title_action.triggered.connect(self.filter_tasks)
        self.search_details_action.triggered.connect(self.filter_tasks)
        self.search_completed_action.triggered.connect(self.filter_tasks)
        # 검색 결과 표시 레이블
        self.search_result_label = QLabel()
        self.search_result_label.setStyleSheet("color: #666; padding: 0 8px;")
        self.search_toolbar.addWidget(self.search_result_label)
        # (검색 초기화 버튼/액션 완전히 제거)

    def filter_tasks(self):
        """작업 필터링"""
        search_text = self.search_input.text().lower()
        if not search_text:
            self.clear_search()
            return
            
        # 검색 옵션 확인
        search_title = self.search_title_action.isChecked()
        search_details = self.search_details_action.isChecked()
        include_completed = self.search_completed_action.isChecked()
        
        # 검색 결과 카운트
        total_tasks = 0
        matched_tasks = 0
        
        # 각 사분면의 작업 필터링
        for quad in self.quadrant_widgets:
            for i in range(quad.list_widget.count()):
                item = quad.list_widget.item(i)
                task_data = item.data(Qt.UserRole)
                total_tasks += 1
                
                # 완료된 작업 필터링
                if not include_completed and task_data.get("checked", False):
                    item.setHidden(True)
                    continue
                    
                # 검색어 매칭
                title_match = search_title and search_text in task_data.get("title", "").lower()
                details_match = search_details and search_text in task_data.get("details", "").lower()
                
                if title_match or details_match:
                    item.setHidden(False)
                    matched_tasks += 1
                else:
                    item.setHidden(True)
                    
        # 검색 결과 표시
        if matched_tasks > 0:
            self.search_result_label.setText(f"검색 결과: {matched_tasks}/{total_tasks}개 작업")
            self.search_result_label.setStyleSheet("color: #2c3e50; padding: 0 8px;")
        else:
            self.search_result_label.setText("검색 결과 없음")
            self.search_result_label.setStyleSheet("color: #e74c3c; padding: 0 8px;")
            
    def clear_search(self):
        """검색 초기화"""
        self.search_input.clear()
        self.search_result_label.clear()
        
        # 모든 작업 표시
        for quad in self.quadrant_widgets:
            for i in range(quad.list_widget.count()):
                quad.list_widget.item(i).setHidden(False)
                
    def show_task_statistics(self):
        """작업 통계 보기"""
        if not self.current_project_name:
            QMessageBox.information(self, "통계", "프로젝트를 선택해주세요.")
            return
            
        # 통계 데이터 수집
        total_tasks = 0
        completed_tasks = 0
        tasks_by_priority = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        tasks_by_quadrant = [0, 0, 0, 0]
        completed_by_quadrant = [0, 0, 0, 0]
        
        for i, quad in enumerate(self.quadrant_widgets):
            for item in quad.items:
                total_tasks += 1
                tasks_by_quadrant[i] += 1
                tasks_by_priority[item.get("priority", 0)] += 1
                
                if item.get("checked", False):
                    completed_tasks += 1
                    completed_by_quadrant[i] += 1
                    
        # 통계 대화상자 생성
        dialog = QDialog(self)
        dialog.setWindowTitle("작업 통계")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # 기본 통계
        basic_stats = QGroupBox("기본 통계")
        basic_layout = QFormLayout()
        basic_layout.addRow("전체 작업:", QLabel(f"{total_tasks}개"))
        basic_layout.addRow("완료된 작업:", QLabel(f"{completed_tasks}개"))
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            basic_layout.addRow("완료율:", QLabel(f"{completion_rate:.1f}%"))
        basic_stats.setLayout(basic_layout)
        layout.addWidget(basic_stats)
        
        # 사분면별 통계
        quadrant_stats = QGroupBox("사분면별 통계")
        quadrant_layout = QFormLayout()
        quadrant_names = ["중요·긴급", "중요", "긴급", "중요 아님·긴급 아님"]
        for i, name in enumerate(quadrant_names):
            total = tasks_by_quadrant[i]
            completed = completed_by_quadrant[i]
            rate = (completed / total * 100) if total > 0 else 0
            quadrant_layout.addRow(f"{name}:", 
                QLabel(f"전체 {total}개, 완료 {completed}개 ({rate:.1f}%)"))
        quadrant_stats.setLayout(quadrant_layout)
        layout.addWidget(quadrant_stats)
        
        # 우선순위별 통계
        priority_stats = QGroupBox("우선순위별 통계")
        priority_layout = QFormLayout()
        for i in range(6):
            count = tasks_by_priority[i]
            if count > 0:
                label = "우선순위 없음" if i == 0 else f"우선순위 {i}"
                priority_layout.addRow(f"{label}:", QLabel(f"{count}개"))
        priority_stats.setLayout(priority_layout)
        layout.addWidget(priority_stats)
        
        # 닫기 버튼
        close_button = QPushButton("닫기")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        dialog.exec_()
        
    def export_task_report(self):
        """작업 보고서 내보내기"""
        if not self.current_project_name:
            QMessageBox.information(self, "보고서", "프로젝트를 선택해주세요.")
            return
        # 파일 저장 다이얼로그
        file_path, _ = QFileDialog.getSaveFileName(
            self, "보고서 저장", 
            f"task_report_{self.current_project_name}.txt",
            "텍스트 파일 (*.txt)"
        )
        if not file_path:
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 보고서 헤더
                f.write(f"작업 보고서: {self.current_project_name}\n")
                f.write(f"생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                # 사분면별 작업 목록
                quadrant_names = ["중요·긴급", "중요", "긴급", "중요 아님·긴급 아님"]
                for i, (name, quad) in enumerate(zip(quadrant_names, self.quadrant_widgets)):
                    f.write(f"[{name}]\n")
                    f.write("-" * 30 + "\n")
                    if not quad.items:
                        f.write("작업 없음\n")
                    else:
                        for item in quad.items:
                            # 상태 표시
                            status = "✓" if item.get("checked", False) else "□"
                            f.write(f"{status} {item['title']}\n")
                            if item.get("details"):
                                f.write(f"    {item['details']}\n")
                            if item.get("due_date"):
                                f.write(f"    마감일: {item['due_date']}\n")
                            if item.get("reminders"):
                                reminder_str = ', '.join([
                                    f"{m//60}시간 전" if m >= 60 else f"{m}분 전" for m in item["reminders"]
                                ])
                                f.write(f"    알림: {reminder_str}\n")
                    f.write("\n")
            QMessageBox.information(self, "보고서 저장", 
                f"작업 보고서가 다음 위치에 저장되었습니다:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "보고서 저장 오류", 
                f"보고서 저장 중 오류가 발생했습니다:\n{e}")

    def toggle_main_toolbar(self):
        visible = not self.toolbar.isVisible()
        self.toolbar.setVisible(visible)
        self.toggle_toolbar_action.setChecked(visible)

    def toggle_search_toolbar(self):
        visible = not self.search_toolbar.isVisible()
        self.search_toolbar.setVisible(visible)
        self.toggle_searchbar_action.setChecked(visible)

    def check_due_reminders(self):
        now = datetime.now()
        for quad in self.quadrant_widgets:
            for idx, item in enumerate(quad.items):
                due_str = item.get("due_date")
                if not due_str:
                    continue
                try:
                    due_dt = datetime.strptime(due_str, "%Y-%m-%d %H:%M")
                except Exception:
                    continue
                # 마감일이 지났으면 경고(한 번만)
                if now > due_dt and (idx, 'overdue') not in quad.notified_set:
                    self.show_reminder_popup(item["title"], due_dt, overdue=True)
                    quad.notified_set.add((idx, 'overdue'))
                # 알림 시점 체크
                for minutes in item.get("reminders", []):
                    remind_time = due_dt - timedelta(minutes=minutes)
                    key = (idx, minutes)
                    if remind_time <= now < due_dt and key not in quad.notified_set:
                        self.show_reminder_popup(item["title"], due_dt, minutes=minutes)
                        quad.notified_set.add(key)

    def show_reminder_popup(self, title, due_dt, minutes=None, overdue=False):
        if overdue:
            msg = f"[마감 경과] '{title}'의 마감일이 지났습니다! (마감: {due_dt.strftime('%Y-%m-%d %H:%M')})"
        elif minutes is not None:
            if minutes >= 60:
                t = f"{minutes//60}시간 전"
            else:
                t = f"{minutes}분 전"
            msg = f"[알림] '{title}'의 마감이 {t}입니다! (마감: {due_dt.strftime('%Y-%m-%d %H:%M')})"
        else:
            msg = f"[알림] '{title}'의 마감이 임박했습니다! (마감: {due_dt.strftime('%Y-%m-%d %H:%M')})"
        # 팝업 및 상태바 동시 표시
        QMessageBox.information(self, "마감 알림", msg)
        self.statusBar().showMessage(msg, 10000)

    def update_project_status_label(self):
        """상태바에 현재 프로젝트명 표시 (방어적 체크)"""
        if not hasattr(self, "project_status_label") or self.project_status_label is None:
            return
        if self.current_project_name:
            self.project_status_label.setText(f"프로젝트: {self.current_project_name}")
        else:
            self.project_status_label.setText("")

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
                background-color: rgba(240, 240, 240, 0.95);
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
        self.setFixedSize(220, 60)

    def slider_value_changed(self, value):
        self.value_label.setText(f"{value}%")
        self.main_window.set_window_opacity(value / 100.0)

    def show_at(self, pos):
        self.move(pos)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f8f9fa;
        }
        QWidget {
            font-family: "Segoe UI", "SF Pro Display", "Helvetica Neue", "Arial", sans-serif;
            color: #2c3e50;
        }
        QGroupBox {
            font-weight: 600;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 8px;
            background-color: #ffffff;
            padding: 12px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            color: #34495e;
        }
        QListWidget {
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            background-color: #ffffff;
            padding: 4px;
        }
        QListWidget::item {
            padding: 6px;
            border-radius: 4px;
            margin: 2px 0;
        }
        QListWidget::item:selected {
            background-color: #3498db;
            color: white;
        }
        QListWidget::item:hover {
            background-color: #f0f0f0;
        }
        QTextEdit, QLineEdit {
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 6px;
            background-color: #ffffff;
            selection-background-color: #3498db;
            selection-color: white;
        }
        QTextEdit:focus, QLineEdit:focus {
            border: 1px solid #3498db;
            background-color: #ffffff;
        }
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 6px 12px;
            min-height: 24px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #f8f9fa;
            border-color: #3498db;
        }
        QPushButton:pressed {
            background-color: #e9ecef;
        }
        QPushButton:disabled {
            background-color: #f8f9fa;
            color: #adb5bd;
        }
        QToolBar {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            padding: 4px;
            spacing: 4px;
        }
        QToolButton {
            padding: 4px;
            border-radius: 4px;
            background: transparent;
        }
        QToolButton:hover {
            background-color: #f8f9fa;
        }
        QToolButton:pressed {
            background-color: #e9ecef;
        }
        QMenu {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 4px;
        }
        QMenu::item {
            padding: 6px 24px;
            border-radius: 4px;
        }
        QMenu::item:selected {
            background-color: #3498db;
            color: white;
        }
        QDialog {
            background-color: #f8f9fa;
        }
        QLabel {
            background-color: transparent;
        }
        QCheckBox {
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            background-color: #ffffff;
        }
        QCheckBox::indicator:checked {
            background-color: #3498db;
            border-color: #3498db;
        }
        QCheckBox::indicator:hover {
            border-color: #3498db;
        }
        QSlider::groove:horizontal {
            border: 1px solid #e0e0e0;
            background: #ffffff;
            height: 8px;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #3498db;
            border: none;
            width: 16px;
            margin: -4px 0;
            border-radius: 8px;
        }
        QSlider::handle:horizontal:hover {
            background: #2980b9;
        }
        QStatusBar {
            background-color: #ffffff;
            border-top: 1px solid #e0e0e0;
            padding: 4px;
        }
        QStatusBar QLabel {
            padding: 2px 8px;
            color: #666;
        }
    """)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_()) 