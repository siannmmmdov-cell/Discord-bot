import discord
from discord.ext import commands
import os
import re
import time
import asyncio
import random
from datetime import timedelta
from flask import Flask
import threading

# Render port xatası verməsin deyə veb-server
app = Flask('')

@app.route('/')
def home():
    return "yenilmez səs sistemi aktivdir və qoruyur!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_server).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='r?', intents=intents)

spam_tracker = {}

@bot.event
async def on_ready():
    print(f'🛡️ YENİLMEZ (SƏS VƏ QORUMA) AKTİVDİR: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="r?bot | səs və qoruma aktivdir"))

@bot.event
async def on_member_join(member):
    if member.bot:
        icazeli_bot_idleri = [bot.user.id]
        if member.id not in icazeli_bot_idleri:
            try:
                await member.kick(reason="İcazəsiz bot girişinə qadağa qoyulub.")
            except:
                pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content
    lower_content = content.lower()

    # 1. Salamlaşma Sistemi (Auralı)
    words = lower_content.split()
    salam_sozleri = ["salam", "salamun aleykum", "sa", "as", "slm", "səlam"]
    if any(word in salam_sozleri for word in words):
        server_adi = message.guild.name
        cevaplar = [
            f"Aleykum salam, {message.author.mention}. `{server_adi}` ərazisindəyik.",
            f"Salam, {message.author.mention}. Sistem izləmədədir.",
            f"Aleykum salam, {message.author.mention}. Buyur, dinləyirəm."
        ]
        try:
            await message.channel.send(random.choice(cevaplar))
        except:
            pass

    # 2. Link Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite|t\.me|instagram\.com|youtube\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə link paylaşmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. @everyone Qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, @everyone qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 4. Caps Lock Qoruması
    if len(content) > 8:
        uppercase_count = sum(1 for c in content if c.isupper())
        if uppercase_count / len(content) > 0.7:
            try:
                await message.delete()
                warn = await message.channel.send(f"⚠️ {message.author.mention}, böyük hərf qadağandır!")
                await asyncio.sleep(4)
                await warn.delete()
                return
            except:
                pass

    # 5. Spam / Flood Qoruması
    author_id = message.author.id
    current_time = time.time()

    if author_id not in spam_tracker:
        spam_tracker[author_id] = []

    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 3]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) > 6:
        spam_tracker[author_id].clear()
        try:
            await message.delete()
            duration = timedelta(minutes=5)
            await message.author.timeout(duration, reason="Spam")
            await message.channel.send(f"🔇 **{message.author.mention}** spam cəhdinə görə 5 dəqiqəlik susduruldu.")
        except:
            pass
        return

    await bot.process_commands(message)

# --- İDARƏETMƏ VƏ PANEL ---
@bot.command(name="bot")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="👑 yenilmez - Gelişmiş Təhlükəsizlik və Səs Paneli",
        description="Server yenilmez sistemi tərəfindən idarə olunur. Əmrlər:",
        color=discord.Color.dark_theme()
    )
    embed.add_field(name="🔒 Müdafiə Modulları", value="Avtomatik Salam, Link, Spam Mute, Caps Lock filtri.", inline=False)
    embed.add_field(name="🎧 Səs / Musiqi", value="`r?qosul`, `r?ayril`", inline=False)
    embed.add_field(name="⚙️ Moderasiya", value="`r?sil [say]`, `r?ban [@istifadəçi]`, `r?at [@istifadəçi]`, `r?mute [@istifadəçi] [dəqiqə]`", inline=False)
    embed.add_field(name="🎮 Əyləncə", value="`r?ping`, `r?zar`, `r?yazıqtura`, `r?zarafat`, `r?status`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="status")
async def status(ctx):
    embed = discord.Embed(
        title="🛡️ yenilmez - Sistem Statusu",
        description=f"Server və səs modulları aktivdir.",
        color=discord.Color.green()
    )
    embed.add_field(name="Vəziyyət", value="🟢 Stabil", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Gecikmə", description=f"`{latency}ms`", color=discord.Color.blue())
    await ctx.send(embed=embed)

# --- SƏS (VOICE) ƏMRLƏRİ ---
@bot.command(name="qosul")
async def qosul(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"🔊 Səs kanalına qoşuldum: **{channel.name}**")
    else:
        await ctx.send("❌ Əvvəlcə hər hansı bir səs kanalına qoşulmalısan!")

@bot.command(name="ayril")
async def ayril(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Səs kanalından ayrıldım.")
    else:
        await ctx.send("❌ Bot heç bir səs kanalında deyil!")

# --- MODERASİYA ƏMRLƏRİ ---
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ `{amount}` ədəd mesaj silindi.")
    await msg.delete(delay=3)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** ban olundu.")

@bot.command(name="at")
@commands.has_permissions(kick_members=True)
async def at(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.mention}** qovuldu.")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Səbəb yoxdur"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"🔇 **{member.mention}** {minutes} dəqiqə susduruldu.")

# --- OYUNLAR ---
@bot.command(name="zar")
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 Zər: **{sayi}**")

@bot.command(name="yazıqtura")
async def yazıqtura(ctx):
    netice = random.choice(["Yazı 🦅", "Tura 🪙"])
    await ctx.send(f"🪙 Nəticə: **{netice}**")

@bot.command(name="zarafat")
async def zarafat(ctx):
    latifeler = [
        "Müəllim şagirdə: — De görüm, su nişanı nədir? Şagird: — Suya basanda görünür müəllim! 😄",
        "İki dana dəni kosmosdan gəlir, biri deyir: 'Ay nə gözəl yer idi, gəl bir də gedək!' 🚀"
    ]
    await ctx.send(random.choice(latifeler))

token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
        
