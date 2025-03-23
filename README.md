# AWS CDK: S3 + Lambda + API Gateway ファイル変換サンプル

AWS CDKを使い、S3にファイルをアップロードし、自動的にLambdaで変換後、別のS3バケットに保存する仕組みです。API Gatewayを利用して、一般ユーザーが簡単にcurlでファイルのアップロード・ダウンロードができます。

## 🧑‍💻 アーキテクチャ

```
[curl (ユーザー)]
   │（HTTPリクエストでファイル送信）
   ▼
[API Gateway]
   │（HTTPリクエストをLambdaに渡す）
   ▼
[Lambda関数 (api_handler)]
   │（受け取ったファイルをS3に保存）
   ▼
[S3バケット（入力用）]
   │（新規ファイル保存のイベント通知でLambdaを起動）
   ▼
[Lambda関数 (converter_handler)]
   │（ファイルを変換）
   ▼
[S3バケット（出力用）]
   │（変換後のファイルを保存）
   ▼
[curl (ユーザー)]
   │（S3の署名付きURLでファイルをダウンロード）
```

## 🚀 できること

- curlでAPIにファイルを送信。
- LambdaがファイルをS3に保存後、変換を実行。
- 結果のダウンロードURLをcurlに返す。

## 🛠 構成

- **AWS CDK (Python)**
- **AWS Lambda (Python 3.11)**
- **Amazon API Gateway**
- **Amazon S3**

## 📁 プロジェクト構造

```
cdk/
├── app.py
├── cdk/
│   └── cdk_stack.py
├── lambda/
│   ├── converter/
│   │   └── handler.py
│   └── api/
│       └── handler.py
├── requirements.txt
└── .gitignore
```

## 🚩 デプロイ手順

### 前提
- AWS CLI & AWS CDK 設定済み

### 手順

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap aws://YOUR_AWS_ACCOUNT_ID/ap-northeast-1
cdk deploy
```

## ✅ 動作確認

1. curlでファイルアップロード

```bash
echo "Hello World" > hello.txt
curl -X POST --data-binary @hello.txt https://{API_ENDPOINT_URL}
```

レスポンス例:

```json
{"download_url": "https://s3..."}
```

2. curlで変換後ファイルをダウンロード

```bash
curl -o converted.txt "{download_url}"
```

### 複数ファイルをアップロードする場合

複数のファイルを順番にアップロードする場合は、以下のコマンドを実行します。

```bash
for file in hello1.txt hello2.txt hello3.txt
do
    curl -X POST --data-binary @"$file" https://{API_ENDPOINT_URL}
done
```

各リクエストごとに個別のダウンロードリンクが返されます。

## 🔧 注意事項

- AWS Lambdaの最大実行時間は15分のため、それを超える処理は強制終了されます。長時間の処理が必要な場合は、AWS BatchやAWS Fargateなどの利用を検討してください。
- S3へのアクセス権限不足によりLambdaが正常に動作しない場合があります。Lambdaの権限設定を確認してください。
- API Gatewayはデフォルトで最大10MBのリクエストサイズに制限されており、これを超えるファイルはアップロードできません。
- Lambdaのメモリ割り当てが不十分な場合、メモリ不足によるエラーが発生する可能性があります。
- Lambdaの同時実行数が制限を超えると、処理が遅延またはエラーになる可能性があります（デフォルトの同時実行数は1000）。
- 本プロジェクトのコードおよびドキュメントはChatGPTによって作成されました。

