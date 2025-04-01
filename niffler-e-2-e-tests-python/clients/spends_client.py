from urllib.parse import urljoin

import requests

class SpendHttpClient:

    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def get_categories(self) -> dict:
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        response.raise_for_status()
        return response.json()

    def get_spends(self) -> dict:
        response = self.session.get(urljoin(self.base_url, "/api/spends/all"))
        response.raise_for_status()
        return response.json()

    def add_category(self, category_name: str) -> dict:
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={
            'name': category_name
        })
        response.raise_for_status()
        return response.json()

    def update_category(self, body: dict) -> dict:
        response = self.session.patch(urljoin(self.base_url, "/api/categories/add"), json=body)
        response.raise_for_status()
        return response.json()

    def add_spends(self, body: dict) -> dict:
        url = urljoin(self.base_url, "/api/spends/add")
        response = self.session.post(url, json=body)
        response.raise_for_status()
        return response.json()

    def update_spends(self, body: dict) -> dict:
        url = urljoin(self.base_url, "/api/spends/edit")
        response = self.session.patch(url, json=body)
        response.raise_for_status()
        return response.json()

    def remove_spends(self, ids: list[str]):
        url = urljoin(self.base_url, "/api/spends/remove")
        response = self.session.delete(url, params={"ids": ids})
        response.raise_for_status()
