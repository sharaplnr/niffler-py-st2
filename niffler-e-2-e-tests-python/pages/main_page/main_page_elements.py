from playwright.sync_api import Page

class MainPageElements:
    def __init__(self, page: Page):
        self.page = page

    @property
    def history_of_spendings_title(self):
        return self.page.locator("//div[@id='spendings']/h2")

    @property
    def no_spendings_text(self):
        return self.page.locator("//p[contains(text(), 'no spendings')]")

    @property
    def general_checkbox(self):
        return self.page.locator("//thead//th[1]//input")

    @property
    def new_spending_btn(self):
        return self.page.locator("//a[@href='/spending']")

    @property
    def delete_button(self):
        return self.page.locator("//button[@id='delete']")

    @property
    def delete_button_in_delete_spendings_form(self):
        return self.page.locator("//div[contains(@class, 'MuiDialogActions-root')]/button[contains(text(), 'Delete')]")