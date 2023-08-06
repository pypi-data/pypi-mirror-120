import os
import typer
import time

"""
    This part handles the generating of application folders
"""

def generate_folders(projectname):
    os.mkdir(projectname)
    os.chdir(projectname)
    os.mkdir("v1")
    os.mkdir("config")
    os.chdir("v1")
    os.mkdir("Components")
    os.mkdir("Handler")
    os.mkdir("Config")
    os.mkdir("Schema")
    os.mkdir("Models")
    os.mkdir("Routes")
    total = 0
    generating_folders = typer.style(f"Generating folders and files", fg=typer.colors.BLUE, bold=True)
    with typer.progressbar(range(100), label=generating_folders) as progress:
        for value in progress:
            # Fake processing time
            time.sleep(0.02)
            total += 1

