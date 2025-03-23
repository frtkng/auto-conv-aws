# AWS CDK: S3 + Lambda + API Gateway ファイル変換サンプル

AWS CDKを使い、S3にファイルをアップロードし、自動的にLambdaで変換後、別のS3バケットに保存する仕組みです。API Gatewayを利用して、一般ユーザーが簡単にcurlでファイルのアップロード・ダウンロードができます。

## 🧑‍💻 アーキテクチャ

```
[curl (ユーザー)]
   │（ファイルをHTTPでアップロード）
   ▼
[API Gateway → Lambda]
   │（S3に保存・変換処理を実行）
   ▼
[S3 (変換前)]
   │（Lambdaで変換）
   ▼
[S3 (変換後)]
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

## 🔧 注意事項

- 本構成はデモ用のため、本番利用時はセキュリティや権限設定を調整してください。
- 本プロジェクトのコードおよびドキュメントはChatGPTによって作成されました。

