import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.spending_page.spending_page_elements import SpendingPageElements

class SpendingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.elements = SpendingPageElements(page)

    def fill_amount(self, amount: str):
        self.elements.amount.fill(amount)

    def fill_currency(self, currency: str):
        self.elements.currency.fill(currency)

    def fill_category(self, category: str):
        self.elements.category.fill(category)

    def fill_date(self, date: str = "01/01/2025"):
        self.elements.date.fill(date)

    def fill_description(self, description: str):
        self.elements.description.fill(description)

    def click_add(self):
        self.elements.add_button.click()


    def add_spending(self, amount: str, category:str, description:str, date:str = '01/01/2025', currency:str = None):
        self.fill_amount(amount)
        self.fill_category(category)
        if currency:
            self.fill_currency(currency)
        self.fill_date(date)
        if description:
            self.fill_description(description)
        self.click_add()
