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

# Environment to make rendering work under Xvfb (no GPU)
SW_RENDER_ENV = {
    "LIBGL_ALWAYS_SOFTWARE": "1",
    "MESA_LOADER_DRIVER_OVERRIDE": "llvmpipe",
    "__GLX_VENDOR_LIBRARY_NAME": "mesa",
    "GDK_BACKEND": "x11",
    "QT_QPA_PLATFORM": "xcb",
    "SDL_VIDEODRIVER": "x11",
    "SDL_AUDIODRIVER": "dummy",
    # If the game is Windows-only via Proton and you have no Vulkan, prefer OpenGL:
    # "PROTON_USE_WINED3D": "1",
    # If you want software Vulkan (very slow), point to lavapipe ICD (path may vary):
    # "VK_ICD_FILENAMES": "/usr/share/vulkan/icd.d/lvp_icd.x86_64.json",
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
        p = subprocess.Popen(["steam", "-applaunch", str(STEAM_APPID)], env=env)

        try:
            # First launch can take a while (updates, Proton setup, etc.)
            time.sleep(40)
            window_pattern ="Polytopia"
            maximize_or_resize(window_pattern, WIDTH, HEIGHT)
            # Optional: grab a screenshot of the virtual desktop
            time.sleep(1.0)
            screenshot_window_by_name(window_pattern, "polytopia.png")
            print("Saved screenshot to steam_game.png")
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
