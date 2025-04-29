from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 32x32 크기의 투명 배경 이미지 생성
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 파란색 원 그리기
    draw.ellipse([2, 2, 30, 30], fill='#0078d7')
    
    # 폰트 설정 (더 크고 두꺼운 폰트)
    try:
        font = ImageFont.truetype("arial.ttf", 24)  # 폰트 크기를 24로 증가
    except:
        font = ImageFont.load_default()
    
    # "A" 문자 그리기 (중앙 정렬)
    text = "A"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (32 - text_width) // 2
    y = (32 - text_height) // 2 - 2  # 약간 위로 조정
    
    # 흰색으로 "A" 문자 그리기
    draw.text((x, y), text, fill='white', font=font)
    
    # 아이콘 파일로 저장
    img.save('icon.ico', format='ICO')

if __name__ == "__main__":
    create_icon() 