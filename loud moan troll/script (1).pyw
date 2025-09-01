import sys
import subprocess
import tempfile
import time

# -----------------------------
# Ensure required modules are installed
# -----------------------------
for package in ["gdown", "pygame", "pycaw", "comtypes"]:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

import gdown
import pygame
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# -----------------------------
# Set Windows system volume to 100%
# -----------------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
original_volume = volume.GetMasterVolumeLevelScalar()  # Save current volume
volume.SetMasterVolumeLevelScalar(1.0, None)           # Set to 100%

# -----------------------------
# Google Drive file ID
# -----------------------------
file_id = "1bxdOgQWtDlBDjgpq4Jh1KrRsgN1uOa7w"

# -----------------------------
# Download the file
# -----------------------------
print("Downloading audio from Google Drive...")
output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)

# -----------------------------
# Play audio at full Python volume
# -----------------------------
pygame.mixer.init()
pygame.mixer.music.load(output_file)
pygame.mixer.music.set_volume(1.0)  # Max Python volume
pygame.mixer.music.play()

# Wait until playback finishes
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# -----------------------------
# Restore original Windows volume
# -----------------------------
volume.SetMasterVolumeLevelScalar(original_volume, None)

sys.exit(0)
