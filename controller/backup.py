"""
controller/backup.py

백업/복원 서비스 함수 모음
"""
import os
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QListWidgetItem

def backup_data(main_window):
    """현재 프로젝트 데이터를 백업 디렉토리에 복사 저장"""
    if not main_window.current_project_name:
        QMessageBox.information(main_window, "백업", "백업할 프로젝트가 없습니다.")
        return
    backup_dir = os.path.join(main_window.data_dir, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    src_file = os.path.join(main_window.data_dir, f"{main_window.current_project_name}.json")
    if not os.path.exists(src_file):
        QMessageBox.warning(main_window, "백업", "프로젝트 데이터 파일이 존재하지 않습니다.")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{main_window.current_project_name}_{timestamp}.json")
    try:
        import shutil
        shutil.copy2(src_file, backup_file)
        QMessageBox.information(main_window, "백업", f"프로젝트가 백업되었습니다:\n{backup_file}")
    except Exception as e:
        QMessageBox.critical(main_window, "오류", f"백업 중 오류가 발생했습니다:\n{str(e)}")

def restore_from_backup(main_window):
    """백업 파일에서 현재 프로젝트 복원"""
    if not main_window.current_project_name:
        QMessageBox.information(main_window, "복원", "프로젝트를 선택해주세요.")
        return
    backup_dir = os.path.join(main_window.data_dir, "backups")
    if not os.path.exists(backup_dir):
        QMessageBox.information(main_window, "복원", "백업 파일이 없습니다.")
        return
    backup_files = []
    for file_name in os.listdir(backup_dir):
        if file_name.startswith(f"{main_window.current_project_name}_") and file_name.endswith(".json"):
            file_path = os.path.join(backup_dir, file_name)
            backup_files.append((file_path, os.path.getmtime(file_path)))
    if not backup_files:
        QMessageBox.information(main_window, "복원", "복원할 백업 파일이 없습니다.")
        return
    backup_files.sort(key=lambda x: x[1], reverse=True)
    dialog = QDialog(main_window)
    dialog.setWindowTitle("백업에서 복원")
    dialog.setMinimumSize(400, 300)
    layout = QVBoxLayout(dialog)
    backup_list = QListWidget()
    for file_path, mtime in backup_files:
        timestamp = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        item = QListWidgetItem(f"백업: {timestamp}")
        item.setData(0x0100, file_path)  # Qt.UserRole = 0x0100
        backup_list.addItem(item)
    layout.addWidget(backup_list)
    button_layout = QHBoxLayout()
    restore_btn = QPushButton("복원")
    restore_btn.clicked.connect(lambda: _restore_selected_backup(main_window, backup_list.currentItem(), dialog))
    button_layout.addWidget(restore_btn)
    close_btn = QPushButton("닫기")
    close_btn.clicked.connect(dialog.close)
    button_layout.addWidget(close_btn)
    layout.addLayout(button_layout)
    dialog.exec_()

def _restore_selected_backup(main_window, item, dialog):
    if not item:
        return
    file_path = item.data(0x0100)  # Qt.UserRole = 0x0100
    reply = QMessageBox.question(
        main_window, "백업 복원",
        "선택한 백업에서 복원하시겠습니까?\n현재 데이터는 백업됩니다.",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        try:
            import shutil
            dst_file = os.path.join(main_window.data_dir, f"{main_window.current_project_name}.json")
            shutil.copy2(file_path, dst_file)
            main_window.load_project_from_file(main_window.current_project_name)
            main_window.update_quadrant_display(main_window.current_project_name)
            QMessageBox.information(main_window, "복원", "백업에서 복원되었습니다.")
            dialog.close()
        except Exception as e:
            QMessageBox.critical(main_window, "오류", f"복원 중 오류가 발생했습니다:\n{str(e)}") 