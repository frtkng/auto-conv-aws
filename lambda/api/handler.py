import boto3
import os
import uuid
import json

s3 = boto3.client('s3')
INPUT_BUCKET = os.environ['INPUT_BUCKET']
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']

def lambda_handler(event, context):
    method = event['httpMethod']

    if method == 'POST':
        # API Gatewayから直接テキストデータを受け取る
        file_content = event['body']
        
        # curlで送った場合にJSONでない場合があるため、文字列をそのままバイトに変換
        if file_content is None:
            return {'statusCode': 400, 'body': 'No file content found'}

        file_content = file_content.encode('utf-8')
        
        file_name = f"{uuid.uuid4()}.txt"

        # ファイルをS3にアップロード
        s3.put_object(Bucket=INPUT_BUCKET, Key=file_name, Body=file_content)

        converted_file_name = f"converted-{file_name}"

        # コンバート結果用の署名付きURLを生成
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': OUTPUT_BUCKET, 'Key': converted_file_name},
            ExpiresIn=3600
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'download_url': url})
        }

    return {'statusCode': 400, 'body': 'Invalid request'}
