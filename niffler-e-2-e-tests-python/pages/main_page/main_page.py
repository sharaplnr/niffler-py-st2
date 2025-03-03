import allure

from pages.base_page import BasePage
from pages.spending_page.spending_page import SpendingPage
from pages.main_page.main_page_elements import MainPageElements
from playwright.sync_api import Page


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.elements = MainPageElements(page)

    def open(self, url: str):
        with allure.step("Open login page"):
            self.page.goto(url=url, wait_until="load")
            return self

    def open_add_new_spending_form(self):
        with allure.step("Open new spending form"):
            self.elements.new_spending_btn.click()
            spending_page = SpendingPage(self.page)
            return spending_page

    def check_all_rows(self):
        with allure.step("Check all rows in table"):
            self.elements.general_checkbox.is_visible()
            self.elements.general_checkbox.click()

    def delete_rows(self):
        with allure.step("Delete row/s in table"):
            self.elements.delete_button.click()
            self.elements.delete_button_in_delete_spendings_form.click()

    def is_table_empty(self):
        with allure.step("Check that the table is empty"):
            self.elements.no_spendings_text.wait_for(timeout=2000)
            return self.elements.no_spendings_text.is_visible()

    def check_expense_in_table(self, category:str = None, amount:str = None, description: str = None, date: str = None):
        self.page.locator("//tbody/tr[contains(@class,'MuiTableRow-root')]").first.wait_for(timeout=2000)

        rows = self.page.locator("//tbody/tr[contains(@class,'MuiTableRow-root')]").all()
        for row in rows:
            category_field = row.locator("xpath=/td[2]/span").inner_text()
            amount_field = row.locator("xpath=/td[3]/span").inner_text()
            description_field = row.locator("xpath=/td[4]/span").inner_text()
            date_field = row.locator("xpath=/td[5]/span").inner_text()

            match = True

            if category and category != category_field:
                match = False
            if amount and amount != amount_field:
                match = False
            if description and description != description_field:
                match = False
            if date and date != date_field:
                match = False

            if match:
                return True

        return False


