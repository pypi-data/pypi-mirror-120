import logging
import os
import json
import requests

SERVICE_CATALOG = json.loads(os.getenv("SERVICE_CATALOG", "{}"))


def get_service_account_metadata(field, params=None):
    url = (
        "http://metadata.google.internal"
        f"/computeMetadata/v1/instance/service-accounts/default/{field}"
    )
    return requests.get(
        url=url, headers={"Metadata-Flavor": "Google"}, params=params
    ).content.decode()


def get_service_url(service_name, service_path=None):
    url = SERVICE_CATALOG.get(service_name)
    if not url:
        raise Exception(f"Service '{service_name}' not found in catalog.")
    if service_path:
        url += f"/{service_path}"
    return url


def call(service_name, service_path=None, **kwargs):
    url = get_service_url(service_name, service_path)
    headers = None
    if not os.getenv("LOCAL"):
        token = get_service_account_metadata("identity", {"audience": url})
        headers = {"Authorization": "Bearer " + token}
    r = requests.post(url, headers=headers, json=kwargs)
    if r.status_code >= 500:
        r.raise_for_status()
    return r
