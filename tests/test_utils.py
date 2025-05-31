"""
core/utils.py 테스트
"""
import pytest
from datetime import datetime, timedelta
from core.utils import (
    format_date,
    calculate_days_remaining,
    is_valid_date,
    sanitize_filename
)

def test_format_date():
    """날짜 포맷 테스트"""
    date = datetime(2024, 3, 15)
    assert format_date(date) == "2024-03-15"
    
    # None 입력 처리
    assert format_date(None) == ""

def test_calculate_days_remaining():
    """남은 일수 계산 테스트"""
    today = datetime.now()
    future_date = today + timedelta(days=5)
    past_date = today - timedelta(days=5)
    
    assert calculate_days_remaining(future_date) == 5
    assert calculate_days_remaining(past_date) == -5
    assert calculate_days_remaining(None) == 0

def test_is_valid_date():
    """날짜 유효성 검사 테스트"""
    valid_date = datetime.now()
    assert is_valid_date(valid_date) is True
    
    # 잘못된 입력
    assert is_valid_date(None) is False
    assert is_valid_date("invalid") is False

def test_sanitize_filename():
    """파일명 정리 테스트"""
    # 기본 케이스
    assert sanitize_filename("test file.txt") == "test_file.txt"
    
    # 특수문자 제거
    assert sanitize_filename("file*name?.txt") == "filename.txt"
    
    # 공백 처리
    assert sanitize_filename("  spaces  .txt") == "spaces.txt"
    
    # 빈 문자열 처리
    assert sanitize_filename("") == "untitled"
    
    # None 처리
    assert sanitize_filename(None) == "untitled" 