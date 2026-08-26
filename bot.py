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
    return "Yenilmez OS v31.0 [STRICT OWNER EXCLUSIVE SUITE] - Online"

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
intents.reactions = True

bot = commands.Bot(command_prefix='r?', intents=intents)

spam_tracker = {}
afk_users = {}
user_wallet = {}
whitelist = set()
blacklist = set()

SAHIB_ID = 641014966312501259

@bot.event
async def on_ready():
    print(f'🛡️ [YENİLMEZ OS v31]: Sahibə özəl çekiliş və anket sistemləri aktivdir -> {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="r?yardim | Server Qorunur"))

# ==========================================
# REAKSİYA AYNALAMA SİSTEMİ (REACTION MIRROR)
# ==========================================
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    try:
        await reaction.message.add_reaction(reaction.emoji)
    except:
        pass

# ==========================================
# GÜVƏNLİK VƏ SALAMLAMA SİSTEMİ
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

    content = message.content
    lower_content = content.lower()
    words = lower_content.split()

    # SALAMLAMA SİSTEMİ
    salam_sozleri = ["salam", "sa", "slm", "səlam", "salamun"]
    if any(word in salam_sozleri for word in words) and "as" not in words:
        cevaplar = [
            f"Aleykum salam, {message.author.mention}. Xoş gəldin! 🛡️",
            f"Salam, {message.author.mention}. Bağlantı quruldu, necəsən? 😎",
            f"Aleykum salam, {message.author.mention}! Terminala xoş gəldin."
        ]
        try:
            await message.channel.send(random.choice(cevaplar))
        except:
            pass

    if message.author.guild_permissions.administrator or message.author.id in whitelist:
        await bot.process_commands(message)
        return

    # Link və Reklam Qoruması
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

    # Everyone / Here Bloku
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ **{message.author.mention}**, kütləvi etiket atmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # Spam Flood Qoruması
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
# MASTER İDARƏETMƏ PANELİ (TƏKCƏ SAHİB ÜÇÜN)
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu master paneli yalnız botun sahibi aça bilər!")
        return

    embed = discord.Embed(
        title="🛡️ YENİLMEZ OS // SAHİB MASTER PANEL v31",
        description="Serverin idarəetməsi, təhlükəsizliyi və xüsusi sahib əmrləri:",
        color=0x0b0e14
    )
    
    embed.add_field(
        name="👑 Sahibə Özəl Alətlər (Yalnız Sən Edə Bilərsən)",
        value=(
            "`r?elan [mətn]` — Rəsmi server elanı atır\n"
            "`r?çekiliş / r?cekilis [vaxt] [hədiyyə]` — Məs: `r?çekiliş 1d 5h Nitro`\n"
            "`r?anket / r?sorğu [sual]` — Anket açır"
        ),
        inline=False
    )

    embed.add_field(
        name="🛡️ Moderasiya & Təhlükəsizlik",
        value=(
            "`r?sil [say]` — Mesajları təmizləyir\n"
            "`r?ban` / `r?kick` / `r?mute` — Cəza əmrləri\n"
            "`r?lock` / `r?unlock` / `r?nuke` — Kanal idarəsi"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔒 Whitelist & Blacklist",
        value="`r?white add/remove` — Toxunulmazlıq\n`r?black add/remove` — Qara siyahı",
        inline=False
    )
    
    embed.add_field(
        name="🏰 Server və Əyləncə",
        value="`r?server`, `r?profil`, `r?avatar`, `r?ping`, `r?cuzdan`, `r?rusruleti`, `r?afk`",
        inline=False
    )
    
    embed.set_footer(text="Yenilmez OS v31.0 • Strict Owner Exclusive Suite")
    await ctx.send(embed=embed)

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="📖 Yardım — Bütün Komandalar Siyahısı",
        description="Prefiks: `r?`",
        color=0x0b0e14
    )
    embed.add_field(
        name="Komandalar", 
        value="`r?bot`, `r?elan`, `r?çekiliş`, `r?anket`, `r?sil`, `r?ban`, `r?kick`, `r?mute`, `r?lock`, `r?unlock`, `r?nuke`, `r?white`, `r?black`, `r?server`, `r?profil`, `r?avatar`, `r?ping`, `r?cuzdan`, `r?rusruleti`, `r?qosul`, `r?ayril`, `r?afk`", 
        inline=False
    )
    await ctx.send(embed=embed)

# ==========================================
# SAHİBƏ ÖZƏL: ELAN, ÇEKİLİŞ VƏ ANKET SİSTEMLƏRİ
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, text):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız botun sahibi istifadə edə bilər!")
        return
    try: await ctx.message.delete()
    except: pass

    embed = discord.Embed(title="📢 SERVERİN RƏSMİ ELANI", description=text, color=0xff4500)
    embed.set_footer(text=f"Elan edən: {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="çekiliş", aliases=["cekilis"])
async def cekilis(ctx, time_str: str, *, prize):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Çekilişi yalnız botun sahibi başlada bilər!")
        return

    seconds = 0
    match_d = re.search(r'(\d+)d', time_str)
    match_h = re.search(r'(\d+)h', time_str)
    match_m = re.search(r'(\d+)m', time_str)
    match_s = re.search(r'(\d+)s', time_str)

    if match_d: seconds += int(match_d.group(1)) * 86400
    if match_h: seconds += int(match_h.group(1)) * 3600
    if match_m: seconds += int(match_m.group(1)) * 60
    if match_s: seconds += int(match_s.group(1))

    if seconds == 0:
        try:
            seconds = int(time_str)
        except:
            await ctx.send("❌ Xəta! Vaxtı düzgün qeyd et. Məsələn: `r?çekiliş 1d 5h 30m Nitro` və ya `r?çekiliş 60 Nitro`")
            return

    embed = discord.Embed(title="🎉 ÇEKİLİŞ BAŞLADI! 🎉", description=f"Hədiyyə: **{prize}**\nQatılmaq üçün 🎁 emojisinə toxun!", color=0xffd700)
    embed.set_footer(text=f"Müddət: {time_str}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎁")
    
    await asyncio.sleep(seconds)

    new_msg = await ctx.channel.fetch_message(msg.id)
    reaction = discord.utils.get(new_msg.reactions, emoji="🎁")
    users = [user async for user in reaction.users() if not user.bot]

    if users:
        winner = random.choice(users)
        await ctx.send(f"🏆 Təbriklər {winner.mention}! Çekilişi qazandın: **{prize}** 🎉")
    else:
        await ctx.send("😢 Heç kim qatılmadı.")

@bot.command(name="anket", aliases=["sorğu"])
async def anket(ctx, *, question):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Anketləri yalnız botun sahibi aça bilər!")
        return
    try: await ctx.message.delete()
    except: pass
    
    embed = discord.Embed(title="📊 SERVER ANKETİ", description=question, color=0x00ffff)
    embed.set_footer(text=f"Sorğunu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

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
async def ban(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.ban_members: return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** ban edildi.")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.kick_members: return
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.mention}** qovuldu.")

@bot.command(name="mute")
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.moderate_members: return
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"🔇 **{member.mention}** {minutes} dəqiqə susduruldu.")

@bot.command(name="lock")
async def lock(ctx):
    if not ctx.author.guild_permissions.manage_channels: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal kilidləndi.")

@bot.command(name="unlock")
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanalın kilidi açıldı.")

@bot.command(name="nuke")
async def nuke(ctx):
    if not ctx.author.guild_permissions.manage_channels: return
    pos = ctx.channel.position
    new_ch = await ctx.channel.clone(reason="Nuke")
    await ctx.channel.delete()
    await new_ch.edit(position=pos)
    await new_ch.send("💥 Kanal yeniləndi!")

# ==========================================
# GÜVƏNLİK İDARƏSİ
# ==========================================
@bot.group(name="white", invoke_without_command=True)
async def white(ctx): pass

@white.command(name="add")
async def white_add(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator: return
    whitelist.add(member.id)
    await ctx.send(f"🛡️ **{member.name}** whitelist-ə əlavə edildi.")

@white.command(name="remove")
async def white_remove(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator: return
    whitelist.discard(member.id)
    await ctx.send(f"⚠️ **{member.name}** whitelist-dən çıxarıldı.")

@bot.group(name="black", invoke_without_command=True)
async def black(ctx): pass

@black.command(name="add")
async def black_add(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator: return
    blacklist.add(member.id)
    try: await member.ban(reason="Blacklist")
    except: pass
    await ctx.send(f"⛔ **{member.name}** qara siyahıya salındı.")

@black.command(name="remove")
async def black_remove(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator: return
    blacklist.discard(member.id)
    await ctx.send(f"✅ **{member.name}** qara siyahıdan silindi.")

# ==========================================
# SERVER MƏLUMAT & ƏYLƏNCƏ
# ==========================================
@bot.command(name="server")
async def server(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 {guild.name}", color=0x0b0e14)
    embed.add_field(name="👑 Sahib", value=f"{guild.owner.mention if guild.owner else 'Naməlum'}", inline=True)
    embed.add_field(name="👥 Üzv", value=str(guild.member_count), inline=True)
    embed.add_field(name="📅 Yaradılış", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="profil")
async def profil(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 {member.name}", color=0x0b0e14)
    embed.add_field(name="ID", value=str(member.id), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0x0b0e14)
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send(f"⚡ Gecikmə: {round(bot.latency * 1000)}ms")

@bot.command(name="cuzdan")
async def cuzdan(ctx):
    balans = user_wallet.get(ctx.author.id, 500)
    await ctx.send(embed=discord.Embed(title="🪙 Kiber Cüzdan", description=f"Balansın: **{balans} YNC**", color=0xffd700))

@bot.command(name="rusruleti")
async def rusruleti(ctx):
    if random.choice([True, False, False, False, False]):
        await ctx.send(f"💥 **{ctx.author.mention}**, patron partladı! 💀")
    else:
        await ctx.send(f"✨ **{ctx.author.mention}**, klik... Sağ qaldın! 😎")

@bot.command(name="qosul")
async def qosul(ctx):
    if ctx.author.voice:
        ch = ctx.author.voice.channel
        if ctx.voice_client: await ctx.voice_client.move_to(ch)
        else: await ch.connect()
        await ctx.send(f"🔊 Qoşuldum: **{ch.name}**")
    else: await ctx.send("❌ Səs kanalında deyiləm!")

@bot.command(name="ayril")
async def ayril(ctx, *, args=None):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Ayrıldım.")
    else: await ctx.send("❌ Səs kanalında deyiləm.")

@bot.command(name="afk")
async def afk(ctx, *, reason="Səbəb yoxdur"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"💤 **{ctx.author.name}**, AFK-san. Səbəb: {reason}")

# ==========================================
# TOKEN
# ==========================================
token = os.environ.get("DISCORD_TOKEN")
if token: bot.run(token)
else: print("XƏTA: DISCORD_TOKEN tapılmadı!")
    
