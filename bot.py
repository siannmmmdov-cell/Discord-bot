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
    return "Yenilmez OS v25.0 [ULTRA SECURITY & DEFENSE] - Online"

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
    print(f'🛡️ [YENİLMEZ OS v25]: Təhlükəsizlik divarları aktivdir -> {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="r?bot | Server Qorunur"))

# ==========================================
# ULTRA GÜVƏNLİK VƏ QORUMA SİSTEMİ
# ==========================================
@bot.event
async def on_member_join(member):
    if member.id in blacklist:
        try:
            await member.ban(reason="Blacklist sistemində olduğu üçün avtomatik qovuldu.")
            return
        except:
            pass
            
    if member.bot:
        if member.id != bot.user.id and member.id not in whitelist:
            try:
                await member.ban(reason="Təhlükəsizlik: İcazəsiz kənar bot inyeksiya cəhdi (Anti-Nuke).")
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

    # AFK Sistem
    if message.author.id in afk_users:
        del afk_users[message.author.id]
        try:
            await message.channel.send(f"⚠️ Qayıtdın, {message.author.mention}. AFK rejimi söndürüldü.", delete_after=4)
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

    # 1. Zərərli Link və Reklam Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club|com/invite)|t\.me|instagram\.com|youtube\.com|steamcommunity\.com/gift|nitro|free-nitro|discord-gifts\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            await message.author.timeout(timedelta(hours=2), reason="Zərərli link / Reklam yayımı")
            warn = await message.channel.send(f"🚨 **{message.author.mention}**, reklam tipli linklər qadağandır! 2 saatlıq təcrid edildin.")
            await asyncio.sleep(5)
            await warn.delete()
            return
        except:
            pass

    # 2. @everyone / @here Qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ **{message.author.mention}**, kütləvi etiket (Mass Mention) sərt şəkildə qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. Spam / Flood Mühafizəsi
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
            await message.author.timeout(timedelta(minutes=15), reason="Həddindən artıq sürətli spam hücumu")
            await message.channel.send(f"🔒 **{message.author.mention}** sürətli mesaj spamına görə 15 dəqiqəlik mute edildi.")
        except:
            pass
        return

    await bot.process_commands(message)

# ==========================================
# MASTER İDARƏETMƏ PANELİ (r?bot)
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bu paneli yalnız səlahiyyətlilər aça bilər!")
        return

    embed = discord.Embed(
        title="🛡️ YENİLMEZ OS // MASTER PANEL v25",
        description="Serverin təhlükəsizliyi və idarəetməsi üçün tam mərkəz:",
        color=0x0b0e14
    )
    
    embed.add_field(
        name="🛡️ Moderasiya & Mühafizə",
        value="`r?sil [say]` — Mesajları təmizləyir\n`r?ban @user [səbəb]` — İstifadəçini banlayır\n`r?kick @user [səbəb]` — Serverdən qovur\n`r?mute @user [dəqiqə]` — Timeout (m艇) atır\n`r?lock` / `r?unlock` — Kanalı kilidləyir/açır\n`r?nuke` — Kanalı tamamilə yeniləyir",
        inline=False
    )
    
    embed.add_field(
        name="🔒 Whitelist & Blacklist (Güvənlik)",
        value="`r?white add / remove @user` — Toxunulmaz edir\n`r?black add / remove @user` — Qara siyahıya atır",
        inline=False
    )
    
    embed.add_field(
        name="⚡ Əyləncə & Alətlər",
        value="`r?cuzdan` — Balansını yoxlayırsan\n`r?rusruleti` — Riskli rus ruleti oyunu\n`r?qosul` / `r?ayril` — Səs kanalı idarəsi\n`r?avatar` / `r?profil` — Məlumatlar",
        inline=False
    )
    
    embed.set_footer(text="Yenilmez OS v25.0 • Ultimate Security System")
    await ctx.send(embed=embed)

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="📖 Yardım — Bütün Komandalar",
        description="Prefiks: `r?`",
        color=0x0b0e14
    )
    embed.add_field(name="Əmrlər", value="`r?bot`, `r?sil`, `r?ban`, `r?kick`, `r?mute`, `r?lock`, `r?unlock`, `r?nuke`, `r?cuzdan`, `r?rusruleti`, `r?qosul`, `r?ayril`, `r?avatar`, `r?ping`", inline=False)
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
    await ctx.send(f"🔨 **{member.mention}** serverdən ban edildi. Səbəb: {reason}")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ Kick səlahiyyətin yoxdur.")
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.mention}** serverdən qovuldu. Səbəb: {reason}")

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
        await ctx.send("❌ Kanal idarəetmə səlahiyyətin yoxdur.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Kanal idarəetmə səlahiyyətin yoxdur.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanalın kilidi açıldı.")

@bot.command(name="nuke")
async def nuke(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Kanal idarəetmə səlahiyyətin yoxdur.")
        return
    pos = ctx.channel.position
    new_ch = await ctx.channel.clone(reason="Nuke əmri icra edildi")
    await ctx.channel.delete()
    await new_ch.edit(position=pos)
    await new_ch.send("💥 Kanal uğurla təmizləndi və sıfırdan quruldu!")

# ==========================================
# GÜVƏNLİK SİSTEMİ İDARƏSİ (Whitelist / Blacklist)
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
        await member.ban(reason="Qara siyahıya (Blacklist) salındı.")
    except:
        pass
    await ctx.send(f"⛔ **{member.name}** qara siyahıya salındı və serverdən uzaqlaşdırıldı.")

@black.command(name="remove")
async def black_remove(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    blacklist.discard(member.id)
    await ctx.send(f"✅ **{member.name}** qara siyahıdan silindi.")

# ==========================================
# AURA QATAN 2 ƏSAS OYUN
# ==========================================
@bot.command(name="cuzdan")
async def cuzdan(ctx):
    uid = ctx.author.id
    balans = user_wallet.get(uid, 500)
    embed = discord.Embed(title="🪙 Kiber Cüzdan", description=f"**{ctx.author.mention}**, hesabındakı balans: **{balans} YNC**", color=0xffd700)
    await ctx.send(embed=embed)

@bot.command(name="rusruleti")
async def rusruleti(ctx):
    risk = random.choice([True, False, False, False, False])
    if risk:
        await ctx.send(f"💥 **{ctx.author.mention}**, patron partladı! 💀 Uduzdun.")
    else:
        await ctx.send(f"✨ **{ctx.author.mention}**, klik... Boş çıxdı, sağ qaldın! 😎")

# ==========================================
# SƏS VƏ DİGƏR ALƏTLƏR
# ==========================================
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
        await ctx.send("❌ Bot heç bir səs kanalında deyil.")

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0x0b0e14)
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="profil")
async def profil(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 İstifadəçi Profili: {member.name}", color=0x0b0e14)
    embed.add_field(name="ID", value=str(member.id), inline=True)
    embed.add_field(name="Serverə Giriş", value=member.joined_at.strftime("%d.%m.%Y"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"⚡ Botun gecikmə sürəti: {lat}ms")

# ==========================================
# TOKEN
# ==========================================
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
    
