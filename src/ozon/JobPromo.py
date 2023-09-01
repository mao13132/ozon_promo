import time

from datetime import datetime

class JobPromo:
    def __init__(self, driver, google_core, data_pars_dict):
        self.driver = driver
        self.google_core = google_core
        self.data_pars_dict = data_pars_dict
        self.old_files_name = []
