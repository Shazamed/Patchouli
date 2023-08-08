from discord.ext import commands
from discord import app_commands
import asyncio
import random
import time
from helpers import bad_apple_helper as ba, fun_helper as fun, reddit_helper as reddit
import discord

class HelpSelect(discord.ui.Select):
    def __init__(self, bot):
        options = [
            discord.SelectOption(label="Buzzle", emoji="🅱️", description="buzzle commands"),
            discord.SelectOption(label="Misc", emoji="🎲", description="miscellaneous commands"),
            discord.SelectOption(label="Music", emoji="🎵", description="music commands")
        ]
        super().__init__(placeholder="Choose a category", max_values=1, min_values=1, options=options)
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        emoji = {"Buzzle": "🅱", "Misc": "🎲", "Music": "🎵"}
        category = self.values[0]
        help_embed = discord.Embed(title=f"{emoji[category]} {category} Commands", colour=0xc566ed)

        for x in self.bot.get_cog(self.values[0]).get_app_commands():
            help_embed.add_field(name=x.name, value=x.description)
        await interaction.response.edit_message(embed=help_embed)


class HelpView(discord.ui.View):
    def __init__(self, *, bot, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(HelpSelect(bot))
class FunCog(commands.Cog, name='Misc'):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stonks", description='Check stonks price')
    async def stonks(self, interaction: discord.Interaction, ticker: str):
        await interaction.response.send_message(await fun.stonks(ticker))

    @commands.command(brief='fumofumo', description='fumofumo')
    async def fumo(self, ctx):
        await ctx.send("ᗜˬᗜ")

    @commands.command(brief='r u da imposter?')
    async def sus(self, ctx):
        randomNum = random.random()
        susText = ['''    ⣿⣿⣿⣿⣿⣿⡟⠁⠄⠄⠄⠄⣠⣤⣴⣶⣶⣶⣶⣤⡀⠈⠙⢿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡟⠄⠄⠄⠄⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠄⠈⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⠁⠄⠄⠄⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⢺⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡄⠄⠄⠄⠙⠻⠿⣿⣿⣿⣿⠿⠿⠛⠛⠻⣿⡄⠄⣾⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡇⠄⠄⠁ :eye: ⠄⢹⣿⡗⠄ :eye: ⢄⡀⣾⢀⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡇⠘⠄⠄⠄⢀⡀⠄⣿⣿⣷⣤⣤⣾⣿⣿⣿⣧⢸⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡇⠄⣰⣿⡿⠟⠃⠄⣿⣿⣿⣿⣿⡛⠿⢿⣿⣷⣾⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡄⠈⠁⠄⠄⠄⠄⠻⠿⢛⣿⣿⠿⠂⠄⢹⢹⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⡐⠐⠄⠄⣠⣀⣀⣚⣯⣵⣶⠆⣰⠄⠞⣾⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣷⡄⠄⠄⠈⠛⠿⠿⠿⣻⡏⢠⣿⣎⣾⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡿⠟⠛⠄⠄⠄⠄⠙⣛⣿⣿⣵⣿⡿⢹⡟⣿⣿⣿⣿⣿⣿⣿''', 'ඞ', '''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⣠⣤⣤⣤⣤⣤⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠛⠉⠙⠛⠛⠛⠛⠻⢿⣿⣷⣤⡀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠋⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠈⢻⣿⣿⡄⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣸⣿⡏⠀⠀⠀⣠⣶⣾⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣄⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⢰⣿⣿⣯⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣷⡄⠀
    ⠀⠀⣀⣤⣴⣶⣶⣿⡟⠀⠀⠀⢸⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀
    ⠀⢰⣿⡟⠋⠉⣹⣿⡇⠀⠀⠀⠘⣿⣿⣿⣿⣷⣦⣤⣤⣤⣶⣶⣶⣶⣿⣿⣿⠀
    ⠀⢸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀
    ⠀⣸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⡿⠿⠿⠛⢻⣿⡇⠀⠀
    ⠀⣿⣿⠁⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀
    ⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀
    ⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀
    ⠀⢿⣿⡆⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀
    ⠀⠸⣿⣧⡀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⠀
    ⠀⠀⠛⢿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⣰⣿⣿⣷⣶⣶⣶⣶⠶⠀⢠⣿⣿⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⣽⣿⡏⠁⠀⠀⢸⣿⡇⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⢹⣿⡆⠀⠀⠀⣸⣿⠇⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⢿⣿⣦⣄⣀⣠⣴⣿⣿⠁⠀⠈⠻⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠿⠿⠿⠋⠁⠀''',
        '''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠟⠉⠉⠉⠉⠉⠉⠉⠙⠻⢶⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡟⠀⣠⣶⠛⠛⠛⠛⠛⠛⠳⣦⡀⠀⠘⣿⡄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⢹⣿⣦⣀⣀⣀⣀⣀⣠⣼⡇⠀⠀⠸⣷⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡏⠀⠀⠀⠉⠛⠿⠿⠿⠿⠛⠋⠁⠀⠀⠀⠀⣿⡄⣠
⠀⠀⢀⣀⣀⣀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠀
⠿⠿⠟⠛⠛⠉⠀⠀⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀
⠀⠀⠀⠀⠀⠀⠀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀
⠀⠀⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀
⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⣠⡶⠶⠿⠿⠿⠿⢷⣦⠀⠀⠀⠀⠀⠀⠀⣿⠀
⠀⠀⣀⣀⣀⠀⣸⡇⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⣿⠀
⣠⡿⠛⠛⠛⠛⠻⠀⠀⠀⠀⠀⢸⣇⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠀⣿⠀
⢻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡟⠀⠀⢀⣤⣤⣴⣿⠀⠀⠀⠀⠀⠀⠀⣿⠀
⠈⠙⢷⣶⣦⣤⣤⣤⣴⣶⣾⠿⠛⠁⢀⣶⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀
⢷⣶⣤⣀⠉⠉⠉⠉⠉⠄⠀⠀⠀⠀⠈⣿⣆⡀⠀⠀⠀⠀⠀⠀⢀⣠⣴⡾⠃⠀
⠀⠈⠉⠛⠿⣶⣦⣄⣀⠀⠀⠀⠀⠀⠀⠈⠛⠻⢿⣿⣾⣿⡿⠿⠟⠋⠁⠀⠀⠀''']
        if randomNum < 0.1:
            await ctx.send('Amogus\n' + susText[3])
        elif randomNum < 0.3:
            await ctx.send('Sussus Amogus!\n' + susText[0])
        elif randomNum < 0.65:
            await ctx.send('not sus\n' + susText[1])
        else:
            await ctx.send('not sus?\n' + susText[2])

    @app_commands.command(name='2hujerk', description='Random meme from r/2hujerk')
    async def touhoujerk(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.channel.is_nsfw():
            nsfw = True
        else:
            nsfw = False
        reddit_link = await reddit.reddit("2hujerk", nsfw)
        await asyncio.sleep(5)
        await interaction.followup.send(reddit_link)


    @app_commands.command(name='reddit', description='Search a random top 10 hot post from a subreddit')
    async def reddit(self, interaction: discord.Interaction, subreddit: str):
        await interaction.response.defer()
        if interaction.channel.is_nsfw():
            nsfw = True
        else:
            nsfw = False
        reddit_link = f'Searching r/{subreddit}\n' + await reddit.reddit(subreddit, nsfw)

        await asyncio.sleep(5)
        await interaction.followup.send(reddit_link)

    @commands.command(hidden=True)
    async def testemoji(self, ctx):
        emoji = '<a:rumiadance:831782682329088000>'
        await ctx.message.add_reaction(emoji)
        await ctx.send(emoji)

    @commands.command(brief="SAD! apple. Spam warning! 1fps lol fuk rate limit")
    async def badapple(self, ctx):
        frames = []
        await ctx.send("☯The girls are now preparing. Please wait warmly.☯")
        for i in range(0, int(6571/30)):
            path = "./frames/BA" + str(i*30) + ".jpg"
            frames.append(ba.runner(path))
        i = 0
        while i < len(frames) - 1:
            await ctx.send(frames[i])
            i += 1
            time.sleep(1)

    @commands.command(brief="Experimental: thedylone can now view webpages as images!")
    async def proxy(self, ctx, arg=None):
        if arg is None:
            await ctx.send("Usage: !proxy <URL>")
        elif fun.proxy(arg) is True:
            await ctx.send(file=discord.File("./data/screenshots/proxy_ss.png"))
        else:
            await ctx.send("That is not a valid url")

    @app_commands.command(name="help")
    async def help_command(self, interactions: discord.Interaction):

        help_embed = discord.Embed(title="Patchouli Help", colour=0xc566ed, description="Choose a category for more info")
        help_embed.add_field(name="🅱️ Buzzle", value="buzzle commands", inline=False)
        help_embed.add_field(name="🎲 Misc", value="miscellaneous commands", inline=False)
        help_embed.add_field(name="🎵 Music", value="music commands", inline=False)
        await interactions.response.send_message(embed=help_embed, view=HelpView(bot=self.bot))

async def setup(bot):
    await bot.add_cog(FunCog(bot))
