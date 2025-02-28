import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import requests
import zipfile
import sys

# URLs for downloading ADB and scrcpy
ADB_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
SCRCPY_URL = "https://github.com/Genymobile/scrcpy/releases/download/v2.1/scrcpy-win64-v2.1.zip"

ADB_DIR = "platform-tools"
SCRCPY_DIR = "scrcpy"
ADB_EXE = os.path.join(ADB_DIR, "adb.exe") if sys.platform == "win32" else os.path.join(ADB_DIR, "adb")
SCRCPY_EXE = os.path.join(SCRCPY_DIR, "scrcpy.exe")

# Function to download and extract a zip file
def download_and_extract(url, extract_to):
    zip_path = f"{extract_to}.zip"
    if not os.path.exists(extract_to):
        print(f"Downloading {url}...")
        response = requests.get(url, stream=True)
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        
        print(f"Extracting {extract_to}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove(zip_path)
        print(f"{extract_to} installed successfully.")

# Function to install ADB and scrcpy
def install_tools():
    download_and_extract(ADB_URL, ADB_DIR)
    download_and_extract(SCRCPY_URL, SCRCPY_DIR)

# Function to check if a device is connected
def check_device():
    try:
        result = subprocess.run([ADB_EXE, "devices"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        devices = [line for line in lines if "device" in line and not "List" in line]
        if devices:
            return True
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check device: {e}")
        return False

# Function to send a tap command
def tap_screen():
    x = x_entry.get()
    y = y_entry.get()
    if not x.isdigit() or not y.isdigit():
        messagebox.showerror("Error", "Enter valid coordinates.")
        return
    subprocess.run([ADB_EXE, "shell", "input", "tap", x, y])
    messagebox.showinfo("Success", f"Tapped at ({x}, {y})")

# Function to launch scrcpy (screen mirroring)
def launch_scrcpy():
    if not check_device():
        messagebox.showwarning("Warning", "No Android device detected. Make sure USB Debugging is enabled.")
        return
    subprocess.Popen([SCRCPY_EXE])

# Function to press Back button
def press_back():
    subprocess.run([ADB_EXE, "shell", "input", "keyevent", "4"])

# Function to press Home button
def press_home():
    subprocess.run([ADB_EXE, "shell", "input", "keyevent", "3"])

# Install tools if not already installed
install_tools()

# Setup GUI
root = tk.Tk()
root.title("Android Control Panel")
root.geometry("300x250")

tk.Label(root, text="X Coordinate:").pack()
x_entry = tk.Entry(root)
x_entry.pack()

tk.Label(root, text="Y Coordinate:").pack()
y_entry = tk.Entry(root)
y_entry.pack()

tk.Button(root, text="Tap Screen", command=tap_screen).pack()
tk.Button(root, text="Launch Scrcpy (View Screen)", command=launch_scrcpy).pack()
tk.Button(root, text="Back", command=press_back).pack()
tk.Button(root, text="Home", command=press_home).pack()

if not check_device():
    messagebox.showwarning("Warning", "No Android device detected. Make sure USB Debugging is enabled.")

root.mainloop()
