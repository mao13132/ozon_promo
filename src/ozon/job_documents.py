import time

from settings import NAME_SERVER
from src.ozon._check_dir import get_all_name_file
from src.ozon.job_cabinet import JobCabinet
from src.ozon.job_region import JobRegion
from src.ozon.job_request_search import JobRequestsSearch
from src.ozon.start_ozon import StartOzon
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class JobDocuments:
    def __init__(self, driver, google_core, list_id, request, core_ozon, dir_project):
        self.driver = driver
        self.google_core = google_core
        self.list_id = list_id
        self.request = request
        self.core_ozon = core_ozon
        self.old_files_name = []
        self.dir_project = dir_project

    def check_start_download(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//button[contains(@class, 'button-module_clear')]")
        except:
            return True

        return False

    def loop_wait_start_download(self):
        count = 0
        count_try = 8

        while True:
            count += 1
            if count > count_try:
                print(f'Не дождался начала скачивания файла')
                return False

            res_start = self.check_start_download()

            if not res_start:
                if count > 1:
                    time.sleep(2)
                continue

            return True

    def click_result_button(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Показать результат')]").click()
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

    def download_button(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Скачать отчёт')]").click()
        except:
            return False

        return True

    def check_load_page(self, _xpatch):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, _xpatch)))
            return True
        except:
            return False

    def end_download(self, driver):
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")
        return driver.execute_script("""
            var items = document.querySelector('downloads-manager')
                .shadowRoot.getElementById('downloadsList').items;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.fileUrl || e.file_url);
            """)

    def get_file_name_down(self):
        new_file_name = ''

        list_name = get_all_name_file(self.dir_project)

        for name in list_name:
            if name == '':
                continue

            if name in self.old_files_name:
                continue

            new_file_name = name

            self.old_files_name.append(name)

        if new_file_name == '':
            print()

        return new_file_name

    def job_one_cabinet(self):

        good_result_list = []

        print(f'Всего ключевых слов {len(self.list_id)}')

        for row, count_row in self.list_id.items():

            res_load_ozon = self.core_ozon.load_ozon_bussines()

            if not res_load_ozon:
                print(f'{NAME_SERVER} Не смог открыть странницу с загрузкой exel файлов')
                return False

            input_data_list = self.get_input_list()

            if not input_data_list:
                print(f'Не могу определить поля для заполнения в ozon')
                continue

            res_insert_requests = JobRequestsSearch(self.driver).start_job_search(input_data_list[0], self.request)

            res_job_region = JobRegion(self.driver).start_job_region(input_data_list[1], 'Москва')

            res_finish_click_but = self.click_result_button()

            res_load_page = self.check_load_page(f'//*[contains(text(), "Скачать отчёт")]')

            if not res_load_page:
                print(f'Не смог загрузить данные для скачивания')
                continue

            res_click_download = self.download_button()

            res_start_download = self.loop_wait_start_download()

            time.sleep(1)

            res_end_dowload = WebDriverWait(self.driver, 20, 1).until(self.end_download)

            file_name = self.get_file_name_down()

            if file_name == '':
                continue

            # job_write_document = JobInsertFilesData(good_result_list, self.google_core).start_iter_files(
            #     cursor_end, self.good_write_count)

        return good_result_list

    def count_my_products(self):

        good_list = {}

        for row in self.list_id:
            try:
                good_list[row['request']] += 1
            except:
                good_list[row['request']] = 1

        return good_list

    def get_formated_cabinet_keyboards(self):

        good_list = []

        stop_list = []

        count_my_products = self.count_my_products()

        # TODO посчитать сколько товаров по каждому ключевику

        for row in self.list_id:

            if row['request'] == '':
                continue

            stop_string = f"{row['name_sheet']}|{row['request']}"

            if stop_string in stop_list:
                continue

            stop_list.append(stop_string)

            _temp_dict = {}

            _temp_dict['name_sheet'] = row['name_sheet']
            _temp_dict['request'] = row['request']
            _temp_dict['my_products'] = count_my_products[row['request']]

            good_list.append(_temp_dict)

        # return return_list
        return good_list

    def start_documents(self):

        data_files_sheet = self.job_one_cabinet()

        print(f'Закончил скачивание файлов')

        return data_files_sheet
