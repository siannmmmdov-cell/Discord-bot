import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# Flask ilə sadə veb server yaradırıq ki, Render yatmasın
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
    print(f"{bot.user} tam təhlükəsizlik və veb server rejimi ilə onlayn oldu!")

# 1. KƏNAR BOT QORUMASI
@bot.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.ban(reason="İcazəsiz bot əlavə edildi - Avtomatik Təhlükəsizlik Qoruması")
        except Exception as e:
            print(e)

# 2. MESAJLARA NƏZARƏT (Link və 18+ şəkil qoruması)
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # Link qoruması
    if "http://" in content or "https://" in content or "www." in content:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə link paylaşmaq qadağandır!", delete_after=5)
            return
        except Exception as e:
            print(e)

    # 18+ / Şəkil qoruması
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov')):
                try:
                    await message.delete()
                    await message.channel.send(f"⚠️ {message.author.mention}, bu kanalda şəkil/video paylaşmaq qadağandır!", delete_after=5)
                    return
                except Exception as e:
                    print(e)

    await bot.process_commands(message)

# Veb serveri işə salırıq və botu işə qoşuruq
keep_alive()
bot.run(os.environ.get("DISCORD_TOKEN"))
@bot.command()
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Server tam qorunur və mən onlaynam! 🛡️")
