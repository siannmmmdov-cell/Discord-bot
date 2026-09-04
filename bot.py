import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
import time
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot online!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True

bot = commands.Bot(command_prefix='r?', intents=intents)

# SAHIB_ID-ni öz ID-n ilə dəyişdir!
SAHIB_ID = 64101496631250258 
user_xp = {}
spam_takip = {}
uyari_sayi = {}
auto_role_name = "Üzv"  # Yeni qoşulana veriləcək rol adı

@bot.event
async def on_ready():
    print(f"YENİLMEZ Bot Aktivləşdi: {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="r?bot | Professional Management Suite 👑"))

# ==================== 1. EMOJİ REAKSİYA SİSTEMİ ====================
# Botun atdığı mesajlara avtomatik reaksiyaları əks etdirir
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    try:
        await reaction.message.add_reaction(reaction.emoji)
    except:
        pass

# ==================== 2. AVTO-ROL (YENİ ÜZV QOŞULANDA) ====================
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Salam, {member.mention}! Xoş gəlmisən, aramızda yerin hazır idi.")
    
    try:
        role = discord.utils.get(member.guild.roles, name=auto_role_name)
        if role:
            await member.add_roles(role)
    except:
        pass

# ==================== 3. SPAM, SALAM & XP SİSTEMİ ====================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Sahib və Adminlər spamdan və salamlaşmadan azaddır
    if message.author.id == SAHIB_ID or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    sindi = time.time()

    # ==================== Qabaqcıl Spam Qoruması ====================
    if author_id not in spam_takip:
        spam_takip[author_id] = []

    spam_takip[author_id] = [t for t in spam_takip[author_id] if sindi - t < 3] # 3 saniyəlik pəncərə
    spam_takip[author_id].append(sindi)

    if len(spam_takip[author_id]) >= 5: # 3 saniyədə 5 mesaj spama gedir
        try:
            if author_id not in uyari_sayi:
                uyari_sayi[author_id] = 0
            
            uyari_sayi[author_id] += 1
            await message.delete()

            if uyari_sayi[author_id] == 1:
                await message.channel.send(f"⚠️ {message.author.mention}, spam etmə! İlk xəbərdarlıq.", delete_after=5)
            elif uyari_sayi[author_id] >= 2:
                await message.author.timeout(discord.utils.utcnow() + discord.timedelta(minutes=5), reason="Spam və flood")
                await message.channel.send(f"🔇 {message.author.mention}, dayanmadığın üçün 5 dəqiqəlik mute aldın!", delete_after=6)
                uyari_sayi[author_id] = 0
        except:
            pass
        return

    # ==================== Səmimi Salamlaşma ====================
    icerik = message.content.lower()
    if icerik in ["salam", "salamlar", "as", "aleykümsalam", "hi", "hello"]:
        try:
            await message.channel.send(f"Salam, {message.author.mention}! Xoş gəlmisən, səni görməyimizə şadıq! 👋")
        except:
            pass

    # ==================== Getdikcə Çətinləşən XP / Level Sistemi ====================
    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}

    # Hər mesaj üçün 15 XP verir
    user_xp[author_id]["xp"] += 15
    
    # Səviyyə atlamaq üçün tələb olunan XP formulu (çətinləşən)
    gerekli_xp = user_xp[author_id]["level"] * 300 + 200

    if user_xp[author_id]["xp"] >= gerekli_xp:
        user_xp[author_id]["xp"] -= gerekli_xp
        user_xp[author_id]["level"] += 1
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Səviyyə atladın! Yeni səviyyən: **{user_xp[author_id]['level']}** 🚀")
        except:
            pass

    await bot.process_commands(message)

# ==================== 4. R?BOT PANELİ (MƏLUMAT ƏMRİ) ====================

@bot.command(name="bot")
async def bot_panel(ctx):
    embed1 = discord.Embed(
        title="🛡️ YENİLMEZ - TƏHLÜKƏSİZLİK & MODERASİYA",
        description="Server təhlükəsizliyi üçün əsas əmrlər:",
        color=0xff0000
    )
    embed1.add_field(name="r?ban / r?unban", value="İstifadəçini ban edir/açır.", inline=True)
    embed1.add_field(name="r?kick", value="İstifadəçini serverdən qovur.", inline=True)
    embed1.add_field(name="r?mute / r?unmute", value="Zaman aşımı verir/qaldırır.", inline=True)
    embed1.add_field(name="r?warn", value="İstifadəçiyə xəbərdarlıq edir.", inline=True)
    embed1.add_field(name="r?clear", value="Mesajları kütləvi təmizləyir.", inline=True)
    embed1.add_field(name="r?lockall / r?unlockall", value="Bütün serveri kilidləyir/açır.", inline=True)

    embed2 = discord.Embed(
        title="⚙️ YENİLMEZ - KANAL VƏ SİFIRLAMA İDARƏSİ",
        description="Kanalların idarə edilməsi, nuke və təmizlənməsi:",
        color=0x00ff00
    )
    embed2.add_field(name="r?createchannel / r?createvoice", value="Kanal yaradır.", inline=True)
    embed2.add_field(name="r?deletechannel", value="Cari kanalı silir.", inline=True)
    embed2.add_field(name="r?lock / r?unlock", value="Kanalı yazışmaya bağlayır/açır.", inline=True)
    embed2.add_field(name="r?hide / r?reveal", value="Kanalı gizlədir/göstərir.", inline=True)
    embed2.add_field(name="r?slowmode", value="Kanalda yavaş rejim tənzimləyir.", inline=True)
    embed2.add_field(name="r?nuke", value="Kanalı silmədən içini sıfırlayır.", inline=True)
    embed2.add_field(name="r?rename", value="Kanalın adını dəyişir.", inline=True)

    embed3 = discord.Embed(
        title="👑 YENİLMEZ - ROL VƏ İSTİFADƏÇİ İDARƏSİ",
        description="Rolların verilməsi və istifadəçi məlumatları:",
        color=0x0099ff
    )
    embed3.add_field(name="r?giverole / r?takerole", value="Rol verir və ya alır.", inline=True)
    embed3.add_field(name="r?createrole / r?deleterole", value="Rol yaradır və ya silir.", inline=True)
    embed3.add_field(name="r?userinfo", value="İstifadəçi haqqında məlumat verir.", inline=True)
    embed3.add_field(name="r?avatar", value="İstifadəçinin profil şəklini göstərir.", inline=True)
    embed3.add_field(name="r?botinfo", value="Botun sistem məlumatlarını göstərir.", inline=True)

    embed4 = discord.Embed(
        title="📊 YENİLMEZ - XÜSUSİ ALƏTLƏR, ÇƏKİLİŞ & XP",
        description="Banner, səsvermə, çəkiliş və səviyyə sistemləri:",
        color=0xffd700
    )
    embed4.add_field(name="r?embed <başlıq> | <mətn>", value="Qəşəng embed mesaj göndərir.", inline=True)
    embed4.add_field(name="r?suggestion <təklif>", value="Təklif paneli yaradır.", inline=True)
    embed4.add_field(name="r?serverlock", value="Serveri yeni qoşulmalara qapadır/açır.", inline=True)
    embed4.add_field(name="r?serverinfo", value="Serverin bütün detallarını göstərir.", inline=True)
    embed4.add_field(name="r?ping", value="Botun gecikmə sürətini ölçür.", inline=True)
    embed4.add_field(name="r?level", value="XP və level göstərir (getdikcə çətinləşən).", inline=True)
    embed4.add_field(name="r?announcement", value="Serverdə rəsmi elan paylaşır.", inline=True)
    embed4.add_field(name="r?banner / r?serverbanner", value="İstifadəçi və ya server bannerini göstərir.", inline=True)
    embed4.add_field(name="r?poll <sual>", value="Avtomatik reaksiyalı anket açır.", inline=True)
    embed4.add_field(name="r?say <mətn>", value="Yazdığın mətni botun dilindən göndərir.", inline=True)
    embed4.add_field(name="r?çekiliş <gün> <hədiyyə>", value="Çəkiliş başladır (Məs: r?çekiliş 2 nitro).", inline=True)
    embed4.set_footer(text="YENİLMEZ Bot © 2026 | Bütün funksiyalar tam işlək vəziyyətdədir ⚡")

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)

# ==================== 5. MODERASİYA KOMANDALARI ====================
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} serverdən ban edildi!")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name.lower() == member_name.lower():
            await ctx.guild.unban(user)
            await ctx.send(f"🔓 {user.mention} ban-dan çıxarıldı!")
            return
    await ctx.send("❌ Bu adda ban edilmiş istifadəçi tapılmadı.")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} serverdən qovuldu!")

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, minutes: int = 5):
    await member.timeout(discord.utils.utcnow() + discord.timedelta(minutes=minutes))
    await ctx.send(f"🔇 {member.mention} {minutes} dəqiqəlik mute-ləndi!")

@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} mute-dən çıxarıldı!")

@bot.command(name="warn")
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    await ctx.send(f"⚠️ {member.mention} xəbərdar edildi! Səbəb: {reason}")

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 `{len(deleted)}` dənə mesaj təmizləndi!", delete_after=3)

# ==================== 6. KANAL VƏ SİFIRLAMA İDARƏSİ ====================
@bot.command(name="createchannel")
@commands.has_permissions(manage_channels=True)
async def createchannel(ctx, *, isim):
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"✅ `{isim}` adlı mətn kanalı yaradıldı.")

@bot.command(name="createvoice")
@commands.has_permissions(manage_channels=True)
async def createvoice(ctx, *, isim):
    await ctx.guild.create_voice_channel(isim)
    await ctx.send(f"✅ `{isim}` adlı səs kanalı yaradıldı.")

@bot.command(name="deletechannel")
@commands.has_permissions(manage_channels=True)
async def deletechannel(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.delete()

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(
    ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal yazışmaya açıldı.")

@bot.command(name="hide")
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await ctx.send("👻 Bu kanal hamıdan gizlətildi!")

@bot.command(name="reveal")
@commands.has_permissions(manage_channels=True)
async def reveal(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=True)
    await ctx.send("👀 Bu kanal yenidən hər kəsə göstərildi.")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Kanalın yavaş modu `{seconds}` saniyə edildi.")

@bot.command(name="nuke")
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    try:
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=None)
        await ctx.send(f"💥 Kanal silmədən sıfırlandı! Toplam `{len(deleted)}` mesaj təmizləndi.", delete_after=5)
    except discord.HTTPException as e:
        if e.code == 50074:
            await ctx.send("❌ Bu kanal İcma (Community) serverinin əsas kanalıdır, təmizlənməsinə Discord icazə vermir.", delete_after=7)
        else:
            raise e

@bot.command(name="rename")
@commands.has_permissions(manage_channels=True)
async def rename(ctx, *, yeni_ad):
    await ctx.channel.edit(name=yeni_ad)
    await ctx.send(f"✏️ Kanalın adı dəyişdirildi: `{yeni_ad}`")

@bot.command(name="giverole")
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} istifadəçisinə `{role.name}` rolu verildi.")

@bot.command(name="takerole")
@commands.has_permissions(manage_roles=True)
async def takerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} istifadəçisindən `{role.name}` rolu alındı.")

@bot.command(name="createrole")
@commands.has_permissions(manage_roles=True)
async def createrole(ctx, *, rol_adi):
    await ctx.guild.create_role(name=rol_adi)
    await ctx.send(f"✨ `{rol_adi}` adlı yeni rol yaradıldı.")

@bot.command(name="deleterole")
@commands.has_permissions(manage_roles=True)
async def deleterole(ctx, role: discord.Role):
    await role.delete()
    await ctx.send(f"🗑️ `{role.name}` rolu silindi.")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 İstifadəçi Məlumatı: {member.name}", color=0x00ffcc)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Qoşulma Tarixi", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0xff00ff)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="botinfo")
async def botinfo(ctx):
    embed = discord.Embed(title="🤖 YENİLMEZ Bot Sistem Məlumatı", description="Professional Discord Management Bot", color=0x7289DA)
    embed.add_field(name="Yaradıcı / Sahib", value="<@64101496631250258>", inline=True)
    embed.add_field(name="Server Sayı", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Status", value="Aktiv & Qorumalı ⚡", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="lockall")
@commands.has_permissions(administrator=True)
async def lockall(ctx):
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        except:
            pass
    await ctx.send("🔒 Bütün serverdəki mətn kanalları yazışmaya bağlandı!")

@bot.command(name="unlockall")
@commands.has_permissions(administrator=True)
async def unlockall(ctx):
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        except:
            pass
    await ctx.send("🔓 Bütün serverdəki mətn kanalları yazışmaya açıldı!")

@bot.command(name="serverlock")
@commands.has_permissions(administrator=True)
async def serverlock(ctx):
    await ctx.guild.edit(verification_level=discord.VerificationLevel.high)
    await ctx.send("🚨 Server təhlükəsizlik rejiminə keçirildi.")

@bot.command(name="embed")
@commands.has_permissions(manage_messages=True)
async def custom_embed(ctx, *, text):
    await ctx.message.delete()
    if "|" in text:
        title, desc = text.split("|", 1)
        embed = discord.Embed(title=title.strip(), description=desc.strip(), color=0x00ffcc)
    else:
        embed = discord.Embed(description=text, color=0x00ffcc)
    await ctx.send(embed=embed)

@bot.command(name="suggestion")
async def suggestion(ctx, *, teklif):
    await ctx.message.delete()
    embed = discord.Embed(title="💡 YENİ TƏKLİF", description=teklif, color=0x9b59b6)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="banner")
async def banner(ctx, member: discord.Member = None):
    member = member or ctx.author
    user = await bot.fetch_user(member.id)
    if user.banner:
        embed = discord.Embed(title=f"🎨 {member.name} - Server Banneri", color=0x9b59b6)
        embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ {member.mention} istifadəçisinin xüsusi banneri yoxdur.")

@bot.command(name="serverbanner")
async def serverbanner(ctx):
    guild = ctx.guild
    if guild.banner:
        embed = discord.Embed(title=f"🖼️ {guild.name} - Server Banneri", color=0x3498DB)
        embed.set_image(url=guild.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Bu serverin xüsusi banner şəkli yoxdur.")

@bot.command(name="poll")
@commands.has_permissions(manage_messages=True)
async def poll(ctx, *, soru):
    await ctx.message.delete()
    embed = discord.Embed(title="📊 ANKET / SƏSVERMƏ", description=soru, color=0x2ecc71)
    embed.set_footer(text=f"Anketi yaradan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="say")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, mesaj):
    await ctx.message.delete()
    await ctx.send(mesaj)

@bot.command(name="çekiliş", aliases=["cekilis"])
@commands.has_permissions(manage_guild=True)
async def çekiliş(ctx, zaman_gun: int, *, odul):
    await ctx.message.delete()
    saniye = zaman_gun * 86400

    embed = discord.Embed(
        title="🎉 YENİ ÇƏKİLİŞ! 🎉",
        description=f"Hədiyyə: **{odul}**\n\nQatılmaq üçün aşağıdakı 🎉 reaksiyasına toxun!\nBitmə müddəti: **{zaman_gun} gün**",
        color=0xe91e63
    )
    embed.set_footer(text=f"Çəkilişi təşkil edən: {ctx.author.name}")
    
    mesaj = await ctx.send(embed=embed)
    await mesaj.add_reaction("🎉")

    await asyncio.sleep(saniye)

    try:
        yeni_mesaj = await ctx.channel.fetch_message(mesaj.id)
        reaksiya = discord.utils.get(yeni_mesaj.reactions, emoji="🎉")
        
        if reaksiya:
            istirakcilar = [user async for user in reaksiya.users() if not user.bot]
            
            if istirakcilar:
                qalib = random.choice(istirakcilar)
                await ctx.send(f"🎊 Təbriklər {qalib.mention}! **{odul}** çəkilişinin qalibi oldun! 🏆")
            else:
                await ctx.send("❌ Çəkilişə heç kim qoşulmadığı üçün qalib seçilmədi.")
        else:
            await ctx.send("❌ Çəkiliş zamanı xəta baş verdi.")
    except Exception as e:
        await ctx.send(f"❌ Çəkiliş nəticələnərkən xəta yarandı: {e}")

@bot.command(name="serverinfo")
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} - Server Statistikası", color=0x3498DB)
    embed.add_field(name="Üzv Sayı", value=guild.member_count, inline=True)
    embed.add_field(name="Kanal Sayı", value=len(guild.channels), inline=True)
    embed.add_field(name="Rol Sayı", value=len(guild.roles), inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Gecikmə: `{round(bot.latency * 1000)}ms`")

@bot.command(name="level")
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = user_xp.get(member.id, {"xp": 0, "level": 1})
    await ctx.send(f"📈 {member.mention} səviyyəsi: **{data['level']} / 10000** (XP: {data['xp']})")

@bot.command(name="announcement")
@commands.has_permissions(administrator=True)
async def announcement(ctx, *, mesaj):
    await ctx.message.delete()
    embed = discord.Embed(title="📢 SERVER ELANI", description=mesaj, color=0xff9900)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if token:
        bot.run(token)
             
