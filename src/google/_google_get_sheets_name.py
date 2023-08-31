from settings import ID_SHEET, BLACK_NAME
from src.telegram_debug import SendlerOneCreate


class GoogleGetSheetsName:
    def __init__(self, google_core):
        self.google_core = google_core
        self.service = google_core.service

    def get_name_sheets(self):

        # Пример чтения файла
        try:
            self.connect = self.service.spreadsheets().get(spreadsheetId=ID_SHEET).execute()

            sheetList = self.connect.get('sheets')

        except Exception as es:
            msg = (f'🚫 Ошибка при подключении к Google таблицам "{es}"')

            print(msg)

            SendlerOneCreate('').save_text(msg)

            return False

        try:

            name_list = [x['properties']['title'] for x in sheetList if x['properties']['title'] not in BLACK_NAME]

        except Exception as es:
            msg = (f'Ошибка при формирования списка имен вкладок "{es}"')

            print(msg)

            SendlerOneCreate('').save_text(msg)

            return []

        return name_list
