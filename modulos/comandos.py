from datetime import datetime

import nextcord
from nextcord.ext import commands
from utils.vars import channel_bv, channel_status, bot

class comandos(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'> Módulo Carregado - "{self.__cog_name__}".')
        self.channel_bv = self.client.get_channel(channel_bv)
        self.channel_status = self.client.get_channel(channel_status)

    @commands.command()
    async def avatar(self, ctx, user: nextcord.User = None):
        embed = nextcord.Embed(
            title=f"**Avatar de {user.name}:**",
            timestamp=datetime.utcnow(),
            color=0xf003fc)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text=f'Pedido por: {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def limpar(self, ctx, num:int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=num)
        if num > 1:
            await ctx.send(f'**{num} Mensagens deletadas.**', delete_after=3)
        else:
            await ctx.send(f'**{num} Mensagem deletada.**', delete_after=3)

    @commands.command()
    async def dado(self, ctx, dado, num):
        from random import randint
        num = int(num)
        inde = str(dado).upper()

        if inde not in 'D20D8D6' or num > 20:
            embed = nextcord.Embed(color=0xf003fc)
            embed.add_field(
                name=f'**Erro no comando**',
                value=f'Syntax: >dado (Arg1) (Arg2)'
                      f'``Arg1 = Tente usar D20, D8 ou D6.``\n'
                      f'``Arg2 = Limite de dados excedido (Limite = 20).``')
            await ctx.reply(embed=embed, mention_author=False, delete_after=3)
        else:
            embed = nextcord.Embed(title=f'**Rolando {num} dados {inde}**', timestamp=datetime.utcnow(), color=0xfc54ff)
            embed.description=f'**Resultado:**'
            if inde in 'D20':
                for i in range(0, num):
                    embed.add_field(name=f'**Dado {i+1}**', value=f'``{randint(1, 20)}``', inline=False)
            elif inde in 'D8':
                for i in range(0, num):
                    embed.add_field(name=f'**Dado {i+1}**', value=f'``{randint(1, 8)}``', inline=False)
            elif inde in 'D6':
                for i in range(0, num):
                    embed.add_field(name=f'**Dado {i+1}**', value=f'``{randint(1, 6)}``', inline=False)
            await ctx.reply(embed=embed, mention_author=False)
    
    @commands.is_owner()
    @commands.command()
    async def status(self, ctx, stat):
        status = str(stat).upper()

        channel = bot.get_channel(channel_status)

        await channel.purge()

        embed = nextcord.Embed(
        title="**STATUS ATUAL:**",
        timestamp=datetime.now().astimezone(),
        color=0xf003fc)

        if status not in "ONOFFMANU":
            return
        else:
            if status in "ON":
                embed.add_field(name="\u200b", value="**Online**", inline=False)
                embed.set_thumbnail(url="https://www.theflockingshop.co.uk/ekmps/shops/theflockingshop/images/neon-green-802c-239-p.jpg")

            elif status in "OFF":
                embed.add_field(name="\u200b", value="**Offline**", inline=False)
                embed.set_thumbnail(url="https://syowindo.com/wp-content/uploads/2019/10/red.jpg")

            elif status in "MANU":
                embed.add_field(name="\u200b", value="**Em Manutenção**", inline=False)
                embed.set_thumbnail(url="https://www.mbfg.co.uk/user/products/sil_pig_yellow.jpg")
            
            channel = bot.get_channel(channel_status)
            await channel.send(embed=embed)

#   validando a classe como cog
def setup(bot):
    bot.add_cog(comandos(bot))
