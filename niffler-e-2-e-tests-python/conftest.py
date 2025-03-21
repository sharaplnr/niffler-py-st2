import os

import pytest
from playwright.sync_api import Playwright
from dotenv import load_dotenv
from faker import Faker

from pages.base_page import BasePage
from pages.login_page.login_page import LoginPage
from pages.main_page.main_page import MainPage
from pages.profile_page.profile_page import ProfilePage
from pages.spending_page.spending_page import SpendingPage
from clients.spends_client import SpendHttpClient


fake = Faker()


@pytest.fixture(scope="session", autouse=True)
def envs():
    load_dotenv()

@pytest.fixture(scope="session")
def page_init(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()

@pytest.fixture(scope="session")
def app_user():
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")

@pytest.fixture(scope="session")
def frontend_url():
    return os.getenv("FRONTEND_URL")

@pytest.fixture(scope="session")
def auth_url():
    return os.getenv("AUTH_URL")

@pytest.fixture(scope="session")
def gateway_url():
    return os.getenv("GATEWAY_URL")

@pytest.fixture(scope="session")
def auth(login_page: LoginPage, app_user):
    username, password = app_user
    login_page.login_with_valid_credentials(username, password)
    token = login_page.page.evaluate(expression='window.localStorage.getItem("id_token")')

    if token is None:
        raise ValueError("Token not found in localStorage")

    yield token

@pytest.fixture(scope="session")
def spends_client(gateway_url, auth) -> SpendHttpClient:
    return SpendHttpClient(gateway_url, auth)

@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["name"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)

    return category_name

@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["name"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)

    return category_name

@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    current_spends = spends_client.get_spends()
    spends_ids = [spend["id"] for spend in current_spends]
    if spend["id"] in spends_ids:
        spends_client.remove_spends([spend["id"]])


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

# @pytest.fixture()
# def random_category_name():
#     return fake.word()

@pytest.fixture()
def base_page(page_init):
    yield BasePage(page_init)

@pytest.fixture(scope="session")
def login_page(page_init, auth_url):
    LoginPage(page_init).open(auth_url)
    yield LoginPage(page_init).open(auth_url)

@pytest.fixture()
def spending_page(page_init, auth, frontend_url):
    yield SpendingPage(page_init).open(url=f"{frontend_url}/spending")

@pytest.fixture()
def main_page(page_init, auth):
    yield MainPage(page_init)

@pytest.fixture()
def profile_page(page_init, auth, frontend_url):
    yield ProfilePage(page_init).open(url=f"{frontend_url}/profile")