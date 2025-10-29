import subprocess

#opens replay from id. Polytopia window has to be already open
def open_replay(id):
    # Steam URL to run the game
    steam_url = f"'steam://run/{app_id}'"
    # Use 'open' to launch the steam URL directly
    subprocess.run(["open", steam_url])