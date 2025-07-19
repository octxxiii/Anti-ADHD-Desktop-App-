"""
Project 모델 - 프로젝트 데이터 구조
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from .task_model import Task, Quadrant
import uuid


@dataclass
class Project:
    """프로젝트 모델"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """초기화 후 처리"""
        if not self.name.strip():
            raise ValueError("Project name cannot be empty")
    
    def add_task(self, task: Task) -> None:
        """작업 추가"""
        self.tasks.append(task)
        self.updated_at = datetime.now()
    
    def update_name(self, name: str) -> None:
        """프로젝트 이름 업데이트"""
        if not name.strip():
            raise ValueError("Project name cannot be empty")
        self.name = name.strip()
        self.updated_at = datetime.now()
    
    def remove_task(self, task_id: str) -> bool:
        """작업 제거"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.updated_at = datetime.now()
                return True
        return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """작업 조회"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_by_quadrant(self, quadrant: Quadrant) -> List[Task]:
        """사분면별 작업 조회"""
        return [task for task in self.tasks if task.quadrant == quadrant]
    
    def get_completed_tasks(self) -> List[Task]:
        """완료된 작업 조회"""
        return [task for task in self.tasks if task.is_completed]
    
    def get_pending_tasks(self) -> List[Task]:
        """미완료 작업 조회"""
        return [task for task in self.tasks if not task.is_completed]
    
    def get_task_count(self) -> int:
        """전체 작업 수"""
        return len(self.tasks)
    
    def get_completion_rate(self) -> float:
        """완료율 계산"""
        if not self.tasks:
            return 0.0
        completed_count = len(self.get_completed_tasks())
        return (completed_count / len(self.tasks)) * 100
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tasks': [task.to_dict() for task in self.tasks],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """딕셔너리에서 생성"""
        project = cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data.get('name', ''),
            description=data.get('description', ''),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )
        
        # 작업들 복원
        tasks_data = data.get('tasks', [])
        for task_data in tasks_data:
            task = Task.from_dict(task_data)
            project.tasks.append(task)
        
        return project
    
    @classmethod
    def create_new(cls, name: str, description: str = "") -> 'Project':
        """새 프로젝트 생성"""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            description=description
        )