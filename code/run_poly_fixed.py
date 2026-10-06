import os
import time
import subprocess
import psutil
import pyscreenshot as ImageGrab
from pyvirtualdisplay import Display
import imageProcessing as ipro
import colorProcessing as cpro
import dataHandling
import pandas as pd
import numpy as np
import sys

# Configuration
WIDTH = 1280
HEIGHT = 800
STEAM_APPID = 874390  # Polytopia
LOG_FILE = "steam_run.log"
SCREENSHOT_DIR = "debug_screenshots"

# Environment for software rendering
SW_RENDER_ENV = {
    "LIBGL_ALWAYS_SOFTWARE": "1",
    "MESA_LOADER_DRIVER_OVERRIDE": "llvmpipe",
    "SDL_VIDEODRIVER": "x11",
    "LIBGL_DEBUG": "verbose",
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
    game_names = ["Polytopia", "Polytopia.x86_64", "Polytopia.exe"]

    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            name = proc.info["name"]
            if "steam" in name.lower():
                steam_running = True

            if name in game_names:
                game_running = True
                log(f"FOUND GAME PROCESS: {name} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return steam_running, game_running


def take_screenshot(name=None):
    try:
        img = ImageGrab.grab(bbox=(0, 0, WIDTH, HEIGHT))
        if name:
            filename = os.path.join(SCREENSHOT_DIR, f"{name}.png")
            img.save(filename)
            log(f"Screenshot saved: {filename}")
        return img
    except Exception as e:
        log(f"Failed to take screenshot: {e}")
        return None


def setup_input_module():
    """Detect and import the best available input module."""
    # the input modules live in Linux-specific/ (not importable as a package because of the hyphen)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "Linux-specific"))
    try:
        import linuxInputs_evdev as inputs

        log("Using evdev (hardware-level input)")
        return inputs, "evdev"
    except (ImportError, OSError, RuntimeError) as e:  # the module raises RuntimeError if evdev is missing
        log(f"evdev not available ({e}), falling back to pynput")
        try:
            import linuxInputs as inputs

            log("Using pynput (X11 input)")
            return inputs, "pynput"
        except (ImportError, RuntimeError):
            log("WARNING: No input module available!")
            return None, None


def launch_replay(replay_id, inputs, env):
    """Launch Steam with a specific replay ID and wait for game to start."""
    log(f"Launching Steam with Replay ID {replay_id}...")
    steam_cmd = ["steam", f"steam://run/{STEAM_APPID}//opengame?id={replay_id}"]
    
    steam_out = open("steam_output.txt", "w")
    p = subprocess.Popen(steam_cmd, env=env, stdout=steam_out, stderr=steam_out)
    
    # Wait for game to start
    max_retries = 24  # 2 minutes
    game_started = False
    
    for i in range(max_retries):
        time.sleep(5)
        steam_active, game_active = check_processes()
        
        status = f"Steam: {'UP' if steam_active else 'DOWN'}, Game: {'UP' if game_active else 'DOWN'}"
        log(f"Loop {i + 1}/{max_retries}: {status}")
        
        if game_active and not game_started:
            game_started = True
            log("Game detected! Waiting for it to fully load...")
            time.sleep(5)
            return p, steam_out, True
        
        if not steam_active and i > 5:
            log("Steam process died.")
            break
    
    return p, steam_out, False


def collect_replay_data(replay_id, inputs):
    """Collect data from a single replay. This mirrors dataCollection.py logic."""
    log(f"Collecting data for replay {replay_id}")
    
    # Pause game
    time.sleep(0.8)
    inputs.pause_game()
    inputs.mouse_diag_drag(120, 120)  # move camera to avoid messy background
    
    data = {}
    player_colors = {}
    
    # Get menu info
    log("Getting menu infos")
    inputs.mouse_click_nominal(640, 430)  # open menu
    time.sleep(1.5)
    frame = take_screenshot()
    if frame is None:
        log("Failed to capture screenshot")
        return None
    
    mSize, mType = ipro.get_menu_info(frame)
    data["mSize"] = mSize
    data["mType"] = mType
    inputs.press_key(53)  # escape menu
    
    # Identify Tribes
    for Player in ["A", "B"]:
        log(f"Identifying tribe of Player {Player}")
        inputs.press_key(18 if Player == "A" else 19)  # press 1 or 2
        time.sleep(0.1)
        frame = take_screenshot()
        if frame is None:
            continue
        
        player_color = ipro.get_color_from_coords(frame, [(9, 33)])[0]
        player_colors[Player] = player_color
        tribe_by_color = cpro.identify_tribe(player_color)
        
        inputs.mouse_click_nominal(700, 430)  # open tech tree
        time.sleep(0.1)
        inputs.scroll(-50)  # zoom out
        time.sleep(0.2)
        frame = take_screenshot()
        if frame is None:
            continue
        
        starting_tech = ipro.get_techs(frame)
        tribes_by_techs = ipro.tribe_from_tech(starting_tech)
        
        if tribe_by_color in tribes_by_techs:
            data[f"Tribe{Player}"] = tribe_by_color
            log(f"Player {Player} has color: {player_color}")
        else:
            data[f"Tribe{Player}"] = np.nan
        
        inputs.press_key(53)  # press escape
        time.sleep(0.2)
    
    # Check if 1v1
    inputs.press_key(20)  # press 3 to see if there is a third player
    time.sleep(0.2)
    frame = take_screenshot()
    if frame is not None and "B" in player_colors:
        if cpro.colors_are_similar(ipro.get_color_from_coords(frame, [(9, 33)])[0], player_colors["B"]):
            data["1v1"] = True
        else:
            data["1v1"] = False
    
    # Winner detection for 1v1 games
    if data.get("1v1") == True:
        inputs.press_key(29)
        counter = 0
        is_at_end = False
        log("Scrolling to the end")
        while not is_at_end:
            counter += 1
            inputs.move_turn_bar()
            time.sleep(0.5)
            frame = take_screenshot()
            if frame is not None:
                is_at_end = ipro.check_for_end(frame)
            time.sleep(0.5)
            if counter == 40:
                log("Scrolled 40 times without finding the end")
                break
        
        if frame is not None:
            color_at_end = ipro.get_color_from_coords(frame, [(9, 33)])[:3][0]
            log(f"Color at end is: {color_at_end}")
            if cpro.colors_are_similar(color_at_end, player_colors["B"]):
                data["Winner"] = "B"
            elif cpro.colors_are_similar(color_at_end, player_colors["A"]):
                data["Winner"] = "A"
            else:  # matches neither player: leave the winner empty instead of guessing
                log(f"Color at end matches neither player (A: {player_colors['A']}, B: {player_colors['B']})")
    
    time.sleep(3)
    return data


def main():
    ensure_dir(SCREENSHOT_DIR)
    ensure_dir("collected_data")
    with open(LOG_FILE, "w") as f:
        f.write("Starting Run Session\n")

    # Setup input system
    inputs, input_type = setup_input_module()
    if not inputs:
        log("ERROR: No input module available!")
        return
    log(f"Input system: {input_type}")

    # Start Virtual Display
    log("Starting Xvfb...")
    with Display(visible=False, size=(WIDTH, HEIGHT), color_depth=24) as disp:
        env = os.environ.copy()
        env.update(SW_RENDER_ENV)

        # FIX: Set XAUTHORITY to avoid warnings
        xauth_path = os.path.expanduser("~/.Xauthority")
        if os.path.exists(xauth_path):
            env["XAUTHORITY"] = xauth_path
        else:
            env["XAUTHORITY"] = "/dev/null"

        log(f"DISPLAY: {env.get('DISPLAY')}")
        log(f"XAUTHORITY: {env.get('XAUTHORITY')}")

        # Start Window Manager (Openbox)
        log("Starting Openbox...")
        wm = subprocess.Popen(
            ["openbox"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        time.sleep(2)

        # Process batches of replays
        for batch_num in range(1, 2):
            columns = ["mType", "mSize", "TribeA", "TribeB", "1v1", "Winner"]
            batch = dataHandling.takebatch(batch_num)
            df = pd.DataFrame(index=batch, columns=columns)
            
            for replay_id in batch:
                log(f"Processing replay {replay_id}")
                
                # Launch replay
                p, steam_out, game_started = launch_replay(replay_id, inputs, env)
                
                if game_started:
                    # Collect data
                    data = collect_replay_data(replay_id, inputs)
                    
                    if data:
                        for key, value in data.items():
                            df.at[replay_id, key] = value
                        
                        # Check if we got all required data
                        if df.loc[replay_id].iloc[:4].isnull().all():
                            log(f"WARNING: Got None values in a row at id {replay_id}")
                
                # Cleanup this replay
                log("Stopping game...")
                p.terminate()
                try:
                    p.wait(timeout=10)
                except:
                    p.kill()
                steam_out.close()
                
                # Save after every game, so a crash doesn't lose the batch
                df.to_csv(f"collected_data/Batch{batch_num}.csv")

                # Wait for cleanup
                time.sleep(5)
            
            # Save batch results
            output_file = f"collected_data/Batch{batch_num}.csv"
            df.to_csv(output_file)
            log(f"Saved batch {batch_num} to {output_file}")
            print(df)

        # Final cleanup
        log("Stopping WM...")
        wm.terminate()

        # Cleanup input devices if using evdev
        if inputs and input_type == "evdev":
            try:
                inputs.cleanup()
                log("Cleaned up evdev devices")
            except:
                pass


if __name__ == "__main__":
    main()
