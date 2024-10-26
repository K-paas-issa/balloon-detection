import boto3
import os

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = os.getenv('NCP_ACCESSKEY')
secret_key = os.getenv('NCP_SECRETKEY')

def download_csv(object_name):
    print('download_csv start, data-path : ', object_name)
    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    bucket_name = 'contest73-bucket'

    local_file_path = 'image.' + extract_extension(object_name)
    try:
        s3.download_file(bucket_name, object_name, local_file_path)
        return local_file_path
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # 예외 메시지 출력
        return 'exception throws'
    
def extract_extension(image_path):
    image_name = os.path.basename(image_path)
    image_split = image_name.split('.')
    return image_split[-1] # 확장자 추출