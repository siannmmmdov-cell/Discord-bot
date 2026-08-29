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
salam_flood_kontrol = {}

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

    content_lower = message.content.strip().lower()
    author_id = message.author.id
    simdi = time.time()

    # Sən (Sahib) yazanda bot heç bir avtomatik cavab verməyəcək
    if author_id == SAHIB_ID:
        await bot.process_commands(message)
        return

    # Yalnız dəqiq "salam" sözü ardıcıl yazılarsa yoxlanılır
    if content_lower == "salam":
        if author_id not in salam_flood_kontrol:
            salam_flood_kontrol[author_id] = []
        
        # Son 15 saniyə içindəki salamlar nəzərə alınır
        salam_flood_kontrol[author_id] = [t for t in salam_flood_kontrol[author_id] if simdi - t < 15]
        salam_flood_kontrol[author_id].append(simdi)

        # 3 dəfə dalbadal salam yazanda işə düşür
        if len(salam_flood_kontrol[author_id]) >= 3:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Anası gehbe az salam yazda")
                salam_flood_kontrol[author_id] = []
            except:
                pass
            return

    # Link qoruması
    if "discord.gg/" in content_lower or "discord.com/invite/" in content_lower:
        try:
            await message.delete()
            await message.author.timeout(timedelta(minutes=10), reason="Dəvət linki!")
        except:
            pass
        return

    # Spam tənzimləməsi
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

# --- YALNIZ SƏNİN ÜÇÜN REAKSİYA SİSTEMİ ---
UYGUN_EMOJI_GRUPLARI = {
    "👍": ["✅", "🔥", "💯", "🎯", "👑", "🚀"],
    "❤️": ["💖", "😍", "✨", "💞", "💘", "💋"],
    "🔥": ["⚡", "🚀", "💥", "👑", "🌟", "🔥"],
    "⭐": ["🌟", "💫", "💎", "✨", "🌠", "🔥"],
    "😂": ["💀", "🤣", "😹", "🔥", "💀", "💥"],
    "🎉": ["🎊", "🥳", "🏆", "🌟", "🎈", "🚀"]
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
    secilenler = UYGUN_EMOJI_GRUPLARI.get(emoji_str, ["🔥", "⚡", "⭐", "🎯", "🚀", "💎"])
    
    for exsar in random.sample(secilenler, min(5, len(secilenler))):
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
        title="👑 MASTER PANEL v3401",
        description="Bütün əmrlər (Yalnız sənə məxsusdur):",
        color=0x050505
    )
    embed.add_field(
        name="👑 Sahib & İdarəetmə Əmrləri",
        value="`r?elan` - Elan atır\n`r?anket` - Anket yaradır\n`r?cekilis` - Çəkiş qurur\n`r?duyuru` - Bildiriş edir\n`r?bakim` - Baxım rejimi",
        inline=False
    )
    embed.add_field(
        name="🛡️ Mütləq Təhlükəsizlik & Gizlilik (Mətn və Səs)",
        value="`r?gizle` - Mətn kanalını gizlədir\n`r?goster` - Mətn kanalını açır\n`r?sesgizle` - Səs kanalını gizlədir\n`r?sesgoster` - Səs kanalını açır\n`r?tumunugizle` - Bütün kanalları (mətn+səs) gizlədir\n`r?tumunugoster` - Bütün kanalları açır",
        inline=False
    )
    embed.add_field(
        name="📋 Məlumat Əmrləri",
        value="`r?server` - Server bilgisi\n`r?userinfo` - İstifadəçi məlumatı\n`r?botinfo` - Botun işləmə müddəti\n`r?ping` - Gecikmə müddəti\n`r?online` - Aktiv üzvlər\n`r?hava` - Hava durumu\n`r?hesabla` - Riyazi hesab",
        inline=False
    )
    embed.add_field(
        name="🛠️ Moderasiya (Yalnız Sən)",
        value="`r?sil [say]` - Say ilə mesaj silir\n`r?temizle` - Chati tər-təmin təmizləyir\n`r?silkanal` - Kanalı silir\n`r?kanalac` - Yeni kanal açır\n`r?mute` / `r?unmute` - Timeout ver/al\n`r?ban` / `r?kick` - Ban/Atma\n`r?lock` / `r?unlock` - Kilidlə\n`r?slowmode` - Yavaş rejim",
        inline=False
    )
    embed.add_field(
        name="⚙️ Rol & Üzv",
        value="`r?rolver` / `r?rolsil` - Rol idarəsi\n`r?nick` - Ad dəyişir\n`r?avatar` - Avatar göstərir\n`r?yetkililer` - Admin siyahısı",
        inline=False
    )
    embed.add_field(
        name="🎮 Oyunlar & Əyləncə",
        value="`r?duel` - Duel at\n`r?coinflip` - Yazı-tura\n`r?slot` - Slot\n`r?hacker` - Hackləmə\n`r?zar` - Zər\n`r?sevgili` - Sevgi ölçən\n`r?ascii` - Şrift",
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
    await ctx.send(f"🛡️ **{ctx.guild.name}** | Üzv: `{ctx.guild.member_count}` | Sahib: `{ctx.guild.owner}`")

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
    await ctx.send(f"👤 **{m.name}** | ID: `{m.id}` | Qoşulma: `{m.joined_at.strftime('%Y-%m-%d')}`")

@bot.command(name="kanalbilgi")
async def kanalbilgi(ctx):
    await ctx.send(f"📁 Kanal: **{ctx.channel.name}** | ID: `{ctx.channel.id}`")

@bot.command(name="rolbilgi")
async def rolbilgi(ctx, role: discord.Role):
    await ctx.send(f"🛡️ Rol: **{role.name}** | Üzv: `{len(role.members)}`")

@bot.command(name="boosters")
async def boosters(ctx):
    await ctx.send(f"💎 Boost: **{ctx.guild.premium_subscription_count}**")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Baku"):
    await ctx.send(f"🌤️ `{seher}`: 28°C, Günəşli və isti.")

@bot.command(name="hesabla")
async def hesabla(ctx, *, ifade: str):
    try:
        await ctx.send(f"🧮 Nəticə: `{eval(ifade)}`")
    except:
        await ctx.send("⚠️ Xətali misal!")

# --- MODERASİYA & GİZLİLİK ƏMRLƏRİ ---

@bot.command(name="gizle")
async def gizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🔒 Bu mətn kanalı hamıdan gizlədildi!")

@bot.command(name="goster")
async def goster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🔓 Bu mətn kanalının gizliliyi açıldı!")

@bot.command(name="sesgizle")
async def sesgizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, connect=False)
        await ctx.send(f"🔇 **{channel.name}** səs kanalı hamıdan gizlədildi (bağlandı)!")
    else:
        await ctx.send("⚠️ Əvvəlcə gizlətmək istədiyiniz səs kanalına qoşulun!")

@bot.command(name="sesgoster")
async def sesgoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, connect=True)
        await ctx.send(f"🔊 **{channel.name}** səs kanalının gizliliyi açıldı!")
    else:
        await ctx.send("⚠️ Əvvəlcə açmaq istədiyiniz səs kanalına qoşulun!")

@bot.command(name="tumunugizle")
async def tumunugizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        except:
            pass
    for channel in ctx.guild.voice_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, connect=False)
        except:
            pass
    await ctx.send("🔒 Serverdəki bütün mətn və səs kanalları gizliliyə alındı!")

@bot.command(name="tumunugoster")
async def tumunugoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        except:
            pass
    for channel in ctx.guild.voice_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, connect=True)
        except:
            pass
    await ctx.send("🔓 Serverdəki bütün mətn və səs kanallarının gizliliyi açıldı!")

@bot.command(name="sil")
async def sil(ctx, say: int = 5):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=say)
    await ctx.send(f"🧹 `{len(deleted)}` mesaj silindi.", delete_after=3)

@bot.command(name="temizle")
async def temizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=100)
    await ctx.send(f"✨ Kanal tər-təmin təmizləndi! 🧹", delete_after=3)

@bot.command(name="silkanal")
async def silkanal(ctx, kanal: discord.TextChannel = None):
    if ctx.author.id != SAHIB_ID: return
    k = kanal or ctx.channel
    try:
        await k.delete()
    except Exception as e:
        await ctx.send(f"❌ Xəta: {e}")

@bot.command(name="kanalac")
async def kanalac(ctx, *, kanal_adi: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.guild.create_text_channel(kanal_adi)
    await ctx.send(f"📁 Kanal açıldı: **{kanal_adi}** 🚀")

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member, dakika: int = 5):
    if ctx.author.id != SAHIB_ID: return
    await member.timeout(timedelta(minutes=dakika))
    await ctx.send(f"🔇 {member.mention} `{dakika}` dəqiqə mute olundu.")

@bot.command(name="unmute")
async def unmute_cmd(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} mutesi açıldı.")

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} banlandı!")

@bot.command(name="unban")
async def unban_cmd(ctx, user_id: int):
    if ctx.author.id != SAHIB_ID: return
    u = await bot.fetch_user(user_id)
    await ctx.guild.unban(u)
    await ctx.send(f"🔓 {u.name} banı açıldı.")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} atıldı!")

@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal bağlandı.")

@bot.command(name="unlock")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı.")

@bot.command(name="slowmode")
async def slowmode(ctx, saniye: int = 0):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Slowmode: **{saniye}** san.")

@bot.command(name="sesmute")
async def sesmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    if member.voice:
        await member.edit(mute=True)
        await ctx.send(f"🔇 {member.mention} susduruldu.")

@bot.command(name="sesunmute")
async def sesunmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    if member.voice:
        await member.edit(mute=False)
        await ctx.send(f"🔊 {member.mention} səsi açıldı.")

# --- ROL VƏ ÜZV ---
@bot.command(name="rolver")
async def rolver(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} rol verildi.")

@bot.command(name="rolsil")
async def rolsil(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await member.remove_roles(role)
    await ctx.send(f"✅ {member.mention} rol alındı.")

@bot.command(name="nick")
async def nick(ctx, member: discord.Member, *, yeni_ad: str):
    if ctx.author.id != SAHIB_ID: return
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

# --- OYUNlar & ƏYLƏNCƏ ---
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
    bot.run(os.environ.get("DISCORD_TOKEN"))
        
