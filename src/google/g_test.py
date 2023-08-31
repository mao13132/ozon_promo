from oauth2client.service_account import ServiceAccountCredentials
import gspread

json_keyfile = 'ozonproject-1.json'

# Конфигурирование учетных данных
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)

# Аутентификация и получение доступа к таблице
gc = gspread.authorize(credentials)

# Открытие таблицы
sheet = gc.open('Копия Сводный отчет продвижения | Ozon')

worksheet = sheet.worksheet('Severli')

worksheet.delete_dimension_group_rows()
worksheet.unhide_rows()

