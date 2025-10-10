import os
import sys
import subprocess

def main():
    print("Setting up virtual environment...")

    # Navigate to the target directory
    os.chdir("./Files")

    # Create venv
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    # Determine activation command based on OS
    if os.name == "nt":  # Windows
        activate_script = ".\\venv\\Scripts\\activate.bat"
    else:  # Unix-like
        activate_script = "source ./venv/bin/activate"

    print(f"To activate the venv, run:\n{activate_script}")

    # Install requirements
    pip_path = os.path.join("venv", "Scripts" if os.name == "nt" else "bin", "pip")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)

    print("Setup complete.")

if __name__ == "__main__":
    main()