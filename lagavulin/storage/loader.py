from pathlib import Path
from urllib.parse import urlparse

from .storage import Storage


def new_storage(furi: str) -> Storage:
    p = urlparse(furi)
    if p.scheme == "file":
        pass

    elif p.scheme == "s3":
        pass

    elif p.scheme == "gcs":
        pass

    else:
        raise RuntimeError(f'invalid scheme: "{furi}"')
