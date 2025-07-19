"""
Main ViewModel - 메인 윈도우 ViewModel
"""
from PyQt6.QtCore import pyqtSignal, QTimer
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base_viewmodel import BaseViewModel
from ..models.task_model import Task, Quadrant
from ..models.project_model import Project
from ..models.settings_model import AppSettings
from ..models.data_service import DataService


class MainViewModel(BaseViewModel):
    """메인 윈도우 ViewModel"""
    
    # 시그널 정의
    projects_changed = pyqtSignal()
    current_project_changed = pyqtSignal()
    settings_changed = pyqtSignal()
    auto_save_triggered = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 데이터 서비스 초기화
        self._settings = AppSettings()
        self._data_service = DataService(self._settings.data_directory)
        
        # 상태 변수
        self._projects: List[Project] = []
        self._current_project: Optional[Project] = None
        
        # 자동 저장 타이머
        self._auto_save_timer = QTimer()
        self._auto_save_timer.timeout.connect(self._auto_save)
        
        # 초기화
        self._load_settings()
        self._load_projects()
        self._setup_auto_save()
    
    # Properties
    @property
    def projects(self) -> List[Project]:
        """프로젝트 목록"""
        return self._projects
    
    @property
    def current_project(self) -> Optional[Project]:
        """현재 프로젝트"""
        return self._current_project
    
    @property
    def settings(self) -> AppSettings:
        """애플리케이션 설정"""
        return self._settings
    
    # Project Management
    def create_project(self, name: str, description: str = "") -> bool:
        """새 프로젝트 생성"""
        try:
            self.is_loading = True
            
            # 중복 이름 확인
            if any(p.name == name for p in self._projects):
                self.emit_error(f"프로젝트 이름 '{name}'이 이미 존재합니다.")
                return False
            
            # 새 프로젝트 생성
            project = Project(name=name, description=description)
            
            # 저장
            if self._data_service.save_project(project):
                self._projects.append(project)
                self.set_current_project(project)
                # 프로젝트 순서 저장
                self._save_project_order()
                self.projects_changed.emit()
                return True
            else:
                self.emit_error("프로젝트 저장에 실패했습니다.")
                return False
                
        except Exception as e:
            self.emit_error(f"프로젝트 생성 중 오류: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    def delete_project(self, project_id: str) -> bool:
        """프로젝트 삭제"""
        try:
            self.is_loading = True
            
            # 프로젝트 찾기
            project = next((p for p in self._projects if p.id == project_id), None)
            if not project:
                self.emit_error("삭제할 프로젝트를 찾을 수 없습니다.")
                return False
            
            # 데이터 삭제
            if self._data_service.delete_project(project_id):
                self._projects.remove(project)
                
                # 현재 프로젝트가 삭제된 경우
                if self._current_project and self._current_project.id == project_id:
                    self._current_project = self._projects[0] if self._projects else None
                    self.current_project_changed.emit()
                
                # 프로젝트 순서 저장
                self._save_project_order()
                self.projects_changed.emit()
                return True
            else:
                self.emit_error("프로젝트 삭제에 실패했습니다.")
                return False
                
        except Exception as e:
            self.emit_error(f"프로젝트 삭제 중 오류: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    def rename_project(self, project_id: str, new_name: str) -> bool:
        """프로젝트 이름 변경"""
        try:
            # 중복 이름 확인
            if any(p.name == new_name and p.id != project_id for p in self._projects):
                self.emit_error(f"프로젝트 이름 '{new_name}'이 이미 존재합니다.")
                return False
            
            # 프로젝트 찾기
            project = next((p for p in self._projects if p.id == project_id), None)
            if not project:
                self.emit_error("프로젝트를 찾을 수 없습니다.")
                return False
            
            # 이름 변경
            project.update_name(new_name)
            
            # 저장
            if self._data_service.save_project(project):
                self.projects_changed.emit()
                if self._current_project and self._current_project.id == project_id:
                    self.current_project_changed.emit()
                return True
            else:
                self.emit_error("프로젝트 저장에 실패했습니다.")
                return False
                
        except Exception as e:
            self.emit_error(f"프로젝트 이름 변경 중 오류: {str(e)}")
            return False
    
    def set_current_project(self, project: Optional[Project]) -> None:
        """현재 프로젝트 설정"""
        if self._current_project != project:
            self._current_project = project
            self.current_project_changed.emit()
    
    def set_current_project_by_id(self, project_id: str) -> bool:
        """ID로 현재 프로젝트 설정"""
        project = next((p for p in self._projects if p.id == project_id), None)
        if project:
            self.set_current_project(project)
            return True
        return False
    
    def move_project_up(self, project_id: str) -> bool:
        """프로젝트 위로 이동"""
        try:
            # 프로젝트 인덱스 찾기
            project_index = next((i for i, p in enumerate(self._projects) if p.id == project_id), -1)
            
            if project_index <= 0:
                return False  # 이미 맨 위이거나 찾을 수 없음
            
            # 프로젝트 순서 변경
            self._projects[project_index], self._projects[project_index - 1] = \
                self._projects[project_index - 1], self._projects[project_index]
            
            # 프로젝트 순서 정보 저장
            self._save_project_order()
            
            self.projects_changed.emit()
            return True
            
        except Exception as e:
            self.emit_error(f"프로젝트 이동 중 오류: {str(e)}")
            return False
    
    def move_project_down(self, project_id: str) -> bool:
        """프로젝트 아래로 이동"""
        try:
            # 프로젝트 인덱스 찾기
            project_index = next((i for i, p in enumerate(self._projects) if p.id == project_id), -1)
            
            if project_index < 0 or project_index >= len(self._projects) - 1:
                return False  # 이미 맨 아래이거나 찾을 수 없음
            
            # 프로젝트 순서 변경
            self._projects[project_index], self._projects[project_index + 1] = \
                self._projects[project_index + 1], self._projects[project_index]
            
            # 프로젝트 순서 정보 저장
            self._save_project_order()
            
            self.projects_changed.emit()
            return True
            
        except Exception as e:
            self.emit_error(f"프로젝트 이동 중 오류: {str(e)}")
            return False
    
    # Task Management
    def add_task(self, title: str, quadrant: Quadrant, description: str = "") -> bool:
        """할 일 추가"""
        if not self._current_project:
            self.emit_error("프로젝트를 먼저 선택해주세요.")
            return False
        
        try:
            task = Task(title=title, description=description, quadrant=quadrant)
            self._current_project.add_task(task)
            
            if self._data_service.save_project(self._current_project):
                self.current_project_changed.emit()
                return True
            else:
                self.emit_error("할 일 저장에 실패했습니다.")
                return False
                
        except Exception as e:
            self.emit_error(f"할 일 추가 중 오류: {str(e)}")
            return False
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """할 일 업데이트"""
        if not self._current_project:
            return False
        
        try:
            task = self._current_project.get_task(task_id)
            if not task:
                self.emit_error("할 일을 찾을 수 없습니다.")
                return False
            
            # 속성 업데이트
            if 'title' in kwargs:
                task.update_title(kwargs['title'])
            if 'description' in kwargs:
                task.update_description(kwargs['description'])
            if 'quadrant' in kwargs:
                task.move_to_quadrant(kwargs['quadrant'])
            if 'priority' in kwargs:
                task.set_priority(kwargs['priority'])
            if 'due_date' in kwargs:
                task.set_due_date(kwargs['due_date'])
            if 'reminder_time' in kwargs:
                task.reminder_time = kwargs['reminder_time']
                task.updated_at = datetime.now()
            if 'is_completed' in kwargs:
                if kwargs['is_completed']:
                    task.mark_completed()
                else:
                    task.mark_incomplete()
            
            if self._data_service.save_project(self._current_project):
                self.current_project_changed.emit()
                return True
            else:
                self.emit_error("할 일 저장에 실패했습니다.")
                return False
                
        except Exception as e:
            self.emit_error(f"할 일 업데이트 중 오류: {str(e)}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """할 일 삭제"""
        if not self._current_project:
            return False
        
        try:
            if self._current_project.remove_task(task_id):
                if self._data_service.save_project(self._current_project):
                    self.current_project_changed.emit()
                    return True
                else:
                    self.emit_error("할 일 저장에 실패했습니다.")
                    return False
            else:
                self.emit_error("삭제할 할 일을 찾을 수 없습니다.")
                return False
                
        except Exception as e:
            self.emit_error(f"할 일 삭제 중 오류: {str(e)}")
            return False
    
    def get_tasks_by_quadrant(self, quadrant: Quadrant) -> List[Task]:
        """사분면별 할 일 조회"""
        if not self._current_project:
            return []
        return self._current_project.get_tasks_by_quadrant(quadrant)
    
    # Settings Management
    def update_settings(self, **kwargs) -> bool:
        """설정 업데이트"""
        try:
            # 설정 업데이트
            for key, value in kwargs.items():
                if key == 'window_settings' and isinstance(value, dict):
                    # window_settings는 개별적으로 처리
                    for window_key, window_value in value.items():
                        if hasattr(self._settings.window_settings, window_key):
                            setattr(self._settings.window_settings, window_key, window_value)
                elif key == 'language':
                    # 언어 설정 처리
                    from ..models.settings_model import Language
                    if value == "ko":
                        self._settings.language = Language.KOREAN
                    elif value == "en":
                        self._settings.language = Language.ENGLISH
                elif key == 'theme':
                    # 테마 설정 처리
                    from ..models.settings_model import Theme
                    if value == "system":
                        self._settings.theme = Theme.SYSTEM
                    elif value == "light":
                        self._settings.theme = Theme.LIGHT
                    elif value == "dark":
                        self._settings.theme = Theme.DARK
                elif hasattr(self._settings, key):
                    setattr(self._settings, key, value)
            
            # 저장
            if self._data_service.save_settings(self._settings):
                self.settings_changed.emit()
                self._setup_auto_save()  # 자동 저장 설정 재적용
                return True
            else:
                self.emit_error("설정 저장에 실패했습니다.")
                return False
                
        except Exception as e:
            self.emit_error(f"설정 업데이트 중 오류: {str(e)}")
            return False
    
    # Data Management
    def backup_data(self, backup_path: str) -> bool:
        """데이터 백업"""
        try:
            self.is_loading = True
            return self._data_service.backup_data(backup_path)
        except Exception as e:
            self.emit_error(f"백업 중 오류: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    def restore_data(self, backup_path: str) -> bool:
        """데이터 복원"""
        try:
            self.is_loading = True
            if self._data_service.restore_data(backup_path):
                self._load_projects()
                return True
            return False
        except Exception as e:
            self.emit_error(f"복원 중 오류: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    def reset_data(self) -> bool:
        """데이터 초기화"""
        try:
            self.is_loading = True
            if self._data_service.reset_data():
                self._projects.clear()
                self._current_project = None
                self.projects_changed.emit()
                self.current_project_changed.emit()
                return True
            return False
        except Exception as e:
            self.emit_error(f"데이터 초기화 중 오류: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    def export_project(self, project_id: str, export_path: str) -> bool:
        """프로젝트 내보내기"""
        try:
            return self._data_service.export_project(project_id, export_path)
        except Exception as e:
            self.emit_error(f"프로젝트 내보내기 중 오류: {str(e)}")
            return False
    
    def import_project(self, import_path: str) -> bool:
        """프로젝트 가져오기"""
        try:
            self.is_loading = True
            project = self._data_service.import_project(import_path)
            if project:
                self._projects.append(project)
                self.set_current_project(project)
                # 프로젝트 순서 저장
                self._save_project_order()
                self.projects_changed.emit()
                return True
            return False
        except Exception as e:
            self.emit_error(f"프로젝트 가져오기 중 오류: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    # Statistics
    def get_project_statistics(self) -> Dict[str, Any]:
        """프로젝트 통계"""
        if not self._current_project:
            return {}
        
        total_tasks = len(self._current_project.tasks)
        completed_tasks = len(self._current_project.get_completed_tasks())
        pending_tasks = len(self._current_project.get_pending_tasks())
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        quadrant_stats = {}
        for quadrant in Quadrant:
            tasks = self._current_project.get_tasks_by_quadrant(quadrant)
            completed = sum(1 for task in tasks if task.is_completed)
            quadrant_stats[quadrant.value] = {
                'total': len(tasks),
                'completed': completed,
                'pending': len(tasks) - completed
            }
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': completion_rate,
            'quadrant_stats': quadrant_stats
        }
    
    # Private Methods
    def _load_settings(self) -> None:
        """설정 로드"""
        self._settings = self._data_service.load_settings()
        self.settings_changed.emit()
    
    def _load_projects(self) -> None:
        """프로젝트 로드"""
        self._projects = self._data_service.load_all_projects()
        
        # 프로젝트가 없으면 기본 프로젝트 생성
        if not self._projects:
            try:
                from ..models.project_model import Project
                default_project = Project(name="기본 프로젝트", description="첫 번째 프로젝트입니다.")
                if self._data_service.save_project(default_project):
                    self._projects.append(default_project)
            except Exception as e:
                print(f"기본 프로젝트 생성 실패: {e}")
        
        # 첫 번째 프로젝트를 현재 프로젝트로 설정
        if self._projects and not self._current_project:
            self._current_project = self._projects[0]
        
        self.projects_changed.emit()
        self.current_project_changed.emit()
    
    def _setup_auto_save(self) -> None:
        """자동 저장 설정"""
        if self._settings.auto_save:
            self._auto_save_timer.start(self._settings.auto_save_interval * 1000)
        else:
            self._auto_save_timer.stop()
    
    def _auto_save(self) -> None:
        """자동 저장 실행"""
        if self._current_project:
            self._data_service.save_project(self._current_project)
        self._data_service.save_settings(self._settings)
        self.auto_save_triggered.emit()
    
    def _save_project_order(self) -> None:
        """프로젝트 순서 저장"""
        try:
            # 프로젝트 순서 정보를 데이터 서비스에 저장
            project_order = [project.id for project in self._projects]
            self._data_service.save_project_order(project_order)
        except Exception as e:
            self.emit_error(f"프로젝트 순서 저장 중 오류: {str(e)}")