import os
import json
import shutil
from datetime import datetime
from typing import Any, Dict, List

PROJECT_FILE_SUFFIX = ".json"

# --- 프로젝트 데이터 저장 ---
def save_project_to_file(data_dir: str, project_name: str, project_data: dict) -> None:
    file_path = os.path.join(data_dir, f"{project_name}{PROJECT_FILE_SUFFIX}")
    project_data["updated_at"] = datetime.now().isoformat()
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)

# --- 프로젝트 데이터 로드 ---
def load_project_from_file(data_dir: str, project_name: str) -> dict:
    file_path = os.path.join(data_dir, f"{project_name}{PROJECT_FILE_SUFFIX}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        project_data = json.load(f)
    validate_project_data(project_data)
    return project_data

# --- 프로젝트 파일 목록 ---
def list_project_files(data_dir: str) -> List[str]:
    return [f[:-5] for f in os.listdir(data_dir) if f.endswith(PROJECT_FILE_SUFFIX)]

# --- 데이터 검증 ---
def validate_project_data(project_data: dict) -> None:
    if not isinstance(project_data, dict):
        raise ValueError("잘못된 프로젝트 데이터 형식")
    if "quadrants" not in project_data:
        raise ValueError("프로젝트 데이터에 quadrants가 없습니다")
    if not isinstance(project_data["quadrants"], list) or len(project_data["quadrants"]) != 4:
        raise ValueError("잘못된 quadrants 데이터 형식")

# --- 백업 ---
def backup_project_file(data_dir: str, project_name: str, backup_dir: str) -> str:
    src = os.path.join(data_dir, f"{project_name}{PROJECT_FILE_SUFFIX}")
    if not os.path.exists(src):
        raise FileNotFoundError(src)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(backup_dir, f"{project_name}_{timestamp}{PROJECT_FILE_SUFFIX}")
    shutil.copy2(src, dst)
    return dst

# --- 복원 ---
def restore_project_file(data_dir: str, project_name: str, backup_file: str) -> None:
    dst = os.path.join(data_dir, f"{project_name}{PROJECT_FILE_SUFFIX}")
    shutil.copy2(backup_file, dst) 