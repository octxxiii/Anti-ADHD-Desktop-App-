from PyQt5.QtCore import QObject, pyqtSignal

class MainWindowViewModel(QObject):
    # 상태 변경 시그널
    projectChanged = pyqtSignal(str)
    tasksChanged = pyqtSignal(list)
    statusChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_project = None
        self.tasks = []
        self.status = ""

    def set_project(self, project_name):
        self.current_project = project_name
        self.projectChanged.emit(project_name)

    def set_tasks(self, tasks):
        self.tasks = tasks
        self.tasksChanged.emit(tasks)

    def set_status(self, status):
        self.status = status
        self.statusChanged.emit(status)

    # 예시: 할 일 추가
    def add_task(self, task):
        self.tasks.append(task)
        self.tasksChanged.emit(self.tasks)
        self.set_status(f"할 일 추가됨: {task}") 