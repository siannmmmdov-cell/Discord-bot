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
    await bot.change_presence(activity=discord.Game(name="r?bot | Moderasiya və İdarəetmə 👑"))

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

    # Sadə Salamlaşma (Kimin yazmasından asılı olmayaraq sadə və qısa cavab)
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

# ==================== R?BOT PANELİ ====================

@bot.command(name="bot")
async def bot_panel(ctx):
    # 1-ci Embed: Təhlükəsizlik və Moderasiya
    embed1 = discord.Embed(
        title="🛡️ YENİLMEZ - TƏHLÜKƏSİZLİK & MODERASİYA",
        description="Serveri qorumaq və tənzimləmək üçün əsas əmrlər:",
        color=0xff0000
    )
    embed1.add_field(name="r?ban <istifadəçi>", value="Seçilən istifadəçini serverdən tamamilə qovur.", inline=False)
    embed1.add_field(name="r?kick <istifadəçi>", value="İstifadəçini serverdən uzaqlaşdırır.", inline=False)
    embed1.add_field(name="r?mute <istifadəçi> <dəqiqə>", value="Qayda pozana zaman aşımı (timeout) verir.", inline=False)
    embed1.add_field(name="r?unmute <istifadəçi>", value="Cəza alan istifadəçinin qadağasını qaldırır.", inline=False)
    embed1.add_field(name="r?warn <istifadəçi> <səbəb>", value="İstifadəçiyə xəbərdarlıq göndərir.", inline=False)
    embed1.add_field(name="r?clear <say>", value="Mətndəki mesajları qeyd edilən sayda təmizləyir.", inline=False)

    # 2-ci Embed: Kanal və Server İdarəetməsi
    embed2 = discord.Embed(
        title="⚙️ YENİLMEZ - KANAL VƏ İDARƏETMƏ",
        description="Kanal, səs və rol idarəetmə əmrləri:",
        color=0x00ff00
    )
    embed2.add_field(name="r?createchannel <ad>", value="Yeni mətn kanalı yaradır.", inline=False)
    embed2.add_field(name="r?deletechannel", value="Hazırda yazılan kanalı silir.", inline=False)
    embed2.add_field(name="r?lock", value="Kanalı yazışmaya bağlayır.", inline=False)
    embed2.add_field(name="r?unlock", value="Bağlanmış kanalın kilidini açır.", inline=False)
    embed2.add_field(name="r?hide", value="Mətn kanalını hamıdan gizlədir.", inline=False)
    embed2.add_field(name="r?reveal", value="Gizlədilmiş kanalı yenidən göstərir.", inline=False)
    embed2.add_field(name="r?slowmode <saniyə>", value="Kanalda yavaş rejim (slowmode) qoyur.", inline=False)
    embed2.add_field(name="r?nuke", value="Kanalı təmizləmək üçün klonlayıb yenidən yaradır.", inline=False)
    embed2.add_field(name="r?giverole / r?takerole", value="İstifadəçiyə rol verir və ya rolunu alır.", inline=False)
    embed2.add_field(name="r?announcement", value="Serverdə diqqət çəkən elan açır.", inline=False)

    # 3-cü Embed: Məlumat və Sistem
    embed3 = discord.Embed(
        title="📊 YENİLMEZ - MƏLUMAT VƏ SƏVİYYƏ",
        description="Statistika və səviyyə izləmə əmrləri:",
        color=0xffd700
    )
    embed3.add_field(name="r?ping", value="Botun serverlə əlaqə sürətini (ms) ölçür.", inline=False)
    embed3.add_field(name="r?level [istifadəçi]", value="10.000 səviyyəlik sistemdə cari səviyyəni və XP-ni göstərir.", inline=False)
    embed3.set_footer(text="YENİLMEZ Bot © 2026 | Bütün əmrlər tam işlək vəziyyətdədir ⚡")

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)

# ---- Moderasiya Əmrləri (İngiliscə Adlar) ----
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} serverdən ban edildi!")

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

# ---- Kanal & Səs İdarəetməsi (İngiliscə Adlar & Nuke) ----
@bot.command(name="createchannel")
@commands.has_permissions(manage_channels=True)
async def createchannel(ctx, *, isim):
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"✅ `{isim}` adlı mətn kanalı yaradıldı.")

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

# ---- Rol & Elan Əmrləri (İngiliscə Adlar) ----
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

@bot.command(name="announcement")
@commands.has_permissions(administrator=True)
async def announcement(ctx, *, mesaj):
    await ctx.message.delete()
    embed = discord.Embed(title="📢 SERVER ELANI", description=mesaj, color=0xff9900)
    await ctx.send(embed=embed)

# ---- Məlumat Əmrləri ----
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Gecikmə: `{round(bot.latency * 1000)}ms`")

@bot.command(name="level")
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = user_xp.get(member.id, {"xp": 0, "level": 1})
    await ctx.send(f"📈 {member.mention} səviyyəsi: **{data['level']} / 10000** (XP: {data['xp']})")

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if token:
        bot.run(token)
                
