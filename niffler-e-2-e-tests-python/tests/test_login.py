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


    def test_add_spending(self, spending_page: SpendingPage, main_page: MainPage):
        amount = str(randint(1, 1000))
        category = "test category"
        description = fake.word()

        spending_page.add_spending(amount, category, description)

        assert main_page.check_expense_in_table(category=category, description=description)

    def test_add_spending_without_amount_and_category(self, spending_page: SpendingPage):
        spending_page.click_add()

        expect(spending_page.elements.empty_amount_hint).to_be_visible()
        expect(spending_page.elements.empty_category_hint).to_be_visible()

    def test_delete_all_spendings(self, main_page: MainPage, spending_page: SpendingPage):
        amount = str(randint(1, 1000))
        category = "test category"
        description = fake.word()

        spending_page.add_spending(amount, category, description)
        assert main_page.check_expense_in_table(category=category, description=description)

        main_page.check_all_rows()
        main_page.delete_rows()

        assert main_page.is_table_empty()

    @TestData.category(TEST_CATEGORY)
    @TestData.spends({"amount":"414","description":"QA.GURU Python Advanced 2","currency":"RUB","spendDate":"2025-03-19T19:32:19.762Z","category":{"name":TEST_CATEGORY}})
    def test_spending_is_displayed_in_the_table(self, main_page, category, spends):
        main_page.check_expense_in_table(amount=spends["amount"], description=spends["description"], category=spends["category"]["name"])