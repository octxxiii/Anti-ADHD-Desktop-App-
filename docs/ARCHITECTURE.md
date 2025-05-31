# 프로젝트 아키텍처 및 구조

## 📁 폴더 구조

```
antiadhd2/
├── core/                # 데이터, 상수, 유틸 등 비-UI 로직
│   ├── data.py          # 데이터 저장/로드/백업/복원/검증 (pure function)
│   ├── constants.py     # 상수 정의
│   └── utils.py         # 범용 유틸리티 함수
├── ui/                  # 모든 UI 컴포넌트 및 창
│   ├── main_window.py   # MainWindow 클래스 (앱 진입점)
│   ├── eisenhower.py    # EisenhowerQuadrantWidget (매트릭스)
│   ├── project_list.py  # ProjectListWidget (프로젝트/할 일 리스트)
│   ├── settings.py      # SettingsDialog (설정 창)
│   └── opacity_popup.py # OpacityPopup (투명도 팝업)
├── scripts/             # 빌드/버전/아이콘 등 자동화 스크립트
│   ├── create_icon.py   # 아이콘 생성
│   ├── version_update.py# 버전 자동화
│   ├── build.py         # 빌드 자동화 (예정)
│   └── test.py          # 테스트 자동화 (예정)
├── docs/                # 문서 및 MkDocs 설정
│   ├── index.md         # 소개/설치/실행법
│   ├── user-guide.md    # 통합 사용 가이드
│   ├── troubleshooting.md # 문제 해결
│   ├── faq.md           # FAQ
│   └── ...
├── main.py              # 앱 실행 진입점
├── requirements.txt     # Python 의존성 명세
└── pyproject.toml       # (선택) 빌드/버전 관리
```

## 🧩 주요 모듈 역할

- **core/**: 데이터 계층, pure function, 비-UI 로직, 테스트 용이
- **ui/**: 모든 PyQt 위젯/창, UI 상태/이벤트 관리
- **scripts/**: 빌드, 버전, 테스트 등 자동화
- **docs/**: 사용자/개발자 문서, MkDocs 기반

## 🔗 의존성
- Python 3.9+
- PyQt5
- (테스트) pytest
- (빌드) pyinstaller
- (문서) mkdocs, mkdocs-material

## 🧪 테스트/확장/배포
- **테스트**: core/ 함수 단위 테스트, scripts/test.py로 자동화 예정
- **확장**: UI/데이터 계층 완전 분리, 신규 기능은 별도 파일/클래스로 추가
- **배포**: pyinstaller로 단일 실행 파일 빌드, scripts/build.py로 자동화 예정

## 🛡️ 유지보수/품질 원칙
- UI/비UI 계층 분리, pure function 우선
- 문서/스크립트 자동화, 코드 일관성
- 모든 사용자 입력/상호작용에 즉각적 피드백 제공
- 접근성/반응성/미학적 일관성 준수

---

> 구조/아키텍처 관련 문의는 언제든 [이슈](https://github.com/octxxiii/Anti-ADHD/issues)로 남겨주세요. 