from PyQt5.QtCore import QObject, pyqtSignal
from typing import List, Optional
from datetime import datetime

class ProjectListViewModel(QObject):
    # 상태 변경 시그널
    projectsChanged = pyqtSignal(list)  # 프로젝트 목록 변경
    selectedProjectChanged = pyqtSignal(str)  # 선택된 프로젝트 변경
    statusMessageChanged = pyqtSignal(str, int)  # 상태 메시지 (message, duration)

    def __init__(self, project_usecase):
        super().__init__()
        self.project_usecase = project_usecase
        self.projects: List[str] = []
        self.selected_project: Optional[str] = None
        self._load_projects()

    def _load_projects(self):
        """프로젝트 목록 로드"""
        self.projects = self.project_usecase.get_all_projects()
        self.projectsChanged.emit(self.projects)

    def add_project(self, name: str) -> bool:
        """새 프로젝트 추가"""
        if not name:
            return False
            
        # 중복 체크
        if name in self.projects:
            self.statusMessageChanged.emit("이미 존재하는 프로젝트 이름입니다.", 2000)
            return False

        # UseCase를 통해 프로젝트 생성
        self.project_usecase.create_project(name)
        self._load_projects()
        self.statusMessageChanged.emit("프로젝트가 생성되었습니다.", 1500)
        return True

    def rename_project(self, old_name: str, new_name: str) -> bool:
        """프로젝트 이름 변경"""
        if not new_name or new_name == old_name:
            return False
            
        if new_name in self.projects:
            self.statusMessageChanged.emit("이미 존재하는 프로젝트 이름입니다.", 2000)
            return False

        # UseCase를 통해 프로젝트 이름 변경
        self.project_usecase.rename_project(old_name, new_name)
        self._load_projects()
        self.statusMessageChanged.emit("프로젝트 이름이 변경되었습니다.", 1500)
        return True

    def delete_project(self, name: str) -> bool:
        """프로젝트 삭제"""
        if name not in self.projects:
            return False

        # UseCase를 통해 프로젝트 삭제
        self.project_usecase.delete_project(name)
        self._load_projects()
        self.statusMessageChanged.emit("프로젝트가 삭제되었습니다.", 1500)
        return True

    def select_project(self, name: Optional[str]):
        """프로젝트 선택"""
        self.selected_project = name
        self.selectedProjectChanged.emit(name if name else "")

    def get_project_info(self, name: str) -> dict:
        """프로젝트 정보 조회"""
        return self.project_usecase.get_project_info(name) 