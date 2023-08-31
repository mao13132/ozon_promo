import os

from pathlib import Path

from settings import NAME_API_FILE

from oauth2client.service_account import ServiceAccountCredentials

import httplib2

import apiclient


class GoogleModul:
    def __init__(self, dir_project):
        self.dir_project = dir_project

    def _load_file_security(self):
        file_dir = Path(f"{self.dir_project}/src/google_api_file/{NAME_API_FILE}")
        if not os.path.exists(file_dir):
            print(f'Не добавлен API файл-ключ от google sheets. Добавьте ключ-файл .json от API гугл таблиц в '
                  f'папку google_api_file, а так же его название в settings.py')
            return False

        return file_dir

    def connect_sheet(self):
        self.api_key_file = self._load_file_security()

        if not self.api_key_file:
            return False

        # Авторизуемся и получаем service — экземпляр доступа к API
        try:
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.api_key_file, ['https://www.googleapis.com/auth/spreadsheets',
                                    'https://www.googleapis.com/auth/drive'])

            self.httpAuth = self.credentials.authorize(httplib2.Http())

            self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)

        except Exception as es:
            msg_er = (f'ошибка при подключении к GOOGLE Sheets "{es}"')
            print(msg_er)

            return False

        return self
