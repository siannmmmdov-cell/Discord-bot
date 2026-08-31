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
user_xp = {}
ticket_spam_kontrol = {}

GUILD_ACAR_SOZU = "yenilmez"
XUSUSI_ROL_ADI = "Yenilməz"

@bot.event
async def on_ready():
    print(f"BOT AKTİVDİR: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Master Panel v3500"))

# --- GİRİŞ QORUMASI: İNSİZ BOTLAR ---
@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.guild.ban(member, reason="İnsiz bot girişi qadağandır!")
        except:
            pass

# --- GÜCLƏNDİRİLMİŞ SPAM, RANDOM, SALAM VƏ XP QORUMASI ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    content_lower = content.lower()
    author_id = message.author.id
    simdi = time.time()

    # XP Sistemi
    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}
    
    user_xp[author_id]["xp"] += random.randint(10, 25)
    gerekli_xp = user_xp[author_id]["level"] * 100
    
    if user_xp[author_id]["xp"] >= gerekli_xp:
        user_xp[author_id]["level"] += 1
        user_xp[author_id]["xp"] = 0
        await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Səviyyə atladın: **{user_xp[author_id]['level']}** səviyyə oldun! 🚀")

    if author_id == SAHIB_ID:
        await bot.process_commands(message)
        return

    # 1. Ağıllı Salam Sistemi
    salam_kaliplari = ["salam", "s.a", "sa", "selam", "salamun aleykum", "salamlayıram"]
    if any(k in content_lower for k in salam_kaliplari):
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

    # 3. Random / Anlamsız Simvol Spam Qoruması
    is_random = False
    if len(content) > 6 and (content.isalnum() == False or len(set(content)) < 3):
        is_random = True

    # 4. Ümumi Spam və Sürətli Mesaj Qoruması
    if author_id not in spam_kontrol:
        spam_kontrol[author_id] = []

    spam_kontrol[author_id] = [t for t in spam_kontrol[author_id] if simdi - t < 5]
    spam_kontrol[author_id].append(simdi)

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
            await after.remove_roles(rol, reason="Statusundan gildiya tagi çıxarıldı.")
        except:
            pass

# --- TƏKMİLLƏŞDİRİLMİŞ REAKSİYA SİSTEMİ ---
UYGUN_EMOJI_GRUPLARI = {
    "👍": ["✅", "💯", "🎯", "👑", "🚀", "🔥", "⭐", "💪", "👊"],
    "👎": ["❌", "⚠️", "⛔", "🛑", "👎"],
    "❤️": ["💖", "💗", "💓", "💞", "💕", "💘", "💋", "😍", "✨", "🥰", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"],
    "🔥": ["⚡", "🚀", "💥", "👑", "🌟", "✨", "💫", "🔥", "💯", "🎯"],
    "😂": ["💀", "🤣", "😹", "😆", "😅", "👻", "💥", "😁"],
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

    for qrup_adi, emojiler in UYGUN_EMOJI_GRUPLARI.items():
        if emoji_str == qrup_adi or emoji_str in emojiler:
            for exsar in random.sample(emojiler, min(4, len(emojiler))):
                if exsar != emoji_str:
                    try:
                        await message.add_reaction(exsar)
                    except:
                        pass
            break

# --- MASTER PANEL (İzahlı Versiya) ---
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        return

    embed = discord.Embed(
        title="👑 MASTER PANEL v3500 (Bütün Komutlar və İzahları)",
        description="Botun bütün gücləndirilmiş əmrləri və funksiyaları:",
        color=0x050505
    )
    embed.add_field(
        name="👑 Sahib & İdarəetmə", 
        value="`r?elan` - Elan atır (@everyone)\n`r?anket` - Səsvermə yaradır\n`r?cekilis` - Çəkiliş keçirir\n`r?duyuru` - Bildiriş paylaşır\n`r?bakim` - Baxım mesajı atır\n`r?ticketpanel` - Dəstək panelini açır", 
        inline=False
    )
    embed.add_field(
        name="🛡️ Təhlükəsizlik & Gizlilik", 
        value="`r?gizle` / `r?goster` - Kanalı gizlədir/açır\n`r?sesgizle` / `r?sesgoster` - Səs kanalını idarə edir\n`r?tumunugizle` / `r?tumunugoster` - Bütün kanalları bağlayır/açır", 
        inline=False
    )
    embed.add_field(
        name="📋 Məlumat & Statistikalar", 
        value="`r?server` - Server məlumatı\n`r?online` - Aktiv üzvlər\n`r?ping` - Gecikmə (ms)\n`r?botinfo` - İşləmə müddəti\n`r?userinfo` - İstifadəçi bilgisi\n`r?level` - Səviyyə/XP yoxlayır\n`r?hava` - Hava proqnozu\n`r?hesabla` - Riyazi hesab\n`r?rolbilgi` / `r?kanalbilgi` - Rol və kanal məlumatı", 
        inline=False
    )
    embed.add_field(
        name="🛠️ Moderasiya & İdarə", 
        value="`r?sil` / `r?temizle` - Mesaj silir\n`r?silkanal` / `r?kanalac` - Kanal idarəsi\n`r?mute` / `r?unmute` - Timeout verir\n`r?ban` / `r?unban` / `r?kick` - Cəza əmrləri\n`r?lock` / `r?unlock` - Kanalı kilidləyir\n`r?slowmode` - Yavaş rejim\n`r?temizlemesaj` - Şəxsin mesajlarını silir\n`r?nuke` - Kanalı sıfırlayır\n`r?reklamver` - Reklam embedi atır", 
        inline=False
    )
    embed.add_field(
        name="⚙️ Rol & Üzv İdarəsi", 
        value="`r?rolver` / `r?rolsil` - Rol verir/alır\n`r?rolac` / `r?rolsil_komanda` - Rol yaradır/silir\n`r?nick` - Ləqəb dəyişir\n`r?avatar` - Profil şəklini atır\n`r?yetkililer` - Adminləri göstərir\n`r?botsay` - Bot sayını yazır\n`r?uyeara` - İstifadəçi axtarır\n`r?sesdesan` - Səsdəki adamları sayır", 
        inline=False
    )
    embed.add_field(
        name="🎮 Oyunlar & Əyləncə", 
        value="`r?duel` - Duel atır\n`r?coinflip` - Yazı-tura\n`r?slot` - Slot oyunu\n`r?hacker` - Hack zarafatı\n`r?zar` - Zər atır\n`r?sevgili` - Uyğunluq yoxlayır\n`r?ascii` - ASCII yazı\n`r?iq` - IQ ölçür\n`r?rip` - Məzar şəkli\n`r?soz` - Günün sözü\n`r?8ball` - Sehrli 8 topu\n`r?istilik` - Hava istiliyi\n`r?afk` - AFK rejimi\n`r?tapsir` - Tapşırıq verir\n`r?balıq` - Balıq tutur", 
        inline=False
    )
    await ctx.send(embed=embed)

# --- 1. SAHİB & İDARƏETMƏ ---
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

# --- 2. TƏHLÜKƏSİZLİK & GİZLİLİK ---
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
        await ctx.author.voice.channel.set_permissions(ctx.guild.default_role, connect=False)
        await ctx.send("🔒 Səs kanalı gizlədildi!")
    else:
        await ctx.send("⚠️ Səs kanalında olmalısan!")

@bot.command(name="sesgoster")
async def sesgoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    if ctx.author.voice and ctx.author.voice.channel:
        await ctx.author.voice.channel.set_permissions(ctx.guild.default_role, connect=True)
        await ctx.send("🔓 Səs kanalının girişi açıldı!")
    else:
        await ctx.send("⚠️ Səs kanalında olmalısan!")

@bot.command(name="tumunugizle")
async def tumunugizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    for channel in ctx.guild.channels:
        try: await channel.set_permissions(ctx.guild.default_role, view_channel=False, connect=False)
        except: pass
    await ctx.send("🔒 Bütün kanallar gizlədildi!")

@bot.command(name="tumunugoster")
async def tumunugoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    for channel in ctx.guild.channels:
        try: await channel.set_permissions(ctx.guild.default_role, view_channel=True, connect=True)
        except: pass
    await ctx.send("🔓 Bütün kanallar açıldı!")

# --- 3. MƏLUMAT & STATİSTİKALAR ---
@bot.command(name="server")
async def server_info(ctx):
    await ctx.send(f"🛡️ **{ctx.guild.name}** | Üzv: `{ctx.guild.member_count}` | Sahib: `{ctx.guild.owner}` | Kanal sayı: `{len(ctx.guild.channels)}`")

@bot.command(name="online")
async def online_stats(ctx):
    c = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 Aktiv üzv: **{c}**")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Gecikmə: **{round(bot.latency * 1000)}ms**")

@bot.command(name="botinfo")
async def botinfo(ctx):
    await ctx.send(f"⏱️ İşləmə müddəti: `{str(timedelta(seconds=int(time.time() - START_TIMING)))}`")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    m = member or ctx.author
    roles = [r.name for r in m.roles if r.name != "@everyone"]
    await ctx.send(f"👤 **{m.name}** | ID: `{m.id}` | Qoşulma: `{m.joined_at.strftime('%Y-%m-%d')}`\nRollar: {', '.join(roles[:5])}")

@bot.command(name="level")
async def level_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    data = user_xp.get(m.id, {"xp": 0, "level": 1})
    await ctx.send(f"📊 **{m.name}** | Səviyyə: **{data['level']}** | XP: **{data['xp']}/{data['level'] * 100}**")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Baku"):
    await ctx.send(f"🌤️ `{seher}`: 28°C, Günəşli və isti.")

@bot.command(name="hesabla")
async def hesabla(ctx, *, ifade: str):
    try: await ctx.send(f"🧮 Nəticə: `{eval(ifade)}`")
    except: await ctx.send("⚠️ Xətali misal!")

@bot.command(name="rolbilgi")
async def rolbilgi(ctx, role: discord.Role):
    await ctx.send(f"📌 Rol: **{role.name}** | ID: `{role.id}` | Rəng: `{role.color}` | Üzv sayı: `{len(role.members)}`")

@bot.command(name="kanalbilgi")
async def kanalbilgi(ctx, channel: discord.TextChannel = None):
    k = channel or ctx.channel
    await ctx.send(f"📁 Kanal: **{k.name}** | ID: `{k.id}` | Yaradılma: `{k.created_at.strftime('%Y-%m-%d')}`")

# --- 4. MODERASİYA & İDARƏ ---
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
    await ctx.send(f"✨ Kanal təmizləndi! 🧹", delete_after=3)

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
        if ban_entry.user.name.lower() == user_name.lower():
            await ctx.guild.unban(ban_entry.user)
            await ctx.send(f"✅ `{ban_entry.user.name}` banı açıldı!")
            return
    await ctx.send("❌ Tapılmadı.")

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

@bot.command(name="temizlemesaj")
async def temizlemesaj(ctx, uye: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=50, check=lambda m: m.author == uye)
    await ctx.send(f"🧹 {uye.name} adlı şəxsin `{len(deleted)}` mesajı təmizləndi.", delete_after=3)

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID: return
    pos = ctx.channel.position
    yeni = await ctx.channel.clone(reason="Nuke olundu")
    await ctx.channel.delete()
    await yeni.edit(position=pos)
    await yeni.send("💥 Kanal sıfırlandı və yenidən quruldu! 🚀")

@bot.command(name="reklamver")
async def reklamver(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="🌟 TÖVSİYƏ / REKLAM", description=metin, color=0xff0055)
    await ctx.send(embed=embed)

# --- 5. ROL & ÜZV İDARƏSİ ---
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

@bot.command(name="rolac")
async def rolac(ctx, *, rol_adi: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.guild.create_role(name=rol_adi, color=discord.Color.random())
    await ctx.send(f"✨ Yeni rol yaradıldı: **{rol_adi}**")

@bot.command(name="rolsil_komanda")
async def rolsil_komanda(ctx, role: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await role.delete()
    await ctx.send(f"🗑️ Rol silindi.")

@bot.command(name="nick")
async def nick(ctx, member: discord.Member, *, yeni_ad: str):
    if ctx.author.id != SAHIB_ID: return
    await member.edit(nick=yeni_ad)
    await ctx.send("📝 Ad dəyişdi.")

@bot.command(name="avatar")
async def avata
# --- START ---
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if not token:
        print("XƏTA: TOKEN tapılmadı! Render mühitində (Environment Variables) TOKEN əlavə etdiyinizdən əmin olun.")
    else:
        bot.run(token)
        
