import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class QuadrantChecklist:
    def __init__(self, root):
        self.root = root
        self.root.title("4분할 체크리스트")
        self.root.geometry("800x600")
        
        # 데이터 저장 파일 경로
        self.data_file = "checklist_data.json"
        
        # 불투명도와 고정 상태 변수
        self.opacity = 0.8
        self.is_pinned = False
        
        # 4개의 프레임 생성
        self.frames = []
        self.lists = []
        self.entries = []
        self.memos = [{}, {}, {}, {}]  # 각 항목의 메모를 저장할 딕셔너리
        
        # 카테고리 이름
        categories = ["긴급하고 중요한 일", "긴급하지 않지만 중요한 일", 
                     "긴급하지만 중요하지 않은 일", "긴급하지도 중요하지도 않은 일"]
        
        # 우클릭 메뉴 생성
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="수정", command=self.edit_item)
        self.context_menu.add_command(label="상세보기", command=self.show_memo)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="삭제", command=self.delete_selected_item)
        
        # 각 카테고리별 프레임 생성
        for i in range(4):
            frame = ttk.LabelFrame(root, text=categories[i])
            frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            self.frames.append(frame)
            
            # 체크리스트 리스트박스
            listbox_frame = ttk.Frame(frame)
            listbox_frame.pack(padx=5, pady=5, fill="both", expand=True)
            
            listbox = tk.Listbox(listbox_frame, height=10, width=30)
            scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
            listbox.configure(yscrollcommand=scrollbar.set)
            
            listbox.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.lists.append(listbox)
            
            # 우클릭 이벤트 바인딩
            listbox.bind("<Button-3>", lambda e, idx=i: self.show_context_menu(e, idx))
            
            # 입력 필드와 버튼
            entry_frame = ttk.Frame(frame)
            entry_frame.pack(fill="x", padx=5, pady=5)
            
            entry = ttk.Entry(entry_frame)
            entry.pack(side="left", fill="x", expand=True)
            self.entries.append(entry)
            
            # 엔터 키 바인딩 추가
            entry.bind('<Return>', lambda e, idx=i: self.add_item(idx))
            
            add_button = ttk.Button(entry_frame, text="추가", 
                                  command=lambda idx=i: self.add_item(idx))
            add_button.pack(side="right", padx=5)
            
            # 체크박스 스타일 설정
            listbox.bind('<<ListboxSelect>>', lambda e, idx=i: self.toggle_item(idx))
        
        # 그리드 가중치 설정
        for i in range(2):
            root.grid_rowconfigure(i, weight=1)
            root.grid_columnconfigure(i, weight=1)
        
        # 설정 버튼 프레임
        settings_frame = ttk.Frame(root)
        settings_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # 불투명도 조절
        opacity_frame = ttk.Frame(settings_frame)
        opacity_frame.pack(side="left", padx=5)
        
        ttk.Label(opacity_frame, text="불투명도:").pack(side="left")
        self.opacity_scale = ttk.Scale(opacity_frame, from_=0.1, to=1.0, 
                                     value=self.opacity, orient="horizontal",
                                     command=self.update_opacity)
        self.opacity_scale.pack(side="left", padx=5)
        
        # 고정 버튼
        self.pin_button = ttk.Button(settings_frame, text="고정 해제", 
                                   command=self.toggle_pin)
        self.pin_button.pack(side="left", padx=5)
        
        # 설정 버튼
        settings_button = ttk.Button(settings_frame, text="설정", command=self.show_settings)
        settings_button.pack(side="left", padx=5)
        
        # 초기 데이터 로드
        self.load_data()
        
        # 초기 불투명도 설정
        self.root.attributes('-alpha', self.opacity)
        
        # 자동 저장 설정
        self.auto_save_enabled = True
        self.auto_save_interval = 300000  # 5분
        self.schedule_auto_save()
    
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
        manual_save_frame = ttk.LabelFrame(data_frame, text="수동 데이터 관리")
        manual_save_frame.pack(fill="x", padx=5, pady=5)
        
        button_frame = ttk.Frame(manual_save_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="저장", 
                  command=lambda: self.save_data(show_message=True)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="불러오기", 
                  command=self.load_data).pack(side="left", padx=5)
        
        # 정보 탭
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="정보")
        
        info_text = """4분할 체크리스트 프로그램

버전: 1.0
개발자: Your Name
이메일: your.email@example.com

이 프로그램은 아이젠하워 매트릭스를 기반으로 한
할 일 관리 도구입니다.

문의사항이 있으시면 이메일로 연락주세요."""
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack(padx=20, pady=20)
    
    def toggle_auto_save(self, enabled):
        self.auto_save_enabled = enabled
        if enabled:
            self.schedule_auto_save()
    
    def show_context_menu(self, event, quadrant_idx):
        self.current_quadrant = quadrant_idx
        selection = self.lists[quadrant_idx].curselection()
        if selection:
            self.context_menu.post(event.x_root, event.y_root)
    
    def delete_selected_item(self):
        if hasattr(self, 'current_quadrant'):
            selection = self.lists[self.current_quadrant].curselection()
            if selection:
                item = self.lists[self.current_quadrant].get(selection[0])
                # 메모도 함께 삭제
                if item in self.memos[self.current_quadrant]:
                    del self.memos[self.current_quadrant][item]
                self.lists[self.current_quadrant].delete(selection[0])
                self.lists[self.current_quadrant].selection_clear(0, tk.END)
    
    def update_opacity(self, value):
        self.opacity = float(value)
        self.root.attributes('-alpha', self.opacity)
    
    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.root.attributes('-topmost', self.is_pinned)
        self.pin_button.config(text="고정 해제" if self.is_pinned else "고정")
    
    def add_item(self, quadrant_idx, event=None):
        text = self.entries[quadrant_idx].get()
        if text:
            self.lists[quadrant_idx].insert(tk.END, f"□ {text}")
            self.entries[quadrant_idx].delete(0, tk.END)
            # 포커스 유지
            self.entries[quadrant_idx].focus_set()
    
    def toggle_item(self, quadrant_idx):
        selection = self.lists[quadrant_idx].curselection()
        if selection:
            item = self.lists[quadrant_idx].get(selection[0])
            if item.startswith("✓ "):
                new_item = f"□ {item[2:]}"
            elif item.startswith("□ "):
                new_item = f"✓ {item[2:]}"
            else:
                return
            
            # 메모 상태 유지
            if item in self.memos[quadrant_idx]:
                memo = self.memos[quadrant_idx].pop(item)
                self.memos[quadrant_idx][new_item] = memo
            
            self.lists[quadrant_idx].delete(selection[0])
            self.lists[quadrant_idx].insert(selection[0], new_item)
    
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
    
    def show_memo(self):
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
                    memo_content = memo_text.get("1.0", "end-1c")
                    self.memos[self.current_quadrant][item] = memo_content
                    memo_window.destroy()
                
                button_frame = ttk.Frame(memo_window)
                button_frame.pack(fill="x", padx=10, pady=5)
                
                ttk.Button(button_frame, text="저장", command=save_memo).pack(side="right", padx=5)
    
    def save_data(self, show_message=True):
        try:
            data = {
                'items': [],
                'memos': [],
                'last_saved': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for i in range(4):
                items = list(self.lists[i].get(0, tk.END))
                data['items'].append(items)
                data['memos'].append(self.memos[i])
            
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
                    for item in data['items'][i]:
                        self.lists[i].insert(tk.END, item)
                    
                    # 메모 데이터 로드
                    if 'memos' in data:
                        self.memos[i] = data['memos'][i]
                
                if 'last_saved' in data:
                    messagebox.showinfo("불러오기 완료", 
                                      f"마지막 저장 시간: {data['last_saved']}\n데이터가 성공적으로 불러와졌습니다.")
            except Exception as e:
                messagebox.showerror("불러오기 실패", f"데이터 불러오기 중 오류가 발생했습니다:\n{str(e)}")
        else:
            messagebox.showinfo("새 파일", "저장된 데이터가 없습니다. 새로운 체크리스트를 시작합니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrantChecklist(root)
    root.mainloop() 