from playwright.sync_api import Page

class ProfilePageElements:
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_new_category_field(self):
        return self.page.locator("//input[@id='category']")

    @property
    def name_field(self):
        return self.page.locator("//input[@id='name']")

    @property
    def save_changes_button(self):
        return self.page.locator("//button[@id=':r1:']")

    @property
    def show_archived_toggle(self):
        return self.page.locator("//input[@type='checkbox']")

    def edit_category_button(self, category_name: str):
        return self.page.locator(f"f//span[contains(text(), '{category_name}')]/"
                                 f"../..//button[@aria-label='Edit category']")

    def archive_category_button(self, category_name: str):
        return self.page.locator(f"f//span[contains(text(), '{category_name}')]/"
                                 f"../..//button[@aria-label='Archive category']")