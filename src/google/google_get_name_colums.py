from settings import ID_SHEET


class GoogleGetNameColums:
    def __init__(self, google_core):
        self.google_core = google_core
        self.service = google_core.service
        self.count = 100000000

    def get_name_columns(self, name_sheet):

        try:

            self.values = self.service.spreadsheets().values().get(
                spreadsheetId=ID_SHEET,
                range=f'{name_sheet}!A1:ZZ1',
                majorDimension='ROWS'
            ).execute()

        except Exception as es:
            print(f'🚫 Ошибка при подключении к Google ({name_sheet}) таблицам "{es}"')

            return False

        return self.values

    def get_geography_cabinet_name(self):

        try:

            self.values = self.service.spreadsheets().values().get(
                spreadsheetId=ID_SHEET,
                range=f'Индексы!B2:B{self.count}',
                majorDimension='COLUMNS'
            ).execute()

        except Exception as es:
            print(f'🚫 Ошибка при подключении к Google (индексы) таблицам "{es}"')

            return False

        return self.values

    @staticmethod
    def get_index_competitor(list_name_columns):
        ip_list_index = []
        article = 0
        for count, colm in enumerate(list_name_columns['values'][0]):

            _temp_ip = {}

            if 'Артикул' in colm:
                article = count

            if 'Запрос' in colm:
                _temp_ip['name'] = colm
                _temp_ip['index'] = count
                _temp_ip['article_inx'] = article

                ip_list_index.append(_temp_ip)

        return ip_list_index

    # @staticmethod
    # def get_index_article(list_name_columns):
    #     for count, colm in enumerate(list_name_columns['values'][0]):
    #
    #         if 'Артикул' in colm:
    #             return count
    #
    #     return False
