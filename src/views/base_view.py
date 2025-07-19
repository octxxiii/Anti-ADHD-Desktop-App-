"""
Base View - MVVM 패턴의 기본 View
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject
from typing import Optional, TypeVar, Generic

from ..viewmodels.base_viewmodel import BaseViewModel

T = TypeVar('T', bound=BaseViewModel)


class BaseView(QWidget, Generic[T]):
    """기본 View 클래스"""
    
    def __init__(self, viewmodel: Optional[T] = None, parent=None):
        super().__init__(parent)
        self._viewmodel: Optional[T] = None
        
        if viewmodel:
            self.set_viewmodel(viewmodel)
    
    @property
    def viewmodel(self) -> Optional[T]:
        """ViewModel 반환"""
        return self._viewmodel
    
    def set_viewmodel(self, viewmodel: T) -> None:
        """ViewModel 설정"""
        # 기존 연결 해제
        if self._viewmodel:
            self._disconnect_viewmodel()
        
        self._viewmodel = viewmodel
        
        # 새 연결 설정
        if self._viewmodel:
            self._connect_viewmodel()
            self._update_from_viewmodel()
    
    def _connect_viewmodel(self) -> None:
        """ViewModel 시그널 연결"""
        if self._viewmodel:
            self._viewmodel.property_changed.connect(self._on_property_changed)
            self._viewmodel.error_occurred.connect(self._on_error_occurred)
            self._viewmodel.loading_changed.connect(self._on_loading_changed)
    
    def _disconnect_viewmodel(self) -> None:
        """ViewModel 시그널 연결 해제"""
        if self._viewmodel:
            self._viewmodel.property_changed.disconnect()
            self._viewmodel.error_occurred.disconnect()
            self._viewmodel.loading_changed.disconnect()
    
    def _update_from_viewmodel(self) -> None:
        """ViewModel에서 UI 업데이트"""
        # 서브클래스에서 구현
        pass
    
    def _on_property_changed(self, property_name: str, value) -> None:
        """속성 변경 처리"""
        # 서브클래스에서 구현
        pass
    
    def _on_error_occurred(self, message: str) -> None:
        """에러 발생 처리"""
        # 기본적으로 콘솔에 출력
        print(f"Error: {message}")
    
    def _on_loading_changed(self, is_loading: bool) -> None:
        """로딩 상태 변경 처리"""
        # 서브클래스에서 구현
        pass