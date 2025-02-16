import allure

from pages.base_page import BasePage
from playwright.sync_api import Page


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, url: str):
        with allure.step("Open login page"):
            self.page.goto(url=url, wait_until="load")
            return self