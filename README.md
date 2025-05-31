# Anti-ADHD

> 아이젠하워 매트릭스 기반 할 일 관리 앱 (PyQt)

## 🚀 설치 및 실행

1. Python 3.9+ 설치
2. `pip install -r requirements.txt`
3. `python main.py` 실행
4. (선택) 빌드: `pyinstaller --onefile --windowed main.py`

## 📚 문서
- [사용 가이드](docs/user-guide.md)
- [문제 해결](docs/troubleshooting.md)
- [FAQ](docs/faq.md)
- [아키텍처/구조](docs/ARCHITECTURE.md)

## 🛠️ 자동화 스크립트
- 버전 업데이트: `python scripts/version_update.py [--patch|--minor|--major]`
- 빌드: `python scripts/build.py [--docs|--app|--all]`
- 테스트: `python scripts/test.py`

## 🤝 기여/테스트
- core/ 함수 단위 테스트 권장
- scripts/test.py로 전체 테스트 자동화

## 📁 폴더 구조

(자세한 구조는 [ARCHITECTURE.md](docs/ARCHITECTURE.md) 참고)

## 라이선스
MIT License
