import os

from datetime import datetime

from settings import PROMO_JOB, NAME_SERVER
from src.browser.createbrowser_uc import CreatBrowser

from src.google.google_alternative import ConnectGoogleAlternative

from src.google.google_promo_get_data import GooglePromoGetData
from src.ozon.JobPromo import JobPromo

from src.ozon._check_dir import one_start
from src.telegram_debug import SendlerOneCreate


def main():
    dir_project = os.getcwd()

    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} начал работу')

    one_start(dir_project)

    google_alternate = ConnectGoogleAlternative()

    try:
        browser = CreatBrowser(dir_project)


        if PROMO_JOB:
            data_pars_dict = GooglePromoGetData(google_alternate).reviews_get_data()

            print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Обработал все вкладки. Начинаю работу с Ozon\n')

            res_job = JobPromo(browser.driver, data_pars_dict, google_alternate, dir_project).start_promo()

        print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Закончил работу\n')

    except Exception as es:
        msg = f'{NAME_SERVER} Ошибка main поток ошибка: "{es}"'

        print(msg)

        SendlerOneCreate('').save_text(msg)

    finally:
        browser.driver.close()
        browser.driver.quit()


if __name__ == '__main__':
    main()
