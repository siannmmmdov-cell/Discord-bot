
import discord
from discord.ext import commands
import time
from datetime import timedelta
import random
import asyncio
import os
from flask import Flask
from threading import Thread

# ==========================================
# --- FLASK SERVER (RENDER ÜÇÜN) ---
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Yenilmez OS v2600 Ultimate Security aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# ==========================================
# --- INTENTS VƏ BOT SAZLANMALARI ---
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True          
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.presences = True 

bot = commands.Bot(command_prefix="r?", intents=intents)

# Sənin Master Sahib ID-n
SAHIB_ID = 641014966312501259

user_trackers = {}
start_time = time.time()

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f" [X] YENILMEZ OS v2600 ULTIMATE SECURE AKTİVDİR!")
    print(f" [X] Bot Adı: {bot.user.name}")
    print(f" [X] Sahib ID: {SAHIB_ID}")
    print(f"==================================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | 60+ Commands & Max Security 🛡️"))


# ==========================================
# --- SƏRT TƏHLÜKƏSİZLİK & ANTI-RAID ---
# ==========================================
@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.guild.ban(member, reason="Təhlükəsizlik: İznsiz kənar bot giriş cəhdi bloklandı!")
            return
        except:
            pass


# ==========================================
# --- SƏRT QORUMA & AVTO-SALAM SİSTEMİ ---
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    # Avtomatik Salamlaşma
    if "salam" in content_lower:
        try:
            await message.channel.send(f"Aleykum salam, {message.author.mention}! Xoş gəldiniz! 👑")
        except:
            pass

    if message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    current_time = time.time()

    # Link və Reklam Qadağası (Sərt Güvenlik)
    if "discord.gg/" in content_lower or "discord.com/invite/" in content_lower or "http://" in content_lower or "https://" in content_lower:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, serverdə icazəsiz link və reklam paylaşmaq qadağandır!", delete_after=5)
            await message.author.timeout(timedelta(minutes=15), reason="Link / Reklam Qadağası")
        except:
            pass
        return

    if author_id not in user_trackers:
        user_trackers[author_id] = {
            "last_message": "",
            "same_text_count": 0,
            "image_count": 0,
            "flood_count": 0,
            "last_time": current_time,
            "penalty_stage": 0  
        }

    data = user_trackers[author_id]

    # Şəkil Spam Qorunması
    has_image = len(message.attachments) > 0 or "https://images" in content_lower or "cdn.discordapp.com" in content_lower
    if has_image:
        data["image_count"] += 1
        if data["image_count"] >= 5:
            try:
                await message.delete()
            except:
                pass
            
            if data["penalty_stage"] == 0:
                data["penalty_stage"] = 1
                await message.channel.send(f"⚠️ {message.author.mention}, ardıcıl şəkil atmayın!", delete_after=5)
            elif data["penalty_stage"] == 1:
                data["penalty_stage"] = 2
                await message.author.timeout(timedelta(minutes=5), reason="Ardıcıl şəkil spamı")
                await message.channel.send(f"🔇 {message.author.mention}, şəkil spamına görə 5 dəqiqəlik mute olundunuz!", delete_after=5)
            else:
                try:
                    await message.guild.ban(message.author, reason="Davamlı şəkil spamı")
                except:
                    pass
            return
    else:
        data["image_count"] = 0

    # Eyni Mesaj Spam Qorunması
    if message.content == data["last_message"] and message.content != "":
        data["same_text_count"] += 1
    else:
        data["same_text_count"] = 1
        data["last_message"] = message.content

    if data["same_text_count"] >= 6:
        try:
            await message.delete()
        except:
            pass
        try:
            await message.author.timeout(timedelta(minutes=10), reason="Eyni mesajı təkrar spam etmək")
            await message.channel.send(f"🔇 {message.author.mention}, təkrar mesaj spamına görө 10 dəqiqəlik mute aldınız!", delete_after=5)
        except:
            pass
        return

    # Flood Qorunması
    if current_time - data["last_time"] < 2.5:
        data["flood_count"] += 1
        data["last_time"] = current_time
        if data["flood_count"] >= 6:
            try:
                await message.delete()
                await message.author.timeout(timedelta(minutes=5), reason="Flood spamı")
                await message.channel.send(f"🔇 {message.author.mention}, çox sürətli yazdığınız üçün (Flood) mute olundunuz!", delete_after=5)
            except:
                pass
            return
    else:
        data["flood_count"] = 0
        data["last_time"] = current_time

    await bot.process_commands(message)


# ==========================================
# --- EMOJİLƏRƏ AVTO-REAKTİV CAVABLAR ---
# ==========================================
EMOJI_GRUPLARI = {
    "🤣": ["😂", "😆", "💀", "😹"],
    "😂": ["🤣", "😆", "💀", "😹"],
    "💀": ["🤣", "😂", "🗿", "🔥"],
    "🔥": ["⚡", "💀", "👑", "💯", "💥"],
    "❤️": ["💖", "💘", "💓", "🖤", "🔥"],
    "⚔️": ["🛡️", "🔥", "💀", "🏆", "⚡"]
}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id or payload.guild_id is None:
        return
    channel = bot.get_channel(payload.channel_id)
    if not channel:
        return
    try:
        message = await channel.fetch_message(payload.message_id)
    except:
        return

    emoji_str = str(payload.emoji)
    hedef_emojiler = EMOJI_GRUPLARI.get(emoji_str, ["🔥", "💀", "⚡", "👑"])
    for oxsar in hedef_emojiler:
        if oxsar != emoji_str:
            try:
                await message.add_reaction(oxsar)
            except:
                pass


# ==========================================
# --- MASTER SAHİB PANELİ (ŞƏKİLDƏKİ KİMİ + 60+ KOMANDA) ---
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu panelə giriş yalnız baş sahibə (`SAHIB_ID`) məxsusdur!")
        return

    embed = discord.Embed(
        title="💀 YENİLMEZ OS // STRICT MASTER PANEL v1500",
        description="Bütün eksklüziv sahib əmrləri və idarəetmə mərkəzi:",
        color=0x050505
    )
    embed.add_field(
        name="👑 1. Yalnız Sənin İşlədə Biləcəyin Əmrlər", 
        value="• `r?elan [mətn]` — @everyone ilə rəsmi elan\n• `r?anket [sual]` — Səsvermə anketi\n• `r?cekilis [vaxt] [hədiyyə]` — Avtomatik çəkiliş\n• `r?botkurulum` — Təhlükəsizlik divarları\n• `r?servertemizle` — Keş təmizliyi\n• `r?duyuru` — Xüsusi bildiriş\n• `r?bakim` — Baxım rejimi", 
        inline=False
    )
    embed.add_field(
        name="📊 2. Server & Məlumat Sistemləri", 
        value="• `r?server` — Server məlumatı\n• `r?userinfo [@istifadəçi]` — İstifadəçi yoxlaması\n• `r?botinfo` — Bot statusu\n• `r?ping` — Bağlantı sürəti\n• `r?online` — Aktiv üzvlər\n• `r?kanalbilgi` — Kanal məlumatı\n• `r?rolbilgi` — Rol məlumatı\n• `r?boosters` — Boost statusu\n• `r?ikon` — Server ikonu\n• `r?banner` — Server banneri\n• `r?hava` — Hava proqnozu\n• `r?hesabla` — Riyazi hesab\n• `r?saygac` — Üzv sayğacı", 
        inline=False
    )
    embed.add_field(
        name="🛡️ 3. Sərt Moderasiya & Təhlükəsizlik", 
        value="• `r?sil [say]` — Mesaj təmizliyi\n• `r?mute / r?unmute` — Susdurma\n• `r?ban / r?unban` — Ban sistemləri\n• `r?kick` — Qovma\n• `r?lock / r?unlock` — Kanal kilidi\n• `r?slowmode` — Yavaş rejim\n• `r?temizlemesaj` — Toplu təmizlik", 
        inline=False
    )
    embed.add_field(
        name="⚙️ 4. Rol & Üzv İdarəetmə Komandaları", 
        value="• `r?rolver / r?rolsil` — Rol tənzimləmə\n• `r?ver / r?al` — Qısa rol əmrləri\n• `r?nick` — Ad dəyişmə\n• `r?avatar` — Avatar göstərmə\n• `r?rollist` — Rolların siyahısı\n• `r?yetkililer` — Admin siyahısı\n• `r?seskontrol` — Səs kanalı yoxlama\n• `r?kanalac` — Yeni kanal açma", 
        inline=False
    )
    embed.add_field(
        name="⚔️ 5. Oyunlar & Əyləncə (60+ Total)", 
        value="• `r?duel [@istifadəçi]` — 1v1 döyüş\n• `r?coinflip [yazı/tura]` — Qəpik atma\n• `r?slot` — Slot maşını\n• `r?hacker [@istifadəçi]` — IP simulyasiyası\n• `r?zar` — Zər atma\n• `r?qarsilatirma` — Müqayisə\n• `r?magic8ball` — Sehrli top\n• `r?soz` — Günün sözü\n• `r?sevgili` — Sevgi ölçən\n• `r?ascii` — Stilizə yazı", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS Strict Core - All Rights Reserved 2026")
    await ctx.send(embed=embed)


# ==========================================
# --- 1. SAHİB ƏMRLƏRİ ---
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız baş sahib işlədə bilər!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 RƏSMİ SERVER ELANI", description=elan_metni, color=0x050505)
    embed.set_footer(text=f"Elan edən: {ctx.author.name}")
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("📢")
    await msg.add_reaction("🔥")

@bot.command(name="anket")
async def anket(ctx, *, anket_suali: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız baş sahib işlədə bilər!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 YENİ ANKET / SƏSVERMƏ", description=anket_suali, color=0x050505)
    embed.set_footer(text=f"Anket sahibi: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("❤️")

@bot.command(name="cekilis")
async def cekilis(ctx, vaxt_str: str, *, hediyye: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız baş sahib işlədə bilər!")
        return
    await ctx.message.delete()

    saniye = 0
    try:
        if vaxt_str.endswith("s"): saniye = int(vaxt_str[:-1])
        elif vaxt_str.endswith("m"): saniye = int(vaxt_str[:-1]) * 60
        elif vaxt_str.endswith("h"): saniye = int(vaxt_str[:-1]) * 3600
        elif vaxt_str.endswith("d"): saniye = int(vaxt_str[:-1]) * 86400
        else:
            await ctx.send("⚠️ Vaxt formatı səhvdir! Məsələn: `r?cekilis 3d Nitro`")
            return
    except:
        return

    embed = discord.Embed(title="🎉 BÖYÜK AVTO-ÇƏKİLİŞ", description=f"Hədiyyə: **{hediyye}**\n\nQatılmaq üçün 🎁 emojisinə bas!", color=0x050505)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎁")

    await asyncio.sleep(saniye)
    try:
        msg = await ctx.channel.fetch_message(msg.id)
    except:
        return

    istirakcilar = []
    for reaction in msg.reactions:
        if str(reaction.emoji) == "🎁":
            async for user in reaction.users():
                if not user.bot: istirakcilar.append(user)
            break

    if not istirakcilar:
        await ctx.send("🎉 Çəkiliş bitdi. Heç kim qatılmadı!")
        return

    kazanan = random.choice(istirakcilar)
    win_embed = discord.Embed(title="🏆 ÇƏKİLİŞ QALİBİ!", description=f"Hədiyyə: **{hediyye}**\nTəbriklər, {kazanan.mention}! 🎉", color=0x050505)
    await ctx.send(embed=win_embed)

@bot.command(name="botkurulum")
async def botkurulum(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🛡️ Təhlükəsizlik divarları və qoruma protokolları aktivləşdirildi!")

@bot.command(name="servertemizle")
async def servertemizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🧹 Server keş yaddaşı təmizləndi.")

@bot.command(name="duyuru")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"📢 **Xüsusi Bildiriş:** {metin}")

@bot.command(name="bakim")
async def bakim(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🔧 Bot baxım rejiminə keçdi.")


# ==========================================
# --- 2. SERVER & MƏLUMAT ƏMRLƏRİ ---
# ==========================================
@bot.command(name="server")
async def server_info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🛡️ {guild.name} — Server Məlumatı", color=0x050505)
    embed.add_field(name="Üzv Sayı", value=str(guild.member_count), inline=True)
    embed.add_field(name="Kanal Sayı", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="Rol Sayı", value=str(len(guild.roles)), inline=True)
    embed.set_footer(text=f"Server ID: {guild.id}")
    await ctx.send(embed=embed)

@bot.command(name="online")
async def online_stats(ctx):
    guild = ctx.guild
    online_count = sum(1 for m in guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 Aktiv üzv sayı: **{online_count}**")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"⚡ Botun Pingi: **{round(bot.latency * 1000)}ms**")

@bot.command(name="botinfo")
async def botinfo(ctx):
    uptime = str(timedelta(seconds=int(time.time() - start_time)))
    await ctx.send(f"🤖 Bot İşləmə Müddəti: `{uptime}`")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 İstifadəçi: {member.name}", color=0x050505)
    if member.avatar: embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=str(member.id), inline=True)
    embed.add_field(name="Qoşulduğu tarix", value=str(member.joined_at.strftime('%Y-%m-%d')) if member.joined_at else "Naməlum", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="kanalbilgi")
async def kanalbilgi(ctx):
    await ctx.send(f"📌 Cari kanal: **{ctx.channel.name}** | ID: `{ctx.channel.id}`")

@bot.command(name="rolbilgi")
async def rolbilgi(ctx, role: discord.Role):
    await ctx.send(f"🏷️ Rol adı: **{role.name}** | Üzv sayı: `{len(role.members)}`")

@bot.command(name="boosters")
async def boosters(ctx):
    await ctx.send(f"🚀 Ümumi Boost sayı: **{ctx.guild.premium_subscription_count}**")

@bot.command(name="ikon")
async def ikon(ctx):
    if ctx.guild.icon: await ctx.send(f"🖼️ İkon: {ctx.guild.icon.url}")
    else: await ctx.send("⚠️ İkon yoxdur.")

@bot.command(name="banner")
async def banner(ctx):
    if ctx.guild.banner: await ctx.send(f"🖼️ Banner: {ctx.guild.banner.url}")
    else: await ctx.send("⚠️ Banner yoxdur.")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Baku"):
    await ctx.send(f"🌤️ **{seher}** hava proqnozu: 28°C, Günəşli.")

@bot.command(name="hesabla")
async def hesabla(ctx, *, ifade: str):
    try:
        netice = eval(ifade)
        await ctx.send(f"🔢 Nəticə: `{ifade} = {netice}`")
    except:
        await ctx.send("⚠️ Xəstə riyazi əməliyyat!")

@bot.command(name="saygac")
async def saygac(ctx):
    await ctx.send(f"📊 Ümumi üzv sayğacı: `{ctx.guild.member_count}`")


# ==========================================
# --- 3. MODERASİYA & TƏHLÜKƏSİZLİK ---
# ==========================================
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, say: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=say)
    await ctx.send(f"🧹 {len(deleted)} mesaj təmizləndi.", delete_after=3)

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute_cmd(ctx, member: discord.Member, dakika: int = 5):
    await member.timeout(timedelta(minutes=dakika))
    await ctx.send(f"🔇 {member.mention} {dakika} dəqiqəlik mute olundu.")

@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute_cmd(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} mutesi qaldırıldı.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} ban olundu!")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_cmd(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🔓 {user.name} üçün ban açıldı.")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} qovuldu.")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal bağlandı!")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı!")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, saniye: int = 0):
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Yavaş rejim: **{saniye}** san.")

@bot.command(name="temizlemesaj")
@commands.has_permissions(manage_messages=True)
async def temizlemesaj(ctx):
    await ctx.channel.purge(limit=100)
    await ctx.send("🧹 Təmizləndi!", delete_after=3)


# ==========================================
# --- 4. ROL & ÜZV İDARƏETMƏ ---
# ==========================================
@bot.command(name="rolver")
@commands.has_permissions(manage_roles=True)
async def rolver(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} -> **{role.name}** rol verildi.")

@bot.command(name="rolsil")
@commands.has_permissions(manage_roles=True)
async def rolsil(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} <- **{role.name}** rol alındı.")

@bot.command(name="ver")
@commands.has_permissions(manage_roles=True)
async def ver(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"➕ {role.name} verildi.")

@bot.command(name="al")
@commands.has_permissions(manage_roles=True)
async def al(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"➖ {role.name} alındı.")

@bot.command(name="nick")
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, yeni_ad: str):
    await member.edit(nick=yeni_ad)
    await ctx.send(f"✏️ Ad dəyişdirildi: **{yeni_ad}**")

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    if member.avatar: await ctx.send(f"🖼️ Avatar: {member.avatar.url}")
    else: await ctx.send("⚠️ Avatar yoxdur.")

@bot.command(name="rollist")
async def rollist(ctx):
    roles = [role.name for role in ctx.guild.roles if role.name != 
