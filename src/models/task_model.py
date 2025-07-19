"""
Task Model - 할 일 데이터 모델
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid


class Priority(Enum):
    """우선순위 열거형"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Quadrant(Enum):
    """아이젠하워 매트릭스 사분면"""
    URGENT_IMPORTANT = "urgent_important"          # 1사분면: 긴급하고 중요
    NOT_URGENT_IMPORTANT = "not_urgent_important"  # 2사분면: 긴급하지 않지만 중요
    URGENT_NOT_IMPORTANT = "urgent_not_important"  # 3사분면: 긴급하지만 중요하지 않음
    NOT_URGENT_NOT_IMPORTANT = "not_urgent_not_important"  # 4사분면: 긴급하지도 중요하지도 않음


@dataclass
class Task:
    """할 일 모델"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    quadrant: Quadrant = Quadrant.URGENT_IMPORTANT
    priority: Priority = Priority.MEDIUM
    is_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    
    def __post_init__(self):
        """초기화 후 처리"""
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")
    
    def mark_completed(self) -> None:
        """할 일을 완료로 표시"""
        self.is_completed = True
        self.updated_at = datetime.now()
    
    def mark_incomplete(self) -> None:
        """할 일을 미완료로 표시"""
        self.is_completed = False
        self.updated_at = datetime.now()
    
    def update_title(self, title: str) -> None:
        """제목 업데이트"""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        self.title = title.strip()
        self.updated_at = datetime.now()
    
    def update_description(self, description: str) -> None:
        """설명 업데이트"""
        self.description = description
        self.updated_at = datetime.now()
    
    def move_to_quadrant(self, quadrant: Quadrant) -> None:
        """다른 사분면으로 이동"""
        self.quadrant = quadrant
        self.updated_at = datetime.now()
    
    def set_due_date(self, due_date: Optional[datetime]) -> None:
        """마감일 설정"""
        self.due_date = due_date
        self.updated_at = datetime.now()
    
    def set_priority(self, priority: Priority) -> None:
        """우선순위 설정"""
        self.priority = priority
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환 (JSON 직렬화용)"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'quadrant': self.quadrant.value,
            'priority': self.priority.value,
            'is_completed': self.is_completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'reminder_time': self.reminder_time.isoformat() if self.reminder_time else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """딕셔너리에서 Task 객체 생성"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            title=data.get('title', ''),
            description=data.get('description', ''),
            quadrant=Quadrant(data.get('quadrant', Quadrant.URGENT_IMPORTANT.value)),
            priority=Priority(data.get('priority', Priority.MEDIUM.value)),
            is_completed=data.get('is_completed', False),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now(),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            reminder_time=datetime.fromisoformat(data['reminder_time']) if data.get('reminder_time') else None
        )


# Project 클래스는 project_model.py로 이동됨