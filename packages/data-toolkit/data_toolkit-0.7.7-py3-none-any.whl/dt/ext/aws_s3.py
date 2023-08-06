'''
Operations to speed up S3 access.
'''

def get_lastest_file(dongle_id: str):
    """
    Get the lastest file in the bucket.
    """
    import boto3
    import pandas as pd

    bucket = 'creationlabs-raw-data'

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, dongle_id)
    files = obj.meta.client.list_objects(Bucket=bucket, Prefix=dongle_id)
    df = pd.DataFrame(files['Contents'])
    last_file = df.sort_values('LastModified',ascending=False).iloc[0]
    last_segment = '/'.join(last_file['Key'].split('/')[:-1])
    ret = f"s3://creationablas-raw-data/{last_segment}"
    return ret

def get_latest_bucket(target, bucket_name: str = 'creationlabs-raw-data'):
    # TODO: profile
    # get all dongle ids
    import boto3 
    import pandas as pd
    import humanize

    pd.set_option('display.max_colwidth',70)
    
    s3 = boto3.session.Session(region_name='eu-west-1').client('s3')

    raw_data_buckets = s3.list_objects_v2(Bucket='creationlabs-raw-data',Delimiter='/')
    dongle_ids = [x['Prefix'].split('/')[0] for x in raw_data_buckets['CommonPrefixes']]

    latest_files = []

    for did in dongle_ids:
        latest_files.append(get_lastest_file(did))

    df = pd.DataFrame(latest_files, columns=['file'])
    df['dongle_id'] = dongle_ids

    # remove dongles with no drives
    df = df.loc[df['file'].str.contains('--')]

    df['upload_time'] =  df.file.str.split('/').str[-1].str.split('--').str[0:2].str.join('--')
    df['upload_time'] = pd.to_datetime(df.upload_time, format='%Y-%m-%d--%H-%M-%S')

    # get naturaltime from now to the time of the latest file
    df['time'] = df['upload_time'].apply(lambda x: humanize.naturaldelta(x))
    print(df)

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
    print(f"Running {cmd}")
    os.system(cmd)