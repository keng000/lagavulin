from pathlib import Path

from .storage import Storage


class FileSystem(Storage):
    def __init__(self, dsn: str):
        """
        Args:
            dsn: absolute path to dir
        """
        self.dsn = Path(dsn)

    def read(self, path: str) -> bytes:
        filepath = self.dsn / path
        if not filepath.exists():
            raise FileNotFoundError(f"dsn: {self.dsn}, path: {path}")

        with filepath.open("rb") as f:
            return f.read()

    def write(self, path: str, data: bytes) -> None:
        filepath = self.dsn / path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open("wb") as f:
            f.write(data)
