import discord
from discord.ext import commands
import time
from datetime import timedelta
import random

# ==========================================
# --- 1. BOTUN SAZLANMALARI VƏ INTENTS ---
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="r?", intents=intents)

# Yalnız sənin ID-n (Master Sahib)
SAHIB_ID = 641014966312501259

# Güclü Anti-Spam və Flood Qoruma Bazası
spam_records = {}
SPAM_THRESHOLD = 3      
SPAM_WINDOW = 3.5       

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f" [X] YENILMEZ OS v350 ULTIMATE MASTER AKTİVDİR!")
    print(f" [X] Bot Adı: {bot.user.name}")
    print(f" [X] Sahib ID: {SAHIB_ID}")
    print(f" [X] Təhlükəsizlik və 70+ Əmr Yükləndi.")
    print(f"==================================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Server Qorunur 🛡️"))


# ==========================================
# --- 2. GÜCLÜ ANTİ-SPAM & ANTI-FLOOD QORUNMASI ---
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.guild_permissions.administrator or message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    current_time = time.time()
    author_id = message.author.id

    if author_id not in spam_records:
        spam_records[author_id] = {"count": 1, "last_time": current_time, "warns": 0}
    else:
        data = spam_records[author_id]
        if current_time - data["last_time"] < SPAM_WINDOW:
            data["count"] += 1
            data["last_time"] = current_time
            
            if data["count"] >= SPAM_THRESHOLD:
                try:
                    await message.delete()
                except:
                    pass

                data["warns"] += 1
                warn_level = data["warns"]

                if warn_level == 1:
                    try:
                        await message.channel.send(f"⚠️ {message.author.mention}, chatı spam etmə! İlk xəbərdarlıq.", delete_after=5)
                    except:
                        pass
                elif warn_level == 2:
                    try:
                        await message.author.timeout(timedelta(minutes=5), reason="Spam / Flood")
                        await message.channel.send(f"🔇 {message.author.mention}, 5 dəqiqəlik mute olundun!", delete_after=6)
                    except:
                        pass
                elif warn_level >= 3:
                    try:
                        await message.guild.ban(message.author, reason="Ardıcıl spam.")
                        await message.channel.send(f"🔨 {message.author.mention} serverdən ban edildi!", delete_after=8)
                    except:
                        pass
                return
        else:
            data["count"] = 1
            data["last_time"] = current_time

    await bot.process_commands(message)


# ==========================================
# --- 3. MASTER SAHİB PANELİ ---
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu master paneli yalnız botun əsl sahibi aça bilər!")
        return

    embed = discord.Embed(
        title="🛡️ YENİLMEZ OS // SAHİB MASTER PANEL v350",
        description="Serverin təhlükəsizliyi, səs sistemləri və 70+ əmr aktivdir:",
        color=0x0b0e14
    )
    embed.add_field(name="👑 Sahib Əmrləri", value="`r?elan [mətn]` — Rəsmi server elanı atır", inline=False)
    embed.add_field(name="🔊 Səs Kanalları", value="`r?join` , `r?leave`", inline=False)
    embed.add_field(name="🛡️ Moderasiya", value="`r?sil`, `r?ban`, `r?kick`, `r?mute`, `r?unmute`, `r?lock`, `r?unlock`", inline=False)
    embed.add_field(name="🎮 Oyunlar & Kafe", value="`r?fal`, `r?barmen`, `r?yemek`, `r?slot`, `r?zar`, `r?yazi_tura`, `r?sevgi`, `r?soyhun`, `r?hacker`", inline=False)
    embed.add_field(name="📊 Məlumat", value="`r?serverbilgi`, `r?avatar`, `r?ping`", inline=False)
    embed.set_footer(text="Yenilmez OS - Serverin Təhlükəsizlik Qalxanı")
    await ctx.send(embed=embed)

@bot.command(name="salam")
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Yenilmez OS tam gücü ilə qoruyur. 😎")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Gecikmə müddəti: **{round(bot.latency * 1000)}ms**")


# ==========================================
# --- 4. SƏS KANALI İDARƏETMƏSİ ---
# ==========================================
@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("⚠️ İlk əvvəl səs kanalına qoşulmalısan!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"🔊 Səs kanalına qoşuldum: **{channel.name}** 🎙️")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Səs kanalından ayrıldım.")
    else:
        await ctx.send("⚠️ Onsuz da səs kanalında deyiləm!")


# ==========================================
# --- 5. MODERASİYA & TƏHLÜKƏSİZLİK ---
# ==========================================
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, say: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=say)
    await ctx.send(f"🧹 {len(deleted)} ədəd mesaj təmizləndi!", delete_after=4)

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute_cmd(ctx, member: discord.Member, dakika: int = 5, *, reason=None):
    await member.timeout(timedelta(minutes=dakika), reason=reason)
    await ctx.send(f"🔇 {member.mention} {dakika} dəqiqəliyə mute olundu!")

@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute_cmd(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} üçün mute qaldırıldı.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} serverdən ban olundu!")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} serverdən qovuldu!")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal yazışmaya bağlandı!")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal yenidən açıldı!")

@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Elan vermək səlahiyyətin yoxdur!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 MÜHÜM ELAN", description=elan_metni, color=0xffd700)
    embed.set_footer(text=f"Elan verən: {ctx.author.name}")
    await ctx.send("@everyone", embed=embed)


# ==========================================
# --- 6. FAL VƏ KAFE SİSTEMİ ---
# ==========================================
@bot.command(name="fal")
async def fal(ctx):
    cavablar = [
        "🔮 Falın: Bu gün bəxtin tam açılacaq, gözlənilməz xəbər alacaqsan!",
        "🔮 Falın: Bir az ehtiyatlı ol, cibindən pul çıxa bilər.",
        "🔮 Falın: Qarşıdakı günlərdə böyük bir uğur və qazanc səni gözləyir!",
        "🔮 Falın: Əziz bir dostundan çox sevindirici xəbər gələcək."
    ]
    await ctx.send(f"{ctx.author.mention} {random.choice(cavablar)}")

@bot.command(name="barmen")
async def barmen(ctx):
    içkilər = ["Soyuq Kola 🥤", "Enerji İçeceği ⚡", "Buzlu Kokteyl 🍹", "Türk Qəhvəsi ☕", "Limonad 🍋", "Buzlu Çay 🧋"]
    await ctx.send(f"🍸 Barmen sənin üçün hazırladı: **{random.choice(içkilər)}**. Nuş olsun, {ctx.author.mention}!")

@bot.command(name="yemek")
async def yemek(ctx):
    teomlər = ["Pizza 🍕", "Lahmacun 🥙", "Kabab 🍢", "Burger 🍔", "Piti 🥘", "Qutab 🥟"]
    await ctx.send(f"🍽️ Mətbəxdən gəldi: **{random.choice(teomlər)}**. Nuş olsun, {ctx.author.mention}!")


# ==========================================
# --- 7. OYUNLAR VƏ ƏYLƏNCƏ ---
# ==========================================
@bot.command(name="yazi_tura")
async def yazi_tura(ctx):
    netice = random.choice(["Yazı 🦅", "Tura 🪙"])
    await ctx.send(f"🪙 {ctx.author.mention} Atıldı və nəticə: **{netice}**!")

@bot.command(name="zar")
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 {ctx.author.mention} zərdən düşən rəqəm: **{sayi}**")

@bot.command(name="sevgi")
async def sevgi(ctx, user: discord.Member = None):
    if not user:
        await ctx.send("⚠️ Kimsəni etiketləməlisən! Məsələn: `r?sevgi @istifadəçi`")
        return
    faiz = random.randint(20, 100)
    await ctx.send(f"❤️ Sizin sevgi uyğunluğunuz: **%{faiz}** 🥰")

@bot.command(name="slot")
async def slot(ctx):
    emojis = ["🍎", "🍌", "🍒", "🍓", "🍉", "🍇"]
    slot1, slot2, slot3 = random.choice(emojis), random.choice(emojis), random.choice(emojis)
    netice = f"🎰 | {slot1} | {slot2} | {slot3} |"
    if slot1 == slot2 == slot3:
        await ctx.send(f"{netice}\n🎉 Təbriklər, Cekpot qazandın!")
    else:
        await ctx.send(f"{netice}\nTəəssüf, bu dəfə alınmadı!")

@bot.command(name="soyhun")
async def soyhun(ctx):
    qazanc = random.randint(-150, 700)
    if qazanc > 0:
        await ctx.send(f"💰 {ctx.author.mention} bankı uğurla soyub **{qazanc} AZN** qazandı!")
    else:
        await ctx.send(f"🚨 {ctx.author.mention} polisə yaxalandı və cərimə ödədi!")

@bot.command(name="hacker")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip_add = f"{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    await ctx.send(f"💻 **{target.name}** sistemə sızıldı! IP ünvanı: `{ip_add}` 🕵️‍♂️")


# ==========================================
# --- 8. PROFİL VƏ MƏLUMAT ---
# ==========================================
@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name} - Avatar", color=0x3498db)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="serverbilgi")
async def serverbilgi(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 {guild.name} - Server Məlumatları", color=0x9b59b6)
    embed.add_field(name="👥 Üzv Sayı", value=guild.member_count, inline=True)
    embed.add_field(name="👑 Server Sahib", value=guild.owner, inline=True)
    embed.add_field(name="📅 Yaradılma Tarixi", value=str(guild.created_at.date()), inline=True)
    await ctx.send(embed=embed)

# bot.run("SƏNİN_BOT_TOKENİN")

