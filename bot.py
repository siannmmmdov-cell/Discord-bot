import subprocess
import sys

# Avtomatik kitabxana yoxlama və yükləmə bloku
def install_pkg(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import discord
except ImportError:
    install_pkg("discord.py")
    import discord

try:
    import nacl
except ImportError:
    install_pkg("PyNaCl")

try:
    import flask
except ImportError:
    install_pkg("Flask")
    import flask

from discord.ext import commands
import os
import re
import time
import asyncio
import random
from datetime import timedelta
from flask import Flask
import threading

# ==========================================
# RENDER VEB SERVER MODULU
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "yenilmez firewall v24.0 [ULTRA SECURITY] - System Online"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_server).start()

# ==========================================
# BOT KONQİQURASİYASI
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='r?', intents=intents)

spam_tracker = {}
afk_users = {}
user_wallet = {}

# Sənin unikal sahib ID-n
SAHIB_ID = 641014966312501259

@bot.event
async def on_ready():
    print(f'🛡️ [YENİLMEZ OS // ULTRA]: Kiber şəbəkə tam güclə aktivdir -> {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="r?yardim | Server Qorunur"))

# ==========================================
# TƏHLÜKƏSİZLİK VƏ GÜCLƏNDİRİLMİŞ FİLTER SİSTEMİ
# ==========================================
@bot.event
async def on_member_join(member):
    if member.bot:
        if member.id != bot.user.id:
            try:
                await member.ban(reason="Təhlükəsizlik: İcazəsiz kənar bot inyeksiya cəhdi (Avto-Ban).")
            except:
                pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # AFK Sistem yoxlaması
    if message.author.id in afk_users:
        del afk_users[message.author.id]
        try:
            await message.channel.send(f"⚠️ Qayıtdın, {message.author.mention}. AFK rejimi ləğv edildi.", delete_after=5)
        except:
            pass

    for mention in message.mentions:
        if mention.id in afk_users:
            reason = afk_users[mention.id]
            try:
                await message.channel.send(f"💤 **{mention.name}** şu an AFK-dır. Səbəb: {reason}")
            except:
                pass

    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content
    lower_content = content.lower()

    # 1. Salamlama Sistemi
    words = lower_content.split()
    salam_sozleri = ["salam", "salamun aleykum", "sa", "slm", "səlam"]
    if any(word in salam_sozleri for word in words) and "as" not in words:
        cevaplar = [
            f"Aleykum salam, {message.author.mention}. Terminala xoş gəldin!",
            f"Salam, {message.author.mention}. Bağlantı quruldu."
        ]
        try:
            await message.channel.send(random.choice(cevaplar))
        except:
            pass

    # 2. Reklam və Link Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club|com/invite)|t\.me|instagram\.com|youtube\.com|steamcommunity\.com/gift|nitro|free-nitro|discord-gifts\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            duration = timedelta(hours=1)
            await message.author.timeout(duration, reason="Zərərli link və ya reklam paylaşımı")
            warn = await message.channel.send(f"🚨 **{message.author.mention}**, reklam/link paylaşdığın üçün 1 saatlıq təcrid edildin!")
            await asyncio.sleep(5)
            await warn.delete()
            return
        except:
            pass

    # 3. @everyone / @here Bloku
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ **{message.author.mention}**, kütləvi etiket qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 4. Spam / Flood Qoruması
    author_id = message.author.id
    current_time = time.time()

    if author_id not in spam_tracker:
        spam_tracker[author_id] = []

    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 4]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) > 4:
        spam_tracker[author_id].clear()
        try:
            await message.delete()
            duration = timedelta(minutes=10)
            await message.author.timeout(duration, reason="Həddindən artıq spam hücumu")
            await message.channel.send(f"🔒 **{message.author.mention}** intensiv spam etdiyi üçün 10 dəqiqəlik mute edildi.")
        except:
            pass
        return

    await bot.process_commands(message)

# ==========================================
# GİZLİ MASTER PANEL (YALNIZ SƏNİN ÜÇÜN: r?bot)
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız botun sahibi işlədə bilər!")
        return

    embed = discord.Embed(
        title="⚡ YENİLMEZ OS // MASTER PANEL",
        description="Sənin üçün xüsusi aktiv olan idarəetmə mərkəzi:",
        color=0x050505
    )
    embed.add_field(
        name="🏴‍☠️ Kiber Simulyasiya və Oyunlar",
        value="• r?hack - Hədəf sistemə sızma\n• r?cuzdan - Balansı yoxlamaq\n• r?yazitura - Sikkə oyunu\n• r?slot - Slot maşını\n• r?rusruleti - Rus ruleti", 
        inline=False
    )
    embed.add_field(
        name="⚔️ Moderasiya və Mühafizə",
        value="• r?sil - Mesajları təmizlə\n• r?ban - İstifadəçini ban et\n• r?at - Serverdən qov\n• r?mute - Təcrid etmək\n• r?lock / r?unlock - Kanalı kilidlə/aç\n• r?nuke - Kanalı sıfırla", 
        inline=False
    )
    embed.add_field(
        name="🎧 Səs və Digər Alətlər",
        value="• r?qosul / r?ayril - Səs kanalları\n• r?afk - AFK rejimi\n• r?avatar - Profil şəkli\n• r?profil - İstifadəçi məlumatı\n• r?server - Server bilgisi\n• r?ping - Gecikmə ölçmə", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS v24.0 • Owner Only")
    await ctx.send(embed=embed)

# Ümumi Hamı üçün Yardım Əmri
@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="🛡️ YENİLMEZ OS // KİBER MƏRKƏZ",
        description="Serverin təhlükəsizliyini qoruyan və əyləncə təqdim edən sistem.",
        color=0x111111
    )
    embed.add_field(name="Əmrlər Siyahısı", value="r?hack, r?cuzdan, r?yazitura, r?slot, r?rusruleti, r?qosul, r?ayril, r?afk, r?avatar, r?profil, r?server, r?ping", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"⚡ Gecikmə müddəti: {latency}ms")

# ==========================================
# MODERASİYA ƏMRLƏRİ
# ==========================================
@bot.command(name="sil")
async def sil(ctx, amount: int = 10):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    if amount > 100: amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ {amount} ədəd mesaj təmizləndi.")
    await msg.delete(delay=3)

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** ban edildi. Səbəb: {reason}")

@bot.command(name="at")
async def at(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.mention}** qovuldu (Kick).")

@bot.command(name="mute")
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Səbəb yoxdur"):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"🔇 **{member.mention}** {minutes} dəqiqəlik təcrid edildi.")

@bot.command(name="lock")
async def lock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal kilidləndi.")

@bot.command(name="unlock")
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanalın kilidi açıldı.")

@bot.command(name="nuke")
async def nuke(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    position = ctx.channel.position
    new_channel = await ctx.channel.clone(reason="Kanal nuke edildi")
    await ctx.channel.delete()
    await new_channel.edit(position=position)
    await new_channel.send("💥 Kanal sıfırlandı və təmizdən quruldu!")

# ==========================================
# OYUN VƏ HACK SİMULYASİYA ƏMRLƏRİ
# ==========================================
@bot.command(name="hack")
async def hack(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("❌ Hədəf qeyd etməlisən: r?hack @istifadəçi")
        return
    if member.id == ctx.author.id:
        await ctx.send("❌ Özünü hackləyə bilməzsən!")
        return

    asamalar = [
        f"💻 {member.name} sisteminə sızılır...",
        f"🔓 Firewall mühafizəsi aşılır...",
        f"📂 Verilənlər ələ keçirilir...",
        f"✅ Əməliyyat uğurla başa çatdı!"
    ]
    
    msg = await ctx.send(asamalar[0])
    await asyncio.sleep(1.5)
    for i in range(1, len(asamalar)):
        await msg.edit(content=asamalar[i])
        await asyncio.sleep(1.5)
    
    para = random.randint(200, 600)
    if ctx.author.id not in user_wallet:
        user_wallet[ctx.author.id] = 100
    user_wallet[ctx.author.id] += para

    embed = discord.Embed(title="🏴‍☠️ HACK REPORT", description=f"**{ctx.author.mention}**, {member.name} hədəfini hacklədin və {para} YNC oğurladın!", color=0x050505)
    await ctx.send(embed=embed)

@bot.command(name="cuzdan")
async def cuzdan(ctx):
    uid = ctx.author.id
    balans = user_wallet.get(uid, 100)
    embed = discord.Embed(title="🪙 Kiber Cüzdan", description=f"**{ctx.author.mention}**, balansın: **{balans} YNC**", color=0xffd700)
    await ctx.send(embed=embed)

@bot.command(name="yazitura")
async def yazitura(ctx, secim: str = None):
    if not secim or secim.lower() not in ["yazı", "tura", "yazi"]:
        await ctx.send("❌ Doğru istifadə: r?yazitura yazı və ya r?yazitura tura")
        return
    neticə = random.choice(["yazı", "tura"])
    secim = "yazı" if secim.lower() == "yazi" else secim.lower()
    
    if secim == neticə:
        await ctx.send(f"🪙 Sikkə: **{neticə.capitalize()}**! Qazandın! 🎉")
    else:
        await ctx.send(f"🪙 Sikkə: **{neticə.capitalize()}**! Uduzdun! 💀")

@bot.command(name="slot")
async def slot(ctx):
    sembollər = ["🍒", "🍋", "🍊", "🔔", "⭐", "💎"]
    s1, s2, s3 = random.choice(sembollər), random.choice(sembollər), random.choice(sembollər)
    slot_mesaj = f"🎰 | {s1} | {s2} | {s3} |"
    
    if s1 == s2 and s2 == s3:
        await ctx.send(f"{slot_mesaj}\n🎉 Jackpot! Böyük mükafat sənin!")
    elif s1 == s2 or s2 == s3 or s1 == s3:
        await ctx.send(f"{slot_mesaj}\n✨ İkisi eyni çıxdı, qazandın!")
    else:
        await ctx.send(f"{slot_mesaj}\n💀 Uduzdun, bəxtini yenidən sına.")

@bot.command(name="rusruleti")
async def rusruleti(ctx):
    risk = random.choice([True, False, False, False])
    if risk:
        await ctx.send(f"💥 **{ctx.author.mention}**, patron partladı! Uduzdun.")
    else:
        await ctx.send(f"✨ **{ctx.author.mention}**, klik! Boş çıxdı, sağ qaldın.")

# ==========================================
# SƏS VƏ DİGƏR ALƏTLƏR
# ==========================================
@bot.command(name="qosul")
async def qosul(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ Əvvəlcə səs kanalında olmalısan!")
        return
    channel = ctx.author.voice.channel
    try:
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"🔊 Səs kanalına qoşuldum: **{channel.name}**")
    except Exception as e:
        await ctx.send(f"❌ Xəta: {e}")

@bot.command(name="ayril")
async def ayril(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Səs kanalından ayrıldım.")
    else:
        await ctx.send("❌ Bot səs kanalında deyil.")

@bot.command(name="afk")
async def afk(ctx, *, reason="Səbəb yoxdur"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"💤 **{ctx.author.name}**, AFK rejiminə keçdin.")

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0x111111)
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="profil")
async def profil(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 İstifadəçi: {member.name}", color=0x111111)
    embed.add_field(name="ID", value=str(member.id), inline=True)
    embed.add_field(name="Giriş", value=member.joined_at.strftime("%d.%m.%Y"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="server")
async def server(ctx: commands.Context):
    guild = ctx.guild
    if guild is None:
        return
    embed = discord.Embed(title=f"🏰 Server: {guild.name}", color=0x111111)
    embed.add_field(name="Üzv Sayı", value=str(guild.member_count), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

# ==========================================
# TOKEN
# ==========================================
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")

