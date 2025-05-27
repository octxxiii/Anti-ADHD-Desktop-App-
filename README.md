# Anti-ADHD (Eisenhower Matrix 기반 생산성 도구)

## 소개

**Anti-ADHD**는 Eisenhower 매트릭스(중요/긴급 사분면)를 기반으로 한 직관적이고 강력한 생산성 관리 데스크탑 앱입니다. 프로젝트별 할 일 관리, 마감/알림, 다크모드, 자동 백업 등 실전 업무에 최적화된 기능을 제공합니다.

> "중요한 일에 집중하고, 급한 일에 휘둘리지 마세요."

---

## 주요 기능

- **Eisenhower Matrix**: 4분면(중요·긴급/중요/긴급/중요 아님·긴급 아님) 기반 할 일 관리
- **프로젝트별 관리**: 프로젝트 생성/이름변경/삭제, 데이터 자동 저장
- **마감일 & 알림**: D-Day, 마감 임박/경과 알림, 커스텀 알림 시점
- **다크모드 지원**: 라이트/다크 테마 전환
- **자동 백업/복원**: 5분마다 자동 백업, 백업에서 복원
- **검색/필터**: 제목·세부내용·완료여부로 실시간 검색
- **설정 UI**: 데이터 경로, 자동저장, 업데이트 등 설정 대화상자
- **직관적 UX**: 키보드 단축키, 드래그&드롭, 상태바 피드백, 접근성 강화

---

## 설치 및 실행

### 1. Python 환경에서 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
python anti_adhd_pyqt.py
```

### 2. 빌드된 실행파일(Windows)
- (빌드 산출물은 git에 포함되지 않음)
- 직접 빌드하려면 PyInstaller 사용:

```bash
pyinstaller --noconfirm --windowed --icon=icon.ico anti_adhd_pyqt.py
```

---

## 폴더 구조

```
antiadhd2/
├── anti_adhd_pyqt.py      # 메인 애플리케이션 (곧 분할 예정)
├── requirements.txt       # 의존성 목록
├── README.md              # 이 문서
├── LICENSE                # MIT 라이선스
├── docs/                  # 사용자/개발자 문서
├── scripts/               # 빌드/유틸 스크립트
└── ... (불필요한 산출물은 .gitignore로 관리)
```

---

## 단축키/사용법

- **Ctrl+N**: 새 프로젝트
- **Ctrl+S**: 현재 프로젝트 저장
- **Ctrl+Shift+S**: 다른 이름으로 저장
- **Ctrl+R**: 프로젝트 이름 변경
- **Delete**: 프로젝트 삭제
- **Ctrl+B**: 사이드바 토글
- **Ctrl+Shift+B**: 메인 툴바 토글
- **Ctrl+Shift+F**: 검색 툴바 토글
- **Ctrl+Comma(,)**: 설정 열기
- **Ctrl+Z**: 백업에서 복원

---

## 기여 가이드

1. **이슈 등록**: 버그/기능요청/질문은 GitHub Issues에 남겨주세요.
2. **포크 & 브랜치**: main 브랜치에서 포크 후, 기능별 브랜치 생성 권장
3. **PR 작성**: 명확한 제목/설명, 관련 이슈 링크
4. **코드 스타일**: 가독성, 주석, 함수 분리, 한글 주석 환영
5. **테스트**: 주요 기능은 직접 실행 테스트 권장

---

## 라이선스

MIT License (자유롭게 사용/수정/배포 가능, 단 저작권 고지 유지)

---

## 문의/연락

- GitHub: [octaxii/antiadhd2](https://github.com/octxxiii/antiadhd2)
- 이메일: octaxii@gmail.com

---

> **이 프로젝트는 누구나 기여할 수 있습니다.**
> 피드백, 버그 제보, 기능 제안 모두 환영합니다!
