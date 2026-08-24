import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# Flask ilə sadə veb server (Render yatmasın deyə)
app = Flask('')

@app.route('/')
def home():
    return "Bot onlayndır və işləyir!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Discord Bot hissəsi
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} onlayndır!")

# 1. KƏNAR BOT QORUMASI (Serverə başqa bot gələndə atır)
@bot.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.ban(reason="İcazəsiz bot - Təhlükəsizlik Qoruması")
        except Exception as e:
            print(e)

# 2. MESAJLARA NƏZARƏT (Yalnız linkləri silir, şəkillərə toxunmur!)
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # Link qoruması (Mesajda link varsa silir)
    if "http://" in content or "https://" in content or "www." in content:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə link paylaşmaq qadağandır!", delete_after=5)
            return
        except Exception as e:
            print(e)

    # Botun əmrləri işləməsi üçün bu mütləqdir
    await bot.process_commands(message)

# Salam əmri
@bot.command()
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Server tam qorunur və mən onlaynam! 🛡️")

# Veb serveri işə salırıq və botu qoşuruq
keep_alive()
bot.run(os.environ.get("DISCORD_TOKEN"))
