import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import requests
import subprocess
import sys
import webbrowser

# 버전 정보 상수
VERSION = "1.0.1"
GITHUB_REPO = "octxxiii/Anti-ADHD"

# 테마 색상
LIGHT_THEME = {
    'bg': '#ffffff',
    'fg': '#000000',
    'select_bg': '#0078d7',
    'select_fg': '#ffffff',
    'listbox_bg': '#ffffff',
    'listbox_fg': '#000000',
    'frame_bg': '#f0f0f0'
}

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class QuadrantChecklist:
    def __init__(self, root):
        self.root = root
        self.root.title("Anti-ADHD")
        self.root.geometry("800x510")  # 전체 높이를 510으로 조정
        
        # 아이콘 설정
        icon_path = resource_path('icon.ico')
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except tk.TclError:
                print(f"아이콘 로드 실패: {icon_path}")
        
        # 버전 정보
        self.current_version = VERSION
        self.github_repo = GITHUB_REPO
        
        # 자동 업데이트 설정
        self.auto_update_enabled = True
        
        # 테마 설정
        self.current_theme = LIGHT_THEME
        
        # 시작 시 업데이트 확인
        self.check_for_updates()
        
        # 스타일 설정
        self.style = ttk.Style()
        
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
            frame.grid(row=i//2, column=i%2, padx=10, pady=(5, 5), sticky="nsew")  # row 위치를 0부터 시작하도록 변경
            self.frames.append(frame)
            
            # 체크리스트 리스트박스
            listbox_frame = ttk.Frame(frame)
            listbox_frame.pack(padx=0, pady=10, fill="both", expand=True)  # 모든 여백 제거
            
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
        settings_frame.grid(row=0, column=1, sticky="ne", pady=0, padx=(0, 5))  # 상단 여백을 0으로 설정
        
        # 모든 버튼을 오른쪽에 배치
        right_buttons = ttk.Frame(settings_frame)
        right_buttons.pack(side="right", padx=2, pady=0)  # 상하 여백 제거
        
        # 스타일 설정
        self.style.configure('Icon.TButton', padding=1)  # padding 값 감소
        
        # 불투명도 조절
        opacity_frame = ttk.Frame(right_buttons)
        opacity_frame.pack(side="left", padx=1)  # padx 값 감소
        
        # opacity_icon = "🔍"
        ttk.Label(opacity_frame, text="", font=('Segoe UI Emoji', 9)).pack(side="left")
        self.opacity_scale = ttk.Scale(opacity_frame, from_=0.1, to=1.0, 
                                     value=self.opacity, orient="horizontal",
                                     length=60,
                                     command=self.update_opacity)
        self.opacity_scale.pack(side="left", padx=1)  # padx 값 감소
        
        # 고정 버튼 (핀 아이콘)
        pin_icon = "📍"
        self.pin_button = ttk.Button(right_buttons, text=pin_icon, width=3,
                                   style='Icon.TButton',
                                   command=self.toggle_pin)
        self.pin_button.pack(side="left", padx=1)  # padx 값 감소
        
        # 설정 버튼 (기어 아이콘)
        settings_icon = "⚙️"
        settings_button = ttk.Button(right_buttons, text=settings_icon, width=3,
                                   style='Icon.TButton',
                                   command=self.show_settings)
        settings_button.pack(side="left", padx=1)  # padx 값 감소
        
        # 초기 데이터 로드
        self.load_data(show_message=False)  # 프로그램 시작 시에는 알림창 표시하지 않음
        
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
        
        # 설정 불러오기
        self.load_settings()
        
        # 테마 적용
        self.apply_theme()
    
    def check_for_updates(self):
        # 자동 업데이트가 비활성화되어 있으면 확인하지 않음
        if not self.auto_update_enabled:
            return
        
        try:
            # 상태 레이블 업데이트
            if hasattr(self, 'update_status_label'):
                self.update_status_label.config(text="업데이트 확인 중...")
                self.update_status_label.update()
            
            # GitHub API를 통해 최신 릴리즈 정보 가져오기
            response = requests.get(f"https://api.github.com/repos/{self.github_repo}/releases/latest")
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release["tag_name"].lstrip('v')
                
                # 현재 버전과 최신 버전 비교
                if self.compare_versions(latest_version, self.current_version) > 0:
                    # 상태 레이블 업데이트
                    if hasattr(self, 'update_status_label'):
                        self.update_status_label.config(text=f"새 버전 {latest_version} 사용 가능")
                        self.update_status_label.update()
                    
                    # 업데이트 확인 다이얼로그
                    update_message = f"새로운 버전 {latest_version}이(가) 있습니다.\n현재 버전: {self.current_version}\n\n릴리즈 노트:\n{latest_release.get('body', '')}\n\n업데이트하시겠습니까?"
                    if messagebox.askyesno("업데이트 확인", update_message):
                        webbrowser.open(latest_release["html_url"])
                else:
                    # 상태 레이블 업데이트
                    if hasattr(self, 'update_status_label'):
                        self.update_status_label.config(text="최신 버전입니다")
                        self.update_status_label.update()
        except Exception as e:
            print(f"업데이트 확인 중 오류 발생: {e}")
            # 상태 레이블 업데이트
            if hasattr(self, 'update_status_label'):
                self.update_status_label.config(text="업데이트 확인 실패")
                self.update_status_label.update()

    def compare_versions(self, v1, v2):
        """버전 문자열 비교"""
        v1_parts = list(map(int, v1.split('.')))
        v2_parts = list(map(int, v2.split('.')))
        
        for v1_part, v2_part in zip(v1_parts, v2_parts):
            if v1_part > v2_part:
                return 1
            elif v1_part < v2_part:
                return -1
        return 0

    def download_and_install_update(self, download_url):
        """업데이트 다운로드 및 설치"""
        try:
            # 임시 파일로 다운로드
            response = requests.get(download_url, stream=True)
            temp_path = os.path.join(os.environ['TEMP'], 'anti_adhd_update.exe')
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 설치 스크립트 생성
            install_script = f"""@echo off
timeout /t 2 /nobreak
start "" "{temp_path}"
del "%~f0"
"""
            script_path = os.path.join(os.environ['TEMP'], 'install_update.bat')
            with open(script_path, 'w') as f:
                f.write(install_script)
            
            # 현재 프로그램 종료 및 설치 스크립트 실행
            subprocess.Popen([script_path], shell=True)
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("업데이트 오류", f"업데이트 설치 중 오류가 발생했습니다: {e}")
    
    def schedule_auto_save(self):
        if self.auto_save_enabled:
            self.save_data(show_message=False)
            self.root.after(self.auto_save_interval, self.schedule_auto_save)
    
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("설정")
        settings_window.geometry("400x500")
        settings_window.resizable(False, False)
        
        # 설정 창 아이콘 설정
        icon_path = resource_path('icon.ico')
        if os.path.exists(icon_path):
            try:
                settings_window.iconbitmap(icon_path)
            except tk.TclError:
                print(f"설정 창 아이콘 로드 실패: {icon_path}")
        
        # 설정 창이 부모 창의 중앙에 표시되도록 위치 조정
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 항상 최상위에 표시되도록 설정
        settings_window.attributes('-topmost', True)
        settings_window.lift()
        
        # 노트북 생성
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 일반 설정 탭
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="일반")
        
        # 자동 저장 설정
        save_frame = ttk.LabelFrame(general_frame, text="자동 저장", padding=(10, 5))
        save_frame.pack(fill="x", padx=5, pady=5)
        
        auto_save_var = tk.BooleanVar(value=self.auto_save_enabled)
        ttk.Checkbutton(save_frame, text="자동 저장 사용", 
                        variable=auto_save_var,
                        command=lambda: self.toggle_auto_save(auto_save_var.get())).pack(anchor="w")
        
        # 자동 업데이트 설정
        update_frame = ttk.LabelFrame(general_frame, text="자동 업데이트", padding=(10, 5))
        update_frame.pack(fill="x", padx=5, pady=5)
        
        auto_update_var = tk.BooleanVar(value=self.auto_update_enabled)
        ttk.Checkbutton(update_frame, text="자동 업데이트 확인", 
                        variable=auto_update_var,
                        command=lambda: self.toggle_auto_update(auto_update_var.get())).pack(anchor="w")
        
        # 수동 업데이트 확인 버튼
        update_button_frame = ttk.Frame(update_frame)
        update_button_frame.pack(fill="x", pady=(5, 0))
        
        self.update_status_label = ttk.Label(update_button_frame, text="")
        self.update_status_label.pack(side="left", padx=(0, 10))
        
        ttk.Button(update_button_frame, text="지금 확인", 
                  command=self.check_for_updates).pack(side="right")
        
        # 수동 저장/불러오기 버튼
        manual_save_frame = ttk.LabelFrame(general_frame, text="데이터 관리")
        manual_save_frame.pack(fill="x", padx=3, pady=3)  # 여백 축소
        
        button_frame = ttk.Frame(manual_save_frame)
        button_frame.pack(fill="x", padx=3, pady=3)  # 여백 축소
        
        ttk.Button(button_frame, text="저장", 
                  command=lambda: self.save_data(show_message=True)).pack(side="left", padx=3)  # 여백 축소
        ttk.Button(button_frame, text="불러오기", 
                  command=lambda: self.load_data(show_message=True)).pack(side="left", padx=3)  # 여백 축소
        ttk.Button(button_frame, text="프린트", 
                  command=self.print_checklist).pack(side="left", padx=3)  # 여백 축소
        
        # 정보 탭
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="정보")
        
        # 정보 탭 스타일 설정
        style = ttk.Style()
        style.configure("Info.TLabel", font=("맑은 고딕", 10))
        style.configure("Info.TButton", font=("맑은 고딕", 9))
        
        # 프로그램 정보 프레임
        program_info_frame = ttk.LabelFrame(info_frame, text="프로그램 정보", padding=10)
        program_info_frame.pack(fill="x", padx=10, pady=5)
        
        # 프로그램 이름
        program_name = ttk.Label(program_info_frame, text="Anti-ADHD", font=("맑은 고딕", 14, "bold"))
        program_name.pack(pady=(0, 5))
        
        # 버전 정보
        version_label = ttk.Label(program_info_frame, text=f"버전: {self.current_version}", style="Info.TLabel")
        version_label.pack(pady=2)
        
        # 개발자 정보
        developer_label = ttk.Label(program_info_frame, text="개발자: octxxiii", style="Info.TLabel")
        developer_label.pack(pady=2)
        
        # GitHub 링크
        github_frame = ttk.Frame(program_info_frame)
        github_frame.pack(pady=5)
        github_label = ttk.Label(github_frame, text="GitHub: ", style="Info.TLabel")
        github_label.pack(side="left")
        github_link = ttk.Label(github_frame, text="octxxiii/Anti-ADHD", style="Info.TLabel", foreground="blue", cursor="hand2")
        github_link.pack(side="left")
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/octxxiii/Anti-ADHD"))
        
        # 라이선스 정보
        license_frame = ttk.LabelFrame(info_frame, text="라이선스", padding=10)
        license_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 스크롤바와 캔버스 생성
        license_canvas = tk.Canvas(license_frame)
        license_scrollbar = ttk.Scrollbar(license_frame, orient="vertical", command=license_canvas.yview)
        scrollable_frame = ttk.Frame(license_canvas)
        
        # 스크롤바 설정
        scrollable_frame.bind(
            "<Configure>",
            lambda e: license_canvas.configure(scrollregion=license_canvas.bbox("all"))
        )
        
        # 캔버스에 프레임 추가
        license_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        license_canvas.configure(yscrollcommand=license_scrollbar.set)
        
        # 스크롤바와 캔버스 배치
        license_scrollbar.pack(side="right", fill="y")
        license_canvas.pack(side="left", fill="both", expand=True)
        
        # 마우스 휠 이벤트 바인딩
        def _on_mousewheel(event):
            license_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        license_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 캔버스 크기가 변경될 때 내부 프레임 너비 조정
        def _on_canvas_configure(event):
            license_canvas.itemconfig("window", width=event.width)
        
        license_canvas.bind("<Configure>", _on_canvas_configure)
        
        license_text = """이 프로그램은 MIT 라이선스 하에 배포됩니다.

MIT License

Copyright (c) 2024 octxxiii

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
        
        license_label = ttk.Label(scrollable_frame, text=license_text, style="Info.TLabel", wraplength=350, justify="left")
        license_label.pack(padx=5, pady=5, fill="x")
        
        # 닫기 버튼
        close_button = ttk.Button(info_frame, text="닫기", command=settings_window.destroy, style="Info.TButton")
        close_button.pack(pady=10)
    
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
                # 삭제 후 자동 저장
                if self.auto_save_enabled:
                    self.save_data(show_message=False)
    
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
    
    def load_data(self, show_message=True):
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
                
                if 'last_saved' in data and show_message:
                    messagebox.showinfo("불러오기 완료", 
                                      f"마지막 저장 시간: {data['last_saved']}\n데이터 로딩 성공.")
            except Exception as e:
                messagebox.showerror("불러오기 실패", f"데이터 불러오기 중 오류가 발생했습니다:\n{str(e)}")
        else:
            if show_message:
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

    def apply_theme(self):
        theme = self.current_theme
        
        # TTK 스타일 설정
        self.style.configure('TFrame', background=theme['bg'])
        self.style.configure('TLabelframe', background=theme['bg'])
        self.style.configure('TLabelframe.Label', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TButton', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TEntry', fieldbackground=theme['listbox_bg'], foreground=theme['fg'])
        self.style.configure('TScale', background=theme['bg'], troughcolor=theme['frame_bg'])
        
        # 루트 윈도우 설정
        self.root.configure(bg=theme['bg'])
        
        # 리스트박스 설정
        for listbox in self.lists:
            listbox.configure(
                bg=theme['listbox_bg'],
                fg=theme['listbox_fg'],
                selectbackground=theme['select_bg'],
                selectforeground=theme['select_fg']
            )
        
        # 프레임 설정
        for frame in self.frames:
            frame.configure(style='TLabelframe')
            
        # 컨텍스트 메뉴 설정
        self.context_menu.configure(
            bg=theme['listbox_bg'],
            fg=theme['listbox_fg'],
            activebackground=theme['select_bg'],
            activeforeground=theme['select_fg']
        )

    def save_settings(self):
        settings = {
            'opacity': self.opacity,
            'is_pinned': self.is_pinned,
            'auto_save_enabled': self.auto_save_enabled,
            'auto_update_enabled': self.auto_update_enabled  # 자동 업데이트 설정 추가
        }
        
        try:
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"설정 저장 중 오류 발생: {e}")

    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                self.opacity = settings.get('opacity', 1)
                self.is_pinned = settings.get('is_pinned', True)
                self.auto_save_enabled = settings.get('auto_save_enabled', True)
                self.auto_update_enabled = settings.get('auto_update_enabled', True)  # 자동 업데이트 설정 추가
                
                # 설정 적용
                self.opacity_scale.set(self.opacity)
                self.root.attributes('-alpha', self.opacity)
                self.root.attributes('-topmost', self.is_pinned)
                
                if not self.auto_save_enabled:
                    self.root.after_cancel(self.auto_save_job)
        except Exception as e:
            print(f"설정 로드 중 오류 발생: {e}")

    def toggle_auto_update(self, enabled):
        self.auto_update_enabled = enabled
        self.save_settings()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrantChecklist(root)
    
    # 프로그램 종료 시 자동 저장
    def on_closing():
        if app.auto_save_enabled:
            app.save_data(show_message=False)
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop() 