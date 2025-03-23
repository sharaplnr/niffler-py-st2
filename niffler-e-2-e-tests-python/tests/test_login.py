from conftest import main_page
from pages.login_page.login_page import LoginPage
from pages.main_page.main_page import MainPage
from pages.spending_page.spending_page import SpendingPage
from playwright.sync_api import expect
from random import randint
from faker import Faker
from marks import TestData

fake = Faker()


class TestNifflerIntro:

    TEST_CATEGORY: str = "sharap"

    def test_login_valid_creds(self, main_page: MainPage):
        expect(main_page.elements.history_of_spendings_title).to_have_text("History of Spendings")

    def test_login_without_password(self, login_page: LoginPage):
        login_page.fill_username('Ilnur')
        login_page.click_log_in()

        expect(login_page.elements.history_spendings_text_on_main_page).not_to_be_visible()


    def test_create_valid_user(self, login_page: LoginPage, random_credentials):
        username, password = random_credentials

        login_page.open_create_new_acc_from()
        login_page.fill_username(username)
        login_page.fill_password(password)
        login_page.fill_sumbit_password(password)
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).to_be_visible()

    def test_create_user_with_empty_passwords(self, login_page: LoginPage, random_username):
        username = random_username

        login_page.open_create_new_acc_from()
        login_page.fill_username(username)
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).not_to_be_visible()

    def test_create_user_with_empty_username(self, login_page: LoginPage, random_password):
        password = random_password

        login_page.open_create_new_acc_from()
        login_page.fill_password(password)
        login_page.fill_sumbit_password(password)
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).not_to_be_visible()

    def test_create_user_with_empty_username_and_password(self, login_page: LoginPage):
        login_page.open_create_new_acc_from()
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).not_to_be_visible()

    def test_create_user_with_empty_submit_password(self, login_page: LoginPage, user_credentials):
        username, password = user_credentials

        login_page.open_create_new_acc_from()
        login_page.fill_username(username)
        login_page.fill_password(password)
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).not_to_be_visible()