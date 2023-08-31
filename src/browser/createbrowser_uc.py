import os
import platform

import undetected_chromedriver as uc

import getpass

from settings import NAME_PROFILE


class CreatBrowser:

    def create_dir(self):
        from pathlib import Path
        _dirs_project = Path(f"{os.getcwd()}\download")

        dir_s = 'C:\\'
        for x in _dirs_project.parts[1:]:
            dir_s += f"{x}\\"

        return dir_s

    def __init__(self):

        platform_to_os = platform.system()

        if platform_to_os == "Linux":
            from xvfbwrapper import Xvfb
            vdisplay = Xvfb(width=1280, height=720)
            vdisplay.start()

        platform_to_os = platform.system()
        options = uc.ChromeOptions()
        options.add_argument("start-maximized")

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('ignore-certificate-errors')
        options.add_argument("--log-level=3")
        user_system = getpass.getuser()
        name_profile = NAME_PROFILE

        if platform_to_os == "Linux":
            path_dir = (f'/Users/{user_system}/Library/Application Support/Google/Chrome/{name_profile}')
        else:
            path_dir = (f'C:\\Users\\{user_system}\\AppData\\Local\\Google\\Chrome\\User Data\\{name_profile}')

        options.add_argument(f'--user-data-dir={path_dir}')

        options.add_argument(f'--proxy-server = {None}')

        options.add_argument(
            f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/114.0.0.0 Safari/537.36")

        _dirs = self.create_dir()
        prefs = {"download.default_directory": _dirs}
        options.add_experimental_option("prefs", prefs)

        try:
            self.driver = uc.Chrome(options=options)

        except Exception as es:
            print(f'Ошибка создания браузера {es}')
            return False

        try:
            browser_version = self.driver.capabilities['browserVersion']
            driver_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
            print(f"Браузер: {browser_version} драйвер: {driver_version}")
        except:
            print(f'Не получилось определить версию uc браузера')
