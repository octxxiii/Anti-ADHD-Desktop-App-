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
                "Show Main Toolbar": "메인 툴바 보이기",
                "Show Search Toolbar": "검색 툴바 보이기",
                
                # 편집 메뉴
                "Add Task": "할 일 추가",
                "Edit Task": "할 일 수정",
                "Delete Task": "할 일 삭제",
                
                # 도구 메뉴
                "Settings": "설정",
                "Statistics": "통계",
                "Task Statistics": "작업 통계",
                "Export Report": "보고서 내보내기",
                
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
                "Appearance": "외관",
                "Data": "데이터",
                "Shortcuts": "단축키",
                "About": "정보",
                "Language:": "언어:",
                "Theme:": "테마:",
                "System": "시스템",
                "Light": "라이트",
                "Dark": "다크",
                "Auto Save": "자동 저장",
                "Enable Notifications": "알림 사용",
                "Check for Updates": "업데이트 확인",
                "Data Directory": "데이터 디렉토리",
                "Browse": "찾아보기",
                "Backup": "백업",
                "Restore": "복원",
                "Reset": "초기화",
                "Dark Mode": "다크 모드",
                "Window Opacity": "창 투명도",
                "Always on Top": "항상 위",
                "OK": "확인",
                "Cancel": "취소",
                "Korean": "한국어",
                "English": "영어",
                
                # 검색 관련
                "Search": "검색",
                "Search in Title": "제목에서 검색",
                "Search in Details": "내용에서 검색",
                "Include Completed": "완료된 항목 포함",
                
                # 메시지
                "Ready": "준비",
                "Project created": "프로젝트가 생성되었습니다",
                "Project renamed": "프로젝트 이름이 변경되었습니다",
                "Project deleted": "프로젝트가 삭제되었습니다",
                "Task added": "할 일이 추가되었습니다",
                "Task updated": "할 일이 수정되었습니다",
                "Task deleted": "할 일이 삭제되었습니다",
                "Task moved": "할 일이 이동되었습니다",
                
                # 작업 편집 다이얼로그
                "Edit Task": "항목 수정",
                "Title:": "제목:",
                "Details:": "세부 내용:",
                "Due Date:": "마감일:",
                "No Due Date": "마감일 없음",
                "Reminder Time:": "알림 시점:",
                "1 day before": "1일 전",
                "3 hours before": "3시간 전", 
                "1 hour before": "1시간 전",
                "30 minutes before": "30분 전",
                "10 minutes before": "10분 전",
                
                # 통계 다이얼로그
                "Basic Statistics": "기본 통계",
                "Total Tasks:": "전체 작업:",
                "Completed Tasks:": "완료된 작업:",
                "Completion Rate:": "완료율:",
                "Quadrant Statistics": "사분면별 통계",
                "Close": "닫기",
                
                "Are you sure you want to delete this project?": "이 프로젝트를 삭제하시겠습니까?",
                "Are you sure you want to delete this task?": "이 할 일을 삭제하시겠습니까?",
                "Project Name:": "프로젝트 이름:",
                "New Name:": "새 이름:",
                "Task:": "할 일:",
                "Title:": "제목:",
                "Description:": "설명:",
                "Due Date:": "마감일:",
                "Priority:": "우선순위:",
                "High": "높음",
                "Medium": "보통",
                "Low": "낮음",
                "None": "없음",
                "Save": "저장",
                "Close": "닫기",
                
                # 알림 및 팝업
                "Reminder": "알림",
                "Task Due": "할 일 마감",
                "Task Overdue": "할 일 지연",
                "minutes ago": "분 전",
                "hours ago": "시간 전",
                "days ago": "일 전",
                "is due in": "마감까지",
                "is overdue by": "지연",
                
                # 통계 및 보고서
                "Statistics": "통계",
                "Total Tasks": "전체 작업",
                "Completed Tasks": "완료된 작업",
                "Pending Tasks": "대기 중인 작업",
                "Completion Rate": "완료율",
                "Export Report": "보고서 내보내기",
                "Print Report": "보고서 인쇄",
                
                # 도움말
                "Help": "도움말",
                "Version": "버전",
                "Developer": "개발자",
                "License": "라이선스",
                "MIT License": "MIT 라이선스",
                "Anti-ADHD (Eisenhower Matrix)": "Anti-ADHD (아이젠하워 매트릭스)",
                "Program Information": "프로그램 정보",
                "Name": "이름",
                "GitHub Repository": "GitHub 저장소",
                "Enable": "사용",
                "Check on startup": "시작 시 확인",
                "Check Now": "지금 확인",
                "Current Path": "현재 경로",
                "Data Management": "데이터 관리",
                "Backup Data": "데이터 백업",
                "Restore Data": "데이터 복원",
                "Reset Data": "데이터 초기화",
                "Korean": "한국어",
                
                # 애플리케이션 설정
                "Application Settings": "애플리케이션 설정",
                "Show/Hide Project List": "프로젝트 목록 보이기/숨기기",
                "Toggle Dark Mode": "다크 모드 전환",
                "Data backup completed successfully": "데이터 백업이 성공적으로 완료되었습니다",
                "Data restore completed successfully": "데이터 복원이 성공적으로 완료되었습니다",
                "Data reset completed successfully": "데이터 초기화가 성공적으로 완료되었습니다",
                "Data directory changed": "데이터 디렉토리가 변경되었습니다",
                "Please restart the application for the changes to take effect": "변경사항을 적용하려면 애플리케이션을 재시작하세요",
                
                # 투명도 팝업
                "Opacity": "투명도",
                "Transparency": "투명도",
                
                # 프로젝트 관리
                "New Project": "새 프로젝트",
                "Import Project": "프로젝트 가져오기",
                "Save Project": "프로젝트 저장",
                "Save Project As": "다른 이름으로 저장",
                "Rename Project": "프로젝트 이름 변경",
                "Delete Project": "프로젝트 삭제",
                "Enter project name:": "프로젝트 이름을 입력하세요:",
                "Enter new name:": "새 이름을 입력하세요:",
                
                # 작업 편집
                "Edit Task": "작업 편집",
                "Task Title": "작업 제목",
                "Task Description": "작업 설명",
                "Due Date": "마감일",
                "Priority": "우선순위",
                "No Due Date": "마감일 없음",
                "Set Due Date": "마감일 설정",
                "Remove Due Date": "마감일 제거",
                
                # 기타
                "Loading...": "로딩 중...",
                "Saving...": "저장 중...",
                "Error": "오류",
                "Warning": "경고",
                "Information": "정보",
                "Question": "질문",
                "Yes": "예",
                "No": "아니오",
                "All": "모두",
                "Clear": "지우기",
                "Apply": "적용",
                "Reset": "초기화",
                "Default": "기본값",
                "Custom": "사용자 정의",
                "Warning": "경고",
                "Project name already exists.": "이미 존재하는 프로젝트 이름입니다.",
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
                "Show Main Toolbar": "Show Main Toolbar",
                "Show Search Toolbar": "Show Search Toolbar",
                
                # 편집 메뉴
                "Add Task": "Add Task",
                "Edit Task": "Edit Task",
                "Delete Task": "Delete Task",
                
                # 도구 메뉴
                "Settings": "Settings",
                "Statistics": "Statistics",
                "Task Statistics": "Task Statistics",
                "Export Report": "Export Report",
                
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
                "Appearance": "Appearance",
                "Data": "Data",
                "Shortcuts": "Shortcuts",
                "About": "About",
                "Language:": "Language:",
                "Theme:": "Theme:",
                "System": "System",
                "Light": "Light",
                "Dark": "Dark",
                "Auto Save": "Auto Save",
                "Enable Notifications": "Enable Notifications",
                "Check for Updates": "Check for Updates",
                "Data Directory": "Data Directory",
                "Browse": "Browse",
                "Backup": "Backup",
                "Restore": "Restore",
                "Reset": "Reset",
                "Dark Mode": "Dark Mode",
                "Window Opacity": "Window Opacity",
                "Always on Top": "Always on Top",
                "OK": "OK",
                "Cancel": "Cancel",
                
                # 검색 관련
                "Search": "Search",
                "Search in Title": "Search in Title",
                "Search in Details": "Search in Details",
                "Include Completed": "Include Completed",
                
                # 메시지
                "Ready": "Ready",
                "Project created": "Project created",
                "Project renamed": "Project renamed",
                "Project deleted": "Project deleted",
                "Task added": "Task added",
                "Task updated": "Task updated",
                "Task deleted": "Task deleted",
                "Task moved": "Task moved",
                
                # 작업 편집 다이얼로그
                "Edit Task": "Edit Task",
                "Title:": "Title:",
                "Details:": "Details:",
                "Due Date:": "Due Date:",
                "No Due Date": "No Due Date",
                "Reminder Time:": "Reminder Time:",
                "1 day before": "1 day before",
                "3 hours before": "3 hours before", 
                "1 hour before": "1 hour before",
                "30 minutes before": "30 minutes before",
                "10 minutes before": "10 minutes before",
                
                # 통계 다이얼로그
                "Basic Statistics": "Basic Statistics",
                "Total Tasks:": "Total Tasks:",
                "Completed Tasks:": "Completed Tasks:",
                "Completion Rate:": "Completion Rate:",
                "Quadrant Statistics": "Quadrant Statistics",
                "Close": "Close",
                
                "Are you sure you want to delete this project?": "Are you sure you want to delete this project?",
                "Are you sure you want to delete this task?": "Are you sure you want to delete this task?",
                "Project Name:": "Project Name:",
                "New Name:": "New Name:",
                "Task:": "Task:",
                "Title:": "Title:",
                "Description:": "Description:",
                "Due Date:": "Due Date:",
                "Priority:": "Priority:",
                "High": "High",
                "Medium": "Medium",
                "Low": "Low",
                "None": "None",
                "Save": "Save",
                "Close": "Close",
                
                # 알림 및 팝업
                "Reminder": "Reminder",
                "Task Due": "Task Due",
                "Task Overdue": "Task Overdue",
                "minutes ago": "minutes ago",
                "hours ago": "hours ago",
                "days ago": "days ago",
                "is due in": "is due in",
                "is overdue by": "is overdue by",
                
                # 통계 및 보고서
                "Statistics": "Statistics",
                "Total Tasks": "Total Tasks",
                "Completed Tasks": "Completed Tasks",
                "Pending Tasks": "Pending Tasks",
                "Completion Rate": "Completion Rate",
                "Export Report": "Export Report",
                "Print Report": "Print Report",
                
                # 도움말
                "Help": "Help",
                "Version": "Version",
                "Developer": "Developer",
                "License": "License",
                "MIT License": "MIT License",
                "Anti-ADHD (Eisenhower Matrix)": "Anti-ADHD (Eisenhower Matrix)",
                "Program Information": "Program Information",
                "Name": "Name",
                "GitHub Repository": "GitHub Repository",
                "Enable": "Enable",
                "Check on startup": "Check on startup",
                "Check Now": "Check Now",
                "Current Path": "Current Path",
                "Data Management": "Data Management",
                "Backup Data": "Backup Data",
                "Restore Data": "Restore Data",
                "Reset Data": "Reset Data",
                "Korean": "Korean",
                
                # 애플리케이션 설정
                "Application Settings": "Application Settings",
                "Show/Hide Project List": "Show/Hide Project List",
                "Toggle Dark Mode": "Toggle Dark Mode",
                "Data backup completed successfully": "Data backup completed successfully",
                "Data restore completed successfully": "Data restore completed successfully",
                "Data reset completed successfully": "Data reset completed successfully",
                "Data directory changed": "Data directory changed",
                "Please restart the application for the changes to take effect": "Please restart the application for the changes to take effect",
                
                # 투명도 팝업
                "Opacity": "Opacity",
                "Transparency": "Transparency",
                
                # 프로젝트 관리
                "New Project": "New Project",
                "Import Project": "Import Project",
                "Save Project": "Save Project",
                "Save Project As": "Save Project As",
                "Rename Project": "Rename Project",
                "Delete Project": "Delete Project",
                "Enter project name:": "Enter project name:",
                "Enter new name:": "Enter new name:",
                
                # 작업 편집
                "Edit Task": "Edit Task",
                "Task Title": "Task Title",
                "Task Description": "Task Description",
                "Due Date": "Due Date",
                "Priority": "Priority",
                "No Due Date": "No Due Date",
                "Set Due Date": "Set Due Date",
                "Remove Due Date": "Remove Due Date",
                
                # 기타
                "Loading...": "Loading...",
                "Saving...": "Saving...",
                "Error": "Error",
                "Warning": "Warning",
                "Information": "Information",
                "Question": "Question",
                "Yes": "Yes",
                "No": "No",
                "All": "All",
                "Clear": "Clear",
                "Apply": "Apply",
                "Reset": "Reset",
                "Default": "Default",
                "Custom": "Custom",
                "Warning": "Warning",
                "Project name already exists.": "Project name already exists.",
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