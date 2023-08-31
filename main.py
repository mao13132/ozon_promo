import os
from datetime import datetime

from settings import PROMO_JOB
from src.google.google_modul import GoogleModul
from src.google.google_promo_get_data import GooglePromoGetData
from src.ozon.check_dir import one_start


def main():
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} начал работу')

    dir_project = os.getcwd()

    one_start(dir_project)

    google_core = GoogleModul(dir_project).connect_sheet()

    if PROMO_JOB:
        data_pars_dict = GooglePromoGetData(google_core).reviews_get_data()

    print()


if __name__ == '__main__':
    main()
