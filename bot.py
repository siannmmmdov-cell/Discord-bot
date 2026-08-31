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

# 👑 SƏNİN DİSCORD İD-N 👑
SAHIB_ID = 1391781251390451713

# Yaddaş Sistemləri
ticket_span_kontrol = {}
user_xp = {}

@bot.event
async def on_ready():
    print(f"🔥 Bot uğurla işə düşdü: {bot.user.name} 🔥")
    await bot.change_presence(activity=discord.Game(name="r?yardim | DEADAZE v5000 👑"))

# ==============================================================================
# 🛡️ XP VƏ MESAJ SİSTEMİ (Spam qoruması tamamilə silindi, heç kimə mute düşmür)
# ==============================================================================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_id = message.author.id

    # Level & XP Sistemi
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

    await bot.process_commands(message)

# ==============================================================================
# ✨ EMOJI MIRROR SİSTEMİ (Kim emoji bassa, bot da basacaq)
# ==============================================================================

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    
    try:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.add_reaction(payload.emoji)
    except Exception as e:
        print(f"Reaction xətası: {e}")

# ==============================================================================
# 👑 YARDIM VƏ BÜTÜN MƏLUMAT KOMANDALARI
# ==============================================================================

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="👑 MASTER PANEL v5000 (Bütün Komutlar)",
        description="Bütün gücləndirilmiş əmrlər və idarəetmə sistemləri:",
        color=0xffa200
    )
    embed.add_field(name="👑 Sahib & İdarəetmə", value="`r?elan`, `r?anket`, `r?cekilis`, `r?duyuru`, `r?bakim`, `r?ticketpanel`", inline=False)
    embed.add_field(name="🛡️ Kanal İdarəsi", value="`r?gizle`, `r?goster`, `r?sesgizle`, `r?sesgoster`, `r?tumunugizle`, `r?tumunugoster`", inline=False)
    embed.add_field(name="📋 Məlumat & Statistika", value="`r?server`, `r?userinfo`, `r?botinfo`, `r?ping`, `r?online`, `r?hava`, `r?hesabla`, `r?level`", inline=False)
    embed.add_field(name="🛠️ Moderasiya & Rol", value="`r?sil`, `r?temizle`, `r?silkanal`, `r?kanalac`, `r?mute`, `r?unmute`, `r?ban`, `r?unban`, `r?kick`, `r?lock`, `r?unlock`, `r?rolver`, `r?rolsil`, `r?nuke`", inline=False)
    embed.add_field(name="🎮 Oyunlar & Əyləncə", value="`r?duel`, `r?coinflip`, `r?slot`, `r?hacker`, `r?zar`, `r?sevgili`, `r?iq`, `r?balıq`, `r?sifre`", inline=False)
    embed.set_footer(text="DEADAZE Security Systems | v5000 Pro Max")
    await ctx.send(embed=embed)

@bot.command(name="botinfo")
async def botinfo(ctx):
    await ctx.send("🤖 **Bot Sürümü:** `v5000 Ultra Pro Max` | Python & Discord.py ⚡")

@bot.command(name="server")
async def server(ctx):
    g = ctx.guild
    await ctx.send(f"🏰 **Server:** {g.name} | **Üzv:** {g.member_count} | **Yaradılma:** {g.created_at.strftime('%d.%m.%Y')}")

@bot.command(name="userinfo")
async def userinfo(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(f"👤 **İstifadəçi:** {u.name} | **ID:** {u.id} | **Qoşuldu:** {u.joined_at.strftime('%d.%m.%Y')}")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Gecikmə: **{round(bot.latency * 1000)}ms** ⚡")

@bot.command(name="online")
async def online(ctx):
    c = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 **Aktiv (Onlayn) Üzv sayı:** {c}")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Bakı"):
    await ctx.send(f"🌤️ **{seher}** üçün hava istiliyi: **{random.randint(18, 35)}°C** (Günəşli ☀️)")

@bot.command(name="hesabla")
async def hesabla(ctx, *, islem: str):
    try:
        netice = eval(islem)
        await ctx.send(f"🧮 **Nəticə:** `{netice}` ✅")
    except:
        await ctx.send("❌ Xəta! Doğru riyazi əməliyyat daxil et ⚠️")

@bot.command(name="level")
async def level(ctx, m: discord.Member = None):
    target = m or ctx.author
    if target.id in user_xp:
        lvl = user_xp[target.id]["level"]
        xp = user_xp[target.id]["xp"]
        await ctx.send(f"⭐ **{target.name}** | Səviyyə: **{lvl}** 🏆 | XP: **{xp}** ⚡")
    else:
        await ctx.send(f"⭐ **{target.name}** hələ XP qazanmayıb! (Səviyyə 1) 🚀")

# ==============================================================================
# 👑 SAHİB & İDARƏƏTMƏ KOMUTLARI
# ==============================================================================

@bot.command(name="elan")
async def elan(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 ELAN", description=metin, color=0xffaa00)
    await ctx.send(embed=embed)

@bot.command(name="anket")
async def anket(ctx, *, soru: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 ANKET", description=soru, color=0x00ffcc)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, *, odul: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="🎉 ÇƏKİLİŞ", description=f"Ödül: **{odul}**\nQatılmaq üçün 🎉 emojisinə bas!", color=0xff0055)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")

@bot.command(name="duyuru")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"🔔 **DUYURU:** {metin}")

@bot.command(name="bakim")
async def bakim(ctx, durum: str = "açıq"):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send(f"🛠️ Baxım rejimi: **{durum}** olaraq dəyişdirildi! ⚠️")

# ==============================================================================
# 🛡️ KANAL GİZLƏMƏ KOMUTLARI
# ==============================================================================

@bot.command(name="gizle")
async def gizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🔒 Kanal uğurla gizlədildi! 👁️‍🗨️")

@bot.command(name="goster")
async def goster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🔓 Kanal hamı üçün göstərildi! ✅")

@bot.command(name="sesgizle")
async def sesgizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=False)
    await ctx.send("🔴 Səs kanalı girişə bağlandı! 🚫")

@bot.command(name="sesgoster")
async def sesgoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=True)
    await ctx.send("🟢 Səs kanalı girişə açıldı! 🟢")

@bot.command(name="tumunugizle")
async def tumunugizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    for c in ctx.guild.channels:
        try: await c.set_permissions(ctx.guild.default_role, view_channel=False)
        except: pass
    await ctx.send("🛡️ Bütün server kanalları gizlətildi! 🔒")

@bot.command(name="tumunugoster")
async def tumunugoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    for c in ctx.guild.channels:
        try: await c.set_permissions(ctx.guild.default_role, view_channel=True)
        except: pass
    await ctx.send("🔓 Bütün server kanalları açıldı! 💎")

# ==============================================================================
# 🛠️ MODERASİYA, ROL VƏ İDARƏ KOMUTLARI
# ==============================================================================

@bot.command(name="sil")
async def sil(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 {amount} ədəd mesaj silindi! ✨", delete_after=3)

@bot.command(name="temizle")
async def temizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.purge(limit=100)

@bot.command(name="silkanal")
async def silkanal(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.delete()

@bot.command(name="kanalac")
async def kanalac(ctx, *, isim: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"✨ #{isim} kanalı uğurla yaradıldı! 🎉")

@bot.command(name="rolver")
async def rolver(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} adlı istifadəçiyə **{role.name}** rolu verildi! 👑")

@bot.command(name="rolsil")
async def rolsil(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} adlı istifadəçidən **{role.name}** rolu alındı! ⚠️")

@bot.command(name="mute")
async def mute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for c in ctx.guild.channels:
            await c.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.mention} səssizləşdirildi! 🔴")

@bot.command(name="unmute")
async def unmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role: await member.remove_roles(role)
    await ctx.send(f"🔊 {member.mention} səsi açıldı! 🟢")

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} banlandı! 🔴")

@bot.command(name="unban")
async def unban(ctx, *, member_name: str):
    if ctx.author.id != SAHIB_ID: return
    banned = await ctx.guild.bans()
    for entry in banned:
        if entry.user.name == member_name:
            await ctx.guild.unban(entry.user)
            await ctx.send(f"🔓 {entry.user.name} üçün ban qaldırıldı!")
            return
    await ctx.send("❌ İstifadəçi tapılmadı! ⚠️")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} qovuldu! ⚡")

@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal mesajlara bağlandı! 🔴")

@bot.command(name="unlock")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal mesajlara açıldı! ✅")

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID: return
    pos = ctx.channel.position
    yeni = await ctx.channel.clone(reason="Nuke olundu")
    await ctx.channel.delete()
    await yeni.edit(position=pos)
    await yeni.send("💥 Kanal sıfırlandı və yenidən quruldu! 🔥🚀")

# ==============================================================================
# 🎮 OYUNLAR & ƏYLƏNCƏ KOMUTLARI
# ==============================================================================

@bot.command(name="duel")
async def duel(ctx, member: discord.Member):
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ **{ctx.author.name}** vs **{member.name}** dueli başladı! 🏆 Qalib: {kazanan.mention}!")

@bot.command(name="coinflip")
async def coinflip(ctx):
    res = random.choice(["Yazı 🪙", "Tura 👑"])
    await ctx.send(f"🎲 Nəticə: **{res}**")

@bot.command(name="slot")
async def slot(ctx):
    emojis = ["🍎", "🍋", "🍒", "7️⃣", "💎"]
    a, b, c = random.choice(emojis), random.choice(emojis), random.choice(emojis)
    msg = f"🎰 [{a} | {b} | {c}]\n"
    msg += "🎉 UDDUNUZ! 💎" if a == b == c else "❌ Uduzdunuz, yenidən cəhd edin!"
    await ctx.send(msg)

@bot.command(name="hacker")
async def hacker(ctx, member: discord.Member):
    msg = await ctx.send(f"💻 {member.name} hakerlik hücumu başladılır...")
    await asyncio.sleep(1)
    await msg.edit(content=f"🔍 IP Adresi tapılır... 192.168.1.{random.randint(10, 99)}")
    await asyncio.sleep(1)
    await msg.edit(content=f"🔑 Parollar sındırılır...")
    await asyncio.sleep(1)
    await msg.edit(content=f"✅ {member.name} tamamilə hakerləndi! 😈")

@bot.command(name="zar")
async def zar(ctx):
    await ctx.send(f"🎲 Zərdə çıxan xal: **{random.randint(1, 6)}**")

@bot.command(name="sevgili")
async def sevgili(ctx, m: discord.Member):
    await ctx.send(f"❤️ {ctx.author.mention} və {m.mention} sevgi faizi: **%{random.randint(1, 100)}** 💕")

@bot.command(name="iq")
async def iq(ctx, m: discord.Member = None):
    target = m or ctx.author
    await ctx.send(f"🧠 **{target.name}** IQ Səviyyəsi: **{random.randint(50, 160)}**")

@bot.command(name="balıq")
async def balıq(ctx):
    fishes = ["🐟 Balıq", "🐠 Qızıl Balıq", "🦈 Akula", "👞 Köhnə Başmaq"]
    await ctx.send(f"🎣 Tutduğun əşya: **{random.choice(fishes)}**")

@bot.command(name="sifre")
async def sifre(ctx, uzunluk: int = 10):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$"
    res = "".join(random.choice(chars) for _ in range(uzunluk))
    await ctx.send(f"🔑 Sənin üçün yaradılan şifrə: `{res}`")

# ==============================================================================
# 🎫 TICKET SİSTEMİ (Düyməli və Emojili)
# ==============================================================================

class TicketKapatView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket-i Bağla", emoji="🔒", style=discord.ButtonStyle.red, custom_id="ticket_kapat_buton")
    async def ticket_kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Dəstək kanalı 3 saniyəyə silinir...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket Aç", emoji="📩", style=discord.ButtonStyle.green, custom_id="ticket_ac_buton")
    async def ticket_ac(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        author = interaction.user
        sindi = time.time()

        if author.id != SAHIB_ID:
            if author.id not in ticket_span_kontrol:
                ticket_span_kontrol[author.id] = []
            ticket_span_kontrol[author.id] = [t for t in ticket_span_kontrol[author.id] if sindi - t < 30]
            ticket_span_kontrol[author.id].append(sindi)
            if len(ticket_span_kontrol[author.id]) >= 3:
                await interaction.response.send_message("⚠️ Çox sürətli ticket açmağa çalışırsan!", ephemeral=True)
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
        }

        channel = await guild.create_text_channel(f"ticket-{author.name.lower()}", overwrites=overwrites)
        await channel.send(embed=discord.Embed(title="📩 Dəstək Mərkəzi", description="Səlahiyyətli şəxslər cavab verəcək.", color=0x00ff00), view=TicketKapatView())
        await interaction.response.send_message(f"✅ Ticket kanalınız yaradıldı: {channel.mention}", ephemeral=True)

@bot.command(name="ticketpanel")
async def ticketpanel(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📩 Dəstək Paneli", description="Kömək üçün aşağıdakı düyməyə basın!", color=0x00aaff)
    await ctx.send(embed=embed, view=TicketButton())

# ==============================================================================
# 🚀 BOTU BAŞLAT
# ==============================================================================

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if not token:
        print("❌ XƏTA: Token tapılmadı!")
    else:
        bot.run(token)
    
