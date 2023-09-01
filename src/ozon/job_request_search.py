import time

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys


class JobRequestsSearch:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'Ozon'

    def insert_quiest_search(self, row, request):
        try:
            row.find_element(by=By.XPATH,
                             value=f".//input").send_keys(request)
        except:
            return False

        return True

    def get_value_search(self, row):
        try:
            _value = row.find_element(by=By.XPATH,
                                      value=f".//input").get_attribute('value')
        except:
            return ''

        return _value

    def get_len_value(self, row):
        try:
            _res = row.find_element(by=By.XPATH,
                                    value=f".//input").get_attribute('value')
        except:
            return 0
        try:
            _res = len(_res)
        except:
            return 0

        return _res

    def loop_clear(self, row, count):
        for x in range(count):
            try:
                row.find_element(by=By.XPATH,
                                 value=f".//input").send_keys(Keys.BACKSPACE)
            except:
                continue

        return True

    def send_enter(self, row):
        try:
            row.find_element(by=By.XPATH,
                             value=f".//input").send_keys(Keys.ENTER)
        except:
            return False

        return True

    def loop_job_search(self, row, request):
        try:
            request = request.strip()
        except:
            request = request

        count = 0
        count_try = 5
        while True:
            count += 1
            if count > count_try:
                print(f'Не смог вставить поисковый запрос')
                return False

            _request = self.get_value_search(row)

            if _request != request:

                get_len = self.get_len_value(row)

                if get_len > 0:
                    self.loop_clear(row, get_len)

                res_insert_req = self.insert_quiest_search(row, request)

                if count > 1:
                    time.sleep(1)

                continue

            return True

    def check_scroll(self, ):
        try:
            res = self.driver.find_element(by=By.XPATH,
                                           value=f"//*[contains(@class, 'dropdown-wrapper-module')]")
        except:
            return False

        return True

    def loop_close_conteiner(self, row):
        count = 0
        count_try = 5
        while True:
            count += 1
            if count > count_try:
                print(f'Не могу закрыть окно с подсказками запросов')
                return False

            res_check_scroll = self.check_scroll()
            if res_check_scroll:
                self.send_enter(row)
                if count > 1:
                    time.sleep(1)
                continue

            return True

    def start_job_search(self, row, request):
        try:
            request = request.strip()
        except:
            request = request

        res_ = self.loop_job_search(row, request)

        if not res_:
            return False

        res_close_scroll = self.loop_close_conteiner(row)

        return True
