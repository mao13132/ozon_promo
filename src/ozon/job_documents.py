import time

from settings import NAME_SERVER
from src.ozon._check_dir import get_all_name_file
from src.ozon.job_insert_files_data import JobInsertFilesData
from src.ozon.job_region import JobRegion
from src.ozon.job_request_search import JobRequestsSearch
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class JobDocuments:
    def __init__(self, driver, google_core, list_id, request, core_ozon, dir_project, good_range_date):
        self.driver = driver
        self.google_core = google_core
        self.list_id = list_id
        self.request = request
        self.core_ozon = core_ozon
        self.old_files_name = []
        self.dir_project = dir_project
        self.good_range_date = good_range_date

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

    def download_file_by_request(self):

        print(f'Всего ключевых слов {len(self.list_id)}')

        res_load_ozon = self.core_ozon.load_ozon_bussines()

        if not res_load_ozon:
            print(f'{NAME_SERVER} Не смог открыть странницу с загрузкой exel файлов')
            return False

        input_data_list = self.get_input_list()

        if not input_data_list:
            print(f'Не могу определить поля для заполнения в ozon')
            return False

        res_insert_requests = JobRequestsSearch(self.driver).start_job_search(input_data_list[0], self.request)

        res_job_region = JobRegion(self.driver).start_job_region(input_data_list[1], 'Москва')

        res_finish_click_but = self.click_result_button()

        res_load_page = self.check_load_page(f'//*[contains(text(), "Скачать отчёт")]')

        if not res_load_page:
            print(f'Не смог загрузить данные для скачивания')
            return False

        res_click_download = self.download_button()

        res_start_download = self.loop_wait_start_download()

        time.sleep(1)

        res_end_download = WebDriverWait(self.driver, 20, 1).until(self.end_download)

        file_name = self.get_file_name_down()

        if file_name == '':
            print(f'Нет файла exel надо ответить или ещё раз скачать')
            return False

        return file_name

    def count_my_products(self):

        good_list = {}

        for row in self.list_id:
            try:
                good_list[row['request']] += 1
            except:
                good_list[row['request']] = 1

        return good_list

    def start_documents(self, cabinet_name):

        file_name = self.download_file_by_request()

        if not file_name:
            return False

        good_id = JobInsertFilesData(self.list_id, self.google_core, self.good_range_date)\
            .start_iter_files(file_name, cabinet_name)

        print(f'Закончил обработку ID в файлах и их запись')

        return good_id
