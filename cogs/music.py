from discord.ext import commands
import youtube_dl
import os
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

    async def connect_channel(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command()
    async def play(self, ctx, arg=None):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        if ctx.author.voice is None:
            return await ctx.send("Join a voice channel first")
        if arg is None:
            return await ctx.send("Usage !play <URL or search term>")

        if voice_client is None:
            player.store('channel', ctx.channel.id)
            await self.connect_channel(ctx.guild.id, ctx.author.voice.channel.id)

        player = self.bot.music.player_manager.get(ctx.guild.id)
        results = await player.node.get_tracks(arg)
        print(results)
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
        else:
            track = results['tracks'][0]
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
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
        await ctx.send('Disconnected.')





def setup(bot):
    bot.add_cog(MusicCog(bot))
