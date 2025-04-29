from PIL import Image, ImageDraw

def create_icon():
    # 64x64 크기의 이미지 생성
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 4개의 사분면 그리기
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    for i in range(4):
        x = (i % 2) * 32
        y = (i // 2) * 32
        draw.rectangle([x, y, x+32, y+32], fill=colors[i])
    
    # 체크 표시 추가
    for i in range(4):
        x = (i % 2) * 32 + 16
        y = (i // 2) * 32 + 16
        draw.line([x-8, y, x, y+8, x+8, y-8], fill=(255, 255, 255), width=2)
    
    # 이미지 저장
    img.save('checklist_icon.ico')

if __name__ == "__main__":
    create_icon() 