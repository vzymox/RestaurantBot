import discord
from discord.ext import commands
import datetime
import requests
import random
import math
import time
from discord.ext.commands import errors, converter
from random import randint, choice as rnd
import aiohttp
import asyncio
import json
import os
import re
from pymongo import MongoClient
import pymongo
import string
import food
import config
from .utils import do
import psutil

client = MongoClient(config.mongo_client)
db = client['siri']

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = 'r!'
        self.process = psutil.Process(os.getpid())
        self.rs = []
        self._last_result = None

    @commands.command(aliases=['Stats', 'info', 'botinfo', 'status'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def stats(self, ctx):
        
        users = len(set(self.bot.get_all_members()))
        channels = []
        for guild in self.bot.guilds:
            for channel in guild.channels:
                channels.append(channel)
        channels = len(channels)
        emojis = len(self.bot.emojis)
        commands = len(self.bot.all_commands)

        author = ctx.message.author

        ram = self.process.memory_full_info().rss / 1024**2

        stat = discord.Embed(colour=0xa82021, description=f"**Restaurant** `by lukee#0420`\n\n\n" \
        f"\> **Python**... `3.6`\n" \
        f"\> **Ubuntu**... `18.04`\n" \
        f"\> **RAM Usage**... `{ram:.2f}MB`\n\n"
        f"I am in **{str(len(self.bot.guilds))} servers**!\n"\
        f"I can view **{channels} channels**!\n"\
        f"I am with **{users} users**!\n"\
        f"I can use **{emojis} emojis**!\n\n"\
        f"[[Invite]](https://discordapp.com/api/oauth2/authorize?client_id=648065060559781889&permissions=8192&scope=bot)"\
        f" [[Support]](https://discord.gg/BCRtw7c)")
        stat.set_footer(text="Thanks for using Restaurant! | Res-V1")
        await ctx.send(embed=stat)
        
    @commands.command(aliases=['debug', 'ev'])
    async def eval(self, ctx, *, code):
        if ctx.author.id == 396153668820402197:
            o_code = code
            code = code.replace('“', '"').replace('”', '"').replace("-silent", "").replace("-s", "").replace("```py", "").replace("```", "")
            try:
                env = {
                    'bot': ctx.bot,
                    'ctx': ctx,
                    'channel': ctx.message.channel,
                    'author': ctx.message.author,
                    'guild': ctx.message.guild,
                    'message': ctx.message,
                    'discord': discord,
                    'random': random,
                    'commands': commands,
                    'requests': requests,
                    'asyncio': asyncio,
                    're': re,
                    'os': os,
                    'pymongo': pymongo,
                    'MongoClient': client,
                    'json': json,
                    'db': db,
                    'rnd': rnd,
                    'do':do,
                    'time_rx': re.compile('[0-9]+'),
                    '_': self._last_result
                }

                try:
                    result = eval(code, env)
                except SyntaxError as e:
                    embed=discord.Embed(colour=0xff0000, description=f":inbox_tray: **INPUT**:\n```py\n{code}```\n:outbox_tray: **OUTPUT**:\n```py\n{e}```")
                    embed.set_footer(text="Error")
                    return await ctx.send(embed=embed)
                except Exception as e:
                    embed=discord.Embed(colour=0xff0000, description=f":inbox_tray: **INPUT**:\n```py\n{code}```\n:outbox_tray: **OUTPUT**:\n```py\n{e}```")
                    embed.set_footer(text="Error")
                    return await ctx.send(embed=embed)

                if asyncio.iscoroutine(result):
                    result = await result

                self._last_result = result

                if code == "bot.http.token":
                    embed=discord.Embed(colour=0xa82021, description=f":inbox_tray: **INPUT**:\n```py\n{code}```\n:outbox_tray: **OUTPUT**:\n```py\n{result}```")
                    return await ctx.send(embed=embed)

                elif o_code.endswith(" -silent") or o_code.endswith(" -s"):
                    pass

                else:
                    if len(str(result)) > 1500:
                        r = requests.post(f"https://hastebin.com/documents", data=str(result).encode('utf-8')).json()
                        return await ctx.send(":weary::ok_hand: The output is too long to send to chat. Here is a hastebin file for ya.. :point_right: https://hastebin.com/" + r['key'])                    
                    else:
                        try:
                            embed=discord.Embed(colour=0xa82021, description=f":inbox_tray: **INPUT**:\n```py\n\u200b{code}```\n:outbox_tray: **OUTPUT**:\n```py\n{result}```")
                            return await ctx.send(embed=embed)
                        except Exception as e:
                            embed=discord.Embed(colour=0xff0000, description=f":inbox_tray: **INPUT**:\n```py\n{code}```\n:outbox_tray: **OUTPUT**:\n```py\n{e}```")
                            embed.set_footer(text="Error")
                            return await ctx.send(embed=embed)
            except Exception as e:
                embed=discord.Embed(colour=0xff0000, description=f":inbox_tray: **INPUT**:\n```py\n{code}```\n:outbox_tray: **OUTPUT**:\n```py\n{e}```")
                embed.set_footer(text="Error")
                return await ctx.send(embed=embed)
        else:
            pass



def setup(bot):
    bot.add_cog(Dev(bot))
