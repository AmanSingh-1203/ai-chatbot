import sys
import subprocess
import importlib
import os

REQ_FILE = "requirements.txt"


def install_requirements():
    if not os.path.exists(REQ_FILE):
        return True
    print("Checking and installing dependencies (may ask for permission)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQ_FILE])
        return True
    except subprocess.CalledProcessError:
        print("Failed to install requirements. Please install them manually:")
        print(f"    {sys.executable} -m pip install -r {REQ_FILE}")
        return False


def ensure_pygame():
    try:
        import pygame  # noqa: F401
        return True
    except ImportError:
        ok = install_requirements()
        if not ok:
            return False
        try:
            import pygame  # noqa: F401
            return True
        except ImportError:
            print("Pygame still not available after attempting install.")
            return False


def main():
    # Try to ensure pygame is installed
    ok = ensure_pygame()
    if not ok:
        input("Press Enter to open README and see manual install instructions...")
        # Attempt to open README in the default editor/viewer
        readme = "README.md"
        if os.path.exists(readme):
            if sys.platform.startswith("win"):
                os.startfile(readme)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", readme])
            else:
                subprocess.Popen(["xdg-open", readme])
        return

    # Import the game module and run it
    try:
        game_mod = importlib.import_module("visual_game")
        if hasattr(game_mod, "main"):
            game_mod.main()
        else:
            # fallback: run as a script
            subprocess.check_call([sys.executable, "visual_game.py"])
    except Exception as e:
        print("Failed to start the game:", e)
        raise


if __name__ == "__main__":
    main()
