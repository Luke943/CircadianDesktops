import ctypes
import datetime
import os
import random
import sys
import winreg

from astral import LocationInfo, sun
import geocoder

appname = 'CircadianDesktops'


def get_times():
    """Get sunrise/sunset times for default values in app"""
    try:
        mylocation = geocoder.ip('me')
        mylatlng = mylocation.latlng
        mytimezone = mylocation.json['raw']['timezone']
        loc = LocationInfo(latitude=mylatlng[0], longitude=mylatlng[1])
        s = sun.sun(loc.observer, datetime.datetime.now(), tzinfo=mytimezone)

        # adjustment to widen dawn/dusk window (quite short by default)
        adjustment = datetime.timedelta(minutes=20)
        times = {'dawn': (s['dawn'] - adjustment).time(),
                 'sunrise': (s['sunrise'] + adjustment).time(),
                 'sunset': (s['sunset'] - adjustment).time(),
                 'dusk': (s['dusk'] + adjustment).time()}

    except:
        """For when no connection"""
        times = {'dawn': datetime.time(hour=5),
                 'sunrise': datetime.time(hour=7),
                 'sunset': datetime.time(hour=17),
                 'dusk': datetime.time(hour=19)}

    return times


def get_settings(filePath: str):
    """Read settings file or create one when none exits"""
    s = dict()

    try:
        with open(filePath, 'r') as f:
            lines = f.read().split('\n')
        for line in lines:
            try:
                key, value = line.split('\t')
                try:
                    s[key] = int(value)
                except:
                    s[key] = value
            except:
                pass

    except:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\Desktop') as key:
            imgPath = winreg.QueryValueEx(key, 'WallPaper')[0]
        s['labelDayImg'] = imgPath
        s['labelDDImg'] = imgPath
        s['labelNightImg'] = imgPath
        s['isDarkMode'] = 0
        s['runOnStartup'] = 0
        s['isCustomTimes'] = 0
        s['minimizeToTray'] = 1
        s['isSlideshow'] = 0
        s['shuffleTime'] = 30

    return s


def write_settings(filePath: str, settings: dict):
    with open(filePath, 'w') as f:
        for key, value in settings.items():
            f.write(f'{key}\t{value}\n')


def random_image(fullPath: str):
    folderPath = os.path.dirname(fullPath)  # Allows input to be file or folder
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
    images = [f for f in os.listdir(folderPath) if any(
        f.endswith(s) for s in image_extensions)]
    if images:
        return os.path.join(folderPath, random.choice(images))
    else:
        return ''


def set_desktop(imagePath: str):
    # SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 0)


def run_on_startup(isRunOnStartup: bool):
    """Write to or delete from registry"""
    sub_key = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
    if isRunOnStartup:
        if hasattr(sys, "frozen"):
            regString = f'"{os.path.abspath(os.path.basename(sys.executable))}" /noshow'
        else:
            # Use of os.path.basename accounts for having cd'd into __main__ directory
            mainAbsPath = os.path.abspath(
                os.path.basename(sys.modules['__main__'].__file__))
            regString = f'"{sys.executable}" "{mainAbsPath}" /noshow'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, appname, 0, winreg.REG_SZ, regString)
    else:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key, 0, winreg.KEY_WRITE) as key:
            winreg.DeleteValue(key, appname)


def explicit_app():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appname)