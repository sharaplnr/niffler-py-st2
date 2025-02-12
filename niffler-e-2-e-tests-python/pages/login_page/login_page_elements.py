from playwright.sync_api import Page

class LoginPageElements:
    def __init__(self, page: Page):
        self.page = page

    @property
    def username(self):
        return self.page.locator("#username")

    @property
    def password(self):
        return self.page.locator("#password")

    @property
    def sumbit_button(self):
        return self.page.locator("#submit")

    @property
    def sign_up_link(self):
        return self.page.locator("#signup")

