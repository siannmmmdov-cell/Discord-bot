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

# 👑 BURAYA ÖZ DİSCORD İD-Nİ YAZ (Yalnız sən idarə edə bilərsən) 👑
SAHIB_ID = 123456789012345678  

# 📊 Təhlükəsizlik, Spam və Level sisteminin yaddaşı (Dictionary) 📊
ticket_spam_kontrol = {}
user_xp = {}
spam_takip = {}

@bot.event
async def on_ready():
    print(f"🤖 Bot uğurla işə düşdü: {bot.user.name} 🔥")
    await bot.change_presence(activity=discord.Game(name="r?yardim | DEADAZE 👑"))

# =====================================================================
# 🛡️ GÜCLƏNDİRİLMİŞ TƏHLÜKƏSİZLİK & XP SİSTEMİ (Anti-Spam, Caps, Level) 🛡️
# =====================================================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_id = message.author.id
    simdi = time.time()

    # ⭐ 1. LEVEL & XP SİSTEMİ: Hər mesaj atanda istifadəçi avtomatik XP qazanır və səviyyə atlayır! ⭐
    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}
    
    user_xp[author_id]["xp"] += 10
    gerekli_xp = user_xp[author_id]["level"] * 100
    
    if user_xp[author_id]["xp"] >= gerekli_xp:
        user_xp[author_id]["level"] += 1
        user_xp[author_id]["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Yeni səviyyəyə yüksəldin: **Səviyyə {user_xp[author_id]['level']}** 🚀✨")
        except:
            pass

    # ⚡ 2. SPAM & FLOOD QORUMASI: Qısa müddətdə çox mesaj atanların mesajı silinir və xəbərdarlıq verilir! ⚡
    if author_id != SAHIB_ID:
        if author_id not in spam_takip:
            spam_takip[author_id] = []
        
        spam_takip[author_id] = [t for t in spam_takip[author_id] if simdi - t < 5]
        spam_takip[author_id].append(simdi)
        
        if len(spam_takip[author_id]) >= 6:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, çox sürətli mesaj yazırsan (Spam Qoruması)! Bir az yavaşla 🛑", delete_after=5)
            except:
                pass
            return

    # 🔠 3. CAPSLOCK QORUMASI: Cümlənin 70%-dən çoxu böyük hərflə yazılıbsa avtomatik silinir! 🔠
    if author_id != SAHIB_ID and len(message.content) > 7:
        buyuk_harf_sayisi = sum(1 for c in message.content if c.isupper())
        if (buyuk_harf_sayisi / len(message.content)) > 0.7:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, zəhmət olmasa daimi böyük hərflə (CapsLock) yazma! 🔕", delete_after=5)
                return
            except:
                pass

    await bot.process_commands(message)

# =====================================================================
# 👑 1. SAHİB & İDARƏETMƏ KOMUTLARI 👑
# =====================================================================
@bot.command(name="elan", help="📢 Serverdə xüsusi elan embed mesajı atır.")
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

@bot.command(name="cekilis", help="🎁 Serverdə hədiyyə çəkilişi başladır.")
async def cekilis(ctx, *, odul: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="🎁 ÇEKİLİŞ", description=f"Ödül: **{odul}**\nQatılmaq üçün 🎉 emojisinə bas! 🚀", color=0xff00ff)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")

@bot.command(name="duyuru", help="🔔 Ümumi məlumatləndirmə duyurusu göndərir.")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"🔔 **DÜYURU:** {metin} 📢")

@bot.command(name="bakim", help="🛠️ Serverin baxım rejimini aktivləşdirir.")
async def bakim(ctx, durum: str = "açıq"):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send(f"🛠️ Baxım rejimi: **{durum}** olaraq dəyişdirildi! ⚠️")

# =====================================================================
# 🛡️ 2. TƏHLÜKƏSİZLİK & GİZLİLİK KOMUTLARI 🛡️
# =====================================================================
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

@bot.command(name="sesgizle", help="🔇 Səs kanalına qoşulmanı bağlayır.")
async def sesgizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=False)
    await ctx.send("🔇 Səs kanalı girişə bağlandı! 🛑")

@bot.command(name="sesgoster", help="🔊 Səs kanalına qoşulmanı açır.")
async def sesgoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=True)
    await ctx.send("🔊 Səs kanalı girişə açıldı! 🟢")

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
    await ctx.send("🔓 Bütün server kanalları açıldı! 🌍")

# =====================================================================
# 📋 3. MƏLUMAT & STATİSTİKALAR KOMUTLARI 📋
# =====================================================================
@bot.command(name="server", help="🏰 Server haqqında ümumi statistik məlumat verir.")
async def server(ctx):
    g = ctx.guild
    await ctx.send(f"🏰 Server: **{g.name}** | Üzv: **{g.member_count}** | Yaradılma: **{g.created_at.strftime('%d.%m.%Y')}** 🌟")

@bot.command(name="userinfo", help="👤 İstifadəçinin qeydiyyat və profil məlumatlarını göstərir.")
async def userinfo(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(f"👤 İstifadəçi: **{u.name}** | ID: `{u.id}` | Qoşuldu: **{u.joined_at.strftime('%d.%m.%Y')}** 📌")

@bot.command(name="botinfo", help="🤖 Botun versiya və sistem məlumatlarını göstərir.")
async def botinfo(ctx):
    await ctx.send("🤖 Bot sürümü: **v3500 Pro Max** | Python & Discord.py ⚡")

@bot.command(name="ping", help="🏓 Botun internet gecikmə sürətini (ms) ölçür.")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Botun gecikməsi: `{round(bot.latency * 1000)}ms` ⚡")

@bot.command(name="online", help="🟢 Serverdə onlayn olan üzvlərin sayını göstərir.")
async def online(ctx):
    c = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 Aktiv (Onlayn) üzv sayı: **{c}** ✨")

@bot.command(name="hava", help="🌤️ Seçilən şəhərin təxmini hava şəraitini göstərir.")
async def hava(ctx, *, seher: str = "Bakı"):
    await ctx.send(f"🌤️ {seher} üçün hava istiliyi: **{random.randint(18, 35)}°C** (Günəşli ☀️)")

@bot.command(name="hesabla", help="🧮 Riyazi əməliyyatları hesablayır.")
async def hesabla(ctx, *, islem: str):
    try:
        netice = eval(islem)
        await ctx.send(f"🧮 Nəticə: `{netice}` ✅")
    except:
        await ctx.send("❌ Xəta! Doğru riyazi əməliyyat daxil et ⚠️")

@bot.command(name="rolbilgi", help="📌 Qeyd edilən rol haqqında məlumat verir.")
async def rolbilgi(ctx, role: discord.Role):
    await ctx.send(f"📌 Rol: **{role.name}** | ID: `{role.id}` | Üzv sayı: **{len(role.members)}** 🛡️")

@bot.command(name="kanalbilgi", help="📌 Kanalın ID və digər məlumatlarını göstərir.")
async def kanalbilgi(ctx, channel: discord.TextChannel = None):
    ch = channel or ctx.channel
    await ctx.send(f"📌 Kanal: **{ch.name}** | ID: `{ch.id}` 📂")

@bot.command(name="level", help="⭐ Sənin və ya başqasının səviyyə və XP durumunu göstərir.")
async def level(ctx, m: discord.Member = None):
    target = m or ctx.author
    if target.id in user_xp:
        lvl = user_xp[target.id]["level"]
        xp = user_xp[target.id]["xp"]
        await ctx.send(f"⭐ **{target.name}** | Səviyyə: **{lvl}** 🏆 | XP: **{xp}** ⚡")
    else:
        await ctx.send(f"⭐ **{target.name}** hələ heç XP qazanmayıb! (Səviyyə 1) 📌")

# =====================================================================
# 🛠️ 4. MODERASİYA & İDARƏ KOMUTLARI 🛠️
# =====================================================================
@bot.command(name="sil", help="🧹 Yazılan miqdarda mesajı dərhal silir.")
async def sil(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 {amount} ədəd mesaj silindi! ✨", delete_after=3)

@bot.command(name="temizle", help="🧹 Kanalı təmamilə təmizləyir (100 mesaj).")
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
    await ctx.send(f"✅ #{isim} kanalı uğurla yaradıldı! 📂")

@bot.command(name="mute", help="🔇 İstifadəçinin yazmaq və danışmaq hüququnu məhdudlaşdırır.")
async def mute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for c in ctx.guild.channels:
            await c.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.name} mürtədləşdirildi (Cəzalandırıldı) 🛑")

@bot.command(name="unmute", help="🔊 İstifadəçinin cəzasını ləğv edib səbini açır.")
async def unmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role: await member.remove_roles(role)
    await ctx.send(f"🔊 {member.name} cəzası qaldırıldı, səsi açıldı! 🟢")

@bot.command(name="ban", help="🔨 İstifadəçini serverdən qovur və tamamilə banlayır.")
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} serverdən banlandı! ⛔")

@bot.command(name="unban", help="✅ Banlanmış istifadəçinin qadağasını qaldırır.")
async def unban(ctx, *, member_name: str):
    if ctx.author.id != SAHIB_ID: return
    banned = await ctx.guild.bans()
    for entry in banned:
        if entry.user.name == member_name:
            await ctx.guild.unban(entry.user)
            await ctx.send(f"✅ {entry.user.name} üçün ban qaldırıldı! 🔓")
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
    await ctx.send("🔒 Kanal mesajlara bağlandı! 🛑")

@bot.command(name="unlock", help="🔓 Kanalı mesaj yazmağa açır.")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal mesajlara açıldı! ✅")

@bot.command(name="slowmode", help="🐢 Kanalda yavaş rejim (slowmode) tənzimləyir.")
async def slowmode(ctx, saniye: int = 0):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"🐢 Yavaş rejim (Slowmode): **{saniye} saniyə** olaraq tənzimləndi. ⏱️")

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
    await yeni.send("💥 Kanal sıfırlandı və yenidən quruldu! 🚀🔥")

@bot.command(name="reklamver", help="📢 Xüsusi reklam/tövsiyə embed mesajı paylaşır.")
async def reklamver(ctx, *, netin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 TÖVSİYƏ / REKLAM", description=netin, color=0xff0055)
    await ctx.send(embed=embed)

# =====================================================================
# ⚙️ 5. ROL & ÜZV İDARƏSİ KOMUTLARI ⚙️
# =====================================================================
@bot.command(name="rolver", help="✅ İstifadəçiyə xüsusi rol verir.")
async def rolver(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} istifadəçisinə **{role.name}** rolu verildi! 🎖️")

@bot.command(name="rolsil", help="❌ İstifadəçidən müəyyən rolu alır.")
async def rolsil(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} istifadəçisindən **{role.name}** rolu alındı! ⚠️")

@bot.command(name="rolac", help="✨ Serverdə təsadüfi rəngdə yeni rol yaradır.")
async def rolac(ctx, *, rol_adi: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.guild.create_role(name=rol_adi, color=discord.Color.random())
    await ctx.send(f"✨ Yeni rol yaradıldı: **{rol_adi}** 🎨")

@bot.command(name="rolsil_komanda", help="🗑️ Mövcud rolu serverdən tamamilə silir.")
async def rolsil_komanda(ctx, role: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await role.delete()
    await ctx.send("🗑️ Seçilən rol serverdən silindi! ⚠️")

@bot.command(name="nick", help="📝 İstifadəçinin server ləqəbini (Nickname) dəyişir.")
async def nick(ctx, member: discord.Member, *, yeni_ad: str):
    if ctx.author.id != SAHIB_ID: return
    await member.edit(nick=yeni_ad)
    await ctx.send(f"📝 İstifadəçinin adı **{yeni_ad}** olaraq dəyişdirildi! ✨")

@bot.command(name="avatar", help="🖼️ İstifadəçinin profil şəklini böyük şəkildə atır.")
async def avatar(ctx, member: discord.Member = None):
    m = member or ctx.author
    url = m.avatar.url if m.avatar else m.default_avatar.url
    await ctx.send(f"🖼️ {m.name} istifadəçisinin avatarı:\n{url} ✨")

@bot.command(name="yetkililer", help="🛡️ Serverdə səlahiyyətli adminləri göstərir.")
async def yetkililer(ctx):
    staff = [m.name for m in ctx.guild.members if m.guild_permissions.administrator]
    await ctx.send(f"🛡️ Server Adminləri: {', '.join(staff[:10])} 👑")

@bot.command(name="botsay", help="🤖 Serverdəki botların ümumi sayını göstərir.")
async def botsay(ctx):
    c = sum(1 for m in ctx.guild.members if m.bot)
    await ctx.send(f"🤖 Serverdəki bot sayı: **{c}** ⚙️")

@bot.command(name="uyeara", help="🔍 Adında müəyyən hərf/simvol olan üzvləri axtarır.")
async def uyeara(ctx, *, ad: str):
    bulunanlar = [m.name for m in ctx.guild.members if ad.lower() in m.name.lower()]
    await ctx.send(f"🔍 Tapılan üzvlər ({len(bulunanlar)}): {', '.join(bulunanlar[:10])} ✨")

@bot.command(name="sesdesan", help="🔊 Səs kanallarındakı toplam aktiv adam sayını göstərir.")
async def sesdesan(ctx):
    toplam = sum(len(c.members) for c in ctx.guild.voice_channels)
    await ctx.send(f"🔊 Səs kanallarındakı toplam adam sayı: **{toplam}** 🎧")

# =====================================================================
# 🎫 6. TICKET SİSTEMİ & TICKET SPAM QORUMASI 🎫
# =====================================================================
class TicketKapatView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🔒 Ticket-i Bağla", style=discord.ButtonStyle.red, custom_id="ticket_kapat_buton")
    async def ticket_kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Dəstək kanalı 3 saniyəyə silinir... ⏳", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🎫 Ticket Aç", style=discord.ButtonStyle.green, custom_id="ticket_ac_buton")
    async def ticket_ac(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild, author = interaction.guild, interaction.user
        simdi = time.time()
        
        # ⚡ Ticket Spam Qoruması: Qısa müddətdə çox ticket açmağın qarşısını alır! ⚡
        if author.id != SAHIB_ID:
            if author.id not in ticket_spam_kontrol: ticket_spam_kontrol[author.id] = []
            ticket_spam_kontrol[author.id] = [t for t in ticket_spam_kontrol[author.id] if simdi - t < 30]
            ticket_spam_kontrol[author.id].append(simdi)
            if len(ticket_spam_kontrol[author.id]) >= 3:
                await interaction.response.send_message("⚠️ Çox sürətli ticket açmağa çalışırsan! Bir az gözlə 🛑", ephemeral=True)
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
        }
        
        channel = await guild.create_text_channel(f"ticket-{author.name.lower()}", overwrites=overwrites)
        await channel.send(embed=discord.Embed(title="🎫 Dəstək Mərkəzi", description="Səlahiyyətli şəxslər qısa zamanda sizinlə maraqlanacaq. 📌", color=0x00ffcc), view=TicketKapatView())
        await interaction.response.send_message(f"✅ Ticket kanalınız yaradıldı: {channel.mention} 🚀", ephemeral=True)

@bot.command(name="ticketpanel", help="🎫 Ticket açmaq üçün düyməli dəstək paneli yaradır.")
async def ticketpanel(ctx):
  # =====================================================================
# 🚀 BOTU BAŞLATMA QISMI 🚀
# =====================================================================
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    
    if not token:
        print("❌ XƏTA: Replit Secret içində TOKEN tapılmadı! Zəhmət olmasa TOKEN əlavə edin.")
    else:
        bot.run(token)
        
    
