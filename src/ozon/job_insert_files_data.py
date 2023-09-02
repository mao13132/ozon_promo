import time
from datetime import datetime

import openpyxl

from settings import ID_SHEET
from src.ozon._check_dir import clear_folder


class JobInsertFilesData:
    def __init__(self, job_list, google_core, good_range_date, dir_project, request):
        self.job_list = job_list
        self.google_core = google_core
        self.good_range_date = good_range_date
        self.dir_project = dir_project
        self.request = request

    def load_exel_file(self, file):
        try:
            load_file = openpyxl.load_workbook(file)
        except:
            return False

        load_file = load_file.active

        return load_file

    def get_rows_exel(self, load_file):
        good_row_list = []

        for row in load_file.iter_rows(min_col=0, max_col=20, min_row=1, max_row=300, values_only=True):
            if row[0] is None:
                continue
            good_row_list.append(row)

        return good_row_list

    def iter_file_exel(self, rows_exel, cabinet_name):

        good_id = []

        for row in rows_exel[10:]:

            position, _id, _, _, rez_ocenka, _, _, _, _, _, price, _, \
                delivery, popular_request, trade_product, popular_total, *_ = row

            try:
                count_google_row = self.job_list[str(_id)]
            except:
                continue

            print(f'- Записываю значения для ID: {_id}')

            res_write = self.google_core.write_data_from_exel_file(self.good_range_date, cabinet_name, count_google_row,
                                                                   position, rez_ocenka, popular_request, trade_product,
                                                                   popular_total)

            good_id.append(f'{_id}_{self.request}')

        return good_id

    def start_iter_files(self, file_name, cabinet_name):

        res_load = self.load_exel_file(file_name)

        if not res_load:
            print(f'Не смог загрузить файл екселя')
            return False

        clear_folder(self.dir_project)

        rows_exel = self.get_rows_exel(res_load)

        if rows_exel == []:
            print(f'Нет строчек в файле exel')
            return False

        good_id = self.iter_file_exel(rows_exel, cabinet_name)

        return good_id
