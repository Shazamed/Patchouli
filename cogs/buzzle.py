from discord.ext import commands, tasks
import buzzleTools as Buzzle


class buzzleCogs(commands.Cog, name='Buzzle'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.timer.start()

    @tasks.loop(seconds=1)
    async def timer(self):
        timer_state = Buzzle.timer()
        if timer_state == 'start':
            await self.bot.get_channel(826343308870680646).send(f"Buzzle time")  # spam
            await self.bot.get_channel(768448152826282019).send(f"Buzzle time")  # buzzle
        elif timer_state == 'end':
            await self.bot.get_channel(826343308870680646).send(f"Buzzle end")
            await self.bot.get_channel(768448152826282019).send(f"Buzzle end")  # buzzle

    @commands.command(brief='Checks the countdown to the next buzzle', aliases=['countdown'])
    async def cd(self, ctx):
        await ctx.send(Buzzle.schedule_countdown())

    @commands.command(brief='A1Z26 encoder/decoder')
    async def a1z26(self, ctx, *, arg=None):
        if not arg:
            await ctx.send('Usage !a1z26 <text to decode/encode>')
        else:
            await ctx.send(Buzzle.a1z26(arg))

    @commands.command(brief='Caesar/ROT cipher', aliases=['rot', 'ROT'], description='d/e to shift left/right respectively')
    async def caesar(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Usage: !caesar <e/d>, <text>, <shift number/'all'>")
        else:
            await ctx.send(Buzzle.caesar(arg))

    @commands.command(brief='Int/Binary to ASCII encoder/decoder')
    async def ascii(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Usage: !ascii [+(for hex)]<int, str, 8bit binary or hex>")
        else:
            await ctx.send(Buzzle.ascii_decoder(arg))

    @commands.command(brief='Morse code encoder/decoder')
    async def morse(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Usage: !morse <text or morse code sequence>")
        else:
            await ctx.send(Buzzle.morse(arg))

    @commands.command(aliases=['v', 'vigenere'], brief='Vigenere cipher encoder/decoder')
    async def vig(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Usage: !v <e/d>, <text>, <key>")
        else:
            await ctx.send(Buzzle.vigenere(arg))

    @commands.command(aliases=['base64'], brief='Base64 text encoder/decoder')
    async def b64(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Usage: !b64 <e/d>, <text>")
        else:
            await ctx.send(Buzzle.b64(arg))

    @commands.command(brief='Frequency analysis', aliases=['frequency'])
    async def freq(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Usage: !freq <text>")
        else:
            await ctx.send(Buzzle.freq(arg))

    @commands.command(aliases=['nutrimatic'], brief='Searches the text on nutrimatic')
    async def nut(self, ctx, *, arg=None):
        if not arg:
            await ctx.send("Usage: !nut <text>")
        else:
            await ctx.send(Buzzle.nutrimatic(arg))

    @commands.command(aliases=['calendar'], brief='Puzzle hunt calender')
    async def cal(self, ctx):
        await ctx.send(Buzzle.calendar())

    @commands.command(name='hex', aliases=['hexadecimal'], brief='Hexadecimal to decimal encoder/decoder')
    async def hexadecimal(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("Usage: !hex <e/d>, <string of numbers>")
        else:
            await ctx.send(Buzzle.hexadecimal(arg))

    @commands.command(brief='String reverser', aliases=['reverse'])
    async def rev(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("Usage: !rev <text>")
        else:
            await ctx.send(Buzzle.reverse(arg))

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

    @commands.command(brief='Searches the text on qat')
    async def qat(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("usage: !qat <text>")
        else:
            await ctx.send(Buzzle.qat(arg)[:2000])

    @commands.command(brief="Multitap phone cipher encoder/decoder", aliases=["multitap", "keypad", "multi"])
    async def phone(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("Usage: !phone <keypad sequence or text>")
        else:
            await ctx.send(Buzzle.multi_tap(arg))

    @commands.command(aliases=['sch'], brief='Schedule a queue of upcoming buzzle hunt')
    async def schedule(self, ctx, arg='c'):
        if arg is None:
            await ctx.send("Usage: !sch <list number on !cal or 'c' to check>")
        elif arg == 'c':
            await ctx.send(Buzzle.schedule_read())
        else:
            await ctx.send(Buzzle.schedule_add(arg))

    @commands.command(brief='Remove the last added item on the schedule')
    async def pop(self, ctx):
        await ctx.send(Buzzle.schedule_remove())


def setup(bot):
    bot.add_cog(buzzleCogs(bot))
