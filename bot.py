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
    return "Kral Bot aktivdir və serveri qoruyur!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_server).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Spam və flood izləmə sistemləri
spam_tracker = {}
spam_warnings = {}

@bot.event
async def on_ready():
    print(f'👑 KRAL BOT AKTİVDİR VƏ QORUYUR: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="!yardim yaz və əylən!"))

@bot.event
async def on_member_join(member):
    if member.bot:
        icazeli_bot_idleri = [bot.user.id]
        if member.id not in icazeli_bot_idleri:
            try:
                await member.kick(reason="İcazəsiz bot girişinə qadağa qoyulub.")
                print(f"⚠️ İcazəsiz bot aşkarlandı və qovuldu: {member.name}")
            except Exception as e:
                print(f"Botu qovmaq mümkün olmadı: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Adminda olanlara qoruma qadağaları şamil olunmur
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content
    lower_content = content.lower()

    # 1. Salamlaşma Sistemi (Yalnız dəqiq söz olaraq yazıldıqda işləyir)
    words = lower_content.split()
    salam_sozleri = ["salam", "salamun aleykum", "sa", "as", "slm", "səlam"]
    if any(word in salam_sozleri for word in words):
        cevaplar = [
            f"Aleykum salam, {message.author.mention}! Xoş gəldin, necəsən? 😎",
            f"Salam, {message.author.mention}! Günün gözəl keçsin! 👑",
            f"Aleykum salam, qardaş! Bot sənin xidmətindədir. 🤖"
        ]
        try:
            await message.channel.send(random.choice(cevaplar))
        except:
            pass

    # 2. Reklam, Link və Discord Dəvəti Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite|t\.me|instagram\.com|youtube\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə link və dəvət paylaşmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. @everyone / @here Spam Qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, @everyone və ya @here qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 4. Caps Lock Qoruması (>70%)
    if len(content) > 8:
        uppercase_count = sum(1 for c in content if c.isupper())
        if uppercase_count / len(content) > 0.7:
            try:
                await message.delete()
                warn = await message.channel.send(f"⚠️ {message.author.mention}, çoxlu böyük hərf (Caps Lock) istifadə etmək qadağandır!")
                await asyncio.sleep(4)
                await warn.delete()
                return
            except:
                pass

    # 5. Sürətli Flood / Spam Qoruması
    author_id = message.author.id
    current_time = time.time()

    if author_id not in spam_tracker:
        spam_tracker[author_id] = []

    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) > 5:
        spam_tracker[author_id].clear()
        if author_id not in spam_warnings:
            spam_warnings[author_id] = 0
        spam_warnings[author_id] += 1

        try:
            await message.delete()
        except:
            pass

        if spam_warnings[author_id] >= 1:
            try:
                duration = timedelta(minutes=3)
                await message.author.timeout(duration, reason="Çox sürətli mesaj yazmaq (Flood)")
                await message.channel.send(f"🔇 {message.author.mention} həddindən artıq sürətli mesaj yazdığı üçün 3 dəqiqəlik susduruldu.")
            except:
                pass
            return

    await bot.process_commands(message)

# --- İDARƏETMƏ VƏ PANEL ƏMRLƏRİ ---
@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="👑 Kral Bot - İdarəetmə və Təhlükəsizlik Paneli",
        description="Server tam təhlükəsizlik altındadır, qardaş! Bütün əmrlər aşağıdadır:",
        color=discord.Color.gold()
    )
    embed.add_field(name="🛡️ Təhlükəsizlik və Qoruma", value="Avtomatik Salam, Link, Flood, Caps Lock və Bot Qoruması aktivdir.", inline=False)
    embed.add_field(name="⚡ Moderasiya", value="`!sil [say]`, `!ban [@istifadəçi]`, `!mute [@istifadəçi] [dəqiqə]`", inline=False)
    embed.add_field(name="🎮 Oyunlar və Əyləncə", value="`!ping`, `!zar`, `!yazıqtura`, `!zarafat`, `!sunucukoru`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="sunucukoru")
async def sunucukoru(ctx):
    embed = discord.Embed(
        title="🛡️ Sunucu Qoruma Statusu",
        description="Server hazırda **Kral Bot** tərəfindən 7/24 tam qorunur!",
        color=discord.Color.blue()
    )
    embed.add_field(name="Status", value="✅ Aktiv və İşlək", inline=True)
    embed.add_field(name="Qorunan Sahələr", value="Link, Reklam, Flood, Caps Lock, İcazəsiz Botlar", inline=False)
    embed.set_footer(text="Gecə-gündüz serverin güvəndədir!")
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Botun gecikmə sürəti: `{latency}ms` 🚀", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ `{amount}` ədəd mesaj təmizləndi!")
    await msg.delete(delay=3)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** serverdən ban olundu! Səbəb: {reason}")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Səbəb yoxdur"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"🔇 **{member.mention}** `{minutes}` dəqiqə müddətinə susduruldu.")

# --- OYUNLAR VƏ SALAM ƏMRLƏRİ ---
@bot.command(name="zar")
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 Zər atıldı və düşən rəqəm: **{sayi}**!")

@bot.command(name="yazıqtura")
async def yazıqtura(ctx):
    netice = random.choice(["Yazı 🦅", "Tura 🪙"])
    await ctx.send(f"🪙 Pul atıldı... Nəticə: **{netice}**!")

@bot.command(name="zarafat")
async def zarafat(ctx):
    latifeler = [
        "Müəllim şagirdə: — De görüm, su nişanı nədir? Şagird: — Suya basanda görünür müəllim! 😄",
        "İki dana dəni kosmosdan gəlir, biri deyir: 'Ay nə gözəl yer idi, gəl bir də gedək!' 🚀",
        "İnternetin o qədər yavaşdır ki, 'Google' axtarışa verəndə cavab gələnə kimi əsr dəyişir. 💻"
    ]
    await ctx.send(random.choice(latifeler))

@bot.command(name="salam")
async def salam_cmd(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Xoş gəldin, qardaşım! 😎")

@bot.command(name="sa")
async def sa_cmd(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Necəsən? 👑")

@bot.command(name="slm")
async def slm_cmd(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Xoş gördük! 🤖")

# --- BOTU İŞƏ SALMA ---
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
            
