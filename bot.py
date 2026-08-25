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

# Render port xətası verməsin deyə veb-server
app = Flask('')

@app.route('/')
def home():
    return "Kral Bot aktivdir!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_server).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=".", intents=intents)

# Güvənlik və Spam izləmə lüğətləri
spam_tracker = {}
spam_warnings = {}

@bot.event
async def on_ready():
    print(f"👑 KRAL BOT AKTİVDİR: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Server Qorunur | .yardim"))

# --- +1000000 GÜVƏNLİK VƏ QORUMA SİSTEMİ ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Adminlərə güvənlik qadağaları şamil olunmur
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content

    # 1. Reklam, Discord dəvəti və Link Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite|t\.me|instagram\.com|tiktok\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə reklam, link və dəvət atmaq qəti qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 2. @everyone və @here Spam Qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, @everyone və ya @here atmၵ qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. Həddindən artıq Böyük Hərf (Caps Lock) Qoruması (>70%)
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

    # 4. Sürətli Spam (Flood) Qoruması
    author_id = message.author.id
    current_time = time.time()
    
    if author_id not in spam_tracker:
        spam_tracker[author_id] = []
    
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) >= 4:
        spam_tracker[author_id].clear()
        if author_id not in spam_warnings:
            spam_warnings[author_id] = 0
        spam_warnings[author_id] += 1
        
        try:
            await message.delete()
        except:
            pass

        warn_count = spam_warnings[author_id]
        if warn_count == 1:
            await message.channel.send(f"⚠️ {message.author.mention}, spam etməyi dayandır!")
        elif warn_count >= 2:
            try:
                await message.author.timeout(timedelta(minutes=3), reason="Sürətli spam (Flood)")
                await message.channel.send(f"⏳ {message.author.mention}, spam yazdığı üçün 3 dəqiqəlik mute (timeout) aldı!")
            except:
                pass
        return

    await bot.process_commands(message)

# --- İDARƏETMƏ VƏ MODERASİYA ƏMRLƏRİ ---
@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="👑 Kral Bot - İdarəetmə və Qoruma Paneli",
        description="Serverin bütün güvənliyi və əyləncəsi bu botdadır, Ruhum:",
        color=discord.Color.gold()
    )
    embed.add_field(name="🛡️ Güvənlik", value="Reklam, Link, Caps Lock, Everyone və Spam avtomatik qorunur (+1000000).", inline=False)
    embed.add_field(name="🧹 `.sil [say]`", value="Göstərilən qədər mesajı silir.", inline=False)
    embed.add_field(name="🔨 `.ban [@istifadəçi]`", value="Qayda pozan şəxsi banlayır.", inline=False)
    embed.add_field(name="⏳ `.mute [@istifadəçi] [dəqiqə]`", value="İstifadəçini müvəqqəti susdurur.", inline=False)
    embed.add_field(name="🎮 Əyləncə Əmrləri", value="`.zar` - Zər atır | `.zarafat` - Lətifə deyir | `.ping` - Gecikməni yoxlayır", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Botun gecikmə sürəti: **{latency}ms**", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 **{amount}** ədəd mesaj təmizləndi!", delete_after=3)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** serverdən ban olundu! Səbəb: *{reason}*")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Qayda pozuntusu"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"⏳ **{member.mention}** {minutes} dəqiqə müddətinə susduruldu!")

# --- ƏYLƏNCƏ ƏMRLƏRİ ---
@bot.command(name="zar")
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 Zər atıldı və düşən rəqəm: **{sayi}**!")

@bot.command(name="zarafat")
async def zarafat(ctx):
    zarafatlar = [
        "Müəllim şagirdə: — De görüm, Su nişanı nədir? Şagird: — Suya basdırdığımız möhür müəllim? 😄",
        "İki dənə dəli kosmosdan gəlir, biri deyir: 'Ay nə gözəl yer idi, amma havanı heç bəyənmədim.' 🚀",
        "– Ana, ata niyə göydə uçur? – Lal ol, uje hündürdən atma özünü!",
        "İnternetim o qədər yavaşdır ki, 'Google' axtarışa verəndə cavabını gələn il öyrənəcəm."
    ]
    await ctx.send(random.choice(zarafatlar))

# Token oxuma və işə salma
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
          
