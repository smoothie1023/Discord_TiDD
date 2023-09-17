import discord
from discord import app_commands
from discord.ui import Select, View

#!/usr/bin/env python3
import os
import json
import datetime

from typing import Literal

#Constant Values=================================================
STATUS=["新規","進行中","リリース待ち","完了"]
TRACKER=["バグ","機能追加","仕様変更","サポート"]
PRIORITY=["高","通常","低"]
ROW_NUM=15

#Folder Path=====================================================
#Discord Bot Token and IDs
DiscordIDs_FolderPath="DiscordIDs/"

#Json File Path
Json_FolderPath="Json/"
Json_FileName="Tickets.json"

#Discord Bot Initialize===========================================
client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

#Load Discord IDs
with open(os.path.join(DiscordIDs_FolderPath,"token.txt")) as t, \
     open(os.path.join(DiscordIDs_FolderPath,"guild_id.txt")) as g, \
     open(os.path.join(DiscordIDs_FolderPath,"channel_id.txt")) as c:
        TOKEN = t.read()
        GUILD_ID = g.read()
        CHANNEL_ID = int(c.read())

        guild=discord.Object(GUILD_ID)

#Functions=======================================================
#Load Json File
def load_json():
    try:
        with open(os.path.join(Json_FolderPath,Json_FileName),encoding="utf-8") as f:
            json_data = json.load(f)
            ticket_num=len(json_data)
        return ticket_num,json_data
    except:
        return -1,""

#Save Json File
def save_json(json_data):
    with open(os.path.join(Json_FolderPath,Json_FileName), 'w',encoding="utf-8") as f:
        json.dump(json_data, f, indent=4,ensure_ascii=False)

#Check Json Folder and File
def check_json():
    if not os.path.exists(Json_FolderPath):
        os.mkdir(Json_FolderPath)

#Show Ticket Embed
def show_Ticket_embed(ticket_id):
    _,read_data=load_json()

    if read_data[ticket_id]["tracker"]==TRACKER[0]:
        color=0xff0000
    elif read_data[ticket_id]["tracker"]==TRACKER[1]:
        color=0xfff68f
    elif read_data[ticket_id]["tracker"]==TRACKER[2]:
        color=0x99c0ff
    elif read_data[ticket_id]["tracker"]==TRACKER[3]:
        color=0x99e394
    else:
        color=0x555555
    embed = discord.Embed(title=f"#{ticket_id} {read_data[ticket_id]['title']}",
                      description=f"{read_data[ticket_id]['description']}",
                      colour=color,
                      timestamp=datetime.datetime.now())
    embed.set_author(name="開発チケット")
    embed.add_field(name="ステータス",
                value=f"{read_data[ticket_id]['status']}",
                inline=False)
    embed.add_field(name="優先度",
                value=f"{read_data[ticket_id]['priority']}",
                inline=True)
    embed.add_field(name="進捗率",
                value=f"{read_data[ticket_id]['progressRate']}%",
                inline=True)
    embed.add_field(name="トラッカー",
                value=f"{read_data[ticket_id]['tracker']}",
                inline=True)
    embed.add_field(name="チケット発行日",
                value=f"{read_data[ticket_id]['createdDate']}",
                inline=False)

    embed.set_footer(text=f"チケット作成者:{read_data[ticket_id]['ticketCreator']}")
    return embed

#Discord Bot UI===================================================
#Discord Bot UI Ticket Search Option Panel
class TicketOptionPanel(discord.ui.View):
    def __init__(self, ctx:discord.Interaction):
        self.ctx=ctx
        super().__init__(timeout=50)
    
    @discord.ui.select(
        cls=Select,
        placeholder="検索オプション",
        min_values=1,
        max_values=11,
        options=[
            discord.SelectOption(label="すべて", value="すべて"),
            discord.SelectOption(label=STATUS[0], value=STATUS[0]),
            discord.SelectOption(label=STATUS[1], value=STATUS[1]),
            discord.SelectOption(label=STATUS[2], value=STATUS[2]),
            discord.SelectOption(label=STATUS[3], value=STATUS[3]),
            discord.SelectOption(label=TRACKER[0], value=TRACKER[0]),
            discord.SelectOption(label=TRACKER[1], value=TRACKER[1]),
            discord.SelectOption(label=TRACKER[2], value=TRACKER[2]),
            discord.SelectOption(label=TRACKER[3], value=TRACKER[3]),
            discord.SelectOption(label=PRIORITY[0], value=PRIORITY[0]),
            discord.SelectOption(label=PRIORITY[1], value=PRIORITY[1]),
            discord.SelectOption(label=PRIORITY[2], value=PRIORITY[2])
        ]
    )
    async def selectMenu(self, interaction: discord.Interaction, select: Select):
        await interaction.response.defer()
        ticket_num,read_data=load_json()
        if ticket_num==-1:
            embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
            await interaction.followup.send(embed=embed)
            return
        
        tracker_icons = [":red_square:" if read_data[f'{n:05d}']['tracker'] == TRACKER[0] else ":yellow_square:" if read_data[f'{n:05d}']['tracker'] == TRACKER[1] else ":blue_square:" if read_data[f'{n:05d}']['tracker'] == TRACKER[2] else ":green_square:" if read_data[f'{n:05d}']['tracker'] == TRACKER[3] else ":white_large_square:" for n in range(1,ticket_num+1)]

        # 検索条件を指定
        selected_status=[value for value in select.values if value in STATUS]
        selected_tracker=[value for value in select.values if value in TRACKER]
        selected_priority=[value for value in select.values if value in PRIORITY]

        filtered_data = {key: value for key, value in read_data.items() if
                 (not selected_status or value["status"] in selected_status) and
                 (not selected_tracker or value["tracker"] in selected_tracker) and
                 (not selected_priority or value["priority"] in selected_priority)}
        ticket_num=len(filtered_data)
        
        if ticket_num==0:
            embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
            await interaction.followup.send(embed=embed)
            return
        
        await interaction.followup.send(f"チケット一覧を表示します。")

        for i in range(0,(ticket_num+ROW_NUM)//ROW_NUM):
            embed=discord.Embed(title=f"チケット一覧[{i+1}/{(ticket_num+ROW_NUM-1)//(ROW_NUM)}]",color=0xffffff)
            for parent_key in list(filtered_data.keys())[i*ROW_NUM:ROW_NUM*(i+1)]:
                embed.add_field(name=f"{tracker_icons[int(parent_key)-1]} #{parent_key} チケット名:{filtered_data[parent_key]['title']}",value=f"ステータス:{filtered_data[parent_key]['status']}\r\n優先度:{filtered_data[parent_key]['priority']}　進捗度:{filtered_data[parent_key]['progressRate']}%　トラッカー:{filtered_data[parent_key]['tracker']}",inline=False)
            await interaction.channel.send(embed=embed)

        select.disabled=True
        await self.ctx.edit_original_response(content="検索オプションが選択されました。",view=self)
        self.stop()
    
    async def on_timeout(self):
        self.clear_items()
        await self.ctx.edit_original_response(content="タイムアウトしました。", view=self)
        self.stop()

#Discord Bot Commands============================================
#Create Ticket Command
@tree.command(
    guild=guild,
    name="チケット発行",
    description="開発チケットを発行します"
)
@discord.app_commands.describe(
     title="チケットタイトル",
     tracker="チケットの種類",
     priority="チケットの優先度",
     description="チケットの説明"
)
async def createTicket(ctx:discord.Interaction,title:str,tracker:Literal[f"{TRACKER[0]}",f"{TRACKER[1]}",f"{TRACKER[2]}",f"{TRACKER[3]}"],priority:Literal[f"{PRIORITY[0]}",f"{PRIORITY[1]}",f"{PRIORITY[2]}"],description:str):
    await ctx.response.defer()
    username=await client.fetch_user(ctx.user.id)
    json_data={
        "title":title,
        "description":description,
        "status":STATUS[0],
        "priority":priority,
        "progressRate":0,
        "tracker":tracker,
        "ticketCreator":username.display_name,
        "createdDate":datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    }
    #Save Ticket Data
    ticket_num,read_data=load_json()
    if ticket_num==-1:
        read_data={}
        ticket_num=0
    json_data={
        f"{ticket_num+1:05d}":json_data
    }
    read_data.update(json_data)
    save_json(read_data)
    embed=discord.Embed(title=":white_check_mark:チケットを発行しました。",color=0xffffff)
    await ctx.channel.send(embed=embed)
    await ctx.followup.send(embed=show_Ticket_embed(f"{ticket_num+1:05d}"))

#Update Ticket Command
@tree.command(
    guild=guild,
    name="チケット更新",
    description="開発チケットを更新します"
)
@discord.app_commands.describe(
    ticket_id="チケットID",
    status="チケットのステータス",
    progressrate="チケットの進捗率",
    description="チケットの説明"
)
async def updateTicket(ctx:discord.Interaction,ticket_id:str,status:Literal[f"{STATUS[0]}",f"{STATUS[1]}",f"{STATUS[2]}",f"{STATUS[3]}"]=None,progressrate:int=None,description:str=None):
    try:
        int(ticket_id)
    except ValueError:
        embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
        await ctx.response.send_message(embed=embed)
        return
    if len(ticket_id)!=5:
        ticket_id=f"{int(ticket_id):05d}"
    if int(ticket_id)<=0 and int(ticket_id)>=100000:
        embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
        await ctx.response.send_message(embed=embed)
        return
    if (status==None and progressrate==None and description==None):
        embed=discord.Embed(title=":speech_balloon:info",description=f"チケットID:**#{ticket_id}**のステータスは更新されませんでした。",color=0xffffff)
        await ctx.response.send_message(embed=embed)
        return
    await ctx.response.defer()
    _,read_data=load_json()
    if _==-1:
        embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
        await ctx.followup.send(embed=embed)
        return
    if status!=None:
        read_data[f"{ticket_id}"]["status"]=status
    if progressrate!=None:
        read_data[f"{ticket_id}"]["progressRate"]=progressrate
    if description!=None:
        read_data[f"{ticket_id}"]["description"]=description
    save_json(read_data)
    embed=discord.Embed(title=":arrows_counterclockwise:チケットを更新しました。",color=0xffffff)
    await ctx.channel.send(embed=embed)
    await ctx.followup.send(embed=show_Ticket_embed(f"{ticket_id}"))

#Edit Ticket Command
@tree.command(
    guild=guild,
    name="チケット編集",
    description="開発チケットを編集します"
)
@discord.app_commands.describe(
    ticket_id="チケットID",
    title="チケットタイトル",
    tracker="チケットの種類",
    priority="チケットの優先度",
    description="チケットの説明"
)
async def editTicket(ctx:discord.Interaction,ticket_id:str,title:str=None,tracker:Literal[f"{TRACKER[0]}",f"{TRACKER[1]}",f"{TRACKER[2]}",f"{TRACKER[3]}"]=None,priority:Literal[f"{PRIORITY[0]}",f"{PRIORITY[1]}",f"{PRIORITY[2]}"]=None,description:str=None):
    try:
        int(ticket_id)
    except ValueError:
        embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
        await ctx.response.send_message(embed=embed)
        return
    if len(ticket_id)!=5:
        ticket_id=f"{int(ticket_id):05d}"
    if int(ticket_id)<=0 and int(ticket_id)>=100000:
        embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
        await ctx.response.send_message(embed=embed)
        return
    if(title==None and tracker==None and priority==None and description==None):
        embed=discord.Embed(title=":speech_balloon:info",description=f"チケットID:**#{ticket_id}**の内容は更新されませんでした。",color=0xffffff)
        await ctx.response.send_message(embed=embed)
        return
    await ctx.response.defer()
    _,read_data=load_json()
    if _==-1:
        embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
        await ctx.followup.send(embed=embed)
        return
    if title!=None:
        read_data[f"{ticket_id}"]["title"]=title
    if tracker!=None:
        read_data[f"{ticket_id}"]["tracker"]=tracker
    if priority!=None:
        read_data[f"{ticket_id}"]["priority"]=priority
    if description!=None:
        read_data[f"{ticket_id}"]["description"]=description
    save_json(read_data)
    embed=discord.Embed(title=":pencil:チケットを編集しました。",color=0xffffff)
    await ctx.channel.send(embed=embed)
    await ctx.followup.send(embed=show_Ticket_embed(f"{ticket_id}"))

#Show Ticket List Command
@tree.command(
    guild=guild,
    name="チケット一覧",
    description="開発チケットの一覧を表示します"
)
#async def showTicketList(ctx:discord.Interaction,status:Literal[f"{STATUS[0]}",f"{STATUS[1]}",f"{STATUS[2]}"]=None,tracker:Literal[f"{TRACKER[0]}",f"{TRACKER[1]}",f"{TRACKER[2]}",f"{TRACKER[3]}"]=None,priority:Literal[f"{PRIORITY[0]}",f"{PRIORITY[1]}",f"{PRIORITY[2]}"]=None):
async def showTicketList(ctx:discord.Interaction):
    await ctx.response.send_message("検索オプションを選択してください。",view=TicketOptionPanel(ctx))

#Discord Bot Event================================================
#Discord Bot Ready
@client.event
async def on_ready():
     check_json()
     print("ready...")
     await tree.sync(guild=guild)
     print("sync commands...")

client.run(TOKEN)