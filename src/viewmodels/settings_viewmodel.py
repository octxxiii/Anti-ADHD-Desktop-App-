"""
Settings ViewModel - 설정 다이얼로그 ViewModel
"""
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from .base_viewmodel import BaseViewModel
from ..models.settings_model import AppSettings, Language, Theme


class SettingsViewModel(BaseViewModel):
    """설정 ViewModel"""
    
    # 시그널
    language_changed = pyqtSignal(str)
    theme_changed = pyqtSignal(str)
    data_directory_changed = pyqtSignal(str)
    
    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)
        self._settings = settings
        self._original_settings = self._copy_settings(settings)
        
        # 초기 속성 설정
        self._update_properties()
    
    @property
    def settings(self) -> AppSettings:
        """현재 설정"""
        return self._settings
    
    def get_language(self) -> str:
        """현재 언어"""
        return self._settings.language.value
    
    def set_language(self, language: str) -> None:
        """언어 설정"""
        try:
            new_language = Language(language)
            if self._settings.language != new_language:
                self._settings.language = new_language
                self.set_property('language', language)
                self.language_changed.emit(language)
        except ValueError:
            self.emit_error(f"지원하지 않는 언어입니다: {language}")
    
    def get_theme(self) -> str:
        """현재 테마"""
        return self._settings.theme.value
    
    def set_theme(self, theme: str) -> None:
        """테마 설정"""
        try:
            new_theme = Theme(theme)
            if self._settings.theme != new_theme:
                self._settings.theme = new_theme
                self.set_property('theme', theme)
                self.theme_changed.emit(theme)
        except ValueError:
            self.emit_error(f"지원하지 않는 테마입니다: {theme}")
    
    def get_auto_save(self) -> bool:
        """자동 저장 설정"""
        return self._settings.auto_save
    
    def set_auto_save(self, enabled: bool) -> None:
        """자동 저장 설정"""
        if self._settings.auto_save != enabled:
            self._settings.auto_save = enabled
            self.set_property('auto_save', enabled)
    
    def get_auto_save_interval(self) -> int:
        """자동 저장 간격 (초)"""
        return self._settings.auto_save_interval
    
    def set_auto_save_interval(self, interval: int) -> None:
        """자동 저장 간격 설정"""
        if interval < 60:  # 최소 1분
            self.emit_error("자동 저장 간격은 최소 60초입니다.")
            return
        
        if self._settings.auto_save_interval != interval:
            self._settings.auto_save_interval = interval
            self.set_property('auto_save_interval', interval)
    
    def get_check_updates(self) -> bool:
        """업데이트 확인 설정"""
        return self._settings.check_updates
    
    def set_check_updates(self, enabled: bool) -> None:
        """업데이트 확인 설정"""
        if self._settings.check_updates != enabled:
            self._settings.check_updates = enabled
            self.set_property('check_updates', enabled)
    
    def get_data_directory(self) -> str:
        """데이터 디렉토리"""
        return self._settings.data_directory
    
    def set_data_directory(self, directory: str) -> None:
        """데이터 디렉토리 설정"""
        try:
            if self._settings.data_directory != directory:
                self._settings.update_data_directory(directory)
                self.set_property('data_directory', directory)
                self.data_directory_changed.emit(directory)
        except ValueError as e:
            self.emit_error(str(e))
    
    def get_window_settings(self) -> Dict[str, Any]:
        """창 설정"""
        return self._settings.window_settings.to_dict()
    
    def set_window_setting(self, key: str, value: Any) -> None:
        """창 설정 업데이트"""
        if hasattr(self._settings.window_settings, key):
            setattr(self._settings.window_settings, key, value)
            self.set_property(f'window_{key}', value)
    
    def get_always_on_top(self) -> bool:
        """항상 위 설정"""
        return self._settings.window_settings.always_on_top
    
    def set_always_on_top(self, enabled: bool) -> None:
        """항상 위 설정"""
        if self._settings.window_settings.always_on_top != enabled:
            self._settings.window_settings.always_on_top = enabled
            self.set_property('always_on_top', enabled)
    
    def get_opacity(self) -> float:
        """창 투명도"""
        return self._settings.window_settings.opacity
    
    def set_opacity(self, opacity: float) -> None:
        """창 투명도 설정"""
        opacity = max(0.2, min(1.0, opacity))  # 0.2 ~ 1.0 범위
        if self._settings.window_settings.opacity != opacity:
            self._settings.window_settings.opacity = opacity
            self.set_property('opacity', opacity)
    
    def get_sidebar_visible(self) -> bool:
        """사이드바 표시 설정"""
        return self._settings.sidebar_visible
    
    def set_sidebar_visible(self, visible: bool) -> None:
        """사이드바 표시 설정"""
        if self._settings.sidebar_visible != visible:
            self._settings.sidebar_visible = visible
            self.set_property('sidebar_visible', visible)
    
    def get_toolbar_visible(self) -> bool:
        """툴바 표시 설정"""
        return self._settings.toolbar_visible
    
    def set_toolbar_visible(self, visible: bool) -> None:
        """툴바 표시 설정"""
        if self._settings.toolbar_visible != visible:
            self._settings.toolbar_visible = visible
            self.set_property('toolbar_visible', visible)
    
    def get_statusbar_visible(self) -> bool:
        """상태바 표시 설정"""
        return self._settings.statusbar_visible
    
    def set_statusbar_visible(self, visible: bool) -> None:
        """상태바 표시 설정"""
        if self._settings.statusbar_visible != visible:
            self._settings.statusbar_visible = visible
            self.set_property('statusbar_visible', visible)
    
    def has_changes(self) -> bool:
        """설정 변경 여부 확인"""
        return self._settings.to_dict() != self._original_settings.to_dict()
    
    def apply_changes(self) -> None:
        """변경사항 적용"""
        self._original_settings = self._copy_settings(self._settings)
    
    def cancel_changes(self) -> None:
        """변경사항 취소"""
        self._settings = self._copy_settings(self._original_settings)
        self._update_properties()
    
    def reset_to_defaults(self) -> None:
        """기본값으로 재설정"""
        default_settings = AppSettings()
        
        # 데이터 디렉토리는 유지
        default_settings.data_directory = self._settings.data_directory
        
        self._settings = default_settings
        self._update_properties()
    
    def _copy_settings(self, settings: AppSettings) -> AppSettings:
        """설정 복사"""
        return AppSettings.from_dict(settings.to_dict())
    
    def _update_properties(self) -> None:
        """속성 업데이트"""
        self.set_property('language', self._settings.language.value)
        self.set_property('theme', self._settings.theme.value)
        self.set_property('auto_save', self._settings.auto_save)
        self.set_property('auto_save_interval', self._settings.auto_save_interval)
        self.set_property('check_updates', self._settings.check_updates)
        self.set_property('data_directory', self._settings.data_directory)
        self.set_property('always_on_top', self._settings.window_settings.always_on_top)
        self.set_property('opacity', self._settings.window_settings.opacity)
        self.set_property('sidebar_visible', self._settings.sidebar_visible)
        self.set_property('toolbar_visible', self._settings.toolbar_visible)
        self.set_property('statusbar_visible', self._settings.statusbar_visible)