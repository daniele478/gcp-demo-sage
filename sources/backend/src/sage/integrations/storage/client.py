"""Cloud Storage client factory."""

from functools import lru_cache

from google.cloud import storage

from sage.config import get_app_config


@lru_cache
def get_storage_client() -> storage.Client:
    return storage.Client(project=get_app_config().project_id)
