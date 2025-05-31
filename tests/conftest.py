"""
pytest 설정 및 공통 fixture
"""
import pytest
import os
import tempfile
from pathlib import Path
from PyQt5.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    """Qt 애플리케이션 fixture"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

@pytest.fixture
def temp_data_dir():
    """임시 데이터 디렉토리 생성"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_todo_data():
    """샘플 할 일 데이터"""
    return {
        "quadrant1": [
            {"text": "긴급 보고서 작성", "done": False},
            {"text": "중요 미팅 준비", "done": True}
        ],
        "quadrant2": [
            {"text": "자기계발 계획", "done": False}
        ],
        "quadrant3": [
            {"text": "일상 업무 처리", "done": False}
        ],
        "quadrant4": [
            {"text": "불필요한 회의", "done": True}
        ]
    } 