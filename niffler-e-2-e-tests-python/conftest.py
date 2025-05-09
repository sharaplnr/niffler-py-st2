import os

import pytest
from playwright.sync_api import Playwright
from dotenv import load_dotenv
from faker import Faker

from databases.spend_db import SpendDB
from models.api.category import CategoriesResponse
from models.api.spend import SpendResponse
from models.config import Envs
from pages.base_page import BasePage
from pages.login_page.login_page import LoginPage
from pages.main_page.main_page import MainPage
from pages.profile_page.profile_page import ProfilePage
from pages.spending_page.spending_page import SpendingPage
from clients.spends_client import SpendHttpClient


fake = Faker()


@pytest.fixture(scope="session", autouse=True)
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        auth_url=os.getenv("AUTH_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )

@pytest.fixture()
def page_init(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()

@pytest.fixture()
def auth(login_page: LoginPage, envs):
    username, password = envs.test_username, envs.test_password
    login_page.login_with_valid_credentials(username, password)
    token = login_page.page.evaluate(expression='window.localStorage.getItem("id_token")')

    if token is None:
        raise ValueError("Token not found in localStorage")

    yield token

@pytest.fixture()
def spends_client(envs, auth) -> SpendHttpClient:
    return SpendHttpClient(envs.gateway_url, auth)

@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDB:
    return SpendDB(envs.spend_db_url)

@pytest.fixture(params=[])
def category(request, spends_client, spend_db):
    category_name: str = request.param
    category: CategoriesResponse = spends_client.add_category(category_name)
    yield category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def archive_category(request, profile_page):
    category_name: str = request.param
    yield
    profile_page.reload()
    profile_page.archive_category(category_name)
    profile_page.check_category_not_in_listed(category_name)


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend: SpendResponse = spends_client.add_spends(request.param)
    yield spend
    current_spends: list[SpendResponse] = spends_client.get_spends()
    spends_ids = [spend.id for spend in current_spends]
    if spend.id in spends_ids:
        spends_client.remove_spends([spend.id])

@pytest.fixture(params=[])
def spend_update(request, spends_client):
    spends_client.update_spends(request.param)

@pytest.fixture()
def category_name(request):
    """Фикстура генерирует и кэширует category_name для текущего теста."""
    if not hasattr(request.node, "category_name_cache"):
        category_name = fake.word()
        request.node.user_credentials_cache = category_name
    return request.node.user_credentials_cache

@pytest.fixture()
def random_category(category_name):
    return category_name

@pytest.fixture()
def category_for_spend(main_page, random_category, spend_db):
    category_name: str = random_category
    yield category_name
    main_page.delete_spend_by_category_name(category_name)
    spend_db.delete_category_by_name(category_name)

@pytest.fixture()
def user_credentials(request):
    """Фикстура генерирует и кэширует username и password для текущего теста."""
    if not hasattr(request.node, "user_credentials_cache"):
        username = fake.user_name()
        password = fake.password()
        request.node.user_credentials_cache = (username, password)
    return request.node.user_credentials_cache

@pytest.fixture()
def random_username(user_credentials):
    """Возвращает username из кэша текущего теста."""
    return user_credentials[0]

@pytest.fixture()
def random_password(user_credentials):
    """Возвращает password из кэша текущего теста."""
    return user_credentials[1]

@pytest.fixture()
def random_credentials(user_credentials):
    """Возвращает кортеж (username, password) для текущего теста."""
    return user_credentials

@pytest.fixture()
def base_page(page_init):
    yield BasePage(page_init)

@pytest.fixture()
def login_page(page_init, envs):
    yield LoginPage(page_init).open(envs.auth_url)

@pytest.fixture()
def spending_page(page_init, auth, envs):
    yield SpendingPage(page_init).open(url=f"{envs.frontend_url}/spending")

@pytest.fixture()
def main_page(page_init, auth):
    yield MainPage(page_init)

@pytest.fixture()
def profile_page(page_init, auth, envs):
    yield ProfilePage(page_init).open(url=f"{envs.frontend_url}/profile")