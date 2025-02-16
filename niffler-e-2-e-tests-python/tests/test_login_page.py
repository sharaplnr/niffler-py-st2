from pages.login_page.login_page import LoginPage


class TestLoginPage:

    def test_login_valid_creds(self, login_page: LoginPage):
        page = login_page
        page.login_with_valid_credentials(username="Ilnur", password="12345")
