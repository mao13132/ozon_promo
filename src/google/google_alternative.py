from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials
import gspread

from settings import ID_SHEET
from src.telegram_debug import SendlerOneCreate


class ConnectGoogleAlternative:
    def __init__(self):
        self.name_columns_1 = 'Позиция в выдаче'
        self.name_columns_2 = 'Рез.оценка'
        self.name_columns_3 = 'Популярность по запросу'
        self.name_columns_4 = 'Продажи товара'
        self.name_columns_5 = 'Популярность'

        json_keyfile = r'src/google_api_file/ozonproject-1.json'

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)

        gc = gspread.authorize(credentials)

        self.sheet = gc.open_by_key(ID_SHEET)

    def get_range_date_columns(self, name_list):
        worksheet = self.sheet.worksheet(name_list)

        list_columns = worksheet.range('AZ1:ZZ1')

        return list_columns

    def calculation_range_date(self, list_columns):

        _dict = {}

        for count, column in enumerate(list_columns):

            if self.name_columns_1 in column.value:
                _dict['column1_start'] = column.address[:-1] + '2'

            if self.name_columns_2 in column.value:
                _dict['column1_end'] = list_columns[count - 1].address[:-1] + '2'

                _dict['column2_start'] = column.address[:-1] + '2'

            if self.name_columns_3 in column.value:
                _dict['column2_end'] = list_columns[count - 1].address[:-1] + '2'

                _dict['column3_start'] = column.address[:-1] + '2'

            if self.name_columns_4 in column.value:
                _dict['column3_end'] = list_columns[count - 1].address[:-1] + '2'

                _dict['column4_start'] = column.address[:-1] + '2'

            if self.name_columns_5 in column.value and self.name_columns_3 not in column.value:
                _dict['column4_end'] = list_columns[count - 1].address[:-1] + '2'

                _dict['column5_start'] = column.address[:-1] + '2'

                _dict['column5_end'] = list_columns[count + 30].address[:-1] + '2'

        return _dict

    def get_range_(self, worksheet, start_index, end_index):
        try:
            list_call = worksheet.range(f'{start_index}:{end_index}')
        except Exception as es:
            msg = (f'Ошибка при получения ренджа для вычисления даты ({start_index} - {end_index}) "{es}"')

            print(msg)

            SendlerOneCreate('').save_text(msg)

            return []

        return list_call

    def iter_cell_find_mouth(self, range, now_day, now_month):
        list_now_mouth_day = []

        for count, cell in enumerate(range):

            date_cell = cell.value

            if cell.value == '':
                continue

            try:
                date_cell = datetime.strptime(date_cell, "%d.%m.%Y")
                day_cell = date_cell.day
                month_cell = date_cell.month
            except Exception as es:
                msg = (f'Ошибка формирование даты из эксель ячейки ({cell.value}) "{es}"')

                print(msg)

                SendlerOneCreate('').save_text(msg)

                continue

            if now_month == month_cell:
                if now_day >= day_cell:
                    list_now_mouth_day.append(count)

        return list_now_mouth_day

    def _search_start_index_write_date(self, range, now_day, now_month, start_index):

        job_columns = start_index

        if now_day == 1:
            return job_columns

        find_now_moth_cell = self.iter_cell_find_mouth(range, now_day, now_month)

        if find_now_moth_cell == [] or 30 in find_now_moth_cell:
            return job_columns

        job_index = find_now_moth_cell.pop() + 1

        job_columns = range[job_index].address

        print()

        return job_columns

    def calculation_last_date(self, dict_range_row, name_sheet):
        now_day = datetime.now().day

        now_month = datetime.now().month

        worksheet = self.sheet.worksheet(name_sheet)

        _dict_start_index = {}

        for count_range_date in range(len(dict_range_row) // 2):
            _count = count_range_date + 1

            _range_1 = self.get_range_(worksheet, dict_range_row[f"column{_count}_start"],
                                       dict_range_row[f"column{_count}_end"])

            start_index_date = self._search_start_index_write_date(_range_1, now_day, now_month,
                                                                   dict_range_row[f"column{_count}_start"])

            _dict_start_index[f'range{_count}'] = start_index_date

        return _dict_start_index

    def clear_hide_group(self, name_list):
        worksheet = self.sheet.worksheet(name_list)

        worksheet.delete_dimension_group_columns(50, 1000)

        worksheet.unhide_columns(50, 1000)

        return True
