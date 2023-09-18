"""
Remove registry entry and settings file for circadian_desktops.
These would not be removed by a pip uninstall.
"""

if __name__ == "__main__":
    import os

    from circadian_desktops.functions import run_on_startup
    from circadian_desktops.app import SETTINGS_FILE

    run_on_startup(False)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.remove(SETTINGS_FILE)
