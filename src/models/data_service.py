"""
Data Service - 데이터 저장/로드 서비스
"""
import json
import os
import zipfile
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .task_model import Task
from .project_model import Project
from .settings_model import AppSettings


class DataService:
    """데이터 관리 서비스"""
    
    def __init__(self, data_directory: str):
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)
        self.settings_file = self.data_directory / "settings.json"
        self.project_order_file = self.data_directory / "project_order.json"
    
    def save_project(self, project: Project) -> bool:
        """프로젝트 저장"""
        try:
            project_file = self.data_directory / f"project_{project.id}.json"
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(project.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
    
    def load_project(self, project_id: str) -> Optional[Project]:
        """프로젝트 로드"""
        try:
            project_file = self.data_directory / f"project_{project_id}.json"
            if not project_file.exists():
                return None
            
            with open(project_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return Project.from_dict(data)
        except Exception as e:
            print(f"Error loading project: {e}")
            return None
    
    def load_all_projects(self) -> List[Project]:
        """모든 프로젝트 로드 (순서 유지)"""
        projects = []
        try:
            # 모든 프로젝트 로드 (project_order.json 제외)
            for project_file in self.data_directory.glob("project_*.json"):
                # project_order.json 파일은 건너뜀
                if project_file.name == "project_order.json":
                    continue
                    
                try:
                    with open(project_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 데이터 형식 검증
                    if not isinstance(data, dict):
                        print(f"Invalid project file format in {project_file}: data is not a dictionary")
                        continue
                        
                    # 필수 필드 확인
                    if 'name' not in data or not data['name']:
                        print(f"Invalid project file format in {project_file}: missing name field")
                        continue
                        
                    project = Project.from_dict(data)
                    projects.append(project)
                except Exception as e:
                    print(f"Error loading project file {project_file}: {e}")
                    continue
            
            # 저장된 순서대로 정렬
            try:
                project_order = self.load_project_order()
                if project_order and isinstance(project_order, list):
                    # 순서 정보가 있는 프로젝트들을 먼저 정렬
                    ordered_projects = []
                    remaining_projects = projects.copy()
                    
                    for project_id in project_order:
                        project = next((p for p in remaining_projects if p.id == project_id), None)
                        if project:
                            ordered_projects.append(project)
                            remaining_projects.remove(project)
                    
                    # 순서 정보가 없는 새 프로젝트들을 뒤에 추가
                    ordered_projects.extend(sorted(remaining_projects, key=lambda p: p.updated_at, reverse=True))
                    return ordered_projects
                else:
                    # 순서 정보가 없으면 업데이트 시간순으로 정렬
                    return sorted(projects, key=lambda p: p.updated_at, reverse=True)
            except Exception as e:
                print(f"Error sorting projects: {e}")
                return sorted(projects, key=lambda p: p.updated_at, reverse=True)
        except Exception as e:
            print(f"Error loading projects: {e}")
            return []
    
    def delete_project(self, project_id: str) -> bool:
        """프로젝트 삭제"""
        try:
            project_file = self.data_directory / f"project_{project_id}.json"
            if project_file.exists():
                project_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting project: {e}")
            return False
    
    def save_settings(self, settings: AppSettings) -> bool:
        """설정 저장"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def load_settings(self) -> AppSettings:
        """설정 로드"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return AppSettings.from_dict(data)
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        # 기본 설정 반환
        return AppSettings()
    
    def backup_data(self, backup_path: str) -> bool:
        """데이터 백업"""
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # 모든 프로젝트 파일 백업
                for project_file in self.data_directory.glob("project_*.json"):
                    zf.write(project_file, project_file.name)
                
                # 설정 파일 백업
                if self.settings_file.exists():
                    zf.write(self.settings_file, self.settings_file.name)
            
            return True
        except Exception as e:
            print(f"Error backing up data: {e}")
            return False
    
    def restore_data(self, backup_path: str) -> bool:
        """데이터 복원"""
        try:
            if not zipfile.is_zipfile(backup_path):
                return False
            
            # 기존 데이터 백업
            temp_backup = self.data_directory / f"temp_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            temp_backup.mkdir(exist_ok=True)
            
            # 기존 파일들을 임시 백업
            for file in self.data_directory.glob("*.json"):
                shutil.copy2(file, temp_backup)
            
            try:
                # 백업 파일에서 복원
                with zipfile.ZipFile(backup_path, 'r') as zf:
                    zf.extractall(self.data_directory)
                
                # 임시 백업 삭제
                shutil.rmtree(temp_backup)
                return True
                
            except Exception as e:
                # 복원 실패 시 원본 복구
                for file in temp_backup.glob("*.json"):
                    shutil.copy2(file, self.data_directory)
                shutil.rmtree(temp_backup)
                raise e
                
        except Exception as e:
            print(f"Error restoring data: {e}")
            return False
    
    def reset_data(self) -> bool:
        """데이터 초기화"""
        try:
            # 모든 프로젝트 파일 삭제
            for project_file in self.data_directory.glob("project_*.json"):
                project_file.unlink()
            
            # 설정 파일은 유지 (사용자가 원할 경우에만 삭제)
            return True
        except Exception as e:
            print(f"Error resetting data: {e}")
            return False
    
    def export_project(self, project_id: str, export_path: str) -> bool:
        """프로젝트 내보내기"""
        try:
            project = self.load_project(project_id)
            if not project:
                return False
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(project.to_dict(), f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting project: {e}")
            return False
    
    def import_project(self, import_path: str) -> Optional[Project]:
        """프로젝트 가져오기"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            project = Project.from_dict(data)
            
            # 새로운 ID 생성 (중복 방지)
            import uuid
            project.id = str(uuid.uuid4())
            
            # 저장
            if self.save_project(project):
                return project
            
            return None
        except Exception as e:
            print(f"Error importing project: {e}")
            return None
    
    def get_project_list(self) -> List[Dict[str, Any]]:
        """프로젝트 목록 정보 반환"""
        project_list = []
        try:
            for project_file in self.data_directory.glob("project_*.json"):
                with open(project_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                project_info = {
                    'id': data.get('id'),
                    'name': data.get('name'),
                    'description': data.get('description', ''),
                    'task_count': len(data.get('tasks', [])),
                    'completed_count': sum(1 for task in data.get('tasks', []) if task.get('is_completed', False)),
                    'created_at': data.get('created_at'),
                    'updated_at': data.get('updated_at')
                }
                project_list.append(project_info)
        except Exception as e:
            print(f"Error getting project list: {e}")
        
        return sorted(project_list, key=lambda p: p['updated_at'], reverse=True)
    
    def save_project_order(self, project_ids: List[str]) -> bool:
        """프로젝트 순서 저장"""
        try:
            order_data = {
                'project_order': project_ids,
                'updated_at': datetime.now().isoformat()
            }
            with open(self.project_order_file, 'w', encoding='utf-8') as f:
                json.dump(order_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving project order: {e}")
            return False
    
    def load_project_order(self) -> List[str]:
        """프로젝트 순서 로드"""
        try:
            if self.project_order_file.exists():
                with open(self.project_order_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data.get('project_order', [])
                elif isinstance(data, list):
                    return data
        except Exception as e:
            print(f"Error loading project order: {e}")
        
        return []