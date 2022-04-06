from nextcord.ext import commands
from nextcord import FFmpegPCMAudio, Embed

from utils.vars import play_bot, guilds_, save_song, bot

from pytube import YouTube
from youtube_dl import YoutubeDL
import youtube_dl

import asyncio
import utils.jsonloader

from datetime import datetime

from youtubesearchpython import VideosSearch

class musica_prot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'> Módulo Carregado - "{self.__cog_name__}".')

    # FUNÇÃO PARA CHECAR PLAYLIST
    async def check_queue(self, ctx):
        if play_bot[str(ctx.guild.id)] == 0:
            ctx.voice_client.stop()

            embed = Embed(
                title='',
                color=0xFF632C,
                timestamp=datetime.now().astimezone())

            await ctx.send(embed=embed)
        else:
            ctx.voice_client.stop()

            YDL_OPTIONS = {
            'format': 'bestaudio',
            'noplaylist': 'True',
            'format': 'bestaudio/best',
            'extractaudio' : True}

            with YoutubeDL(YDL_OPTIONS) as ydl:
                info_video = ydl.extract_info(
                    play_bot[str(ctx.guild.id)][0],
                    download=False)

            await self.song_play(ctx, info_video['url'])

    # FUNÇÃO PARA TOCAR MÚSICA
    async def song_play(self, ctx, url):
        ffmpeg_options = {
        'options': '-vn',
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"}

        ctx.voice_client.play(FFmpegPCMAudio(
            url,
            **ffmpeg_options),
            after=lambda e: self.check_queue(ctx))
        
        save_song[str(ctx.guild.id)] = play_bot[str(ctx.guild.id)][0]
        play_bot[str(ctx.guild.id)].pop(0)

        musica = YouTube(save_song[str(ctx.guild.id)])
        
        embed = Embed(
            title=f"Tocando agora:",
            timestamp=datetime.now().astimezone(),
            color=0xFF632C)

        name = musica.title
        link = save_song[str(ctx.guild.id)]

        embed.set_thumbnail(url=musica.thumbnail_url)
        embed.description=f'**[{name}]({link})**\n\n *Enviado por: ``{musica.author}``*'
        embed.set_footer(text=f'Pedido por: {ctx.message.author}', icon_url=ctx.message.author.avatar.url)

        channel = bot.get_channel(int(guilds_[f'{ctx.guild.id}']['last_channel']))
        await channel.send(embed=embed)

        utils.jsonloader.write_json(save_song, './music/', 'last_song')
        utils.jsonloader.write_json(play_bot, './music/', 'playlist')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if not member.id == self.bot.user.id:
            return

        # elif member.id

        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == 60:
                    await voice.disconnect()

                    guild = after.channel.guild.id
                    channel = bot.get_channel(int(guilds_[str(guild)]["last_channel"]))
                    
                    embed = Embed(
                        title=f"**Saindo do canal de voz por inatividade.**",
                        color=0xFF632C,
                        timestamp=datetime.now().astimezone())

                    await channel.send(embed=embed)

                if not voice.is_connected():
                    break
        
    # FUNÇÃO PARA ADICIONAR PLAYLIST
    @commands.command()
    async def play(self, ctx, url):
        _temp = url.lower()

        pass_test = False

        if 'youtube.com' in _temp or 'youtu.be' in _temp:
            if not 'list' in _temp:
                # FUNÇÃO ONE MUSIC
                print('One Music func = Load')

                play_bot[str(ctx.guild.id)].append(url)
                utils.jsonloader.write_json(play_bot, './music/', 'playlist')

            else:
                # FUNÇÃO PLAYLIST
                print('Playlist func = Load')
                if len(play_bot[str(ctx.guild.id)]) == 0:
                    YDL_OPTIONS = {
                    'format': 'bestaudio',
                    'format': 'bestaudio/best',
                    'extractaudio' : True,
                    'noplaylist' : True}

                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as (ydl):
                        extra = ydl.extract_info(url, download=False)

                    link = 'https://www.youtube.com/watch?v=' + extra['id']
                    
                    play_bot[str(ctx.guild.id)].append(link)
                    utils.jsonloader.write_json(play_bot, './music/', 'playlist')
                    
                    pass_test = False
                    await self.check_queue(ctx)

                YDL_OPTIONS = {
                'format': 'bestaudio',
                'format': 'bestaudio/best',
                'extractaudio' : True}

                with youtube_dl.YoutubeDL(YDL_OPTIONS) as (ydl):
                    extra = ydl.extract_info(url, download=False)

                if len(extra["entries"])<1:
                    print('Error : No video found in playlist, probably no public videos in the playlist.')
                    return
                    
                for video in extra['entries']:
                    link = 'https://www.youtube.com/watch?v=' + video['id']
                    play_bot[str(ctx.guild.id)].append(link)
                    utils.jsonloader.write_json(play_bot, './music/', 'playlist')
                
                if pass_test == False:
                    play_bot[str(ctx.guild.id)].pop(0)
                    utils.jsonloader.write_json(play_bot, './music/', 'playlist')
                else:
                    await self.check_queue(ctx)

                # ========MENSAGEM PARA NOTIFICAR A PLAYLIST ADICIONADA========
                embed = Embed(
                    title=f"**Playlist adicionada.**",
                    timestamp=datetime.now().astimezone(),
                    color=0xFF632C)
                    
                test = len(extra['entries'])
                titulo = extra['title']
                link = url
                embed.description=f'**[{titulo}]({url})**'
                embed.set_image(url='https://i.imgur.com/4M7IWwP.gif')
                embed.set_footer(text=f'{test} tracks adicionadas')

                await ctx.reply(embed=embed, mention_author=False)
                return

        else:
            # FUNÇÃO NAME SEARCH
            print('#Search')
            text = ctx.message.content
            text = text[6::].strip().replace(' ', '_')

            print(ctx.message.content)
            videosSearch = VideosSearch(text, limit = 1)
            res = videosSearch.result()

            final = 'https://www.youtube.com/watch?v=' + res['result'][0]['id']

            print(res)

            play_bot[str(ctx.guild.id)].append(final)
            utils.jsonloader.write_json(play_bot, './music/', 'playlist')

            #
            music = YouTube(final)
            embed = Embed(
                title='**Música adicionada.**',
                timestamp=datetime.now().astimezone(),
                color=0xFF632C)

            teste = len(play_bot[str(ctx.guild.id)])

            embed.description = str(
                # f"**[{music.title}]({final})**"
                f"\n\n**Posição ``{teste}`` na fila de reprodução.**")
            embed.set_image(url='https://i.imgur.com/4M7IWwP.gif')

            await ctx.reply(embed=embed, mention_author=False)
            
            await self.check_queue(ctx)
            return
        

        if ctx.voice_client.is_playing():
            music = YouTube(url)
            
            embed = Embed(
                title='**Música adicionada.**',
                timestamp=datetime.now().astimezone(),
                color=0xFF632C)

            teste = len(play_bot[str(ctx.guild.id)])

            embed.description = str(
                f"**[{music.title}]({url})**"
                f"\n\n**Posição ``{teste}`` na fila de reprodução.**")
            embed.set_image(url='https://i.imgur.com/4M7IWwP.gif')

            await ctx.reply(embed=embed, mention_author=False)
        else:
            await self.check_queue(ctx)

    # FUNÇÕES COMPLEMENTARES
    @commands.command()
    async def queue(self, ctx):

        quant = len(play_bot[str(ctx.guild.id)])

        embed = Embed(
            title="Músicas na fila:",
            timestamp=datetime.now().astimezone(),
            color=0xFF632C)

        text = ''

        cont = 0
        for i in range(0, quant):
            video_info = YouTube(play_bot[str(ctx.guild.id)][i])
            cont += 1
            text += f"**{i+1} ▸ ``" + video_info.title + '``**\n'
            if cont > 9:
                break
        
        if len(play_bot[str(ctx.guild.id)]) > 10:
            embed.description = f"{text}\n**E outras {len(play_bot[str(ctx.guild.id)])-9}.**"
        else:
            embed.description = f"{text}\n"
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        await ctx.reply(f'**Pulando para a próxima música...**', mention_author=False)
        
    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.reply(f'**Continuando..**', mention_author=False)
    
    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.reply(f'**Música pausada. (-resume para continuar)**', mention_author=False)
    
    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        play_bot[str(ctx.guild.id)].clear()
        await ctx.voice_client.disconnect()
        utils.jsonloader.write_json(play_bot, './music/', 'playlist')

        await ctx.reply('**Até logo!**', mention_author=False)

    @commands.command()
    async def clear(self, ctx):
        if ctx.voice_client.is_connected():
            ctx.voice_client.stop()

            play_bot[str(ctx.guild.id)].clear()
            utils.jsonloader.write_json(play_bot, './music/', 'playlist')
            
            await ctx.reply(f'**Playlist limpa com sucesso!**', mention_author=False)
        else:
            play_bot[str(ctx.guild.id)].clear()
            utils.jsonloader.write_json(play_bot, './music/', 'playlist')

    # CONFIG INICIAL APÓS O PLAY
    @play.before_invoke
    async def ensure_voice(self, ctx):
        guilds_[f'{ctx.guild.id}']['last_channel'] = str(ctx.channel.id)
        utils.jsonloader.write_json(guilds_, './modulos/', 'guild_ids')

        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.reply("**Você não está conectado em um canal de voz.**", mention_author=False)
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            print('Ignorando "before invoke".')
            
def setup(bot):
    bot.add_cog(musica_prot(bot))