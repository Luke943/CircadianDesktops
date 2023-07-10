"""
To run circadian_desktops library module as a script, execute:
pythonw -m circadian_desktops
Alternatively, execute:
pythonw C:\\path\\to\\folder\\circadian_desktops
"""

import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "app.py"])
sys.exit(0)
