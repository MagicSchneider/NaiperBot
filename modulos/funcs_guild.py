from nextcord.ext import commands
from utils.vars import guilds_, play_bot, mcarregados, bot, save_song

import utils.jsonloader
import os

class guild_on(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'> Módulo Carregado - "{self.__cog_name__}".')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guilds_[f'{guild.id}'] = {}

        guilds_[f'{guild.id}']['guild_name'] = str(guild.name)
        guilds_[f'{guild.id}']['sys_channel'] = None
        guilds_[f'{guild.id}']['updates_ch'] = None
        guilds_[f'{guild.id}']['auto_role'] = None
        guilds_[f'{guild.id}']['custom_prefix'] = None
        guilds_[f'{guild.id}']['last_channel'] = None

        if guild.system_channel:
            guilds_[f'{guild.id}']['sys_channel'] = guild.system_channel.id

        utils.jsonloader.write_json(guilds_, './modulos/', 'guild_ids')

        play_bot[str(guild.id)] = []
        utils.jsonloader.write_json(play_bot, './music/', 'playlist')

        save_song[str(guild.id)] = None
        utils.jsonloader.write_json(save_song, './music/', 'last_song')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guilds_.pop(str(guild.id))
        play_bot.pop(str(guild.id))
        utils.jsonloader.write_json(guilds_, './modulos/', 'guild_ids')
        utils.jsonloader.write_json(play_bot, './music/', 'playlist')
    
    @commands.is_owner()
    @commands.command()
    async def server_reset(self, ctx):
        for guild in self.bot.guilds:

            guilds_[f'{guild.id}'] = {}

            guilds_[f'{guild.id}']['guild_name'] = str(guild.name)
            guilds_[f'{guild.id}']['sys_channel'] = None
            guilds_[f'{guild.id}']['updates_ch'] = None
            guilds_[f'{guild.id}']['auto_role'] = None
            guilds_[f'{guild.id}']['custom_prefix'] = None
            guilds_[f'{guild.id}']['last_channel'] = None

            if guild.system_channel:
                guilds_[f'{guild.id}']['sys_channel'] = guild.system_channel.id

            utils.jsonloader.write_json(guilds_, './modulos/', 'guild_ids')

            play_bot[str(guild.id)] = []
            utils.jsonloader.write_json(play_bot, './music/', 'playlist')

            save_song[str(guild.id)] = None
            utils.jsonloader.write_json(save_song, './music/', 'last_song')

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx):
        for modulo in os.listdir('./modulos/'): 
            #   carrega modulos .py que não começam com _
            if modulo.endswith('.py') and not modulo.startswith('_'):
                bot.reload_extension(f'modulos.{modulo[:-3]}')
                mcarregados.append(modulo[:-3])

        for modulo in os.listdir('./music/'):
            #   carrega modulos .py que não começam com _
            if modulo.endswith('.py') and not modulo.startswith('_'):
                bot.reload_extension(f'music.{modulo[:-3]}')
                mcarregados.append(modulo[:-3])
                
                await ctx.send('**Módulos Recarregados com sucesso!**')

def setup(bot):
    bot.add_cog(guild_on(bot))
