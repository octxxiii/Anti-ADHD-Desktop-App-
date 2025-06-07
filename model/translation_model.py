from PyQt5.QtCore import QSettings

class TranslationModel:
    """번역 모델"""
    def __init__(self):
        self.settings = QSettings("Anti-ADHD", "Eisenhower Matrix")
        self.current_language = self.settings.value("language", "ko")
        
        # 번역 데이터
        self.translations = {
            "ko": {
                # 메뉴
                "File": "파일",
                "View": "보기",
                "Edit": "편집",
                "Tools": "도구",
                "Help": "도움말",
                
                # 파일 메뉴
                "New Project": "새 프로젝트",
                "Import Project": "프로젝트 가져오기",
                "Save Project": "프로젝트 저장",
                "Save Project As": "다른 이름으로 저장",
                "Exit": "종료",
                
                # 보기 메뉴
                "Show Toolbar": "툴바 보기",
                "Show Statusbar": "상태바 보기",
                
                # 편집 메뉴
                "Add Task": "할 일 추가",
                "Edit Task": "할 일 수정",
                "Delete Task": "할 일 삭제",
                
                # 도구 메뉴
                "Settings": "설정",
                "Statistics": "통계",
                
                # 도움말 메뉴
                "About": "정보",
                
                # 사분면
                "Urgent & Important": "긴급 & 중요",
                "Not Urgent & Important": "긴급 아님 & 중요",
                "Urgent & Not Important": "긴급 & 중요 아님",
                "Not Urgent & Not Important": "긴급 아님 & 중요 아님",
                "Do it now": "즉시 처리해야 할 일",
                "Plan to do": "계획적으로 해야 할 일",
                "Delegate or do quickly": "위임/빠르게 처리",
                "Don't do": "하지 않아도 되는 일",
                "New task...": "새 할 일 입력...",
                "Add": "추가",
                
                # 컨텍스트 메뉴
                "Edit": "수정",
                "Delete": "삭제",
                "Move Up": "위로 이동",
                "Move Down": "아래로 이동",
                "Rename": "이름 변경",
                
                # 설정 다이얼로그
                "Settings": "설정",
                "General": "일반",
                "Shortcuts": "단축키",
                "About": "정보",
                "Language:": "언어:",
                "Theme:": "테마:",
                "System": "시스템",
                "Light": "라이트",
                "Dark": "다크",
                "Auto Save": "자동 저장",
                "Enable Notifications": "알림 사용",
                "OK": "확인",
                "Cancel": "취소",
                "Korean": "한국어",
                "English": "영어",
                
                # 메시지
                "Ready": "준비",
                "Project created": "프로젝트가 생성되었습니다",
                "Project renamed": "프로젝트 이름이 변경되었습니다",
                "Project deleted": "프로젝트가 삭제되었습니다",
                "Task added": "할 일이 추가되었습니다",
                "Task updated": "할 일이 수정되었습니다",
                "Task deleted": "할 일이 삭제되었습니다",
                "Task moved": "할 일이 이동되었습니다",
                "Are you sure you want to delete this project?": "이 프로젝트를 삭제하시겠습니까?",
                "Are you sure you want to delete this task?": "이 할 일을 삭제하시겠습니까?",
                "Project Name:": "프로젝트 이름:",
                "New Name:": "새 이름:",
                "Task:": "할 일:",
            },
            "en": {
                # 메뉴
                "File": "File",
                "View": "View",
                "Edit": "Edit",
                "Tools": "Tools",
                "Help": "Help",
                
                # 파일 메뉴
                "New Project": "New Project",
                "Import Project": "Import Project",
                "Save Project": "Save Project",
                "Save Project As": "Save Project As",
                "Exit": "Exit",
                
                # 보기 메뉴
                "Show Toolbar": "Show Toolbar",
                "Show Statusbar": "Show Statusbar",
                
                # 편집 메뉴
                "Add Task": "Add Task",
                "Edit Task": "Edit Task",
                "Delete Task": "Delete Task",
                
                # 도구 메뉴
                "Settings": "Settings",
                "Statistics": "Statistics",
                
                # 도움말 메뉴
                "About": "About",
                
                # 사분면
                "Urgent & Important": "Urgent & Important",
                "Not Urgent & Important": "Not Urgent & Important",
                "Urgent & Not Important": "Urgent & Not Important",
                "Not Urgent & Not Important": "Not Urgent & Not Important",
                "Do it now": "Do it now",
                "Plan to do": "Plan to do",
                "Delegate or do quickly": "Delegate or do quickly",
                "Don't do": "Don't do",
                "New task...": "New task...",
                "Add": "Add",
                
                # 컨텍스트 메뉴
                "Edit": "Edit",
                "Delete": "Delete",
                "Move Up": "Move Up",
                "Move Down": "Move Down",
                "Rename": "Rename",
                
                # 설정 다이얼로그
                "Settings": "Settings",
                "General": "General",
                "Shortcuts": "Shortcuts",
                "About": "About",
                "Language:": "Language:",
                "Theme:": "Theme:",
                "System": "System",
                "Light": "Light",
                "Dark": "Dark",
                "Auto Save": "Auto Save",
                "Enable Notifications": "Enable Notifications",
                "OK": "OK",
                "Cancel": "Cancel",
                
                # 메시지
                "Ready": "Ready",
                "Project created": "Project created",
                "Project renamed": "Project renamed",
                "Project deleted": "Project deleted",
                "Task added": "Task added",
                "Task updated": "Task updated",
                "Task deleted": "Task deleted",
                "Task moved": "Task moved",
                "Are you sure you want to delete this project?": "Are you sure you want to delete this project?",
                "Are you sure you want to delete this task?": "Are you sure you want to delete this task?",
                "Project Name:": "Project Name:",
                "New Name:": "New Name:",
                "Task:": "Task:",
            }
        }

    def get_current_language(self):
        """현재 언어 반환"""
        return self.current_language

    def set_language(self, language):
        """언어 설정"""
        if language in self.translations:
            self.current_language = language
            self.settings.setValue("language", language)
            self.settings.sync()

    def tr(self, text):
        """텍스트 번역"""
        if self.current_language in self.translations:
            return self.translations[self.current_language].get(text, text)
        return text 