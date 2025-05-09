from urllib.parse import urljoin

import requests

from models.api.spend import SpendRequest, SpendResponse
from models.api.category import CategoriesResponse, CategoryRequest


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

    def get_categories(self) -> list[CategoriesResponse]:
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        self.raise_for_status(response)
        return [CategoriesResponse.model_validate(item) for item in response.json()]

    def get_spends(self) -> list[SpendResponse]:
        response = self .session.get(urljoin(self.base_url, "/api/spends/all"))
        self.raise_for_status(response)
        return [SpendResponse.model_validate(item) for item in response.json()]

    def add_category(self, category_name: str) -> CategoriesResponse:
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={
            "name": category_name
        })
        self.raise_for_status(response)
        return CategoriesResponse.model_validate(response.json())

    def update_category(self, body: CategoryRequest) -> CategoriesResponse:
        response = self.session.patch(urljoin(self.base_url, "/api/categories/update"), json=body)
        self.raise_for_status(response)
        return CategoriesResponse.model_validate(response.json())

    def add_spends(self, spend: SpendRequest) -> SpendResponse:
        url = urljoin(self.base_url, "/api/spends/add")
        response = self.session.post(url, json=spend.model_dump())
        self.raise_for_status(response)
        return SpendResponse.model_validate(response.json())

    def update_spends(self, body: SpendRequest) -> SpendResponse:
        url = urljoin(self.base_url, "/api/spends/edit")
        response = self.session.patch(url, json=body.model_dump())
        self.raise_for_status(response)
        return SpendResponse.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        url = urljoin(self.base_url, "/api/spends/remove")
        response = self.session.delete(url, params={"ids": ids})
        self.raise_for_status(response)

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise