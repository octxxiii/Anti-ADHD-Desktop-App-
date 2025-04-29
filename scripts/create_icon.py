from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 32x32 크기의 투명한 이미지 생성
    img = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 원 그리기 (파란색)
    draw.ellipse([2, 2, 30, 30], fill='#1E90FF')
    
    # 텍스트 추가 (흰색 'A')
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = "A"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (32 - text_width) // 2
    y = (32 - text_height) // 2 - 2
    draw.text((x, y), text, fill='white', font=font)
    
    # ICO 파일로 저장
    img.save("app_icon.ico", format='ICO', sizes=[(32, 32)])

if __name__ == "__main__":
    create_icon() 