import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.ozon.auth_ozon import AuthOzon

from src.ozon.load_page import LoadPage


class StartOzon():
    def __init__(self, driver):
        self.driver = driver
        self.links_post = []
        self.source_name = 'Ozon'

    def formated_price(self, value):
        _price = ''

        try:

            for x in value:
                if x.isdigit():
                    _price += x

            _price = int(_price)
        except:
            _price = value

        return _price

    def _click_get_search(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Где товар в поиске')]").click()
        except:
            return False

        return True

    def check_search_position(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Сохранить запрос')]")
        except:
            return False

        return True

    def check_load_good(self, _xpatch):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, _xpatch)))
            return True
        except:
            return False

    def finish_button_search(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Показать результаты')]").click()
        except:
            return False

        return True

    def get_input_list(self):
        try:
            inputs_ = self.driver.find_elements(by=By.XPATH,
                                                value=f"//div[contains(@class, 'input-module_input_')]")
        except:
            return False

        return inputs_

    def get_rows_products(self):
        try:
            rows = self.driver.find_elements(by=By.XPATH,
                                             value=f"//div[contains(@class, 'busyBox')]"
                                                   f"//*[contains(@class, 'resultRow')]")
        except:
            return []

        return rows

    def iter_rows_salle(self, rows_list):
        for row in rows_list:
            try:
                res = row.find_element(by=By.XPATH, value=f".//div[contains(@class, 'productStoreType')]").text
            except:
                continue

            if 'Продается' in res:
                try:
                    row.find_element(by=By.XPATH, value=f".//*[contains(@type, 'checkbox')]").click()
                except:
                    continue

                return True

        return False

    def insert_article(self, article):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//div[contains(@class, 'horizontalLayou')]"
                                           f"//*[contains(@class, 'inputContainer')]//input").send_keys(article)
        except:
            return False

        return True

    def click_add_product(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//div[contains(@class, 'module_window')]"
                                           f"//*[contains(text(), 'Добавить')]").click()
        except:
            return False

        return True

    def reset_article(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Сбросить')]").click()
        except:
            return False

        return True

    def check_insert_article(self):
        try:
            site_article = self.driver.find_element(by=By.XPATH,
                                                    value=f"//div[contains(@class, 'horizontalLayou')]"
                                                          f"//*[contains(@class, 'inputContainer')]"
                                                          f"//input").get_attribute('value')
        except:
            return ''
        return site_article

    def loop_insert_article(self, article):
        count = 0
        count_try = 2
        while True:
            count += 1
            if count > count_try:
                print(f'Не могу вставить артикул')
                return False

            site_article = self.check_insert_article()

            if article != site_article:
                self.insert_article(article)
                if count > 2:
                    time.sleep(1)
                continue

            return True

    def get_popup_products(self, row):
        try:
            row.find_element(by=By.XPATH,
                             value=f".//*[contains(@class, 'rightContent')]").click()
        except:
            return False

        return True

    def check_popup(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//div[contains(@class, 'horizontalLayou')]")
        except:
            return False

        return True

    def loop_open_popup_products(self, row):
        count = 0
        count_try = 10
        while True:
            count += 1
            if count > count_try:
                print(f'Не смог открыть окно с выбором товара')
                return False

            res_click_popup = self.get_popup_products(row)

            res_pop_up = self.check_popup()

            if res_pop_up:
                return True

            time.sleep(1)

    def loop_close_popup_products(self):
        count = 0
        count_try = 5
        while True:
            count += 1
            if count > count_try:
                print(f'Не смог открыть окно с выбором товара')
                return False

            res_pop_up = self.check_popup()

            if not res_pop_up:
                return True

            time.sleep(1)

    def click_get_search(self):
        for count in range(5):

            res_check = self.check_search_position()

            if res_check:
                return True

            res_click = self._click_get_search()

            if not res_click:
                time.sleep(1)

        print(f'Не смог перейти в меню поиска позиций')
        return False

    def start_load_reviews_ozon(self):
        link = f'https://seller.ozon.ru/app/reviews'

        result_start_page = LoadPage(self.driver, link).loop_load_page(f"//*[contains(text(), 'Отзывы покупателей')]")

        if not result_start_page:
            return False

        res_auth = AuthOzon(self.driver).loop_auth()

        return res_auth

    def start_load_ozon(self):
        link = f'https://seller.ozon.ru/app/analytics/search-results/validator'

        result_start_page = LoadPage(self.driver, link).loop_load_page(f"//*[contains(@class, 'addedConten') or "
                                                                       f"//div[contains(@class, 'registration')]]")

        # time.sleep(1)

        if not result_start_page:
            return False

        res_auth = AuthOzon(self.driver).loop_auth()

        return res_auth

    def load_ozon_geograph(self):
        link = f'https://seller.ozon.ru/app/analytics/sales-geography/local-packaging'

        result_start_page = LoadPage(self.driver, link).loop_load_page(
            f"//*[contains(@class, 'totalLocalizationWidget')]")

        if not result_start_page:
            return False

        res_auth = AuthOzon(self.driver).loop_auth()

        return res_auth

    def load_ozon_bussines(self):
        link = f'https://seller.ozon.ru/app/analytics/search-results/explainer'

        result_start_page = LoadPage(self.driver, link).loop_load_page_doc(f"//*[contains(text(), 'Где покупатель')]")

        if not result_start_page:
            return False

        return result_start_page

    def load_ozon_cost(self):
        link = f'https://seller.ozon.ru/app/supply/warehousing-cost/all-categories'

        result_start_page = LoadPage(self.driver, link).loop_load_page(
            f"//*[contains(@class, 'topSummaryBlockContainer')]")

        if not result_start_page:
            return False

        res_auth = AuthOzon(self.driver).loop_auth()

        return res_auth
