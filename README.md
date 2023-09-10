# Discord_TiDD
Tools for Ticket-Driven Development with Discord
Support development by issuing tickets on Discord, like ticket-driven development.

## Requirements
 - Python 3.11.3
 - Discord.py 2.3.2

## Setup
1. Clone the repository:
    `git clone https://github.com/smoothie1023/Discord_TiDD.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create a DiscordIDs folder in the root directory
4. Create a text file in the DiscordIDs folder
    1. token.txt: Your Discord bot token
    2. channel_id.txt: The channel ID of the channel you want to use for TiDD
    3. guild_id.txt: The guild ID of the server you want to use for TiDD
5. Run the bot: `python main.py`
## Usage
Command prefix: `/`
The `--` is prefixed to make it clear that it is an option, but in fact you can use Discord's auto-completion.
In the example, optional arguments are enclosed in［］for clarity.

1. /チケット発行
    1. Option: `--title`: Ticket title (str) `--tracker`: Tracker［バグ、機能追加、仕様変更、サポート］
               `--priority`: Priority［高、通常、低］`--description`: Ticket description (str)
    2. Example: `/チケット発行［Ticket Title］［バグ］［高］［This is a test ticket.］`
    3. The ticket numbers are automatically sequentially issued and stored in json.
2. /チケット更新
    1. Option: `--ticket_id`: Ticket id (int)
       Non-required option: `--status`: Ticket status［新規、処理中、完了］`--progressrate`: Progress rate (int)
    2. Example: `/チケット更新［00001］［完了］［100］`
    3. Note: Even if the progress rate is set to 100%, it will not be completed automatically.
3. /チケット編集
    1. Option: `--ticket_id`: Ticket id (int)
       Non-required option: `--title`: Ticket title (str) `--tracker`: Tracker［バグ、機能追加、仕様変更、サポート］
         `--priority`: Priority［高、通常、低］`--description`: Ticket description (str)
    2. Example: `/チケット編集［00001］［Ticket Title］［バグ］［高］［This is a test edit ticket.］`
4. /チケット一覧
    1. Non-required option: `--status`: Ticket status［新規、処理中、完了］`--tracker`: Tracker［バグ、機能追加、仕様変更、サポート］`--priority`: Priority［高、通常、低］
    2. Example: `/チケット一覧［完了］［バグ］［高］`