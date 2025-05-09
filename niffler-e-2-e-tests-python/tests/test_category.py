from models.db.category import Category
from models.api.category import CategoriesResponse, CategoryRequest
from marks import TestData


class TestCategory:

    TEST_CATEGORY: str = "test_db_category"

    @TestData.category(TEST_CATEGORY)
    def test_validation_added_category(self, spend_db, category):
        category_db_entry: Category = spend_db.get_category_by_id(category.id)

        assert category_db_entry.name == category.name
        assert category_db_entry.username == category.username
        assert category_db_entry.archived == category.archived

    @TestData.category(TEST_CATEGORY)
    def test_validation_updated_category(self, spend_db, category, spends_client):
        category_db_entry: Category = spend_db.get_category_by_id(category.id)

        assert category_db_entry.name == category.name
        assert category_db_entry.username == category.username
        assert category_db_entry.archived == category.archived

        category_data = CategoryRequest(id=category.id, name="updated_name", archived=True)

        updated_category_entry: CategoriesResponse = spends_client.update_category(body=category_data.model_dump())

        assert updated_category_entry.name == category_data.name
        assert updated_category_entry.archived == category_data.archived