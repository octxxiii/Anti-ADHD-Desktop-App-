# Anti-ADHD

> 아이젠하워 매트릭스로 ADHD를 이기는 할 일 관리 프로그램

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __빠른 시작__

    ---

    [:octicons-download-24: 다운로드](https://github.com/octxxiii/Anti-ADHD/releases/latest){ .md-button }
    [:octicons-book-24: 사용법](user-guide.md){ .md-button }

    **설치/실행법**
    1. Python 3.9+ 설치
    2. `requirements.txt` 설치:  
       `pip install -r requirements.txt`
    3. 프로그램 실행:  
       `python main.py`
    4. (선택) 빌드:  
       `pyinstaller --onefile --windowed main.py`

-   :material-lightbulb:{ .lg .middle } __주요 기능__

    ---

    - 🎯 아이젠하워 매트릭스
    - 📌 항상 위
    - 🔍 투명도 조절
    - 💾 자동 저장
    - 🔄 자동 업데이트

-   :material-help:{ .lg .middle } __도움말__

    ---

    [:octicons-question-24: FAQ](faq.md){ .md-button }
    [:octicons-bug-24: 문제 해결](troubleshooting.md){ .md-button }

</div>

## 🚀 시작하기

1. [릴리즈 페이지](https://github.com/octxxiii/Anti-ADHD/releases/latest)에서 최신 버전의 `anti_adhd.exe` 다운로드
2. 또는 소스코드 직접 실행:
    - Python 3.9+ 설치
    - `pip install -r requirements.txt`
    - `python main.py`
3. 프로그램을 실행하고 할 일을 관리하세요!

!!! note "지원 환경"
    현재 Windows 운영체제만 지원합니다.

## 🎨 사용법

=== "할 일 추가"
    - 각 분면의 입력창에 할 일을 입력하고 Enter 키를 누르거나 추가 버튼을 클릭
    - 중요도와 긴급도에 따라 적절한 분면을 선택

=== "할 일 관리"
    - 체크박스로 완료된 할 일을 표시
    - 더블 클릭으로 할 일의 내용을 수정
    - 우클릭 메뉴로 상세보기, 수정, 삭제 가능

=== "설정"
    - ⚙️ 버튼을 클릭하여 설정 창 열기
    - 투명도, 항상 위 등 설정 가능

## 👨‍💻 개발자 및 라이선스

<div class="grid" markdown style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">

-   [:octicons-mark-github-16: GitHub](https://github.com/octxxiii){ .md-button .md-button--small }
-   [:octicons-mail-16: 이메일](mailto:kdyw123@gmail.com){ .md-button .md-button--small }
-   [:octicons-law-16: MIT License](https://github.com/octxxiii/Anti-ADHD/blob/main/LICENSE){ .md-button .md-button--small }

</div>

## 🤝 기여하기

프로젝트에 기여하고 싶으신가요? 언제든 환영합니다!

1. 이 저장소를 포크
2. 새로운 브랜치 생성
3. 변경사항을 커밋
4. 브랜치를 푸시
5. Pull Request 생성

## 최근 변경사항 (v1.0.1)

=== "UI 개선"
    - 설정 창 크기 및 위치 최적화
    - 여백 조정으로 더 컴팩트한 레이아웃
    - 정보 탭 스크롤 기능 추가
    - 이메일과 GitHub 링크 클릭 가능하도록 개선

=== "기능 개선"
    - 자동 업데이트 기능 추가
      - GitHub 릴리즈 기반 버전 체크
      - 자동 다운로드 및 설치 지원
    - 데이터 관리 개선
      - 프로그램 시작 시 자동 불러오기 알림 제거
      - 설정 창에서 수동 불러오기 시에만 알림 표시 