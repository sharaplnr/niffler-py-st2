from playwright.sync_api import Page

class MainPageElements:
    def __init__(self, page: Page):
        self.page = page