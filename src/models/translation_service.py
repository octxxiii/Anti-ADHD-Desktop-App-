"""
Translation Service - 다국어 번역 서비스
"""
from typing import Dict, Optional
from enum import Enum


class Language(Enum):
    """지원 언어"""
    KOREAN = "ko"
    ENGLISH = "en"


class TranslationService:
    """번역 서비스 싱글톤"""
    
    _instance: Optional['TranslationService'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._current_language = Language.KOREAN
        self._translations = {
            Language.KOREAN: {
                # 메뉴
                "File": "파일",
                "Edit": "편집", 
                "View": "보기",
                "Tools": "도구",
                "Help": "도움말",
                
                # 파일 메뉴
                "New Project": "새 프로젝트",
                "Import Project": "프로젝트 가져오기",
                "Export Project": "프로젝트 내보내기",
                "Exit": "종료",
                
                # 편집 메뉴
                "Add Task": "할 일 추가",
                
                # 보기 메뉴
                "Show Sidebar": "사이드바 표시",
                "Show Toolbar": "툴바 표시", 
                "Show Statusbar": "상태바 표시",
                "Always on Top": "항상 위",
                
                # 도구 메뉴
                "Settings": "설정",
                "Statistics": "통계",
                
                # 도움말 메뉴
                "About": "정보",
                
                # 사분면
                "Urgent and Important": "긴급하고 중요",
                "Important but Not Urgent": "중요하지만 긴급하지 않음",
                "Urgent but Not Important": "긴급하지만 중요하지 않음", 
                "Neither Urgent nor Important": "긴급하지도 중요하지도 않음",
                "Do it now": "즉시 처리해야 할 일",
                "Plan to do": "계획을 세워 처리할 일",
                "Delegate or do quickly": "위임하거나 빠르게 처리",
                "Don't do": "하지 않아도 되는 일",
                
                # 설정 다이얼로그
                "General": "일반",
                "Appearance": "외관", 
                "Data": "데이터",
                "About": "정보",
                "Language": "언어",
                "Theme": "테마",
                "System": "시스템",
                "Light": "라이트",
                "Dark": "다크",
                "Auto Save": "자동 저장",
                "Enable auto save": "자동 저장 사용",
                "Save interval": "저장 간격",
                "seconds": "초",
                "Check for Updates": "업데이트 확인",
                "Check on startup": "시작 시 확인",
                "Window Settings": "창 설정",
                "Always on top": "항상 위에 표시",
                "Opacity": "투명도",
                "UI Elements": "UI 요소",
                "Show sidebar": "사이드바 표시",
                "Show toolbar": "툴바 표시",
                "Show statusbar": "상태바 표시",
                "Data Directory": "데이터 저장 위치",
                "Browse": "찾아보기",
                "Data Management": "데이터 관리",
                "Backup Data": "데이터 백업",
                "Restore Data": "데이터 복원",
                "Reset Data": "데이터 초기화",
                "Program Information": "프로그램 정보",
                "Name": "이름",
                "Version": "버전",
                "Developer": "개발자",
                "License": "라이선스",
                "GitHub Repository": "GitHub 저장소",
                
                # 공통
                "OK": "확인",
                "Cancel": "취소",
                "Apply": "적용",
                "Close": "닫기",
                "Yes": "예",
                "No": "아니오",
                "Warning": "경고",
                "Error": "오류",
                "Information": "정보",
                "Ready": "준비",
                
                # 프로젝트
                "Projects": "프로젝트",
                "New Project": "새 프로젝트",
                "Project Name": "프로젝트 이름",
                "Enter project name": "프로젝트 이름을 입력하세요",
                "Delete Project": "프로젝트 삭제",
                "Rename Project": "프로젝트 이름 변경",
                "Are you sure you want to delete this project?": "정말로 이 프로젝트를 삭제하시겠습니까?",
                
                # 할 일
                "New task": "새 할 일 입력",
                "Add": "추가",
                "Edit Task": "할 일 편집",
                "Title": "제목",
                "Memo": "메모",
                "Due Date": "마감일",
                "Set due date": "마감일 설정",
                "Reminder": "알림",
                "Set reminder": "알림 설정",
                "Priority": "우선순위",
                "Low": "낮음",
                "Medium": "보통", 
                "High": "높음",
                "1 day before": "마감 1일 전",
                "3 hours before": "마감 3시간 전",
                "1 hour before": "마감 1시간 전", 
                "30 minutes before": "마감 30분 전",
                "10 minutes before": "마감 10분 전",
                
                # 메시지
                "Please enter a title": "제목을 입력해주세요",
                "Project created": "프로젝트가 생성되었습니다",
                "Project deleted": "프로젝트가 삭제되었습니다",
                "Project renamed": "프로젝트 이름이 변경되었습니다",
                "Auto saved": "자동 저장됨",
                "Project imported": "프로젝트를 가져왔습니다",
                "Project exported": "프로젝트를 내보냈습니다",
                
                # 통계
                "Project Statistics": "프로젝트 통계",
                "Total tasks": "전체 할 일",
                "Completed tasks": "완료된 할 일",
                "Pending tasks": "미완료 할 일",
                "Completion rate": "완료율",
                "Quadrant Statistics": "사분면별 통계",
                
                # 프로젝트 순서
                "Move Up": "위로 이동",
                "Move Down": "아래로 이동",
                
                # 추가 번역
                "Application restart required after changing data directory": "데이터 디렉토리 변경 후 애플리케이션을 재시작해야 합니다",
                "Please select a project first.": "프로젝트를 먼저 선택해주세요.",
                "Project": "프로젝트",
                "Ready": "준비",
                "Processing...": "처리 중...",
                "Error occurred": "오류 발생",
                "Auto saved": "자동 저장됨",
                "New Project": "새 프로젝트",
                "Project Name": "프로젝트 이름",
                "Delete Project": "프로젝트 삭제",
                "Are you sure you want to delete this project?": "정말로 이 프로젝트를 삭제하시겠습니까?",
                "Rename Project": "프로젝트 이름 변경",
                "New name": "새 이름",
                "Export": "내보내기",
                "Please select a project to export first.": "내보낼 프로젝트를 먼저 선택해주세요.",
                "Import Project": "프로젝트 가져오기",
                "Export Project": "프로젝트 내보내기",
                "JSON Files": "JSON 파일",
                "About Anti-ADHD": "Anti-ADHD 정보",
                "Eisenhower Matrix Task Management Tool for ADHD": "ADHD를 위한 아이젠하워 매트릭스 할 일 관리 도구",
                
                # 할 일 편집 다이얼로그
                "Enter task title": "할 일 제목을 입력하세요",
                "Enter memo or detailed description (optional)": "메모나 상세 설명을 입력하세요 (선택사항)",
                "Delete Task": "할 일 삭제",
                "Are you sure you want to delete this task?": "정말로 이 할 일을 삭제하시겠습니까?",
                "Edit": "편집",
                "Delete": "삭제",
                "Move": "이동",
                "No tasks": "할 일 없음",
                "Project moved up": "프로젝트가 위로 이동되었습니다",
                "Project moved down": "프로젝트가 아래로 이동되었습니다",
            },
            
            Language.ENGLISH: {
                # 메뉴
                "File": "File",
                "Edit": "Edit",
                "View": "View", 
                "Tools": "Tools",
                "Help": "Help",
                
                # 파일 메뉴
                "New Project": "New Project",
                "Import Project": "Import Project",
                "Export Project": "Export Project", 
                "Exit": "Exit",
                
                # 편집 메뉴
                "Add Task": "Add Task",
                
                # 보기 메뉴
                "Show Sidebar": "Show Sidebar",
                "Show Toolbar": "Show Toolbar",
                "Show Statusbar": "Show Statusbar",
                "Always on Top": "Always on Top",
                
                # 도구 메뉴
                "Settings": "Settings",
                "Statistics": "Statistics",
                
                # 도움말 메뉴
                "About": "About",
                
                # 사분면
                "Urgent and Important": "Urgent and Important",
                "Important but Not Urgent": "Important but Not Urgent", 
                "Urgent but Not Important": "Urgent but Not Important",
                "Neither Urgent nor Important": "Neither Urgent nor Important",
                "Do it now": "Do it now",
                "Plan to do": "Plan to do",
                "Delegate or do quickly": "Delegate or do quickly",
                "Don't do": "Don't do",
                
                # 설정 다이얼로그
                "General": "General",
                "Appearance": "Appearance",
                "Data": "Data", 
                "About": "About",
                "Language": "Language",
                "Theme": "Theme",
                "System": "System",
                "Light": "Light",
                "Dark": "Dark",
                "Auto Save": "Auto Save",
                "Enable auto save": "Enable auto save",
                "Save interval": "Save interval",
                "seconds": "seconds",
                "Check for Updates": "Check for Updates",
                "Check on startup": "Check on startup",
                "Window Settings": "Window Settings",
                "Always on top": "Always on top",
                "Opacity": "Opacity",
                "UI Elements": "UI Elements",
                "Show sidebar": "Show sidebar",
                "Show toolbar": "Show toolbar", 
                "Show statusbar": "Show statusbar",
                "Data Directory": "Data Directory",
                "Browse": "Browse",
                "Data Management": "Data Management",
                "Backup Data": "Backup Data",
                "Restore Data": "Restore Data",
                "Reset Data": "Reset Data",
                "Program Information": "Program Information",
                "Name": "Name",
                "Version": "Version",
                "Developer": "Developer",
                "License": "License",
                "GitHub Repository": "GitHub Repository",
                
                # 공통
                "OK": "OK",
                "Cancel": "Cancel",
                "Apply": "Apply",
                "Close": "Close",
                "Yes": "Yes",
                "No": "No",
                "Warning": "Warning",
                "Error": "Error",
                "Information": "Information",
                "Ready": "Ready",
                
                # 프로젝트
                "Projects": "Projects",
                "New Project": "New Project",
                "Project Name": "Project Name",
                "Enter project name": "Enter project name",
                "Delete Project": "Delete Project",
                "Rename Project": "Rename Project",
                "Are you sure you want to delete this project?": "Are you sure you want to delete this project?",
                
                # 할 일
                "New task": "New task",
                "Add": "Add",
                "Edit Task": "Edit Task",
                "Title": "Title",
                "Memo": "Memo",
                "Due Date": "Due Date",
                "Set due date": "Set due date",
                "Reminder": "Reminder",
                "Set reminder": "Set reminder",
                "Priority": "Priority",
                "Low": "Low",
                "Medium": "Medium",
                "High": "High",
                "1 day before": "1 day before",
                "3 hours before": "3 hours before",
                "1 hour before": "1 hour before",
                "30 minutes before": "30 minutes before",
                "10 minutes before": "10 minutes before",
                
                # 메시지
                "Please enter a title": "Please enter a title",
                "Project created": "Project created",
                "Project deleted": "Project deleted",
                "Project renamed": "Project renamed",
                "Auto saved": "Auto saved",
                "Project imported": "Project imported",
                "Project exported": "Project exported",
                
                # 통계
                "Project Statistics": "Project Statistics",
                "Total tasks": "Total tasks",
                "Completed tasks": "Completed tasks",
                "Pending tasks": "Pending tasks",
                "Completion rate": "Completion rate",
                "Quadrant Statistics": "Quadrant Statistics",
                
                # 프로젝트 순서
                "Move Up": "Move Up",
                "Move Down": "Move Down",
                
                # 추가 번역
                "Application restart required after changing data directory": "Application restart required after changing data directory",
                "Please select a project first.": "Please select a project first.",
                "Project": "Project",
                "Ready": "Ready",
                "Processing...": "Processing...",
                "Error occurred": "Error occurred",
                "Auto saved": "Auto saved",
                "New Project": "New Project",
                "Project Name": "Project Name",
                "Delete Project": "Delete Project",
                "Are you sure you want to delete this project?": "Are you sure you want to delete this project?",
                "Rename Project": "Rename Project",
                "New name": "New name",
                "Export": "Export",
                "Please select a project to export first.": "Please select a project to export first.",
                "Import Project": "Import Project",
                "Export Project": "Export Project",
                "JSON Files": "JSON Files",
                "About Anti-ADHD": "About Anti-ADHD",
                "Eisenhower Matrix Task Management Tool for ADHD": "Eisenhower Matrix Task Management Tool for ADHD",
                
                # 할 일 편집 다이얼로그
                "Enter task title": "Enter task title",
                "Enter memo or detailed description (optional)": "Enter memo or detailed description (optional)",
                "Delete Task": "Delete Task",
                "Are you sure you want to delete this task?": "Are you sure you want to delete this task?",
                "Edit": "Edit",
                "Delete": "Delete",
                "Move": "Move",
                "No tasks": "No tasks",
                "Project moved up": "Project moved up",
                "Project moved down": "Project moved down",
            }
        }
        
        self._initialized = True
    
    def set_language(self, language: Language) -> None:
        """언어 설정"""
        self._current_language = language
    
    def get_language(self) -> Language:
        """현재 언어 반환"""
        return self._current_language
    
    def tr(self, text: str) -> str:
        """텍스트 번역"""
        translations = self._translations.get(self._current_language, {})
        return translations.get(text, text)


# 전역 번역 서비스 인스턴스
_translation_service = TranslationService()

def tr(text: str) -> str:
    """번역 함수"""
    return _translation_service.tr(text)

def set_language(language: Language) -> None:
    """언어 설정 함수"""
    _translation_service.set_language(language)

def get_language() -> Language:
    """현재 언어 반환 함수"""
    return _translation_service.get_language()