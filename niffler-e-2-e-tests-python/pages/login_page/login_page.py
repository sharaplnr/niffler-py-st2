import allure
from playwright.sync_api import Page

from pages.login_page.login_page_elements import LoginPageElements
from pages.base_page import BasePage
from pages.main_page.main_page import MainPage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.elements = LoginPageElements(page)

    def open(self, url: str):
        with allure.step("Open login page"):
            self.page.goto(url=url, wait_until="load")
            return self

    def fill_username(self, username: str):
        with allure.step("Fill username field"):
            self.elements.username.fill(username)

    def fill_password(self, password: str):
        with allure.step("Fill password field"):
            self.elements.password.fill(password)

    def fill_sumbit_password(self, submit_password: str):
        with allure.step("Fill submit password field"):
            self.elements.submit_password.fill(submit_password)

    def click_sign_up(self):
        with allure.step("Click sing up button"):
            self.elements.sign_up.click()

    def click_log_in(self):
        with allure.step("Click log in button"):
            self.elements.log_in.click()

    def click_submit_button(self) -> MainPage:
        with allure.step("Click login button"):
            self.elements.log_in.click(timeout=20000)
            main_page = MainPage(self.page)
            return main_page

    def open_log_in_form(self):
        with allure.step("Open sign up page"):
            self.click_log_in()

    def open_create_new_acc_from(self):
        with allure.step("Open sign in page"):
            self.elements.create_new_acc.click()

    def login_with_valid_credentials(self, username: str, password: str):
        with allure.step("Login with valid credentials"):
            # self.open_sign_up_form()
            self.fill_username(username)
            self.fill_password(password)
            return self.click_submit_button()


