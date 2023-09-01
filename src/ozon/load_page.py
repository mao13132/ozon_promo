import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoadPage:
    def __init__(self, driver, url):
        self.url = url
        self.driver = driver
        self.source_name = 'Ozon'

    def load_page(self, url):
        try:
            self.driver.get(url)
            return True
        except:
            return False

    def __check_load_page(self, _xpatch):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, _xpatch)))
            return True
        except:
            return False

    def check_2(self):

        try:
            inputs_ = self.driver.find_elements(by=By.XPATH,
                                                value=f"//div[contains(@class, 'input-module_input_')]")
        except:
            return False

        try:
            _value = inputs_[0].find_element(by=By.XPATH,
                                          value=f".//input").get_attribute('value')
        except:
            return False

        return True

    def loop_load_page(self, _xpatch):
        count = 0
        count_ower = 10

        self.driver.set_page_load_timeout(15)

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(self.url)

            if not start_page:
                time.sleep(5)
                continue

            check_page = self.__check_load_page(_xpatch)

            if not check_page:
                self.driver.refresh()
                continue

            # print(f'Успешно зашёл на {self.url[:45]}')

            return True
    def loop_load_page_doc(self, _xpatch):
        count = 0
        count_ower = 10

        self.driver.set_page_load_timeout(15)

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(self.url)

            if not start_page:
                time.sleep(5)
                continue

            check_page = self.__check_load_page(_xpatch)

            if not check_page:
                self.driver.refresh()
                continue

            check2 = self.check_2()

            if not check2:
                continue

            # print(f'Успешно зашёл на {self.url[:45]}')

            return True
