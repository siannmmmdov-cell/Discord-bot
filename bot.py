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
START_TIMING = time.time()
spam_kontrol = {}
salam_flood_kontrol = {}

# Tənzimlənən gildiya/klan etiket açar sözü
GUILD_ACAR_SOZU = "yenilmez"
XUSUSI_ROL_ADI = "Yenilməz"

@bot.event
async def on_ready():
    print(f"BOT AKTİVDİR: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Master Panel"))

# --- GİRİŞ QORUMASI: İNSİZ BOTLAR ---
@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.guild.ban(member, reason="İnsiz bot girişi qadağandır!")
        except:
            pass

# --- GÜCLƏNDİRİLMİŞ SPAM, RANDOM VƏ SALAM QORUMASI ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    content_lower = content.lower()
    author_id = message.author.id
    simdi = time.time()

    if author_id == SAHIB_ID:
        await bot.process_commands(message)
        return

    # 1. Ağıllı Salam Sistemi (Müxtəlif salam variantlarını tanıyır)
    salam_kaliplari = ["salam", "s.a", "sa", "selam", "salamun aleykum", "salamlayıram"]
    if any(salam_kaliplari in content_lower for salam_kaliplari in ["salam", "selam", "s.a", "sa"]):
        if author_id not in salam_flood_kontrol:
            salam_flood_kontrol[author_id] = []
        
        salam_flood_kontrol[author_id] = [t for t in salam_flood_kontrol[author_id] if simdi - t < 15]
        salam_flood_kontrol[author_id].append(simdi)

        if len(salam_flood_kontrol[author_id]) >= 3:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Flood etmə, sakit ol!")
                salam_flood_kontrol[author_id] = []
            except:
                pass
            return
        else:
            # Tək salam yazanda cavab verməsi
            if content_lower in ["salam", "sa", "s.a", "selam"]:
                await message.channel.send(f"Aleykum salam, {message.author.mention}! Xoş gəldin 👑")

    # 2. Reklam və Dəvət Linki Qoruması
    if "discord.gg/" in content_lower or "discord.com/invite/" in content_lower or "https://" in content_lower:
        try:
            await message.delete()
            await message.author.timeout(timedelta(minutes=15), reason="Link / Reklam qadağandır!")
            await message.channel.send(f"⚠️ {message.author.mention}, link paylaşmaq qadağandır və 15 dəqiqəlik mute olundun!", delete_after=5)
        except:
            pass
        return

    # 3. Random / Anlamsız Simvol Spam Qoruması (Botu aldatmaq üçün atılan randomlar)
    # Əgər mətn qısa olub içində mənasız ardıcıl hərflər və ya çoxlu simvollar varsa
    is_random = False
    if len(content) > 6 and (content.isalnum() == False or len(set(content)) < 3):
        # Təkrar simvol və ya həddindən artıq işarə yoxlaması
        is_random = True

    # 4. Ümumi Spam və Sürətli Mesaj (Random daxil) Qoruması
    if author_id not in spam_kontrol:
        spam_kontrol[author_id] = []

    spam_kontrol[author_id] = [t for t in spam_kontrol[author_id] if simdi - t < 5]
    spam_kontrol[author_id].append(simdi)

    # Əgər qısa müddətdə 4-dən çox mesaj atıbsa və ya random atıbsa
    if len(spam_kontrol[author_id]) >= 4 or is_random:
        try:
            await message.delete()
            await message.author.timeout(timedelta(minutes=5), reason="Spam və ya mənasız random atmaq qadağandır!")
            await message.channel.send(f"🚨 {message.author.mention}, spam/random atdığın üçün 5 dəqiqəlik cəzalandırıldın!", delete_after=5)
            spam_kontrol[author_id] = []
        except:
            pass
        return

    await bot.process_commands(message)

# --- ETİKET VƏ STATUS YOXLAMASI ---
@bot.event
async def on_member_update(before, after):
    rol = discord.utils.get(after.guild.roles, name=XUSUSI_ROL_ADI)
    if not rol or rol not in after.roles:
        return

    etiket_varmi = False
    for activity in after.activities:
        if isinstance(activity, discord.CustomActivity) and activity.name:
            if GUILD_ACAR_SOZU.lower() in activity.name.lower():
                etiket_varmi = True
                break

    if not etiket_varmi:
        try:
            await after.remove_roles(rol, reason="Statusundan və ya etiketindən gildiya tagi çıxarıldı.")
        except:
            pass

# --- REAKSİYA SİSTEMİ ---
UYGUN_EMOJI_GRUPLARI = {
    "👍": ["✅", "💯", "🎯", "👑", "🚀", "🔥", "⭐", "💪", "👊"],
    "👎": ["❌", "⚠️", "⛔", "🛑", "👎"],
    "❤️": ["💖", "💗", "💓", "💞", "💕", "💘", "💋", "😍", "✨", "🥰", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"],
    "🔥": ["⚡", "🚀", "💥", "👑", "🌟", "✨", "💫", "🔥", "💯", "🎯"],
    "😂": ["💀", "🤣", "😹", "😆", "😅", "👻", "💥"],
    "🎉": ["🎊", "🥳", "🏆", "🌟", "🎈", "🚀", "🎆", "🎇"]
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
    try:
        await message.add_reaction(payload.emoji)
    except:
        pass

    if emoji_str in UYGUN_EMOJI_GRUPLARI:
        secilenler = UYGUN_EMOJI_GRUPLARI[emoji_str]
        for exsar in random.sample(secilenler, min(4, len(secilenler))):
            if exsar != emoji_str:
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
        title="👑 MASTER PANEL v3404 (Ultra Qoruma)",
        description="Bütün əmrlər və sərt qoruma sistemləri:",
        color=0x050505
    )
    embed.add_field(
        name="👑 Sahib & İdarəetmə Əmrləri",
        value="• `r?elan` - Elan atır\n• `r?anket` - Anket yaradır\n• `r?cekilis` - Çəkiş qurur\n• `r?duyuru` - Bildiriş edir\n• `r?bakim` - Baxım rejimi",
        inline=False
    )
    embed.add_field(
        name="🛡️ Ultra Təhlükəsizlik & Qoruma",
        value="• `r?gizle` - Mətn kanalını gizlədir\n• `r?goster` - Mətn kanalını göstərir\n• `r?sesgizle` - Səs kanalını gizlədir\n• `r?sesgoster` - Səs kanalını açır\n• `r?tumunugizle` - Bütün kanalları gizlədir\n• `r?tumunugoster` - Bütün kanalları açır",
        inline=False
    )
    embed.add_field(
        name="📋 Məlumat Əmrləri",
        value="• `r?server` - Server məlumatı\n• `r?online` - Aktiv üzvlər\n• `r?ping` - Bot gecikməsi\n• `r?botinfo` - Bot işləmə müddəti\n• `r?userinfo` - İstifadəçi məlumatı\n• `r?hava` - Hava proqnozu\n• `r?hesabla` - Riyazi hesablama",
        inline=False
    )
    embed.add_field(
        name="🛠️ Moderasiya Əmrləri",
        value="• `r?sil` - Mesajları təmizləyir\n• `r?temizle` - Çoxlu mesaj silir\n• `r?silkanal` - Kanalı silir\n• `r?kanalac` - Yeni kanal açır\n• `r?mute` - İstifadəçini susdurur\n• `r?unmute` - Susdurmanı açır\n• `r?ban` - Serverdən banlayır\n• `r?unban` - Banı açır\n• `r?kick` - Serverdən atır\n• `r?lock` - Kanalı kilidləyir\n• `r?unlock` - Kilidi açır\n• `r?slowmode` - Yavaş rejim",
        inline=False
    )
    embed.add_field(
        name="🎮 Əyləncə Əmrləri",
        value="• `r?iq` - IQ dərəcəsi ölçür\n• `r?rip` - Məzar şəkli yaradır\n• `r?soz` - Günün sözü\n• `r?8ball` - Sehrli top\n• `r?istilik` - Hava istiliyi\n• `r?afk` - AFK rejimi",
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

@bot.command(name="duyuru")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id == SAHIB_ID:
        await ctx.message.delete()
        await ctx.send(f"📢 **Bildiriş:** {metin}")

@bot.command(name="bakim")
async def bakim(ctx):
    if ctx.author.id == SAHIB_ID: await ctx.send("🛠️ Bot baxımdadır.")

# --- MƏLUMAT & MODERASİYA ƏMRLƏRİ ---
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
    await ctx.send(f"⏱️ Uptime: `{str(timedelta(seconds=int(time.time() - START_TIMING)))}`")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"👤 **{m.name}** | ID: `{m.id}` | Qoşulma: `{m.joined_at.strftime('%Y-%m-%d')}`")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Baku"):
    await ctx.send(f"🌤️ `{seher}`: 28°C, Günəşli və isti.")

@bot.command(name="hesabla")
async def hesabla(ctx, *, ifade: str):
    try:
        await ctx.send(f"🧮 Nəticə: `{eval(ifade)}`")
    except:
        await ctx.send("⚠️ Xətali misal!")

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
    try: await k.delete()
    except Exception as e: await ctx.send(f"❌ Xəta: {e}")

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
async def unban_cmd(ctx, *, user_name: str):
    if ctx.author.id != SAHIB_ID: return
    banlar = await ctx.guild.bans()
    for ban_entry in banlar:
        user = ban_entry.user
        if user.name.lower() == user_name.lower():
            await ctx.guild.unban(user)
            await ctx.send(f"✅ `{user.name}` adlı şəxsin banı açıldı!")
            return
    await ctx.send("❌ Belə bir istifadəçi ban siyahısında tapılmadı.")

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

@bot.command(name="duel")
async def duel(ctx, member: discord.Member = None):
    if member:
        await ctx.send(f"⚔️ Qalib: **{random.choice([ctx.author, member]).name}** 🏆")

@bot.command(name="coinflip")
async def coinflip(ctx, ctx_secim: str = "yazı"):
    netice = random.choice(["yazı", "tura"])
    win = "Qazandın! 🎉" if ctx_secim.lower() == netice else "Udurdun!"
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

@bot.command(name="sevgili")
async def sevgili(ctx, member: discord.Member = None):
    if member:
        await ctx.send(f"💖 Uyğunluq: **%{random.randint(0, 100)}** 💕")

@bot.command(name="ascii")
async def ascii_yaz(ctx, *, yazi: str):
    await ctx.send(f"```fix\n{yazi.upper()}\n```")

# --- ƏYLƏNCƏ ƏMRLƏRİ ---
@bot.command(name="iq")
async def iq(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"🧠 **{target.name}** adlı şəxsin IQ səviyyəsi: **{random.randint(40, 160)}** 📊")

@bot.command(name="rip")
async def rip(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"🪦 RİP **{target.name}**\n*2026 - 2026*\nRest in Peace... 🕯️")

@bot.command(name="soz")
async def soz(ctx):
    sozler = [
        "Həyat sınaqlarla doludur, əsas odur ki, yıxılanda yenidən qalxasan!",
        "Yenilməzlər heç vaxt təslim olmazlar!",
        "Gələcək bu gün nə etdiyindən asılıdır.",
        "Məqsədinə çatmaq üçün hər zaman irəli bax!"
    ]
    await ctx.send(f"💬 **Günün Sözü:** *{random.choice(sozler)}*")

@bot.command(name="8ball")
async def eight_ball(ctx, *, soru: str):
    cavablar = ["Bəli", "Xeyr", "Əlbəttə ki!", "Mümkünsüzdür", "Bəlkə də", "Gələcək qaranlıqdır"]
    await ctx.send(f"🔮 Sual: **{soru}**\n✨ Cavab: **{random.choice(cavablar)}**")

@bot.command(name="istilik")
async def istilik(ctx):
    await ctx.send(f"🌡️ Hazırkı hava istiliyi: **{random.randint(20, 38)}°C** 🔥")

@bot.command(name="afk")
async def afk(ctx, *, sebeb: str = "Məşğul"):
    await ctx.send(f"💤 {ctx.author.mention} AFK rejiminə keçdi. Səbəb: **{sebeb}**")

# --- START ---
if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get("DISCORD_TOKEN"))
        
