from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class Todo:
    id: str
    title: str
    details: Optional[str] = None
    checked: bool = False
    due_date: Optional[str] = None
    reminders: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat()) 