from PyQt5.QtCore import QObject, pyqtSignal
from model.todo import Todo
from typing import Optional, List
import uuid

class EisenhowerQuadrantViewModel(QObject):
    # 상태 변경 시그널
    tasksChanged = pyqtSignal(list)
    selectedTaskChanged = pyqtSignal(object)
    statusMessageChanged = pyqtSignal(str, int)  # message, duration

    def __init__(self, todo_usecase, project_name: str, quadrant_idx: int):
        super().__init__()
        self.todo_usecase = todo_usecase
        self.project_name = project_name
        self.quadrant_idx = quadrant_idx
        self.tasks: List[Todo] = []
        self.selected_task: Optional[Todo] = None
        self._load_tasks()

    def _load_tasks(self):
        """Repository에서 할 일 목록 로드"""
        self.tasks = self.todo_usecase.get_tasks(self.project_name, self.quadrant_idx)
        self.tasksChanged.emit(self.tasks)

    def add_task(self, title: str) -> bool:
        """새 할 일 추가"""
        if not title:
            return False
            
        # 중복 체크
        if any(task.title == title for task in self.tasks):
            self.statusMessageChanged.emit("이미 존재하는 제목입니다.", 2000)
            return False

        # 새 Todo 객체 생성
        task = Todo(
            id=str(uuid.uuid4()),
            title=title
        )
        
        # UseCase를 통해 저장
        self.todo_usecase.add_task(self.project_name, self.quadrant_idx, task)
        self._load_tasks()  # 목록 새로고침
        self.statusMessageChanged.emit("항목이 추가되었습니다.", 1500)
        return True

    def remove_task(self, task_id: str):
        """할 일 삭제"""
        self.todo_usecase.remove_task(self.project_name, self.quadrant_idx, task_id)
        self._load_tasks()

    def update_task(self, task: Todo):
        """할 일 수정"""
        self.todo_usecase.update_task(self.project_name, self.quadrant_idx, task)
        self._load_tasks()

    def check_task(self, task_id: str, checked: bool):
        """할 일 체크 상태 변경"""
        self.todo_usecase.check_task(self.project_name, self.quadrant_idx, task_id, checked)
        self._load_tasks()

    def move_task_to_quadrant(self, task_id: str, target_quadrant_idx: int):
        """다른 사분면으로 할 일 이동"""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            # 현재 사분면에서 삭제
            self.remove_task(task_id)
            # 대상 사분면에 추가
            self.todo_usecase.add_task(self.project_name, target_quadrant_idx, task)
            self.statusMessageChanged.emit(f"'{task.title}'을(를) 이동했습니다.", 2000)

    def select_task(self, task: Optional[Todo]):
        """할 일 선택"""
        self.selected_task = task
        self.selectedTaskChanged.emit(task)

    def clear_tasks(self):
        """모든 할 일 삭제"""
        for task in self.tasks:
            self.remove_task(task.id) 