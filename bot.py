import discord
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
# RENDER VEB SERVER MODULU (KİBER-CORE)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "yenilmez firewall v22.0 [FULL-HEAVY EDITION] - System Online"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_server).start()

# ==========================================
# İNTENTS VƏ BOT KONQİQURASİYASI
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='r?', intents=intents)

# Yaddaş strukturları (Database əvəzi)
spam_tracker = {}
afk_users = {}
user_wallet = {}

# ==========================================
# BOTUN AÇILIŞ VƏ STATUS HADHİSƏLƏRİ
# ==========================================
@bot.event
async def on_ready():
    print(f'🛡️ [YENİLMEZ OS]: Kiber şəbəkə tam güclə aktivdir -> {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="r?yardim | Server Qorunur və İdarə Edilir"))

# ==========================================
# GİRİŞ-ÇIXIŞ VƏ TƏHLÜKƏSİZLİK MÜHAFİZƏSİ
# ==========================================
@bot.event
async def on_member_join(member):
    if member.bot:
        icazeli_bot_idleri = [bot.user.id] 
        if member.id not in icazeli_bot_idleri:
            try:
                await member.kick(reason="Sistem Təhlükəsizliyi: İcazəsiz kənar bot inyeksiya cəhdi bloklandı.")
            except:
                pass

# ==========================================
# QLOBAL MESAJ QORUMA VƏ FİLTER SİSTEMİ
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # AFK Sistem yoxlaması və təmizlənməsi
    if message.author.id in afk_users:
        del afk_users[message.author.id]
        try:
            await message.channel.send(f"⚠️ Sistem xəbərdarlığı: Qayıtdın, {message.author.mention}. AFK rejimi avtomatik ləğv edildi.", delete_after=5)
        except:
            pass

    for mention in message.mentions:
        if mention.id in afk_users:
            reason = afk_users[mention.id]
            try:
                await message.channel.send(f"💤 **{mention.name}** şu an AFK rejimindədir. Səbəb: `{reason}`")
            except:
                pass

    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content
    lower_content = content.lower()

    # 1. Dəqiq Salamlama Sistemi ('as' sözü filtrelenib ki səhv başa düşülməsin)
    words = lower_content.split()
    salam_sozleri = ["salam", "salamun aleykum", "sa", "slm", "səlam"]
    if any(word in salam_sozleri for word in words) and "as" not in words:
        cevaplar = [
            f"Aleykum salam, {message.author.mention}. Terminala xoş gəldin, sistem aktivdir!",
            f"Salam, {message.author.mention}. Bağlantı quruldu."
        ]
        try:
            await message.channel.send(random.choice(cevaplar))
        except:
            pass

    # 2. Qlobal Reklam və Link Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite|t\.me|instagram\.com|youtube\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ **{message.author.mention}**, bu şəbəkədə kənar link və reklam paylaşmaq qəti şəkildə qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. @everyone / @here Qlobal Qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ **{message.author.mention}**, kütləvi etiket (`@everyone/@here`) atmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 4. Sərt Spam / Flood Qoruması (Anti-Spam)
    author_id = message.author.id
    current_time = time.time()

    if author_id not in spam_tracker:
        spam_tracker[author_id] = []

    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 3]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) > 5:
        spam_tracker[author_id].clear()
        try:
            await message.delete()
            duration = timedelta(minutes=5)
            await message.author.timeout(duration, reason="Sistem Mühafizəsi: Spam / Flood cəhdi")
            await message.channel.send(f"🔒 **{message.author.mention}** şəbəkəni spam etdiyi üçün 5 dəqiqəlik təcrid (timeout) edildi.")
        except:
            pass
        return

    await bot.process_commands(message)

# ==========================================
# İDARƏETMƏ VƏ YARDIM PANELİ
# ==========================================
@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="🛡️ YENİLMEZ OS // ULTIMATE PANEL",
        description="Serverin idarə olunması üçün bütün aktiv əmr qrupları:",
        color=0x0f0f0f
    )
    embed.add_field(
        name="⚔️ Moderasiya & Təhlükəsizlik Əmrləri",
        value="`r?sil [say]` — Mesajları təmizləyər\n`r?ban [@istifadəçi]` — Serverdən uzaqlaşdırar\n`r?at [@istifadəçi]` — Serverdən qovar (Kick)\n`r?mute [@istifadəçi] [dəqiqə]` — Timeout verər\n`r?lock` / `r?unlock` — Kanalı kilidləyər / açar\n`r?nuke` — Kanalı sıfırlayıb yenidən qurar", 
        inline=False
    )
    embed.add_field(
        name="🏴‍☠️ Oyunlar & Simulyasiyalar",
        value="`r?hack [@istifadəçi]` — Hədəf sistemə sızma\n`r?cuzdan` — Oğurlanan balans\n`r?yazitura [yazı/tura]` — Sikkə oyunu\n`r?slot` — Slot maşını\n`r?rusruleti` — Risqli oyun", 
        inline=False
    )
    embed.add_field(
        name="🎧 Səs Şəbəkəsi Əmrləri",
        value="`r?qosul` — Səs kanalına qoşular\n`r?ayril` — Səs kanalından çıxar", 
        inline=False
    )
    embed.add_field(
        name="🛠️ Sistem & Alətlər",
        value="`r?afk [səbəb]` • `r?avatar` • `r?profil` • `r?server` • `r?ping`", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS v22 • Full Heavy Edition")
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="⚡ Sistem Gecikməsi", description=f"Terminal cavab sürəti: `{latency}ms`", color=0x111111)
    await ctx.send(embed=embed)

# ==========================================
# MODERASİYA ƏMRLƏRİ (GENİŞLƏNDİRİLMİŞ)
# ==========================================
@bot.command(name="sil")
async def sil(ctx, amount: int = 10):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ Xəta: Bu əmr üçün `Mesajları İdarə Et` səlahiyyətin lazımdır.")
        return
    if amount > 100: amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ Sistem: `{amount}` ədəd mesaj uğurla təmizləndi.")
    await msg.delete(delay=3)

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ Xəta: Bu əmr üçün `Üzvləri Banla` səlahiyyətin lazımdır.")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Təhlükəsizlik: **{member.mention}** serverdən ban edildi! Səbəb: `{reason}`")
    except Exception as e:
        await ctx.send(f"❌ Xəta baş verdi: `{e}`")

@bot.command(name="at")
async def at(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ Xəta: Bu əmr üçün `Üzvləri Qov` səlahiyyətin lazımdır.")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 Təhlükəsizlik: **{member.mention}** serverdən qovuldu (Kick). Səbəb: `{reason}`")
    except Exception as e:
        await ctx.send(f"❌ Xəta baş verdi: `{e}`")

@bot.command(name="mute")
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Səbəb göstərilməyib"):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ Xəta: Bu əmr üçün `Üzvləri cəzalandır` səlahiyyətin lazımdır.")
        return
    try:
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🔇 Təhlükəsizlik: **{member.mention}** {minutes} dəqiqə müddətinə susduruldu. Səbəb: `{reason}`")
    except Exception as e:
        await ctx.send(f"❌ Xəta baş verdi: `{e}`")

@bot.command(name="lock")
async def lock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Xəta: Səlahiyyətin çatmır.")
        return
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Terminal: Bu kanal mesaj yazılması üçün kilidləndi!")
    except Exception as e:
        await ctx.send(f"❌ Xəta: `{e}`")

@bot.command(name="unlock")
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Xəta: Səlahiyyətin çatmır.")
        return
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Terminal: Kanalın kilidi açıldı, yenidən yazı yaza bilərlər.")
    except Exception as e:
        await ctx.send(f"❌ Xəta: `{e}`")

@bot.command(name="nuke")
async def nuke(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Xəta: Səlahiyyətin çatmır.")
        return
    try:
        position = ctx.channel.position
        new_channel = await ctx.channel.clone(reason="Kanal sıfırlandı (Nuke)")
        await ctx.channel.delete()
        await new_channel.edit(position=position)
        await new_channel.send("💥 Sistem: Kanal tamamilə təmizləndi və yenidən quruldu!")
    except Exception as e:
        await ctx.send(f"❌ Xəta: `{e}`")

# ==========================================
# OYUN VƏ HACK SİMULYASİYA ƏMRLƏRİ
# ==========================================
@bot.command(name="hack")
async def hack(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("❌ Doğru istifadə: `r?hack @istifadəçi`")
        return
    if member.id == ctx.author.id:
        await ctx.send("❌ Öz sistemini hackləyə bilməzsən!")
        return

    asamalar = [
        f"💻 Hədəf `{member.name}` sisteminə portlar üzərindən sızılır...",
        f"🔓 Təhlükəsizlik divarları (Firewall) bypass edilir...",
        f"📂 Şəxsi verilənlər və log faylları ələ keçirilir...",
        f"✅ Əməliyyat uğurla başa çatdı! Hədəf tamamilə ələ keçirildi!"
    ]
    
    msg = await ctx.send(asamalar[0])
    await asyncio.sleep(2)
    for i in range(1, len(asamalar)):
        await msg.edit(content=asamalar[i])
        await asyncio.sleep(2)
    
    para = random.randint(200, 800)
    if ctx.author.id not in user_wallet:
        user_wallet[ctx.author.id] = 100
    user_wallet[ctx.author.id] += para

    embed = discord.Embed(title="🏴‍☠️ HACK REPORT", description=f"**{ctx.author.mention}**, `{member.name}` hədəfini hacklədin və balansına **`{para} YNC`** əlavə olundu!", color=0x050505)
    await ctx.send(embed=embed)

@bot.command(name="cuzdan")
async def cuzdan(ctx):
    uid = ctx.author.id
    balans = user_wallet.get(uid, 100)
    embed = discord.Embed(title="🪙 Kiber Cüzdan", description=f"**{ctx.author.mention}**, ümumi balansın: **`{balans} YNC`**", color=0xffd700)
    await ctx.send(embed=embed)

@bot.command(name="yazitura")
async def yazitura(ctx, secim: str = None):
    if not secim or secim.lower() not in ["yazı", "tura", "yazi"]:
        await ctx.send("❌ Doğru istifadə: `r?yazitura yazı` və ya `r?yazitura tura`")
        return
    neticə = random.choice(["yazı", "tura"])
    secim = "yazı" if secim.lower() == "yazi" else secim.lower()
    
    if secim == neticə:
        await ctx.send(f"🪙 Sikkə atıldı: **{neticə.capitalize()}**! Təbriklər, qazandın! 🎉")
    else:
        await ctx.send(f"🪙 Sikkə atıldı: **{neticə.capitalize()}**! Təəssüf, uduzdun! 💀")

@bot.command(name="slot")
async def slot(ctx):
    sembollər = ["🍒", "🍋", "🍊", "🔔", "⭐", "💎"]
    s1, s2, s3 = random.choice(sembollər), random.choice(sembollər), random.choice(sembollər)
    slot_mesaj = f"🎰 | {s1} | {s2} | {s3} |"
    
    if s1 == s2 and s2 == s3:
        await ctx.send(f"{slot_mesaj}\n🎉 Jackpot! Üçü də eyni çıxdı, böyük mükafat sənin!")
    elif s1 == s2 or s2 == s3 or s1 == s3:
        await ctx.send(f"{slot_mesaj}\n✨ İkisi eyni çıxdı, qazanc əldə etdin.")
    else:
        await ctx.send(f"{slot_mesaj}\n💀 Bəxtini yenidən sına, bu dəfə alınmadı.")

@bot.command(name="rusruleti")
async def rusruleti(ctx):
    risk = random.choice([True, False, False, False])
    if risk:
        await ctx.send(f"💥 **{ctx.author.mention}**, patron partladı! Oyunu uduzdun.")
    else:
        await ctx.send(f"✨ **{ctx.author.mention}**, klik! Boş çıxdı, sağ qaldın.")

# ==========================================
# SƏS VƏ DİGƏR YARDIMÇI ƏMRLƏR
# ==========================================
@bot.command(name="qosul")
async def qosul(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ Xəta: Əvvəlcə hər hansı bir səs kanalında olmalısan!")
        return
    channel = ctx.author.voice.channel
    try:
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"🔊 Səs şəbəkəsinə qoşuldum: **{channel.name}**")
    except Exception as e:
        await ctx.send(f"❌ Xəta: `{e}`")

@bot.command(name="ayril")
async def ayril(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Səs şəbəkəsindən ayrıldım.")
    else:
        await ctx.send("❌ Xəta: Bot heç bir səs kanalında deyil.")

@bot.command(name="afk")
async def afk(ctx, *, reason="Səbəb yoxdur"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"💤 **{ctx.author.name}**, AFK rejiminə keçdin. Səbəb: `{reason}`")

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0x111111)
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="profil")
async def profil(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 İstifadəçi Analizi: {member.name}", color=0x111111)
    embed.add_field(name="Unikal ID", value=member.id, inline=True)
    embed.add_field(name="Serverə Giriş", value=member.joined_at.strftime("%d.%m.%Y"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="server")
async def server(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 Server Qovşağı: {guild.name}", color=0x111111)
    embed.add_field(name="Ümumi Üzv", value=guild.member_count, inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

# ==========================================
# TOKEN YOXLAMASI VƏ BOTUN BAŞLADILMASI
# ==========================================
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı! Zəhmət olmasa environment variable əlavə edin.")
                                                                           
