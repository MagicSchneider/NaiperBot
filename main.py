import os
from utils.vars import bot, mcarregados, bot_token

for modulo in os.listdir('./modulos/'): 
    #   carrega modulos .py que não começam com _
    if modulo.endswith('.py') and not modulo.startswith('_'):
        bot.load_extension(f'modulos.{modulo[:-3]}')
        mcarregados.append(modulo[:-3])

for modulo in os.listdir('./music/'):
    #   carrega modulos .py que não começam com _
    if modulo.endswith('.py') and not modulo.startswith('_'):
        bot.load_extension(f'music.{modulo[:-3]}')
        mcarregados.append(modulo[:-3])

print(f'\n*Debug main.py (Carregando módulos...) {mcarregados}\n')

# ALTERNATIVA PARA NÃO USAR O CTX NAS FUNÇÕES:
# ctx = self.client.get_context

bot.run(bot_token)
