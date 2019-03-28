import discord
import json
import random
import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from discord.ext import commands
import asyncio
from selenium.webdriver.chrome.options import Options
from discord.ext import commands
import urllib.parse

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
async def sauce(ctx):
    async for message in ctx.channel.history(limit=20):
        if len(message.attachments) > 0:
            chrome_options = Options()
            chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver",
                                      chrome_options=chrome_options)
            url = "https://trace.moe/?url=" + message.attachments[0].url
            driver.get(url)
            await asyncio.sleep(7)
            content_element = driver.find_element_by_id("results")
            html = content_element.get_attribute("innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            driver.close()
            data = str(soup.find('li', attrs={'class': 'result'}))
            embed = discord.Embed(color=0xfac4c4)
            title = re.findall('(?:data-title-romaji=\")(.*?)(?:\")', data)[0]
            ep = re.findall('(?:class=\"ep\">EP#)(.*?)(?:</span>)', data)[0]
            time = re.findall('(?:class=\"time\">)(.*?)(?:</span>)', data)[0]
            id = re.findall('(?:data-anilist-id=\")(.*?)(?:\")', data)[0]
            file_title = urllib.parse.quote(re.findall('(?:data-title=\")(.*?)(?:\")', data)[0])
            data_start = re.findall('(?:data-start=\")(.*?)(?:\")', data)[0]
            data_end = re.findall('(?:data-end=\")(.*?)(?:\")', data)[0]
            data_token = re.findall('(?:data-token=\")(.*?)(?:\")', data)[0]
            video = 'https://trace.moe/'+id+'/'+ file_title + '?start=' + data_start + '&end=' + data_end + '&token=' + data_token
            embed.add_field(name="Sauce",
                            value="Anime: **" + title + "**\nEpisódio: **" + ep + "**\nTempo estimado: **" + time + "**")
            embed.set_footer(text="https://anilist.co/anime/" + id)
            await asyncio.sleep(1)
            await ctx.send(video)
            await asyncio.sleep(6)
            await ctx.send(embed=embed)
            return

        regex = re.findall("(http.*\.[a-zA-Z]{3})", message.content)
        if str(regex) != "[]":
            chrome_options = Options()
            chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver",
                                      chrome_options=chrome_options)
            url = "https://trace.moe/?url=" + regex[-1]
            driver.get(url)
            await asyncio.sleep(7)
            content_element = driver.find_element_by_id("results")
            html = content_element.get_attribute("innerHTML")
            driver.close()
            soup = BeautifulSoup(html, "html.parser")
            data = str(soup.find('li', attrs={'class': 'result'}))
            embed = discord.Embed(color=0xfac4c4)
            title = re.findall('(?:data-title-romaji=\")(.*?)(?:\")', data)[0]
            ep = re.findall('(?:class=\"ep\">EP#)(.*?)(?:</span>)', data)[0]
            time = re.findall('(?:class=\"time\">)(.*?)(?:</span>)', data)[0]
            id = re.findall('(?:data-anilist-id=\")(.*?)(?:\")', data)[0]
            file_title = urllib.parse.quote(re.findall('(?:data-title=\")(.*?)(?:\")', data)[0])
            print(file_title)
            data_start = re.findall('(?:data-start=\")(.*?)(?:\")', data)[0]
            data_end = re.findall('(?:data-end=\")(.*?)(?:\")', data)[0]
            data_token = re.findall('(?:data-token=\")(.*?)(?:\")', data)[0]
            video = 'https://trace.moe/' + id + '/' + file_title + '?start=' + data_start + '&end=' + data_end + '&token=' + data_token
            embed.add_field(name="Sauce",
                            value="Anime: **" + title + "**\nEpisódio: **" + ep + "**\nTempo estimado: **" + time + "**")
            embed.set_footer(text="https://anilist.co/anime/" + id)
            await asyncio.sleep(1)
            await ctx.send(video)
            await asyncio.sleep(6)
            await ctx.send(embed=embed)
            return


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run('Mzc1NDIwMDYwNjYxMDU1NDkw.D3k7YQ.q8NZ_T2CtjrYH0Ab35N9NLB-kh8')
