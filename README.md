# AWS Chalice を用いて、翻訳 LINE Bot をサーバレスアーキテクチャで作る！
![動画画面10秒gif_320](https://user-images.githubusercontent.com/40209684/112859077-746ecf00-90ed-11eb-87cc-165ae63d9d4b.GIF)  
<img a="https://youtu.be/Rj2vbdTWr0o" src="https://user-images.githubusercontent.com/40209684/112913068-ebc75180-9133-11eb-855d-790289e370fd.png" width="100"> に動作画面の録画をアップロード済

## 本リポジトリについて
- 日本語や中国語でメッセージを送信すると、**英語に翻訳をして返信してくれる LINE Bot** を開発します。
- インターネット上では、PaaS である Heroku を用いておうむ返しをするチュートリアル記事が多く公開されていますが、今回は AWS Lambda と API Gateway を用いた **サーバレスアーキテクチャ** で構築します。
- また、AWS Chalice という Python のフレームワークを用いることで、Lambda と API Gateway の構成をコードとして管理・デプロイします。

## AWS Chalice について
- AWS Chalice とは、AWS が OSS として開発・提供している、Python を用いたサーバレスフレームワークです。
- API Gateway と Lambda を用いた API を簡単に構築することができます。
- ファーストステップとしては、AWS 公式の以下のハンズオンを実施することをおすすめします。
    - [AWS 怠惰なプログラマ向けお手軽アプリ開発手法 2019](https://feature-ai-service.dma9ecr5ksxts.amplifyapp.com/chalice/)

## LINE Bot デプロイ手順

### 前提条件
- PC に Git, Python, pip が入っていること。
- AWS CLI が設定済であること。  
  - AWS CLI の設定方法については[こちら](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html)。

### python と pip が同じバージョンを向いていることを確認します。
```shell
$ python -V
Python 3.7.9
$ pip -V
pip 9.0.3 from /usr/lib/python3.7/site-packages (python 3.7)
```

### 必要に応じて仮想環境を作成・利用します。
```shell
$ pip install virtualenv
$ virtualenv ~/.virtualenvs/chaliceenv
$ source ~/.virtualenvs/chaliceenv/bin/activate
```

### 必要なパッケージをインストールします。
```shell
$ pip install chalice
$ pip install boto3
$ pip install line-bot-sdk
```

### 本リポジトリからソースコードをクローンします。
```shell
$ git clone https://github.com/cloud8high/linebot-translation-chalice.git
```

### LINE Developers で Messaging API を利用できるようにします。
- [公式ドキュメント](https://developers.line.biz/ja/docs/messaging-api/getting-started/#using-console)の手順に沿い、「プロバイダー」と「チャネル」を作ります。
  - LINE Developers の画面右下で言語を「日本語」に切り替えることができます。
  - （参考）作成したプロバイダーとチャネルは、スマホの LINE アプリでは以下のように表示されます。
  - <img src="https://user-images.githubusercontent.com/40209684/112856675-01645900-90eb-11eb-8b2e-76ff01036a5e.png" width="300">
- 「チャネルアクセストークン」と「チャネルシークレット」を発行・メモします。
  - どちらも、[LINE Developersコンソール](https://developers.line.biz/console/) で確認できます。
  - [長期のチャネルアクセストークン](https://developers.line.biz/ja/docs/messaging-api/channel-access-tokens/#long-lived-channel-access-tokens) は、`LINE Developers トップ > プロバイダー選択 > チャネル選択 > 「Messaging API設定」タブ` 画面下部のボタンから発行
  - [チャネルシークレット](https://developers.line.biz/ja/glossary/#channel-secret) は、`LINE Developers トップ > プロバイダー選択 > チャネル選択 > 「チャネル基本設定」タブ` から確認
- ボットとして動かすために、「応答メッセージ」の設定を無効にします。
  - `LINE Developers トップ > プロバイダー選択 > チャネル選択 > 「Messaging API設定」タブ`で設定可能。
  - 「応答モード」の選択画面が出た場合は「Bot」のままにする。「チャット」に変更はしない。
- スマホの LINE アプリから、今回作成したチャネルと友達になります。
  - QRコードは、`LINE Developers トップ > プロバイダー選択 > チャネル選択 > 「Messaging API設定」タブ` にあります。

### chalice の config.json ファイルを設定します。
- 上記手順でメモした「チャネルアクセストークン」と「チャネルシークレット」を`.chalice/config.json` の `CHANNEL_ACCESS_TOKEN` と `CHANNEL_SECRET_TOKEN` に上書きします。

### chaliice deploy コマンドで、APIを作成します。
```shell
$ cd linebot-translation-chalice/
$ chalice deployCreating deployment package.
Updating policy for IAM role: linebot-translation-dev-api_handler
Updating lambda function: linebot-translation-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:ap-northeast-1:XXXXXXXXXXXX:function:linebot-translation-dev
  - Rest API URL: https://XXXXXXXXXX.execute-api.ap-northeast-1.amazonaws.com/dev/
```
デプロイが正常に終了した場合、上記の`Rest API URL`	がAPIのURLとなります。

### Webhook URL の確認
- 今回の app.py ファイルでは、翻訳処理を `/translation` のパスで設定しています。
- そのため、chalice deploy コマンド後に表示された API の URL の末尾に /translation をつけたものが、翻訳ボットを呼び出す Webhook URL となります。  
  - 例：https://XXXXXXXXXX.execute-api.ap-northeast-1.amazonaws.com/api/translation

### 「チャネル」に Webhook URL を登録する
- `LINE Developers トップ > プロバイダー選択 > チャネル選択 > 「Messaging API設定」タブ` を開きます。
- `Webhook URL` の項目にて、上記手順で確認した Webhook URL を入力します。
- `Use webhook` のトグルスイッチを有効にします。

## 動作確認
- LINE アプリから、作成したチャネルにメッセージを送ってみてください。
- 英語に翻訳されて返信が帰ってくるはずです。
- 送信したメッセージは、自動で言語解析がされるため、日本語以外でも英語へ翻訳できます。
  - ※ Amazon Translate の[サポートしている言語](https://docs.aws.amazon.com/translate/latest/dg/what-is.html)に限ります。

## ライセンス
- [MIT](https://github.com/cloud8high/linebot-translation-chalice/blob/main/LICENSE)

## 作成者について
- [Qiita](https://qiita.com/hayate_h)
- [Twitter](https://twitter.com/cloud8high)
- [GitHub](https://github.com/cloud8high)

## 参考資料等
- [GitHub - line/line-bot-sdk-python: LINE Messaging API SDK for Python](https://github.com/line/line-bot-sdk-python)
- [Messaging API | LINE Developers](https://developers.line.biz/ja/docs/messaging-api/)


## 個人備忘録
### 公開時に注意するファイル
以下ファイルはプロジェクト固有の情報を含む可能性があるので、公開前に必ず確認。
```
.chalice/config.json
.chalice/deployed/dev.json
.gitignore
```

### profile を指定した chalice deploy コマンドについて
プロファイルを指定してデプロイする場合、リージョン情報を求められることがある。
```shell
$ export AWS_DEFAULT_REGION=ap-northeast-1
$ chalice deploy --profile $PROFILE_NAME
```