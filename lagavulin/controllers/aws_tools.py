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

    # boto3はスレッドセーフではないため、各スレッド内でセッションを生成する必要がある。
    # その時、スレッド内でセッション生成に失敗する事例があるため、セッションが生成できるまでトライする。
    # https://github.com/boto/boto3/issues/454
    while session is None:
        try:
            session = create_s3_session()
        except:
            session = None

    try:
        session.download_file('streamed', file_path_in_s3, download_path)

    except ClientError as e:
        # Reference: https://github.com/awsdocs/aws-doc-sdk-examples/blob/master/python/example_code/s3/s3-python-example-download-file.py

        if e.response['Error']['Code'] == "404":
            msg = f"The s3 file does not exists: {file_path_in_s3}"
            print_log(msg)

        if do_retry:
            download_file_from_s3(file_path_in_s3, download_path, do_retry=False)

        print_log(f"The s3 file failed to download: {file_path_in_s3}")


def download_with_property_list(dp):
    """
    ひとつのDownloadPropertyに対してダウンロード処理を行う.
    :param dp: 
        namedtuple('DownloadProperty', ['s3_path', 'save_path'])
        s3_path: ダウンロードするS3のパス.
        save_path: ダウンロード先となるローカルのパス.
    """
    download_file_from_s3(dp.s3_path, dp.save_path)


def concurrent_downloading(download_property_list):
    """
    :param download_property_list: 
        DownloadPropertyのリスト. 
        DownloadPropertyについては download_with_property_list() へ.
    """
    # (論理的に)搭載されたコア数＊５スレッドでダウンロードをconcurrent化
    with ThreadPoolExecutor() as executor:
        result = executor.map(download_with_property_list, download_property_list)

        # 完了したものから完了通知。完了するものが出てくるまでresultにはwaitがかかる。
        for idx, _ in enumerate(result):
            print(f"{idx+1}/{len(download_property_list)}")

    print_log("Download Done")
