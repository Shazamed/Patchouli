import asyncio

from discord.ext import commands, tasks
from discord import app_commands
from helpers import buzzle_helper as Buzzle
import discord


class BuzzleCog(commands.Cog, name='Buzzle'):
    def __init__(self, bot):
        self.bot = bot

    roles_list = {'🅱️': "🅱️"}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.timer.start()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = payload.member
        if payload.message_id in [905750912532893717, 905753216568942592]:
            if payload.emoji.name in self.roles_list:
                role_name = self.roles_list.get(payload.emoji.name)
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name=role_name)
                await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = await self.bot.fetch_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        if payload.message_id in [905750912532893717, 905753216568942592]:
            if payload.emoji.name in self.roles_list:
                role_name = self.roles_list.get(payload.emoji.name)
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name=role_name)
                await user.remove_roles(role)

    @tasks.loop(seconds=1)
    async def timer(self):
        timer_state = Buzzle.timer()
        if timer_state == 'start':
            await self.bot.get_channel(826343308870680646).send(f"Buzzle time <@&905730976892715008>")  # spam
            await self.bot.get_channel(768448152826282019).send(f"Buzzle time <@&905750415629516801>")  # buzzle
        elif timer_state == 'end':
            await self.bot.get_channel(826343308870680646).send(f"Buzzle end <@&905730976892715008>")  # spam
            await self.bot.get_channel(768448152826282019).send(f"Buzzle end <@&905750415629516801>")  # buzzle

    @app_commands.command(name='countdown', description='Checks the countdown to the next buzzle')
    async def cd(self, interaction: discord.Interaction):
        await interaction.response.send_message(await Buzzle.schedule_countdown())

    @app_commands.command(name='a1z26_encode', description='A1Z26 encoder, letters to numbers')
    @app_commands.describe(text="Letters to numbers, separate by space")
    async def a1z26_e(self, interaction, text: str):
        await interaction.response.send_message(await Buzzle.a1z26_e(text))

    @app_commands.command(name='a1z26_decode', description='A1Z26 decoder, numbers to letters')
    @app_commands.describe(text="Numbers to letters, separate by space")
    async def a1z26_d(self, interaction, text: str):
        await interaction.response.send_message(await Buzzle.a1z26_d(text))

    @app_commands.command(name='rot', description='Caesar/ROT cipher')
    async def caesar(self, interactions: discord.Interaction, text: str, shift: str):
        await interactions.response.send_message(Buzzle.caesar(text, shift))

    @commands.command(brief='Int/Binary to ASCII encoder/decoder')
    async def ascii(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Usage: !ascii [+(for hex)]<int, str, 8bit binary or hex>")
        else:
            await ctx.send(Buzzle.ascii_decoder(arg)[:2000])

    @commands.command(brief='Morse code encoder/decoder')
    async def morse(self, interactions: discord.Interaction, text: str):
        await interactions.response.send_message(await Buzzle.morse(text))

    @app_commands.command(name='vigenere', description='Vigenere cipher encoder/decoder, decoding is by default')
    async def vig(self, interactions: discord.Interaction, text: str, key: str, direction: str="d"):
        await interactions.response.send_message(await Buzzle.vigenere(text, key, direction))

    @app_commands.command(name='b64', description='Base64 text encoder/decoder, decoding is by default')
    @app_commands.describe(direction="Type 'd' or 'e' for decoding and encoding respectively")
    async def b64(self, interactions: discord.Interaction, text: str, direction: str="d"):
        await interactions.response.send_message(await Buzzle.b64(text, direction))

    @app_commands.command(name='frequency', description='Frequency analysis')
    async def freq(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(await Buzzle.freq(text))

    @app_commands.command(name='nut', description='Searches the text on nutrimatic')
    async def nut(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(await Buzzle.nutrimatic(text))

    @commands.hybrid_command(aliases=['calendar'], brief='Puzzle hunt calender')
    async def cal(self, ctx):
        await ctx.send(await Buzzle.calendar())

    @commands.command(name='hex', aliases=['hexadecimal'], brief='Hexadecimal to decimal encoder/decoder')
    async def hexadecimal(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("Usage: !hex <e/d>, <string of numbers>")
        else:
            await ctx.send(Buzzle.hexadecimal(arg))

    @app_commands.command(name='rev', description='String reverser')
    async def rev(self, interactions: discord.Interaction, text: str):
        await interactions.response.send_message(await Buzzle.reverse(text))

    @commands.command(brief='Braille encoder/decoder')
    async def braille(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("usage: !braille <text>")
        else:
            await ctx.send(Buzzle.braille(arg))

    @commands.command(brief='Atbash cipher encoder/decoder')
    async def atbash(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("Usage: !atbash <text>")
        else:
            await ctx.send(Buzzle.atbash(arg))

    @app_commands.command(name='qat', description='Searches the text on qat')
    async def qat(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        await asyncio.sleep(5)
        await interaction.followup.send((await Buzzle.qat(text))[:2000])

    @app_commands.command(name="multitap",  description="Multitap phone cipher encoder/decoder, decoding is by default")
    async def phone(self, interactions: discord.Interaction, text: str, direction: str):
        await interactions.response.send_message(await Buzzle.multi_tap(text, direction))

    @app_commands.command(name="sch-add", description='Add an upcoming buzzle hunt to the schedule')
    async def schedule_add(self, interaction: discord.Interaction, index: int):
        await interaction.response.send_message(await Buzzle.schedule_add(index))

    @app_commands.command(name="sch-check", description="Check the buzzle hunt schedule")
    async def schedule_check(self, interaction: discord.Interaction):
        await interaction.response.send_message(await Buzzle.schedule_read())

    @app_commands.command(name="sch-pop", description='Remove the last added item on the schedule')
    async def pop(self, interaction: discord.Interaction):
        await interaction.response.send_message(await Buzzle.schedule_remove())

    @commands.command(brief='Cryptogram solver by quipquip', aliases=['quipquip'])
    async def quip(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("Usage: !quip <text to solve>")
        else:
            await ctx.send(Buzzle.quipquip(arg))

    @commands.command(hidden=True)
    async def sync(self, ctx):
        await ctx.bot.tree.sync()
        await ctx.send("sync")

    # @app_commands.command(name="command-1")
    # async def my_command(self, interaction: discord.Interaction) -> None:
    #     # """ /command-1 """
    #     await interaction.response.send_message("Hello from command 1!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(BuzzleCog(bot))
