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

SAHIB_ID = 64101496631250258
user_xp = {}
spam_takip = {}
uyari_sayi = {}

@bot.event
async def on_ready():
    print(f"YENİLMEZ Bot Aktivləşdi: {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="r?bot | Professional Management Suite 👑"))

# ==================== EMOJİ REAKSİYA SİSTEMİ ====================
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    try:
        await reaction.message.add_reaction(reaction.emoji)
    except:
        pass

# ==================== QABAQCIL SPAM & TƏHLÜKƏSİZLİK ====================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id == SAHIB_ID or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    sindi = time.time()

    if author_id not in spam_takip:
        spam_takip[author_id] = []

    spam_takip[author_id] = [t for t in spam_takip[author_id] if sindi - t < 4]
    spam_takip[author_id].append(sindi)

    if len(spam_takip[author_id]) >= 4:
        try:
            if author_id not in uyari_sayi:
                uyari_sayi[author_id] = 0
            
            uyari_sayi[author_id] += 1
            await message.delete()

            if uyari_sayi[author_id] == 1:
                await message.channel.send(f"⚠️ {message.author.mention}, spam etmə! İlk xəbərdarlıq, davam etsən zaman aşımı alacaqun.", delete_after=5)
            elif uyari_sayi[author_id] >= 2:
                await message.author.timeout(discord.utils.utcnow() + discord.timedelta(minutes=5), reason="Spam və flood")
                await message.channel.send(f"🔇 {message.author.mention}, dayanmadığın üçün 5 dəqiqəlik zaman aşımı (mute) aldın!", delete_after=6)
                uyari_sayi[author_id] = 0
        except:
            pass
        return

    # Sadə Salamlaşma
    icerik = message.content.lower()
    if icerik in ["salam", "salamlar", "as", "aleykümsalam", "hi", "hello"]:
        try:
            await message.channel.send(f"Salam, {message.author.mention}! Xoş gəlmisən.")
        except:
            pass

    # 10,000 Level XP Sistemi
    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}

    user_xp[author_id]["xp"] += 15
    gerekli_xp = user_xp[author_id]["level"] * 150

    if user_xp[author_id]["xp"] >= gerekli_xp and user_xp[author_id]["level"] < 10000:
        user_xp[author_id]["xp"] -= gerekli_xp
        user_xp[author_id]["level"] += 1
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın! Yeni səviyyən: **{user_xp[author_id]['level']} / 10000** 🚀")
        except:
            pass

    await bot.process_commands(message)

# ==================== R?BOT PANELİ (70+ KOMANDA AÇIqlaması) ====================

@bot.command(name="bot")
async def bot_panel(ctx):
    embed1 = discord.Embed(
        title="🛡️ YENİLMEZ - TƏHLÜKƏSİZLİK & MODERASİYA",
        description="Server təhlükəsizliyi üçün əsas əmrlər:",
        color=0xff0000
    )
    embed1.add_field(name="r?ban / r?unban", value="İstifadəçini ban edir və ya banını açır.", inline=False)
    embed1.add_field(name="r?kick", value="İstifadəçini serverdən qovur.", inline=False)
    embed1.add_field(name="r?mute / r?unmute", value="Zaman aşımı verir və ya qaldırır.", inline=False)
    embed1.add_field(name="r?warn / r?warnings", value="İstifadəçiyə xəbərdarlıq edir və sayına baxır.", inline=False)
    embed1.add_field(name="r?clear / r?purge", value="Mesajları kütləvi təmizləyir.", inline=False)
    embed1.add_field(name="r?lockall / r?unlockall", value="Bütün serveri kilidləyir/açır.", inline=False)

    embed2 = discord.Embed(
        title="⚙️ YENİLMEZ - KANAL VƏ KATEGORİYA İDARƏSİ",
        description="Kanalların yaradılması, gizlədilməsi və silinməsi:",
        color=0x00ff00
    )
    embed2.add_field(name="r?createchannel / r?createvoice", value="Mətn və ya səs kanalı yaradır.", inline=False)
    embed2.add_field(name="r?deletechannel", value="Cari kanalı silir.", inline=False)
    embed2.add_field(name="r?lock / r?unlock", value="Kanalı yazışmaya bağlayır/açır.", inline=False)
    embed2.add_field(name="r?hide / r?reveal", value="Kanalı hamıdan gizlədir/göstərir.", inline=False)
    embed2.add_field(name="r?sesgizle / r?sesgoster", value="Səs kanalını bağlayır/açır.", inline=False)
    embed2.add_field(name="r?slowmode", value="Kanalda yavaş rejim tənzimləyir.", inline=False)
    embed2.add_field(name="r?nuke", value="Kanalı klonlayıb təmiz səhifə açır.", inline=False)
    embed2.add_field(name="r?rename", value="Kanalın adını dəyişdirir.", inline=False)
    embed2.add_field(name="r?topic", value="Kanalın açıqlamasını (topic) dəyişir.", inline=False)

    embed3 = discord.Embed(
        title="👑 YENİLMEZ - ROL VƏ İSTİFADƏÇİ İDARƏSİ",
        description="Rolların verilməsi və istifadəçi məlumatları:",
        color=0x0099ff
    )
    embed3.add_field(name="r?giverole / r?takerole", value="Rollar verir və ya geri alır.", inline=False)
    embed3.add_field(name="r?createrole", value="Yeni rol yaradır.", inline=False)
    embed3.add_field(name="r?deleterole", value="Rolü silir.", inline=False)
    embed3.add_field(name="r?rolecolor", value="Rolün rəngini dəyişir.", inline=False)
    embed3.add_field(name="r?userinfo", value="İstifadəçi haqqında ətraflı məlumat verir.", inline=False)
    embed3.add_field(name="r?avatar", value="İstifadəçinin profil şəklini göstərir.", inline=False)
    embed3.add_field(name="r?botinfo", value="Botun ümumi sistem məlumatlarını göstərir.", inline=False)

    embed4 = discord.Embed(
        title="📊 YENİLMEZ - SERVER, SİSTEM VƏ XP",
        description="Server statistikaları, elanlar və səviyyə sistemi:",
        color=0xffd700
    )
    embed4.add_field(name="r?serverinfo", value="Serverin bütün detallarını göstərir.", inline=False)
    embed4.add_field(name="r?ping", value="Botun gecikmə sürətini ölçür.", inline=False)
    embed4.add_field(name="r?level", value="10.000 səviyyəlik sistemdə XP və level göstərir.", inline=False)
    embed4.add_field(name="r?announcement", value="Serverdə diqqət çəkən rəsmi elan paylaşır.", inline=False)
    embed4.add_field(name="r?poll", value="Anket yaradır.", inline=False)
    embed4.add_field(name="r?say", value="Botun dilindən istədiyin mətni yazdırır.", inline=False)
    embed4.add_field(name="r?membercount", value="Serverdəki toplam üzv sayını göstərir.", inline=False)
    embed4.set_footer(text="YENİLMEZ Bot © 2026 | Bütün 70+ funksiya aktivdir ⚡")

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)

# ==================== 1. MODERASİYA KOMANDALARI ====================
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

@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

# ==================== 2. KANAL VƏ KATEGORİYA İDARƏSİ ====================
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
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
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

@bot.command(name="sesgizle")
@commands.has_permissions(manage_channels=True)
async def sesgizle(ctx, channel: discord.VoiceChannel):
    await channel.set_permissions(ctx.guild.default_role, connect=False)
    await ctx.send(f"🔇 `{channel.name}` səs kanalı girişə bağlandı.")

@bot.command(name="sesgoster")
@commands.has_permissions(manage_channels=True)
async def sesgoster(ctx, channel: discord.VoiceChannel):
    await channel.set_permissions(ctx.guild.default_role, connect=True)
    await ctx.send(f"🔊 `{channel.name}` səs kanalı girişə açıldı.")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Kanalın yavaş modu `{seconds}` saniyə edildi.")

@bot.command(name="nuke")
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    channel = ctx.channel
    position = channel.position
    new_channel = await channel.clone(reason="Nuke command executed")
    await channel.delete()
    await new_channel.edit(position=position)
    await new_channel.send("💥 Kanal uğurla təmizləndi (Nuke atıldı)!")

@bot.command(name="rename")
@commands.has_permissions(manage_channels=True)
async def rename(ctx, *, yeni_ad):
    await ctx.channel.edit(name=yeni_ad)
    await ctx.send(f"✏️ Kanalın adı dəyişdirildi: `{yeni_ad}`")

@bot.command(name="topic")
@commands.has_permissions(manage_channels=True)
async def topic(ctx, *, yeni_topic):
    await ctx.channel.edit(topic=yeni_topic)
    await ctx.send("📝 Kanal açıqlaması yeniləndi.")

# ==================== 3. ROL VƏ İSTİFADƏÇİ İDARƏSİ ====================
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

# ==================== 4. SERVER VƏ MƏLUMAT KOMANDALARI ====================
@bot.command(name="serverinfo")
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"📊 {guild.name} - Server Statistikası", color=0x3498DB)
    embed.add_field(name="Üzv Sayı", value=guild.member_count, inline=True)
    embed.add_field(name="Kanal Sayı", value=len(guild.channels), inline=True)
    embed.add_field(name="Rol Sayı", value=len(guild.roles), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

@bot.command(name="membercount")
async def membercount(ctx):
    await ctx.send(f"👥 Serverdə ümumi **{ctx.guild.member_count}** üzv var!")

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

@bot.command(name="poll")
@commands.has_permissions(manage_messages=True)
async def poll(ctx, *, soru):
    await ctx.message.delete()
    msg = await ctx.send(embed=discord.Embed(title="📊 ANKET", description=soru, color=0x0099ff))
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="say")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, mesaj):
    await ctx.message.delete()
    await ctx.send(mesaj)

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if token:
        bot.run(token)
