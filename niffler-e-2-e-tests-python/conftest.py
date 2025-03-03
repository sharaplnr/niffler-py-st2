import os

import pytest
from playwright.sync_api import Playwright
from dotenv import load_dotenv

from pages.base_page import BasePage
from pages.login_page.login_page import LoginPage
from pages.main_page.main_page import MainPage
from pages.profile_page.profile_page import ProfilePage


@pytest.fixture(scope="session", autouse=True)
def envs():
    load_dotenv()

@pytest.fixture()
def page_init(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


@pytest.fixture()
def base_page(page_init):
    yield BasePage(page_init)

@pytest.fixture()
def login_page(page_init):
    yield LoginPage(page_init).open(os.getenv("AUTH_URL"))

@pytest.fixture()
def main_page(page_init):
    yield MainPage(page_init).open(os.getenv("FRONTEND_URL"))

@pytest.fixture()
def profile_page(page_init):
    yield ProfilePage(page_init)