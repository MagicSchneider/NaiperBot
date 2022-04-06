import nextcord
from nextcord.ext import commands
from datetime import datetime
from utils.vars import channel_bv, server_id

class mensagens(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'> Módulo Carregado - "{self.__cog_name__}".')
        self.channel_bv = self.client.get_channel(channel_bv)

    @commands.command()
    async def ajuda(self, ctx):
        embed = nextcord.Embed(
            title='**Olá, vim te ajudar com algumas coisinhas ;)**',
            color=0xf003fc)
        url = "https://discord.gg/BVApt3WGPf"

        embed.add_field(name="**\nComandos Normais:**", value=str(
            f'``-test`` \n'
            f'``-avatar (Membro)`` \n'
            f'``-limpar (Quantidade)`` \n'
            f'``-dado (D20, D8 ou D6) (Quantia)``\n'), inline=False)
        
        embed.add_field(name="**Comandos de Música:**", value=str(
            f'``-play (Link do YT)`` \n'
            f'``-skip`` \n'
            f'``-pause`` \n'
            f'``-resume`` \n'
            f'``-stop`` \n'
            f'``-clear`` \n'
            f'``-queue`` \n'), inline=False)
        
        embed.add_field(name='\u200b', value=f'***Deseja ver atualizações? Entre em nosso [Discord]({url})!***')
        
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def embedatt(self, ctx):
        embed = nextcord.Embed(
            title="**Atualização V2.2.0.1**",
            color=0xFF0000,
            timestamp=datetime.now().astimezone())
        
        embed.description=str(
            f"***Novidades do novo update:***\n\n"
            f"***Mudanças no sistema de música:***\n"
            f'**▹ A pesquisa por nome foi habilitada\n.'
            f'**▹ Mensagens visualmente melhoradas.\n'
            f'**▹ Melhora na resposta após solicitação de playlists.'
            f'**\n __(Para saber como usar, digite -ajuda)__')
        await ctx.send(embed=embed)
        await ctx.send('@everyone @here')

#   validando a classe como cog
def setup(bot):
    bot.add_cog(mensagens(bot))
