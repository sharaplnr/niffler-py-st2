from typing import Literal

import allure
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self,
             url: str,
             wait_until: Literal["commit", "domcontentloaded", "load", "networkidle"] | None = "load") -> Page:
        with allure.step(f"Open {url}"):
            self.page.goto(url=url, wait_until=wait_until)
            return self.page

    def reload(self) -> None:
        """Метод для перезагрузки страницы"""
        self.page.reload(wait_until="load")

