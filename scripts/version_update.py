"""
version_update.py

- pyproject.toml, README.md, main.py 등에서 버전 문자열을 자동으로 찾아 증가/치환
- 사용법: python scripts/version_update.py [--patch|--minor|--major]
- 기본은 patch 증가
"""
import re
import sys
from pathlib import Path

FILES = [
    Path('pyproject.toml'),
    Path('README.md'),
    Path('main.py'),
]

VERSION_PATTERN = re.compile(r'(\d+)\.(\d+)\.(\d+)')


def bump_version(version, mode='patch'):
    major, minor, patch = map(int, version.split('.'))
    if mode == 'major':
        major += 1
        minor = 0
        patch = 0
    elif mode == 'minor':
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def find_and_replace_version(text, new_version):
    return VERSION_PATTERN.sub(new_version, text, count=1)


def main():
    mode = 'patch'
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--major', '--minor', '--patch']:
            mode = sys.argv[1][2:]

    # 첫 파일에서 버전 추출
    for file in FILES:
        if file.exists():
            content = file.read_text(encoding='utf-8')
            m = VERSION_PATTERN.search(content)
            if m:
                old_version = m.group(0)
                break
    else:
        print('버전 문자열을 찾을 수 없습니다.')
        sys.exit(1)

    new_version = bump_version(old_version, mode)
    print(f"버전: {old_version} → {new_version}")

    for file in FILES:
        if file.exists():
            content = file.read_text(encoding='utf-8')
            new_content = find_and_replace_version(content, new_version)
            file.write_text(new_content, encoding='utf-8')
            print(f"{file} 업데이트 완료")

if __name__ == '__main__':
    main() 