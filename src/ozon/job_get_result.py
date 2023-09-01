import time

from selenium.webdriver.common.by import By


class GetGetResult:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'Ozon'

    def get_rows(self):
        try:
            rows_list = self.driver.find_elements(by=By.XPATH,
                                                  value=f"//tbody//tr[contains(@class, 'row')]")
        except:
            return []

        return rows_list

    def get_result(self, row):
        try:
            _result = row.find_elements(by=By.XPATH,
                                        value=f"//tbody//tr[contains(@class, 'row')]//td")[2].text
        except:
            return ''

        return _result

    def start_job_get_result(self):
        result_list = self.get_rows()

        if result_list == []:
            return False

        result = self.get_result(result_list[0])

        return result
