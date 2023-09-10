# Discord_TiDD
Discordを使ったチケット駆動開発のためのツール
Discord上でチケットを発行し、チケット駆動開発をサポートします。

## Requirements
 - Python 3.11.3
 - Discord.py 2.3.2

## Setup
1. リポジトリをクローンする:
    `git clone https://github.com/smoothie1023/Discord_TiDD.git`
2. 必要な依存関係をインストールする: `pip install -r requirements.txt`
3. ルートディレクトリにDiscordIDsフォルダーを作成する。
4. DiscordIDsフォルダーに以下のテキストファイルを作成する。
    1. token.txt: Discord Botのトークンを記述する。
    2. channel_id.txt: TiDDに使用したいチャンネルのチャンネルIDを記述する。
    3. guild_id.txt: TiDDで使用したいサーバーのギルドIDを記述する。
5. Run: `python main.py`
## Usage
Command prefix: `/`

コマンドのオプションであることを明確にするために`--`を先頭につけていますが、実際は不要です。

例では、分かりやすくするためにオプションの引数を［］で囲んでいます。

1. /チケット発行
    1. Option:
        - `--title`: チケットのタイトル (str)
        - `--tracker`: トラッカー［バグ、機能追加、仕様変更、サポート］
        - `--priority`: 優先度［高、通常、低］
        - `--description`: チケットの説明 (str)
    3. Example: `/チケット発行［チケットのタイトル］［バグ］［高］［これはテストチケットです。］`
    4. Note:チケット番号は自動的に連番で発行され、json形式で保存されます。
2. /チケット更新
    1. Option:
        - `--ticket_id`: チケットID (int)
       Non-required option:
        - `--status`: チケットステータス［新規、処理中、完了］
        - `--progressrate`: 進捗率 (int)
    3. Example: `/チケット更新［00001］［完了］［100］`
    4. Note: 進捗率を100％に設定しても、自動的にチケットステータスは完了になりません。
3. /チケット編集
    1. Option:
        - `--ticket_id`: チケットID (int)
       Non-required option:
        - `--title`: チケットのタイトル (str)
        - `--tracker`: トラッカー［バグ、機能追加、仕様変更、サポート］
        - `--priority`: 優先度［高、通常、低］
        - `--description`: チケットの説明 (str)
    3. Example: `/チケット編集［00001］［チケットのタイトル］［バグ］［高］［これは編集テストチケットです。］`
4. /チケット一覧
    1. Non-required option:
        - `--status`: チケットステータス［新規、処理中、完了］
        - `--tracker`: トラッカー［バグ、機能追加、仕様変更、サポート］
        - `--priority`: 優先度［高、通常、低］
    3. Example: `/チケット一覧［完了］［バグ］［高］`
