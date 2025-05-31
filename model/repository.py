from model.todo import Todo
from typing import List
import os
import json

class TodoRepository:
    def add_task(self, project_name, quadrant_idx, task: Todo):
        raise NotImplementedError
    def remove_task(self, project_name, quadrant_idx, task_id):
        raise NotImplementedError
    def update_task(self, project_name, quadrant_idx, task: Todo):
        raise NotImplementedError
    def check_task(self, project_name, quadrant_idx, task_id, checked: bool):
        raise NotImplementedError
    def get_tasks(self, project_name, quadrant_idx) -> List[Todo]:
        raise NotImplementedError

class FileTodoRepository(TodoRepository):
    def __init__(self, data_dir):
        self.data_dir = data_dir
    def _get_project_file(self, project_name):
        return os.path.join(self.data_dir, f"{project_name}.json")
    def add_task(self, project_name, quadrant_idx, task: Todo):
        data = self._load_project(project_name)
        data['quadrants'][quadrant_idx].append(task.__dict__)
        self._save_project(project_name, data)
    def remove_task(self, project_name, quadrant_idx, task_id):
        data = self._load_project(project_name)
        data['quadrants'][quadrant_idx] = [t for t in data['quadrants'][quadrant_idx] if t['id'] != task_id]
        self._save_project(project_name, data)
    def update_task(self, project_name, quadrant_idx, task: Todo):
        data = self._load_project(project_name)
        for i, t in enumerate(data['quadrants'][quadrant_idx]):
            if t['id'] == task.id:
                data['quadrants'][quadrant_idx][i] = task.__dict__
                break
        self._save_project(project_name, data)
    def check_task(self, project_name, quadrant_idx, task_id, checked: bool):
        data = self._load_project(project_name)
        for t in data['quadrants'][quadrant_idx]:
            if t['id'] == task_id:
                t['checked'] = checked
        self._save_project(project_name, data)
    def get_tasks(self, project_name, quadrant_idx):
        data = self._load_project(project_name)
        return [Todo(**t) for t in data['quadrants'][quadrant_idx]]
    def _load_project(self, project_name):
        file_path = self._get_project_file(project_name)
        if not os.path.exists(file_path):
            return {'quadrants': [[], [], [], []]}
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 방어코드: quadrants 키가 없으면 기본값 추가
        if 'quadrants' not in data or not isinstance(data['quadrants'], list) or len(data['quadrants']) != 4:
            data['quadrants'] = [[], [], [], []]
        return data
    def _save_project(self, project_name, data):
        file_path = self._get_project_file(project_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    def list_projects(self):
        """데이터 디렉토리 내 모든 프로젝트 이름 리스트 반환"""
        if not os.path.exists(self.data_dir):
            return []
        projects = []
        for fname in os.listdir(self.data_dir):
            if fname.endswith('.json') and not fname.startswith('~'):
                projects.append(os.path.splitext(fname)[0])
        return projects
    def load_project(self, project_name):
        """프로젝트 데이터 조회 (public)"""
        return self._load_project(project_name) 