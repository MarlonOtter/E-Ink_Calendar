import subprocess
import os
import sys
import platform

def main():
    print("Running setup.py...")
    subprocess.run([sys.executable, "setup.py"], check=True)

    # Step 2: Change directory to ./Files
    os.chdir("Files")

    # Step 3: Determine venv Python path
    if platform.system() == "Windows":
        venv_python = os.path.join("venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join("venv", "bin", "python")

    # Step 4: Run main.py using venv's Python
    print("Running main.py inside venv...")
    subprocess.run([venv_python, "main.py"], check=True)

if __name__ == "__main__":
    main()