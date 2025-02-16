from pages.login_page.login_page import LoginPage
from pages.main_page.main_page import MainPage
from playwright.sync_api import expect
import time

class TestLoginPage:

    def test_login_valid_creds(self, login_page: LoginPage):
        main_page: MainPage = login_page.login_with_valid_credentials(username="Ilnur", password="12345")
        expect(main_page.page).to_have_url("http://frontend.niffler.dc/main")