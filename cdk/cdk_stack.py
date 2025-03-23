from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_apigateway as apigw,
    Duration,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3バケット（入力）
        input_bucket = s3.Bucket(self, "InputBucket")

        # S3バケット（出力）
        output_bucket = s3.Bucket(self, "OutputBucket")

        # コンバーターLambda関数
        converter_lambda = _lambda.Function(
            self, "ConverterFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda/converter"),
            timeout=Duration.minutes(5),
            environment={
                "OUTPUT_BUCKET": output_bucket.bucket_name
            }
        )

        input_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(converter_lambda)
        )

        input_bucket.grant_read(converter_lambda)
        output_bucket.grant_put(converter_lambda)

        # API Gateway用Lambda関数
        api_lambda = _lambda.Function(
            self, "ApiHandler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda/api"),
            timeout=Duration.minutes(5),
            environment={
                "INPUT_BUCKET": input_bucket.bucket_name,
                "OUTPUT_BUCKET": output_bucket.bucket_name
            }
        )

        input_bucket.grant_put(api_lambda)
        output_bucket.grant_read(api_lambda)

        # API Gateway設定
        api = apigw.LambdaRestApi(
            self, "FileConverterApi",
            handler=api_lambda,
            proxy=True
        )
