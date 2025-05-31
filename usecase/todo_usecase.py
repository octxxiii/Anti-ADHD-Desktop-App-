"""
할 일 관리 UseCase
- 비즈니스 로직(추가, 삭제, 수정, 체크 등)
- ViewModel에서 호출
"""
from model.todo import Todo

class TodoUseCase:
    def __init__(self, repository):
        self.repository = repository

    def add_task(self, project_name, quadrant_idx, task: Todo):
        self.repository.add_task(project_name, quadrant_idx, task)

    def remove_task(self, project_name, quadrant_idx, task_id):
        self.repository.remove_task(project_name, quadrant_idx, task_id)

    def update_task(self, project_name, quadrant_idx, task: Todo):
        self.repository.update_task(project_name, quadrant_idx, task)

    def check_task(self, project_name, quadrant_idx, task_id, checked: bool):
        self.repository.check_task(project_name, quadrant_idx, task_id, checked)

    def get_tasks(self, project_name, quadrant_idx):
        return self.repository.get_tasks(project_name, quadrant_idx) 