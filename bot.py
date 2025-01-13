import discord
from discord.ext import commands
import src.events
import src.util
import src.com
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description="Run the Discord bot with a specific token.")
parser.add_argument("token", type=str, nargs="?", help="The Discord bot token.")
args = parser.parse_args()

# Load configuration
config = src.util.config

# Determine token to use
token = args.token if args.token else config['DISCORD_TOKEN']

# Konfigurasi intents
intents = discord.Intents.all()

# Inisialisasi bot
bot = commands.Bot(command_prefix=config['PREFIX'], intents=intents)

# Setup events dan commands
src.events.setup(bot)
src.com.setup(bot)

# Run bot with the determined token
bot.run(token)