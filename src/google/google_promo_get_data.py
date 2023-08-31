import time

from settings import NAME_SHEET, ID_SHEET
from src.google._google_get_sheets_name import GoogleGetSheetsName
from src.google.google_alternative import ConnectGoogleAlternative
from src.google.google_get_name_colums import GoogleGetNameColums


class GooglePromoGetData:
    def __init__(self, google_core):
        self.google_core = google_core
        self.count_load_rows = 100000

    def _get_article(self, x, y, name_sheet):
        values = self.google_core.service.spreadsheets().values().get(
            spreadsheetId=ID_SHEET,
            range=f'{name_sheet}!{x}:{y}',
            majorDimension='ROWS'
        ).execute()
        try:
            values = values['values']
        except:
            return []

        return values

    def get_article(self, article, name_sheet):

        x = f"{colums_slovar[article]}2"

        y = f"{colums_slovar[article]}{self.count_load_rows}"

        article_list = self._get_article(x, y, name_sheet)

        return article_list

    @staticmethod
    def get_index_reviews(list_name_columns):
        ip_list_index = []
        article = 0
        for count, colm in enumerate(list_name_columns['values'][0]):

            _temp_ip = {}

            if 'Артикул' in colm:
                article = count

            if 'Отзывы' in colm:
                _temp_ip['name'] = colm
                _temp_ip['index'] = count
                _temp_ip['article_inx'] = article

                ip_list_index.append(_temp_ip)

        return ip_list_index

    def start_format_data(self, name_sheet, name_index_list, article_list):

        good_dict_data = []

        for count, article_ in enumerate(article_list):

            if article_ == []:
                continue

            count = count + 2

            x = f"{colums_slovar[name_index_list[0]['index']]}{count}"

            product = {}

            try:
                product['competitor'] = 'Отзывы'
            except:
                continue

            product['request'] = ''

            product['name_sheet'] = name_sheet
            product['x'] = x
            product['y'] = x
            product['price_index'] = ''
            try:
                product['article'] = article_[0]
            except:
                continue

            good_dict_data.append(product)

        return good_dict_data

    def reviews_get_data(self):

        if NAME_SHEET == []:
            names_list_sheet = GoogleGetSheetsName(self.google_core).get_name_sheets()
        else:
            names_list_sheet = NAME_SHEET

        good_all_job = []

        google_alternate = ConnectGoogleAlternative()

        for name_sheet in names_list_sheet:

            # TODO работа по получению индексов столбцов дат

            range_date_list = google_alternate.get_range_date_columns(name_sheet)

            if range_date_list == []:
                print(f'Не найдены данные на {name_sheet}')
                continue

            dict_range_date = google_alternate.calculation_range_date(range_date_list)

            good_range_date = google_alternate.calculation_last_date(dict_range_date, name_sheet)

            res_group = google_alternate.clear_hide_group(good_range_date, name_sheet)



            print()

            # print(f'Получаю данные для построения отчёта эффективности с вкладки {name_sheet}')
            #
            # name_columns = GoogleGetNameColums(self.google_core).get_name_columns(name_sheet)
            #
            # if not name_columns:
            #     continue
            #
            # name_index_list = self.get_index_reviews(name_columns)
            #
            # if name_index_list == []:
            #     print(f'На вкладке {name_sheet} не обнаружены столбцы с данными')
            #     continue
            #
            # article = name_index_list[0]['article_inx']
            #
            # article_list = self.get_article(article, name_sheet)
            #
            # dict_job_one_sheet = self.start_format_data(name_sheet, name_index_list, article_list)
            #
            # good_all_job.extend(dict_job_one_sheet)
            #
            # time.sleep(5)

        return good_all_job
