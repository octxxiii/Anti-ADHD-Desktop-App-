from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget, QTextEdit, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Anti-ADHD 도움말")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 탭 위젯 생성
        tab_widget = QTabWidget()
        
        # 기본 사용법 탭
        basic_tab = QWidget()
        basic_layout = QVBoxLayout(basic_tab)
        basic_text = QTextEdit()
        basic_text.setReadOnly(True)
        basic_text.setHtml(self.get_basic_help_content())
        basic_layout.addWidget(basic_text)
        tab_widget.addTab(basic_tab, "기본 사용법")
        
        # 단축키 탭
        shortcuts_tab = QWidget()
        shortcuts_layout = QVBoxLayout(shortcuts_tab)
        shortcuts_text = QTextEdit()
        shortcuts_text.setReadOnly(True)
        shortcuts_text.setHtml(self.get_shortcuts_content())
        shortcuts_layout.addWidget(shortcuts_text)
        tab_widget.addTab(shortcuts_tab, "단축키")
        
        # Pro 기능 탭
        pro_tab = QWidget()
        pro_layout = QVBoxLayout(pro_tab)
        pro_text = QTextEdit()
        pro_text.setReadOnly(True)
        pro_text.setHtml(self.get_pro_features_content())
        pro_layout.addWidget(pro_text)
        tab_widget.addTab(pro_tab, "Pro 기능")
        
        # 라이선스 탭
        license_tab = QWidget()
        license_layout = QVBoxLayout(license_tab)
        license_text = QTextEdit()
        license_text.setReadOnly(True)
        license_text.setHtml(self.get_license_content())
        license_layout.addWidget(license_text)
        tab_widget.addTab(license_tab, "라이선스")
        
        layout.addWidget(tab_widget)
        
        # 닫기 버튼
        close_button = QPushButton("닫기")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
    def get_basic_help_content(self):
        return """
        <h2>Anti-ADHD 기본 사용법</h2>
        
        <h3>프로젝트 관리</h3>
        <ul>
            <li>새 프로젝트 생성: 사이드바의 '+' 버튼 클릭</li>
            <li>프로젝트 이름 변경: 프로젝트 우클릭 → 이름 변경</li>
            <li>프로젝트 삭제: 프로젝트 우클릭 → 삭제</li>
        </ul>
        
        <h3>아이젠하워 매트릭스</h3>
        <ul>
            <li>중요·긴급: 즉시 처리해야 할 일</li>
            <li>중요: 계획하고 우선순위를 정해야 할 일</li>
            <li>긴급: 위임하거나 빠르게 처리해야 할 일</li>
            <li>중요 아님·긴급 아님: 나중에 하거나 삭제할 일</li>
        </ul>
        
        <h3>할 일 관리</h3>
        <ul>
            <li>할 일 추가: 각 사분면의 입력창에 입력 후 Enter</li>
            <li>할 일 수정: 항목 더블클릭</li>
            <li>할 일 삭제: 항목 우클릭 → 삭제</li>
            <li>완료 체크: 체크박스 클릭</li>
        </ul>
        """
        
    def get_shortcuts_content(self):
        return """
        <h2>단축키 목록</h2>
        
        <h3>일반</h3>
        <ul>
            <li>Ctrl + N: 새 프로젝트</li>
            <li>Ctrl + S: 현재 프로젝트 저장</li>
            <li>Ctrl + Q: 프로그램 종료</li>
        </ul>
        
        <h3>할 일 관리</h3>
        <ul>
            <li>Enter: 할 일 추가</li>
            <li>Delete: 선택한 할 일 삭제</li>
            <li>Space: 선택한 할 일 완료/미완료 토글</li>
        </ul>
        
        <h3>프로젝트 관리</h3>
        <ul>
            <li>Ctrl + Tab: 다음 프로젝트</li>
            <li>Ctrl + Shift + Tab: 이전 프로젝트</li>
        </ul>
        """
        
    def get_pro_features_content(self):
        return """
        <h2>Pro 기능 소개</h2>
        
        <h3>무제한 프로젝트</h3>
        <p>프로젝트 수 제한 없이 자유롭게 관리하세요.</p>
        
        <h3>고급 기능</h3>
        <ul>
            <li>태그 시스템: 할 일에 태그를 추가하여 분류</li>
            <li>통계 및 리포트: 프로젝트별 진행 상황 분석</li>
            <li>클라우드 동기화: 여러 기기에서 동기화</li>
            <li>팀 협업: 팀원들과 프로젝트 공유</li>
            <li>데이터 내보내기: PDF/HTML 형식으로 내보내기</li>
            <li>고급 알림: 맞춤형 알림 설정</li>
            <li>커스텀 테마: 원하는 대로 UI 커스터마이징</li>
        </ul>
        
        <h3>가격</h3>
        <ul>
            <li>Personal 라이선스: $29.99 (Product Hunt 할인가: $19.99)</li>
            <li>Team 라이선스: $49.99 (Product Hunt 할인가: $34.99)</li>
        </ul>
        """
        
    def get_license_content(self):
        return """
        <h2>라이선스 정보</h2>
        
        <h3>무료 버전</h3>
        <ul>
            <li>프로젝트 1개</li>
            <li>프로젝트당 할 일 20개</li>
            <li>기본 기능 사용 가능</li>
        </ul>
        
        <h3>Pro 버전</h3>
        <ul>
            <li>무제한 프로젝트</li>
            <li>무제한 할 일</li>
            <li>모든 고급 기능 사용 가능</li>
            <li>1년 무료 업데이트</li>
        </ul>
        
        <h3>라이선스 활성화</h3>
        <p>Pro 버전 구매 후 받은 라이선스 키를 입력하여 활성화하세요.</p>
        
        <h3>환불 정책</h3>
        <p>구매 후 14일 이내 100% 환불 보장</p>
        """ 