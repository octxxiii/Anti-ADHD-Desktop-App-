"""
Settings Dialog - 설정 다이얼로그
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QFormLayout, QLabel, QCheckBox, QSpinBox, QComboBox,
    QPushButton, QDialogButtonBox, QGroupBox, QLineEdit,
    QFileDialog, QMessageBox, QSlider, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Dict, Any

from .base_view import BaseView
from ..viewmodels.settings_viewmodel import SettingsViewModel
from ..models.settings_model import AppSettings, Language, Theme
from ..models.translation_service import tr


class SettingsDialog(QDialog, BaseView[SettingsViewModel]):
    """설정 다이얼로그"""
    
    settings_changed = pyqtSignal(dict)  # 변경된 설정들
    
    def __init__(self, settings: AppSettings, parent=None):
        QDialog.__init__(self, parent)
        BaseView.__init__(self)
        
        self.setWindowTitle(tr("Settings"))
        self.setModal(True)
        self.resize(500, 400)
        
        # ViewModel 설정
        viewmodel = SettingsViewModel(settings)
        self.set_viewmodel(viewmodel)
        
        self._setup_ui()
        self._load_settings()
    
    def _setup_ui(self) -> None:
        """UI 설정"""
        layout = QVBoxLayout(self)
        
        # 탭 위젯
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 일반 탭
        self._setup_general_tab()
        
        # 외관 탭
        self._setup_appearance_tab()
        
        # 데이터 탭
        self._setup_data_tab()
        
        # 정보 탭
        self._setup_about_tab()
        
        # 버튼
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply
        )
        button_box.accepted.connect(self._accept_settings)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._apply_settings)
        layout.addWidget(button_box)
    
    def _setup_general_tab(self) -> None:
        """일반 탭 설정"""
        tab = QWidget()
        self.tab_widget.addTab(tab, tr("General"))
        
        layout = QVBoxLayout(tab)
        
        # 언어 설정
        lang_group = QGroupBox(tr("Language"))
        lang_layout = QFormLayout(lang_group)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("한국어", Language.KOREAN.value)
        self.language_combo.addItem("English", Language.ENGLISH.value)
        lang_layout.addRow(tr("Language") + ":", self.language_combo)
        
        layout.addWidget(lang_group)
        
        # 자동 저장 설정
        auto_save_group = QGroupBox(tr("Auto Save"))
        auto_save_layout = QFormLayout(auto_save_group)
        
        self.auto_save_checkbox = QCheckBox(tr("Enable auto save"))
        auto_save_layout.addRow(self.auto_save_checkbox)
        
        self.auto_save_interval_spinbox = QSpinBox()
        self.auto_save_interval_spinbox.setRange(60, 3600)  # 1분 ~ 1시간
        self.auto_save_interval_spinbox.setSuffix(tr("seconds"))
        auto_save_layout.addRow(tr("Save interval") + ":", self.auto_save_interval_spinbox)
        
        layout.addWidget(auto_save_group)
        
        # 업데이트 설정
        update_group = QGroupBox(tr("Check for Updates"))
        update_layout = QFormLayout(update_group)
        
        self.check_updates_checkbox = QCheckBox(tr("Check on startup"))
        update_layout.addRow(self.check_updates_checkbox)
        
        layout.addWidget(update_group)
        
        layout.addStretch()
    
    def _setup_appearance_tab(self) -> None:
        """외관 탭 설정"""
        tab = QWidget()
        self.tab_widget.addTab(tab, tr("Appearance"))
        
        layout = QVBoxLayout(tab)
        
        # 테마 설정
        theme_group = QGroupBox(tr("Theme"))
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItem(tr("System"), Theme.SYSTEM.value)
        self.theme_combo.addItem(tr("Light"), Theme.LIGHT.value)
        self.theme_combo.addItem(tr("Dark"), Theme.DARK.value)
        theme_layout.addRow(tr("Theme") + ":", self.theme_combo)
        
        layout.addWidget(theme_group)
        
        # 창 설정
        window_group = QGroupBox(tr("Window Settings"))
        window_layout = QFormLayout(window_group)
        
        self.always_on_top_checkbox = QCheckBox(tr("Always on top"))
        window_layout.addRow(self.always_on_top_checkbox)
        
        # 투명도 설정
        opacity_layout = QHBoxLayout()
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(20, 100)
        self.opacity_slider.setValue(100)
        self.opacity_label = QLabel("100%")
        self.opacity_slider.valueChanged.connect(
            lambda v: self.opacity_label.setText(f"{v}%")
        )
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_label)
        window_layout.addRow(tr("Opacity") + ":", opacity_layout)
        
        layout.addWidget(window_group)
        
        # UI 요소 표시 설정
        ui_group = QGroupBox(tr("UI Elements"))
        ui_layout = QFormLayout(ui_group)
        
        self.sidebar_checkbox = QCheckBox(tr("Show sidebar"))
        ui_layout.addRow(self.sidebar_checkbox)
        
        self.toolbar_checkbox = QCheckBox(tr("Show toolbar"))
        ui_layout.addRow(self.toolbar_checkbox)
        
        self.statusbar_checkbox = QCheckBox(tr("Show statusbar"))
        ui_layout.addRow(self.statusbar_checkbox)
        
        layout.addWidget(ui_group)
        
        layout.addStretch()
    
    def _setup_data_tab(self) -> None:
        """데이터 탭 설정"""
        tab = QWidget()
        self.tab_widget.addTab(tab, tr("Data"))
        
        layout = QVBoxLayout(tab)
        
        # 데이터 디렉토리 설정
        dir_group = QGroupBox(tr("Data Directory"))
        dir_layout = QVBoxLayout(dir_group)
        
        dir_input_layout = QHBoxLayout()
        self.data_dir_edit = QLineEdit()
        self.data_dir_edit.setReadOnly(True)
        self.browse_btn = QPushButton(tr("Browse") + "...")
        self.browse_btn.clicked.connect(self._browse_data_directory)
        
        dir_input_layout.addWidget(self.data_dir_edit)
        dir_input_layout.addWidget(self.browse_btn)
        dir_layout.addLayout(dir_input_layout)
        
        dir_note = QLabel("※ " + tr("Application restart required after changing data directory"))
        dir_note.setStyleSheet("color: #666; font-size: 11px;")
        dir_layout.addWidget(dir_note)
        
        layout.addWidget(dir_group)
        
        # 데이터 관리
        manage_group = QGroupBox(tr("Data Management"))
        manage_layout = QVBoxLayout(manage_group)
        
        backup_btn = QPushButton(tr("Backup Data") + "...")
        backup_btn.clicked.connect(self._backup_data)
        manage_layout.addWidget(backup_btn)
        
        restore_btn = QPushButton(tr("Restore Data") + "...")
        restore_btn.clicked.connect(self._restore_data)
        manage_layout.addWidget(restore_btn)
        
        reset_btn = QPushButton(tr("Reset Data") + "...")
        reset_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
        reset_btn.clicked.connect(self._reset_data)
        manage_layout.addWidget(reset_btn)
        
        layout.addWidget(manage_group)
        
        layout.addStretch()
    
    def _setup_about_tab(self) -> None:
        """정보 탭 설정"""
        tab = QWidget()
        self.tab_widget.addTab(tab, tr("About"))
        
        layout = QVBoxLayout(tab)
        
        # 프로그램 정보
        info_group = QGroupBox(tr("Program Information"))
        info_layout = QFormLayout(info_group)
        
        app_name = QLabel("Anti-ADHD")
        app_name.setFont(QFont("", 14, QFont.Weight.Bold))
        info_layout.addRow(tr("Name") + ":", app_name)
        
        info_layout.addRow(tr("Version") + ":", QLabel("2.0.0"))
        info_layout.addRow(tr("Developer") + ":", QLabel("octaxii"))
        
        github_label = QLabel(f'<a href="https://github.com/octaxii/Anti-ADHD">{tr("GitHub Repository")}</a>')
        github_label.setOpenExternalLinks(True)
        info_layout.addRow("GitHub:", github_label)
        
        layout.addWidget(info_group)
        
        # 라이선스
        license_group = QGroupBox(tr("License"))
        license_layout = QVBoxLayout(license_group)
        
        license_text = QTextEdit()
        license_text.setReadOnly(True)
        license_text.setMaximumHeight(150)
        license_text.setText("""MIT License

Copyright (c) 2024 octaxii

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.""")
        
        license_layout.addWidget(license_text)
        layout.addWidget(license_group)
        
        layout.addStretch()
    
    def _load_settings(self) -> None:
        """설정 로드"""
        if not self.viewmodel:
            return
        
        # 언어
        lang_index = self.language_combo.findData(self.viewmodel.get_language())
        if lang_index >= 0:
            self.language_combo.setCurrentIndex(lang_index)
        
        # 테마
        theme_index = self.theme_combo.findData(self.viewmodel.get_theme())
        if theme_index >= 0:
            self.theme_combo.setCurrentIndex(theme_index)
        
        # 자동 저장
        self.auto_save_checkbox.setChecked(self.viewmodel.get_auto_save())
        self.auto_save_interval_spinbox.setValue(self.viewmodel.get_auto_save_interval())
        
        # 업데이트 확인
        self.check_updates_checkbox.setChecked(self.viewmodel.get_check_updates())
        
        # 창 설정
        self.always_on_top_checkbox.setChecked(self.viewmodel.get_always_on_top())
        opacity_percent = int(self.viewmodel.get_opacity() * 100)
        self.opacity_slider.setValue(opacity_percent)
        
        # UI 요소
        self.sidebar_checkbox.setChecked(self.viewmodel.get_sidebar_visible())
        self.toolbar_checkbox.setChecked(self.viewmodel.get_toolbar_visible())
        self.statusbar_checkbox.setChecked(self.viewmodel.get_statusbar_visible())
        
        # 데이터 디렉토리
        self.data_dir_edit.setText(self.viewmodel.get_data_directory())
    
    def _browse_data_directory(self) -> None:
        """데이터 디렉토리 찾아보기"""
        directory = QFileDialog.getExistingDirectory(
            self, "데이터 저장 폴더 선택", self.data_dir_edit.text()
        )
        if directory:
            self.data_dir_edit.setText(directory)
    
    def _backup_data(self) -> None:
        """데이터 백업"""
        # TODO: 백업 기능 구현
        QMessageBox.information(self, "백업", "백업 기능은 메인 윈도우에서 사용하세요.")
    
    def _restore_data(self) -> None:
        """데이터 복원"""
        # TODO: 복원 기능 구현
        QMessageBox.information(self, "복원", "복원 기능은 메인 윈도우에서 사용하세요.")
    
    def _reset_data(self) -> None:
        """데이터 초기화"""
        # TODO: 초기화 기능 구현
        QMessageBox.information(self, "초기화", "초기화 기능은 메인 윈도우에서 사용하세요.")
    
    def _apply_settings(self) -> None:
        """설정 적용"""
        try:
            # 언어 변경 시 번역 서비스 업데이트
            from ..models.translation_service import set_language, Language
            selected_language = self.language_combo.currentData()
            if selected_language == "ko":
                set_language(Language.KOREAN)
            elif selected_language == "en":
                set_language(Language.ENGLISH)
            
            # 설정 변경사항을 딕셔너리로 수집
            changes = {
                'language': selected_language,
                'theme': self.theme_combo.currentData(),
                'auto_save': self.auto_save_checkbox.isChecked(),
                'auto_save_interval': self.auto_save_interval_spinbox.value(),
                'check_updates': self.check_updates_checkbox.isChecked(),
                'sidebar_visible': self.sidebar_checkbox.isChecked(),
                'toolbar_visible': self.toolbar_checkbox.isChecked(),
                'statusbar_visible': self.statusbar_checkbox.isChecked(),
                'data_directory': self.data_dir_edit.text(),
                'window_settings': {
                    'always_on_top': self.always_on_top_checkbox.isChecked(),
                    'opacity': self.opacity_slider.value() / 100.0
                }
            }
            
            # 시그널 발생
            self.settings_changed.emit(changes)
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "오류", f"설정 적용 중 오류가 발생했습니다:\n{str(e)}")
    
    def _accept_settings(self) -> None:
        """설정 확인"""
        self._apply_settings()
        self.accept()
    
    def get_changes(self) -> Dict[str, Any]:
        """변경된 설정 반환"""
        if not self.viewmodel:
            return {}
        
        return self.viewmodel.settings.to_dict()