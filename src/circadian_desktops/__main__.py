"""
To run circadian_desktops library module as a script:
python -m circadian_desktops
Alternatively, run:
python C:\\path\\to\\folder\\circadian_desktops
"""

import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
if "/noshow" in sys.argv:
    subprocess.Popen([sys.executable, "app.pyw", "/noshow"])
else:
    subprocess.Popen([sys.executable, "app.pyw"])
sys.exit(0)
