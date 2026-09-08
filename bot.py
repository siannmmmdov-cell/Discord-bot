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
SAHIB_ID = 643014966312001350  # Sənin Sahib ID-n

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.presences = True
intents.invites = True

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
    print(f" [XAS ULTRA] Bot Uğurla İşə Düşdü!")
    print(f" Bot Tag: {bot.user}")
    print(f" Server Sayı: {len(bot.guilds)}")
    print(f"--------------------------------------------------")
    status_task.start()

@tasks.loop(seconds=10)
async def status_task():
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="!panel | XAS Security"),
        discord.Activity(type=discord.ActivityType.playing, name="discord.gg/xas"),
        discord.Activity(type=discord.ActivityType.listening, name="XAS Sistem & Komutlar"),
    ]
    await bot.change_presence(activity=random.choice(activities))

@bot.event
async def on_member_join(member):
    if member.bot:
        return
    try:
        embed = discord.Embed(
            title="XAS Serverinə Xoş Gəldin!",
            description=f"Salam {member.mention}, səni aramızda görməkdən şadıq!\n\n> Qaydaları oxumağı unutma.",
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
            await message.channel.send(f"👋 {message.author.mention}, yenidən xoş gəldin! AFK rejimindən çıxarıldın.", delete_after=5)
        except:
            pass

    for mention in message.mentions:
        if mention.id in afk_users:
            sebep = afk_users[mention.id]
            await message.channel.send(f"💤 Etiketlədiyiniz istifadəçi (`{mention.name}`) şu an AFK-dır. Səbəb: **{sebep}**")

    if "gg/" in icerik or "discord.gg/" in icerik or "https://" in icerik or "http://" in icerik:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə reklam və link paylaşmaq qadağandır!")
            await asyncio.sleep(5)
            await warn.delete()
            return
        except:
            pass

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
                warn = await message.channel.send(f"⚠️ {message.author.mention}, xahiş edirik spam etməyin!")
                await asyncio.sleep(4)
                await warn.delete()
            else:
                await message.author.timeout(timedelta(seconds=60), reason="Spam Flood")
                warn = await message.channel.send(f"🔇 {message.author.mention}, spam səbəbilə 1 dəqiqəlik mute olundu!")
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
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın və **{user_levels[author_id]['level']}** səviyyə oldun!")
        except:
            pass

    await bot.process_commands(message)

# =====================================================================
# 5. INTERACTIVE SELECT MENU (PANEL)
# =====================================================================
class XASMenyu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1. Təhlükəsizlik və Nuke", description="Anti-GG, spam qoruması və kanal idarəsi.", emoji="🛡️"),
            discord.SelectOption(label="2. İdarəetmə və Moderasiya", description="Ban, kick, clear, lock, slowmode.", emoji="⚙️"),
            discord.SelectOption(label="3. Əyləncə, Oyunlar və Alətlər", description="Zər, yazı-pər, daş-kağız, sex, fuck, kiss, iq, slot.", emoji="🎮"),
            discord.SelectOption(label="4. XAS Xüsusi URL & Sistem", description="Server dəvət linki və real istifadə statistikası.", emoji="💎")
        ]
        super().__init__(placeholder="XAS İdarəetmə Menyusundan Bölmə Seçin...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "1. Təhlükəsizlik və Nuke":
            embed = discord.Embed(title="🛡️ Təhlükəsizlik Sistemi", description="Serveri qoruyan avtomatik mexanizmlər.", color=XAS_COLOR)
            embed.add_field(name="Anti-GG Link Qoruması", value="Bütün xarici linkləri və dəvətləri dərhal silir.", inline=False)
            embed.add_field(name="Spam Qoruması", value="Flood edənləri avtomatik cəzalandırır.", inline=False)
            embed.add_field(name="🔥 Nuke Əmri", value="`!nuke` - Kanalı sıfırlayıb yenidən yaradır.", inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "2. İdarəetmə və Moderasiya":
            embed = discord.Embed(title="⚙️ Moderasiya Paneli", description="Aktiv moderasiya əmrləri.", color=XAS_COLOR)
            embed.add_field(name="Kanal Əmrləri", value="`!lock` / `!unlock` / `!hide` / `!reveal` / `!slowmode`", inline=False)
            embed.add_field(name="Cəza Əmrləri", value="`!ban` / `!kick` / `!clear` / `!timeout`", inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "3. Əyləncə, Oyunlar və Alətlər":
            embed = discord.Embed(title="🎮 Əyləncə & Oyunlar", description="İstifadəçilər üçün interaktiv oyunlar.", color=XAS_COLOR)
            embed.add_field(name="Xüsusi Əmrlər", value="`!sex` / `!fuck` / `!kiss` | `!roll` | `!coinflip` | `!rps` | `!slot`", inline=False)
            embed.add_field(name="Testlər & Alətlər", value="`!iq` | `!gay` | `!handsome` | `!hack` | `!calc`", inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "4. XAS Xüsusi URL & Sistem":
            embed = discord.Embed(title="💎 XAS URL & Sistem", description="Serverin aktiv dəvət keçidi və statistika məlumatı.", color=XAS_COLOR)
            embed.add_field(name="Rəsmi Dəvət Məlumatı", value="> `!url` yazaraq anlıq dəvət sayını görə bilərsən.", inline=False)
            await interaction.response.edit_message(embed=embed)

class XASView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(XASMenyu())

@bot.command(name="panel")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="💎 XAS İDARƏETMƏ PANELİ",
        description="Aşağıdakı açılan menyudan istədiyiniz kateqoriyanı seçə bilərsiniz.",
        color=XAS_COLOR
    )
    embed.set_footer(text="XAS Security & Management System")
    await ctx.send(embed=embed, view=XASView())

# =====================================================================
# 6. .URL REAL-TIME İNSTANCE & INVITE TRACKER KOMUTU
# =====================================================================
@bot.command(name="url")
async def server_url(ctx):
    try:
        invites = await ctx.guild.invites()
        if invites:
            # Ən çox işlədilən və ya ilk aktiv dəvət linkini tapırıq
            aktiv_davet = max(invites, key=lambda i: i.uses)
            link_url = aktiv_davet.url
            toplam_istifade = aktiv_davet.uses
            davet_eden = aktiv_davet.inviter.name if aktiv_davet.inviter else "Naməlum"
        else:
            link_url = "Serverin aktiv dəvət linki yoxdur."
            toplam_istifade = 0
            davet_eden = "Yoxdur"
    except:
        link_url = "Botun 'Manage Server' icazəsi yoxdur!"
        toplam_istifade = 0
        davet_eden = "Xəta"

    embed = discord.Embed(
        title=f"📊 {ctx.guild.name} — Real Dəvət Statistikası",
        description="Serverin aktiv dəvət bağlantısı və anlıq istifadə sayı:",
        color=XAS_COLOR
    )
    embed.add_field(name="🔗 Aktiv Dəvət Linki", value=f"> {link_url}", inline=False)
    embed.add_field(name="📈 Neçə Nəfər İstifadə Edib?", value=> **{toplam_istifade}** nəfər bu linklə qoşulub!", inline=False)
    embed.add_field(name="👑 Linki Yaradan", value=f"> `{davet_eden}`", inline=False)
    embed.set_footer(text="XAS Security • Anlıq Yenilənən Statistik Sistem")
    await ctx.send(embed=embed)

# =====================================================================
# 7. İNFORMATİV KOMUTLAR
# =====================================================================
@bot.command(name="ping")
async def ping_cmd(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"Pong! 🏓 Gecikmə müddəti: **{lat}ms**")

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"📊 {g.name} - Server Məlumatları", color=XAS_COLOR)
    embed.add_field(name="👑 Sahib", value=g.owner, inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=g.member_count, inline=True)
    embed.add_field(name="📁 Kanal Sayı", value=len(g.channels), inline=True)
    embed.set_thumbnail(url=g.icon.url if g.icon else None)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"👤 {m.name} Haqqında", color=m.color)
    embed.add_field(name="İstifadəçi ID", value=m.id, inline=True)
    embed.add_field(name="Qoşulduğu Tarix", value=m.joined_at.strftime("%Y-%m-%d"), inline=True)
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
    await ctx.send(f"📊 {m.name} - Səviyyə: **{data['level']}** | XP: **{data['xp']}**")

@bot.command(name="afk")
async def afk_cmd(ctx, *, sebep="Səbəb göstərilməyib"):
    afk_users[ctx.author.id] = sebep
    await ctx.send(f"💤 {ctx.author.mention}, AFK rejiminə keçdin. Səbəb: **{sebep}**")

# =====================================================================
# 8. SAHİB VƏ MODERASİYA ƏMRLƏRİ
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

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Yavaş mod `{seconds}` saniyə edildi.")

@bot.command(name="nuke")
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
    await ctx.send(f"🔇 {member.name} `{minutes}` dəqiqə mute olundu.")

@bot.command(name="clear", aliases=["sil"])
async def clear_cmd(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 `{amount}` ədəd mesaj silindi.")
    await asyncio.sleep(3)
    await msg.delete()

# =====================================================================
# 9. ƏYLƏCƏ, ÖPÜŞMƏ VƏ OYUN KOMUTLARI (GIF & REPLY)
# =====================================================================
@bot.command(name="sex", aliases=["öpüş", "öp"])
async def sex_cmd(ctx, member: discord.Member):
    embed = discord.Embed(
        description=f"🔥 **{ctx.author.name}** ilə **{member.name}** ehtiraslı şəkildə öpüşdülər! (Sex)",
        color=XAS_COLOR
    )
    embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1cGp4cWp3aXJ1OG93YWxoeDNnNXQ2ZXJ6aHB2ZGR4NXB6bDVleiZlcD12MV9pbnternFsX2dpZklkJmZ0PWG/9IG32v3x6Y8L6/giphy.gif")
    await ctx.send(embed=embed, reference=ctx.message)

@bot.command(name="fuck")
async def fuck_cmd(ctx, member: discord.Member):
    embed = discord.Embed(
        description=f"🔥 **{ctx.author.name}** ilə **{member.name}** ehtiraslı şəkildə birlikdə oldular! (Fuck)",
        color=XAS_COLOR
    )
    embed.set_image(url="https://images.unsplash.com/photo-1518199266791-5375a83190b7")
    await ctx.send(embed=embed, reference=ctx.message)

@bot.command(name="kiss")
async def kiss_cmd(ctx, member: discord.Member):
    embed = discord.Embed(
        description=f"💋 **{ctx.author.name}** **{member.name}** adlı şəxsi öpdü!",
        color=XAS_COLOR
    )
    embed.set_image(url="https://images.unsplash.com/photo-1518609878373-06d740f60d8b")
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
    await ctx.send(f"📧 IP: `192.168.1.{random.randint(10, 99)}` | Şifrə: `123456_xas` | Şəhər: `Baku`")

@bot.command(name="slot")
async def slot_cmd(ctx):
    sembollər = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]
    c1, c2, c3 = random.choice(sembollər), random.choice(sembollər), random.choice(sembollər)
    netice = f"🎰 | {c1} | {c2} | {c3} |"
    if c1 == c2 == c3:
        await ctx.send(f"{netice}\n🎉 Təbriklər, **Jackpot** vurdun!")
    elif c1 == c2 or c2 == c3 or c1 == c3:
        await ctx.send(f"{netice}\n✨ Pis deyil, 2 eyni simvol tapdın!")
    else:
        await ctx.send(f"{netice}\n❌ Uduzdun, yenidən sına.")

@bot.command(name="8ball", aliases=["sual"])
async def eight_ball(ctx, *, soru):
    cavablar = ["Bəli, mütləq!", "Şübhəsiz ki, hə.", "Gələcək qaranlıqdır.", "Xeyir, heç vaxt.", "Qətiyyən yox!"]
    await ctx.send(f"🎱 Sual: **{soru}**\n🔮 Cavab: **{random.choice(cavablar)}**")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        res = eval(expression)
        await ctx.send(f"🔢 Nəticə: **{res}**")
    except:
        await ctx.send("❌ Xəta! İfadəni düzgün yazın (məsələn: `!calc 5*5`)")

@bot.command(name="joke", aliases=["zarafat"])
async def joke_cmd(ctx):
    jokes = [
        "Kompyuter niyə soyuqdəymə oldu? Çünki pəncərəni açıq qoymuşdu!",
        "Təmirçi niyə yoruldu? Çünki ziddən deyirlər."
    ]
    await ctx.send(f"😄 Zarafat: {random.choice(jokes)}")

@bot.command(name="rps", aliases=["daşkağızqayçı"])
async def rps_cmd(ctx, choice: str):
    choices = ["daş", "kağız", "qayçı"]
    bot_choice = random.choice(choices)
    cho = choice.lower()
    if cho not in choices:
        await ctx.send("Zəhmət olmasa seç: `daş`, `kağız` və ya `qayçı`!")
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
    embed.set_footer(text=f"Sorğunu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# =====================================================================
# 10. BOTU İŞƏ SALMAQ (RUN)
# =====================================================================
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
        
