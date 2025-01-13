import discord
from discord.ext import commands
import src.events
import src.util
import src.com
from src.util import config

# Konfigurasi intents
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

# Inisialisasi bot
bot = commands.Bot(command_prefix=config['PREFIX'], intents=intents)

# Setup events dan commands
src.events.setup(bot)
src.com.setup(bot)

# Menjalankan bot dengan penanganan error
try:
    bot.run(config['DISCORD_TOKEN'])
except Exception as e:
    print(f"Error when running the bot: {e}")