from marks import TestData
from pages.profile_page.profile_page import ProfilePage
from faker import Faker

class TestProfile:
    TEST_CATEGORY = Faker().word()

    @TestData.category(TEST_CATEGORY)
    @TestData.archive_category(TEST_CATEGORY)
    def test_added_category_is_visible_in_profile_list(self, profile_page: ProfilePage, category, archive_category):
        profile_page.check_category_in_listed(category)