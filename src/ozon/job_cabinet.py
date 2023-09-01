import time
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from src.ozon.auth_ozon import AuthOzon
from src.ozon.load_page import LoadPage


class JobCabinet:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'Ozon'

    def get_name_cabinet(self):
        try:
            _name = self.driver.find_element(by=By.XPATH,
                                             value=f"//div[contains(@class, 'index_controls')]"
                                                   f"//*[contains(@class, 'companyName')]").text
        except:
            return False

        return _name

    def click_in_cabinet(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//div[contains(@class, 'index_controls')]"
                                           f"//*[contains(@class, 'companyName')]").click()
        except:
            return False

        return True

    def check_open_popup_cabinet(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//div[contains(@class, 'dropdown-wrapper')]")
        except:
            return False

        return True

    def open_change_menu(self):
        count = 0
        count_try = 10
        while True:
            count += 1
            if count > count_try:
                print(f'Не смог переключить открыть меню для смены кабинета')
                return False

            res_click = self.click_in_cabinet()

            status_popup = self.check_open_popup_cabinet

            if not status_popup:
                if count > 1:
                    time.sleep(1)
                continue

            return True

    def get_el_cabinet_name(self, name_cabinet):
        try:
            el = self.driver.find_element(by=By.XPATH,
                                          value=f"//div[contains(@class, 'dataCell')]"
                                                f"//*[contains(text(), '{name_cabinet}')]")
        except:
            try:
                el = self.driver.find_element(by=By.XPATH,
                                              value=f"//div[contains(@class, 'dataCell')]"
                                                    f"//*[contains(text(), '{name_cabinet.lower()}')]")
            except:
                return False

        return el

    def navigat_to_elem_cabinet(self, elem):
        try:
            ActionChains(self.driver).move_to_element(elem).perform()
        except:
            return False

        return True

    def click_to_elem_cabinet(self, elem):
        try:
            elem.click()
        except:
            return False

        return True

    def insert_cabinet(self, name_cabinet):
        if name_cabinet == "S'pets":
            name_cabinet = 'pets'

        el_cabinet = self.get_el_cabinet_name(name_cabinet)

        if not el_cabinet:
            return False

        time.sleep(1)

        res_navigator = self.navigat_to_elem_cabinet(el_cabinet)

        if not res_navigator:
            return False

        time.sleep(1)

        res_click_cabinet = self.click_to_elem_cabinet(el_cabinet)

        if not res_click_cabinet:
            return False

        return True

    def change_cabinet(self, name_cabinet):
        open_popup = self.open_change_menu()

        if not open_popup:
            return False

        res_insert_cabinet_name = self.insert_cabinet(name_cabinet)

        return res_insert_cabinet_name

    def loop_change_cabinet(self, name_cabinet):
        count = 0
        count_try = 10
        while True:
            count += 1
            if count > count_try:
                print(f'Не смог переключить кабинет на {name_cabinet}')
                return False

            _name_cabinet = self.get_name_cabinet()

            if _name_cabinet.lower() != name_cabinet.lower():
                res_change = self.change_cabinet(name_cabinet)

                if not res_change:
                    return False

                if count > 1:
                    time.sleep(1)

                continue

            return True

    def start_job_cabinet(self, name_cabinet):
        res_change = self.loop_change_cabinet(name_cabinet)

        return res_change

    def check_name_cabinet(self, name_cabinet):
        _name_cabinet = self.get_name_cabinet()

        if _name_cabinet != name_cabinet:
            return False

        return True
