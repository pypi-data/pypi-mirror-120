import json
from collections import namedtuple
from datetime import datetime

import pydantic
import requests
from requests.auth import HTTPBasicAuth

from gcrc.utils import run

_AUTH_TOKEN: str = ""
ImageRow = namedtuple("ImageRow", ["name"])


class ImageTag(pydantic.BaseModel):
    digest: str
    name: str
    tags: list[str]
    timestamp: datetime

    @classmethod
    def pre_process(cls, data):
        return {
            "digest": data["digest"],
            "name": data["tags"][0],
            "tags": data["tags"],
            "timestamp": data["timestamp"]["datetime"],
        }


def get_auth_token() -> str:
    global _AUTH_TOKEN
    if not _AUTH_TOKEN:
        _AUTH_TOKEN = run(["gcloud", "auth" "print-access-token"]).stdout.decode(
            "utf-8"
        )

    return _AUTH_TOKEN


def list_images(repository: str) -> list[str]:
    cmd = [
        "gcloud",
        "container",
        "images",
        "list",
        "--format",
        "json",
        "--repository",
        repository,
    ]
    result = run(cmd)
    return [ImageRow(**row).name for row in json.loads(result.stdout)]


def list_tags(image: str) -> list[ImageTag]:
    cmd = ["gcloud", "container", "images", "list-tags", "--format", "json", image]
    result = run(cmd)
    return [ImageTag(**ImageTag.pre_process(row)) for row in json.loads(result.stdout)]


def delete_tag(image: str, tag: ImageTag):
    name = f"{image}@{tag.digest}"
    cmd = [
        "gcloud",
        "container",
        "images",
        "delete",
        "--quiet",
        "--force-delete-tags",
        name,
    ]
    run(cmd)


def delete_manifest(repository: str, image: str, tag: ImageTag):
    parts = repository.split("/", maxsplit=2)
    registry = parts[0]
    auth = HTTPBasicAuth("_token", get_auth_token())
    url = f"https://{registry}/v2/{image}/manifests/{tag.digest}"
    requests.delete(url, auth=auth)
