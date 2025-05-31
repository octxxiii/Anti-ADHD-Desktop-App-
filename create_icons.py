from PIL import Image, ImageDraw, ImageFont
import os

def create_calendar_icon():
    # 16x16 크기의 캘린더 아이콘 생성
    size = 16
    icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # 캘린더 외곽선
    draw.rectangle([1, 1, size-2, size-2], outline=(52, 152, 219), width=1)
    
    # 상단 바
    draw.rectangle([1, 1, size-2, 4], fill=(52, 152, 219))
    
    # 날짜 표시
    try:
        font = ImageFont.truetype("arial.ttf", 8)
    except:
        font = ImageFont.load_default()
    draw.text((6, 6), "15", fill=(52, 152, 219), font=font)
    
    # 아이콘 저장
    os.makedirs("icons", exist_ok=True)
    icon.save("icons/calendar.png")
    print("캘린더 아이콘이 생성되었습니다.")

def create_note_icon():
    # 16x16 크기의 노트 아이콘 생성
    size = 16
    icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # 노트 모양
    draw.rectangle([1, 1, size-2, size-2], outline=(52, 152, 219), width=1)
    
    # 선 그리기
    for y in range(4, size-2, 3):
        draw.line([3, y, size-3, y], fill=(52, 152, 219), width=1)
    
    # 아이콘 저장
    os.makedirs("icons", exist_ok=True)
    icon.save("icons/note.png")
    print("노트 아이콘이 생성되었습니다.")

if __name__ == "__main__":
    create_calendar_icon()
    create_note_icon() 