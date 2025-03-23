# AWS CDK: S3 → Lambda (Python) → S3 コンバーターサンプル

AWS CDKを使って、S3にアップロードしたテキストファイルをAWS Lambdaで自動的に変換し、別のS3バケットに保存するサンプルです。

## 🧑‍💻 アーキテクチャ

```
[S3 (Input)]
   │（ファイルをアップロード）
   ▼
[Lambda (Pythonで変換処理)]
   │（変換後ファイルをアップロード）
   ▼
[S3 (Output)]
```

## 🚀 できること

- 入力用S3バケットにテキストファイルを置くと、自動的にLambdaが起動。
- Lambda内のPythonスクリプトがテキストを変換（"Hello World" → "Hello Space"）。
- 変換した結果を出力用S3バケットに保存。

## 🛠 構成

- **AWS CDK (Python)**: インフラをコードで管理
- **AWS Lambda (Python 3.11)**: テキスト変換の実行環境
- **Amazon S3**: 入力/出力ファイル保存先

## 📁 プロジェクト構造

```
cdk/
├── app.py
├── cdk/
│   └── cdk_stack.py
├── lambda/
│   └── handler.py
├── requirements.txt
└── .gitignore
```

## 🚩 デプロイ手順

### 前提

- AWSアカウントおよびAWS CLI設定済み
- AWS CDKインストール済み

### 手順

1. 仮想環境を作成してCDKライブラリをインストール

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 初回のみBootstrapを実行

```bash
cdk bootstrap aws://YOUR_AWS_ACCOUNT_ID/ap-northeast-1
```

3. CDKデプロイ

```bash
cdk deploy
```

## ✅ 動作確認

1. AWSコンソールで、作成されたInputバケットに`hello.txt`をアップロード（内容は"Hello World"）。
2. Outputバケットに`converted-hello.txt`が生成され、内容が"Hello Space"に変換されていることを確認。

## 🔧 Lambdaの変換スクリプト修正方法

`lambda/handler.py`を編集して再度デプロイすれば、変換ロジックを変更可能です。

## 📝 注意事項

- これはプロトタイプ環境を想定した簡易構成です。プロダクション用途ではIAMロールや権限設定をより細かく調整してください。

