from playwright.sync_api import Page


class SpendingPageElements:
    def __init__(self, page: Page):
        self.page = page

    @property
    def amount(self):
        return self.page.locator("//input[@id='amount']")

    @property
    def currency(self):
        return self.page.locator("//input[@name='currency']")

    @property
    def category(self):
        return self.page.locator("//input[@id='category']")

    @property
    def date(self):
        return self.page.locator("//input[@name='date']")

    @property
    def description(self):
        return self.page.locator("//input[@id='description']")

    @property
    def add_button(self):
        return self.page.locator("//button[@id='save']")




