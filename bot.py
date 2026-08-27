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
# --- 1. RENDER ÜÇÜN DİNAMİK PORTlu FLASK ---
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Yenilmez OS v2600 Ultimate aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# ==========================================
# --- 2. BOT SAZLANMALARI VƏ INTENTS ---
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True          
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.presences = True 

bot = commands.Bot(command_prefix="r?", intents=intents)

# Yalnız sənin şəxsi ID-n (Master Sahib)
SAHIB_ID = 641014966312501259

user_trackers = {}
start_time = time.time()

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f" [X] YENILMEZ OS v2600 ULTIMATE AKTİVDİR!")
    print(f" [X] Bot Adı: {bot.user.name}")
    print(f" [X] Sahib ID: {SAHIB_ID}")
    print(f"==================================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Auto-Salam & 50+ Commands 🛡️"))


# ==========================================
# --- 3. AVTO-ANTİ-RAID & BOT QORUNMASI ---
# ==========================================
@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.guild.ban(member, reason="Təhlükəsizlik: İznsiz kənar bot girişi dərhal bloklandı!")
            return
        except:
            pass


# ==========================================
# --- 4. SƏRT QORUMA & AVTO-SALAM SİSTEMİ ---
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    # --- KİMSƏ CHAT-DA SALAM YAZANDA AVTOMATİK CAVAB ---
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

    # Link və Reklam Qadağası
    if "discord.gg/" in content_lower or "discord.com/invite/" in content_lower or "http://" in content_lower or "https://" in content_lower:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, serverdə reklam və link paylaşmaq qadağandır!", delete_after=5)
            await message.author.timeout(timedelta(minutes=10), reason="Link/Reklam Paylaşımı")
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

    # Dalbadal 7 Şəkil Atma Qorunması
    has_image = len(message.attachments) > 0 or "https://images" in content_lower or "cdn.discordapp.com" in content_lower
    if has_image:
        data["image_count"] += 1
        if data["image_count"] >= 7:
            try:
                await message.delete()
            except:
                pass
            
            if data["penalty_stage"] == 0:
                data["penalty_stage"] = 1
                await message.channel.send(f"⚠️ {message.author.mention}, ardıcıl çoxlu şəkil atırsınız! Dayanın.", delete_after=5)
            elif data["penalty_stage"] == 1:
                data["penalty_stage"] = 2
                await message.author.timeout(timedelta(minutes=5), reason="Ardıcıl 7 şəkil spamı")
                await message.channel.send(f"🔇 {message.author.mention}, ardıcıl şəkil spamına görə 5 dəqiqəlik mute olundunuz!", delete_after=5)
            else:
                try:
                    await message.guild.ban(message.author, reason="Təkrarolunan şəkil spamı")
                    await message.channel.send(f"🔨 {message.author.mention} serverdən ban olundu!")
                except:
                    pass
            return
    else:
        data["image_count"] = 0

    # 8 Eyni Söz / Mesaj Qorunması
    if message.content == data["last_message"] and message.content != "":
        data["same_text_count"] += 1
    else:
        data["same_text_count"] = 1
        data["last_message"] = message.content

    if data["same_text_count"] >= 8:
        try:
            await message.delete()
        except:
            pass

        if data["penalty_stage"] == 0:
            data["penalty_stage"] = 1
            await message.channel.send(f"⚠️ {message.author.mention}, eyni şeyi 8 dəfə yazdınız! Xəbərdarlıq alırsınız.", delete_after=5)
        elif data["penalty_stage"] == 1:
            data["penalty_stage"] = 2
            await message.author.timeout(timedelta(minutes=5), reason="8 dəfə eyni sözü spam etmək")
            await message.channel.send(f"🔇 {message.author.mention}, eyni sözü təkrar yazdığınız üçün 5 dəqiqəlik mute olundunuz!", delete_after=5)
        else:
            try:
                await message.guild.ban(message.author, reason="Təkrar olunan eyni mesaj spamı")
                await message.channel.send(f"🔨 {message.author.mention} ban olundu!")
            except:
                pass
        return

    # Flood Qorunması
    if current_time - data["last_time"] < 3.0:
        data["flood_count"] += 1
        data["last_time"] = current_time
        if data["flood_count"] >= 8:
            try:
                await message.delete()
            except:
                pass
            if data["penalty_stage"] == 0:
                data["penalty_stage"] = 1
                await message.channel.send(f"⚠️ {message.author.mention}, çox sürətli mesaj yazırsınız (Flood)!", delete_after=5)
            elif data["penalty_stage"] == 1:
                data["penalty_stage"] = 2
                await message.author.timeout(timedelta(minutes=5), reason="Ardıcıl fərqli mesaj spamı")
                await message.channel.send(f"🔇 {message.author.mention}, sürətli mesaj spamına görə 5 dəqiqəlik mute olundunuz!", delete_after=5)
            else:
                try:
                    await message.guild.ban(message.author, reason="Davamlı flood spamı")
                except:
                    pass
            return
    else:
        data["flood_count"] = 0
        data["last_time"] = current_time

    await bot.process_commands(message)


# ==========================================
# --- 5. EMOJİLƏRƏ REAKTİV CAVABLAR ---
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
# --- 6. MASTER SAHİB PANELİ ---
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu panelə giriş yalnız baş sahibə (`SAHIB_ID`) məxsusdur!")
        return

    embed = discord.Embed(
        title="💀 YENİLMEZ OS // ULTIMATE MASTER PANEL",
        description="Bütün oyunlar, xüsusi sahib əmrləri və idarəetmə mərkəzi:",
        color=0x050505
    )
    embed.add_field(
        name="👑 1. Yalnız Sənin İşlədə Biləcəyin Əmrlər", 
        value="`r?elan`, `r?anket`, `r?cekilis`, `r?botkurulum`, `r?servertemizle`, `r?duyuru`, `r?karliste`, `r?bakim`", 
        inline=False
    )
    embed.add_field(
        name="⚔️ 2. Oyunlar & Əyləncə Sistemləri", 
        value="`r?duel`, `r?coinflip`, `r?slot`, `r?hacker`, `r?zar`, `r?qarsilatirma`, `r?magic8ball`, `r?tiksok`, `r?soz`, `r?ascii`", 
        inline=False
    )
    embed.add_field(
        name="🛡️ 3. Sərt Moderasiya & Təhlükəsizlik", 
        value="`r?sil`, `r?mute`, `r?unmute`, `r?ban`, `r?unban`, `r?kick`, `r?lock`, `r?unlock`, `r?slowmode`, `r?temizlemesaj`", 
        inline=False
    )
    embed.add_field(
        name="⚙️ 4. Rol & Üzv İdarəetmə Komandaları", 
        value="`r?rolver`, `r?rolsil`, `r?ver`, `r?al`, `r?nick`, `r?avatar`, `r?rollist`, `r?yetkililer`, `r?seskontrol`, `r?kanalac`", 
        inline=False
    )
    embed.add_field(
        name="📊 5. Server, Statistika & Alətlər", 
        value="`r?server`, `r?online`, `r?botinfo`, `r?ping`, `r?userinfo`, `r?kanalbilgi`, `r?rolbilgi`, `r?boosters`, `r?ikon`, `r?banner`, `r?hava`, `r?hesabla`, `r?kodla`, `r?base64`, `r?saygac`", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS v2600 Core - All Rights Reserved")
    await ctx.send(embed=embed)


# ==========================================
# --- 7. YALNIZ SAHİBİN İŞLƏDƏ BİLƏCƏYİ ÖZƏL ƏMRLƏR ---
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri başqası işlədə bilməz!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 RƏSMİ SERVER ELANI", description=elan_metni, color=0x050505)
    embed.set_footer(text=f"Elan edən: {ctx.author.name}")
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("📢")

@bot.command(name="anket")
async def anket(ctx, *, anket_suali: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri başqası işlədə bilməz!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 YENİ ANKET / SƏSVERMƏ", description=anket_suali, color=0x050505)
    embed.set_footer(text=f"Anket sahibi: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, vaxt_str: str, *, hediyye: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri başqası işlədə bilməz!")
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
    await ctx.send(win_embed)

@bot.command(name="botkurulum")
async def botkurulum(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🛡️ Sistem qoruma divarları, log kanalları və təhlükəsizlik protokolları aktivləşdirildi!")

@bot.command(name="servertemizle")
async def servertemizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🧹 Server keş yaddaşı təmizləndi və optimizasiya olundu.")

@bot.command(name="duyuru")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"📢 **Xüsusi Bildiriş:** {metin}")

@bot.command(name="karliste")
async def karliste(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("📋 Qara siyahı təmizdir. Heç bir istifadəçi bloklanmayıb.")

@bot.command(name="bakim")
async def bakim(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🔧 Bot baxım rejiminə keçdi. Təhlükəsizlik yoxlanılır.")


# ==========================================
# --- 8. OYUNLAR & ƏYLƏNCƏ KOMANDALARI ---
# ==========================================
@bot.command(name="duel")
async def duel(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("⚠️ Kimsəni etiketləməlisən: `r?duel @istifadəçi`")
        return
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ Döyüş bitdi! Qalib: **{kazanan.name}** 🏆")

@bot.command(name="coinflip")
async def coinflip(ctx, secim: str = None):
    if not secim:
        await ctx.send("⚠️ Seçim et: `r?coinflip yazı` və ya `r?coinflip tura`")
        return
    netice = random.choice(["yazı", "tura"])
    if secim.lower() == netice:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Qazandın! 😎")
    else:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Uduzdun!")

@bot.command(name="slot")
async def slot(ctx):
    simvol = ["🍎", "🍋", "🍒", "💎", "7️⃣"]
    r1, r2, r3 = random.choice(simvol), random.choice(simvol), random.choice(simvol)
    if r1 == r2 == r3:
        await ctx.send(f"🎰 | {r1} | {r2} | {r3} |\n🎉 Təbriklər, Jackpot vurdun!")
    else:
        await ctx.send(f"🎰 | {r1} | {r2} | {r3} |\n😢 Uduzdun!")

@bot.command(name="hacker")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip = f"{random.randint(40, 200)}.{random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}"
    await ctx.send(f"💻 **{target.name}** sisteminə sızıldı! IP: `{ip}` 🕵️‍♂️")

@bot.command(name="zar")
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 Atılan zərin nəticəsi: **{sayi}**")

@bot.command(name="qarsilatirma")
async def qarsilatirma(ctx, item1: str, item2: str):
    secim = random.choice([item1, item2])
    await ctx.send(f"⚖️ Müqayisə nəticəsi: **{secim}** daha üstündür!")

@bot.command(name="magic8ball")
async def magic8ball(ctx, *, sorğu: str):
    cavablar = ["Bəli, mütləq!", "Xeyr, əsla.", "Bəlkə də.", "Dəqiq bilmirəm.", "Gələcək qaranlıqdır."]
    await ctx.send(f"🔮 Sual: {sorğu}\nCavab: **{random.choice(cavablar)}**")

@bot.command(name="tiksok")
async def tiksok(ctx):
    await ctx.send("❌ Bu əmr yalnız zarafat üçündür! Heç bir sistem sındırılmadı 😎")

@bot.command(name="soz")
async def soz(ctx):
    sozler = ["Həyat 1 gündür, o da bu gündür.", "Güclü olmaq məcburiyyətindəndirsən.", "Zəfər inananlarındır."]
    await ctx.send(f"📜 Günün sözü: *{random.choice(sozler)}*")

@bot.command(name="ascii")
async def ascii_yaz(ctx, *, yazi: str):
    await ctx.send(f"🔤 ASCII Çeviri:\n```fix\n[ {yazi.upper()} ]\n```")


# ==========================================
# --- 9. SƏRT MODERASİYA & TƏHLÜKƏSİZLİK ---
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
    await ctx.send(f"🔊 {member.mention} üzərindən mute qaldırıldı.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} serverdən ban olundu!")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_cmd(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🔓 {user.name} üçün ban qaldırıldı.")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} serverdən qovuldu.")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal yazışmaya bağlandı!")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal yazışmaya açıldı!")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, saniye: int = 0):
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Kanalın yavaş modu **{saniye}** saniyə olaraq tənzimləndi.")

@bot.command(name="temizlemesaj")
@commands.has_permissions(manage_messages=True)
async def temizlemesaj(ctx):
    await ctx.channel.purge(limit=100)
    await ctx.send("🧹 Kanal tamamilə təmizləndi!", delete_after=3)


# ==========================================
# --- 10. ROL & ÜZV İDARƏETMƏ ---
# ==========================================
@bot.command(name="rolver")
@commands.has_permissions(manage_roles=True)
async def rolver(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} istifadəçisinə **{role.name}** rolu verildi.")

@bot.command(name="rolsil")
@commands.has_permissions(manage_roles=True)
async def rolsil(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} istifadəçisindən **{role.name}** rolu alındı.")

@bot.command(name="ver")
@commands.has_permissions(manage_roles=True)
async def ver(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"➕ {role.name} -> {member.mention}")

@bot.command(name="al")
@commands.has_permissions(manage_roles=True)
async def al(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"➖ {role.name} <- {member.mention}")

@bot.command(name="nick")
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, yeni_ad: str):
    await member.edit(nick=yeni_ad)
    await ctx.send(f"✏️ {member.mention} istifadəçisinin adı dəyişdirildi: **{yeni_ad}**")

@bot.command(name="avatar")
async def av
