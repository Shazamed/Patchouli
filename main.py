#! python3
from discord.ext import commands
import discord
# import youtube_dl
import os
from helpers import fun_commands as fun
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

initial_extensions = ['cogs.buzzle', 'cogs.fun', 'cogs.puzzlehuntCog', 'cogs.music']
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# if __name__ == '__main__':
#     for extension in initial_extensions:
#         bot.load_extension(extension)
#     bot.help_command.cog = bot.cogs["Misc"]

@bot.event
async def setup_hook():
    await bot.load_extension('cogs.fun')
    await bot.load_extension('cogs.buzzle')
    await bot.load_extension('cogs.puzzlehuntCog')

    bot.help_command.cog = bot.cogs["Misc"]


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="東方Project | !help"))





@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == 'fruce?':
        await message.channel.send('fruce?')
    if message.content.lower() == 'hotel?':
        await message.channel.send('Trivago.')
    if message.content.lower() == 'sus?':
        await message.channel.send('amogus')
    if message.content.lower() == 'cbt':
        await message.channel.send(fun.cbt())
    if message.content.lower().startswith('hmm'):
        emoji = '<a:thonking:831789205225996288>'
        await message.add_reaction(emoji)
    if message.content.lower().endswith('solved') and message.content[0] != "!":
        emoji = '<a:rumiadance:831782682329088000>'
        await message.channel.send(emoji)
    if message.content.lower().startswith('ayaya'):
        emoji = '<:ayayaya:831793340835037184>'
        await message.channel.send(emoji)
    if message.content.lower().startswith('pog'):
        emoji = '<:mokoupoggers:831897999146745938>'
        await message.channel.send(emoji)
    if message.content.lower().startswith('awoo'):
        emoji = '<:awoo:835499877185486848>'
        await message.channel.send(emoji)
    if message.content.lower() == 'le':
        emoji = '<:LeSanae:844559050272145440>'
        await message.channel.send(emoji)
    if message.content.lower().startswith('pekoggers'):
        emoji = '<:pekoggers:844575409798250516>'
        await message.channel.send(emoji)

    if message.content.lower() in ['penis music', 'benis music', '🅱️enis music']:
        await message.channel.send('https://www.youtube.com/watch?v=c4KNd0Yv6d0')
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await message.channel.send("Wait for the current playing music to end")
            return
        voice = discord.utils.get(bot.voice_clients, guild=message.guild)
        voiceChannel = message.author.voice.channel
        if voice is None:
            await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=message.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=c4KNd0Yv6d0'])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("./song.mp3"))

    await bot.process_commands(message)


bot.run(TOKEN)
