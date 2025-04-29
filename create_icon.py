from PIL import Image, ImageDraw, ImageFont
import os

try:
    print("아이콘 생성 시작...")
    
    # 32x32 크기의 이미지 생성
    img = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))
    print("이미지 생성 완료")
    
    draw = ImageDraw.Draw(img)
    print("드로잉 객체 생성 완료")
    
    # 배경 원 그리기 (진한 파란색)
    draw.ellipse([2, 2, 30, 30], fill='#1E90FF')
    print("배경 원 그리기 완료")
    
    # 'A' 문자 그리기 (흰색)
    try:
        # Windows 기본 폰트
        font = ImageFont.truetype('arial.ttf', 20)
        print("Arial 폰트 로드 완료")
    except:
        # 폰트를 찾을 수 없는 경우 기본 폰트 사용
        print("Arial 폰트를 찾을 수 없어 기본 폰트 사용")
        font = ImageFont.load_default()
    
    # 텍스트 중앙 정렬을 위한 위치 계산
    text = 'A'
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (32 - text_width) // 2
    y = (32 - text_height) // 2 - 2  # 약간 위로 조정
    print("텍스트 위치 계산 완료")
    
    # 흰색으로 'A' 그리기
    draw.text((x, y), text, fill='white', font=font)
    print("텍스트 그리기 완료")
    
    # docs/images 디렉토리 생성
    os.makedirs('docs/images', exist_ok=True)
    
    # PNG로 저장
    img.save('docs/images/icon.png')
    print("아이콘 파일 저장 완료")
    
    print("\n아이콘이 성공적으로 생성되었습니다!")
    
except Exception as e:
    print(f"\n오류 발생: {str(e)}") 