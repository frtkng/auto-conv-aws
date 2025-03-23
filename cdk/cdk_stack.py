from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    Duration,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 入力用S3バケット
        input_bucket = s3.Bucket(self, "InputBucket")

        # 出力用S3バケット
        output_bucket = s3.Bucket(self, "OutputBucket")

        # Lambda関数定義
        lambda_function = _lambda.Function(
            self, "ConverterFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.minutes(5),
            environment={
                "OUTPUT_BUCKET": output_bucket.bucket_name
            }
        )

        # 入力バケットのイベント通知設定
        input_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(lambda_function)
        )

        # Lambdaに権限を付与（S3アクセス）
        input_bucket.grant_read(lambda_function)
        output_bucket.grant_put(lambda_function)
