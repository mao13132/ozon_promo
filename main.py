import os

from datetime import datetime

from settings import PROMO_JOB
from src.browser.createbrowser_uc import CreatBrowser

from src.google.google_alternative import ConnectGoogleAlternative

from src.google.google_promo_get_data import GooglePromoGetData
from src.ozon.JobPromo import JobPromo

from src.ozon._check_dir import one_start


def main():

    dir_project = os.getcwd()

    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} начал работу')

    one_start(dir_project)

    google_alternate = ConnectGoogleAlternative()

    browser = CreatBrowser(dir_project)


    if PROMO_JOB:
        data_pars_dict = GooglePromoGetData(google_alternate).reviews_get_data()

        print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Обработал все вкладки. Начинаю работу с Ozon\n')

        res_job = JobPromo(browser.driver, data_pars_dict, google_alternate, dir_project).start_promo()

    print()


if __name__ == '__main__':
    main()
