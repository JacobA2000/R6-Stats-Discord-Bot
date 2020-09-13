#ADD CODE TO HANDLE A HTTP 400 RESPONSE

import discord
from discord.ext import commands

import requests
import json

from datetime import datetime

#START OF R6TAB API HANDLING
class Player:
    def __init__(self, id, name, platform, level, kd, mmr, rank):
        self.id = id
        self.name = name
        self.platform = platform
        self.level = level
        self.kd = kd
        self.mmr = mmr
        self.rank = rank

def FindPlayer(searchData, searchName):
    for playerID in searchData:
        if(searchData[playerID]["profile"]["p_name"] == searchName):
            return searchData[playerID]

    return None

def GetPlayerData(platform, name):
    returnedData = requests.get(f"https://r6.apitab.com/search/{platform}/{name}")
    returnedData = json.loads(returnedData.text)
    playerSearchData = (returnedData["players"])
    playerData = FindPlayer(playerSearchData, name)

    if playerData != None:
        player = Player(playerData["profile"]["p_id"], playerData["profile"]["p_name"], playerData["profile"]["p_platform"], playerData["stats"]["level"], playerData["ranked"]["kd"], playerData["ranked"]["mmr"], playerData["ranked"]["rank"])
        return player
    else:
        return None

def GetRankIcon(rank):
    if rank == 0: rankIcon = "https://i.imgur.com/srSWbpK.png"
    elif rank == 1: rankIcon = "https://i.imgur.com/q1Pf36g.png"
    elif rank == 2: rankIcon = "https://i.imgur.com/jVVRTC8.png"
    elif rank == 3: rankIcon = "https://i.imgur.com/f7uqstW.png"
    elif rank == 4: rankIcon = "https://i.imgur.com/b1fxB0R.png"
    elif rank == 5: rankIcon = "https://i.imgur.com/NoaZ40s.png"
    elif rank == 6: rankIcon = "https://i.imgur.com/kKFKAOO.png"
    elif rank == 7: rankIcon = "https://i.imgur.com/6VTptf2.png"
    elif rank == 8: rankIcon = "https://i.imgur.com/irp8YXj.png"
    elif rank == 9: rankIcon = "https://i.imgur.com/KGxx2D3.png"
    elif rank == 10: rankIcon = "https://i.imgur.com/CVKlWkN.png"
    elif rank == 11: rankIcon = "https://i.imgur.com/JYTUKh5.png"
    elif rank == 12: rankIcon = "https://i.imgur.com/L0GewVB.png"
    elif rank == 13: rankIcon = "https://i.imgur.com/KFyvZk6.png"
    elif rank == 14: rankIcon = "https://i.imgur.com/dOrfsrp.png"
    elif rank == 15: rankIcon = "https://i.imgur.com/OOSccEw.png"
    elif rank == 16: rankIcon = "https://i.imgur.com/xdM98FN.png"
    elif rank == 17: rankIcon = "https://i.imgur.com/yQJuctj.png"
    elif rank == 18: rankIcon = "https://i.imgur.com/JpFKAop.png"
    elif rank == 19: rankIcon = "https://i.imgur.com/JZbcfTt.png"
    elif rank == 20: rankIcon = "https://i.imgur.com/ppcwPtu.png"
    elif rank == 21: rankIcon = "https://i.imgur.com/HQvuEvD.png"

    return rankIcon
    
def GetRankColour(rank):
    if rank >= 0 & rank <=4: rankColour = 0x7c2b00
    elif rank >= 5 & rank <=9: rankColour = 0xbc783c
    elif rank >= 10 & rank <=14: rankColour = 0xa5a5a5
    elif rank >= 15 & rank <=17: rankColour = 0xedaf35
    elif rank >= 18 & rank <=20: rankColour = 0x44ccc0
    elif rank == 21: rankColour = 0x9a7cf4

    return rankColour

def GetRankName(rank):
    if rank == 0: rankName = "Copper V"
    elif rank == 1: rankName = "Copper IV"
    elif rank == 2: rankName = "Copper III"
    elif rank == 3: rankName = "Copper II"
    elif rank == 4: rankName = "Copper I"
    elif rank == 5: rankName = "Bronze V"
    elif rank == 6: rankName = "Bronze IV"
    elif rank == 7: rankName = "Bronze III"
    elif rank == 8: rankName = "Bronze II"
    elif rank == 9: rankName = "Bronze I"
    elif rank == 10: rankName = "Silver V"
    elif rank == 11: rankName = "Silver IV"
    elif rank == 12: rankName = "Silver III"
    elif rank == 13: rankName = "Silver II"
    elif rank == 14: rankName = "Silver I"
    elif rank == 15: rankName = "GOLD III"
    elif rank == 16: rankName = "GOLD II"
    elif rank == 17: rankName = "GOLD I"
    elif rank == 18: rankName = "Platinum III"
    elif rank == 19: rankName = "Platinum II"
    elif rank == 20: rankName = "Platinum I"
    elif rank == 21: rankName = "Diamond"

    return rankName
#END OF R6TAB API HANDLING

#START OF DISCORD HANDLING

with open('./config.json') as f:
    configData = json.load(f)

token = configData["token"]
prefix = configData["prefix"]

bot = commands.Bot(command_prefix= f"{prefix} ")
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot is online.')
    await bot.change_presence(activity=discord.Game(name=f"{prefix}, Help: {prefix} help"))
 
#GENERAL COMMANDS

@bot.command()
async def stats(ctx, platform, name):
    timenow = datetime.now()
    now = timenow.strftime("%m/%d/%Y, %H:%M:%S")
    print(f"User: {ctx.author} ID: {ctx.author.id} called the stats command using the parameters <{platform}><{name}> at {now}")
    
    player = GetPlayerData(platform, name)
    
    if player != None:
        rankIconURL = GetRankIcon(player.rank)
        rankColour = GetRankColour(player.rank)
        rankName = GetRankName(player.rank)

        embed=discord.Embed(title="PLAYER STATS", description="RainbowSixStats retrieved the stats for the player you searched:", color=rankColour)
        embed.set_thumbnail(url=rankIconURL)
        embed.add_field(name="ID:", value=str(player.id), inline=True)
        embed.add_field(name="NAME:", value=player.name, inline=True)
        embed.add_field(name="LEVEL:", value=str(player.level), inline=True)
        embed.add_field(name="KD:", value=str(player.kd), inline=True)
        embed.add_field(name="MMR:", value=str(player.mmr), inline=True)
        embed.add_field(name="RANK:", value=str(rankName), inline=True)
        embed.set_footer(text="MORE INFO: \nPlatform: " + player.platform)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"RainbowSixStats couldn't retreive data for {name}, make sure the spelling and capitalisation is accurate as this tool is case sensitive.")

@bot.command()
async def kd(ctx, platform, name):
    timenow = datetime.now()
    now = timenow.strftime("%m/%d/%Y, %H:%M:%S")
    print(f"User: {ctx.author} ID: {ctx.author.id} called the kd command using the parameters <{platform}><{name}> at {now}")
    
    player = GetPlayerData(platform, name)

    if player != None:
        await ctx.send(f"{name} has a kill/death ratio of {player.kd}.")
    else:
        await ctx.send(f"RainbowSixStats couldn't retreive data for {name}, make sure the spelling and capitalisation is accurate as this tool is case sensitive.")

@bot.command()
async def mmr(ctx, platform, name):
    timenow = datetime.now()
    now = timenow.strftime("%m/%d/%Y, %H:%M:%S")  
    print(f"User: {ctx.author} ID: {ctx.author.id} called the mmr command using the parameters <{platform}><{name}> at {now}")
    
    player = GetPlayerData(platform, name)

    if player != None:      
        await ctx.send(f"{name} has an mmr of {player.mmr}.")
    else:
        await ctx.send(f"RainbowSixStats couldn't retreive data for {name}, make sure the spelling and capitalisation is accurate as this tool is case sensitive.")

@bot.command()
async def rank(ctx, platform, name):
    timenow = datetime.now()
    now = timenow.strftime("%m/%d/%Y, %H:%M:%S")
    print(f"User: {ctx.author} ID: {ctx.author.id} called the rank command using the parameters <{platform}><{name}> at {now}")
    
    player = GetPlayerData(platform, name)

    if player != None:
        rankName = GetRankName(player.rank)
        await ctx.send(f"{name} is the rank {rankName}.")
    else:
        await ctx.send(f"RainbowSixStats couldn't retreive data for {name}, make sure the spelling and capitalisation is accurate as this tool is case sensitive.")

@bot.command()
async def help(ctx):
    timenow = datetime.now()
    now = timenow.strftime("%m/%d/%Y, %H:%M:%S")
    print(f"User: {ctx.author} ID: {ctx.author.id} called the help command at {now}")
    
    author = bot.get_user(ctx.author.id)

    embed=discord.Embed(title="RAINBOWSIXSTATS BOT HELP", description=f"Below is a list of commands and their parameters that this bot can perform. All commands must follow the bots prefix {prefix}, make sure to include a space after the prefix.", color=0x0062ff)
    embed.add_field(name="Commands", value="stats \nkd \nmmr \nrank", inline=True)
    embed.add_field(name="Parmameters", value="platform (uplay, xbl, psn), username \nplatform (uplay, xbl, psn), username \nplatform (uplay, xbl, psn), username \nplatform (uplay, xbl, psn), username", inline=True)
    await author.send(embed=embed)

bot.run(token)