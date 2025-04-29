# Anti-ADHD

아이젠하워 매트릭스를 기반으로 한 할 일 관리 프로그램입니다.

## 주요 기능

- 4분면 매트릭스 기반 할 일 관리
- 항목별 상세 내용 작성
- 자동/수동 데이터 저장
- 창 고정 및 투명도 조절
- 체크리스트 프린트
- 자동 업데이트 체크

## 설치 방법

1. [릴리즈 페이지](https://github.com/octxxiii/Anti-ADHD/releases)에서 최신 버전을 다운로드합니다.
2. 다운로드한 실행 파일을 실행합니다.

## 사용 방법

자세한 사용 방법은 [사용자 가이드](https://octxxiii.github.io/Anti-ADHD/)를 참고하세요.

## 개발 환경 설정

1. Python 3.8 이상 설치
2. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```
3. 실행:
   ```bash
   python anti_adhd.py
   ```

## 빌드 방법

```bash
pyinstaller --onefile --windowed --icon=icon.ico anti_adhd.py
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
