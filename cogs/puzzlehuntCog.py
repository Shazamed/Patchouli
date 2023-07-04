from discord.ext import commands
from modules import puzzlehunt
import discord

class PuzzleHuntCog(commands.Cog, name='Puzzlehunt'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=["puzzle"])
    async def puzzles(self, ctx):
        authorID = ctx.author.id
        des = puzzlehunt.puzzle_check(authorID)
        embedPuzzle = discord.Embed(title="Puzzles", description="", colour=0xc566ed)
        embedPuzzle.add_field(name=f'{des[0]}: {des[1]}', value=f"[{des[2]}]({des[2]})", inline=False)
        await ctx.send(embed=embedPuzzle)

    @commands.command(hidden=True)
    async def guess(self, ctx, *, arg=None):
        authorID = ctx.author.id
        if arg is not None:
            await ctx.send(puzzlehunt.puzzle_guess(authorID, arg))
        else:
            await ctx.send("Usage: !guess (puzzle no), (answer)")

    @commands.command(hidden=True)
    async def solved(self, ctx):
        authorID = ctx.author.id
        listSolved = puzzlehunt.solve_check(authorID)
        embedSolved = discord.Embed(title='Solved Puzzles', description='', colour=0xc566ed)
        for x in range(len(listSolved)):
            puzzleInfo = listSolved[x].split(",")
            embedSolved.add_field(name=f"{puzzleInfo[0]}: {puzzleInfo[1]}", value=f"[{puzzleInfo[2]}]({puzzleInfo[2]})", inline=False)
        if len(listSolved) == 0:
            emoji = '<:marisad:846587491480764436>'
            embedSolved.add_field(name=f'{emoji}', value='Solve more puzzles')
        await ctx.send(embed=embedSolved)

    @commands.command(hidden=True)
    async def phelp(self, ctx):
        embedPHelp = discord.Embed(title="Help", description='', colour=0xc566ed)
        embedPHelp.add_field(name='!guess (puzzle number), (answer)', value='Guess the answer for the puzzle', inline=False)
        embedPHelp.add_field(name='!phelp', value='Shows this embed', inline=False)
        embedPHelp.add_field(name='!hint', value='Pings me', inline=False)
        embedPHelp.add_field(name='!puzzles', value='Shows unlocked puzzles', inline=False)
        embedPHelp.add_field(name='!solved', value='Shows solved puzzles', inline=False)
        await ctx.send(embed=embedPHelp)

    @commands.command(hidden=True)
    async def hint(self, ctx):
        await ctx.send("<@377794624540114944>")


async def setup(bot):
    await bot.add_cog(PuzzleHuntCog(bot))
