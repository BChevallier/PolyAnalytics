import subprocess

#opens replay from id. Polytopia window has to be already open
def open_replay(id):
    # Steam URL to run the game
    steam_url = f"'steam://run/874390//opengame?id={id}'"
    # Use 'open' to launch the steam URL directly
    subprocess.run("open "+steam_url,shell=True)

if __name__=="__main__":
    open_replay("0ad7b170-68d8-496e-3fea-08dd25c45c7b")