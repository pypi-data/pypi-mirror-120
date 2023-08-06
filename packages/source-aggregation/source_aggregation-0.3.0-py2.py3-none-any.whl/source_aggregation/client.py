import logging
import typing
import uuid
from os.path import join

import requests

from .utils import to_json

ArtifactId = typing.Union[int, str]


class ApiClient:
    resources = {}

    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._token = token

    def __getattr__(self, name):
        return self.__class__.resources[name](self._endpoint, self._token)


class _BaseClient:
    """
    Client that exposes required source aggregation service endpoints

    Adds logging and tracing of requests and responses in debug mode. Raises on errors during request.
    """

    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._token = token

    def __init_subclass__(cls, /, resource_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        ApiClient.resources[resource_name] = cls

    def exec_request(self, method, url, **kwargs):
        """ Executes a request, assigning a unique id beforehand and throwing on 4xx / 5xx """
        reqid = str(uuid.uuid4())

        logging.debug(
            f"{self.__class__.__qualname__} -> {method.upper()} {url} {reqid=}"
        )

        # requests.post / requests.get / ...
        method_exec = getattr(requests, method.lower())

        headers = self._build_headers()
        response = method_exec(url, headers=headers, **kwargs)

        status_code = response.status_code
        content_length = len(response.content or "")
        logging.debug(
            f"{self.__class__.__qualname__} <- {status_code} {content_length} {reqid=}"
        )

        # raise by default to halt further exec and bubble
        response.raise_for_status()

        return to_json(response)

    def build_url(self, *paths):
        return join(self._endpoint, *paths)

    def _build_headers(self):
        return {
            "Accept": "application/json",
            "User-Agent": "SAS Python package",
            "Authorization": f"Bearer {self._token}",
        }


class Sources(_BaseClient, resource_name="sources"):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("source"),
            params=(params or {}),
        )
        return response or {}

    def get(self, source_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"source/{source_id}"),
        )
        return response or {}

    def create(self, source_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST", url=self.build_url("source"), json=source_kwargs
        )
        return response or {}

    def update(self, source_id: str, source_kwargs: dict) -> dict:
        response = self.exec_request(
            method="PUT", url=self.build_url(f"source/{source_id}"), json=source_kwargs
        )
        return response or {}


class Artifacts(_BaseClient, resource_name="artifacts"):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("artifact"),
            params=(params or {}),
        )
        return response or {}

    def get(self, artifact_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"artifact/{artifact_id}"),
        )
        return response or {}

    def create(self, source_id: str, artifact_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"source/{source_id}/artifact"),
            json=artifact_kwargs,
        )
        return response or {}

    def update(self, artifact_id: str, artifact_kwargs: dict) -> dict:
        response = self.exec_request(
            method="PUT",
            url=self.build_url(f"artifact/{artifact_id}"),
            json=artifact_kwargs,
        )
        return response or {}

    def export(self, artifacts) -> list:
        ids = ",".join(str(artifact.get("id")) for artifact in artifacts)
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"artifact/{ids}/export"),
        )
        return response.get("id") or []

    def ignore(self, artifacts) -> list:
        ids = ",".join(str(artifact.get("id")) for artifact in artifacts)
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"artifact/{ids}/ignore"),
        )
        return response.get("id") or []


class Labels(_BaseClient, resource_name="labels"):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("label"),
            params=(params or {}),
        )
        return response or {}

    def get(self, label_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"label/{label_id}"),
        )
        return response or {}

    def create(self, label_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST", url=self.build_url("label"), json=label_kwargs
        )
        return response or {}

    def update(self, label_id: str, label_kwargs: dict) -> dict:
        response = self.exec_request(
            method="PUT", url=self.build_url(f"label/{label_id}"), json=label_kwargs
        )
        return response or {}

    def delete(self, label_id: str) -> dict:
        response = self.exec_request(
            method="DELETE", url=self.build_url(f"label/{label_id}")
        )
        return response or {}


class Categories(_BaseClient, resource_name="categories"):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("category"),
            params=(params or {}),
        )
        return response or {}

    def get(self, category_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"category/{category_id}"),
        )
        return response or {}

    def create(self, category_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST", url=self.build_url("category"), json=category_kwargs
        )
        return response or {}

    def update(self, category_id: str, category_kwargs: dict) -> dict:
        response = self.exec_request(
            method="PUT",
            url=self.build_url(f"category/{category_id}"),
            json=category_kwargs,
        )
        return response or {}

    def delete(self, category_id: str) -> dict:
        response = self.exec_request(
            method="DELETE", url=self.build_url(f"category/{category_id}")
        )
        return response or {}
