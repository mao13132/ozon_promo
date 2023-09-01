import time

from selenium.webdriver.common.by import By


class JobRegion:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'Ozon'

    def click_region(self, row):
        try:
            row.click()
        except:
            return False

        return True

    def click_insert_region(self, region):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), '{region}')]").click()
        except:
            return False

        return True

    def get_region_text(self, row):
        try:
            _region = row.find_element(by=By.XPATH,
                                       value=f".//input").get_attribute('value')
        except:
            return ''

        return _region

    def start_job_region(self, row, region):
        count = 0
        count_try = 5
        while True:
            count += 1
            if count > count_try:
                print(f'Не смог выбрать регион')
                return False
            _region = self.get_region_text(row)

            if _region != region:
                res_click_region = self.click_region(row)

                res_reg_insert = self.click_insert_region(region)

                if count > 1:
                    time.sleep(1)
                continue

            return True
