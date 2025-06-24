from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QComboBox, QPushButton, QCheckBox, QGroupBox,
    QRadioButton, QButtonGroup, QFormLayout
)
from PyQt5.QtCore import Qt
from model.translation_model import TranslationModel

class SettingsDialog(QDialog):
    """설정 다이얼로그"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.translation = TranslationModel()
        self.setWindowTitle(self.translation.tr("Settings"))
        self.resize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)

        # 탭 위젯
        self.tab_widget = QTabWidget()
        
        # 일반 설정 탭
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        
        # 언어 설정
        self.language_combo = QComboBox()
        self.language_combo.addItem(self.translation.tr("Korean"), "ko")
        self.language_combo.addItem(self.translation.tr("English"), "en")
        general_layout.addRow(self.translation.tr("Language:"), self.language_combo)
        
        # 테마 설정
        self.theme_combo = QComboBox()
        self.theme_combo.addItem(self.translation.tr("System"), "system")
        self.theme_combo.addItem(self.translation.tr("Light"), "light")
        self.theme_combo.addItem(self.translation.tr("Dark"), "dark")
        general_layout.addRow(self.translation.tr("Theme:"), self.theme_combo)
        
        # 자동 저장 설정
        self.auto_save_check = QCheckBox(self.translation.tr("Auto Save"))
        general_layout.addRow("", self.auto_save_check)
        
        # 알림 설정
        self.notification_check = QCheckBox(self.translation.tr("Enable Notifications"))
        general_layout.addRow("", self.notification_check)
        
        self.tab_widget.addTab(general_tab, self.translation.tr("General"))
        
        # 단축키 설정 탭
        shortcut_tab = QWidget()
        shortcut_layout = QFormLayout(shortcut_tab)
        
        # 단축키 설정 항목들
        shortcut_items = [
            ("New Project", "Ctrl+N"),
            ("Import Project", "Ctrl+I"),
            ("Save Project", "Ctrl+S"),
            ("Add Task", "Ctrl+T"),
            ("Edit Task", "Ctrl+E"),
            ("Delete Task", "Delete")
        ]
        
        for action, shortcut in shortcut_items:
            label = QLabel(self.translation.tr(action))
            shortcut_label = QLabel(shortcut)
            shortcut_layout.addRow(label, shortcut_label)
        
        self.tab_widget.addTab(shortcut_tab, self.translation.tr("Shortcuts"))
        
        # 정보 탭
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        
        # 버전 정보
        version_label = QLabel("Anti-ADHD (Eisenhower Matrix)\nVersion 1.0")
        version_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(version_label)
        
        # 라이선스 정보
        license_label = QLabel("MIT License")
        license_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(license_label)
        
        self.tab_widget.addTab(about_tab, self.translation.tr("About"))
        
        layout.addWidget(self.tab_widget)
        
        # 버튼
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton(self.translation.tr("OK"))
        self.cancel_button = QPushButton(self.translation.tr("Cancel"))
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # 시그널 연결
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)

    def on_language_changed(self, index):
        """언어 변경 시 처리"""
        # 언어 설정 즉시 적용
        language_code = self.language_combo.currentData()
        if language_code:
            self.translation.set_language(language_code)
        self.update_translations()
        
        # 부모 윈도우에 언어 변경 알림
        if self.parent():
            if hasattr(self.parent(), 'update_ui_language'):
                self.parent().update_ui_language()

    def update_translations(self):
        """언어 변경 시 UI 업데이트"""
        self.setWindowTitle(self.translation.tr("Settings"))
        
        # 탭 이름 업데이트
        self.tab_widget.setTabText(0, self.translation.tr("General"))
        self.tab_widget.setTabText(1, self.translation.tr("Shortcuts"))
        self.tab_widget.setTabText(2, self.translation.tr("About"))
        
        # 일반 설정 탭 업데이트
        general_tab = self.tab_widget.widget(0)
        form_layout = general_tab.layout()
        
        # 언어 설정
        form_layout.itemAt(0, QFormLayout.LabelRole).widget().setText(self.translation.tr("Language:"))
        self.language_combo.setItemText(0, self.translation.tr("Korean"))
        self.language_combo.setItemText(1, self.translation.tr("English"))
        
        # 테마 설정
        form_layout.itemAt(2, QFormLayout.LabelRole).widget().setText(self.translation.tr("Theme:"))
        self.theme_combo.setItemText(0, self.translation.tr("System"))
        self.theme_combo.setItemText(1, self.translation.tr("Light"))
        self.theme_combo.setItemText(2, self.translation.tr("Dark"))
        
        # 자동 저장 설정
        self.auto_save_check.setText(self.translation.tr("Auto Save"))
        
        # 알림 설정
        self.notification_check.setText(self.translation.tr("Enable Notifications"))
        
        # 단축키 탭 업데이트
        shortcut_tab = self.tab_widget.widget(1)
        form_layout = shortcut_tab.layout()
        
        # 단축키 항목 업데이트
        shortcut_items = [
            ("New Project", "Ctrl+N"),
            ("Import Project", "Ctrl+I"),
            ("Save Project", "Ctrl+S"),
            ("Add Task", "Ctrl+T"),
            ("Edit Task", "Ctrl+E"),
            ("Delete Task", "Delete")
        ]
        
        for i, (action, _) in enumerate(shortcut_items):
            form_layout.itemAt(i, QFormLayout.LabelRole).widget().setText(self.translation.tr(action))
        
        # 버튼 텍스트 업데이트
        self.ok_button.setText(self.translation.tr("OK"))
        self.cancel_button.setText(self.translation.tr("Cancel")) 