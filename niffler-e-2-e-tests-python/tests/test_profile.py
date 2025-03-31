from marks import TestData
from pages.profile_page.profile_page import ProfilePage
from playwright.sync_api import expect
from faker import Faker

class TestProfile:

    fake = Faker()

    @TestData.category(fake.word())
    def test_added_category_is_visible_in_profile_list(self, profile_page: ProfilePage, category):
        profile_page.check_category_is_listed(category)
