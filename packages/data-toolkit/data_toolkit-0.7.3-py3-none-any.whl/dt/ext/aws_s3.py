'''
Operations to speed up S3 access.
'''

def get_lastest_file(dongle_id: str):
    """
    Get the lastest file in the bucket.
    """
    import boto3

    bucket = 'creationlabs-raw-data'

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, dongle_id)
    files = obj.meta.client.list_objects(Bucket=bucket, Prefix=dongle_id)
    if 'Contents' in files:
        last_segment = '/'.join(files['Contents'][-1]['Key'].split('/')[:-1])
        ret = f"s3://creationablas-raw-data/{last_segment}"
        print(ret)
    return None


def download_latest(dongle_id):
    """
    Download the latest file in the bucket.
    """
    import boto3
    import os

    bucket = 'creationlabs-raw-data'
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, dongle_id)
    files = obj.meta.client.list_objects(Bucket=bucket, Prefix=dongle_id)
    last_segment = '/'.join(files['Contents'][-1]['Key'].split('/')[:-1])
    last_drive = '--'.join(last_segment.split('--')[:-1])
    cmd = f'aws s3 sync s3://{bucket}/{dongle_id} .  --exclude="*" --include="{last_drive}*"'
    # s3.meta.client.download_file(bucket, last_drive, dongle_id)
    print(f"Running {cmd}"
    os.system(cmd)