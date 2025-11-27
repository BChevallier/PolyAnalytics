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
    "SDL_AUDIODRIVER": "dummy",
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

        # Launch the game by AppID; this will start Steam if needed
        steam_cmd = ["steam", "-applaunch", str(STEAM_APPID)]
        if REPLAY_ID:
            print(f"Launching Replay: {REPLAY_ID}")
            # The argument format "opengame?id=UUID" tells Polytopia to open the replay
            steam_cmd.append(f"opengame?id={REPLAY_ID}")

        p = subprocess.Popen(steam_cmd, env=env)

        try:
            # First launch can take a while (updates, Proton setup, etc.)
            # Debugging showed it takes ~55s to appear
            print("Waiting 90 seconds for game to launch...")
            time.sleep(90)
            window_pattern ="Polytopia"
            maximize_or_resize(window_pattern, WIDTH, HEIGHT)
            # Optional: grab a screenshot of the virtual desktop
            time.sleep(1.0)
            out_name = "replay.png" if REPLAY_ID else "polytopia.png"
            screenshot_window_by_name(window_pattern, out_name)
            print(f"Saved screenshot to {out_name}")
        finally:
            # Try to clean up the game/Steam and WM
            p.terminate()
            try:
                p.wait(timeout=10)
            except Exception:
                p.kill()

            wm.terminate()
            try:
                wm.wait(timeout=5)
            except Exception:
                wm.kill()

if __name__ == "__main__":
    main()
