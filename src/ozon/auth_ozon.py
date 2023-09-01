import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import PHONE, NAME_SERVER


class AuthOzon:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'Ozon'

    def write_phone(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@type, 'tel')]").send_keys(PHONE)
        except Exception as es:
            print(f'Не смог ввести логин "{es}"')
            return False

        return True

    def click_login(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'page-anon')]//button").click()
        except Exception as es:
            print(f'Не смог авторизоваться click_login "{es}"')
            return False

        return True

    def check_load_page(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(@type, 'tel')]")))
            return True
        except:
            return False

    def click_signin(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'signin')]"
                                           f"//button[contains(@class, 'signin')]").click()
        except:
            return False

        return True

    def loop_wait_user(self):
        count = 0
        count_try = 200

        while True:
            count += 1
            if count > count_try:
                print(f'Не дождался пользователя, не смог авторизоваться')
                return False

            time.sleep(180)

            # try:
            #     self.driver.find_element(by=By.XPATH, value=f"//div[contains(@class, 'moduleRoot')]")
            #     return True
            # except:
            #     time.sleep(60)
            #     continue

    def start_auth(self):
        self.click_signin()

        check_load = self.check_load_page()

        if not check_load:
            return False

        # res_write_login = self.write_phone()
        #
        # if not res_write_login:
        #     return False

        # res_click = self.click_login()

        msg = (f'Разлогин на {NAME_SERVER} Ввёл данные авторизации жду ввода данных от пользователя')

        print(msg)

        from src.telegram_debug import SendlerOneCreate
        SendlerOneCreate('').save_text(msg)

        res_auth_user = self.loop_wait_user()

        return res_auth_user

    def check_auth(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//div[contains(@class, 'registration')]")

        except:

            return False

        return True

    def loop_auth(self):
        res_auth = self.check_auth()

        if res_auth:
            print(f'Необходима авторизация')
            res_auth = self.start_auth()

            return res_auth

        return True
