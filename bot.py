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

# Spam və flood izləmə lüğəti
spam_tracker = {}

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

    # Adminlərə heç bir qoruma məhdudiyyəti düşmür
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content
    lower_content = content.lower()

    # 1. Salamlaşma Sistemi (Rəsmi və təmiz)
    words = lower_content.split()
    salam_sozleri = ["salam", "salamun aleykum", "sa", "as", "slm", "səlam"]
    if any(word in salam_sozleri for word in words):
        server_adi = message.guild.name
        cevaplar = [
            f"Aleykum salam, {message.author.mention}! `{server_adi}` serverinə xoş gəldin.",
            f"Salam, {message.author.mention}! Necəsən, günün necə keçir?",
            f"Aleykum salam, {message.author.mention}! Xoş gördük."
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

    # 5. Ağıllı Basqın və Flood Qoruması (+100000000 gücləndirilmiş, amma dostlara toxunmayan)
    author_id = message.author.id
    current_time = time.time()

    if author_id not in spam_tracker:
        spam_tracker[author_id] = []

    # Son 3 saniyə içində yazılan mesajları izləyirik
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 3]
    spam_tracker[author_id].append(current_time)

    # Əgər kimsə 3 saniyə içində 6-dan ÇOX mesaj yazarsa (həqiqi basqın/spam halı)
    if len(spam_tracker[author_id]) > 6:
        spam_tracker[author_id].clear()
        try:
            await message.delete()
        except:
            pass

        try:
            duration = timedelta(minutes=5)
            await message.author.timeout(duration, reason="Həddindən artıq sürətli mesaj (Spam/Basqın)")
            await message.channel.send(f"🔇 **{message.author.mention}** çatı spam etdiyi üçün 5 dəqiqəlik susduruldu.")
        except:
            pass
        return

    await bot.process_commands(message)

# --- İDARƏETMƏ VƏ PANEL ƏMRLƏRİ ---
@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="👑 Kral Bot - İdarəetmə və Təhlükəsizlik Paneli",
        description="Server tam təhlükəsizlik altındadır! Bütün əmrlər aşağıdadır:",
        color=discord.Color.gold()
    )
    embed.add_field(name="🛡️ Təhlükəsizlik və Qoruma", value="Avtomatik Salam, Link, Spam Mute, Caps Lock qoruması aktivdir.", inline=False)
    embed.add_field(name="⚡ Moderasiya", value="`!sil [say]`, `!ban [@istifadəçi]`, `!at [@istifadəçi]`, `!mute [@istifadəçi] [dəqiqə]`", inline=False)
    embed.add_field(name="🎮 Oyunlar və Əyləncə", value="`!ping`, `!zar`, `!yazıqtura`, `!zarafat`, `!sunucukoru`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="sunucukoru")
async def sunucukoru(ctx):
    embed = discord.Embed(
        title="🛡️ Sunucu Qoruma Statusu",
        description=f"Server hazırda **Kral Bot** tərəfindən 7/24 tam qorunur!",
        color=discord.Color.blue()
    )
    embed.add_field(name="Status", value="✅ Aktiv və İşlək", inline=True)
    embed.add_field(name="Qorunan Sahələr", value="Link, Reklam, Ağır Spam/Flood (Mute sistemi), Caps Lock, İcazəsiz Botlar", inline=False)
    embed.set_footer(text="Gecə-gündüz serverin güvəndədir!")
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Botun gecikmə sürəti: `{latency}ms` 🚀", color=discord.Color.green())
    await ctx.send(embed=embed)

# 1. Mesaj Təmizləmə
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ `{amount}` ədəd mesaj təmizləndi!")
    await msg.delete(delay=3)

# 2. Ban Əmri
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.mention}** serverdən ban olundu. Səbəb: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Ban etmək olmadı! Xəta: {e}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu əmri işlətmək üçün 'Ban Members' səlahiyyətiniz yoxdur.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Doğru istifadə: `!ban @istifadəçi səbəb`")

# 3. Atmaq (Kick) Əmri (!at)
@bot.command(name="at")
@commands.has_permissions(kick_members=True)
async def at(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 **{member.mention}** serverdən uzaqlaşdırıldı. Səbəb: {reason}")
    except Exception as e:
        await ctx.send(f"❌ İstifadəçini uzaqlaşdırmaq olmadı! Xəta: {e}")

@at.error
async def at_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu əmri işlətmək üçün 'Kick Members' səlahiyyətiniz yoxdur.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Doğru istifadə: `!at @istifadəçi səbəb`")

# 4. Mute (Timeout) Əmri
@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Səbəb yoxdur"):
    try:
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🔇 **{member.mention}** `{minutes}` dəqiqə müddətinə susduruldu. Səbəb: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Susdurmaq olmadı! Xəta: {e}")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu əmri işlətmək üçün səlahiyyətiniz yoxdur.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Doğru istifadə: `!mute @istifadəçi [dəqiqə]`")

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
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Xoş gəldin.")

@bot.command(name="sa")
async def sa_cmd(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Necəsən?")

@bot.command(name="slm")
async def slm_cmd(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Xoş gördük.")

# --- BOTU İŞƏ SALMA ---
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
    
