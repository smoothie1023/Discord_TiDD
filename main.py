#!/usr/bin/env python3
import discord
from discord import app_commands

import os
import json
import datetime

from typing import Literal

#Discord Bot Initialize
client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

#Folder Path=====================================================
#Discord Bot Token and IDs
DiscordIDs_FolderPath="DiscordIDs/"

#Json File Path
Json_FolderPath="Json/"
Json_FileName="Tickets.json"

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

    if read_data[ticket_id]["tracker"]=="バグ":
        color=0xff0000
    elif read_data[ticket_id]["tracker"]=="機能追加":
        color=0xfff68f
    elif read_data[ticket_id]["tracker"]=="仕様変更":
        color=0x99c0ff
    elif read_data[ticket_id]["tracker"]=="サポート":
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
async def createTicket(ctx:discord.Interaction,title:str,tracker:Literal["バグ","機能追加","仕様変更","サポート"],priority:Literal["高","通常","低"],description:str):
    await ctx.response.defer()
    username=await client.fetch_user(ctx.user.id)
    json_data={
        "title":title,
        "description":description,
        "status":"新規",
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
    progressrate="チケットの進捗率"
)
async def updateTicket(ctx:discord.Interaction,ticket_id:str,status:Literal["新規","処理中","リリース待ち","完了"]=None,progressrate:int=None):
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
    if (status==None and progressrate==None):
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
async def editTicket(ctx:discord.Interaction,ticket_id:str,title:str=None,tracker:Literal["バグ","機能追加","仕様変更","サポート"]=None,priority:Literal["高","通常","低"]=None,description:str=None):
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
@discord.app_commands.describe(
    status="チケットのステータス",
    tracker="チケットの種類",
    priority="チケットの優先度"
)
async def showTicketList(ctx:discord.Interaction,status:Literal["新規","処理中","リリース待ち","完了"]=None,tracker:Literal["バグ","機能追加","仕様変更","サポート"]=None,priority:Literal["高","通常","低"]=None):
    await ctx.response.defer()
    ticket_num,read_data=load_json()
    if ticket_num==-1:
        embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
        await ctx.followup.send(embed=embed)
        return

    ROW_NUM=15
    
    tracker_icons = [":red_square:" if read_data[f'{n:05d}']['tracker'] == "バグ" else ":yellow_square:" if read_data[f'{n:05d}']['tracker'] == "機能追加" else ":blue_square:" if read_data[f'{n:05d}']['tracker'] == "仕様変更" else ":green_square:" if read_data[f'{n:05d}']['tracker'] == "サポート" else ":white_large_square:" for n in range(1,ticket_num+1)]
    
    if status!=None:
        read_data = {key: value for key, value in read_data.items() if value["status"] == status}
        ticket_num=len(read_data)

    if tracker!=None:
        read_data = {key: value for key, value in read_data.items() if value["tracker"] == tracker}
        ticket_num=len(read_data)

    if priority!=None:
        read_data = {key: value for key, value in read_data.items() if value["priority"] == priority}
        ticket_num=len(read_data)

    if ticket_num==0:
        embed=discord.Embed(title=":speech_balloon:チケットがありません。",color=0xffffff)
        await ctx.followup.send(embed=embed)
        return
    await ctx.followup.send(f"チケット一覧を表示します。")
    
    for i in range(0,(ticket_num+ROW_NUM)//ROW_NUM):
        embed=discord.Embed(title=f"チケット一覧[{i+1}/{(ticket_num+ROW_NUM-1)//(ROW_NUM)}]",color=0xffffff)
        for parent_key in list(read_data.keys())[i*ROW_NUM:ROW_NUM*(i+1)]:
            embed.add_field(name=f"{tracker_icons[int(parent_key)-1]} #{parent_key} チケット名:{read_data[parent_key]['title']}",value=f"ステータス:{read_data[parent_key]['status']}\r\n優先度:{read_data[parent_key]['priority']}　進捗度:{read_data[parent_key]['progressRate']}%　トラッカー:{read_data[parent_key]['tracker']}",inline=False)
        await ctx.channel.send(embed=embed)

#Discord Bot Event================================================
#Discord Bot Ready
@client.event
async def on_ready():
     check_json()
     print("ready...")
     await tree.sync(guild=guild)
     print("sync commands...")

client.run(TOKEN)