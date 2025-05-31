# Anti-ADHD 데이터 저장 구조

## 기본 구조
```
%APPDATA%/Anti-ADHD/
├── projects/              # 프로젝트 데이터
│   ├── project_*.json    # 각 프로젝트별 JSON 파일
│   └── .backup/          # 자동 백업 파일
├── settings.json         # 앱 설정
└── logs/                 # 로그 파일
```

## 프로젝트 데이터 구조 (project_*.json)
```json
{
    "name": "프로젝트명",
    "created_at": "2024-03-21T10:00:00",
    "last_modified": "2024-03-21T15:30:00",
    "tasks": [
        // 4분면별 할 일 목록
        [
            {
                "title": "할 일 제목",
                "details": "상세 내용",
                "checked": false,
                "due_date": "2024-03-22T18:00:00",
                "reminders": [
                    {
                        "time": "2024-03-22T17:00:00",
                        "notified": false
                    }
                ],
                "created_at": "2024-03-21T10:00:00",
                "modified_at": "2024-03-21T15:30:00"
            }
        ]
    ]
}
```

## 설정 파일 구조 (settings.json)
```json
{
    "data_dir": "%APPDATA%/Anti-ADHD",
    "auto_save": true,
    "auto_save_interval": 5,
    "dark_mode": false,
    "window_opacity": 1.0,
    "always_on_top": false,
    "check_updates": true,
    "last_update_check": "2024-03-21T10:00:00"
}
```

## 백업 구조
- 자동 백업: 5분마다 수행
- 백업 파일명: `project_[이름]_[YYYYMMDD_HHMMSS].json`
- 최대 백업 수: 10개
- 백업 위치: `%APPDATA%/Anti-ADHD/projects/.backup/`

## 로그 구조
- 로그 파일명: `app_[YYYYMMDD].log`
- 로그 위치: `%APPDATA%/Anti-ADHD/logs/`
- 로그 보관 기간: 30일 