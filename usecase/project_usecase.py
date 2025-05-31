from typing import List, Dict
from datetime import datetime
import os
import json
import shutil

class ProjectUseCase:
    def __init__(self, repository):
        self.repository = repository

    def get_all_projects(self) -> List[str]:
        """모든 프로젝트 목록 조회"""
        return self.repository.list_projects()

    def create_project(self, name: str):
        """새 프로젝트 생성"""
        project_data = {
            "quadrants": [[], [], [], []],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.repository.save_project(name, project_data)

    def rename_project(self, old_name: str, new_name: str):
        """프로젝트 이름 변경"""
        project_data = self.repository.load_project(old_name)
        project_data["updated_at"] = datetime.now().isoformat()
        self.repository.rename_project(old_name, new_name, project_data)

    def delete_project(self, name: str):
        """프로젝트 삭제"""
        self.repository.delete_project(name)

    def get_project_info(self, name: str) -> Dict:
        """프로젝트 정보 조회"""
        return self.repository.load_project(name)

    def save_project(self, name: str, project_data: Dict):
        """프로젝트 저장"""
        project_data["updated_at"] = datetime.now().isoformat()
        self.repository.save_project(name, project_data)

    def backup_project(self, name: str):
        """프로젝트 백업"""
        self.repository.backup_project(name)

    def restore_project(self, name: str, backup_name: str):
        """프로젝트 복원"""
        self.repository.restore_project(name, backup_name) 