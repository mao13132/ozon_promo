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

        self.count_group = 7

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
        good_dict = {}

        for x in range(5):
            good_dict[f'dict_columns_{x + 1}'] = {}

        _dict = {}

        for count, column in enumerate(list_columns):

            if self.name_columns_1 in column.value:
                # _dict['column1_start'] = column.address[:-1] + '2'
                # _dict['column1_start_col'] = column.col
                good_dict[f'dict_columns_1']['column1_start'] = column.address[:-1] + '2'
                good_dict[f'dict_columns_1']['column1_start_col'] = column.col

            if self.name_columns_2 in column.value:
                # _dict['column1_end'] = list_columns[count - 1].address[:-1] + '2'
                # _dict['column1_end_col'] = list_columns[count - 1].col
                #
                # _dict['column2_start'] = column.address[:-1] + '2'
                # _dict['column2_start_col'] = column.col

                good_dict[f'dict_columns_1']['column1_end'] = list_columns[count - 1].address[:-1] + '2'
                good_dict[f'dict_columns_1']['column1_end_col'] = list_columns[count - 1].col

                good_dict[f'dict_columns_2']['column2_start'] = column.address[:-1] + '2'
                good_dict[f'dict_columns_2']['column2_start_col'] = column.col

            if self.name_columns_3 in column.value:
                # _dict['column2_end'] = list_columns[count - 1].address[:-1] + '2'
                # _dict['column2_end_col'] = list_columns[count - 1].col
                #
                # _dict['column3_start'] = column.address[:-1] + '2'
                # _dict['column3_start_col'] = column.col
                good_dict[f'dict_columns_2']['column2_end'] = list_columns[count - 1].address[:-1] + '2'
                good_dict[f'dict_columns_2']['column2_end_col'] = list_columns[count - 1].col

                good_dict[f'dict_columns_3']['column3_start'] = column.address[:-1] + '2'
                good_dict[f'dict_columns_3']['column3_start_col'] = column.col

            if self.name_columns_4 in column.value:
                # _dict['column3_end'] = list_columns[count - 1].address[:-1] + '2'
                # _dict['column3_end_col'] = list_columns[count - 1].col
                #
                # _dict['column4_start'] = column.address[:-1] + '2'
                # _dict['column4_start_col'] = column.col

                good_dict[f'dict_columns_3']['column3_end'] = list_columns[count - 1].address[:-1] + '2'
                good_dict[f'dict_columns_3']['column3_end_col'] = list_columns[count - 1].col

                good_dict[f'dict_columns_4']['column4_start'] = column.address[:-1] + '2'
                good_dict[f'dict_columns_4']['column4_start_col'] = column.col

            if self.name_columns_5 in column.value and self.name_columns_3 not in column.value:
                # _dict['column4_end'] = list_columns[count - 1].address[:-1] + '2'
                # _dict['column4_end_col'] = list_columns[count - 1].col
                #
                # _dict['column5_start'] = column.address[:-1] + '2'
                # _dict['column5_start_col'] = column.col

                good_dict[f'dict_columns_4']['column4_end'] = list_columns[count - 1].address[:-1] + '2'
                good_dict[f'dict_columns_4']['column4_end_col'] = list_columns[count - 1].col

                good_dict[f'dict_columns_5']['column5_start'] = column.address[:-1] + '2'
                good_dict[f'dict_columns_5']['column5_start_col'] = column.col

                good_dict[f'dict_columns_5']['column5_end'] = list_columns[count + 30].address[:-1] + '2'
                good_dict[f'dict_columns_5']['column5_end_col'] = list_columns[count + 30].col

                # _dict['column5_end'] = list_columns[count + 30].address[:-1] + '2'
                # _dict['column5_end_col'] = list_columns[count + 30].col

        return good_dict

    def get_range_(self, worksheet, start_index, end_index):
        """Получаю значения из таблицы"""
        try:
            list_call = worksheet.range(f'{start_index}:{end_index}')
        except Exception as es:
            msg = (f'Ошибка при получения ренджа для вычисления даты ({start_index} - {end_index}) "{es}"')

            print(msg)

            SendlerOneCreate('').save_text(msg)

            return []

        return list_call

    def iter_cell_date_range(self, range, now_day, now_month):
        """Итерирую 1 диапазон с полученными значениями в виде дат и сравниваю с текущей датой"""

        list_now_mouth_day = []

        for count, cell in enumerate(range):

            date_cell = cell.value

            if cell.value == '':
                continue

            try:
                date_cell = datetime.strptime(date_cell, "%d.%m.%Y")
                day_cell = date_cell.day
                month_cell = date_cell.month
            except:
                continue

            if now_month == month_cell:
                if now_day >= day_cell:
                    list_now_mouth_day.append(count)

        return list_now_mouth_day

    def iter_range_find_date(self, range, now_day, now_month, start_index, start_index_col):
        """Итерируется диапазон с датами и ищется текущий месяц, если нет то стартовая позиция - первая"""

        job_columns = {'job_index': start_index, 'job_index_col': start_index_col,
                       'left_count': 0, 'right_count': 30, 'range': range}
        # job_columns = start_index

        if now_day == 1:
            return job_columns

        find_now_moth_cell = self.iter_cell_date_range(range, now_day, now_month)

        if find_now_moth_cell == [] or 30 in find_now_moth_cell:
            return job_columns

        job_index = find_now_moth_cell.pop() + 1

        start_index = range[job_index].address

        start_index_col = range[job_index].col

        job_columns = {'job_index': start_index, 'job_index_col': start_index_col,
                       'left_count': job_index, 'right_count': len(range) - job_index - 1,
                       'range': range}

        # job_columns = range[job_index].address

        return job_columns

    def calculation_last_date(self, dict_range_row, name_sheet):
        """Получаю текущую дату и пробегаю по диапазонам, отправляя их в функцию итерации"""

        now_day = datetime.now().day

        now_month = datetime.now().month

        worksheet = self.sheet.worksheet(name_sheet)

        good_list = []

        for count_range_date, range_columns in enumerate(dict_range_row.values()):
            _dict_start_index = {}

            _count = count_range_date + 1

            _range = self.get_range_(worksheet, range_columns[f"column{_count}_start"],
                                     range_columns[f"column{_count}_end"])

            start_index_date = self.iter_range_find_date(_range, now_day, now_month,
                                                         range_columns[f"column{_count}_start"],
                                                         range_columns[f"column{_count}_start_col"])

            _dict_start_index[f'range{_count}'] = start_index_date
            _dict_start_index[f"column{_count}_start"] = range_columns[f"column{_count}_start"]
            _dict_start_index[f"column{_count}_start_col"] = range_columns[f"column{_count}_start_col"]

            _dict_start_index[f"column{_count}_end"] = range_columns[f"column{_count}_end"]
            _dict_start_index[f"column{_count}_end_col"] = range_columns[f"column{_count}_end_col"]

            good_list.append(_dict_start_index)

        return good_list

    def _iter_dict_create_group(self, good_range_date, worksheet):

        for count, _range in enumerate(good_range_date):

            _count = count + 1

            left_count = _range[f"range{_count}"]['left_count']

            right_count = _range[f"range{_count}"]['right_count']

            if left_count > self.count_group:
                difference = left_count - self.count_group

                columns_difference = _range[f"range{_count}"]['range'][difference].col

                worksheet.add_dimension_group_columns(_range[f'column{_count}_start_col'] - 1, columns_difference)

                worksheet._hide_dimension(_range[f'column{_count}_start_col'] - 1, columns_difference, 'COLUMNS')

            if right_count > 1:
                worksheet.add_dimension_group_columns(_range[f"range{_count}"]['job_index_col'] - 1,
                                                      _range[f'column{_count}_end_col'] - 1)

                worksheet._hide_dimension(_range[f"range{_count}"]['job_index_col'] - 1,
                                          _range[f'column{_count}_end_col'] - 1, 'COLUMNS')

        return True

    def clear_hide_group(self, good_range_date, name_sheet):
        worksheet = self.sheet.worksheet(name_sheet)

        worksheet.delete_dimension_group_columns(50, 1000)

        worksheet.unhide_columns(50, 1000)

        res_group = self._iter_dict_create_group(good_range_date, worksheet)

        return True