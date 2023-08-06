import typer
import time
import os
from pathlib import Path

from  .components.generate_folders import *
from  .config import *

app = typer.Typer()

@app.command("create-app")
def main(projectname: str):
    try:
        # Progress Bar
        total = 0
        generating = typer.style(f"Creating {projectname} application boilerplate", fg=typer.colors.BLUE, bold=True)
        with typer.progressbar(range(100), label=generating) as progress:
            for value in progress:
                # Fake processing time
                time.sleep(0.02)
                total += 1

        # Generate Folders
        generate_folders(projectname)

        # Generate Default Python Files
        with open("__init__.py", 'w') as f:
            f.write("")
        os.chdir("..")
        with open("main.py", 'w') as f:
            f.write(main_config)
        with open("requirements.txt", 'w') as f:
            f.write(requirements)
        os.chdir("config")
        with open("settings.py", 'w') as f:
            f.write(settings)
        with open("__init__.py", 'w') as f:
            f.write("")
        with open("constant.py", 'w') as f:
            f.write(constant)

        # Finalizing CLI
        finalizing = typer.style(f"Finalizing boilerplate", fg=typer.colors.BLUE, bold=True)
        with typer.progressbar(range(100), label=finalizing) as progress:
            for value in progress:
                # Fake processing time
                time.sleep(0.03)
                total += 1

        success_message = f"""
        <------------------------------------------------------->
            {projectname} Application Boilerplate Successfully Created.
            Enjoy developing using FastAPI!
            
            CLI Version : v.1.0
            Author : Gian Carlo L. Garcia
        <------------------------------------------------------->
        """
        print(typer.style(success_message, fg=typer.colors.GREEN, bold=True))
    except Exception as e:
        print(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command("test")
def cli_test():
    print("Still")

if __name__ == "__main__":
    app()
