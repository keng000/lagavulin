import google
from google.cloud import storage

from .storage import Storage


class GCS(Storage):
    def __init__(self, dsn: str):
        """
        Args:
            dsn: bucket name
        """
        self.dsn = dsn

    def read(self, path: str) -> bytes:
        sess = self.__create_session()
        try:
            bucket = sess.get_bucket(self.dsn)
        except google.cloud.exceptions.NotFound as e:
            raise FileNotFoundError(f"Bucket not found: dsn={self.dsn}") from e

        blob = bucket.get_blob(path)
        if not blob:
            raise FileNotFoundError(f"dsn={self.dsn}, path={path}")

        return blob.download_as_string(raw_download=True)

    def write(self, path: str, data: bytes) -> None:
        sess = self.__create_session()
        try:
            bucket = sess.get_bucket(self.dsn)
        except google.cloud.exceptions.NotFound as e:
            raise FileNotFoundError(f"Bucket not found: dsn={self.dsn}") from e

        bucket.blob(path).upload_from_string(data)

    @staticmethod
    def __create_session():
        return storage.Client()
