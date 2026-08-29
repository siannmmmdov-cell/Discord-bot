import discord
from discord.ext import commands
import time
from datetime import timedelta
import random
import asyncio
import os
from flask import Flask
from threading import Thread

# --- FLASK SERVER (RENDER ÜÇÜN) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- BOT SAZLANMALARI ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.presences = True

bot = commands.Bot(command_prefix="r?", intents=intents)

SAHIB_ID = 641014966312501259
start_time = time.time()
spam_kontrol = {}

@bot.event
async def on_ready():
    print(f"BOT AKTİVDİR: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Master Panel"))

@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.guild.ban(member, reason="İnsiz bot girişi!")
        except:
            pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    if message.author.id != SAHIB_ID and message.reference is None and "salam" in content_lower:
        try:
            await message.channel.send(f"Aleykum salam, {message.author.mention}! Xoş gəldiniz! 👑")
        except:
            pass

    if message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    if "discord.gg/" in content_lower or "discord.com/invite/" in content_lower:
        try:
            await message.delete()
            await message.author.timeout(timedelta(minutes=10), reason="Dəvət linki!")
        except:
            pass
        return

    author_id = message.author.id
    simdi = time.time()

    if author_id not in spam_kontrol:
        spam_kontrol[author_id] = []

    spam_kontrol[author_id] = [t for t in spam_kontrol[author_id] if simdi - t < 4]
    spam_kontrol[author_id].append(simdi)

    if len(spam_kontrol[author_id]) >= 5:
        try:
            await message.channel.purge(limit=6, check=lambda m: m.author.id == author_id)
            await message.author.timeout(timedelta(minutes=5), reason="Spam")
        except:
            pass
        return

    await bot.process_commands(message)

# --- AVTOMATİK REAKSİYA SİSTEMİ (SƏN EMOJİ BASANDA) ---
UYGUN_EMOJI_GRUPLARI = {
    "👍": ["✅", "🔥", "💯", "🎯"],
    "❤️": ["💖", "😍", "✨", "💞"],
    "🔥": ["⚡", "🚀", "💥", "👑"],
    "⭐": ["🌟", "💫", "💎", "✨"],
    "😂": ["💀", "🤣", "😹", "🔥"],
    "🎉": ["🎊", "🥳", "🏆", "🌟"]
}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id != SAHIB_ID or payload.guild_id is None:
        return

    channel = bot.get_channel(payload.channel_id)
    if not channel:
        return
    try:
        message = await channel.fetch_message(payload.message_id)
    except:
        return

    emoji_str = str(payload.emoji)
    secilenler = UYGUN_EMOJI_GRUPLARI.get(emoji_str, ["🔥", "⚡", "⭐", "🎯"])
    
    for exsar in random.sample(secilenler, min(2, len(secilenler))):
        try:
            await message.add_reaction(exsar)
        except:
            pass

# --- MASTER PANEL ---
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        return

    embed = discord.Embed(
        title="👑 MASTER PANEL v1500",
        description="Bütün əmrlər siyahısı:",
        color=0x050505
    )
    embed.add_field(
        name="👑 Sahib Əmrləri",
        value="`r?elan`, `r?anket`, `r?cekilis`, `r?botkurulum`, `r?servertemizle`, `r?duyuru`, `r?bakim`",
        inline=False
    )
    embed.add_field(
        name="📋 Məlumat",
        value="`r?server`, `r?userinfo`, `r?botinfo`, `r?ping`, `r?online`, `r?kanalbilgi`, `r?rolbilgi`, `r?boosters`, `r?hava`, `r?hesabla`",
        inline=False
    )
    embed.add_field(
        name="🛡️ Moderasiya (Silmək və s.)",
        value="`r?sil`, `r?silkanal`, `r?mute`, `r?unmute`, `r?ban`, `r?unban`, `r?kick`, `r?lock`, `r?unlock`, `r?slowmode`, `r?sesmute`, `r?sesunmute`",
        inline=False
    )
    embed.add_field(
        name="⚙️ Rol & Üzv",
        value="`r?rolver`, `r?rolsil`, `r?nick`, `r?avatar`, `r?yetkililer`, `r?seskontrol`, `r?kanalac`",
        inline=False
    )
    embed.add_field(
        name="🎮 Oyunlar & Əyləncə",
        value="`r?duel`, `r?coinflip`, `r?slot`, `r?hacker`, `r?zar`, `r?magic8ball`, `r?sevgili`, `r?ascii`",
        inline=False
    )
    await ctx.send(embed=embed)

# --- SAHİB ƏMRLƏRİ ---
@bot.command(name="elan")
async def elan(ctx, *, text: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 ELAN", description=text, color=0x050505)
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("✅")

@bot.command(name="anket")
async def anket(ctx, *, sual: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 ANKET", description=sual, color=0x050505)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, vaxt_str: str, *, hediyye: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    saniye = 60
    if vaxt_str.endswith("m"): saniye = int(vaxt_str[:-1]) * 60
    elif vaxt_str.endswith("h"): saniye = int(vaxt_str[:-1]) * 3600
    embed = discord.Embed(title="🎉 ÇƏKİLİŞ", description=f"Hədiyyə: **{hediyye}**\nQatılmaq üçün 🎉 bas!")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(saniye)
    try:
        msg = await ctx.channel.fetch_message(msg.id)
        users = [u async for u in msg.reactions[0].users() if not u.bot]
        if users:
            await ctx.send(f"🏆 Qalib: {random.choice(users).mention}! Hədiyyə: **{hediyye}** 🎉")
        else:
            await ctx.send("❌ Qatılan olmadı.")
    except:
        pass

@bot.command(name="botkurulum")
async def botkurulum(ctx):
    if ctx.author.id == SAHIB_ID: await ctx.send("🛡️ Qoruma aktivdir!")

@bot.command(name="servertemizle")
async def servertemizle(ctx):
    if ctx.author.id == SAHIB_ID: await ctx.send("🧹 Server təmizləndi.")

@bot.command(name="duyuru")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id == SAHIB_ID:
        await ctx.message.delete()
        await ctx.send(f"📢 **Bildiriş:** {metin}")

@bot.command(name="bakim")
async def bakim(ctx):
    if ctx.author.id == SAHIB_ID: await ctx.send("🛠️ Bot baxımdadır.")

# --- MƏLUMAT ƏMRLƏRİ ---
@bot.command(name="server")
async def server_info(ctx):
    await ctx.send(f"🛡️ **{ctx.guild.name}** | Üzv: `{ctx.guild.member_count}`")

@bot.command(name="online")
async def online_stats(ctx):
    c = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 Aktiv üzv: **{c}**")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Ping: **{round(bot.latency * 1000)}ms**")

@bot.command(name="botinfo")
async def botinfo(ctx):
    await ctx.send(f"⏱️ Uptime: `{str(timedelta(seconds=int(time.time() - start_time)))}`")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"👤 **{m.name}** | ID: `{m.id}`")

@bot.command(name="kanalbilgi")
async def kanalbilgi(ctx):
    await ctx.send(f"📁 Kanal: **{ctx.channel.name}**")

@bot.command(name="rolbilgi")
async def rolbilgi(ctx, role: discord.Role):
    await ctx.send(f"🛡️ Rol: **{role.name}** | Üzv: `{len(role.members)}`")

@bot.command(name="boosters")
async def boosters(ctx):
    await ctx.send(f"💎 Boost: **{ctx.guild.premium_subscription_count}**")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Baku"):
    await ctx.send(f"🌤️ `{seher}`: 28°C, Günəşli.")

@bot.command(name="hesabla")
async def hesabla(ctx, *, ifade: str):
    try:
        await ctx.send(f"🧮 Nəticə: `{eval(ifade)}`")
    except:
        await ctx.send("⚠️ Xətali misal!")

# --- MODERASİYA (KANAL SİLMƏ VƏ S.) ---
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, say: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=say)
    await ctx.send(f"🧹 `{len(deleted)}` mesaj silindi.", delete_after=3)

@bot.command(name="silkanal")
@commands.has_permissions(manage_channels=True)
async def silkanal(ctx, kanal: discord.TextChannel = None):
    k = kanal or ctx.channel
    try:
        await k.delete()
    except Exception as e:
        await ctx.send(f"❌ Xəta: {e}")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute_cmd(ctx, member: discord.Member, dakika: int = 5):
    await member.timeout(timedelta(minutes=dakika))
    await ctx.send(f"🔇 {member.mention} `{dakika}` dəqiqə mute olundu.")

@bot.command(name="unmute")
@commands.has_permissions(moderate_members=True)
async def unmute_cmd(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} mutesi açıldı.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} banlandı!")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_cmd(ctx, user_id: int):
    u = await bot.fetch_user(user_id)
    await ctx.guild.unban(u)
    await ctx.send(f"🔓 {u.name} banı açıldı.")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} atıldı!")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal bağlandı.")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı.")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, saniye: int = 0):
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Slowmode: **{saniye}** san.")

@bot.command(name="sesmute")
@commands.has_permissions(mute_members=True)
async def sesmute(ctx, member: discord.Member):
    if member.voice:
        await member.edit(mute=True)
        await ctx.send(f"🔇 {member.mention} susduruldu.")

@bot.command(name="sesunmute")
@commands.has_permissions(mute_members=True)
async def sesunmute(ctx, member: discord.Member):
    if member.voice:
        await member.edit(mute=False)
        await ctx.send(f"🔊 {member.mention} səsi açıldı.")

# --- ROL VƏ ÜZV ---
@bot.command(name="rolver")
@commands.has_permissions(manage_roles=True)
async def rolver(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} rol verildi.")

@bot.command(name="rolsil")
@commands.has_permissions(manage_roles=True)
async def rolsil(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"✅ {member.mention} rol alındı.")

@bot.command(name="nick")
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, yeni_ad: str):
    await member.edit(nick=yeni_ad)
    await ctx.send("📝 Ad dəyişdi.")

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    m = member or ctx.author
    if m.avatar:
        await ctx.send(f"🖼️ {m.avatar.url}")

@bot.command(name="yetkililer")
async def yetkililer(ctx):
    staff = [m.name for m in ctx.guild.members if m.guild_permissions.administrator]
    await ctx.send(f"🛡️ Adminlər: {', '.join(staff[:10])}")

@bot.command(name="seskontrol")
async def seskontrol(ctx):
    if ctx.author.voice:
        await ctx.send(f"🔊 Kanal: **{ctx.author.voice.channel.name}**")

@bot.command(name="kanalac")
@commands.has_permissions(manage_channels=True)
async def kanalac(ctx, *, kanal_adi: str):
    await ctx.guild.create_text_channel(kanal_adi)
    await ctx.send(f"📁 Kanal açıldı: **{kanal_adi}**")

# --- OYUNLAR ---
@bot.command(name="duel")
async def duel(ctx, member: discord.Member = None):
    if member:
        await ctx.send(f"⚔️ Qalib: **{random.choice([ctx.author, member]).name}** 🏆")

@bot.command(name="coinflip")
async def coinflip(ctx, secim: str = "yazı"):
    netice = random.choice(["yazı", "tura"])
    win = "Qazandın! 🎉" if secim.lower() == netice else "Udurdun!"
    await ctx.send(f"🪙 Nəticə: **{netice}**. {win}")

@bot.command(name="slot")
async def slot(ctx):
    s = ["🍎", "🍋", "🍒", "💎", "⭐"]
    r1, r2, r3 = random.choice(s), random.choice(s), random.choice(s)
    res = "🔥 Jackpot!" if r1 == r2 == r3 else "💀 Udurdun!"
    await ctx.send(f"🎰 [ {r1} | {r2} | {r3} ]\n{res}")

@bot.command(name="hacker")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip = f"{random.randint(10,255)}.{random.randint(10,255)}.{random.randint(10,255)}.{random.randint(10,255)}"
    await ctx.send(f"💻 **{target.name}** hackləndi! IP: `{ip}` 🚀")

@bot.command(name="zar")
async def zar(ctx):
    await ctx.send(f"🎲 Zər: **{random.randint(1, 6)}**")

@bot.command(name="magic8ball")
async def magic8ball(ctx, *, sorgu: str):
    ans = ["Bəli, mütləq.", "Xeyr, asla.", "Bəlkə də.", "Dəqiq bilmirəm."]
    await ctx.send(f"🔮 {sorgu}\nCavab: **{random.choice(ans)}**")

@bot.command(name="sevgili")
async def sevgili(ctx, member: discord.Member = None):
    if member:
        await ctx.send(f"💖 Uyğunluq: **%{random.randint(0, 100)}** 💕")

@bot.command(name="ascii")
async def ascii_yaz(ctx, *, yazi: str):
    await ctx.send(f"```fix\n{yazi.upper()}\n```")

# --- START ---
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
