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
# --- 1. RENDER ÜÇÜN DİNAMİK PORTLU FLASK ---
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Yenilmez OS v1100 Ultimate aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# ==========================================
# --- 2. BOTUN SAZLANMALARI VƏ INTENTS ---
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True          # Yeni gələnləri görmək üçün vacibdir
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.presences = True 

bot = commands.Bot(command_prefix="r?", intents=intents)

# Yalnız sənin ID-n (Master Sahib)
SAHIB_ID = 641014966312501259

# Gücləndirilmiş Anti-Spam və Random/Simvol Qorunması
spam_records = {}
SPAM_THRESHOLD = 2      
SPAM_WINDOW = 4.0       

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f" [X] YENILMEZ OS v1100 ULTIMATE MASTER AKTİVDİR!")
    print(f" [X] Bot Adı: {bot.user.name}")
    print(f" [X] Sahib ID: {SAHIB_ID}")
    print(f"==================================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Elite Control 🛡️"))


# ==========================================
# --- 3. YENİ GƏLƏNLƏR ÜÇÜN SƏRT & CİDDİ SALAMLAMA ---
# ==========================================
@bot.event
async def on_member_join(member):
    # Əgər serverdə 'salam' və ya 'chat' adında kanal varsa oraya yazır, yoxdursa ümumi sistem kanalına
    for channel in member.guild.text_channels:
        if "salam" in channel.name or "chat" in channel.name or "genel" in channel.name or "sohbet" in channel.name:
            try:
                await channel.send(f"Salam, xoş gəlmisiz, {member.mention}.")
                return
            except:
                pass
    
    # Əgər uyğun kanal tapılmasa, ilk yazılabilən kanala atır
    if member.guild.system_channel:
        try:
            await member.guild.system_channel.send(f"Salam, xoş gəlmisiz, {member.mention}.")
        except:
            pass


# ==========================================
# --- 4. GÜCLƏNDİRİLMİŞ ANTİ-SPAM & RANDOM QORUNMASI ---
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Adminlər və Sahib bu qorunmadan azaddır
    if message.author.guild_permissions.administrator or message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    current_time = time.time()
    author_id = message.author.id

    if author_id not in spam_records:
        spam_records[author_id] = {"last_time": current_time, "warns": 0}
    else:
        data = spam_records[author_id]
        if current_time - data["last_time"] < SPAM_WINDOW:
            data["last_time"] = current_time
            
            try:
                await message.delete()
            except:
                pass

            data["warns"] += 1
            if data["warns"] == 1:
                try:
                    await message.channel.send(f"⚠️ {message.author.mention}, random və ya sürətli mesaj (spam) yazmaq qadağandır!", delete_after=4)
                except:
                    pass
            elif data["warns"] >= 2:
                try:
                    await message.author.timeout(timedelta(minutes=5), reason="Spam / Random")
                    await message.channel.send(f"🔇 {message.author.mention}, spam/random cəhdinə görə 5 dəqiqəlik mute olundun!", delete_after=5)
                    data["warns"] = 0 
                except:
                    pass
            return
        else:
            data["last_time"] = current_time
            if data["warns"] > 0:
                data["warns"] -= 1

    await bot.process_commands(message)


# ==========================================
# --- 5. BÜTÜN EMOJİLƏR ÜÇÜN UNIVERSAL AVTO-REAKTİV SİSTEMİ ---
# ==========================================
EMOJI_GRUPLARI = {
    "🤣": ["😂", "😆", "💀", "😹"],
    "😂": ["🤣", "😆", "💀", "😹"],
    "😆": ["🤣", "😂", "💀", "🗿"],
    "💀": ["🤣", "😂", "🗿", "🔥"],
    "😹": ["🤣", "😂", "💀", "😆"],
    "🗿": ["💀", "🔥", "👑", "💯"],
    "😭": ["😢", "😿", "💧", "🥺", "💔"],
    "😢": ["😭", "😿", "💧", "🥺"],
    "🥺": ["😭", "😢", "💧", "💔"],
    "💔": ["❤️‍🔥", "❤️", "🖤", "😢"],
    "🐎": ["🦄", "🐴", "⚡", "🔥", "🐾"],
    "🦄": ["🐎", "🐴", "✨", "💫"],
    "🐴": ["🐎", "🦄", "⚡", "🐾"],
    "🔥": ["⚡", "💀", "👑", "💯", "💥"],
    "⚡": ["🔥", "💀", "⭐", "💥"],
    "👑": ["🔥", "⚡", "💀", "💯"],
    "💯": ["🔥", "👑", "⚡", "💀"],
    "❤️": ["💖", "💘", "💓", "🖤", "🔥"],
    "💖": ["❤️", "💘", "💓", "✨"],
    "🖤": ["❤️", "🤍", "💜", "🔥"],
    "💑": ["❤️", "💖", "🔥", "✨"], 
    "😡": ["🤬", "💢", "👊", "🔥"],
    "🤬": ["😡", "💢", "💀", "🔥"],
    "⚔️": ["🛡️", "🔥", "💀", "🏆", "⚡"],
    "🛡️": ["⚔️", "🔥", "💀", "⚡"],
    "👊": ["🔥", "💀", "💢", "👊"],
    "🫵": ["🔥", "💀", "👑", "💯"]
}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id != SAHIB_ID and payload.user_id != bot.user.id:
        return
    
    if payload.guild_id is None:
        return

    channel = bot.get_channel(payload.channel_id)
    if not channel:
        return

    try:
        message = await channel.fetch_message(payload.message_id)
    except:
        return

    if payload.user_id == bot.user.id:
        return

    emoji_str = str(payload.emoji)
    temiz_emoji = emoji_str.replace("\U0001fffb", "").replace("\U0001fffc", "").replace("\U0001fffd", "").replace("\U0001fffe", "").replace("\U0001ffff", "")

    hedef_emojiler = []
    if emoji_str in EMOJI_GRUPLARI:
        hedef_emojiler = EMOJI_GRUPLARI[emoji_str]
    elif temiz_emoji in EMOJI_GRUPLARI:
        hedef_emojiler = EMOJI_GRUPLARI[temiz_emoji]
    else:
        hedef_emojiler = ["🔥", "💀", "⚡", "👑"]

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
        await ctx.send("❌ Bu panel yalnız botun sahibinə məxsusdur!")
        return

    embed = discord.Embed(
        title="💀 YENİLMEZ OS // ELITE MASTER PANEL v1100",
        description="Serverin idarəetmə mərkəzi və xüsusi səlahiyyətli əmrlər siyahısı:",
        color=0x050505
    )
    embed.add_field(
        name="👑 1. Sizin Xüsusi Sahib Əmrləriniz (Özəl)", 
        value="• `r?elan [mətn]` — Rəsmi elan atır\n• `r?anket [sual]` — Serverdə səsvermə anket açır\n• `r?cekilis [vaxt] [hədiyyə]` — Avtomatik vaxtlı çəkiliş", 
        inline=False
    )
    embed.add_field(
        name="📊 2. Server & Məlumat Sistemləri", 
        value="• `r?server` — Server haqqında ətraflı məlumat və aktiv üzvlər", 
        inline=False
    )
    embed.add_field(
        name="🔊 3. Səs Sistemi İdarəsi", 
        value="• `r?join` — Səs kanalına qoşular\n• `r?leave` — Səs kanalından ayrılar", 
        inline=False
    )
    embed.add_field(
        name="🛡️ 4. Sərt Moderasiya & Təhlükəsizlik", 
        value="• `r?sil [say]` — Mesajları təmizləyər\n• `r?mute / r?unmute` — Susdurma əməliyyatları\n• `r?ban / r?kick` — Qovma əməliyyatları\n• `r?lock / r?unlock` — Kanalı bağlar/açar", 
        inline=False
    )
    embed.add_field(
        name="⚔️ 5. Oyunlar & Əyləncə", 
        value="• `r?duel` • `r?coinflip` • `r?hacker` • `r?kasa`", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS Elite - All Rights Reserved 2026")
    await ctx.send(embed=embed)


# ==========================================
# --- 7. ÜMUMI ƏMRLƏR & SERVER MƏLUMAT (r?server) ---
# ==========================================
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"⚡ Ping: **{round(bot.latency * 1000)}ms**")

@bot.command(name="server", aliases=["serverinfo", "bilgi"])
async def server_info(ctx):
    guild = ctx.guild
    
    online_count = sum(1 for m in guild.members if m.status == discord.Status.online)
    idle_count = sum(1 for m in guild.members if m.status == discord.Status.idle)
    dnd_count = sum(1 for m in guild.members if m.status == discord.Status.dnd)
    offline_count = sum(1 for m in guild.members if m.status == discord.Status.offline)
    
    embed = discord.Embed(
        title=f"🛡️ {guild.name} — Server Haqqında Məlumat",
        color=0x050505
    )
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
        
    embed.add_field(
        name="👑 Server Sahib", 
        value=f"{guild.owner.mention if guild.owner else 'Naməlum'}", 
        inline=True
    )
    embed.add_field(
        name="📅 Yaradılma Tarixi", 
        value=f"<t:{int(guild.created_at.timestamp())}:R>", 
        inline=True
    )
    embed.add_field(
        name="👥 Toplam Üzv Sayı", 
        value=f"**{guild.member_count}** nəfər", 
        inline=True
    )
    embed.add_field(
        name="🟢 Aktiv Üzvlər (Statuslar)", 
        value=f"🟢 Online: **{online_count}**\n🌙 Boşda (Idle): **{idle_count}**\n🔴 Narahat Etməyin (DND): **{dnd_count}**\n⚪ Offline: **{offline_count}**", 
        inline=False
    )
    embed.add_field(
        name="💬 Kanal Məlumatları", 
        value=f"📁 Kateqoriyalar: {len(guild.categories)}\n💬 Mətn Kanalları: {len(guild.text_channels)}\n🔊 Səs Kanalları: {len(guild.voice_channels)}", 
        inline=False
    )
    
    embed.set_footer(text=f"Sorğulayan: {ctx.author.name} | Yenilmez OS System", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)


# ==========================================
# --- 8. SƏS KANALI İDARƏSİ ---
# ==========================================
@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("⚠️ Əvvəlcə hər hansı bir səs kanalına qoşulmalısan!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"🔊 Bağlandım səs kanalına: **{channel.name}** 🎙️")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Səs kanalından ayrıldım.")
    else:
        await ctx.send("⚠️ Onsuz da heç bir səs kanalında deyiləm!")


# ==========================================
# --- 9. SAHİBƏ ÖZƏL: ELAN, ANKET, AVTO-ÇƏKİLİŞ ---
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız botun sahibi işlədə bilər!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 RƏSMİ SERVER ELANI", description=elan_metni, color=0x050505)
    embed.set_footer(text=f"Elan edən Sahib: {ctx.author.name}")
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("📢")

@bot.command(name="anket")
async def anket(ctx, *, anket_suali: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmr yalnız sahibə özəldir!")
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
        await ctx.send("❌ Bu əmr yalnız sahibə özəldir!")
        return
    await ctx.message.delete()

    saniye = 0
    try:
        if vaxt_str.endswith("s"):
            saniye = int(vaxt_str[:-1])
        elif vaxt_str.endswith("m"):
            saniye = int(vaxt_str[:-1]) * 60
        elif vaxt_str.endswith("h"):
            saniye = int(vaxt_str[:-1]) * 3600
        elif vaxt_str.endswith("d"):
            saniye = int(vaxt_str[:-1]) * 86400
        else:
            await ctx.send("⚠️ Vaxt formatı səhvdir! Məsələn: `r?cekilis 3d Promo Nitro`")
            return
    except:
        await ctx.send("⚠️ Vaxtı düzgün daxil edin! Məsələn: `3d`, `2h`, `30m`")
        return

    embed = discord.Embed(
        title="🎉 BÖYÜK AVTO-ÇƏKİLİŞ", 
        description=f"Hədiyyə: **{hediyye}**\n\nQatılmaq üçün aşağıdakı 🎁 emojisinə bas!\n⏳ Bitmə müddəti: **{vaxt_str}**", 
        color=0x050505
    )
    embed.set_footer(text="Yenilmez OS Avtomatik Çəkiliş Sistemi")
    
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
                if not user.bot:
                    istirakcilar.append(user)
            break

    if not istirakcilar:
        no_user_embed = discord.Embed(title="🎉 ÇƏKİLİŞ BİTDİ", description=f"Hədiyyə: **{hediyye}**\n\n⚠️ Heç kim 🎁 reaksiyasına basmadığı üçün qalib seçilmədi!", color=0x050505)
        await ctx.send(embed=no_user_embed)
        return

    kazanan = random.choice(istirakcilar)
    
    win_embed = discord.Embed(
        title="🏆 ÇƏKİLİŞ BİTDİ & QALİB SEÇİLDİ!", 
        description=f"Hədiyyə: **{hediyye}**\n\nTəbriklər, {kazanan.mention}! 👑\nSən avtomatik olaraq çəkilişin qalibi oldun! 🎉", 
        color=0x050505
    )
    win_embed.set_footer(text="Yenilmez OS Avtomatik Çəkiliş Sistemi")
    await ctx.send(embed=win_embed)


# ==========================================
# --- 10. MODERASİYA ---
# ==========================================
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, say: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=say)
    await ctx.send(f"🧹 {len(deleted)} mesaj silindi.", delete_after=3)

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute_cmd(ctx, member: discord.Member, dakika: int = 5):
    await member.timeout(timedelta(minutes=dakika))
    await ctx.send(f"🔇 {member.mention} {dakika} dəqiqə mute olundu.")

@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute_cmd(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} ün mute olundu (cəza qaldırıldı).")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} ban olundu!")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} serverdən atıldı!")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal kilitləndi!")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı!")


# ==========================================
# --- 11. OYUNLAR & ƏYLƏNCƏ ---
# ==========================================
@bot.command(name="duel")
async def duel(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("⚠️ Duel etmək üçün kimsəni etiketləməlisən: `r?duel @istifadəçi`")
        return
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ Gərgin döyüş başladı!\n🔥 Qalib gələn tərəf: **{kazanan.name}** oldu! 🏆")

@bot.command(name="coinflip")
async def coinflip(ctx, secim: str = None):
    if not secim:
        await ctx.send("⚠️ Seçim etməlisən: `r?coinflip yazi` və ya `r?coinflip tura`")
        return
    netice = random.choice(["yazı", "tura"])
    if secim.lower() == netice:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Təbriklər, qazandın! 😎")
    else:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Uduzdun!")

@bot.command(name="hacker")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip = f"{random.randint(40, 200)}.{random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}"
    await ctx.send(f"💻 **{target.name}** sisteminə sızıldı! IP: `{ip}` 🕵️‍♂️")

@bot.command(name="kasa")
async def kasa(ctx):
    qazanc = random.randint(100, 5000)
    await ctx.send(f"💎 Xəzinə kassası açıldı! Qənimət: **{qazanc} AZN**, {ctx.author.mention}!")

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name} - Avatar", color=0x050505)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)


# ==========================================
# --- 12. İŞƏ SALMA ---
# ==========================================
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
    
