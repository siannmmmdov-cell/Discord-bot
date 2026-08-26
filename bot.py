import subprocess
import sys

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
    return "Yenilmez OS v26.0 [MAXIMUM SERVER PROTECTION & INFO SUITE] - Online"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_server).start()

# ==========================================
# BOT KONQİQURASİYASI VƏ INTENTS
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
whitelist = set()
blacklist = set()

SAHIB_ID = 641014966312501259

@bot.event
async def on_ready():
    print(f'🛡️ [YENİLMEZ OS v26]: Bütün sistemlər və qoruma modulları aktivdir -> {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="r?yardim | Server Qorunur"))

# ==========================================
# ULTRA GÜVƏNLİK VƏ MÜDAFİƏ SİSTEMİ
# ==========================================
@bot.event
async def on_member_join(member):
    if member.id in blacklist:
        try:
            await member.ban(reason="Blacklist üzvü avtomatik qovuldu.")
            return
        except:
            pass
            
    if member.bot:
        if member.id != bot.user.id and member.id not in whitelist:
            try:
                await member.ban(reason="Anti-Nuke: İcazəsiz kənar bot girişi əngəlləndi.")
            except:
                pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id in blacklist:
        try:
            await message.delete()
            return
        except:
            pass

    # AFK Sistem yoxlaması
    if message.author.id in afk_users:
        del afk_users[message.author.id]
        try:
            await message.channel.send(f"⚠️ Qayıtdın, {message.author.mention}. AFK rejimi ləğv edildi.", delete_after=4)
        except:
            pass

    for mention in message.mentions:
        if mention.id in afk_users:
            reason = afk_users[mention.id]
            try:
                await message.channel.send(f"💤 **{mention.name}** hazırda AFK-dır. Səbəb: {reason}")
            except:
                pass

    if message.author.guild_permissions.administrator or message.author.id in whitelist:
        await bot.process_commands(message)
        return

    content = message.content

    # 1. Link və Reklam Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club|com/invite)|t\.me|instagram\.com|youtube\.com|steamcommunity\.com/gift|nitro|free-nitro|discord-gifts\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            await message.author.timeout(timedelta(hours=3), reason="Reklam / Zərərli link paylaşımı")
            warn = await message.channel.send(f"🚨 **{message.author.mention}**, reklam tipli linklər sərt şəkildə qadağandır! 3 saatlıq təcrid edildin.")
            await asyncio.sleep(5)
            await warn.delete()
            return
        except:
            pass

    # 2. Everyone / Here Bloku
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ **{message.author.mention}**, kütləvi etiket atmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. Spam Flood Qoruması
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
            await message.author.timeout(timedelta(minutes=20), reason="İntensiv spam hücumu")
            await message.channel.send(f"🔒 **{message.author.mention}** sürətli mesaj spamına görə 20 dəqiqəlik mute edildi.")
        except:
            pass
        return

    await bot.process_commands(message)

# ==========================================
# MASTER İDARƏETMƏ PANELİ (r?bot) - FULL VERSİYA
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bu paneli yalnız səlahiyyətlilər aça bilər!")
        return

    embed = discord.Embed(
        title="🛡️ YENİLMEZ OS // ULTIMATE MASTER PANEL v26",
        description="Serverin idarəetməsi, təhlükəsizliyi və bütün alətlər mərkəzi:",
        color=0x0b0e14
    )
    
    embed.add_field(
        name="🛡️ Moderasiya & Təhlükəsizlik",
        value=(
            "`r?sil [say]` — İstənilən sayda mesaj silir\n"
            "`r?ban @user [səbəb]` — İstifadəçini serverdən banlayır\n"
            "`r?kick @user [səbəb]` — İstifadəçini qovur\n"
            "`r?mute @user [dəqiqə]` — Timeout (susdurma) atır\n"
            "`r?lock` / `r?unlock` — Kanalı yazışmaya bağlayır/açır\n"
            "`r?nuke` — Kanalı tamamilə sıfırlayıb yeniləyir"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔒 Whitelist & Blacklist Sistemi",
        value=(
            "`r?white add / remove @user` — Xüsusi toxunulmazlıq verir\n"
            "`r?black add / remove @user` — Qara siyahıya atıb banlayır"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🏰 Server və Məlumat Komandaları",
        value=(
            "`r?server` — Server haqqında ümumi məlumatlar\n"
            "`r?profil [@user]` — İstifadəçi profil məlumatı\n"
            "`r?avatar [@user]` — Profil şəklini böyük göstərir\n"
            "`r?ping` — Botun gecikmə sürətini ölçür"
        ),
        inline=False
    )

    embed.add_field(
        name="⚡ Əyləncə & Alətlər",
        value=(
            "`r?cuzdan` — Şəxsi kiber balansını yoxlayır\n"
            "`r?rusruleti` — Riskli rus ruleti oyunu\n"
            "`r?qosul` / `r?ayril` — Səs kanalı idarəsi\n"
            "`r?afk [səbəb]` — AFK rejiminə keçid"
        ),
        inline=False
    )
    
    embed.set_footer(text="Yenilmez OS v26.0 • Complete Server Suite & Security")
    await ctx.send(embed=embed)

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="📖 Yardım — Bütün Komandalar Siyahısı",
        description="Prefiks: `r?`\nServerin bütün funksiyaları aşağıdakılardır:",
        color=0x0b0e14
    )
    embed.add_field(
        name="Komandalar", 
        value="`r?bot`, `r?sil`, `r?ban`, `r?kick`, `r?mute`, `r?lock`, `r?unlock`, `r?nuke`, `r?white`, `r?black`, `r?server`, `r?profil`, `r?avatar`, `r?ping`, `r?cuzdan`, `r?rusruleti`, `r?qosul`, `r?ayril`, `r?afk`", 
        inline=False
    )
    await ctx.send(embed=embed)

# ==========================================
# MODERASİYA ƏMRLƏRİ
# ==========================================
@bot.command(name="sil")
async def sil(ctx, amount: int = 10):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ Mesaj idarəetmə səlahiyyətin yoxdur.")
        return
    if amount > 100: amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ {amount} ədəd mesaj təmizləndi.")
    await msg.delete(delay=3)

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ Ban səlahiyyətin yoxdur.")
        return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** ban edildi. Səbəb: {reason}")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ Kick səlahiyyətin yoxdur.")
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.mention}** serverdən qovuldu.")

@bot.command(name="mute")
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ Timeout səlahiyyətin yoxdur.")
        return
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"🔇 **{member.mention}** {minutes} dəqiqə müddətinə susduruldu.")

@bot.command(name="lock")
async def lock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal yazışmaya bağlandı.")

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
    pos = ctx.channel.position
    new_ch = await ctx.channel.clone(reason="Nuke əmri icra edildi")
    await ctx.channel.delete()
    await new_ch.edit(position=pos)
    await new_ch.send("💥 Kanal sıfırlandı və yenidən quruldu!")

# ==========================================
# GÜVƏNLİK İDARƏSİ (Whitelist / Blacklist)
# ==========================================
@bot.group(name="white", invoke_without_command=True)
async def white(ctx):
    await ctx.send("❌ Doğru istifadə: `r?white add @user` və ya `r?white remove @user`")

@white.command(name="add")
async def white_add(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    whitelist.add(member.id)
    await ctx.send(f"🛡️ **{member.name}** toxunulmaz (whitelist) siyahısına əlavə edildi.")

@white.command(name="remove")
async def white_remove(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    whitelist.discard(member.id)
    await ctx.send(f"⚠️ **{member.name}** toxunulmaz siyahısından çıxarıldı.")

@bot.group(name="black", invoke_without_command=True)
async def black(ctx):
    await ctx.send("❌ Doğru istifadə: `r?black add @user` və ya `r?black remove @user`")

@black.command(name="add")
async def black_add(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    blacklist.add(member.id)
    try:
        await member.ban(reason="Qara siyahıya salındı.")
    except:
        pass
    await ctx.send(f"⛔ **{member.name}** qara siyahıya salındı və ban edildi.")

@black.command(name="remove")
async def black_remove(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    blacklist.discard(member.id)
    await ctx.send(f"✅ **{member.name}** qara siyahıdan silindi.")

# ==========================================
# SERVER VƏ İSTİFADƏÇİ MƏLUMAT ƏMRLƏRİ
# ==========================================
@bot.command(name="server")
async def server(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 Server Məlumatı: {guild.name}", color=0x0b0e14)
    embed.add_field(name="👑 Sahib", value=f"{guild.owner.mention if guild.owner else 'Naməlum'}", inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=str(guild.member_count), inline=True)
    embed.add_field(name="📅 Yaradılma Tarixi", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="💬 Kanal Sayı", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="🛡️ Rol Sayı", value=str(len(guild.roles)), inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="profil")
async def profil(ctx, member: discord.Member = None):
    member = member or ctx.author
    roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
    roles_str = ", ".join(roles) if roles else "Rol yoxdur"
    
    embed = discord.Embed(title=f"👤 İstifadəçi: {member.name}", color=0x0b0e14)
    embed.add_field(name="ID", value=str(member.id), inline=True)
    embed.add_field(name="Serverə Qoşulma", value=member.joined_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="Rollər", value=roles_str, inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0x0b0e14)
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"⚡ Botun gecikmə sürəti: {lat}ms")

# ==========================================
# ƏYLƏNCƏ VƏ ALƏTLƏR
# ==========================================
@bot.command(name="cuzdan")
async def cuzdan(ctx):
    uid = ctx.author.id
    balans = user_wallet.get(uid, 500)
    embed = discord.Embed(title="🪙 Kiber Cüzdan", description=f"**{ctx.author.mention}**, balansın: **{balans} YNC**", color=0xffd700)
    await ctx.send(embed=embed)

@bot.command(name="rusruleti")
async def rusruleti(ctx):
    risk = random.choice([True, False, False, False, False])
    if risk:
        await ctx.send(f"💥 **{ctx.author.mention}**, patron partladı! 💀 Uduzdun.")
    else:
        await ctx.send(f"✨ **{ctx.author.mention}**, klik... Boş çıxdı, sağ qaldın! 😎")

@bot.command(name="qosul")
async def qosul(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ Əvvəlcə səs kanalına qoşulmalısan!")
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
async def afk(ctx, *, reason="Səbəb qeyd edilməyib"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"💤 **{ctx.author.name}**, AFK rejiminə keçdin. Səbəb: {reason}")

# ==========================================
# TOKEN
# ==========================================
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
        
