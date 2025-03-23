from conftest import fake
from pages.main_page.main_page import MainPage
from pages.spending_page.spending_page import SpendingPage
from playwright.sync_api import expect
from marks import TestData
from random import randint


class TestSpending:

    TEST_CATEGORY: str = "sharap"

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
    @TestData.spends({"amount":"414","description":"QA.GURU Python Advanced 2","currency":"RUB",
                      "spendDate":"2025-03-19T19:32:19.762Z","category":{"name":TEST_CATEGORY}})
    def test_spending_is_displayed_in_the_table(self, main_page, category, spends):
        main_page.check_expense_in_table(amount=spends["amount"], description=spends["description"], category=spends["category"]["name"])

    @TestData.spends({"amount":"414","description":"QA.GURU Python Advanced 2","currency":"RUB",
                      "spendDate":"2025-03-19T19:32:19.762Z","category":{"name":TEST_CATEGORY}})
    def test_update_spending_is_displayed_in_the_table(self, main_page, spends, spends_client):
        main_page.check_expense_in_table(amount=spends["amount"], description=spends["description"], category=spends["category"]["name"], date=spends["spendDate"])

        spend_id = spends["id"]
        update_spend_data = spends_client.update_spends({"amount":"999","description":"QA.GURU","currency":"RUB",
                      "spendDate":"2025-01-01T19:32:19.762Z", "id": spend_id,"category":{"name":"update category"}})

        main_page.check_expense_in_table(amount=update_spend_data["amount"], description=update_spend_data["description"],
                                         category=update_spend_data["category"]["name"], date=update_spend_data["spendDate"])