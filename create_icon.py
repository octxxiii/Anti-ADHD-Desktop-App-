from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 기본 크기를 256x256으로 시작
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 원 크기 계산
    padding = size // 16
    circle_bbox = [padding, padding, size - padding, size - padding]
    
    # 파란색 원 그리기 (#0078d7 - Windows 10 기본 파란색)
    draw.ellipse(circle_bbox, fill='#0078d7')
    
    # 폰트 크기 계산 (원 크기의 약 60%)
    font_size = int(size * 0.6)
    try:
        # Windows 기본 폰트
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            # Windows 기본 볼드 폰트
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # "A" 문자 그리기 (중앙 정렬)
    text = "A"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - (size // 16)  # 약간 위로 조정
    
    # 흰색으로 "A" 문자 그리기
    draw.text((x, y), text, fill='white', font=font)
    
    # 여러 크기로 아이콘 저장
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icon_images = []
    
    for icon_size in sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        icon_images.append(resized)
    
    # 임시 파일들 생성
    temp_files = []
    for i, image in enumerate(icon_images):
        temp_file = f'temp_icon_{i}.png'
        image.save(temp_file, 'PNG')
        temp_files.append(temp_file)
    
    # 아이콘 파일로 저장
    icon_images[0].save('icon.ico', format='ICO', sizes=sizes)
    
    # 임시 파일 삭제
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except:
            pass

if __name__ == "__main__":
    create_icon() 