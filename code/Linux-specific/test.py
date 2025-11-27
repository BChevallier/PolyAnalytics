#!/usr/bin/env python3
"""
Automate launching Polytopia replay under a virtual X display, capture screenshot, then exit.

Steps:
1. Start Xvfb :99 with 800x500 resolution.
2. Launch Steam with Polytopia (AppID 874390).
3. Wait for window named "Polytopia".
4. Open replay via steam:// URL.
5. Resize window to 800x500, take screenshot of that window only.
6. Kill Steam and Xvfb.

Replay example used: 0ad7b170-68d8-496e-3fea-08dd25c45c7b

Tested assumptions:
- Steam in PATH (non-snap). Snap steam may fail under Xvfb due to GPU/permissions.
- xdotool, Xvfb, ImageMagick (import/convert or xwd + convert) installed.
"""

import os
import subprocess
import time
import signal
import shutil
import sys
from pathlib import Path

APP_ID = "874390"
REPLAY_ID = "0ad7b170-68d8-496e-3fea-08dd25c45c7b"
DISPLAY_NUM = 99           # virtual display :99
SCREEN_GEOM = "800x500x24"
TARGET_WIDTH = 800
TARGET_HEIGHT = 500
WINDOW_NAME_PATTERN = "Polytopia"
SCREENSHOT_FILE = "polytopia_replay.png"
XVFB_CMD = ["Xvfb", f":{DISPLAY_NUM}", "-screen", "0", SCREEN_GEOM, "-nolisten", "tcp"]

# Choose screenshot method: xwd + convert is robust in headless X.
USE_XWD = True

def require(cmd):
    if shutil.which(cmd) is None:
        print(f"[ERROR] Required command '{cmd}' not found on PATH.")
        sys.exit(1)

def start_xvfb():
    print(f"[INFO] Starting Xvfb on :{DISPLAY_NUM} with geometry {SCREEN_GEOM}")
    xvfb_proc = subprocess.Popen(XVFB_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait until X socket appears or timeout
    socket_path = Path(f"/tmp/.X11-unix/X{DISPLAY_NUM}")
    for _ in range(50):  # ~5 seconds
        if socket_path.exists():
            print("[INFO] Xvfb is up.")
            return xvfb_proc
        time.sleep(0.1)
    print("[ERROR] Xvfb did not start within timeout.")
    xvfb_proc.terminate()
    sys.exit(1)

def steam_launch_polytopia(env):
    # Launch Steam and directly start Polytopia:
    # Use steam -applaunch <APPID> for direct app start.
    cmd = ["steam", "-applaunch", APP_ID]
    print(f"[INFO] Launching Steam with Polytopia: {' '.join(cmd)}")
    steam_proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return steam_proc

def wait_for_window(name_pattern, env, timeout=120, poll=2):
    print(f"[INFO] Waiting for window named pattern '{name_pattern}' (timeout {timeout}s)")
    end = time.time() + timeout
    while time.time() < end:
        try:
            out = subprocess.check_output(
                ["xdotool", "search", "--onlyvisible", "--name", name_pattern],
                stderr=subprocess.DEVNULL,
                env=env
            ).decode().strip().splitlines()
            if out:
                wid = out[-1]
                print(f"[INFO] Found window id {wid}")
                return wid
        except subprocess.CalledProcessError:
            pass
        print(f"[DEBUG] Window not yet found, retry in {poll}s...")
        time.sleep(poll)
    raise RuntimeError(f"Window '{name_pattern}' not found after {timeout}s")

def open_replay(replay_id, env):
    url = f"steam://run/{APP_ID}//opengame?id={replay_id}"
    print(f"[INFO] Opening replay via URL: {url}")
    # xdg-open will delegate to Steam URL handler
    subprocess.Popen(["xdg-open", url], env=env)

def resize_window(wid, width, height, env):
    print(f"[INFO] Resizing window {wid} to {width}x{height}")
    try:
        subprocess.check_call(["xdotool", "windowsize", wid, str(width), str(height)], env=env)
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Could not resize window: {e}")

def screenshot_window(wid, filename, env):
    print(f"[INFO] Capturing screenshot to {filename}")
    if USE_XWD:
        # xwd capture + convert to PNG
        raw_file = filename + ".xwd"
        subprocess.check_call(["xwd", "-silent", "-id", wid, "-out", raw_file], env=env)
        subprocess.check_call(["convert", raw_file, filename], env=env)
        os.remove(raw_file)
    else:
        # ImageMagick import alternative
        subprocess.check_call(["import", "-window", wid, filename], env=env)
    print(f"[INFO] Screenshot saved: {filename}")

def graceful_terminate(proc, name, timeout=10):
    if proc.poll() is not None:
        print(f"[INFO] {name} already exited.")
        return
    print(f"[INFO] Terminating {name} (PID {proc.pid})")
    proc.terminate()
    try:
        proc.wait(timeout=timeout)
        print(f"[INFO] {name} terminated cleanly.")
    except subprocess.TimeoutExpired:
        print(f"[WARN] {name} did not exit, killing.")
        proc.kill()

def main():
    # Ensure required tools
    for c in ["Xvfb", "xdotool", "xwd" if USE_XWD else "import", "convert" if USE_XWD else "import", "steam", "xdg-open"]:
        require(c)

    # Start virtual display
    xvfb_proc = start_xvfb()
    env = os.environ.copy()
    env["DISPLAY"] = f":{DISPLAY_NUM}"

    try:
        # Launch Steam + game
        steam_proc = steam_launch_polytopia(env)

        # Give Steam time to spin up before searching window (adjust if slow)
        print("[INFO] Initial wait for Steam/Polytopia to start (30s)")
        time.sleep(30)

        # Wait for game window
        wid = wait_for_window(WINDOW_NAME_PATTERN, env, timeout=120)

        # Resize window
        resize_window(wid, TARGET_WIDTH, TARGET_HEIGHT, env)

        # Open specific replay
        open_replay(REPLAY_ID, env)

        print("[INFO] Waiting a bit for replay to load (10s)")
        time.sleep(10)

        # Re-find window (in case of reopening)
        try:
            wid = wait_for_window(WINDOW_NAME_PATTERN, env, timeout=30)
        except RuntimeError:
            print("[WARN] Window disappeared; attempting screenshot of last known id anyway.")

        # Screenshot
        screenshot_window(wid, SCREENSHOT_FILE, env)

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # Close Steam (attempt a polite exit via SIGTERM)
        graceful_terminate(steam_proc, "Steam")

        print("[INFO] Shutting down Xvfb")
        graceful_terminate(xvfb_proc, "Xvfb")

    print("[INFO] Done.")

if __name__ == "__main__":
    main()
