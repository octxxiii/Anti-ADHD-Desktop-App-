import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import base64
from PIL import Image, ImageDraw, ImageFont
import io

class QuadrantChecklist:
    def __init__(self, root):
        self.root = root
        self.root.title("ANTI ADHD")
        self.root.geometry("800x600")
        
        # 아이콘 생성 및 설정
        try:
            # 32x32 크기의 이미지 생성
            img = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 배경 원 그리기 (진한 파란색)
            draw.ellipse([2, 2, 30, 30], fill='#1E90FF')
            
            # 'A' 문자 그리기 (흰색)
            try:
                # Windows 기본 폰트
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                # 폰트를 찾을 수 없는 경우 기본 폰트 사용
                font = ImageFont.load_default()
            
            # 텍스트 중앙 정렬을 위한 위치 계산
            text = "A"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            x = (32 - text_width) // 2
            y = (32 - text_height) // 2 - 2  # 약간 위로 조정
            
            # 흰색으로 'A' 그리기
            draw.text((x, y), text, fill='white', font=font)
            
            # 임시 PNG 파일로 저장 후 ICO로 변환
            temp_png = "temp_icon.png"
            temp_ico = "temp_icon.ico"
            
            img.save(temp_png)
            
            # PNG를 ICO로 변환
            ico_img = Image.open(temp_png)
            ico_img.save(temp_ico, format='ICO', sizes=[(32, 32)])
            
            # 아이콘 설정
            self.root.iconbitmap(temp_ico)
            
            # 임시 파일 삭제
            try:
                os.remove(temp_png)
                os.remove(temp_ico)
            except:
                pass
        except Exception as e:
            print(f"아이콘 설정 중 오류 발생: {str(e)}")
        
        # 그리드 가중치 설정 - 더 큰 가중치 부여
        for i in range(2):
            root.grid_rowconfigure(i, weight=3)  # 상단 행들의 가중치 증가
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(2, weight=1)  # 하단 버튼 행의 가중치
        
        # 데이터 저장 파일 경로
        self.data_file = "checklist_data.json"
        
        # 불투명도와 고정 상태 변수
        self.opacity = 1
        self.is_pinned = True  # 기본값을 True로 변경
        
        # 4개의 프레임 생성
        self.frames = []
        self.lists = []
        self.entries = []
        self.memos = [{}, {}, {}, {}]  # 각 항목의 메모를 저장할 딕셔너리
        
        # 현재 활성화된 입력 필드 인덱스 추가
        self.active_entry = 0
        
        # 윈도우 포커스 이벤트 바인딩
        self.root.bind("<FocusIn>", self.handle_window_focus)
        # 윈도우 표시 이벤트 바인딩
        self.root.bind("<Map>", self.handle_window_map)
        # 윈도우가 처음 표시될 때 포커스 강제 설정
        self.root.focus_force()
        
        # 카테고리 이름
        categories = ["긴급하고 중요한 일", "긴급하지 않지만 중요한 일", 
                     "긴급하지만 중요하지 않은 일", "긴급하지도 중요하지도 않은 일"]
        
        # 우클릭 메뉴 생성
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="상세보기", command=self.show_memo)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="수정", command=self.edit_item)
        self.context_menu.add_command(label="삭제", command=self.delete_selected_item)
        
        # 각 카테고리별 프레임 생성
        for i in range(4):
            frame = ttk.LabelFrame(root, text=categories[i])
            frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            self.frames.append(frame)
            
            # 체크리스트 리스트박스
            listbox_frame = ttk.Frame(frame)
            listbox_frame.pack(padx=5, pady=5, fill="both", expand=True)
            
            listbox = tk.Listbox(listbox_frame, selectmode="single")
            scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
            listbox.configure(yscrollcommand=scrollbar.set)
            
            listbox.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.lists.append(listbox)
            
            # 리스트박스 이벤트 바인딩
            listbox.bind("<Button-3>", lambda e, idx=i: self.show_context_menu(e, idx))
            listbox.bind("<Button-1>", lambda e, idx=i: self.handle_click(e, idx))
            listbox.bind("<Double-Button-1>", lambda e, idx=i: self.show_memo())
            
            # 입력 필드와 버튼
            entry_frame = ttk.Frame(frame)
            entry_frame.pack(fill="x", padx=5, pady=(0, 5))  # 상단 여백 제거
            
            entry = ttk.Entry(entry_frame)
            entry.pack(side="left", fill="x", expand=True)
            self.entries.append(entry)
            
            # 입력 필드 포커스 이벤트 바인딩
            entry.bind('<FocusIn>', lambda e, idx=i: self.handle_entry_focus(idx))
            entry.bind('<Button-1>', lambda e, idx=i: self.focus_entry(e, idx))
            entry.bind('<Return>', lambda e, idx=i: self.add_item(idx))
            
            add_button = ttk.Button(entry_frame, text="추가", 
                                  command=lambda idx=i: self.add_item(idx))
            add_button.pack(side="right", padx=5)
        
        # 그리드 가중치 설정
        for i in range(2):
            root.grid_rowconfigure(i, weight=1)
            root.grid_columnconfigure(i, weight=1)
        
        # 설정 버튼 프레임
        settings_frame = ttk.Frame(root)
        settings_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="e")  # pady 줄임
        
        # 모든 버튼을 오른쪽에 배치
        right_buttons = ttk.Frame(settings_frame)
        right_buttons.pack(side="right", padx=5)  # padx 줄임
        
        # 스타일 설정
        style = ttk.Style()
        style.configure('Icon.TButton', padding=3)  # 패딩 줄임
        
        # 불투명도 조절
        opacity_frame = ttk.Frame(right_buttons)
        opacity_frame.pack(side="left", padx=2)  # 간격 줄임
        
        opacity_icon = "🔍"  # 돋보기 아이콘
        ttk.Label(opacity_frame, text=opacity_icon, font=('Segoe UI Emoji', 9)).pack(side="left")
        self.opacity_scale = ttk.Scale(opacity_frame, from_=0.1, to=1.0, 
                                     value=self.opacity, orient="horizontal",
                                     length=60,  # 슬라이더 길이 줄임
                                     command=self.update_opacity)
        self.opacity_scale.pack(side="left", padx=2)
        
        # 고정 버튼 (핀 아이콘)
        pin_icon = "📌"  # 핀 아이콘
        self.pin_button = ttk.Button(right_buttons, text=pin_icon, width=3,
                                   style='Icon.TButton',
                                   command=self.toggle_pin)
        self.pin_button.pack(side="left", padx=2)
        
        # 설정 버튼 (기어 아이콘)
        settings_icon = "⚙️"  # 기어 아이콘
        settings_button = ttk.Button(right_buttons, text=settings_icon, width=3,
                                   style='Icon.TButton',
                                   command=self.show_settings)
        settings_button.pack(side="left", padx=2)
        
        # 초기 데이터 로드
        self.load_data()
        
        # 초기 불투명도 설정
        self.root.attributes('-alpha', self.opacity)
        
        # 초기 고정 상태 설정
        self.root.attributes('-topmost', self.is_pinned)
        
        # 자동 저장 설정
        self.auto_save_enabled = True
        self.auto_save_interval = 300000  # 5분
        self.schedule_auto_save()
        
        # 프로그램 시작 시 첫 번째 입력 필드에 포커스 설정
        self.root.after(100, self.initial_focus)
    
    def schedule_auto_save(self):
        if self.auto_save_enabled:
            self.save_data(show_message=False)
            self.root.after(self.auto_save_interval, self.schedule_auto_save)
    
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("설정")
        settings_window.geometry("400x500")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 노트북(탭) 생성
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 데이터 관리 탭
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="데이터 관리")
        
        # 자동 저장 설정
        auto_save_frame = ttk.LabelFrame(data_frame, text="자동 저장")
        auto_save_frame.pack(fill="x", padx=5, pady=5)
        
        auto_save_var = tk.BooleanVar(value=self.auto_save_enabled)
        auto_save_check = ttk.Checkbutton(auto_save_frame, text="자동 저장 사용", 
                                        variable=auto_save_var,
                                        command=lambda: self.toggle_auto_save(auto_save_var.get()))
        auto_save_check.pack(side="left", padx=5, pady=5)
        
        # 수동 저장/불러오기 버튼
        manual_save_frame = ttk.LabelFrame(data_frame, text="데이터 관리")
        manual_save_frame.pack(fill="x", padx=5, pady=5)
        
        button_frame = ttk.Frame(manual_save_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="저장", 
                  command=lambda: self.save_data(show_message=True)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="불러오기", 
                  command=self.load_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="프린트", 
                  command=self.print_checklist).pack(side="left", padx=5)
        
        # 정보 탭
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="정보")
        
        info_text = """아이젠하워 매트릭스 프로그램

버전: 1.0
개발자: MinJun Kim
이메일: kdyw123@gmail.com

이 프로그램은 아이젠하워 매트릭스를 기반으로 
한 할 일 관리 도구입니다.

문의사항이 있으시면 이메일로 연락주세요."""
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack(padx=10, pady=10)
    
    def toggle_auto_save(self, enabled):
        self.auto_save_enabled = enabled
        if enabled:
            self.schedule_auto_save()
    
    def handle_click(self, event, quadrant_idx):
        """마우스 클릭 이벤트를 처리하여 선택된 항목 관리"""
        listbox = self.lists[quadrant_idx]
        self.current_quadrant = quadrant_idx
        
        # 클릭된 위치의 항목 선택
        clicked_index = listbox.nearest(event.y)
        if clicked_index >= 0:
            listbox.select_clear(0, tk.END)
            listbox.select_set(clicked_index)
            listbox.activate(clicked_index)
            
            # 클릭된 x 좌표가 체크박스 영역인지 확인 (왼쪽 여백 10px + 체크박스 너비 20px)
            if event.x <= 30:  
                self.toggle_item(quadrant_idx)
    
    def show_context_menu(self, event, quadrant_idx):
        """우클릭 메뉴를 표시"""
        self.current_quadrant = quadrant_idx
        listbox = self.lists[quadrant_idx]
        
        # 클릭된 위치의 항목 선택
        clicked_index = listbox.nearest(event.y)
        if clicked_index >= 0:
            listbox.select_clear(0, tk.END)
            listbox.select_set(clicked_index)
            listbox.activate(clicked_index)
            # 메뉴 표시
            self.context_menu.post(event.x_root, event.y_root)
    
    def delete_selected_item(self):
        """선택된 항목 삭제"""
        if hasattr(self, 'current_quadrant'):
            listbox = self.lists[self.current_quadrant]
            selection = listbox.curselection()
            if selection:
                item = listbox.get(selection[0])
                # 메모도 함께 삭제
                if item in self.memos[self.current_quadrant]:
                    del self.memos[self.current_quadrant][item]
                listbox.delete(selection[0])
                listbox.selection_clear(0, tk.END)
    
    def update_opacity(self, value):
        self.opacity = float(value)
        self.root.attributes('-alpha', self.opacity)
    
    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.root.attributes('-topmost', self.is_pinned)
        # 핀 아이콘 상태 변경
        self.pin_button.configure(text="📍" if self.is_pinned else "📌")
    
    def handle_window_map(self, event):
        """윈도우가 처음 표시될 때 호출되는 이벤트 핸들러"""
        self.initial_focus()
    
    def initial_focus(self):
        """프로그램 시작 시 초기 포커스 설정"""
        # 윈도우에 포커스 강제 설정
        self.root.focus_force()
        # 첫 번째 입력 필드에 포커스 설정
        self.entries[0].focus_force()
        # 입력 필드 선택 상태로 만들기
        self.entries[0].select_range(0, 'end')
        self.active_entry = 0
    
    def handle_window_focus(self, event):
        """윈도우가 포커스를 얻었을 때 마지막 활성화된 입력 필드로 포커스 복원"""
        self.restore_last_focus()
    
    def handle_entry_focus(self, idx):
        """입력 필드가 포커스를 얻었을 때 현재 활성화된 입력 필드 인덱스 저장"""
        self.active_entry = idx
    
    def restore_last_focus(self):
        """마지막으로 활성화된 입력 필드로 포커스 복원"""
        self.entries[self.active_entry].focus_force()
    
    def focus_entry(self, event, quadrant_idx):
        """입력 필드에 포커스 설정"""
        self.active_entry = quadrant_idx
        self.entries[quadrant_idx].focus_force()
        return "break"
    
    def add_item(self, quadrant_idx, event=None):
        """항목 추가"""
        text = self.entries[quadrant_idx].get().strip()
        if text:
            self.lists[quadrant_idx].insert(tk.END, f"□ {text}")
            self.entries[quadrant_idx].delete(0, tk.END)
            # 포커스 유지 및 현재 활성 입력 필드 업데이트
            self.active_entry = quadrant_idx
            self.entries[quadrant_idx].focus_force()
        return "break"
    
    def show_memo(self):
        """상세보기 창 표시"""
        if hasattr(self, 'current_quadrant'):
            selection = self.lists[self.current_quadrant].curselection()
            if selection:
                item = self.lists[self.current_quadrant].get(selection[0])
                
                # 메모 창 생성
                memo_window = tk.Toplevel(self.root)
                memo_window.title("상세보기")
                memo_window.geometry("500x400")
                memo_window.transient(self.root)
                
                # 항목 표시
                item_frame = ttk.LabelFrame(memo_window, text="항목")
                item_frame.pack(fill="x", padx=10, pady=5)
                ttk.Label(item_frame, text=item[2:]).pack(padx=10, pady=5)
                
                # 메모 입력/표시 영역
                memo_frame = ttk.LabelFrame(memo_window, text="메모")
                memo_frame.pack(fill="both", expand=True, padx=10, pady=5)
                
                memo_text = tk.Text(memo_frame, wrap="word", height=10)
                memo_text.pack(fill="both", expand=True, padx=5, pady=5)
                
                # 기존 메모 있으면 표시
                if item in self.memos[self.current_quadrant]:
                    memo_text.insert("1.0", self.memos[self.current_quadrant][item])
                
                def save_memo():
                    memo_content = memo_text.get("1.0", "end-1c").strip()
                    if memo_content:  # 메모 내용이 있는 경우
                        self.memos[self.current_quadrant][item] = memo_content
                        # 메모 있음을 표시
                        self.update_item_display(self.current_quadrant, selection[0], item)
                    else:  # 메모 내용이 없는 경우
                        if item in self.memos[self.current_quadrant]:
                            del self.memos[self.current_quadrant][item]
                            # 메모 표시 제거
                            self.update_item_display(self.current_quadrant, selection[0], item)
                    memo_window.destroy()
                
                button_frame = ttk.Frame(memo_window)
                button_frame.pack(fill="x", padx=10, pady=5)
                
                ttk.Button(button_frame, text="저장", command=save_memo).pack(side="right", padx=5)
    
    def update_item_display(self, quadrant_idx, index, item):
        """항목 표시 업데이트 (메모 있음 표시)"""
        # 기존 메모 데이터 보존을 위해 원본 아이템 키 저장
        original_item = item
        
        # 별표 제거한 상태의 아이템으로 메모 확인
        clean_item = item.replace(" *", "")
        has_memo = clean_item in self.memos[quadrant_idx] and self.memos[quadrant_idx][clean_item].strip()
        
        prefix = item[:2]  # 체크박스 상태 (□ 또는 ✓) 유지
        text = item[2:].replace(" *", "").strip()  # 실제 텍스트 내용 (별표 제거)
        
        # 메모가 있으면 * 표시 추가
        new_item = f"{prefix}{' *' if has_memo else ' '}{text}"
        
        # 메모 데이터 키 업데이트
        if has_memo and original_item in self.memos[quadrant_idx]:
            memo_content = self.memos[quadrant_idx].pop(original_item)
            self.memos[quadrant_idx][new_item] = memo_content
        
        self.lists[quadrant_idx].delete(index)
        self.lists[quadrant_idx].insert(index, new_item)
        self.lists[quadrant_idx].select_set(index)
    
    def toggle_item(self, quadrant_idx, event=None):
        """항목 체크/체크해제 토글"""
        listbox = self.lists[quadrant_idx]
        selection = listbox.curselection()
        if selection:
            idx = selection[0]
            item = listbox.get(idx)
            
            # 메모 표시 제거하고 기본 텍스트 추출
            text = item[2:].replace(" *", " ").strip()
            
            # 체크 상태 토글
            if item.startswith("□"):
                new_item = f"✓ {text}"
            elif item.startswith("✓"):
                new_item = f"□ {text}"
            else:
                return
            
            # 메모 상태 유지
            if item in self.memos[quadrant_idx]:
                memo = self.memos[quadrant_idx].pop(item)
                self.memos[quadrant_idx][new_item] = memo
            
            # 항목 업데이트 (메모 표시 포함)
            listbox.delete(idx)
            listbox.insert(idx, new_item)
            self.update_item_display(quadrant_idx, idx, new_item)
            
            # 자동 저장 트리거
            if self.auto_save_enabled:
                self.save_data(show_message=False)
    
    def edit_item(self):
        if hasattr(self, 'current_quadrant'):
            selection = self.lists[self.current_quadrant].curselection()
            if selection:
                item = self.lists[self.current_quadrant].get(selection[0])
                
                # 수정 창 생성
                edit_window = tk.Toplevel(self.root)
                edit_window.title("항목 수정")
                edit_window.geometry("400x150")
                edit_window.transient(self.root)
                edit_window.grab_set()
                
                # 현재 텍스트 가져오기 (체크박스 제외)
                current_text = item[2:] if item.startswith("□ ") or item.startswith("✓ ") else item
                is_checked = item.startswith("✓ ")
                
                ttk.Label(edit_window, text="내용:").pack(padx=10, pady=5)
                edit_entry = ttk.Entry(edit_window, width=50)
                edit_entry.insert(0, current_text)
                edit_entry.pack(padx=10, pady=5)
                
                def save_edit():
                    new_text = edit_entry.get()
                    if new_text:
                        # 체크 상태 유지하면서 텍스트만 수정
                        prefix = "✓ " if is_checked else "□ "
                        self.lists[self.current_quadrant].delete(selection[0])
                        self.lists[self.current_quadrant].insert(selection[0], prefix + new_text)
                        
                        # 메모가 있다면 메모의 키도 업데이트
                        if item in self.memos[self.current_quadrant]:
                            memo = self.memos[self.current_quadrant].pop(item)
                            self.memos[self.current_quadrant][prefix + new_text] = memo
                        
                        edit_window.destroy()
                
                ttk.Button(edit_window, text="저장", command=save_edit).pack(pady=10)
    
    def save_data(self, show_message=True):
        try:
            data = {
                'items': [],
                'memos': [],
                'last_saved': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for i in range(4):
                items = list(self.lists[i].get(0, tk.END))
                # 저장 시 별표 제거
                clean_items = [item.replace(" *", " ").strip() for item in items]
                data['items'].append(clean_items)
                
                # 메모 데이터도 별표 없는 상태로 저장
                clean_memos = {}
                for key, value in self.memos[i].items():
                    clean_key = key.replace(" *", " ").strip()
                    clean_memos[clean_key] = value
                data['memos'].append(clean_memos)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            if show_message:
                messagebox.showinfo("저장 완료", 
                                  f"데이터가 성공적으로 저장되었습니다.\n저장 시간: {data['last_saved']}")
        except Exception as e:
            if show_message:
                messagebox.showerror("저장 실패", f"데이터 저장 중 오류가 발생했습니다:\n{str(e)}")
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for i in range(4):
                    self.lists[i].delete(0, tk.END)
                    # 메모 데이터 먼저 로드
                    if 'memos' in data:
                        self.memos[i] = data['memos'][i]
                    
                    # 항목 로드 및 메모 표시 업데이트
                    for item in data['items'][i]:
                        clean_item = item.replace(" *", "")  # 별표 제거
                        self.lists[i].insert(tk.END, clean_item)
                        
                        # 메모가 있는 경우 별표 표시 업데이트
                        if clean_item in self.memos[i] and self.memos[i][clean_item].strip():
                            last_idx = self.lists[i].size() - 1
                            self.update_item_display(i, last_idx, clean_item)
                
                if 'last_saved' in data:
                    messagebox.showinfo("불러오기 완료", 
                                      f"마지막 저장 시간: {data['last_saved']}\n데이터가 성공적으로 불러와졌습니다.")
            except Exception as e:
                messagebox.showerror("불러오기 실패", f"데이터 불러오기 중 오류가 발생했습니다:\n{str(e)}")
        else:
            messagebox.showinfo("새 파일", "저장된 데이터가 없습니다. 새로운 체크리스트를 시작합니다.")
    
    def print_checklist(self):
        """체크리스트 프린트"""
        try:
            # HTML 형식으로 프린트 내용 생성
            html_content = """
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    @page { 
                        size: A4; 
                        margin: 1cm;
                    }
                    body { 
                        font-family: 맑은 고딕;
                        margin: 0;
                        padding: 20px;
                    }
                    .container { 
                        display: flex; 
                        flex-wrap: wrap;
                        gap: 20px;
                    }
                    .quadrant { 
                        width: calc(50% - 10px); 
                        box-sizing: border-box;
                        border: 1px solid #000;
                        margin-bottom: 20px;
                        page-break-inside: avoid;
                    }
                    .title { 
                        font-size: 16px;
                        font-weight: bold;
                        margin: 0;
                        padding: 10px;
                        background-color: #f0f0f0;
                        border-bottom: 2px solid #000;
                    }
                    .items {
                        padding: 10px;
                    }
                    .item {
                        display: flex;
                        align-items: center;
                        margin: 8px 0;
                        padding: 5px 0;
                        border-bottom: 1px solid #eee;
                        min-height: 24px;
                    }
                    .checkbox {
                        width: 12px;
                        height: 12px;
                        border: 1px solid #000;
                        margin-right: 8px;
                        display: inline-block;
                        position: relative;
                    }
                    .checkbox.checked::after {
                        content: '✓';
                        position: absolute;
                        top: -4px;
                        left: 1px;
                        font-size: 14px;
                        color: #000;
                    }
                </style>
            </head>
            <body>
                <div class="container">
            """
            
            categories = ["중요 & 긴급", "중요", 
                        "긴급", "중요 X 긴급 X"]
            
            for i in range(4):
                html_content += f"""
                    <div class="quadrant">
                        <div class="title">{categories[i]}</div>
                        <div class="items">
                """
                
                items = list(self.lists[i].get(0, tk.END))
                # 최소 20개의 줄을 생성하되, 항목이 20개 이상이면 모든 항목 표시
                max_lines = max(20, len(items))
                
                for j in range(max_lines):
                    if j < len(items):
                        item = items[j]
                        is_checked = "✓" in item[:2]  # 체크 여부 확인
                        item_text = item[2:].replace(" *", "")  # 체크박스와 메모 표시 제거
                        checkbox_class = 'checkbox checked' if is_checked else 'checkbox'
                        html_content += f'<div class="item"><span class="{checkbox_class}"></span>{item_text}</div>\n'
                    else:
                        html_content += '<div class="item"><span class="checkbox"></span></div>\n'
                
                html_content += """
                        </div>
                    </div>"""
            
            html_content += """
                </div>
            </body>
            </html>
            """
            
            # 임시 HTML 파일로 저장
            temp_file = "checklist_print.html"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # 기본 브라우저로 HTML 파일 열기
            import webbrowser
            webbrowser.open(temp_file)
            
            # 안내 메시지 표시
            messagebox.showinfo("인쇄 안내", 
                "브라우저에서 체크리스트가 열렸습니다.\n브라우저의 인쇄 기능(Ctrl+P)을 사용하여 인쇄하실 수 있습니다.")
            
        except Exception as e:
            messagebox.showerror("프린트 오류", f"프린트 중 오류가 발생했습니다:\n{str(e)}")
            try:
                os.remove(temp_file)
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrantChecklist(root)
    root.mainloop() 