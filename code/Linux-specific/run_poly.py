from pyvirtualdisplay import Display
import subprocess
import time
import os
import shlex

# Configure your virtual screen
WIDTH = 1280
HEIGHT = 800
COLOR_DEPTH = 24

# Your game AppID (example: Polytopia)
STEAM_APPID = 874390
# Optional: Replay ID to launch directly (set to None for normal game)
# Example: "7fd4ddbf-028b-49a3-4071-08dd25c45c7b"
REPLAY_ID = "7fd4ddbf-028b-49a3-4071-08dd25c45c7b"

# Environment to make rendering work under Xvfb (no GPU)
SW_RENDER_ENV = {
    "LIBGL_ALWAYS_SOFTWARE": "1",
    "MESA_LOADER_DRIVER_OVERRIDE": "llvmpipe",
    "SDL_VIDEODRIVER": "x11",
    "LIBGL_DEBUG": "verbose",
}

def start_wm():
    # Lightweight window manager so apps aren't stuck at 0,0 tiny
    return subprocess.Popen(
        ["openbox"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
    )

def screenshot_root(outfile="steam_game.png"):
    # Use xwd + ImageMagick convert for reliable Xvfb screenshots
    cmd = f'xwd -root -silent | convert xwd:- png:{shlex.quote(outfile)}'
    subprocess.run(["bash", "-lc", cmd], check=True, env=os.environ.copy())
    return outfile
def screenshot_window_by_name(name_pattern, outfile="polytopia.png"):
    # Find window id
    wid = subprocess.check_output(
        ["xdotool", "search", "--onlyvisible", "--name", name_pattern],
        stderr=subprocess.STDOUT,
    ).decode().strip().splitlines()[-1]
    cmd = f'xwd -id {shlex.quote(wid)} -silent | convert xwd:- png:{shlex.quote(outfile)}'
    subprocess.run(["bash", "-lc", cmd], check=True, env=os.environ.copy())
    return outfile
def maximize_or_resize(name_pattern, w=WIDTH, h=HEIGHT):
    # Try to maximize via WM; fallback to explicit geometry
    try:
        subprocess.run(
            ["wmctrl", "-r", name_pattern, "-b", "add,maximized_vert,maximized_horz"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return
    except subprocess.CalledProcessError:
        pass
    try:
        wid = subprocess.check_output(
            ["xdotool", "search", "--onlyvisible", "--name", name_pattern],
            stderr=subprocess.STDOUT,
        ).decode().strip().splitlines()[-1]
        subprocess.run(["xdotool", "windowsize", wid, str(w), str(h)], check=False)
        subprocess.run(["xdotool", "windowmove", wid, "0", "0"], check=False)
    except subprocess.CalledProcessError:
        pass


def main():
    env = os.environ.copy()
    env.update(SW_RENDER_ENV)
      #game_flags = [
        #"-windowed",
        #"-noborder",
        #"-screen-fullscreen", "0",
        #"-screen-width", str(WIDTH),
        #"-screen-height", str(HEIGHT),
    #]
    # Start virtual display
    with Display(visible=False, size=(WIDTH, HEIGHT), color_depth=COLOR_DEPTH) as disp:
        print(f"DISPLAY set to {os.environ.get('DISPLAY')}")
        wm = start_wm()
        time.sleep(1.0)

        # 3. Launch Steam (Client only first)
        # This ensures the Steam runtime is loaded before we try to launch the game
        print("Starting Steam client...")
        steam_log = open("steam_run.log", "w")
        steam_proc = subprocess.Popen(["steam", "-silent"], env=env, stdout=steam_log, stderr=steam_log)
        
        # Wait for Steam to initialize
        time.sleep(15)

        # 4. Launch Game / Replay
        print(f"Launching Polytopia (Replay: {REPLAY_ID if REPLAY_ID else 'No'})...")
        if REPLAY_ID:
            # Use steam:// protocol which is robust when Steam is already running
            launch_cmd = ["steam", "-silent", f"steam://run/{STEAM_APPID}//opengame?id={REPLAY_ID}"]
        else:
            launch_cmd = ["steam", "-silent", "-applaunch", str(STEAM_APPID)]
            
        # We don't need to keep track of this process, it just signals the main Steam instance
        subprocess.Popen(launch_cmd, env=env, stdout=steam_log, stderr=steam_log)

        try:
            print("Waiting for game window...")
            window_pattern = "Polytopia"
            
            # Wait up to 120s for window
            found = False
            for i in range(60):
                # Check if Steam client is still alive
                if steam_proc.poll() is not None:
                    print("Steam client exited prematurely!")
                    break
                
                try:
                    subprocess.check_call(["xdotool", "search", "--onlyvisible", "--name", window_pattern], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    found = True
                    break
                except subprocess.CalledProcessError:
                    time.sleep(2)
            
            if not found:
                print("Game window not found (or Steam crashed).")
                # Take a debug screenshot of whatever is there
                screenshot_root("debug_crash.png")
                return

            print("Game window found!")
            time.sleep(5) # Wait for it to fully render
            maximize_or_resize(window_pattern, WIDTH, HEIGHT)
            # Optional: grab a screenshot of the virtual desktop
            time.sleep(1.0)
            out_name = "replay.png" if REPLAY_ID else "polytopia.png"
            screenshot_window_by_name(window_pattern, out_name)
            print(f"Saved screenshot to {out_name}")
        finally:
            # Try to clean up the game/Steam and WM
            if steam_proc:
                steam_proc.terminate()
                try:
                    steam_proc.wait(timeout=10)
                except Exception:
                    steam_proc.kill()
            
            if steam_log:
                steam_log.close()

            wm.terminate()
            try:
                wm.wait(timeout=5)
            except Exception:
                wm.kill()

if __name__ == "__main__":
    main()
