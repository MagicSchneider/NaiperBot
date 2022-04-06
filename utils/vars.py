from nextcord import Intents
import nextcord
import utils.jsonloader
from nextcord.ext import commands
import os

mcarregados = []

#  lê o arquivo config.json como variavel
config_file = utils.jsonloader.read_json('./utils/', 'config')
guilds_ = utils.jsonloader.read_json('./modulos/', 'guild_ids')
play_bot = utils.jsonloader.read_json('./music/', 'playlist')
save_song = utils.jsonloader.read_json('./music/', 'last_song')
#   usa a variavel config_file para acessar os valores do config.json

channel_bv = int(config_file["channel_bv"])
channel_status = int(config_file["bot_status"])

bot_token = str(config_file["BotToken"])
server_id = int(config_file["ServerID"])
log_channel = int(config_file["LogChannel"])

Intents = nextcord.Intents.all()
Intents.members = True
Intents.voice_states = True
Intents.guilds

Atividade = nextcord.Activity(type=nextcord.ActivityType.playing, afk=False, name="OnlyTest")

bot = commands.Bot(
    help_command=None,
    command_prefix=">",
    intents=Intents,
    activity=Atividade,
    owner_id = os.environ["BOT_OWNER_ID"])
