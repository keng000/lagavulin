import boto3


def load_config():
    return {'aws_access_key_id': None, 'aws_secret_access_key': None}


def create_s3_session():
    config = load_config()
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'])
    return s3


def download_file_from_s3(file_path_in_s3, download_path, session=None, do_retry=False):
    if session is None:
        session = create_s3_session()

    try:
        session.download_file('streamed', file_path_in_s3, download_path)

    except ClientError as e:
        # Reference: https://github.com/awsdocs/aws-doc-sdk-examples/blob/master/python/example_code/s3/s3-python-example-download-file.py

        if e.response['Error']['Code'] == "404":
            msg = f"The s3 file does not exists: {file_path_in_s3}"
            print(msg)
            raise KeyError(msg)

        if do_retry:
            download_file_from_s3(file_path_in_s3, download_path, do_retry=False)

        print(f"The s3 file failed to download: {file_path_in_s3}")
