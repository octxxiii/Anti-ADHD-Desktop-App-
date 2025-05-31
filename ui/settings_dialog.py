from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit, QGroupBox, QCheckBox, QSlider, QStyle, QFormLayout, QInputDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import QSettings

class SettingsDialog(QDialog):
    def __init__(self, current_data_dir, settings_file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("애플리케이션 설정")
        self.setModal(True)
        self.main_window_ref = parent
        self.current_data_dir = current_data_dir
        self.new_data_dir = current_data_dir
        self.settings_file_path = settings_file_path
        self.settings = QSettings(self.settings_file_path, 1)
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(16, 16, 16, 16)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabBar::tab { min-width: 80px; min-height: 24px; font-size: 10.5pt; padding: 4px 10px; } QTabBar::tab:selected { font-weight: bold; color: #1565c0; }")
        main_layout.addWidget(self.tab_widget)
        self.general_tab = QWidget()
        self.tab_widget.addTab(self.general_tab, "일반")
        self.setup_general_tab()
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
    def browse_data_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "데이터 저장 폴더 선택", self.new_data_dir)
        if directory and directory != self.current_data_dir:
            self.new_data_dir = directory
            self.data_dir_edit.setText(self.new_data_dir)
    def _on_auto_save_changed(self, state):
        self.settings.setValue("general/autoSaveEnabled", self.auto_save_checkbox.isChecked())
        self.settings.sync()
        if self.main_window_ref:
            self.main_window_ref.auto_save_enabled = self.auto_save_checkbox.isChecked()
    def _on_check_updates_changed(self, state):
        self.settings.setValue("general/checkUpdatesOnStart", self.check_updates_checkbox.isChecked())
        self.settings.sync()
    def accept_settings(self):
        if self.new_data_dir != self.current_data_dir:
            self.settings.setValue("dataDir", self.new_data_dir)
            self.current_data_dir = self.new_data_dir
            if self.main_window_ref:
                 pass
            QMessageBox.information(self, "설정 변경",
                                    f"데이터 저장 경로가 다음으로 설정되었습니다:\n'{self.new_data_dir}'\n\n애플리케이션을 재시작해야 변경 사항이 완전히 적용됩니다.")
        self.accept()
    def perform_update_check(self):
        QMessageBox.information(self, "업데이트 확인", "업데이트 확인 기능은 아직 구현되지 않았습니다.")
    def backup_data(self):
        pass
    def restore_data(self):
        pass
    def reset_data(self):
        pass 