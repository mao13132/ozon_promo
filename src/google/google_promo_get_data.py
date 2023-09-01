import time
from datetime import datetime

from settings import NAME_SHEET, ID_SHEET, NAME_SERVER
from src.google.google_alternative import ConnectGoogleAlternative
from src.google.google_get_name_colums import GoogleGetNameColums
from src.telegram_debug import SendlerOneCreate


class GooglePromoGetData:
    def __init__(self):
        self.count_load_rows = 100000


    @staticmethod
    def search_index_columns(list_name_columns):
        ip_list_index = []

        _temp_ip = {}

        for count, colm in enumerate(list_name_columns):

            if 'запрос' in colm.value.lower():
                _temp_ip['request_inx'] = colm.address

            if 'артикул' in colm.value.lower():
                _temp_ip['article_inx'] = colm.address

            if 'id' in colm.value.lower():
                _temp_ip['id'] = colm.address

                ip_list_index.append(_temp_ip)

        return ip_list_index

    def reviews_get_data(self):

        google_alternate = ConnectGoogleAlternative()

        if NAME_SHEET == []:
            names_list_sheet = google_alternate.get_name_sheets()
        else:
            names_list_sheet = NAME_SHEET

        _temp = {}

        for name_sheet in names_list_sheet:
            _temp[name_sheet] = {}

            # TODO работа по получению индексов столбцов дат===============================

            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                  f'Высчитываю данные для группировки колонок на {name_sheet}')

            try:
                range_date_list = google_alternate.get_range_date_columns(name_sheet, 'AZ1:ZZ1')
            except:
                print(f'Ошибка при получение данных с вкладки {name_sheet}')
                continue

            time.sleep(1)

            if range_date_list == []:
                print(f'Не найдены данные на {name_sheet}')
                continue

            dict_range_date = google_alternate.calculation_range_date(range_date_list)

            time.sleep(1)

            good_range_date = google_alternate.calculation_last_date(dict_range_date, name_sheet)

            time.sleep(1)

            _temp[name_sheet]['good_range_date'] = good_range_date

            try:
                res_group = google_alternate.clear_hide_group_and_create_new_group(good_range_date, name_sheet)
            except Exception as es:
                msg = f'{NAME_SERVER} Ошибка при создание группы в на странице {name_sheet} ошибка: "{es}"'

                print(msg)

                SendlerOneCreate('').save_text(msg)

            # TODO работа по получению индексов столбцов дат===============================

            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                  f'Получаю данные для построения отчёта эффективности с вкладки {name_sheet}')

            range_date_list = google_alternate.get_range_date_columns(name_sheet, 'A2:BP2')

            time.sleep(1)

            if range_date_list == []:
                continue

            name_index_list = self.search_index_columns(range_date_list)

            if name_index_list == []:
                print(f'На вкладке {name_sheet} не обнаружены столбцы с данными')
                continue

            start_data_columns = f"{name_index_list[0]['request_inx'][:-1]}3"

            over_data_columns = f"{name_index_list[0]['id'][:-1]}{self.count_load_rows}"

            list_data_job = google_alternate.get_data_by_range(start_data_columns, over_data_columns, name_sheet)

            _temp[name_sheet]['list_data_job'] = list_data_job

            time.sleep(5)

        return _temp
