from discord.ext import commands
import discord
import lavalink


class MusicCog(commands.Cog, name='Music'):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node('localhost', 6000, 'shazam', 'asia', 'music_node')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild.id)
            await self.connect_channel(guild_id, None)

    async def connect_channel(self, guild_id: int, channel_id):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command()
    async def play(self, ctx, *, arg=None):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        if ctx.author.voice is None:
            return await ctx.send("Join a voice channel first")
        if arg is None:
            return await ctx.send("Usage !play <URL or search term>")
        elif arg.startswith("http"):
            query = arg
            search = False
        else:
            query = f'ytsearch:{arg}'
            search = True
        if voice_client is None:
            player.store('channel', ctx.channel.id)
            await self.connect_channel(ctx.guild.id, ctx.author.voice.channel.id)

        player = self.bot.music.player_manager.get(ctx.guild.id)
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send('The archives are incomplete!')
        if search:
            tracks = results['tracks'][0:10]
            embedSearch = discord.Embed(title='Select song', colour=0xc566ed)
            i = 0
            for track in tracks:
                i += 1
                embedSearch.add_field(name=f'{i}. {track["info"]["title"]}', value=f'{track["info"]["uri"]}', inline=False)
            await ctx.send(embed=embedSearch)

            def check(m):
                return m.author.id == ctx.author.id and m.content.isdecimal()

            responseNo = await self.bot.wait_for('message', check=check)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
        else:
            if search:
                track = results['tracks'][int(responseNo.content)-1]
            else:
                track = results['tracks'][0]
            player.add(requester=ctx.author.id, track=track)
        if not player.is_playing:
            await player.play()

    @commands.command()
    async def stop(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send("Not connected")
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("You are not in my voice channel!")
        player.queue.clear()
        await player.stop()
        await self.connect_channel(ctx.guild.id, None)
        await ctx.send('Disconnected')





def setup(bot):
    bot.add_cog(MusicCog(bot))
