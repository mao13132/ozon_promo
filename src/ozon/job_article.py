import time
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.ozon.auth_ozon import AuthOzon
from src.ozon.load_page import LoadPage


class JobArticle:
    def __init__(self, driver, ozon_core):
        self.driver = driver
        self.source_name = 'Ozon'
        self.ozon_core = ozon_core

    def start_job_article(self, article, row):
        # вызываю окно с выбором товара для вставки артикула
        res_popup = self.ozon_core.loop_open_popup_products(row)

        time.sleep(1)

        res_reset = self.ozon_core.reset_article()

        try:
            article = article.strip()
        except:
            article = article

        res_insert_article = self.ozon_core.loop_insert_article(article)

        time.sleep(2)

        rows_products = self.ozon_core.get_rows_products()

        if rows_products == []:
            return False

        res_select_products = self.ozon_core.iter_rows_salle(rows_products)

        if not res_select_products:
            print(f'Не смог выбрать/найти артикл {article}')
            return False

        res_click_add_products = self.ozon_core.click_add_product()

        if not res_click_add_products:
            print(f'Не смог закрыть окна выбора продукта {article}')
            return False

        check_close_popup = self.ozon_core.loop_close_popup_products()

        return check_close_popup
