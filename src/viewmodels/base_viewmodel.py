"""
Base ViewModel - MVVM 패턴의 기본 ViewModel
"""
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Any, Dict, Optional


class BaseViewModel(QObject):
    """기본 ViewModel 클래스"""
    
    # 공통 시그널
    property_changed = pyqtSignal(str, object)  # 속성 변경 시그널
    error_occurred = pyqtSignal(str)  # 에러 발생 시그널
    loading_changed = pyqtSignal(bool)  # 로딩 상태 변경 시그널
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._properties: Dict[str, Any] = {}
        self._is_loading = False
    
    def get_property(self, name: str) -> Any:
        """속성 값 가져오기"""
        return self._properties.get(name)
    
    def set_property(self, name: str, value: Any) -> None:
        """속성 값 설정"""
        old_value = self._properties.get(name)
        if old_value != value:
            self._properties[name] = value
            self.property_changed.emit(name, value)
    
    @property
    def is_loading(self) -> bool:
        """로딩 상태"""
        return self._is_loading
    
    @is_loading.setter
    def is_loading(self, value: bool) -> None:
        """로딩 상태 설정"""
        if self._is_loading != value:
            self._is_loading = value
            self.loading_changed.emit(value)
    
    def emit_error(self, message: str) -> None:
        """에러 시그널 발생"""
        self.error_occurred.emit(message)
    
    def reset(self) -> None:
        """ViewModel 초기화"""
        self._properties.clear()
        self._is_loading = False