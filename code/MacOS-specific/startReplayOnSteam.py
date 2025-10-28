import subprocess
import shutil

def run_steam_app(app_id):
    # Try to find 'steam' command in PATH
    steam_cmd = shutil.which("steam")
    if steam_cmd:
        command = [steam_cmd, f"steam://run/{app_id}/"]
    else:
        # Assume macOS default Steam path
        steam_cmd = "/Applications/Steam.app/Contents/MacOS/steam_osx"
        command = [steam_cmd, f"steam://run/{app_id}/"]

    try:
        subprocess.run(command, check=True)
        print(f"Steam app {app_id} launched successfully.")
    except Exception as e:
        print(f"Failed to launch Steam app {app_id}: {e}")

if __name__ == "__main__":
    app_id = "0ad7b170-68d8-496e-3fea-08dd25c45c7b"  # Change to your Steam AppID here
    run_steam_app(app_id)
