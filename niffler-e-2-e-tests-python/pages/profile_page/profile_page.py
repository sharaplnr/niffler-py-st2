from __future__ import annotations

import allure

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.profile_page.profile_page_elements import ProfilePageElements

class ProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.elements = ProfilePageElements(page)

    def open(self, url: str) -> ProfilePage:
        with allure.step("Open profile page"):
            profile_page: ProfilePage = ProfilePage(self.page)
            self.page.goto(url=url, wait_until="load")

            return profile_page

    def add_categories(self, category_name: str):
        self.elements.add_new_category_field.fill(category_name)
        self.elements.add_new_category_field.press("Enter")

    def archive_category(self, category_name: str):
        self.elements.archive_category_button(category_name).click()
        self.elements.archive_category_button_agreement.click()
        self.elements.successeful_archived_pop_up.is_visible()

    def get_active_categories(self) -> list[str]:
        self.page.locator("//span[contains(@class, 'MuiChip-label')]").first.wait_for()
        active_categories = self.page.locator("//span[contains(@class, 'MuiChip-label')]").all_inner_texts()
        return active_categories

    def get_all_categories(self) -> list[str]:
        self.elements.show_archived_toggle.click()
        all_categories = self.page.locator("//span[contains(@class, 'MuiChip-label')]").all_inner_texts()
        return all_categories

    def check_category_in_listed(self, category_name: str):
        assert category_name in self.get_active_categories()

    def check_category_not_in_listed(self, category_name: str):
        assert category_name not in self.get_active_categories()