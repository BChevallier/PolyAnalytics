import os
import time
import subprocess
import psutil
import pyscreenshot as ImageGrab
from pyvirtualdisplay import Display

# Configuration
WIDTH = 1280
HEIGHT = 800
STEAM_APPID = 874390  # Polytopia
REPLAY_ID = "7fd4ddbf-028b-49a3-4071-08dd25c45c7b"
LOG_FILE = "steam_run.log"
SCREENSHOT_DIR = "debug_screenshots"

# Environment for software rendering
SW_RENDER_ENV = {
    "LIBGL_ALWAYS_SOFTWARE": "1",
    "MESA_LOADER_DRIVER_OVERRIDE": "llvmpipe",
    "SDL_VIDEODRIVER": "x11",
    "LIBGL_DEBUG": "verbose"
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")

def check_processes():
    """Check if Steam or the Game is running."""
    steam_running = False
    game_running = False
    # Polytopia's binary name on Linux is usually 'Polytopia' or 'Polytopia.x86_64'
    game_names = ["Polytopia", "Polytopia.x86_64", "Polytopia.exe"]
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info['name']
            if "steam" in name.lower():
                steam_running = True
            
            if name in game_names:
                game_running = True
                log(f"FOUND GAME PROCESS: {name} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return steam_running, game_running

def take_screenshot(name):
    try:
        filename = os.path.join(SCREENSHOT_DIR, f"{name}.png")
        img = ImageGrab.grab(bbox=(0, 0, WIDTH, HEIGHT))
        img.save(filename)
        log(f"Screenshot saved: {filename}")
    except Exception as e:
        log(f"Failed to take screenshot: {e}")

def main():
    ensure_dir(SCREENSHOT_DIR)
    # Clear old log
    with open(LOG_FILE, "w") as f: f.write("Starting Run Session\n")

    # 1. Start Virtual Display
    log("Starting Xvfb...")
    with Display(visible=False, size=(WIDTH, HEIGHT), color_depth=24) as disp:
        env = os.environ.copy()
        env.update(SW_RENDER_ENV)
        # pyvirtualdisplay sets the DISPLAY variable in os.environ
        log(f"DISPLAY passed to subprocess: {env.get('DISPLAY')}")

        # 2. Start Window Manager (Openbox)
        log("Starting Openbox...")
        wm = subprocess.Popen(["openbox"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)

        # 3. Launch Steam with Replay
        log(f"Launching Steam with Replay ID {REPLAY_ID}...")
        
        # Use steam:// protocol to avoid argument parsing crashes
        steam_cmd = ["steam", f"steam://run/{STEAM_APPID}//opengame?id={REPLAY_ID}"]
        
        # Open a file for steam stdout/stderr
        steam_out = open("steam_output.txt", "w")
        p = subprocess.Popen(steam_cmd, env=env, stdout=steam_out, stderr=steam_out)

        # 4. Monitor Loop
        # We will loop for 2 minutes, taking screenshots and checking processes
        max_retries = 24 # 24 * 5 seconds = 120 seconds
        for i in range(max_retries):
            time.sleep(5)
            steam_active, game_active = check_processes()
            
            status = f"Steam: {'UP' if steam_active else 'DOWN'}, Game: {'UP' if game_active else 'DOWN'}"
            log(f"Loop {i+1}/{max_retries}: {status}")
            
            take_screenshot(f"step_{i:02d}_{'game' if game_active else 'wait'}")

            if not steam_active and i > 5:
                log("Steam process seems to have died.")
                break

        # Cleanup
        log("Stopping Steam...")
        p.terminate()
        try:
            p.wait(timeout=10)
        except:
            p.kill()
        
        steam_out.close()
        
        log("Stopping WM...")
        wm.terminate()

if __name__ == "__main__":
    main()
