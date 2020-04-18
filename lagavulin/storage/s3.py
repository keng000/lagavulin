import warnings

import boto3

from .storage import Storage


class S3(Storage):
    def __init__(self, dsn: str):
        """
        Args:
            dsn: bucket name
        """
        # ignore known warning of ssl socket
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.dsn = dsn

    def read(self, path: str) -> bytes:
        sess = self.__create_session()

        try:
            s3_object = sess.get_object(Bucket=self.dsn, Key=path)
        except sess.exceptions.NoSuchBucket as e:
            raise FileNotFoundError(f"Bucket not found: dsn={self.dsn}, path={path}") from e
        except sess.exceptions.NoSuchKey as e:
            raise FileNotFoundError(f"dsn={self.dsn}, path={path}") from e

        body = s3_object["Body"].read()
        return body

    def write(self, path: str, data: bytes) -> None:
        sess = self.__create_session()
        sess.put_object(Bucket=self.dsn, Key=path, Body=data)

    @staticmethod
    def __create_session():
        return boto3.client("s3")
