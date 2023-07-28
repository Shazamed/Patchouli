from discord.ext import commands
import discord
from discord import app_commands
import lavalink


class LavalinkVoiceClient(discord.VoiceClient):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://discordpy.readthedocs.io/en/latest/api.html#voiceprotocol
    """
    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel
        # ensure a client already exists
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                'localhost',
                6000,
                'shazam',
                'asia',
                'music-node'
            )
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
            't': 'VOICE_SERVER_UPDATE',
            'd': data
        }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
            't': 'VOICE_STATE_UPDATE',
            'd': data
        }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool, self_deaf: bool = False, self_mute: bool = False) -> None:
        """
        Connect the bot to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        # ensure there is a player_manager when creating a new voice_client
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel, self_mute=self_mute, self_deaf=self_deaf)

    async def disconnect(self, *, force: bool = False) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        # no need to disconnect if we are not connected
        if not force and not player.is_connected:
            return

        # None means disconnect
        await self.channel.guild.change_voice_state(channel=None)

        # update the channel_id of the player to None
        # this must be done because the on_voice_state_update that would set channel_id
        # to None doesn't get dispatched after the disconnect
        player.channel_id = None
        self.cleanup()


class MusicCog(commands.Cog, name='Music'):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, "lavalink"):
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('localhost', 6000, 'shazam', 'asia', 'music_node')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    # async def check_guild(self, ctx):
    #     guild_check = ctx.guild is not None
    #     if guild_check:
    #         await self.ensure_voice(ctx)
    #     return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def ensure_voice(self, interactions):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(interactions.guild.id)
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = interactions.command.name in ('play','skip','stop')
        # should_connect = True
        if not interactions.user.voice or not interactions.user.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            raise commands.CommandInvokeError('Join a voice channel first.')

        v_client = interactions.guild.voice_client
        if not v_client:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = interactions.user.voice.channel.permissions_for(interactions.guild.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', interactions.channel.id)
            await interactions.user.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if v_client.channel.id != interactions.user.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voice channel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = event.player.guild_id
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    @app_commands.command(name="play")
    async def play(self, interactions: discord.Interaction, song: str):
        await self.cog_before_invoke(interactions)
        player = self.bot.lavalink.player_manager.get(interactions.guild.id)

        if song.startswith("http"):
            query = song
            search = False
        else:
            query = f'ytsearch:{song}'
            search = True

        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await interactions.response.send_message('Perhaps the archives are incomplete!')
        if search:
            tracks = results['tracks'][0:10]
            embed_search = discord.Embed(title='Select song by replying with integer of the choice', colour=0xc566ed)
            i = 0
            for track in tracks:
                i += 1
                embed_search.add_field(name=f'{i}. {track["info"]["title"]}', value=f'{track["info"]["uri"]}', inline=False)
            await interactions.response.send_message(embed=embed_search)

            def check(m):
                return m.author.id == interactions.user.id and m.content.isdecimal()

            response_num = await self.bot.wait_for('message', check=check)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=interactions.user.id, track=track)
        else:
            if search:
                track = results['tracks'][int(response_num.content)-1]
            else:
                track = results['tracks'][0]
            print(track)
            player.add(requester=interactions.user.id, track=track)

        if not player.is_playing:
            await player.play()

    @commands.command()
    async def play2(self, ctx, *, arg=None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if arg is None:
            return await ctx.send("Usage !play <URL or search term>")
        elif arg.startswith("http"):
            query = arg
            search = False
        else:
            query = f'ytsearch:{arg}'
            search = True

        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send('Perhaps the archives are incomplete!')
        if search:
            tracks = results['tracks'][0:10]
            embed_search = discord.Embed(title='Select song by replying with integer of the choice', colour=0xc566ed)
            i = 0
            for track in tracks:
                i += 1
                embed_search.add_field(name=f'{i}. {track["info"]["title"]}', value=f'{track["info"]["uri"]}',
                                       inline=False)
            await ctx.send(embed=embed_search)

            def check(m):
                return m.author.id == ctx.author.id and m.content.isdecimal()

            response_num = await self.bot.wait_for('message', check=check)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
        else:
            if search:
                track = results['tracks'][int(response_num.content) - 1]
            else:
                track = results['tracks'][0]
            print(track)
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

    @app_commands.command(name="stop")
    async def stop(self, interactions: discord.Interaction):
        player = self.bot.lavalink.player_manager.get(interactions.guild.id)
        # if player is None:
        #     return await interactions.send("Use the !play command first")
        # if not player.is_connected:
        #     return await interactions.send("I'm not in a voice channel!")
        # if not ctx.author.voice or (player.is_connected and interactions.user.voice.channel.id != int(player.channel_id)):
        #     return await ctx.send("You are not in my voice channel!")
        await self.cog_before_invoke(interactions)
        player.queue.clear()
        await player.stop()

        # disconnect bot
        guild_id = interactions.guild.id
        guild = self.bot.get_guild(guild_id)
        await guild.voice_client.disconnect(force=True)
        await interactions.response.send_message('Disconnected')

    @app_commands.command(name="skip")
    async def skip(self, interactions: discord.Interaction):
        player = self.bot.lavalink.player_manager.get(interactions.guild.id)
        # if player is None:
        #     return await ctx.send("Use the !play command first")
        # if not player.is_connected:
        #     return await ctx.send("I'm not in a voice channel!")
        # if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
        #     return await ctx.send("You are not in my voice channel!")
        await player.skip()
        await interactions.response.send_message("Skipping current song")

    @app_commands.command()
    async def shuffle(self, interactions: discord.Interaction):
        player = self.bot.lavalink.player_manager.get(interactions.guild.id)
        # if player is None:
        #     return await ctx.send("Use the !play command first")
        # if not player.is_connected:
        #     return await ctx.send("I'm not in a voice channel!")
        # if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
        #     return await ctx.send("You are not in my voice channel!")
        player.set_shuffle(not player.shuffle)
        await interactions.response.send_message(f"Shuffling {player.shuffle}")

    @app_commands.command(name="loop")
    async def loop(self, interactions: discord.Interaction):
        player = self.bot.lavalink.player_manager.get(interactions.guild.id)
        # if player is None:
        #     return await ctx.send("Use the !play command first")
        # if not player.is_connected:
        #     return await ctx.send("I'm not in a voice channel!")
        # if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
        #     return await ctx.send("You are not in my voice channel!")
        player.set_repeat(not player.repeat)
        await interactions.response.send_message(f"Looping {player.repeat}")


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
