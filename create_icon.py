from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 512x512 크기의 이미지 생성
    size = 512
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 배경 원 그리기
    draw.ellipse([(0, 0), (size, size)], fill=(41, 47, 54))
    
    # 중앙 원 그리기
    center_size = int(size * 0.7)
    center_pos = (size - center_size) // 2
    draw.ellipse([(center_pos, center_pos), 
                 (size - center_pos, size - center_pos)], 
                 fill=(33, 38, 45))  # 더 어두운 색상
    
    # "A" 문자 그리기
    try:
        font = ImageFont.truetype("arial.ttf", int(size * 0.4))
    except:
        font = ImageFont.load_default()
    
    text = "A"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2
    
    # 메인 텍스트
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))
    
    # 아이콘 저장
    image.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])

if __name__ == "__main__":
    create_icon() 