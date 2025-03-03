from pages.login_page.login_page import LoginPage
from pages.main_page.main_page import MainPage
from playwright.sync_api import expect
from faker import Faker
from random import randint

from pages.spending_page.spending_page import SpendingPage

fake = Faker()


class TestNiffler:

    def test_login_valid_creds(self, login_page: LoginPage):
        main_page: MainPage = login_page.login_with_valid_credentials(username="Ilnur", password="12345")
        expect(main_page.elements.history_of_spendings_title).to_have_text("History of Spendings")

    def test_login_without_password(self, login_page: LoginPage):
        login_page.fill_username('Ilnur')
        login_page.click_log_in()
        expect(login_page.page.locator("//div[@id='spendings']/h2")).not_to_be_visible()


    def test_create_valid_user(self, login_page: LoginPage):
        username, password = (fake.user_name(), fake.password())

        login_page.open_create_new_acc_from()
        login_page.fill_username(username)
        login_page.fill_password(password)
        login_page.fill_sumbit_password(password)
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).to_be_visible()

    def test_create_user_with_empty_passwords(self, login_page: LoginPage):
        username = fake.user_name()

        login_page.open_create_new_acc_from()
        login_page.fill_username(username)
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).not_to_be_visible()

    def test_create_user_with_empty_username(self, login_page: LoginPage):
        password = fake.password()

        login_page.open_create_new_acc_from()
        login_page.fill_password(password)
        login_page.fill_sumbit_password(password)
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).not_to_be_visible()

    def test_create_user_with_empty_username_and_password(self, login_page: LoginPage):
        login_page.open_create_new_acc_from()
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).not_to_be_visible()

    def test_create_user_with_empty_submit_password(self, login_page: LoginPage):
        username, password = (fake.user_name(), fake.password())

        login_page.open_create_new_acc_from()
        login_page.fill_username(username)
        login_page.fill_password(password)
        login_page.click_sign_up()

        expect(login_page.elements.successeful_registered_text).not_to_be_visible()


    def test_add_spending(self, login_page: LoginPage):
        username, password = ("Ilnur", "12345")
        amount = str(randint(1, 1000))
        category = "test category"
        description = fake.word()


        main_page: MainPage = login_page.login_with_valid_credentials(username, password)
        spending_page: SpendingPage = main_page.open_add_new_spending_form()
        spending_page.add_spending(amount, category, description)

        assert main_page.check_expense_in_table(category=category, description=description)

    def test_delete_all_spendings(self, login_page: LoginPage):
        username, password = ("Ilnur", "12345")
        amount = str(randint(1, 1000))
        category = "test category"
        description = fake.word()

        main_page: MainPage = login_page.login_with_valid_credentials(username, password)
        spending_page: SpendingPage = main_page.open_add_new_spending_form()
        spending_page.add_spending(amount, category, description)
        assert main_page.check_expense_in_table(category=category, description=description)

        main_page.check_all_rows()
        main_page.delete_rows()

        assert main_page.is_table_empty()


