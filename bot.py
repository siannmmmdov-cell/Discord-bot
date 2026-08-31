import discord
from discord.ext import commands
import asyncio
import os
import random
import time
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="r?", intents=intents)

# 👑 BURAYA ÖZ DISCORD ID-Nİ YAZ 👑
SAHIB_ID = 100412345678901234  # Öz ID-ni bura qoyarsan

# Yaddaş Sistemləri (Dictionary)
ticket_span_kontrol = {}
user_xp = {}
spam_takip = {}

@bot.event
async def on_ready():
    print(f"🔥 Bot uğurla işə düşdü: {bot.user.name} 🔥")
    await bot.change_presence(activity=discord.Game(name="r?yardim | DEADAZE v5000 👑"))

# ==============================================================================
# 🛡️ ULTRA TƏHLÜKƏSİZLİK, ANTI-SPAM, CAPS-LOCK VƏ XP SISTEMI 🛡️
# ==============================================================================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_id = message.author.id
    sindi = time.time()

    # 1. LEVEL & XP SISTEMI
    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}
    
    user_xp[author_id]["xp"] += 10
    gerekli_xp = user_xp[author_id]["level"] * 100

    if user_xp[author_id]["xp"] >= gerekli_xp:
        user_xp[author_id]["level"] += 1
        user_xp[author_id]["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Yeni səviyyəyə yüksəldin: **Səviyyə {user_xp[author_id]['level']}** 🚀")
        except:
            pass

    # Sahib üçün qoruma istisnası
    if author_id != SAHIB_ID:
        # 2. LINK VƏ REKLAM QORUMASI
        if "http://" in message.content or "https://" in message.content or "discord.gg/" in message.content:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, Bu serverdə reklam/link paylaşmaq qadağandır!", delete_after=3)
                return
            except:
                pass

        # 3. RANDOM SPAM / ÇOX UZUN MESAJ QORUMASI
        if len(message.content) > 300:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, Uzun simvol spamı etmək qadağandır!", delete_after=3)
                return
            except:
                pass

        # 4. SPAM & FLOOD QORUMASI (5 saniyədə 5-dən çox mesaj)
        if author_id not in spam_takip:
            spam_takip[author_id] = []
        
        spam_takip[author_id] = [t for t in spam_takip[author_id] if sindi - t < 5]
        spam_takip[author_id].append(sindi)

        if len(spam_takip[author_id]) >= 5:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, Çox sürətli mesaj yazırsan (Spam Qoruması)!", delete_after=3)
                return
            except:
                pass

        # 5. CAPSLOCK QORUMASI (Cümlənin 70%-dən çoxu böyük hərfdirsə)
        if len(message.content) > 7:
            buyuk_harf_sayisi = sum(1 for c in message.content if c.isupper())
            if (buyuk_harf_sayisi / len(message.content)) > 0.7:
                try:
                    await message.delete()
                    await message.channel.send(f"⚠️ {message.author.mention}, Daimi böyük hərflərlə (CapsLock) yazmaq qadağandır!", delete_after=3)
                    return
                except:
                    pass

    await bot.process_commands(message)

# ==============================================================================
# ✨ REACTION (EMOJI) REACTION MİRROR SİSTEMİ ✨
# ==============================================================================

@bot.event
async def on_raw_reaction_add(payload):
    # Bot özü reaksiyaya qatıldıqda dövrəyə girməsin
    if payload.user_id == bot.user.id:
        return
    
    # Kanalı və mesajı tapırıq
    try:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        
        # İstifadəçi hər hansı mesaja emoji basanda bot da həmin emoji ilə eyni mesaja reaksiya atır
        await message.add_reaction(payload.emoji)
    except Exception as e:
        print(f"Reaction xətası: {e}")

# ==============================================================================
# 👑 YARDIM VƏ MƏLUMAT ƏMRLƏRİ
# ==============================================================================

@bot.command(name="yardim", help="👑 Bütün komutların siyahısını və izahını göstərir.")
async def yardim(ctx):
    embed = discord.Embed(
        title="👑 MASTER PANEL v5000 (70+ Komut)",
        description="Bütün gücləndirilmiş əmrlər və ultra qoruma sistemləri:",
        color=0xffa200
    )
    embed.add_field(name="👑 Sahib & İdarəetmə", value="`r?elan`, `r?anket`, `r?cekilis`, `r?duyuru`, `r?bakim`", inline=False)
    embed.add_field(name="🛡️ Təhlükəsizlik & Gizlilik", value="`r?gizle`, `r?goster`, `r?sesgizle`, `r?sesgoster`, `r?tumunugizle`, `r?tumunugoster`", inline=False)
    embed.add_field(name="📋 Məlumat & Statistika", value="`r?server`, `r?userinfo`, `r?botinfo`, `r?ping`, `r?online`, `r?hava`, `r?hesabla`, `r?rolbilgi`, `r?kanalbilgi`, `r?level`", inline=False)
    embed.add_field(name="🛠️ Moderasiya & İdarə", value="`r?sil`, `r?temizle`, `r?silkanal`, `r?kanalac`, `r?mute`, `r?unmute`, `r?ban`, `r?unban`, `r?kick`, `r?lock`, `r?unlock`, `r?slowmode`, `r?temizlemesaj`, `r?nuke`, `r?reklamver`", inline=False)
    embed.add_field(name="⚙️ Rol & Üzv İdarəsi", value="`r?rolver`, `r?rolsil`, `r?rolac`, `r?rolsil_komanda`, `r?nick`, `r?avatar`, `r?yetkililer`, `r?botsay`, `r?uyeara`, `r?sesdesan`", inline=False)
    embed.add_field(name="🎮 Oyunlar & Əyləncə", value="`r?duel`, `r?coinflip`, `r?slot`, `r?hacker`, `r?zar`, `r?sevgili`, `r?ascii`, `r?iq`, `r?rip`, `r?soz`, `r?8ball`, `r?istilik`, `r?afk`, `r?tapsir`, `r?balıq`, `r?sifre`, `r?sans`, `r?yazi`, `r?fal`", inline=False)
    embed.set_footer(text="DEADAZE Security Systems | v5000 Pro Max")
    await ctx.send(embed=embed)

@bot.command(name="botinfo", help="🤖 Botun versiyası və sistem məlumatlarını göstərir.")
async def botinfo(ctx):
    await ctx.send("🤖 **Bot Sürümü:** `v5000 Ultra Pro Max` | Python & Discord.py ⚡")

@bot.command(name="server", help="🏰 Server haqqında ümumi statistik məlumat verir.")
async def server(ctx):
    g = ctx.guild
    await ctx.send(f"🏰 **Server:** {g.name} | **Üzv:** {g.member_count} | **Yaradılma:** {g.created_at.strftime('%d.%m.%Y')}")

@bot.command(name="userinfo", help="👤 İstfadəçinin qeydiyyat və profil məlumatlarını göstərir.")
async def userinfo(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(f"👤 **İstifadəçi:** {u.name} | **ID:** {u.id} | **Qoşuldu:** {u.joined_at.strftime('%d.%m.%Y')}")

@bot.command(name="ping", help="🏓 Botun internet gecikmə sürətini (ms) ölçür.")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Botun gecikməsi: **{round(bot.latency * 1000)}ms** ⚡")

@bot.command(name="online", help="🟢 Serverdə onlayn olan üzvlərin sayını göstərir.")
async def online(ctx):
    c = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 **Aktiv (Onlayn) Üzv sayı:** {c}")

@bot.command(name="hava", help="🌤️ Seçilən şəhərin təxmini hava şəraitini göstərir.")
async def hava(ctx, *, seher: str = "Bakı"):
    await ctx.send(f"🌤️ **{seher}** üçün hava istiliyi: **{random.randint(18, 35)}°C** (Günəşli ☀️)")

@bot.command(name="hesabla", help="➗ Riyazi əməliyyatları hesablayır.")
async def hesabla(ctx, *, islem: str):
    try:
        netice = eval(islem)
        await ctx.send(f"🧮 **Nəticə:** `{netice}` ✅")
    except:
        await ctx.send("❌ Xəta! Doğru riyazi əməliyyat daxil et ⚠️")

@bot.command(name="level", help="⭐ Sənin və ya başqasının səviyyə və XP durumunu göstərir.")
async def level(ctx, m: discord.Member = None):
    target = m or ctx.author
    if target.id in user_xp:
        lvl = user_xp[target.id]["level"]
        xp = user_xp[target.id]["xp"]
        await ctx.send(f"⭐ **{target.name}** | Səviyyə: **{lvl}** 🏆 | XP: **{xp}** ⚡")
    else:
        await ctx.send(f"⭐ **{target.name}** hələ heç XP qazanmayıb! (Səviyyə 1) 🚀")

# ==============================================================================
# 👑 SAHİB & İDARƏƏTMƏ KOMUTLARI
# ==============================================================================

@bot.command(name="elan", help="📢 Serverdə xüsusi embed mesajı atır.")
async def elan(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 ELAN", description=metin, color=0xffaa00)
    await ctx.send(embed=embed)

@bot.command(name="anket", help="📊 Üzvlərin səs verməsi üçün anket yaradır.")
async def anket(ctx, *, soru: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 ANKET", description=soru, color=0x00ffcc)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis", help="🎉 Serverdə hədiyyə çəkilişi başladır.")
async def cekilis(ctx, *, odul: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="🎉 ÇƏKİLİŞ", description=f"Ödül: **{odul}**\nQatılmaq üçün 🎉 emojisinə bas!", color=0xff0055)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")

@bot.command(name="duyuru", help="🔔 Xüsusi məlumatlandırma duyurusu gönderir.")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"🔔 **DUYURU:** {metin}")

@bot.command(name="bakim", help="🛠️ Serverin baxın rejimini aktivləşdirir.")
async def bakim(ctx, durum: str = "açıq"):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send(f"🛠️ Baxım rejimi: **{durum}** olaraq dəyişdirildi! ⚠️")

# ==============================================================================
# 🛡️ TƏHLÜKƏSİZLİK & GİZLİLİK KOMUTLARI
# ==============================================================================

@bot.command(name="gizle", help="🔒 Aktiv kanalı adi üzvlər üçün gizlədir.")
async def gizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🔒 Kanal uğurla gizlədildi! 👁️‍🗨️")

@bot.command(name="goster", help="🔓 Gizlədilmiş kanalı yenidən hamıya açır.")
async def goster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🔓 Kanal hamı üçün göstərildi! ✅")

@bot.command(name="sesgizle", help="🚫 Səs kanalına qoşulmanı bağlayır.")
async def sesgizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=False)
    await ctx.send("🔴 Səs kanalı girişə bağlandı! 🚫")

@bot.command(name="sesgoster", help="🟢 Səs kanalına qoşulmanı açır.")
async def sesgoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=True)
    await ctx.send("🟢 Səs kanalı girişə açıldı! 🟢")

@bot.command(name="tumunugizle", help="🛡️ Serverdəki bütün kanalları gizlədir.")
async def tumunugizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    for c in ctx.guild.channels:
        try: await c.set_permissions(ctx.guild.default_role, view_channel=False)
        except: pass
    await ctx.send("🛡️ Bütün server kanalları gizlətildi! 🔒")

@bot.command(name="tumunugoster", help="🔓 Serverdəki bütün kanalları açır.")
async def tumunugoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    for c in ctx.guild.channels:
        try: await c.set_permissions(ctx.guild.default_role, view_channel=True)
        except: pass
    await ctx.send("🔓 Bütün server kanalları açıldı! 💎")

# ==============================================================================
# 🛠️ MODERASİYA & İDARƏ KOMUTLARI
# ==============================================================================

@bot.command(name="sil", help="🧹 Yazılan miqdarda mesajı dərhal silir.")
async def sil(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 {amount} ədəd mesaj silindi! ✨", delete_after=3)

@bot.command(name="temizle", help="🧹 Kanalı tamamilə təmizləyir (100 mesaj).")
async def temizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.purge(limit=100)

@bot.command(name="silkanal", help="🗑️ Aktiv kanalı tamamilə silir.")
async def silkanal(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.delete()

@bot.command(name="kanalac", help="✨ Yeni mətn kanalı yaradır.")
async def kanalac(ctx, *, isim: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"✨ #{isim} kanalı uğurla yaradıldı! 🎉")

@bot.command(name="mute", help="🔇 İstifadəçinin yazmaq və konuşmaq hüququnu məhdudlaşdırır.")
async def mute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for c in ctx.guild.channels:
            await c.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.mention} səssizləşdirildi (Cəzalandırıldı)! 🔴")

@bot.command(name="unmute", help="🔊 İstifadəçinin cəzasını ləğv edir.")
async def unmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role: await member.remove_roles(role)
    await ctx.send(f"🔊 {member.mention} cəzası qaldırıldı, səsi açıldı! 🟢")

@bot.command(name="ban", help="🔨 İstifadəçini serverdən qovur və tamamilə banlayır.")
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} serverdən banlandı! 🔴")

@bot.command(name="unban", help="🔓 Banlanmış istifadəçinin qadağasını qaldırır.")
async def unban(ctx, *, member_name: str):
    if ctx.author.id != SAHIB_ID: return
    banned = await ctx.guild.bans()
    for entry in banned:
        if entry.user.name == member_name:
            await ctx.guild.unban(entry.user)
            await ctx.send(f"🔓 {entry.user.name} üçün ban qaldırıldı! 🔓")
            return
    await ctx.send("❌ İstifadəçi ban siyahısında tapılmadı! ⚠️")

@bot.command(name="kick", help="👢 İstifadəçini serverdən atır (Kick).")
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} serverdən qovuldu! ⚡")

@bot.command(name="lock", help="🔒 Kanalı mesaj yazmağa bağlayır.")
async def lock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal mesajlara bağlandı! 🔴")

@bot.command(name="unlock", help="🔓 Kanalı mesaj yazmağa açır.")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal mesajlara açıldı! ✅")

@bot.command(name="slowmode", help="🐢 Kanalda yavaş rejim (slowmode) tənzimləyir.")
async def slowmode(ctx, saniye: int = 0):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"🐢 Yavaş rejim (Slowmode): **{saniye} saniyə** olaraq tənzimləndi. 🐢")

@bot.command(name="temizlemesaj", help="🧹 Müəyyən üzvün son mesajlarını təmizləyir.")
async def temizlemesaj(ctx, uye: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=50, check=lambda m: m.author == uye)
    await ctx.send(f"🧹 {uye.name} adlı şəxsin {len(deleted)} mesajı təmizləndi! ✨", delete_after=3)

@bot.command(name="nuke", help="💥 Kanalı kökündən silib yenidən eynisi ilə əvəz edir.")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID: return
    pos = ctx.channel.position
    yeni = await ctx.channel.clone(reason="Nuke olundu")
    await ctx.channel.delete()
    await yeni.edit(position=pos)
    await yeni.send("💥 Kanal sıfırlandı və yenidən quruldu! 🔥🚀")

# ==============================================================================
# 🎮 OYUNlar & ƏYLƏNCƏ KOMUTLARI
# ==============================================================================

@bot.command(name="duel", help="⚔️ Başqa bir oyunçu ilə duel et.")
async def duel(ctx, member: discord.Member):
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ **{ctx.author.name}** vs **{member.name}** dueli başladı! 🏆 Qalib: {kazanan.mention}!")

@bot.command(name="coinflip", help="🪙 Yazı-tura atır.")
async def coinflip(ctx):
    res = random.choice(["Yazı 🪙", "Tura 👑"])
    await ctx.send(f"🎲 Nəticə: **{res}**")

@bot.command(name="slot", help="🎰 Slot maşını oyunu.")
async def slot(ctx):
    emojis = ["🍎", "🍋", "🍒", "7️⃣", "💎"]
    a, b, c = random.choice(emojis), random.choice(emojis), random.choice(emojis)
    msg = f"🎰 [{a} | {b} | {c}]\n"
    msg += "🎉 UDDUNUZ! 💎" if a == b == c else "❌ Uduzdunuz, yenidən cəhd edin!"
    await ctx.send(msg)

@bot.command(name="hacker", help="💻 Əyləncəli haker simulyasiyası.")
async def hacker(ctx, member: discord.Member):
    msg = await ctx.send(f"💻 {member.name} hakerlik hücumu başladılır...")
    await asyncio.sleep(1)
    await msg.edit(content=f"🔍 IP Adresi tapılır... 192.168.1.{random.randint(10, 99)}")
    await asyncio.sleep(1)
    await msg.edit(content=f"🔑 Parollar sındırılır...")
    await asyncio.sleep(1)
    await msg.edit(content=f"✅ {member.name} tamamilə hakerləndi! 😈")

@bot.command(name="zar", help="🎲 Zar atır.")
async def zar(ctx):
    await ctx.send(f"🎲 Zərdə çıxan xal: **{random.randint(1, 6)}**")

@bot.command(name="sevgili", help="❤️ Sevgi uyğunluğunu ölçür.")
async def sevgili(ctx, m: discord.Member):
    await ctx.send(f"❤️ {ctx.author.mention} və {m.mention} sevgi faizi: **%{random.randint(1, 100)}** 💕")

@bot.command(name="iq", help="🧠 Zəka səviyyəsini yoxlayır.")
async def iq(ctx, m: discord.Member = None):
    target = m or ctx.author
    await ctx.send(f"🧠 **{target.name}** IQ Səviyyəsi: **{random.randint(50, 160)}**")

@bot.command(name="balıq", help="🎣 Virtual balıq tutma oyunu.")
async def balıq(ctx):
    fishes = ["🐟 Balıq", "🐠 Qızıl Balıq", "🦈 Akula", "👞 Köhnə Başmaq"]
    await ctx.send(f"🎣 Tutduğun əşya: **{random.choice(fishes)}**")

@bot.command(name="sifre", help="🔑 Təhlükəsiz şifrə yaradır.")
async def sifre(ctx, uzunluq: int = 10):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$"
    res = "".join(random.choice(chars) for _ in range(uzunluq))
    await ctx.send(f"🔑 Sənin üçün yaradılan şifrə: `{res}`")

# ==============================================================================
# 🎫 TICKET SISTEMI & PANELI (Emoji ilə düymələr)
# ==============================================================================

class TicketKapatView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket-i Bağla", emoji="🔒", style=discord.ButtonStyle.red, custom_id="ticket_kapat_buton")
    async def ticket_kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Dəstək kanalı 3 saniyəyə silinir... ⌛", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()

class TicketButton(discord.ui.View):
   
