import pytest

class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    archive_category = lambda x: pytest.mark.parametrize("archive_category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])
    spend_update = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])