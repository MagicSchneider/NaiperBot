import nextcord
from nextcord.ext import commands
from datetime import datetime

class Erros(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'> Módulo Carregado - "{self.__cog_name__}".')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = nextcord.Embed(color=0xf55047, timestamp=datetime.now().astimezone())
        
        #   Comandos
        if isinstance(error, commands.CommandNotFound):
            embed.add_field(name="**ERRO**", value="``Comando não existe.``", inline=False)
            await ctx.reply(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name="**ERRO**", value="``Argumentos obrigatórios não existentes.``", inline=False)
            await ctx.reply(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed.add_field(name="**ERRO**", value="``Não possui permissão para usar este comando.``", inline=False)
            await ctx.reply(embed=embed)
        if isinstance(error, commands.TooManyArguments):
            embed.add_field(name="**ERRO**", value="``Muitos argumentos.``", inline=False)
            await ctx.reply(embed=embed)
        if isinstance(error, commands.ArgumentParsingError):
            embed.add_field(name="**ERRO**", value="``Argumento inválido.``", inline=False)
            await ctx.reply(embed=embed)
            

def setup(client):
    client.add_cog(Erros(client))