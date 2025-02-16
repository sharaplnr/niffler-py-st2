from playwright.sync_api import Page

class LoginPageElements:
    def __init__(self, page: Page):
        self.page = page

    @property
    def username(self):
        return self.page.locator("//input[@name='username']")

    @property
    def password(self):
        return self.page.locator("//input[@name='password']")

    @property
    def log_in(self):
        return self.page.locator("//button[contains(text(), 'Log in')]")

    @property
    def login_in_link(self):
        return self.page.locator("//a[@href='http://frontend.niffler.dc/main']")

    @property
    def create_new_acc(self):
        return self.page.locator("//a[@href='/register']")

