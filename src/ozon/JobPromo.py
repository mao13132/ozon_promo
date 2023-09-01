import time

from datetime import datetime

from settings import NAME_SERVER
from src.ozon.job_cabinet import JobCabinet
from src.ozon.job_documents import JobDocuments
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

        return good_id

    def iter_row_in_sheet(self, rows_list, good_range_date, cabinet_name):

        stop_request = []

        stop_id = []

        # Захожу первый раз на Ozon
        res_load_ozon = self.core_ozon.start_load_ozon()

        if not res_load_ozon:
            return False

        # Переключаю кабинет
        res_ozon = self.change_cabinet(cabinet_name)

        if not res_ozon:
            return False

        # TODO итерация строчек из таблицы
        for count, row in enumerate(rows_list):

            request, _, name, _, article, _id = row

            if request not in stop_request:
                list_id_by_request = {x[-1]: _count for _count, x in enumerate(rows_list) if x[0] == request}

                good_id = self.job_document(request, list_id_by_request, good_range_date, cabinet_name)

                if not good_id:
                    continue

                stop_id.extend(good_id)

                print()

            stop_request.append(request)

            if _id in stop_id:
                continue

            self.core_ozon.click_get_search()

            print(row)

    def iter_sheets(self):
        # TODO итерация страниц из google
        for cabinet_name, job in self.data_pars_dict.items():
            good_range_date = job['good_range_date']

            job = job['list_data_job']

            res_iter_rows = self.iter_row_in_sheet(job, good_range_date, cabinet_name)

            if not res_iter_rows:
                continue

            print()

    def start_promo(self):
        res_iter = self.iter_sheets()

        print()
