"""
Settings Model - 애플리케이션 설정 모델
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import os
from pathlib import Path


class Language(Enum):
    """지원 언어"""
    KOREAN = "ko"
    ENGLISH = "en"


class Theme(Enum):
    """테마"""
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass
class WindowSettings:
    """창 설정"""
    width: int = 800
    height: int = 600
    x: int = 100
    y: int = 100
    always_on_top: bool = False
    opacity: float = 1.0
    maximized: bool = False
    
    def to_dict(self) -> dict:
        return {
            'width': self.width,
            'height': self.height,
            'x': self.x,
            'y': self.y,
            'always_on_top': self.always_on_top,
            'opacity': self.opacity,
            'maximized': self.maximized
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WindowSettings':
        return cls(
            width=data.get('width', 800),
            height=data.get('height', 600),
            x=data.get('x', 100),
            y=data.get('y', 100),
            always_on_top=data.get('always_on_top', False),
            opacity=data.get('opacity', 1.0),
            maximized=data.get('maximized', False)
        )


@dataclass
class AppSettings:
    """애플리케이션 설정 모델"""
    language: Language = Language.KOREAN
    theme: Theme = Theme.SYSTEM
    auto_save: bool = True
    auto_save_interval: int = 300  # 5분 (초 단위)
    check_updates: bool = True
    data_directory: str = field(default_factory=lambda: str(Path.home() / "AppData" / "Local" / "Anti-ADHD" / "data"))
    window_settings: WindowSettings = field(default_factory=WindowSettings)
    sidebar_visible: bool = True
    toolbar_visible: bool = True
    statusbar_visible: bool = True
    
    def __post_init__(self):
        """초기화 후 처리"""
        # 데이터 디렉토리가 존재하지 않으면 생성
        os.makedirs(self.data_directory, exist_ok=True)
    
    def update_language(self, language: Language) -> None:
        """언어 설정 업데이트"""
        self.language = language
    
    def update_theme(self, theme: Theme) -> None:
        """테마 설정 업데이트"""
        self.theme = theme
    
    def update_data_directory(self, directory: str) -> None:
        """데이터 디렉토리 업데이트"""
        if os.path.exists(directory) or self._create_directory(directory):
            self.data_directory = directory
        else:
            raise ValueError(f"Cannot create or access directory: {directory}")
    
    def _create_directory(self, directory: str) -> bool:
        """디렉토리 생성 시도"""
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except (OSError, PermissionError):
            return False
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            'language': self.language.value,
            'theme': self.theme.value,
            'auto_save': self.auto_save,
            'auto_save_interval': self.auto_save_interval,
            'check_updates': self.check_updates,
            'data_directory': self.data_directory,
            'window_settings': self.window_settings.to_dict(),
            'sidebar_visible': self.sidebar_visible,
            'toolbar_visible': self.toolbar_visible,
            'statusbar_visible': self.statusbar_visible
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AppSettings':
        """딕셔너리에서 AppSettings 객체 생성"""
        return cls(
            language=Language(data.get('language', Language.KOREAN.value)),
            theme=Theme(data.get('theme', Theme.SYSTEM.value)),
            auto_save=data.get('auto_save', True),
            auto_save_interval=data.get('auto_save_interval', 300),
            check_updates=data.get('check_updates', True),
            data_directory=data.get('data_directory', str(Path.home() / "AppData" / "Local" / "Anti-ADHD" / "data")),
            window_settings=WindowSettings.from_dict(data.get('window_settings', {})),
            sidebar_visible=data.get('sidebar_visible', True),
            toolbar_visible=data.get('toolbar_visible', True),
            statusbar_visible=data.get('statusbar_visible', True)
        )