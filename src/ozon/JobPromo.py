import time

from datetime import datetime

from settings import NAME_SERVER
from src.ozon.job_article import JobArticle
from src.ozon.job_cabinet import JobCabinet
from src.ozon.job_documents import JobDocuments
from src.ozon.job_get_result import GetGetResult
from src.ozon.job_region import JobRegion
from src.ozon.job_request_search import JobRequestsSearch
from src.ozon.start_ozon import StartOzon
from src.telegram_debug import SendlerOneCreate


class JobPromo:
    def __init__(self, driver, data_pars_dict, google_core, dir_project):
        self.driver = driver
        self.google_core = google_core
        self.data_pars_dict = data_pars_dict
        self.old_files_name = []
        self.core_ozon = StartOzon(self.driver)
        self.dir_project = dir_project
        self.cabinet_core = JobCabinet(self.driver)

    def change_cabinet(self, cabinet_name):

        valid_cabinet_name = self.cabinet_core.check_name_cabinet(cabinet_name)

        if not valid_cabinet_name:
            print(f'Переключаю кабинет на {cabinet_name}')
            res_change_cabinet = self.cabinet_core.start_job_cabinet(cabinet_name)

            if not res_change_cabinet:
                print(f'Не смог включить {cabinet_name} кабинет')
                return False

        return True

    def job_document(self, request, list_id, good_range_date, cabinet_name):

        if list_id == []:
            return False

        good_id = JobDocuments(self.driver, self.google_core, list_id, request, self.core_ozon,
                               self.dir_project, good_range_date).start_documents(cabinet_name)

        if good_id == []:
            return ['null']

        return good_id

    def check_position(self, request, article):
        res_load_ozon = self.core_ozon.start_load_ozon()

        self.core_ozon.click_get_search()

        input_data_list = self.core_ozon.get_input_list()

        if not input_data_list:
            print(f'Не могу определить поля для заполнения в ozon')
            return False

        res_job_article = JobArticle(self.driver, self.core_ozon).start_job_article(article, input_data_list[2])

        if not res_job_article:
            return False

        res_job_region = JobRegion(self.driver).start_job_region(input_data_list[1], 'Москва')

        res_insert_requests = JobRequestsSearch(self.driver).start_job_search(input_data_list[0], request)

        res_finish_click_but = self.core_ozon.finish_button_search()

        res_good_res = self.core_ozon.check_load_good(f"//tbody//tr[contains(@class, 'row')]//td")

        result = GetGetResult(self.driver).start_job_get_result()

        if not result:
            return False

        return result

    def formated_value(self, value):
        try:
            value = value.strip()
        except:
            value = value

        try:
            value = value.replace('\t', '')
        except:
            value = value

        try:
            value = value.replace('\n', '')
        except:
            value = value

        return value

    def iter_row_in_sheet(self, rows_list, good_range_date, cabinet_name):

        stop_request = []

        stop_id = []

        # Захожу первый раз на Ozon
        res_load_ozon = self.core_ozon.start_load_ozon()

        if not res_load_ozon:
            return False

        count = 0
        count_try = 3

        while True:

            count += 1

            if count > count_try:
                return False

            # Переключаю кабинет
            res_ozon = self.change_cabinet(cabinet_name)

            if not res_ozon:
                continue

            break

        # TODO итерация строчек из таблицы
        for count_, row in enumerate(rows_list):

            _request, _, name, _, article, _id = row

            if _request == '' or article == '':
                print(f'! У "{name}" пустое значение пропускаю "{article}" "{_request}"')
                continue

            request = self.formated_value(_request)

            article = self.formated_value(article)

            _id = self.formated_value(_id)

            if request not in stop_request:

                list_id_by_request = {x[-1]: _count for _count, x in enumerate(rows_list) if x[0] == _request}

                print(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Начинаю загружать файл для запроса "{request}" '
                    f'с ID: {list_id_by_request}')

                count = 0
                count_try = 3

                while True:

                    count += 1

                    if count > count_try:
                        print(f'Прекратил попытки работы с файлами')
                        break

                    good_id = self.job_document(request, list_id_by_request, good_range_date, cabinet_name)

                    if not good_id:
                        print(f'Пробую ещё раз работу с файлом')
                        continue

                    stop_id.extend(good_id)

                    break

            stop_request.append(request)

            if f"{_id}_{request}" in stop_id:
                continue

            if article in stop_id:
                continue

            print(f'ID: {_id} с запросом "{request}" нет в файлах Exel. Получаю его место в поиске дополнительно')

            count = 0
            count_try = 3

            while True:

                count += 1

                if count > count_try:
                    break

                position = self.check_position(request, article)

                if not position:
                    continue

                break

            stop_request.append(article)

            res_write_position = self.google_core.write_position_no_document(good_range_date, cabinet_name,
                                                                             count_, position)

        return True

    def iter_sheets(self):
        # TODO итерация страниц из google
        for cabinet_name, job in self.data_pars_dict.items():
            good_range_date = job['good_range_date']

            job = job['list_data_job']

            res_iter_rows = self.iter_row_in_sheet(job, good_range_date, cabinet_name)

            if not res_iter_rows:
                continue

            print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Закончил обработку {cabinet_name}\n')

        print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Обработал все кабинеты\n')

        return True

    def start_promo(self):

        res_iter = self.iter_sheets()

        return True
