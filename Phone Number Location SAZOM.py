import os
import requests
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style, ttk
from tqdm import tqdm
import shutil
import subprocess

# إعدادات التحميل
GITHUB_URL = "https://raw.githubusercontent.com/SAZOMa-z/files-pro/main/pnlp/"  # استبدل بالمسار الصحيح للملفات
RELEASE_URL = "https://github.com/SAZOMa-z/files-pro/releases/download/v1.0/main.exe"  # استبدل برابط الإصدار
FILES_TO_DOWNLOAD = [
    "bg.gif",
    "bg.mp3",
    "delete.mp3",
    "error.mp3",
    "locate.mp3",
    "notification.mp3"
]
DOWNLOAD_DIR = "./pnlp/"
EXT_DOWNLOAD_DIR = f"./pnlp/ext/"

# التأكد من وجود مجلد التحميل الرئيسي
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# التأكد من وجود مجلد التحميل الإضافي
if not os.path.exists(EXT_DOWNLOAD_DIR):
    os.makedirs(EXT_DOWNLOAD_DIR)

def download_file(url, dest_folder, progress_callback, file_index):
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 كيلو بايت
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    
    downloaded_size = 0
    with open(local_filename, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            downloaded_size += len(data)
            progress_callback(file_index, downloaded_size, total_size)
            f.write(data)
    progress_bar.close()
    
    if total_size != 0 and progress_bar.n != total_size:
        print("ERROR, something went wrong")
    return local_filename

def download_files(progress_callback):
    for index, file in enumerate(FILES_TO_DOWNLOAD):
        url = GITHUB_URL + file
        file_path = download_file(url, DOWNLOAD_DIR, progress_callback, index)
        print(f"Downloaded {file_path}")

def download_main_exe(progress_callback):
    url = RELEASE_URL
    file_path = download_file(url, DOWNLOAD_DIR, progress_callback, len(FILES_TO_DOWNLOAD))
    print(f"Downloaded {file_path}")

def move_files_except_main():
    for file in os.listdir(DOWNLOAD_DIR):
        src_file = os.path.join(DOWNLOAD_DIR, file)
        dst_file = os.path.join(EXT_DOWNLOAD_DIR, file)
        if os.path.isfile(src_file) and file != "main.exe":
            if os.path.exists(dst_file):
                os.remove(dst_file)  # حذف الملف إذا كان موجودًا
            shutil.move(src_file, dst_file)

def check_files_complete():
    missing_files = [file for file in FILES_TO_DOWNLOAD if not os.path.exists(os.path.join(EXT_DOWNLOAD_DIR, file))]
    if not os.path.exists(os.path.join(DOWNLOAD_DIR, "main.exe")):
        missing_files.append("main.exe")
    return len(missing_files) == 0

def start_main_program():
    try:
        main_exe_path = os.path.join(DOWNLOAD_DIR, "main.exe")
        if os.path.exists(main_exe_path):
            subprocess.Popen(main_exe_path, shell=True)
            os._exit(0)  # لإغلاق البرنامج الحالي بعد فتح main.exe
        else:
            raise FileNotFoundError(f"{main_exe_path} not found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start main program: {e}")

def setup_gui():
    root = tk.Tk()
    root.title("Phone Number Location Downloader Files")
    root.geometry("400x430")
    root.resizable(False, False)
    Style(theme="cosmo")

    frame = ttk.Frame(root, padding="10")
    frame.pack(pady=20)

    title_label = ttk.Label(frame, text="Downloading Files...", font=("Helvetica", 16))
    title_label.pack(pady=10)

    progress_bars = []
    progress_labels = []
    for file in FILES_TO_DOWNLOAD + ["main.exe"]:
        file_frame = ttk.Frame(frame)
        file_frame.pack(fill="x", pady=5)
        progress_label = ttk.Label(file_frame, text=file)
        progress_label.pack(side="left")
        progress_bar = ttk.Progressbar(file_frame, mode="determinate")
        progress_bar.pack(side="right", fill="x", expand=True, padx=10)
        progress_bars.append(progress_bar)
        progress_labels.append(progress_label)

    def progress_callback(file_index, downloaded_size, total_size):
        progress = int((downloaded_size / total_size) * 100)
        progress_bars[file_index].config(value=progress)
        root.update_idletasks()

    def start_download():
        for bar in progress_bars:
            bar.config(value=0)
        root.after(100, lambda: download_files(progress_callback))
        root.after(2000, lambda: download_main_exe(progress_callback))
        root.after(3000, move_files_except_main)
        root.after(4000, lambda: messagebox.showinfo("Download Complete", "All files have been downloaded successfully."))
        root.after(5000, start_main_program)

    download_button = ttk.Button(frame, text="Start Download", style="success.TButton", command=start_download)
    download_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    if check_files_complete():
        tk.Tk().withdraw()  # لإخفاء نافذة tkinter الأساسية
        messagebox.showwarning("Files Check", "All required files are already present.")
        start_main_program()
    else:
        setup_gui()
