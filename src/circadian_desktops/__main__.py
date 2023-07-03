"""
To run circadian_desktops library module as a script, execute:
python -m circadian_desktops
"""

import sys


def main():
    if __package__ == "circadian_desktops":
        from circadian_desktops.app import run_app

        run_app()
    else:
        print("Use Python's -m flag to run library module as a script")


main()
