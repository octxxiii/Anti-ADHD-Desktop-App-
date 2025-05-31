"""
test.py

- pytest 등 테스트 자동 실행
- 사용법: python scripts/test.py
"""
import subprocess
import sys

def main():
    code = subprocess.call(['pytest'] + sys.argv[1:])
    sys.exit(code)

if __name__ == '__main__':
    main() 