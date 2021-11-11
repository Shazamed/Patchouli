from discord.ext import commands, tasks
from modules import puzzlehunt
import discord

class PuzzleHuntCogs(commands.Cog, name='Puzzlehunt'):
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
        await ctx.send(puzzlehunt.puzzle_guess(authorID, arg))

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
            embedSolved.add_field(name=f'{emoji}',value='Solve more puzzles')
        await ctx.send(embed=embedSolved)

def setup(bot):
    bot.add_cog(PuzzleHuntCogs(bot))
