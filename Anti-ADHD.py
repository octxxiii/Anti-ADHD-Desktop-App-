from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter, QListWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLineEdit, QPushButton, QAction, QMenu, QGridLayout, QTextEdit, QInputDialog,
    QMessageBox, QFileDialog, QListWidgetItem, QDialog, QLabel, QCheckBox, QSlider, QStyle, QSizePolicy,
    QTabWidget, QFormLayout, QToolButton, QFrame, QStatusBar, QShortcut, QDateTimeEdit, QAbstractItemView,
    QDialogButtonBox, QComboBox, QScrollArea, QDesktopWidget
)
from PyQt5.QtCore import Qt, QSettings, QUrl, QPoint, QSize, QTimer, QDateTime, QCoreApplication, QLocale
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QIcon, QDesktopServices, QPainter, QPen, QColor, QPixmap, QCursor, QFont, QPalette
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
import sys
import os
import json
import zipfile
import shutil
import time
from datetime import datetime, timedelta
from typing import Optional

# 번역 데이터
TRANSLATIONS = {
    "ko": {
        "Language": "언어",
        "Korean": "한국어",
        "English": "영어",
        "Settings": "설정",
        "General": "일반",
        "Appearance": "외관",
        "Data": "데이터",
        "About": "정보",
        "Auto Save": "자동 저장",
        "Check for Updates": "업데이트 확인",
        "Data Directory": "데이터 디렉토리",
        "Browse": "찾아보기",
        "Backup": "백업",
        "Restore": "복원",
        "Reset": "초기화",
        "Dark Mode": "다크 모드",
        "Window Opacity": "창 투명도",
        "Always on Top": "항상 위",
        "Search": "검색",
        "Search in Title": "제목에서 검색",
        "Search in Details": "내용에서 검색",
        "Include Completed": "완료된 항목 포함",
        "Statistics": "통계",
        "Export Report": "보고서 내보내기",
        "Help": "도움말",
        "Version": "버전",
        "Developer": "개발자",
        "License": "라이선스",
        "File": "파일",
        "New Project": "새 프로젝트",
        "Import Project": "프로젝트 가져오기",
        "Save Project": "프로젝트 저장",
        "Save Project As": "다른 이름으로 저장",
        "Exit": "종료",
        "View": "보기",
        "Show Main Toolbar": "메인 툴바 보이기",
        "Show Search Toolbar": "검색 툴바 보이기",
        "Edit": "편집",
        "Add Task": "작업 추가",
        "Edit Task": "작업 수정",
        "Delete Task": "작업 삭제",
        "Move Up": "위로 이동",
        "Move Down": "아래로 이동",
        "Tools": "도구",
        "Task Statistics": "작업 통계",
        "Export Report": "보고서 내보내기",
        "Settings": "설정",
        "Help": "도움말",
        "About": "정보"
    },
    "en": {
        "Language": "Language",
        "Korean": "Korean",
        "English": "English",
        "Settings": "Settings",
        "General": "General",
        "Appearance": "Appearance",
        "Data": "Data",
        "About": "About",
        "Auto Save": "Auto Save",
        "Check for Updates": "Check for Updates",
        "Data Directory": "Data Directory",
        "Browse": "Browse",
        "Backup": "Backup",
        "Restore": "Restore",
        "Reset": "Reset",
        "Dark Mode": "Dark Mode",
        "Window Opacity": "Window Opacity",
        "Always on Top": "Always on Top",
        "Search": "Search",
        "Search in Title": "Search in Title",
        "Search in Details": "Search in Details",
        "Include Completed": "Include Completed",
        "Statistics": "Statistics",
        "Export Report": "Export Report",
        "Help": "Help",
        "Version": "Version",
        "Developer": "Developer",
        "License": "License",
        "File": "File",
        "New Project": "New Project",
        "Import Project": "Import Project",
        "Save Project": "Save Project",
        "Save Project As": "Save Project As",
        "Exit": "Exit",
        "View": "View",
        "Show Main Toolbar": "Show Main Toolbar",
        "Show Search Toolbar": "Show Search Toolbar",
        "Edit": "Edit",
        "Add Task": "Add Task",
        "Edit Task": "Edit Task",
        "Delete Task": "Delete Task",
        "Move Up": "Move Up",
        "Move Down": "Move Down",
        "Tools": "Tools",
        "Task Statistics": "Task Statistics",
        "Export Report": "Export Report",
        "Settings": "Settings",
        "Help": "Help",
        "About": "About"
    }
}

def tr(key):
    """번역 함수"""
    from PyQt5.QtCore import QSettings
    lang = QSettings("anti_adhd_settings.ini", 1).value("general/language", "ko")
    return TRANSLATIONS.get(lang, {}).get(key, key)

# --- Qt 및 PyQt5 상수 대체값 정의 ---
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

        # --- 스크롤 영역 적용 ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        main_layout = QVBoxLayout(content)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        # 저해상도 친화적 스타일시트 적용
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #fff;
                color: #222;
                padding: 4px 10px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
                min-width: 60px;
                margin-right: 1px;
            }
            QTabBar::tab:selected {
                background: #e3f0ff;
                color: #1976d2;
            }
            QTabBar::tab:!selected {
                background: #f5f5f5;
                color: #888;
            }
            QTabWidget::pane {
                border-top: 1px solid #e3f0ff;
                background: #fafbfc;
                border-radius: 6px;
            }
        """)
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
        self.close_button.setStyleSheet(
            "QPushButton { font-size: 9pt; padding: 2px 10px; border-radius: 5px; background: #1565c0; color: white; font-weight: bold; } QPushButton:hover { background: #1976d2; }")
        self.close_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.close_button.clicked.connect(self.accept_settings)
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)
        button_layout.setContentsMargins(0, 8, 0, 0)

        scroll.setWidget(content)
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(scroll)

        # 화면 해상도에 맞게 크기 제한
        screen = QDesktopWidget().screenGeometry()
        max_w = int(screen.width() * 0.9)
        max_h = int(screen.height() * 0.9)
        self.setMaximumSize(max_w, max_h)
        self.resize(min(420, max_w), min(420, max_h))

        # (생성자 마지막에 테마 적용은 MainWindow에서 호출)

    def setup_general_tab(self):
        # 기존 layout = QVBoxLayout(self.general_tab) 제거
        outer_layout = QVBoxLayout(self.general_tab)
        # 각 QGroupBox마다 content QWidget을 생성하여 addWidget으로 추가
        # 언어 설정 그룹
        lang_group = QGroupBox(tr("Language"))
        lang_group.setStyleSheet(
            "QGroupBox { font-size: 9pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 6px; margin-top: 4px; background: #fafbfc; padding: 4px; }")
        lang_outer_layout = QVBoxLayout(lang_group)
        lang_content = QWidget()
        lang_content.setStyleSheet('background: #232323; color: #e0e0e0;')
        lang_layout = QHBoxLayout(lang_content)
        lang_layout.setSpacing(4)
        lang_layout.setContentsMargins(6, 4, 6, 6)
        self.lang_combo = QComboBox()
        self.lang_combo.setStyleSheet("font-size: 9pt;")
        self.lang_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.lang_combo.addItem(tr("Korean"), "ko")
        self.lang_combo.addItem(tr("English"), "en")
        current_lang = self.settings.value("general/language", "ko")
        index = self.lang_combo.findData(current_lang)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
        lang_layout.addWidget(QLabel(tr("Language") + ":"))
        lang_layout.addWidget(self.lang_combo)
        lang_content.setLayout(lang_layout)
        lang_outer_layout.addWidget(lang_content)
        outer_layout.addWidget(lang_group)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)

        # 데이터 경로 설정 그룹
        data_dir_group = QGroupBox(tr("Data Directory"))
        data_dir_group.setStyleSheet(
            "QGroupBox { font-size: 9pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 6px; margin-top: 4px; background: #fafbfc; padding: 4px; }")
        data_dir_group_layout = QVBoxLayout()
        data_dir_group_layout.setSpacing(4)
        data_dir_group_layout.setContentsMargins(6, 4, 6, 6)
        path_input_layout = QHBoxLayout()
        self.data_dir_label = QLabel(tr("Current Path") + ":")
        self.data_dir_label.setStyleSheet("font-size: 9pt; color: #666;")
        self.data_dir_edit = QLineEdit(self.current_data_dir)
        self.data_dir_edit.setReadOnly(True)
        self.data_dir_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.browse_button = QPushButton(tr("Change Folder") + "...")
        self.browse_button.setStyleSheet(
            "QPushButton { font-size: 9pt; padding: 2px 6px; border-radius: 4px; background: #e3f2fd; color: #1565c0; } QPushButton:hover { background: #bbdefb; }")
        self.browse_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.browse_button.clicked.connect(self.browse_data_directory)
        path_input_layout.addWidget(self.data_dir_label)
        path_input_layout.addWidget(self.data_dir_edit, 1)
        path_input_layout.addWidget(self.browse_button)
        data_dir_group_layout.addLayout(path_input_layout)
        path_notice_label = QLabel(tr("Restart the application after changing the path."))
        path_notice_label.setStyleSheet("font-size: 8pt; color: #aaa;")
        data_dir_group_layout.addWidget(path_notice_label, 0x0004)
        data_dir_group.setLayout(data_dir_group_layout)
        outer_layout.addWidget(data_dir_group)

        # 자동 저장 그룹 (QVBoxLayout, 체크박스만 단독)
        auto_save_group = QGroupBox(tr("자동 저장"))
        auto_save_group.setStyleSheet(
            "QGroupBox { font-size: 9pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 6px; margin-top: 2px; background: #fafbfc; padding: 2px; }"
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 6px; }"
        )
        auto_save_layout = QVBoxLayout()
        auto_save_layout.setContentsMargins(8, 28, 8, 6)  # top=28로 충분히 띄움
        auto_save_layout.setSpacing(8)
        self.auto_save_checkbox = QCheckBox(tr("사용"))
        self.auto_save_checkbox.setChecked(self.settings.value(
            "general/auto_save", True, type=bool))
        self.auto_save_checkbox.setStyleSheet("font-size: 9pt; padding: 0 2px;")
        self.auto_save_checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.auto_save_checkbox.stateChanged.connect(
            self._on_auto_save_changed)
        auto_save_layout.addWidget(self.auto_save_checkbox)
        auto_save_group.setLayout(auto_save_layout)
        outer_layout.addWidget(auto_save_group)

        # 업데이트 그룹 (QVBoxLayout, 체크박스만 단독)
        update_group = QGroupBox(tr("업데이트 확인"))
        update_group.setStyleSheet(
            "QGroupBox { font-size: 9pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 6px; margin-top: 2px; background: #fafbfc; padding: 2px; }"
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 6px; }"
        )
        update_layout = QVBoxLayout()
        update_layout.setContentsMargins(8, 28, 8, 6)  # top=28로 충분히 띄움
        update_layout.setSpacing(8)
        self.check_updates_checkbox = QCheckBox(tr("시작 시 확인"))
        self.check_updates_checkbox.setChecked(self.settings.value(
            "general/check_updates", True, type=bool))
        self.check_updates_checkbox.setStyleSheet("font-size: 9pt; padding: 0 2px;")
        self.check_updates_checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.check_updates_checkbox.stateChanged.connect(
            self._on_check_updates_changed)
        self.check_now_button = QPushButton(tr("지금 확인"))
        self.check_now_button.setStyleSheet(
            "QPushButton { font-size: 9pt; padding: 2px 6px; border-radius: 4px; background: #e3f2fd; color: #1565c0; } QPushButton:hover { background: #bbdefb; }")
        self.check_now_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.check_now_button.clicked.connect(self.perform_update_check)
        update_layout.addWidget(self.check_updates_checkbox)
        update_layout.addWidget(self.check_now_button)
        update_group.setLayout(update_layout)
        outer_layout.addWidget(update_group)

        # 데이터 관리 그룹 spacing 추가
        data_management_group = QGroupBox(tr("Data Management"))
        data_management_group.setStyleSheet(
            "QGroupBox { font-size: 9pt; font-weight: 600; border: 1px solid #e0e0e0; border-radius: 6px; margin-top: 4px; background: #fafbfc; padding: 4px; }"
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 6px; }"
        )
        data_management_layout = QHBoxLayout()
        data_management_layout.setSpacing(8)
        data_management_layout.setContentsMargins(6, 6, 6, 6)
        self.backup_data_button = QPushButton(tr("Backup Data") + "...")
        self.restore_data_button = QPushButton(tr("Restore Data") + "...")
        self.reset_data_button = QPushButton(tr("Reset Data") + "...")
        for btn in [self.backup_data_button, self.restore_data_button, self.reset_data_button]:
            btn.setStyleSheet(
                "QPushButton { font-size: 9pt; padding: 2px 6px; border-radius: 4px; background: #fff3e0; color: #e65100; font-weight: bold; } QPushButton:hover { background: #ffe0b2; }")
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.backup_data_button.clicked.connect(self.backup_data)
        self.restore_data_button.clicked.connect(self.restore_data)
        self.reset_data_button.clicked.connect(self.reset_data)
        data_management_layout.addWidget(self.backup_data_button)
        data_management_layout.addSpacing(8)
        data_management_layout.addWidget(self.restore_data_button)
        data_management_layout.addSpacing(8)
        data_management_layout.addWidget(self.reset_data_button)
        data_management_layout.addStretch()
        data_management_group.setLayout(data_management_layout)
        outer_layout.addWidget(data_management_group)
        outer_layout.addStretch()

        self.general_tab.setLayout(outer_layout)

    def _on_language_changed(self, index):
        """언어가 변경되었을 때 호출되는 함수"""
        lang = self.lang_combo.itemData(index)
        self.settings.setValue("general/language", lang)
        # UI 업데이트를 위해 부모 윈도우에 알림
        if self.parent():
            self.parent().reload_data_and_ui()

    def setup_info_tab(self):
        outer_layout = QVBoxLayout(self.info_tab)
        # 프로그램 정보 QGroupBox
        info_group_box = QGroupBox("프로그램 정보")
        info_outer_layout = QVBoxLayout(info_group_box)
        info_content = QWidget()
        info_content.setStyleSheet('background: #232323; color: #e0e0e0;')
        form_layout = QFormLayout(info_content)
        form_layout.setSpacing(8)
        form_layout.setContentsMargins(10, 26, 10, 10)
        app_name_label = QLabel("Anti-ADHD")
        font = app_name_label.font()
        font.setPointSize(13)
        font.setBold(True)
        app_name_label.setFont(font)
        app_name_label.setStyleSheet("color: #1565c0;")
        form_layout.addRow(QLabel("이름:"), app_name_label)
        form_layout.addRow(QLabel("버전:"), QLabel("1.0.1"))
        form_layout.addRow(QLabel("개발자:"), QLabel("octaxii"))
        github_link = QLabel(
            "<a href=\"https://github.com/octaxii/Anti-ADHD\">GitHub 저장소</a>")
        github_link.setOpenExternalLinks(True)
        form_layout.addRow(QLabel("GitHub:"), github_link)
        info_content.setLayout(form_layout)
        info_outer_layout.addWidget(info_content)
        outer_layout.addWidget(info_group_box)
        # 라이선스 QGroupBox
        license_group_box = QGroupBox("라이선스")
        license_outer_layout = QVBoxLayout(license_group_box)
        license_content = QWidget()
        license_content.setStyleSheet('background: #232323; color: #e0e0e0;')
        license_layout = QVBoxLayout(license_content)
        license_layout.setContentsMargins(10, 26, 10, 10)
        license_layout.setSpacing(8)
        license_text_edit = QTextEdit()
        license_text_edit.setReadOnly(True)
        license_text_edit.setStyleSheet(
            "font-size: 8.5pt; background: #232323; color: #fff; border-radius: 6px; padding: 6px;")
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
        license_text_edit.setText(mit_license_text.strip())
        license_layout.addSpacing(8)
        license_layout.addWidget(license_text_edit)
        license_layout.addSpacing(8)
        license_content.setLayout(license_layout)
        license_outer_layout.addWidget(license_content)
        outer_layout.addWidget(license_group_box)
        outer_layout.addStretch()
        self.info_tab.setLayout(outer_layout)

    def browse_data_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "데이터 저장 폴더 선택", self.new_data_dir)
        if directory and directory != self.current_data_dir:
            self.new_data_dir = directory
            self.data_dir_edit.setText(self.new_data_dir)
            # 경로 변경 시 즉시 알림은 여기서 하지 않고, "닫기" 누를 때 accept_settings에서 처리

    def _on_auto_save_changed(self, state):
        self.settings.setValue("general/auto_save",
                               self.auto_save_checkbox.isChecked())
        self.settings.sync()
        if self.main_window_ref:  # MainWindow에 즉시 반영 (선택적)
            self.main_window_ref.auto_save_enabled = self.auto_save_checkbox.isChecked()

    def _on_check_updates_changed(self, state):
        self.settings.setValue("general/check_updates",
                               self.check_updates_checkbox.isChecked())
        self.settings.sync()

    def accept_settings(self):
        # 데이터 경로 변경 사항이 있다면 저장하고 알림
        if self.new_data_dir != self.current_data_dir:
            self.settings.setValue("dataDir", self.new_data_dir)
            self.current_data_dir = self.new_data_dir  # 현재 대화상자 내의 current_data_dir도 업데이트
            if self.main_window_ref:  # MainWindow의 data_dir은 재시작 후 반영됨을 명심
                pass  # MainWindow의 data_dir을 직접 바꾸는 것은 재시작 전에는 의미가 적을 수 있음
            QMessageBox.information(self, "설정 변경",
                                    f"데이터 저장 경로가 다음으로 설정되었습니다:\\n'{self.new_data_dir}'\\n\\n애플리케이션을 재시작해야 변경 사항이 완전히 적용됩니다.")
        
        # 체크박스 값들은 이미 stateChanged 시그널에서 즉시 저장되었음
        # self.settings.sync() # 각 시그널 핸들러에서 이미 호출됨
        self.accept()  # QDialog.Accepted 상태로 다이얼로그 닫기

    def perform_update_check(self):
        QMessageBox.information(self, "업데이트 확인", "업데이트 확인 기능은 아직 구현되지 않았습니다.")

    def backup_data(self):
        # 현재 활성화된 데이터 디렉토리 사용 (MainWindow의 data_dir)
        # SettingsDialog 생성 시 current_data_dir로 전달받음
        source_dir = self.current_data_dir 
        if not os.path.isdir(source_dir):
            QMessageBox.warning(
                self, "백업 오류", f"데이터 디렉토리를 찾을 수 없습니다: {source_dir}")
            return

        # 백업 파일명 제안 (예: anti_adhd_backup_YYYYMMDD_HHMMSS.zip)
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        suggested_filename = f"anti_adhd_backup_{timestamp}.zip"

        file_path, _ = QFileDialog.getSaveFileName(
            self, "데이터 백업 파일 저장", suggested_filename, "ZIP 파일 (*.zip)")

        if not file_path:
            return  # 사용자가 취소

        try:
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for foldername, subfolders, filenames in os.walk(source_dir):
                    for filename in filenames:
                        if filename.startswith("project_") and filename.endswith(".json"):
                            abs_path = os.path.join(foldername, filename)
                            # zip 파일 내에서는 source_dir 다음 경로만 유지 (상대 경로)
                            rel_path = os.path.relpath(abs_path, source_dir)
                            zf.write(abs_path, rel_path)
            QMessageBox.information(
                self, "백업 성공", f"데이터가 다음 파일로 성공적으로 백업되었습니다:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "백업 실패", f"데이터 백업 중 오류가 발생했습니다:\n{e}")

    def restore_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "데이터 백업 파일 선택", "", "ZIP 파일 (*.zip)")
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
                QMessageBox.critical(
                    self, "복원 오류", f"데이터 디렉토리 생성 실패: {target_dir}\n{e}")
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
                    QMessageBox.warning(
                        self, "복원 준비 오류", f"기존 프로젝트 파일 '{item}' 삭제 실패: {e}")
                    # 실패해도 계속 진행할지, 중단할지 결정 필요. 여기서는 계속 진행.
        if cleaned_count > 0:
            print(f"{cleaned_count}개의 기존 프로젝트 파일을 삭제했습니다.")

        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                # zip 파일 내의 모든 project_*.json 파일만 압축 해제
                project_files_in_zip = [name for name in zf.namelist(
                ) if name.startswith("project_") and name.endswith(".json")]
                if not project_files_in_zip:
                    QMessageBox.warning(
                        self, "복원 오류", "선택한 ZIP 파일에 유효한 프로젝트 데이터(project_*.json)가 없습니다.")
                    return

                zf.extractall(target_dir, members=project_files_in_zip)
            
            QMessageBox.information(
                self, "복원 성공", "데이터가 성공적으로 복원되었습니다. 애플리케이션 데이터를 새로고침합니다.")
            
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
            QMessageBox.information(
                self, "데이터 초기화", "데이터 디렉토리가 이미 존재하지 않습니다. 초기화할 데이터가 없습니다.")
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
            QMessageBox.warning(
                self, "초기화 중 오류", f"일부 프로젝트 파일 삭제 중 오류가 발생했습니다:\n{error_message}")
        else:
            QMessageBox.information(
                self, "데이터 초기화 성공", f"{deleted_count}개의 프로젝트 파일이 성공적으로 삭제되었습니다. 애플리케이션 데이터를 새로고침합니다.")

        if self.main_window_ref and hasattr(self.main_window_ref, 'reload_data_and_ui'):
            self.main_window_ref.reload_data_and_ui()

    def apply_theme(self, dark_mode):
        from PyQt5.QtGui import QPalette, QColor
        if dark_mode:
            self.setStyleSheet("""
                QDialog, QWidget {
                    background: #232323;
                    color: #e0e0e0;
                }
                QFrame {
                    background: #232323;
                    border: 1px solid #404040;
                }
                QScrollArea, QScrollArea > QWidget {
                    background: #232323;
                    border: none;
                }
                QGroupBox {
                    background: #232323;
                    border: 1.5px solid #404040;
                    border-radius: 8px;
                    margin-top: 8px;
                    color: #e0e0e0;
                }
                QGroupBox > QWidget, QGroupBox > QFrame {
                    background: #232323;
                }
                QGroupBox:title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    background: #232323;
                    color: #90caf9;
                    padding: 0 6px;
                }
                QTabWidget::pane {
                    background: #232323;
                    border: 1px solid #404040;
                }
                QTabBar::tab {
                    background: #232323;
                    color: #e0e0e0;
                }
                QTabBar::tab:selected {
                    background: #0d47a1;
                    color: #fff;
                }
                QTabBar::tab:!selected {
                    background: #404040;
                    color: #aaa;
                }
                QLineEdit, QTextEdit, QComboBox {
                    background: #2d2d2d;
                    color: #fff;
                    border: 1.5px solid #404040;
                }
                QComboBox QAbstractItemView {
                    background: #232323;
                    color: #fff;
                    selection-background-color: #0d47a1;
                    selection-color: #fff;
                }
                QCheckBox, QRadioButton {
                    color: #e0e0e0;
                }
                QCheckBox::indicator, QRadioButton::indicator {
                    background: #232323;
                    border: 1.5px solid #404040;
                }
                QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                    background: #0d47a1;
                    border: 1.5px solid #1976d2;
                }
                QScrollBar:vertical, QScrollBar:horizontal {
                    background: #232323;
                    border: none;
                    width: 12px;
                }
                QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                    background: #444;
                    border-radius: 6px;
                }
                QScrollBar::add-line, QScrollBar::sub-line {
                    background: none;
                    border: none;
                }
                QPushButton {
                    background: #0d47a1;
                    color: #fff;
                    border: none;
                }
                QPushButton:hover {
                    background: #1976d2;
                }
                QPushButton:disabled {
                    background: #404040;
                    color: #888;
                }
                QLabel {
                    color: #e0e0e0;
                }
            """)
            # 탭 content QWidget, QTabWidget, QDialog 등에도 직접 스타일 적용
            if hasattr(self, 'general_tab'):
                self.general_tab.setStyleSheet('background: #232323; color: #e0e0e0;')
            if hasattr(self, 'info_tab'):
                self.info_tab.setStyleSheet('background: #232323; color: #e0e0e0;')
            if hasattr(self, 'tab_widget'):
                self.tab_widget.setStyleSheet('background: #232323; color: #e0e0e0;')
            self.setStyleSheet(self.styleSheet() + '\nQDialog { background: #232323; color: #e0e0e0; }')
        else:
            self.setStyleSheet("")

    def open_settings_dialog(self):
        dialog = SettingsDialog(current_data_dir=self.data_dir, 
                                settings_file_path=self.settings_file,
                                parent=self)
        # 다크모드 상태 전달 및 적용
        if hasattr(self, 'dark_mode'):
            dialog.apply_theme(self.dark_mode)
        if dialog.exec_() == QDialog.Accepted:
            pass


class ProjectListWidget(QListWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px 4px;
                border-radius: 4px;
                color: #333333;
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.viewport().setContextMenuPolicy(Qt.CustomContextMenu)
        self.viewport().customContextMenuRequested.connect(
            self.main_window.show_project_context_menu)
        
    def showEvent(self, event):
        super().showEvent(event)
        # 현재 선택된 프로젝트 강조
        current_item = self.currentItem()
        if current_item:
            self.setCurrentItem(current_item)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            pos = event.pos()
            self.main_window.show_project_context_menu(pos)
            event.accept()
        else:
            super().mousePressEvent(event)
        # 클릭한 항목이 있는 경우에만 선택 상태 업데이트
        item = self.itemAt(event.pos())
        if item:
            self.setCurrentItem(item)
            # 메인 윈도우의 프로젝트 선택 이벤트 발생
            self.main_window.on_project_selection_changed(
                item, self.currentItem())
            
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        # 키보드로 선택 변경 시에도 상태 업데이트
        if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Home, Qt.Key_End):
            current_item = self.currentItem()
            if current_item:
                self.main_window.on_project_selection_changed(
                    current_item, None)


class EisenhowerQuadrantWidget(QFrame):
    class EisenhowerTaskListWidget(QListWidget):
        def __init__(self, parent_quadrant):
            super().__init__()
            self.parent_quadrant = parent_quadrant
            self.setDragEnabled(True)
            self.setAcceptDrops(True)
            self.setDropIndicatorShown(True)
            self.setDefaultDropAction(Qt.MoveAction)
            self.setSelectionMode(QAbstractItemView.SingleSelection)

        def mimeTypes(self):
            return ['application/x-antiadhd-task']

        def mimeData(self, items):
            # 하나의 아이템만 지원
            item = items[0]
            idx = self.row(item)
            item_data = self.parent_quadrant.items[idx]
            mime = super().mimeData(items)
            mime.setData('application/x-antiadhd-task',
                         json.dumps(item_data).encode('utf-8'))
            return mime

        def dropMimeData(self, index, data, action):
            if data.hasFormat('application/x-antiadhd-task'):
                try:
                    item_data = json.loads(
                        bytes(data.data('application/x-antiadhd-task')).decode('utf-8'))
                except Exception as e:
                    print(f"[DEBUG] 드롭 데이터 역직렬화 오류: {e}")
                    return False
                # 원본 Quadrant에서 삭제
                for quad in self.parent_quadrant.main_window.quadrant_widgets:
                    if item_data in quad.items:
                        idx = quad.items.index(item_data)
                        quad.items.pop(idx)
                        quad._reorder_items()
                        quad._save_current_state()
                        break
                # 대상 Quadrant에 추가
                self.parent_quadrant.items.append(item_data)
                self.parent_quadrant._reorder_items()
                self.parent_quadrant._save_current_state()
                # 상태바 알림
                if self.parent_quadrant.main_window:
                    self.parent_quadrant.main_window.statusBar().showMessage(
                        f"'{item_data['title']}'이(가) 사분면 간 이동됨", 2000)
                return True
            return super().dropMimeData(index, data, action)

        def supportedDropActions(self):
            return Qt.MoveAction

    def __init__(self, color, keyword, description, icon=None, main_window_ref=None):
        super().__init__()
        self.color = color
        self.keyword = keyword
        self.description = description
        self.icon = icon
        self.main_window = main_window_ref
        self.items = []
        self._test_mode = False  # 테스트 자동 입력 모드
        
        # 색상 계산
        from PyQt5.QtGui import QColor
        base = QColor(color)
        light = base.lighter(170).name()
        dark = base.darker(130).name()
        border = base.darker(120).name()
        
        self._init_widgets()
        self._setup_styles(color, light, dark, border)
        self._setup_layout()
        self._connect_signals()
        self._setup_animations()
        
    def _update_list_item(self, item: QListWidgetItem, idx: int) -> None:
        """리스트 아이템 업데이트 (참조 오류 방지)"""
        is_checked = item.checkState() == Qt.CheckState.Checked
        self.items[idx]["checked"] = is_checked
        title = self.items[idx]["title"]
        self.items[idx]["title"] = title
        # UI 업데이트
        item.setText(self.render_task_title_with_emoji(self.items[idx]))
        if is_checked:
            item.setForeground(QColor("#666666"))
            item.setFont(QFont("Helvetica", 9, QFont.Weight.Normal))
        else:
            item.setForeground(QColor("#000000"))
            item.setFont(QFont("Helvetica", 9, QFont.Weight.Normal))
        if self.items[idx]["details"]:
            item.setToolTip(
                f"{self.items[idx]['title']}\n\n{self.items[idx]['details']}")
        else:
            item.setToolTip(self.items[idx]["title"])
        # self._reorder_items() 호출 제거 (참조 오류 방지)
        self._save_current_state()
        
    def _save_current_state(self):
        """현재 상태를 즉시 저장"""
        if not self.main_window or not self.main_window.current_project_name:
            return
            
        # 현재 사분면의 인덱스 찾기
        quadrant_idx = -1
        for i, quad in enumerate(self.main_window.quadrant_widgets):
            if quad == self:
                quadrant_idx = i
                break
                
        if quadrant_idx >= 0:
            # 프로젝트 데이터 업데이트
            project_data = self.main_window.projects_data[self.main_window.current_project_name]
            if "tasks" in project_data and len(project_data["tasks"]) > quadrant_idx:
                project_data["tasks"][quadrant_idx] = self.items
                # 즉시 파일에 저장
                self.main_window.save_project_to_file(
                    self.main_window.current_project_name)
                
    def _add_list_item(self, item_data: dict, idx: Optional[int] = None) -> None:
        """항목을 리스트에 추가합니다."""
        try:
            # 항목 데이터 검증
            if not isinstance(item_data, dict):
                raise ValueError("item_data must be a dictionary")

            # 필수 키 검증
            required_keys = ['title', 'completed', 'priority',
                'due_date', 'details', 'created_at', 'updated_at']
            if not all(key in item_data for key in required_keys):
                raise ValueError(
                    f"item_data must contain all required keys: {required_keys}")

            # 항목 생성 및 설정
            item = QListWidgetItem()
            
            # 데이터 설정
            item.setData(Qt.UserRole, item_data)

            # 폰트 설정
            font = QFont()
            font.setPointSize(10)
            item.setFont(font)

            # 체크박스 설정
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(
                Qt.Checked if item_data['completed'] else Qt.Unchecked)

            # 텍스트 설정
            item.setText(self.render_task_title_with_emoji(item_data))

            # 체크 상태에 따라 스타일 적용
            if item_data['completed']:
                item.setForeground(QColor("#666666"))
                font = QFont("Helvetica", 9, QFont.Weight.Normal)
                font.setStrikeOut(True)
                item.setFont(font)
            else:
                item.setForeground(QColor("#000000"))
                font = QFont("Helvetica", 9, QFont.Weight.Normal)
                font.setStrikeOut(False)
                item.setFont(font)

            # 툴팁 설정
            if item_data['details']:
                item.setToolTip(f"{item_data['title']}\n\n{item_data['details']}")
            else:
                item.setToolTip(item_data['title'])

            # 항목 추가
            if idx is not None:
                self.list_widget.insertItem(idx, item)
            else:
                self.list_widget.addItem(item)
            
            # 항목 데이터 저장 (UI만 업데이트하는 경우가 아닐 때만)
            if not hasattr(self, '_skip_items_append'):
                self.items.append(item_data)

            # 항목 변경 시그널 연결
            item.setData(Qt.UserRole + 1, True)  # 변경 플래그 설정

            # 항목 선택
            self.list_widget.setCurrentItem(item)

            # 항목 추가 애니메이션
            self._animate_add(item)

        except Exception as e:
            print(f"Error in _add_list_item: {str(e)}")
            # 에러 발생 시 메모리 정리
            if 'item' in locals():
                del item
            raise
            
    def _reorder_items(self):
        """체크된 항목을 하단으로 이동"""
        # 체크되지 않은 항목과 체크된 항목 분리
        unchecked_items = []
        checked_items = []
        
        for i, item_data in enumerate(self.items):
            if item_data["checked"]:
                checked_items.append((i, item_data))
            else:
                unchecked_items.append((i, item_data))
                
        # 새로운 순서로 items 배열 재구성
        new_items = []
        for _, item_data in unchecked_items:
            new_items.append(item_data)
        for _, item_data in checked_items:
            new_items.append(item_data)
            
        # items 배열 업데이트
        self.items = new_items
        
        # 리스트 위젯 업데이트
        self.list_widget.clear()
        for item_data in self.items:
            self._add_list_item(item_data)
            
        # 즉시 저장
        self._save_current_state()

    def _init_widgets(self):
        """위젯 초기화 (Drag&Drop 지원 커스텀 리스트 사용)"""
        self.list_widget = EisenhowerQuadrantWidget.EisenhowerTaskListWidget(
            self)
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
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {pastel_light}, stop:1 white);
                border-radius: 14px;
                border: 2px solid {pastel_border_c};
            }}
            QLabel {{
                color: {pastel_dark_c};
                font-family: 'Segoe UI', 'Noto Sans KR', 'Pretendard', Arial, sans-serif;
                font-size: 11px;
                font-weight: bold;
                background: transparent;
                border: none;
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
                background: transparent;
            }}
            QListWidget::item:selected, QListWidget::item:focus {{
                background: {pastel_border_c};
                color: #fff;
                outline: 2px solid #1976d2;
            }}
            QListWidget::item:hover {{
                background: #f3f6fa;
            }}
            QListWidget::item:checked {{
                color: #666666;
                text-decoration: line-through;
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
        title_label.setStyleSheet(
            f"font-size: 10.5pt; font-weight: bold; color: {self.color}; margin-bottom: 0px;")
        if self.icon:
            icon_label = QLabel()
            icon_label.setPixmap(self.icon.pixmap(15, 15))
            title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.setSpacing(4)
        title_layout.setContentsMargins(2, 2, 2, 0)
        desc_label = QLabel(self.description)
        desc_label.setStyleSheet(
            "font-size: 8.5pt; color: #666; margin-bottom: 2px;")
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
        self.add_button.clicked.connect(self.add_task)
        self.input_field.returnPressed.connect(self.add_task)  # 엔터키로 추가
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.list_widget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(
            self.show_context_menu)
        # 체크박스 상태 변경 이벤트 연결
        self.list_widget.itemChanged.connect(self._on_item_changed)
        
    def _on_item_changed(self, item: QListWidgetItem):
        """아이템 체크 상태 변경 처리 (참조 오류 완전 차단)"""
        if not item:
            return
        idx = self.list_widget.row(item)
        if idx < 0 or idx >= len(self.items):
            return
        # 체크 상태만 데이터에 반영
        is_checked = item.checkState() == Qt.CheckState.Checked
        self.items[idx]["checked"] = is_checked
        # UI는 전체 재생성 (item 직접 접근 금지)
        self._reorder_items()
        # 즉시 저장
        self._save_current_state()
        
    def _reorder_items_without_recursion(self):
        """체크된 항목을 하단으로 이동 (재귀 없이)"""
        # 체크되지 않은 항목과 체크된 항목 분리
        unchecked_items = []
        checked_items = []
        
        for item_data in self.items:
            if item_data["checked"]:
                checked_items.append(item_data)
            else:
                unchecked_items.append(item_data)
                
        # 새로운 순서로 items 배열 재구성
        self.items = unchecked_items + checked_items
        
        # 리스트 위젯 업데이트
        self.list_widget.blockSignals(True)  # 시그널 차단
        self.list_widget.clear()
        
        for item_data in self.items:
            title = item_data["title"]
            item = QListWidgetItem(title)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if item_data["checked"] else Qt.CheckState.Unchecked)
            
            # 체크 상태에 따라 스타일 적용
            if item_data["checked"]:
                item.setForeground(QColor("#666666"))
                item.setFont(QFont("Segoe UI", 9, QFont.Weight.Normal))
            else:
                item.setForeground(QColor("#000000"))
                item.setFont(QFont("Segoe UI", 9, QFont.Weight.Normal))
                
            # 상세 내용이 있으면 툴팁으로 표시
            if item_data["details"]:
                item.setToolTip(f"{title}\n\n{item_data['details']}")
            else:
                item.setToolTip(title)
                
            self.list_widget.addItem(item)
            
        self.list_widget.blockSignals(False)  # 시그널 차단 해제
        
    def _add_list_item(self, item_data: dict, idx: Optional[int] = None) -> None:
        """리스트에 새 항목 추가"""
        title = item_data["title"]
        if item_data["checked"]:
            title = f"✓ {title}"
            
        item = QListWidgetItem(title)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked if item_data["checked"] else Qt.CheckState.Unchecked)
        
        if idx is not None:
            self.list_widget.insertItem(idx, item)
        else:
            self.list_widget.addItem(item)
            
        # 체크 상태에 따라 스타일 적용
        if item_data["checked"]:
            item.setForeground(QColor("#666666"))
            item.setFont(QFont("Segoe UI", 9, QFont.Weight.Normal))
        else:
            item.setForeground(QColor("#000000"))
            item.setFont(QFont("Segoe UI", 9, QFont.Weight.Normal))
            
        # 상세 내용이 있으면 툴팁으로 표시
        if item_data["details"]:
            item.setToolTip(f"{title}\n\n{item_data['details']}")
        else:
            item.setToolTip(title)
            
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
        """새 작업 추가"""
        try:
            # 입력 필드에서 타이틀 가져오기
            title = self.input_field.text().strip()
            if not title:  # 타이틀이 비어있으면 추가하지 않음
                return
                
            # 새 작업 데이터 생성
            new_item = {
                'title': title,
                'details': '',
                'checked': False,
                'completed': False,  # checked와 동기화
                'priority': 0,  # 우선순위 추가
                'due_date': None,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # 데이터 리스트에 추가
            self.items.append(new_item)
            
            # UI 업데이트 전에 시그널 차단
            self.list_widget.blockSignals(True)
            try:
                # UI에 아이템 추가
                self._add_list_item(new_item)
                # 새로 추가된 아이템 선택
                last_item = self.list_widget.item(self.list_widget.count() - 1)
                if last_item:
                    self.list_widget.setCurrentItem(last_item)
            finally:
                # 시그널 차단 해제
                self.list_widget.blockSignals(False)
            
            # 상태 저장
            self._save_current_state()
            
        except Exception as e:
            print(f"Error in add_task: {str(e)}")
            # 에러 발생 시 UI 상태 복구
            self.list_widget.blockSignals(False)
            # 마지막으로 추가된 아이템이 있다면 제거
            if self.items and len(self.items) > 0:
                self.items.pop()
            self.load_tasks(self.items)  # 현재 데이터로 UI 재구성

    def on_item_double_clicked(self, item) -> None:
        idx = self.list_widget.row(item)
        if idx < 0 or idx >= len(self.items):
            return
        self.edit_task_dialog(idx, item)

    def show_context_menu(self, position) -> None:
        """컨텍스트 메뉴 표시"""
        item = self.list_widget.itemAt(position)
        if not item:
            return
        menu = QMenu()
        move_menu = menu.addMenu("중요도/긴급도 변경")
        quadrant_meanings = {
            0: "중요/긴급",
            1: "중요",
            2: "긴급",
            3: "중요X/긴급X"
        }
        for i, quad in enumerate(self.main_window.quadrant_widgets):
            if quad != self:  # 현재 사분면 제외
                action = move_menu.addAction(quadrant_meanings[i])
                # item_data만 넘기도록 수정
                action.triggered.connect(lambda checked, target_quad=quad, item_data=self.items[self.list_widget.row(
                    item)].copy(): self._move_item_data_to_quadrant(item_data, target_quad))
        edit_action = menu.addAction("수정")
        delete_action = menu.addAction("삭제")
        action = menu.exec(self.list_widget.mapToGlobal(position))
        if action == edit_action:
            self.edit_task_dialog(self.list_widget.row(item), item)
        elif action == delete_action:
            self.list_widget.takeItem(self.list_widget.row(item))
            self.items.pop(self.list_widget.row(item))
            self._save_current_state()
            
    def _move_item_data_to_quadrant(self, item_data: dict, target_quadrant) -> None:
        """아이템 데이터를 다른 사분면으로 이동 (QListWidgetItem 참조 없이)"""
        if not item_data or not target_quadrant:
            return
        idx = None
        for i, d in enumerate(self.items):
            if d is item_data or d == item_data:
                idx = i
                break
        if idx is not None:
            self.list_widget.takeItem(idx)
        self.items.pop(idx)
            # 대상 사분면에 아이템 추가 (중복 append 방지)
        target_quadrant.items.append(item_data)
        target_quadrant._add_list_item(item_data)
        quadrant_meanings = {
            0: "중요/긴급",
            1: "중요",
            2: "긴급",
            3: "중요X/긴급X"
        }
        target_idx = self.main_window.quadrant_widgets.index(
                target_quadrant)
        if self.main_window:
            self.main_window.statusBar().showMessage(
                f"'{item_data['title']}'을(를) {quadrant_meanings[target_idx]}로 이동했습니다.",
                2000
            )
        self._save_current_state()
        target_quadrant._save_current_state()

    def edit_task_dialog(self, idx, item, item_data=None):
        if getattr(self, '_test_mode', False):
            return True
        from PyQt5.QtWidgets import QDateTimeEdit, QCheckBox, QGridLayout
        from PyQt5.QtCore import QDateTime, QLocale
        dialog = QDialog(self)
        dialog.setWindowTitle("항목 수정")
        layout = QVBoxLayout(dialog)
        data = item_data if item_data is not None else (
            self.items[idx] if idx is not None and idx < len(self.items) else None)
        if data is None:
            return False
        title_edit = QLineEdit(data["title"])
        details_edit = QTextEdit(data["details"])
        layout.addWidget(QLabel("제목:"))
        layout.addWidget(title_edit)
        layout.addWidget(QLabel("세부 내용:"))
        layout.addWidget(details_edit)
        due_label = QLabel("마감일:")
        due_edit = QDateTimeEdit()
        due_edit.setCalendarPopup(True)
        due_edit.setDisplayFormat("yyyy년 MM월 dd일 HH:mm")
        due_edit.setLocale(QLocale(QLocale.Korean, QLocale.SouthKorea))
        due_edit.setStyleSheet("""
            QDateTimeEdit, QCalendarWidget, QToolButton {
                background: #fff;
                color: #222;
                border: 1.5px solid #b0b0b0;
                border-radius: 6px;
                selection-background-color: #e3f0ff;
                selection-color: #1976d2;
            }
            QCalendarWidget QAbstractItemView {
                background: #fff;
                color: #222;
                selection-background-color: #e3f0ff;
                selection-color: #1976d2;
            }
        """)
        calendar = due_edit.calendarWidget()
        if calendar:
            calendar.setMinimumHeight(260)
            calendar.setMaximumHeight(260)
            calendar.setMinimumWidth(320)
            calendar.setMaximumWidth(320)
            calendar.setLocale(QLocale(QLocale.Korean, QLocale.SouthKorea))
            calendar.setStyleSheet(
                """
QCalendarWidget QWidget {
    background: #fff;
    border-radius: 0;
}
QCalendarWidget QToolButton {
                background: transparent;
    color: #222;
    font-family: 'SF Pro', 'Helvetica Neue', 'Apple SD Gothic Neo', Arial, sans-serif;
    font-weight: 500;
    font-size: 18px;
                border: none;
    margin: 0 2px;
    padding: 2px 8px 2px 8px;
}
QCalendarWidget QToolButton#qt_calendar_prevmonth,
QCalendarWidget QToolButton#qt_calendar_nextmonth {
    background: #f2f2f7;
    color: #222;
    border-radius: 50%;
    min-width: 28px; min-height: 28px;
    font-size: 20px;
                border: none;
}
QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
    background: #e5e5ea;
}
QCalendarWidget QMenu { background: #fff; color: #222; border-radius: 8px; }
QCalendarWidget QSpinBox { font-size: 18px; border: none; }
QCalendarWidget QAbstractItemView:enabled {
    font-size: 16px;
    color: #222;
                background: #fff;
    selection-background-color: #e5e5ea;
    selection-color: #222;
    outline: none;
}
QCalendarWidget QAbstractItemView::item {
    border-radius: 0;
    margin: 0;
    padding: 8px 0;
    min-width: 32px;
    min-height: 32px;
}
QCalendarWidget QAbstractItemView::item:selected {
    background: #e5e5ea;
                color: #222;
}
QCalendarWidget QAbstractItemView::item:today {
    background: transparent;
    color: #007aff;
    border: 2px solid #007aff;
    border-radius: 16px;
}
QCalendarWidget QAbstractItemView::item:enabled:weekend {
    color: #ff3b30;
}
QCalendarWidget QAbstractItemView::item:enabled:weekday {
    color: #222;
}
QCalendarWidget QHeaderView {
    background: transparent;
    color: #222;
    font-weight: 500;
    border: none;
    font-size: 14px;
}
                """
            )
        due_none_cb = QCheckBox("마감일 없음")
        if data.get("due_date"):
            due_edit.setDateTime(QDateTime.fromString(
                data["due_date"], "yyyy-MM-dd HH:mm"))
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
            if minutes in data.get("reminders", []):
                cb.setChecked(True)
            reminder_checks.append((cb, minutes))
            reminder_grid.addWidget(cb, i // 3, i % 3)
        layout.addWidget(reminder_label)
        layout.addLayout(reminder_grid)
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("확인")
        cancel_btn = QPushButton("취소")
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        def save_and_accept():
            title_edit.clearFocus()
            details_edit.clearFocus()
            new_title = title_edit.text().strip()
            new_details = details_edit.toPlainText().strip()
            if due_none_cb.isChecked():
                due_dt = None
            else:
                due_dt = due_edit.dateTime().toString("yyyy-MM-dd HH:mm")
            reminders = [minutes for cb, minutes in reminder_checks if cb.isChecked()]
            if new_title:
                data["title"] = new_title
                data["details"] = new_details
                data["due_date"] = due_dt
                data["reminders"] = reminders
                if "due_date" not in data:
                    data["due_date"] = None
                if "reminders" not in data:
                    data["reminders"] = []
                if "checked" in data:
                    data["completed"] = data["checked"]
                elif "completed" in data:
                    data["checked"] = data["completed"]
                self._reorder_items()
            dialog.accept()
        try:
            ok_btn.clicked.disconnect()
        except Exception:
            pass
        ok_btn.clicked.connect(save_and_accept)
        cancel_btn.clicked.connect(dialog.reject)
        dialog.exec_()

    def clear_tasks(self):
        self.items = []
        self.list_widget.clear()

    def load_tasks(self, tasks_list):
        """태스크 목록 로드"""
        self.items = list(tasks_list)  # 복사본 사용
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        
        # UI만 업데이트하는 경우임을 표시
        self._skip_items_append = True
        try:
            for item_data in self.items:
                self._add_list_item(item_data)
        finally:
            # 플래그 제거
            delattr(self, '_skip_items_append')
            
        self.list_widget.blockSignals(False)

    def _add_list_item(self, item_data: dict, idx: Optional[int] = None) -> None:
        """리스트에 새 항목 추가 (UI만, self.items에는 append하지 않음)"""
        title = self.render_task_title_with_emoji(item_data)
        item = QListWidgetItem(title)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
                Qt.CheckState.Checked if item_data["checked"] else Qt.CheckState.Unchecked)
        if idx is not None:
            self.list_widget.insertItem(idx, item)
        else:
            self.list_widget.addItem(item)
        # 체크 상태에 따라 스타일 적용
        if item_data["checked"]:
            item.setForeground(QColor("#666666"))
            font = QFont("Helvetica", 9, QFont.Weight.Normal)
            font.setStrikeOut(True)
            item.setFont(font)
        else:
            item.setForeground(QColor("#000000"))
            font = QFont("Helvetica", 9, QFont.Weight.Normal)
            font.setStrikeOut(False)
            item.setFont(font)
        if item_data["details"]:
                item.setToolTip(f"{item_data['title']}\n\n{item_data['details']}")
        else:
                item.setToolTip(item_data["title"])

    def render_task_title_with_emoji(self, item_data):
        title = item_data.get("title", "")
        details = item_data.get("details", "")
        due_date = item_data.get("due_date")
        parts = []
        # 세부내용 있으면 메모지 이모지
        if details:
            parts.append("📝")
        # 마감일 있으면 D-xx
        if due_date:
            try:
                try:
                    due_dt = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
                except ValueError:
                    due_dt = datetime.fromisoformat(due_date)
                days_left = (due_dt.date() - datetime.now().date()).days
                if days_left > 0:
                    parts.append(f"D-{days_left}")
                elif days_left == 0:
                    parts.append("D-DAY")
                else:
                    parts.append(f"D+{abs(days_left)}")
            except Exception as e:
                print(f"[DEBUG] D-day 계산 오류: {e}")
                pass
        # 제목 앞에 체크 표시
        if item_data.get("checked"):
            parts.append("✓")
        # 실제 제목
        parts.append(title)
        return " ".join(parts)

    def _update_list_item(self, item: QListWidgetItem, idx: int) -> None:
        """리스트 아이템 업데이트 (참조 오류 방지)"""
        is_checked = self.items[idx]["checked"]
        # 텍스트는 항상 render_task_title_with_emoji로
        item.setText(self.render_task_title_with_emoji(self.items[idx]))
        if is_checked:
                item.setForeground(QColor("#666666"))
                font = QFont("Helvetica", 9, QFont.Weight.Normal)
                font.setStrikeOut(True)
                item.setFont(font)
        else:
            item.setForeground(QColor("#000000"))
            font = QFont("Helvetica", 9, QFont.Weight.Normal)
            font.setStrikeOut(False)
            item.setFont(font)
        if self.items[idx]["details"]:
            item.setToolTip(
                f"{self.items[idx]['title']}\n\n{self.items[idx]['details']}")
        else:
            item.setToolTip(self.items[idx]["title"])
            self._save_current_state()
            
    def _reorder_items(self):
        """체크된 항목을 하단으로 이동, UI와 데이터 완전 동기화"""
        try:
            # 데이터만 재정렬
            unchecked_items = [d for d in self.items if not d.get("checked", False)]
            checked_items = [d for d in self.items if d.get("checked", False)]
            self.items = unchecked_items + checked_items
            
            # UI 재생성
            self.list_widget.blockSignals(True)
            self.list_widget.clear()
            
            # UI만 업데이트하는 경우임을 표시
            self._skip_items_append = True
            try:
                # 아이템 추가
                for item_data in self.items:
                    self._add_list_item(item_data)
            finally:
                # 플래그 제거
                delattr(self, '_skip_items_append')
                
            self.list_widget.blockSignals(False)
            self._save_current_state()
            
        except Exception as e:
            print(f"Error in _reorder_items: {str(e)}")
            # 에러 발생 시 UI 상태 복구
            self.list_widget.blockSignals(False)
            if hasattr(self, '_skip_items_append'):
                delattr(self, '_skip_items_append')
            self.load_tasks(self.items)  # 현재 데이터로 UI 재구성

    def load_tasks(self, tasks_list):
        """태스크 목록 로드 (데이터와 UI 완전 동기화)"""
        self.items = list(tasks_list)  # 복사본 사용
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for item_data in self.items:
            self._add_list_item(item_data)
        self.list_widget.blockSignals(False)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_file = "anti_adhd_settings.ini"
        
        # 절대 경로로 변경 (AppData/Local 사용)
        app_data_dir = os.path.join(
            os.environ.get('LOCALAPPDATA', ''), 'Anti-ADHD')
        self.data_dir = os.path.join(app_data_dir, 'data')
        print(f"[DEBUG] 초기화: 데이터 디렉토리 = {self.data_dir}")
        
        # 데이터 디렉토리 생성
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            print(f"[DEBUG] 데이터 디렉토리 생성/확인 완료")
        except OSError as e:
            print(f"[DEBUG] 데이터 디렉토리 생성 실패: {e}")
            QMessageBox.critical(self, "초기화 오류", 
                f"데이터 디렉토리 생성 실패:\n{self.data_dir}\n{e}")
        
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

        # UI 초기화
        self.init_ui()
        
        # 설정 로드
        self.load_settings()
        
        # 단축키 설정
        self.setup_shortcuts()
        
        # 검색 기능 초기화
        self.setup_search()

        self.projects_data = {}
        self.current_project_name = None
        self.load_all_projects()
        self.select_initial_project()

        # 사이드바 초기 상태 설정
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
        sidebar_visible = settings.value("sidebarVisible", False, type=bool)
        self.sidebar.setVisible(sidebar_visible)
        self.update_sidebar_toggle_icon()

        self.is_test_mode = False  # 테스트 모드 플래그 추가
        self.dark_mode = False  # 다크 모드 상태 초기화
        # 프로그램 최초 실행 시 테마 적용
        self.apply_theme()

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
        QShortcut(Qt.CTRL + Qt.Key_Return, self,
                  self.add_task_to_current_quadrant)
        QShortcut(Qt.CTRL + Qt.Key_Up, self, self.move_selected_task_up)
        QShortcut(Qt.CTRL + Qt.Key_Down, self, self.move_selected_task_down)
        
        # 기타
        QShortcut(Qt.CTRL + Qt.Key_Comma, self, self.open_settings_dialog)
        QShortcut(Qt.CTRL + Qt.Key_Z, self, self.restore_from_backup)
        
        QShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_B,
                  self, self.toggle_main_toolbar)
        QShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_F,
                  self, self.toggle_search_toolbar)
        
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
        """사이드바 너비 강제 조정 (더 이상 사용하지 않음)"""
        pass  # 고정 너비를 사용하므로 이 메서드는 더 이상 필요하지 않음

    def adjust_sidebar_width(self):
        """사이드바 너비 조정 (더 이상 사용하지 않음)"""
        pass  # 고정 너비를 사용하므로 이 메서드는 더 이상 필요하지 않음

    def init_ui(self):
        self.setWindowTitle("Anti-ADHD")
        # --- 디자인 토큰 ---
        PRIMARY = "#1976d2"
        ACCENT = "#ff9800"
        ERROR = "#d32f2f"
        BG = "#f8f9fa"
        BORDER = "#e0e0e0"
        FONT = "'Segoe UI', 'Noto Sans KR', 'Pretendard', Arial, sans-serif"
        
        # --- 메뉴바 ---
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
        self.toggle_searchbar_action.triggered.connect(
            self.toggle_search_toolbar)
        view_menu.addAction(self.toggle_searchbar_action)
        
        # 통계 메뉴
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
        help_action = QAction("도움말 보기", self)
        help_action.triggered.connect(self.open_help_dialog)
        help_menu.addAction(help_action)
        
        # --- 메인 툴바 ---
        self.toolbar = self.addToolBar("메인 툴바")
        self.toolbar.setObjectName("main_toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setAllowedAreas(Qt.NoToolBarArea)  # 툴바 영역 고정
        self.toolbar.setIconSize(QSize(20, 20))
        # self.toolbar.setStyleSheet(...)  # <-- 기존 스타일시트 적용 코드 삭제
        
        # opacity_icon은 툴바 생성 후에 만들어야 함
        opacity_icon = QIcon(self.create_opacity_icon(QColor("black")))
        self.opacity_action = QAction(opacity_icon, "", self)
        self.opacity_action.setToolTip("창 투명도 조절")
        self.opacity_action.triggered.connect(self.show_opacity_popup)
        self.opacity_popup = None
        
        # --- 툴바 액션 인스턴스 생성 및 설정 ---
        self.toggle_sidebar_action = QAction(self)
        self.toggle_sidebar_action.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.toggle_sidebar_action.setToolTip("프로젝트 목록 보이기/숨기기")
        self.toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        
        self.dark_mode_action = QAction(self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setIcon(
            self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.dark_mode_action.setToolTip("다크 모드 전환")
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        
        self.always_on_top_action = QAction(self)
        self.always_on_top_action.setCheckable(True)
        self.update_always_on_top_icon()
        self.always_on_top_action.triggered.connect(self.toggle_always_on_top)
        
        # 톱니바퀴 이모지(⚙️)를 아이콘으로 사용
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        font = QFont()
        font.setPointSize(16)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "⚙️")
        painter.end()
        settings_toolbar_icon = QIcon(pixmap)
        self.settings_toolbar_action = QAction(settings_toolbar_icon, "", self)
        self.settings_toolbar_action.setToolTip("애플리케이션 설정 열기")
        self.settings_toolbar_action.triggered.connect(
            self.open_settings_dialog)
        
        # --- 툴바 액션 추가 ---
        self.toolbar.addAction(self.toggle_sidebar_action)
        self.toolbar.addAction(self.dark_mode_action)
        self.toolbar.addAction(self.opacity_action)
        self.toolbar.addAction(self.always_on_top_action)
        self.toolbar.addAction(self.settings_toolbar_action)
        
        # --- 사이드바 생성 및 스타일 ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        # 상단 버튼/라벨 완전 제거
        # 프로젝트 리스트
        self.project_list = ProjectListWidget(self)
        # 고정 높이 제거, Expanding 정책 적용
        self.project_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.project_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px 4px;
                border-radius: 4px;
                color: #333333;
                height: 30px;  /* 아이템 높이 고정 */
                min-height: 30px;  /* 최소 높이 설정 */
                max-height: 30px;  /* 최대 높이 설정 */
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        self.project_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_list.viewport().setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_list.viewport().customContextMenuRequested.connect(
            self.show_project_context_menu)
        self.project_list.currentItemChanged.connect(
            self.on_project_selection_changed)
        self.project_list.setHorizontalScrollBarPolicy(
            1)  # Qt.ScrollBarAlwaysOff = 1
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
        # self.sidebar_layout.addStretch()
        # 사이드바 크기 설정
        self.sidebar.setMaximumWidth(200)

        # --- 검색바 스타일 개선 ---
        self.search_toolbar = self.addToolBar("검색")
        self.search_toolbar.setObjectName("search_toolbar")
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

        # Eisenhower Matrix 색상/키워드/설명/아이콘 (한글화)
        quadrant_info = [
            ("#d32f2f", "중요·긴급", "즉시 처리", self.style().standardIcon(
                QStyle.SP_DialogApplyButton)),
            ("#f57c00", "중요", "계획/우선순위",
             self.style().standardIcon(QStyle.SP_BrowserReload)),
            ("#388e3c", "긴급", "위임/빠른 처리",
             self.style().standardIcon(QStyle.SP_ArrowRight)),
            ("#757575", "중요 아님·긴급 아님", "삭제/미루기",
             self.style().standardIcon(QStyle.SP_TrashIcon)),
        ]
        # 3x3 그리드로 확장하여 축 라벨이 사분면 바깥에 위치하도록
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        grid_layout.setContentsMargins(16, 16, 16, 16)
        self.quadrant_widgets = []
        for i, (color, keyword, desc, icon) in enumerate(quadrant_info):
            quad_widget = EisenhowerQuadrantWidget(
                color, keyword, desc, icon, self)
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
        self.splitter.setStyleSheet(
            "QSplitter { border: none; margin: 0; padding: 0; }")
        self.setCentralWidget(self.splitter)
        self.update_sidebar_toggle_icon()
        # 스타일시트는 기존과 동일하게 유지 또는 필요시 추가

        # 메인 툴바 우클릭 메뉴 및 옵션 완전 비활성화
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.setAllowedAreas(Qt.NoToolBarArea)
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

    def create_opacity_icon(self, color):
        icon_size = self.toolbar.iconSize()  # 툴바 아이콘 크기 참조
        pixmap = QPixmap(icon_size)  # 참조한 크기로 QPixmap 생성
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        # 아이콘 내부 여백을 고려하여 그림 크기 조정 (예: 전체 크기의 70-80%)
        padding = int(icon_size.width() * 0.15)
        draw_rect = pixmap.rect().adjusted(padding, padding, -padding, -padding)
        painter.setPen(QPen(color, 1.5 if icon_size.width()
                       > 16 else 1))  # 선 두께도 크기에 따라 조정
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
            except RuntimeError:  # 이미 삭제된 객체에 접근하려 할 때
                pass  # 특별히 할 작업 없음
            self.opacity_popup = None  # 이전 참조 정리

        # 팝업을 새로 생성하고 표시
        button = self.toolbar.widgetForAction(self.opacity_action)
        if button:
            point = button.mapToGlobal(QPoint(0, button.height()))
            self.opacity_popup = OpacityPopup(self)
            self.opacity_popup.show_at(point)
        else: 
            cursor_pos = QCursor.pos()  # QCursor를 사용하려면 QtGui에서 import 필요
            self.opacity_popup = OpacityPopup(self)
            self.opacity_popup.show_at(cursor_pos)

    def show_project_context_menu(self, position):
        """프로젝트 컨텍스트 메뉴를 표시합니다."""
        menu = QMenu(self)
        
        # 메뉴 액션 생성
        add_action = menu.addAction("새 프로젝트")
        rename_action = menu.addAction("이름 변경")
        delete_action = menu.addAction("삭제")
        
        # 현재 선택된 항목이 있는 경우에만 일부 메뉴 활성화
        current_item = self.project_list.currentItem()
        if current_item:
            rename_action.setEnabled(True)
            delete_action.setEnabled(True)
        else:
            rename_action.setEnabled(False)
            delete_action.setEnabled(False)
        
        # 메뉴 표시 및 액션 처리
        action = menu.exec_(self.project_list.mapToGlobal(position))
        
        if action == add_action:
            self.add_new_project()
        elif action == rename_action and current_item:
            self.rename_selected_project()
        elif action == delete_action and current_item:
            self.delete_selected_project()

    def add_new_project(self, name=None):
        if name is None:
            if not self.is_test_mode:  # 테스트 모드가 아닐 때만 다이얼로그 표시
                name, ok = QInputDialog.getText(self, "새 프로젝트", "프로젝트 이름:")
                if not ok or not name:
                    return
            else:
                name = "TestProject"  # 테스트 모드에서는 기본 이름 사용
        
        if name in self.projects_data:
            if not self.is_test_mode:  # 테스트 모드가 아닐 때만 경고 표시
                QMessageBox.warning(self, "경고", "이미 존재하는 프로젝트 이름입니다.")
            return
        
        self.projects_data[name] = {
            "quadrant1": [],
            "quadrant2": [],
            "quadrant3": [],
            "quadrant4": []
        }
        
        item = QListWidgetItem(name)
        self.project_list.addItem(item)
        self.project_list.setCurrentItem(item)
        self.save_project_to_file(name)

    def rename_selected_project(self):
        current_item = self.project_list.currentItem()
        if not current_item:
            return
        old_name = current_item.text()
        new_name, ok = QInputDialog.getText(
            self, "이름 변경", f"'{old_name}'의 새 이름:", text=old_name)
        if ok and new_name.strip() and new_name.strip() != old_name:
            new_name_stripped = new_name.strip()
            if new_name_stripped in self.projects_data:
                QMessageBox.warning(self, "중복 오류", "이미 존재하는 프로젝트 이름입니다.")
                return
            self.projects_data[new_name_stripped] = self.projects_data.pop(
                old_name)
            current_item.setText(new_name_stripped)
            old_file_path = os.path.join(
                self.data_dir, f"project_{old_name}.json")
            new_file_path = os.path.join(
                self.data_dir, f"project_{new_name_stripped}.json")
            if os.path.exists(old_file_path):
                try:
                    os.rename(old_file_path, new_file_path)
                except OSError as e:
                    QMessageBox.critical(
                        self, "파일 오류", f"프로젝트 파일 이름 변경 실패: {e}")
            if self.auto_save_enabled:
                self.save_project_to_file(new_name_stripped) 
            self.adjust_sidebar_width()

    def delete_selected_project(self):
        current_item = self.project_list.currentItem()
        if not current_item:
            return
            
        project_name = current_item.text()
        
        # 사용자 확인
        reply = QMessageBox.question(
            self, 
            "프로젝트 삭제", 
            f"'{project_name}' 프로젝트를 삭제하시겠습니까?\n(데이터와 해당 프로젝트 파일 모두 삭제됩니다!)",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # UI에서 제거
                row = self.project_list.row(current_item)
                self.project_list.takeItem(row)
                
                # 메모리에서 제거
                if project_name in self.projects_data:
                    del self.projects_data[project_name]
                
                # 파일 시스템에서 제거
                file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        QMessageBox.critical(self, "파일 오류", f"프로젝트 파일 삭제 실패: {e}")
                        return
                
                # 다음 프로젝트 선택
                if self.project_list.count() > 0:
                    new_row = max(0, row - 1)
                    if new_row < self.project_list.count():
                        self.project_list.setCurrentRow(new_row)
                    else:
                        self.project_list.setCurrentRow(self.project_list.count() - 1)
                else:
                    self.current_project_name = None
                    self.clear_all_quadrants()
                
                # UI 업데이트
                self.adjust_sidebar_width()
                self.statusBar().showMessage(f"'{project_name}' 프로젝트가 삭제되었습니다.", 3000)
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"프로젝트 삭제 중 오류가 발생했습니다: {str(e)}")
                # 오류 발생 시 UI 복구
                self.reload_data_and_ui()

    def on_project_selection_changed(self, current_item, previous_item):
        """프로젝트 선택 변경 시 호출"""
        if not current_item:
            return
            
        project_name = current_item.text()
        print(f"[DEBUG] 프로젝트 선택 변경: {project_name}")
        
        # 이전 프로젝트 저장 (자동 저장 옵션에 따라)
        if previous_item and self.auto_save_enabled:
            previous_project = previous_item.text()
            print(f"[DEBUG] 이전 프로젝트 저장: {previous_project}")
            self.save_project_to_file(previous_project)
        
        # 새 프로젝트 로드
        if project_name not in self.projects_data:
            print(f"[DEBUG] 새 프로젝트 데이터 로드: {project_name}")
            self.projects_data[project_name] = self.load_project_from_file(
                project_name)
        
        # 현재 프로젝트 이름 업데이트
        self.current_project_name = project_name
        print(f"[DEBUG] 현재 프로젝트 설정: {project_name}")
        
        # UI 업데이트
        self.update_quadrant_display(project_name)
        self.update_project_status_label()
        
        # 프로젝트 목록 UI 업데이트
        for i in range(self.project_list.count()):
            item = self.project_list.item(i)
            if item.text() == project_name:
                self.project_list.setCurrentItem(item)
                item.setSelected(True)
                break
        
        # 상태바 메시지
        self.statusBar().showMessage(f"'{project_name}' 프로젝트로 전환", 2000)

    def save_project_to_file(self, project_name, file_path=None):
        """프로젝트를 파일로 저장"""
        if file_path is None:
            file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
        if not project_name or project_name not in self.projects_data:
            print(
                f"[DEBUG] 저장 실패: 프로젝트 이름이 유효하지 않음 (project_name={project_name})")
            return
            
        print(f"[DEBUG] 저장 시작: {project_name}")
        print(f"[DEBUG] 데이터 디렉토리: {self.data_dir}")
        
        # 데이터 구조 검증 및 보정
        project_data = self.projects_data[project_name]
        if "tasks" not in project_data:
            project_data["tasks"] = [[], [], [], []]
            
        # 각 사분면의 데이터 구조 검증
        for quadrant in project_data["tasks"]:
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
        
        print(f"[DEBUG] 검증된 프로젝트 데이터: {project_data}")
        
        # 데이터 디렉토리 존재 확인 및 생성
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir, exist_ok=True)
                print(f"[DEBUG] 데이터 디렉토리 생성됨: {self.data_dir}")
            except OSError as e:
                print(f"[DEBUG] 데이터 디렉토리 생성 실패: {e}")
                QMessageBox.critical(self, "저장 오류", 
                    f"데이터 디렉토리 생성 실패:\n{self.data_dir}\n{e}")
                return

        self.statusBar().showMessage(f"'{project_name}' 저장 중...")
        QApplication.processEvents()
        
        file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
        print(f"[DEBUG] 저장할 파일 경로: {file_path}")
        
        try:
            # 임시 파일에 먼저 저장
            temp_file_path = file_path + '.tmp'
            print(f"[DEBUG] 임시 파일에 저장 시도: {temp_file_path}")
            
            # 데이터를 JSON으로 직렬화
            json_data = json.dumps(project_data, ensure_ascii=False, indent=4)
            print(f"[DEBUG] 직렬화된 데이터: {json_data}")
            
            # 임시 파일에 저장
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
            
            # 저장 성공 시 기존 파일 교체
            if os.path.exists(file_path):
                os.replace(temp_file_path, file_path)
            else:
                os.rename(temp_file_path, file_path)
                
            print(f"[DEBUG] 파일 저장 완료: {file_path}")
            
            # 저장된 파일 확인
            if os.path.exists(file_path):
                print(f"[DEBUG] 저장된 파일 크기: {os.path.getsize(file_path)} bytes")
            else:
                print(f"[DEBUG] 저장된 파일이 존재하지 않음!")
            
            # 캐시 업데이트
            self._project_cache[project_name] = {
                'data': project_data,
                'last_access': time.time()
            }
            
        except (IOError, OSError) as e:
            print(f"[DEBUG] 저장 중 오류 발생: {e}")
            QMessageBox.critical(self, "저장 오류", 
                f"프로젝트 '{project_name}' 저장 중 오류가 발생했습니다:\n{e}\n\n"
                "임시 파일이 남아있을 수 있습니다. 프로그램을 다시 시작해주세요.")
            try:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            except:
                pass
            return
            
        self.statusBar().showMessage(f"'{project_name}' 저장 완료", 3000)
        print(f"[DEBUG] 저장 프로세스 완료: {project_name}")

    def load_project_from_file(self, project_name):
        print(f"[DEBUG] 프로젝트 파일 로드 시작: {project_name}")
        self.statusBar().showMessage(f"'{project_name}' 로드 중...")
        QApplication.processEvents()
        
        file_path = os.path.join(self.data_dir, f"project_{project_name}.json")
        print(f"[DEBUG] 파일 경로: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"[DEBUG] 파일이 존재하지 않음: {file_path}")
            return {"tasks": [[], [], [], []]}
            
        try:
            print(f"[DEBUG] 파일 읽기 시도")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[DEBUG] 파일 읽기 성공")
            
            # 데이터 구조 검증 및 보정
            if not isinstance(data, dict):
                print(f"[DEBUG] 데이터가 딕셔너리가 아님: {type(data)}")
                raise ValueError("프로젝트 데이터가 올바른 형식이 아닙니다.")
                
            if "tasks" not in data:
                print(f"[DEBUG] tasks 필드 없음, 기본값으로 초기화")
                data["tasks"] = [[], [], [], []]
            elif not isinstance(data["tasks"], list) or len(data["tasks"]) != 4:
                print(f"[DEBUG] tasks 배열이 올바르지 않음: {data['tasks']}")
                data["tasks"] = [[], [], [], []]
                
            print(f"[DEBUG] 데이터 구조 검증 완료")
            self.statusBar().showMessage(f"'{project_name}' 로드 완료", 3000)
            return data
            
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON 디코딩 오류: {e}")
            QMessageBox.critical(self, "로드 오류", 
                f"프로젝트 '{project_name}' 파일이 손상되었습니다:\n{e}\n\n"
                "프로젝트를 백업에서 복원하거나 새로 만들어주세요.")
            return {"tasks": [[], [], [], []]}
        except Exception as e:
            QMessageBox.critical(self, "로드 오류", 
                f"프로젝트 '{project_name}' 로드 중 오류가 발생했습니다:\n{e}")
            return {"tasks": [[], [], [], []]}

    def load_all_projects(self):
        print(f"[DEBUG] 프로젝트 로드 시작")
        print(f"[DEBUG] 데이터 디렉토리: {self.data_dir}")
        
        self.project_list.clear()
        self.projects_data.clear()
        
        if not os.path.exists(self.data_dir):
            print(f"[DEBUG] 데이터 디렉토리가 존재하지 않음, 생성 시도")
            try:
                os.makedirs(self.data_dir)
                print(f"[DEBUG] 데이터 디렉토리 생성됨")
            except OSError as e:
                print(f"[DEBUG] 데이터 디렉토리 생성 실패: {e}")
                QMessageBox.critical(
                    self, "오류", f"데이터 디렉토리 생성 실패: {self.data_dir}\n{e}")
                return
        
        # 디렉토리 내용 확인
        try:
            files = os.listdir(self.data_dir)
            print(f"[DEBUG] 디렉토리 내용: {files}")
        except OSError as e:
            print(f"[DEBUG] 디렉토리 읽기 실패: {e}")
            return
            
        for filename in os.listdir(self.data_dir):
            if filename.startswith("project_") and filename.endswith(".json"):
                project_name = filename[8:-5]  # "project_" 제거하고 ".json" 제거
                print(f"[DEBUG] 프로젝트 파일 발견: {filename}")
                print(f"[DEBUG] 프로젝트 이름 추출: {project_name}")
                
                project_data = self.load_project_from_file(project_name)
                print(f"[DEBUG] 프로젝트 데이터 로드: {project_name}")
                print(f"[DEBUG] 데이터 내용: {project_data}")
                
                if "completed" not in project_data:
                    project_data["completed"] = []
                    for tasks in project_data.get("tasks", [[], [], [], []]):
                        project_data["completed"].append([False] * len(tasks))
                
                self.projects_data[project_name] = project_data
                self.project_list.addItem(project_name)
                print(f"[DEBUG] 프로젝트 추가 완료: {project_name}")
        
        print(f"[DEBUG] 전체 프로젝트 로드 완료")
        print(f"[DEBUG] 로드된 프로젝트 수: {len(self.projects_data)}")
        self.adjust_sidebar_width()
    
    def select_initial_project(self):
        if self.project_list.count() > 0:
            self.project_list.setCurrentRow(0)
        else:
            # 기본 프로젝트가 없으면 하나 생성
            default_project_name = "기본 프로젝트"
            self.projects_data[default_project_name] = {
                "tasks": [[], [], [], []]}
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
                    quad_widget.clear_tasks()  # 데이터가 부족할 경우 대비
        else:
            self.clear_all_quadrants()

    def clear_all_quadrants(self):
        for quad_widget in self.quadrant_widgets:
            quad_widget.clear_tasks()
            
    def toggle_sidebar(self):
        """사이드바 토글 (QSplitter 기반 완전 교정)"""
        sidebar_index = 0  # splitter에서 sidebar의 인덱스
        main_index = 1     # splitter에서 메인 컨텐츠 인덱스
        sizes = self.splitter.sizes()
        sidebar_visible = sizes[sidebar_index] > 0
        
        if sidebar_visible:
            # 사이드바 숨기기
            self.sidebar.setVisible(False)  # 먼저 숨기기
            self.splitter.setSizes([0, sizes[main_index] + sizes[sidebar_index]])
        else:
            # 사이드바 보이기 (최대 너비로)
            self.sidebar.setVisible(True)  # 먼저 보이기
            self.splitter.setSizes([self.sidebar.maximumWidth(), sizes[main_index]])
        
        self.update_sidebar_toggle_icon()
        
        # 메뉴 액션 체크 상태 동기화
        for action in self.menuBar().actions():
            if action.text() == "보기":
                for sub_action in action.menu().actions():
                    if sub_action.text() == "사이드바":
                        sub_action.setChecked(not sidebar_visible)
                        break
        
        # 설정 저장
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
        settings.setValue("sidebarVisible", not sidebar_visible)

    def _update_sidebar_state(self, visible):
        """사이드바 상태 업데이트"""
        # 아이콘 업데이트
        self.update_sidebar_toggle_icon()

        # 메뉴 액션 체크 상태 동기화
        for action in self.menuBar().actions():
            if action.text() == "보기":
                for sub_action in action.menu().actions():
                    if sub_action.text() == "사이드바":
                        sub_action.setChecked(visible)
                        break

        # 설정 저장
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
        settings.setValue("sidebarVisible", visible)

    def set_always_on_top(self, enabled):
        self.always_on_top = enabled
        if enabled:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.update_always_on_top_icon()  # 아이콘 및 툴큐 업데이트
        self.show()  # 플래그 변경 후 show() 호출 필수

    def toggle_always_on_top(self):
        # QAction의 checked 상태가 이미 변경된 후 호출됨
        self.set_always_on_top(self.always_on_top_action.isChecked())

    def update_always_on_top_icon(self):
        if not hasattr(self, 'always_on_top_action'):  # 초기화 중 오류 방지
            return
        if self.always_on_top_action.isChecked(): 
            # "고정됨" 상태 아이콘: SP_DialogYesButton 또는 핀 모양 아이콘
            icon = self.style().standardIcon(QStyle.SP_DialogYesButton) 
            self.always_on_top_action.setIcon(icon)
            self.always_on_top_action.setToolTip(
                "창 고정 해제 (Always on Top 비활성화)")
        else:
            # "고정 안됨" 상태 아이콘: SP_DialogNoButton 또는 빈 핀 모양 아이콘
            icon = self.style().standardIcon(QStyle.SP_DialogNoButton) 
            self.always_on_top_action.setIcon(icon)
            self.always_on_top_action.setToolTip(
                "창 항상 위에 고정 (Always on Top 활성화)")

    def set_window_opacity(self, opacity):
        self.window_opacity = opacity 
        super().setWindowOpacity(opacity)
        # OpacityPopup이 열려있다면 슬라이더 값도 동기화 (선택적, 이미 popup 내부에서 처리 중)
        # if self.opacity_popup and self.opacity_popup.isVisible():
        #    self.opacity_popup.slider.setValue(int(opacity * 100))

    def load_settings(self):
        """설정 로드 (QSplitter 사이즈까지 복원)"""
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
        sidebar_visible = settings.value("sidebarVisible", False, type=bool)
        if sidebar_visible:
            self.splitter.setSizes([self.sidebar.maximumWidth(), 1])
            self.sidebar.setVisible(True)
        else:
            self.splitter.setSizes([0, 1])
            self.sidebar.setVisible(False)
        self.update_sidebar_toggle_icon()
        # 메뉴 액션 체크 상태 동기화
        for action in self.menuBar().actions():
            if action.text() == "보기":
                for sub_action in action.menu().actions():
                    if sub_action.text() == "사이드바":
                        sub_action.setChecked(sidebar_visible)
                        break
        self.data_dir = settings.value("dataDir", self.data_dir)
        self.always_on_top = settings.value("alwaysOnTop", False, type=bool)
        if hasattr(self, 'always_on_top_action'): 
            self.always_on_top_action.setChecked(self.always_on_top) 
        self.update_always_on_top_icon()
        if self.always_on_top_action.isChecked():
             self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
             self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.window_opacity = settings.value("windowOpacity", 1.0, type=float)
        self.set_window_opacity(self.window_opacity)
        self.auto_save_enabled = settings.value(
            "general/auto_save", True, type=bool)
    
    def save_settings(self):
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
        settings.setValue("geometry", self.saveGeometry())
        
        # 툴바 상태 저장
        if hasattr(self, 'toolbar'):
            settings.setValue("toolbarVisible", self.toolbar.isVisible())
        if hasattr(self, 'search_toolbar'):
            settings.setValue("searchToolbarVisible",
                              self.search_toolbar.isVisible())
            
        settings.setValue("sidebarVisible", self.sidebar.isVisible())
        settings.setValue("dataDir", self.data_dir)  # 현재 사용 중인 data_dir을 저장
        settings.setValue("alwaysOnTop", self.always_on_top)
        settings.setValue("windowOpacity", self.window_opacity)
        # 자동 저장 설정은 SettingsDialog에서 직접 QSettings에 저장함
        # settings.setValue("general/auto_save", self.auto_save_enabled) # MainWindow에서 관리 시 필요

    def open_settings_dialog(self):
        dialog = SettingsDialog(current_data_dir=self.data_dir, 
                                settings_file_path=self.settings_file,
                                parent=self)
        # 다크모드 상태 전달 및 적용
        if hasattr(self, 'dark_mode'):
            dialog.apply_theme(self.dark_mode)
        if dialog.exec_() == QDialog.Accepted:
            pass

    # --- 신규 파일 작업 메서드 --- #
    def import_project_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "프로젝트 파일 가져오기", "", "JSON 파일 (*.json);;모든 파일 (*)", options=options)
        
        if not file_path:
            return  # 사용자가 취소

        try:
            # 1. 파일 내용 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # 기본 JSON 구조 검증 및 보정
            if not isinstance(imported_data, dict):
                QMessageBox.warning(
                    self, "가져오기 오류", "선택한 파일의 최상위 데이터가 딕셔너리 형식이 아닙니다.")
                return
            
            tasks_data = imported_data.get("tasks")
            if not isinstance(tasks_data, list) or len(tasks_data) != 4:
                # tasks가 없거나, 리스트가 아니거나, 4개의 quadrant 구조가 아니면 기본 구조라도 만들어줌
                # 사용자의 데이터를 최대한 보존하되, 앱 구조에 맞게끔 최소한으로 조정
                corrected_tasks = [[], [], [], []]
                if isinstance(tasks_data, list):  # 일부 데이터가 리스트 형태로 있다면 최대한 활용
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
        if not new_project_name:  # 이름이 비었으면 기본 이름 사용
            new_project_name = "가져온_프로젝트"

        # 중복 이름 처리
        name_suffix = 1
        final_project_name = new_project_name
        while final_project_name in self.projects_data:
            final_project_name = f"{new_project_name}_{name_suffix}"
            name_suffix += 1
        
        text, ok = QInputDialog.getText(
            self, "프로젝트 이름 확인", "가져올 프로젝트의 이름을 입력하세요:", text=final_project_name)
        if ok and text.strip():
            final_project_name = text.strip()
            if final_project_name in self.projects_data:
                QMessageBox.warning(
                    self, "이름 중복", f"프로젝트 이름 '{final_project_name}'은(는) 이미 존재합니다. 가져오기를 취소합니다.")
                return
        elif not ok: 
            return
        
        new_project_file_path = os.path.join(
            self.data_dir, f"project_{final_project_name}.json")
        try:
            with open(new_project_file_path, 'w', encoding='utf-8') as f:
                json.dump(imported_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(
                self, "가져오기 오류", f"가져온 프로젝트를 저장하는 중 오류가 발생했습니다: {e}")
            return

        self.projects_data[final_project_name] = imported_data
        self.project_list.addItem(final_project_name)

        items = self.project_list.findItems(
            final_project_name, Qt.MatchExactly)
        if items:
            self.project_list.setCurrentItem(items[0]) 
        
        QMessageBox.information(
            self, "가져오기 성공", f"프로젝트 '{final_project_name}'(으)로 성공적으로 가져왔습니다.")

    def save_current_project(self):
        if self.current_project_name:
            self.save_project_to_file(self.current_project_name)
            # 사용자에게 저장되었음을 알리는 피드백 (선택적)
            # self.statusBar().showMessage(f"'{self.current_project_name}' 저장됨", 2000)
        else:
            QMessageBox.information(self, "알림", "저장할 프로젝트가 선택되지 않았습니다.")

    def save_project_as(self):
        if not self.current_project_name:
            QMessageBox.information(
                self, "알림", "'다른 이름으로 저장'할 프로젝트가 선택되지 않았습니다.")
            return

        current_project_data = self.projects_data.get(
            self.current_project_name)
        if not current_project_data:
            QMessageBox.warning(
                self, "오류", f"현재 프로젝트 '{self.current_project_name}'의 데이터를 찾을 수 없습니다.")
            return

        # 새 프로젝트 이름 제안 시 현재 이름 기반
        suggested_new_name = f"{self.current_project_name}_복사본"
        
        # 파일 저장 다이얼로그
        new_file_path, _ = QFileDialog.getSaveFileName(
            self,
            "프로젝트 다른 이름으로 저장",
            os.path.join(self.data_dir, f"project_{suggested_new_name}.json"),
            "JSON 파일 (*.json)"
        )
        
        if not new_file_path:
            return  # 사용자가 취소

        try:
            # 선택한 경로에 파일 저장
            with open(new_file_path, 'w', encoding='utf-8') as f:
                json.dump(current_project_data, f,
                          ensure_ascii=False, indent=4)

            # 파일명에서 프로젝트 이름 추출
            new_project_name = os.path.splitext(
                os.path.basename(new_file_path))[0]
            if new_project_name.startswith("project_"):
                new_project_name = new_project_name[8:]

            # 프로젝트 목록에 새 프로젝트 추가
            self.projects_data[new_project_name] = current_project_data
            self.project_list.addItem(new_project_name)

            # 새 프로젝트 선택
            items = self.project_list.findItems(
                new_project_name, Qt.MatchExactly)
            if items:
                self.project_list.setCurrentItem(items[0])

            QMessageBox.information(
                self, "저장 완료", f"프로젝트가 '{new_project_name}'(으)로 저장되었습니다.")

        except Exception as e:
            QMessageBox.critical(
                self, "저장 오류", f"프로젝트 저장 중 오류가 발생했습니다: {str(e)}")
            return

    def reload_data_and_ui(self):
        """
        데이터 디렉토리 변경(복원, 초기화 등) 후 프로젝트 데이터와 UI를 새로고침합니다.
        """
        # 1. 현재 로드된 프로젝트 데이터 및 사이드바 초기화
        self.projects_data.clear()
        self.project_list.clear()
        self.current_project_name = None  # 현재 선택된 프로젝트 없음으로 설정
        self.clear_all_quadrants()  # 4분면 클리어

        # 2. 데이터 디렉토리에서 모든 프로젝트 다시 로드
        # 데이터 디렉토리가 존재하지 않을 경우를 대비 (예: 초기화 직후)
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir)
            except OSError as e:
                QMessageBox.critical(
                    self, "오류", f"데이터 디렉토리 생성 실패: {self.data_dir}\n{e}")
                return  # 디렉토리 생성 실패 시 더 이상 진행 불가

        self.load_all_projects()  # 사이드바도 채워짐

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

    def update_sidebar_toggle_icon(self):
        """사이드바 토글 아이콘 업데이트"""
        if self.sidebar.isVisible():
            self.toggle_sidebar_action.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowLeft))
            self.toggle_sidebar_action.setToolTip("프로젝트 목록 숨기기 (Ctrl+B)")
        else:
            self.toggle_sidebar_action.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowRight))
            self.toggle_sidebar_action.setToolTip("프로젝트 목록 보이기 (Ctrl+B)")

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
        # 이미 다크 모드 액션이 있으면
        if hasattr(self, 'dark_mode_action'):
            return
            
        # 다크 모드 액션 생성
        self.dark_mode_action = QAction(self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setIcon(
            self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.dark_mode_action.setToolTip("다크 모드 전환")
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        
        # 툴바에 액션 추가
        if hasattr(self, 'toolbar'):
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
            font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', 'Arial', sans-serif;
            color: #e0e0e0;
        }
        # 기타 다크 테마 스타일 ... */
        """)
            # --- 다크 모드: 사이드바/프로젝트 리스트/툴바 스타일시트 동적 적용 ---
            if hasattr(self, 'sidebar'):
                self.sidebar.setStyleSheet("background: #232323; border: none;")
            if hasattr(self, 'project_list'):
                self.project_list.setStyleSheet("""
                    QListWidget {
                        background: #232323;
                        border: 1px solid #404040;
                        border-radius: 7px;
                        color: #e0e0e0;
                    }
                    QListWidget::item {
                        background: transparent;
                        color: #e0e0e0;
                    }
                    QListWidget::item:selected, QListWidget::item:focus {
                        background: #0d47a1;
                        color: #fff;
                    }
                    QListWidget::item:hover {
                        background: #404040;
                    }
                """)
            if hasattr(self, 'toolbar'):
                toolbar_style = """
                    QToolBar {
                        background: #232323 !important;
                        border-bottom: 1.5px solid #404040 !important;
                        padding: 0 0 0 0 !important;
                        spacing: 0px !important;
                        min-height: 32px !important;
                        margin: 0 !important;
                    }
                    QToolButton {
                        padding: 3px 4px !important;
                        border-radius: 5px !important;
                        background: transparent !important;
                        color: #e0e0e0 !important;
                    }
                    QToolButton:checked {
                        background: #0d47a1 !important;
                    }
                    QToolButton:hover {
                        background: #404040 !important;
                    }
                    QToolButton:focus {
                        outline: 2px solid #0d47a1 !important;
                        background: #0d47a1 !important;
                    }
                """
                self.toolbar.setStyleSheet(toolbar_style)
                if hasattr(self, 'search_toolbar'):
                    self.search_toolbar.setStyleSheet(toolbar_style)
            # 메뉴바/메뉴 다크 테마 적용
            self.menuBar().setStyleSheet("""
                QMenuBar {
                    background: #232323;
                    color: #e0e0e0;
                }
                QMenuBar::item {
                    background: transparent;
                    color: #e0e0e0;
                }
                QMenuBar::item:selected, QMenuBar::item:pressed {
                    background: #404040;
                    color: #fff;
                }
                QMenu {
                    background: #232323;
                    color: #e0e0e0;
                    border: 1.5px solid #404040;
                }
                QMenu::item {
                    background: transparent;
                    color: #e0e0e0;
                }
                QMenu::item:selected {
                    background: #0d47a1;
                    color: #fff;
                }
                QMenu::separator {
                    height: 1px;
                    background: #404040;
                    margin: 4px 0;
                }
            """)
        else:
            self.setStyleSheet("""
        QMainWindow {
            background-color: #f8f9fa;
        }
        QWidget {
            font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', 'Arial', sans-serif;
            color: #2c3e50;
        }
        # 기타 라이트 테마 스타일 ... */
        """)
            if hasattr(self, 'sidebar'):
                self.sidebar.setStyleSheet("")
            if hasattr(self, 'project_list'):
                self.project_list.setStyleSheet(f"""
                    QListWidget {{
                        background: #fff;
                        border: 1px solid #e0e0e0;
                        border-radius: 7px;
                        color: #333;
                    }}
                    QListWidget::item {{
                        background: transparent;
                        color: #333;
                    }}
                    QListWidget::item:selected, QListWidget::item:focus {{
                        background: #1976d2;
                        color: #fff;
                    }}
                    QListWidget::item:hover {{
                        background: #f3f6fa;
                    }}
                """)
            if hasattr(self, 'toolbar'):
                toolbar_style = f"""
                    QToolBar {{
                        background: #fff !important;
                        border-bottom: 1.5px solid #e0e0e0 !important;
                        padding: 0 0 0 0 !important;
                        spacing: 0px !important;
                        min-height: 32px !important;
                        margin: 0 !important;
                    }}
                    QToolButton {{
                        padding: 3px 4px !important;
                        border-radius: 5px !important;
                        background: transparent !important;
                        color: #1976d2 !important;
                    }}
                    QToolButton:checked {{
                        background: #e3f0ff !important;
                    }}
                    QToolButton:hover {{
                        background: #e8e8e8 !important;
                    }}
                    QToolButton:focus {{
                        outline: 2px solid #1976d2 !important;
                        background: #e3f0ff !important;
                    }}
                """
                self.toolbar.setStyleSheet(toolbar_style)
                if hasattr(self, 'search_toolbar'):
                    self.search_toolbar.setStyleSheet(toolbar_style)
            # 메뉴바/메뉴 라이트 테마 적용
            self.menuBar().setStyleSheet(f"""
                QMenuBar {{
                    background: #fff;
                    color: #2c3e50;
                }}
                QMenuBar::item {{
                    background: transparent;
                    color: #2c3e50;
                }}
                QMenuBar::item:selected, QMenuBar::item:pressed {{
                    background: #e3f0ff;
                    color: #1976d2;
                }}
                QMenu {{
                    background: #fff;
                    color: #2c3e50;
                    border: 1.5px solid #e0e0e0;
                }}
                QMenu::item {{
                    background: transparent;
                    color: #2c3e50;
                }}
                QMenu::item:selected {{
                    background: #1976d2;
                    color: #fff;
                }}
                QMenu::separator {{
                    height: 1px;
                    background: #e0e0e0;
                    margin: 4px 0;
                }}
            """)
        # 다크 모드에서 검색 입력창 텍스트와 placeholder 모두 흰색으로
        if hasattr(self, 'search_input'):
            if self.dark_mode:
                self.search_input.setStyleSheet(
                    """
                    QLineEdit {
                        color: #fff;
                        background: #232323;
                        border: 1.5px solid #404040;
                        border-radius: 6px;
                        selection-background-color: #0d47a1;
                        selection-color: #fff;
                    }
                    QLineEdit::placeholder {
                        color: #fff;
                    }
                    """
                )
                # placeholder 강제 재설정 (일부 환경에서 필요)
                ph = self.search_input.placeholderText()
                self.search_input.setPlaceholderText('')
                self.search_input.setPlaceholderText(ph)
            else:
                self.search_input.setStyleSheet("")

    def setup_search(self):
        """검색 기능 설정"""
        # 검색 입력 필드
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("작업 검색...")
        self.search_input.setMinimumWidth(200)
        self.search_input.textChanged.connect(self.filter_tasks)
        self.search_toolbar.addWidget(self.search_input)

        # 검색 옵션
        self.search_options = QToolButton()
        self.search_options.setPopupMode(QToolButton.InstantPopup)
        self.search_options.setIcon(
            self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
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

        # 검색 결과 레이블 추가
        self.search_result_label = QLabel()
        self.search_result_label.setText("")
        self.search_toolbar.addWidget(self.search_result_label)

        # 검색 옵션 변경 시 필터링 다시 실행
        self.search_title_action.triggered.connect(self.filter_tasks)
        self.search_details_action.triggered.connect(self.filter_tasks)
        self.search_completed_action.triggered.connect(self.filter_tasks)

    def filter_tasks(self):
        """작업 필터링"""
        search_text = self.search_input.text().lower().strip()
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
                if task_data is None:
                    continue
                total_tasks += 1
                
                # 완료된 작업 필터링
                if not include_completed and task_data.get("checked", False):
                    item.setHidden(True)
                    continue
                    
                # 검색어 매칭 (부분 일치)
                title_match = False
                details_match = False
                
                if search_title:
                    title = task_data.get("title", "").lower()
                    title_match = search_text in title
                    
                if search_details:
                    details = task_data.get("details", "").lower()
                    details_match = search_text in details
                
                # 검색 결과 하이라이트
                if title_match or details_match:
                    item.setHidden(False)
                    matched_tasks += 1
                    # 검색어 하이라이트를 위한 스타일 설정
                    if title_match:
                        title = task_data.get("title", "")
                        item.setText(title)  # 원래 텍스트로 복원
                    if details_match:
                        details = task_data.get("details", "")
                        item.setToolTip(details)  # 툴팁으로 세부 내용 표시
                else:
                    item.setHidden(True)
                    
        # 검색 결과 표시
        if matched_tasks > 0:
            self.search_result_label.setText(
                f"검색 결과: {matched_tasks}/{total_tasks}개 작업")
            self.search_result_label.setStyleSheet(
                "color: #2c3e50; padding: 0 8px;")
        else:
            self.search_result_label.setText("검색 결과 없음")
            self.search_result_label.setStyleSheet(
                "color: #e74c3c; padding: 0 8px;")
            
    def clear_search(self):
        """검색 초기화"""
        self.search_input.clear()
        if hasattr(self, 'search_result_label'):
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
        tasks_by_quadrant = [0, 0, 0, 0]
        completed_by_quadrant = [0, 0, 0, 0]
        
        for i, quad in enumerate(self.quadrant_widgets):
            for item in quad.items:
                total_tasks += 1
                tasks_by_quadrant[i] += 1
                
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
        
        # 닫기 버튼
        close_button = QPushButton("닫기")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        dialog.exec_()
        
    def export_task_report(self):
        """작업 보고서 프린트"""
        if not self.current_project_name:
            QMessageBox.information(self, "보고서", "프로젝트를 선택해주세요.")
            return

        # 프린트 미리보기 다이얼로그 생성
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(lambda p: self.print_report(p))
        preview.exec_()

    def print_report(self, printer):
        """보고서 프린트"""
        painter = QPainter()
        painter.begin(printer)
        
        # 페이지 설정
        page_rect = printer.pageRect()
        margin = 50
        y = margin
        line_height = 20
        
        # 폰트 설정
        title_font = QFont("Arial", 14, QFont.Bold)
        header_font = QFont("Arial", 12, QFont.Bold)
        normal_font = QFont("Arial", 10)
        
        # 제목
        painter.setFont(title_font)
        painter.drawText(margin, int(
            y), f"작업 보고서: {self.current_project_name}")
        y += line_height * 2
        
        # 생성일시
        painter.setFont(normal_font)
        painter.drawText(margin, int(
            y), f"생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        y += line_height * 2
        
        # 사분면별 작업 목록
        quadrant_names = ["중요·긴급", "중요", "긴급", "중요 아님·긴급 아님"]
        for i, (name, quad) in enumerate(zip(quadrant_names, self.quadrant_widgets)):
            # 사분면 제목
            painter.setFont(header_font)
            painter.drawText(margin, int(y), f"[{name}]")
            y += line_height * 1.5
            
            # 작업 목록
            painter.setFont(normal_font)
            if not quad.items:
                painter.drawText(margin + 20, int(y), "작업 없음")
                y += line_height
            else:
                for item in quad.items:
                    # 작업 제목
                    title = item.get("title", "")
                    checked = "✓ " if item.get("checked", False) else "□ "
                    painter.drawText(margin + 20, int(y), checked + title)
                    y += line_height
                    
                    # 세부 내용
                    details = item.get("details", "")
                    if details:
                        painter.drawText(margin + 40, int(y), details)
                        y += line_height
                    
                    # 마감일
                    due_date = item.get("due_date")
                    if due_date:
                        painter.drawText(margin + 40, int(y),
                                         f"마감일: {due_date}")
                        y += line_height
                    
                    y += line_height * 0.5
            
            y += line_height
            
            # 페이지 나누기
            if y > page_rect.height() - margin:
                printer.newPage()
                y = margin
        
        painter.end()

    def toggle_main_toolbar(self):
        """메인 툴바 토글"""
        if hasattr(self, 'toolbar'):
            visible = not self.toolbar.isVisible()
            self.toolbar.setVisible(visible)
        if hasattr(self, 'toggle_toolbar_action'):
            self.toggle_toolbar_action.setChecked(visible)
        # 설정 저장
        settings = QSettings(self.settings_file, QSETTINGS_INIFMT)
        settings.setValue("toolbarVisible", visible)

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
                    self.show_reminder_popup(
                        item["title"], due_dt, overdue=True)
                    quad.notified_set.add((idx, 'overdue'))
                # 알림 시점 체크
                for minutes in item.get("reminders", []):
                    remind_time = due_dt - timedelta(minutes=minutes)
                    key = (idx, minutes)
                    if remind_time <= now < due_dt and key not in quad.notified_set:
                        self.show_reminder_popup(
                            item["title"], due_dt, minutes=minutes)
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
            self.project_status_label.setText(
                f"프로젝트: {self.current_project_name}")
        else:
            self.project_status_label.setText("")

    def open_help_dialog(self):
        from ui.help_dialog import HelpDialog
        dialog = HelpDialog(self)
        dialog.exec_()

# --- 투명도 조절 팝업 위젯 --- #

class OpacityPopup(QWidget):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.main_window = parent_window
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint |
                            Qt.NoDropShadowWindowHint)
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


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("도움말")
        self.setMinimumSize(600, 400)
        
        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        
        # 정보 탭
        self.info_tab = QWidget()
        self.setup_info_tab()
        self.tab_widget.addTab(self.info_tab, "프로그램 정보")
        
        # 라이선스 탭
        self.license_tab = QWidget()
        self.setup_license_tab()
        self.tab_widget.addTab(self.license_tab, "라이선스")
        
        # 도움말 탭
        self.help_tab = QWidget()
        self.setup_help_tab()
        self.tab_widget.addTab(self.help_tab, "사용 방법")
        
        # 메인 레이아웃
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        
        # 닫기 버튼
        close_button = QPushButton("닫기")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
    def setup_info_tab(self):
        outer_layout = QVBoxLayout(self.info_tab)
        # 프로그램 정보 QGroupBox
        info_group_box = QGroupBox("프로그램 정보")
        info_outer_layout = QVBoxLayout(info_group_box)
        info_content = QWidget()
        info_content.setStyleSheet('background: #232323; color: #e0e0e0;')
        form_layout = QFormLayout(info_content)
        form_layout.setSpacing(8)
        form_layout.setContentsMargins(10, 26, 10, 10)
        app_name_label = QLabel("Anti-ADHD")
        font = app_name_label.font()
        font.setPointSize(13)
        font.setBold(True)
        app_name_label.setFont(font)
        app_name_label.setStyleSheet("color: #1565c0;")
        form_layout.addRow(QLabel("이름:"), app_name_label)
        form_layout.addRow(QLabel("버전:"), QLabel("1.0.1"))
        form_layout.addRow(QLabel("개발자:"), QLabel("octaxii"))
        github_link = QLabel(
            "<a href=\"https://github.com/octaxii/Anti-ADHD\">GitHub 저장소</a>")
        github_link.setOpenExternalLinks(True)
        form_layout.addRow(QLabel("GitHub:"), github_link)
        info_content.setLayout(form_layout)
        info_outer_layout.addWidget(info_content)
        outer_layout.addWidget(info_group_box)
        # 라이선스 QGroupBox
        license_group_box = QGroupBox("라이선스")
        license_outer_layout = QVBoxLayout(license_group_box)
        license_content = QWidget()
        license_content.setStyleSheet('background: #232323; color: #e0e0e0;')
        license_layout = QVBoxLayout(license_content)
        license_layout.setContentsMargins(10, 26, 10, 10)
        license_layout.setSpacing(8)
        license_text_edit = QTextEdit()
        license_text_edit.setReadOnly(True)
        license_text_edit.setStyleSheet(
            "font-size: 8.5pt; background: #232323; color: #fff; border-radius: 6px; padding: 6px;")
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
        license_text_edit.setText(mit_license_text.strip())
        license_layout.addSpacing(8)
        license_layout.addWidget(license_text_edit)
        license_layout.addSpacing(8)
        license_content.setLayout(license_layout)
        license_outer_layout.addWidget(license_content)
        outer_layout.addWidget(license_group_box)
        outer_layout.addStretch()
        self.info_tab.setLayout(outer_layout)
        
    def setup_license_tab(self):
        layout = QVBoxLayout(self.license_tab)
        layout.setContentsMargins(16, 16, 16, 16)
        
        license_text_edit = QTextEdit()
        license_text_edit.setReadOnly(True)
        license_text_edit.setStyleSheet(
            "font-size: 8.5pt; background: #f8f9fa; color: #333; border-radius: 6px; padding: 6px;")
        
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
        license_text_edit.setText(mit_license_text.strip())
        layout.addWidget(license_text_edit)
        
    def setup_help_tab(self):
        layout = QVBoxLayout(self.help_tab)
        layout.setContentsMargins(16, 16, 16, 16)
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setStyleSheet(
            "font-size: 9pt; background: #f8f9fa; color: #333; border-radius: 6px; padding: 6px;")
        
        help_content = """
<h2>Anti-ADHD 사용 방법</h2>

<h3>기본 기능</h3>
<ul>
    <li><b>작업 추가:</b> 각 사분면의 + 버튼을 클릭하거나 Ctrl+N을 눌러 새 작업을 추가할 수 있습니다.</li>
    <li><b>작업 편집:</b> 작업을 더블클릭하여 제목, 세부 내용, 마감일 등을 수정할 수 있습니다.</li>
    <li><b>작업 이동:</b> 작업을 드래그하여 다른 사분면으로 이동할 수 있습니다.</li>
    <li><b>작업 완료:</b> 작업을 체크하여 완료 표시를 할 수 있습니다.</li>
</ul>

<h3>프로젝트 관리</h3>
<ul>
    <li><b>프로젝트 생성:</b> 사이드바의 + 버튼을 클릭하여 새 프로젝트를 만들 수 있습니다.</li>
    <li><b>프로젝트 이름 변경:</b> 프로젝트를 우클릭하여 이름을 변경할 수 있습니다.</li>
    <li><b>프로젝트 삭제:</b> 프로젝트를 우클릭하여 삭제할 수 있습니다.</li>
</ul>

<h3>기타 기능</h3>
<ul>
    <li><b>검색:</b> 상단 검색창을 사용하여 작업을 검색할 수 있습니다.</li>
    <li><b>통계:</b> 통계 버튼을 클릭하여 작업 완료율 등을 확인할 수 있습니다.</li>
    <li><b>보고서:</b> 보고서 버튼을 클릭하여 작업 목록을 프린트할 수 있습니다.</li>
    <li><b>테마 변경:</b> 설정에서 다크 모드를 켜고 끌 수 있습니다.</li>
</ul>
"""
        help_text.setHtml(help_content)
        layout.addWidget(help_text)


# --- 테마 상수 ---
THEME = {
    'FONT_FAMILY': "'Segoe UI', 'Noto Sans KR', 'Pretendard', Arial, sans-serif",
    'FONT_SIZE': '9.5pt',
    'LIGHT': {
        'BG': '#f8f9fa',
        'TEXT': '#2c3e50',
        'BORDER': '#e0e0e0',
        'ACCENT': '#3498db',
        'HOVER': '#f0f0f0',
        'SELECTED': '#3498db',
        'DISABLED': '#adb5bd'
    },
    'DARK': {
        'BG': '#1e1e1e',
        'TEXT': '#e0e0e0',
        'BORDER': '#404040',
        'ACCENT': '#0d47a1',
        'HOVER': '#404040',
        'SELECTED': '#0d47a1',
        'DISABLED': '#808080'
    }
}

# --- 스타일시트 템플릿 ---
STYLE_TEMPLATE = {
    'LIGHT': f"""
        QMainWindow {{
            background-color: {THEME['LIGHT']['BG']};
        }}
        QWidget {{
            font-family: {THEME['FONT_FAMILY']};
            color: {THEME['LIGHT']['TEXT']};
        }}
        QListWidget {{
            border: 1px solid {THEME['LIGHT']['BORDER']};
            border-radius: 6px;
            background-color: white;
            padding: 4px;
        }}
        QListWidget::item {{
            padding: 6px;
            border-radius: 4px;
            margin: 2px 0;
        }}
        QListWidget::item:selected {{
            background-color: {THEME['LIGHT']['SELECTED']};
            color: white;
        }}
        QListWidget::item:hover {{
            background-color: {THEME['LIGHT']['HOVER']};
        }}
        QLineEdit {{
            border: 1px solid {THEME['LIGHT']['BORDER']};
            border-radius: 6px;
            padding: 6px;
            background-color: white;
        }}
        QLineEdit:focus {{
            border: 1px solid {THEME['LIGHT']['ACCENT']};
        }}
        QPushButton {{
            background-color: white;
            border: 1px solid {THEME['LIGHT']['BORDER']};
            border-radius: 6px;
            padding: 6px 12px;
            min-height: 24px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {THEME['LIGHT']['HOVER']};
            border-color: {THEME['LIGHT']['ACCENT']};
        }}
        QPushButton:pressed {{
            background-color: #e9ecef;
        }}
        QPushButton:disabled {{
            background-color: {THEME['LIGHT']['BG']};
            color: {THEME['LIGHT']['DISABLED']};
        }}
    """,
    'DARK': f"""
        QMainWindow {{
            background-color: {THEME['DARK']['BG']};
        }}
        QWidget {{
            font-family: {THEME['FONT_FAMILY']};
            color: {THEME['DARK']['TEXT']};
        }}
        QListWidget {{
            border: 1px solid {THEME['DARK']['BORDER']};
            border-radius: 6px;
            background-color: #2d2d2d;
            padding: 4px;
        }}
        QListWidget::item {{
            padding: 6px;
            border-radius: 4px;
            margin: 2px 0;
        }}
        QListWidget::item:selected {{
            background-color: {THEME['DARK']['SELECTED']};
            color: white;
        }}
        QListWidget::item:hover {{
            background-color: {THEME['DARK']['HOVER']};
        }}
        QLineEdit {{
            border: 1px solid {THEME['DARK']['BORDER']};
            border-radius: 6px;
            padding: 6px;
            background-color: #2d2d2d;
            color: {THEME['DARK']['TEXT']};
        }}
        QLineEdit:focus {{
            border: 1px solid {THEME['DARK']['ACCENT']};
        }}
        QPushButton {{
            background-color: #2d2d2d;
            border: 1px solid {THEME['DARK']['BORDER']};
            border-radius: 6px;
            padding: 6px 12px;
            min-height: 24px;
            font-weight: 500;
            color: {THEME['DARK']['TEXT']};
        }}
        QPushButton:hover {{
            background-color: {THEME['DARK']['HOVER']};
            border-color: {THEME['DARK']['ACCENT']};
        }}
        QPushButton:pressed {{
            background-color: #505050;
        }}
        QPushButton:disabled {{
            background-color: #2d2d2d;
            color: {THEME['DARK']['DISABLED']};
        }}
    """
}

# ... existing code ...

def apply_theme(self):
    """현재 테마 적용"""
    if self.dark_mode:
        self.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e1e;
        }
        QWidget {
            font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', 'Arial', sans-serif;
            color: #e0e0e0;
        }
        # 기타 다크 테마 스타일 ... */
        """)
        # --- 다크 모드: 사이드바/프로젝트 리스트/툴바 스타일시트 동적 적용 ---
        if hasattr(self, 'sidebar'):
            self.sidebar.setStyleSheet("background: #232323; border: none;")
        if hasattr(self, 'project_list'):
            self.project_list.setStyleSheet("""
                QListWidget {
                    background: #232323;
                    border: 1px solid #404040;
                    border-radius: 7px;
                    color: #e0e0e0;
                }
                QListWidget::item {
                    background: transparent;
                    color: #e0e0e0;
                }
                QListWidget::item:selected, QListWidget::item:focus {
                    background: #0d47a1;
                    color: #fff;
                }
                QListWidget::item:hover {
                    background: #404040;
                }
            """)
        toolbar_style = """
                QToolBar {
                    background: #232323 !important;
                    border-bottom: 1.5px solid #404040 !important;
                    padding: 0 0 0 0 !important;
                    spacing: 0px !important;
                    min-height: 32px !important;
                    margin: 0 !important;
                }
                QToolButton {
                    padding: 3px 4px !important;
                    border-radius: 5px !important;
                    background: transparent !important;
                    color: #e0e0e0 !important;
                }
                QToolButton:checked {
                    background: #0d47a1 !important;
                }
                QToolButton:hover {
                    background: #404040 !important;
                }
                QToolButton:focus {
                    outline: 2px solid #0d47a1 !important;
                    background: #0d47a1 !important;
                }
            """
    else:
        self.setStyleSheet("""
        QMainWindow {
            background-color: #f8f9fa;
        }
        QWidget {
            font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', 'Arial', sans-serif;
            color: #2c3e50;
        }
        # 기타 라이트 테마 스타일 ... */
        """)
        # --- 라이트 모드: 기존 스타일시트 적용 ---
        if hasattr(self, 'sidebar'):
            self.sidebar.setStyleSheet("")
        if hasattr(self, 'project_list'):
            self.project_list.setStyleSheet(f"""
                QListWidget {{
                    background: #fff;
                    border: 1px solid #e0e0e0;
                    border-radius: 7px;
                    color: #333;
                }}
                QListWidget::item {{
                    background: transparent;
                    color: #333;
                }}
                QListWidget::item:selected, QListWidget::item:focus {{
                    background: #1976d2;
                    color: #fff;
                }}
                QListWidget::item:hover {{
                    background: #f3f6fa;
                }}
            """)
        toolbar_style = f"""
                QToolBar {{
                    background: #fff !important;
                    border-bottom: 1.5px solid #e0e0e0 !important;
                    padding: 0 0 0 0 !important;
                    spacing: 0px !important;
                    min-height: 32px !important;
                    margin: 0 !important;
                }}
                QToolButton {{
                    padding: 3px 4px !important;
                    border-radius: 5px !important;
                    background: transparent !important;
                    color: #1976d2 !important;
                }}
                QToolButton:checked {{
                    background: #e3f0ff !important;
                }}
                QToolButton:hover {{
                    background: #e8e8e8 !important;
                }}
                QToolButton:focus {{
                    outline: 2px solid #1976d2 !important;
                    background: #e3f0ff !important;
                }}
            """
    if hasattr(self, 'toolbar'):
        self.toolbar.setStyleSheet(toolbar_style)
    if hasattr(self, 'search_toolbar'):
        self.search_toolbar.setStyleSheet(toolbar_style)
        # 다크 모드에서 검색 입력창 텍스트와 placeholder 모두 흰색으로
        if hasattr(self, 'search_input'):
            if self.dark_mode:
                self.search_input.setStyleSheet("QLineEdit, QLineEdit::placeholder { color: #fff; }")
            else:
                self.search_input.setStyleSheet("")

# --- 스타일 통합: 졈니 아이브 총괄, 스티브 잡스 컨펌 ---
APP_FONT = "'SF Pro', 'Helvetica Neue', 'Apple SD Gothic Neo', Arial, sans-serif"
APP_BG = "#fff"
APP_TEXT = "#222"
APP_POINT = "#007aff"
APP_SELECT = "#e5e5ea"
APP_WEEKEND = "#ff3b30"

# 메인 윈도우 전체 스타일
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 기본 스타일시트 설정
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QWidget {
            font-family: 'Noto Sans KR', 'Pretendard', Arial, sans-serif;
        }
        QPushButton {
            background-color: #1976d2;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1565c0;
        }
        QPushButton:pressed {
            background-color: #0d47a1;
        }
        QLineEdit {
            border: 1px solid #bdbdbd;
            border-radius: 4px;
            padding: 5px;
        }
        QLineEdit:focus {
            border: 1px solid #1976d2;
        }
        QListWidget {
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            background-color: white;
        }
        QListWidget::item {
            padding: 5px;
        }
        QListWidget::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
    """)
    
    # 다크 모드 설정
    if QSettings().value('dark_mode', False, type=bool):
        app.setStyleSheet(app.styleSheet() + """
            QMainWindow, QWidget {
                background-color: #121212;
                color: #ffffff;
            }
            QPushButton {
                background-color: #1976d2;
                color: white;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #424242;
            }
            QListWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #424242;
            }
            QListWidget::item:selected {
                background-color: #1976d2;
                color: white;
            }
        """)
    
    # 폰트 설정
    font = QFont('Noto Sans KR', 9)
    app.setFont(font)
    
    # 로케일 설정
    QLocale.setDefault(QLocale(QLocale.Korean, QLocale.SouthKorea))
    
    # 메인 윈도우 생성 및 표시
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_()) 

TRANSLATIONS = {
    "ko": {
        "Language": "언어",
        "Korean": "한국어",
        "English": "영어",
        # ... 기타 번역 ...
    },
    "en": {
        "Language": "Language",
        "Korean": "Korean",
        "English": "English",
        # ... 기타 번역 ...
    }
}

def tr(key):
    from PyQt5.QtCore import QSettings
    lang = QSettings("anti_adhd_settings.ini", 1).value("general/language", "ko")
    return TRANSLATIONS.get(lang, {}).get(key, key)