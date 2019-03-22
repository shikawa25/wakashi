import discord
import json
import random
import re
import requests

from discord.ext import commands

bot = commands.Bot(command_prefix='~', command_not_found='O comando {} não existe.',
                   command_has_no_subcommands='O subcomando {} não existe.', case_insensitive=True,
                   description='um bot mal feito com funções inúteis')

r = requests.get("https://raw.githubusercontent.com/shikawa25/wakashi/master/weeb_nomes.json")
nomes = json.loads(r.text)


@bot.event
async def on_ready():
    print('Wakashi despertou')
    server_list = re.findall("(?:name=')(.*?)(?:'.?)", str(bot.guilds))
    print('Estou nos servers:', str(server_list).replace("[", "").replace("]", "").replace("'", ""))
    print('Latência:', bot.latency)
    await bot.change_presence(activity=discord.Game("memes"))


@bot.event
async def on_member_join(member):
    if "Grupo Kirinashi" in member.guild.name:
        await member.edit(nick=random.choice(nomes) + ' ' + random.choice(nomes))


@bot.command()
async def mocinha(ctx):
    for role in ctx.message.author.roles:
        if role.id == 521094117854281738:
            if len(ctx.message.mentions) == 0:
                for user in ctx.message.guild.members:
                    if user.id == 140454194464161793:
                        continue
                    else:
                        await user.edit(nick=random.choice(nomes) + ' ' + random.choice(nomes))
                break
            else:
                for mention in ctx.message.mentions:
                    await mention.edit(nick=random.choice(nomes) + ' ' + random.choice(nomes))
                break
    else:
        await ctx.send('**vc não tem rola pra isso**')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run('Mzc1NDIwMDYwNjYxMDU1NDkw.D3YDvA.j9KR9aO3lGsHTdmvF44vCGBGhCs')