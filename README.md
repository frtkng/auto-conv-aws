# AWS CDK: S3 + Lambda + API Gateway ファイル変換サンプル

AWS CDKを使い、S3にファイルをアップロードし、自動的にLambdaで変換後、別のS3バケットに保存する仕組みです。API Gatewayを利用して、一般ユーザーが簡単にcurlでファイルのアップロード・ダウンロードができます。

## 🧑‍💻 アーキテクチャ（詳細）

```
[curl (ユーザー)]
   │（HTTPリクエストでファイル送信）
   ▼
[API Gateway]
   │（Lambda: api_handlerを呼び出す）
   ▼
[Lambda関数 (api_handler)]
   │① S3バケット（入力用）にファイル保存
   │② 署名付きURL（変換後ファイル用）を生成（この時点ではファイルは未作成）
   │③ 署名付きURLをAPI Gateway経由でユーザーに返す
   ▼
[S3バケット（入力用）]
   │（ファイル保存をトリガーにLambda関数 converter_handlerが起動）
   ▼
[Lambda関数 (converter_handler)]
   │① ファイルを変換処理
   │② 変換後のファイルをS3バケット（出力用）に保存
   ▼
[S3バケット（出力用）]
   │（ファイルが保存される）
   ▼
[curl (ユーザー)]
   │（事前に受け取ったURLを使い、ファイルをダウンロード）
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

## 🚩 AWS環境設定手順（未設定の場合）

AWS CLIとAWS CDKの環境設定が必要です。

### AWS CLIの設定

1. AWS CLIを[公式ページ](https://aws.amazon.com/jp/cli/)からインストール。
2. コマンドラインでAWS認証情報を設定します。

```bash
aws configure
```

AWS Access Key ID、Secret Access Key、デフォルトリージョン（ap-northeast-1）を入力します。

### AWS CDKの設定

AWS CDKをインストールします。

```bash
npm install -g aws-cdk
```

## 🚩 デプロイ手順

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
- curlでファイルをアップロードする際、AWSの仕様上の制限で、10MBを超えるファイルをAPI Gateway経由でLambdaに送信することはできません
- S3へのアクセス権限不足によりLambdaが正常に動作しない場合があります。Lambdaの権限設定を確認してください。
- API Gatewayはデフォルトで最大10MBのリクエストサイズに制限されており、これを超えるファイルはアップロードできません。
- Lambdaのメモリ割り当てが不十分な場合、メモリ不足によるエラーが発生する可能性があります。
- Lambdaの同時実行数が制限を超えると、処理が遅延またはエラーになる可能性があります（デフォルトの同時実行数は1000）。
- 本構成では、変換処理（converter\_handler）にエラーが発生した場合、ファイルが出力されず、事前に渡されたダウンロードURLが無効になる場合があります。エラー時の通知・対応方法を別途検討してください（AWS SNSによる通知など）。
- 本プロジェクトのコードおよびドキュメントの作成にはChatGPTが利用されています。
