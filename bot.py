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
    return "yenilmez sistemi aktivdir və qoruyur!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_server).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Prefix r? olaraq təyin olundu
bot = commands.Bot(command_prefix='r?', intents=intents)

# Spam və flood izləmə lüğəti
spam_tracker = {}

@bot.event
async def on_ready():
    print(f'🛡️ YENİLMEZ SİSTEMİ AKTİVDİR: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="r?bot | yenilmez aktivdir"))

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

    # Adminlərə heç bir qoruma məhdudiyyəti şamil olunmur
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content
    lower_content = content.lower()

    # 1. Salamlaşma Sistemi
    words = lower_content.split()
    salam_sozleri = ["salam", "salamun aleykum", "sa", "as", "slm", "səlam"]
    if any(word in salam_sozleri for word in words):
        server_adi = message.guild.name
        cevaplar = [
            f"Aleykum salam, {message.author.mention}. `{server_adi}` kanalına xoş gəldin.",
            f"Salam, {message.author.mention}. Günün necə keçir?",
            f"Aleykum salam, {message.author.mention}. Xoş gördük."
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
                warn = await message.channel.send(f"⚠️ {message.author.mention}, həddindən artıq böyük hərf istifadəsi qadağandır!")
                await asyncio.sleep(4)
                await warn.delete()
                return
            except:
                pass

    # 5. Ağıllı Basqın və Flood Qoruması (Dostların randomlarına toxunmur)
    author_id = message.author.id
    current_time = time.time()

    if author_id not in spam_tracker:
        spam_tracker[author_id] = []

    # Son 3 saniyə içində yazılan mesajları izləyirik
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 3]
    spam_tracker[author_id].append(current_time)

    # Əgər kimsə 3 saniyədə 6-dan ÇOX mesaj yazarsa (həqiqi basqın)
    if len(spam_tracker[author_id]) > 6:
        spam_tracker[author_id].clear()
        try:
            await message.delete()
        except:
            pass

        try:
            duration = timedelta(minutes=5)
            await message.author.timeout(duration, reason="Həddindən artıq sürətli mesaj (Spam/Basqın)")
            await message.channel.send(f"🔇 **{message.author.mention}** spam cəhdinə görə 5 dəqiqəlik susduruldu.")
        except:
            pass
        return

    await bot.process_commands(message)

# --- İDARƏETMƏ VƏ PANEL ƏMRLƏRİ (r?bot) ---
@bot.command(name="bot")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="👑 yenilmez - Təhlükəsizlik və İdarəetmə Paneli",
        description="Server yenilmez sistemi tərəfindən qorunur. Mövcud əmrlər:",
        color=discord.Color.dark_theme()
    )
    embed.add_field(name="🔒 Müdafiə Modulları", value="Avtomatik Salam, Link/Reklam, Spam Mute, Caps Lock filtri aktivdir.", inline=False)
    embed.add_field(name="⚙️ Moderasiya", value="`r?sil [say]`, `r?ban [@istifadəçi]`, `r?at [@istifadəçi]`, `r?mute [@istifadəçi] [dəqiqə]`", inline=False)
    embed.add_field(name="🎮 Əyləncə", value="`r?ping`, `r?zar`, `r?yazıqtura`, `r?zarafat`, `r?status`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="status")
async def status(ctx):
    embed = discord.Embed(
        title="🛡️ yenilmez - Sistem Statusu",
        description=f"Server hazırda **yenilmez** tərəfindən 7/24 idarə olunur.",
        color=discord.Color.green()
    )
    embed.add_field(name="Vəziyyət", value="🟢 Stabil və İşlək", inline=True)
    embed.add_field(name="Aktiv Qoruma", value="Link, Spam, Flood, İcazəsiz Botlar", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 yenilmez - Bağlantı Sürəti", description=f"Gecikmə dəyəri: `{latency}ms`", color=discord.Color.blue())
    await ctx.send(embed=embed)

# 1. Mesaj Təmizləmə
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ `{amount}` ədəd mesaj təmizləndi.")
    await msg.delete(delay=3)

# 2. Ban Əmri
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.mention}** serverdən uzaqlaşdırıldı. Səbəb: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Xəta baş verdi: {e}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu əmri işlətmək üçün 'Ban Members' səlahiyyətiniz yoxdur.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Doğru istifadə: `r?ban @istifadəçi səbəb`")

# 3. Atmaq (Kick) Əmri
@bot.command(name="at")
@commands.has_permissions(kick_members=True)
async def at(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 **{member.mention}** serverdən qovuldu. Səbəb: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Xəta baş verdi: {e}")

@at.error
async def at_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu əmri işlətmək üçün 'Kick Members' səlahiyyətiniz yoxdur.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Doğru istifadə: `r?at @istifadəçi səbəb`")

# 4. Mute (Timeout) Əmri
@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Səbəb yoxdur"):
    try:
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🔇 **{member.mention}** `{minutes}` dəqiqə müddətinə susduruldu. Səbəb: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Xəta baş verdi: {e}")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu əmri işlətmək üçün səlahiyyətiniz yoxdur.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Doğru istifadə: `r?mute @istifadəçi [dəqiqə]`")

# --- OYUNLAR VƏ ƏYLƏNCƏ ---
@bot.command(name="zar")
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 yenilmez zər atdı: **{sayi}**")

@bot.command(name="yazıqtura")
async def yazıqtura(ctx):
    netice = random.choice(["Yazı 🦅", "Tura 🪙"])
    await ctx.send(f"🪙 yenilmez nəticəni açıqlayır: **{netice}**")

@bot.command(name="zarafat")
async def zarafat(ctx):
    latifeler = [
        "Müəllim şagirdə: — De görüm, su nişanı nədir? Şagird: — Suya basanda görünür müəllim! 😄",
        "İki dana dəni kosmosdan gəlir, biri deyir: 'Ay nə gözəl yer idi, gəl bir də gedək!' 🚀",
        "İnternetin o qədər yavaşdır ki, 'Google' axtarışa verəndə cavab gələnə kimi əsr dəyişir. 💻"
    ]
    await ctx.send(random.choice(latifeler))

# --- BOTU İŞƏ SALMA ---
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
           
