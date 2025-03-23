import boto3
import os

s3 = boto3.client('s3')
output_bucket = os.environ['OUTPUT_BUCKET']

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    input_file = f'/tmp/{os.path.basename(object_key)}'
    output_file = f'/tmp/converted-{os.path.basename(object_key)}'

    # 入力ファイルをS3からダウンロード
    s3.download_file(bucket_name, object_key, input_file)

    # 変換処理：Hello World → Hello Space
    with open(input_file, 'r') as f_in:
        content = f_in.read().replace("Hello World", "Hello Space")

    # 出力ファイルを作成
    with open(output_file, 'w') as f_out:
        f_out.write(content)

    # 出力バケットにアップロード
    s3.upload_file(output_file, output_bucket, f'converted-{object_key}')

    return {'status': 'success'}
