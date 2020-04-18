from pathlib import Path
from urllib.parse import urlparse

from .file import FileSystem
from .gcs import GCS
from .s3 import S3
from .storage import Storage


"""
```python
if __name__ == '__main__':
    storage = new_storage(furi="s3://bucket")
    data: bytes = storage.read("file_path")
    print(data.decode())

    storage = new_storage(furi="file:///path/to/dir")
    data: bytes = storage.read("file_path")
    print(data.decode())

    storage = new_storage(furi="gcs://bucket")
    data: bytes = storage.read("file_path")
    print(data.decode())
```
"""


def new_storage(furi: str) -> Storage:
    p = urlparse(furi)
    if p.scheme == "file":
        dsn = Path(p.netloc) / p.path
        return FileSystem(str(dsn))

    elif p.scheme == "s3":
        return S3(p.netloc)

    elif p.scheme == "gcs":
        return GCS(p.netloc)

    else:
        raise RuntimeError(f'invalid scheme: "{furi}"')
