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
    await bot.change_presence(activity=discord.Game(name="r?bot | Hər Komut Ayrı İzahlı 👑"))

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

    # Səmimi Salamlaşma
    icerik = message.content.lower()
    if icerik in ["salam", "salamlar", "as", "aleykümsalam", "hi", "hello"]:
        try:
            await message.channel.send(f"Salam, xoş gəlmisən {message.author.mention}! 👑 Səfəmizə şad olduq.")
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

# ==================== HƏR KOMUT HAQQINDA AYRI-AYRI İZAHLI r?bot PANELİ ====================

@bot.command(name="bot")
async def bot_panel(ctx):
    # 1-ci Embed: Təhlükəsizlik və Moderasiya
    embed1 = discord.Embed(
        title="🛡️ YENİLMEZ - TƏHLÜKƏSİZLİK & MODERASİYA KOMUTLARI",
        description="Serveri qorumaq və qayda pozanları tənzimləmək üçün əsas əmrlər:",
        color=0xff0000
    )
    embed1.add_field(name="r?ban <istifadəçi>", value="Seçilən istifadəçini serverdən tamamilə qovur (ban edir).", inline=False)
    embed1.add_field(name="r?kick <istifadəçi>", value="İstifadəçini serverdən uzaqlaşdırır (istəsə yenə gələ bilər).", inline=False)
    embed1.add_field(name="r?mute <istifadəçi> <dəqiqə>", value="Qayda pozana göstərilən dəqiqə qədər zaman aşımı (timeout) verir.", inline=False)
    embed1.add_field(name="r?unmute <istifadəçi>", value="Cəza alan istifadəçinin səs/yazı qadağasını qaldırır.", inline=False)
    embed1.add_field(name="r?warn <istifadəçi> <səbəb>", value="İstifadəçiyə rəsmi xəbərdarlıq göndərir.", inline=False)
    embed1.add_field(name="r?sil <say>", value="Mətndəki mesajları qeyd edilən sayda təmizləyir.", inline=False)

    # 2-ci Embed: Kanal və Səs İdarəetməsi
    embed2 = discord.Embed(
        title="⚙️ YENİLMEZ - KANAL, SƏS VƏ ROL İDARƏSİ",
        description="Otaqların və səslərin gizlədilməsi, açılması və idarə edilməsi:",
        color=0x00ff00
    )
    embed2.add_field(name="r?kanalac <ad>", value="Yeni mətn kanalı yaradır.", inline=False)
    embed2.add_field(name="r?kanalsil", value="Hazırda yazdığın və ya işarələdiyin kanalı silir.", inline=False)
    embed2.add_field(name="r?kanalbagla", value="Kanalı üzvlərin yazışmasına bağlayır (Lock).", inline=False)
    embed2.add_field(name="r?kanalas", value="Bağlanmış kanalın kilidini açır.", inline=False)
    embed2.add_field(name="r?kanalgizle", value="Mətn kanalını hamıdan gizlədir.", inline=False)
    embed2.add_field(name="r?kanalgoster", value="Gizlədilmiş kanalı yenidən hər kəsə göstərir.", inline=False)
    embed2.add_field(name="r?sesgizle <kanal>", value="Səs kanalını üzvlərin girişinə bağlayır/gizlədir.", inline=False)
    embed2.add_field(name="r?sesgoster <kanal>", value="Səs kanalının girişini hər kəsə açır.", inline=False)
    embed2.add_field(name="r?yavasmod <saniyə>", value="Kanalda mesajlar arası gözləmə müddəti (slowmode) qoyur.", inline=False)
    embed2.add_field(name="r?rolver / r?rolal", value="İstifadəçiyə rol verir və ya rolunu geri alır.", inline=False)
    embed2.add_field(name="r?duyuru / r?anket", value="Serverdə diqqət çəkən elanlar və ya səsvermə anketləri açır.", inline=False)

    # 3-cü Embed: Əyləncə və Zarafat Komutları
    embed3 = discord.Embed(
        title="🎉 YENİLMEZ - ƏYLƏNCƏ VƏ ZARAFAT KOMUTLARI",
        description="Serverdə darıxmağın qarşısını alacaq əyləncəli əmrlər:",
        color=0x0099ff
    )
    embed3.add_field(name="r?zarafat", value="Bot gülməli lətifələr və zarafatlar danışır.", inline=False)
    embed3.add_field(name="r?sevgi <ad>", value="Qeyd edilən şəxslə sevgi uyğunluğunu faizlə hesablayır.", inline=False)
    embed3.add_field(name="r?hacklə <istifadəçi>", value="Zarafat məqsədilə istifadəçini 'hackləyir' və saxta IP göstərir.", inline=False)
    embed3.add_field(name="r?mənasız", value="Həyatdan mənasız və gülməli fəlsəfi cümlələr verir.", inline=False)
    embed3.add_field(name="r?tiryaki", value="Siqaret/tiryaki əleyhinə dostca xəbərdarlıq edir.", inline=False)
    embed3.add_field(name="r?falbax", value="Gələcəyin barədə qısa və gülməli fal baxır.", inline=False)
    embed3.add_field(name="r?dava <kimlə>", value="İstifadəçi ilə kimsə arasında 'dava' səhnəsi yaradır.", inline=False)
    embed3.add_field(name="r?kral", value="Serverin əsl kralının kim olduğunu açıqlayır.", inline=False)
    embed3.add_field(name="r?zarat / r?yazitura", value="Zər atır və ya yazı-tərəf oyunu oynayır.", inline=False)

    # 4-cü Embed: Məlumat və Sistem
    embed4 = discord.Embed(
        title="📊 YENİLMEZ - MƏLUMAT VƏ SƏVİYYƏ KOMUTLARI",
        description="Statistika və səviyyə izləmə əmrləri:",
        color=0xffd700
    )
    embed4.add_field(name="r?ping", value="Botun serverlə əlaqə sürətini (ms) ölçür.", inline=False)
    embed4.add_field(name="r?seviye [istifadəçi]", value="10.000 səviyyəlik sistemdə cari səviyyəni və XP-ni göstərir.", inline=False)
    embed4.set_footer(text="YENİLMEZ Bot © 2026 | Bütün əmrlər tam işlək vəziyyətdədir ⚡")

    # Hamısını ardıcıl olaraq göndər ki, hər komut haqqında ayrı-ayrı məlumat görünsün!
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)

# ---- Moderasiya Əmrləri ----
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

# ---- Kanal & Səs İdarəetməsi ----
@bot.command(name="kanalac")
@commands.has_permissions(manage_channels=True)
async def kanalac(ctx, *, isim):
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"✅ `{isim}` adlı mətn kanalı yaradıldı.")

@bot.command(name="kanalsil")
@commands.has_permissions(manage_channels=True)
async def kanalsil(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.delete()

@bot.command(name="kanalbagla")
@commands.has_permissions(manage_channels=True)
async def kanalbagla(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")

@bot.command(name="kanalas")
@commands.has_permissions(manage_channels=True)
async def kanalas(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal yazışmaya açıldı.")

@bot.command(name="kanalgizle")
@commands.has_permissions(manage_channels=True)
async def kanalgizle(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await ctx.send("👻 Bu kanal hamıdan gizlətildi!")

@bot.command(name="kanalgoster")
@commands.has_permissions(manage_channels=True)
async def kanalgoster(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=True)
    await ctx.send("👀 Bu kanal yenidən hər kəsə göstərildi.")

@bot.command(name="sesgizle")
@commands.has_permissions(manage_channels=True)
async def sesgizle(ctx, channel: discord.VoiceChannel):
    await channel.set_permissions(ctx.guild.default_role, connect=False)
    await ctx.send(f"🔇 `{channel.name}` səs kanalı gizlətildi.")

@bot.command(name="sesgoster")
@commands.has_permissions(manage_channels=True)
async def sesgoster(ctx, channel: discord.VoiceChannel):
    await channel.set_permissions(ctx.guild.default_role, connect=True)
    await ctx.send(f"🔊 `{channel.name}` səs kanalı açıldı.")

@bot.command(name="yavasmod")
@commands.has_permissions(manage_channels=True)
async def yavasmod(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Kanalın yavaş modu `{seconds}` saniyə edildi.")

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 `{len(deleted)}` dənə mesaj təmizləndi!", delete_after=3)

# ---- Rol & Elan Əmrləri ----
@bot.command(name="rolver")
@commands.has_permissions(manage_roles=True)
async def rolver(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} istifadəçisinə `{role.name}` rolu verildi.")

@bot.command(name="rolal")
@commands.has_permissions(manage_roles=True)
async def rolal(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} istifadəçisindən `{role.name}` rolu alındı.")

@bot.command(name="duyuru")
@commands.has_permissions(administrator=True)
async def duyuru(ctx, *, mesaj):
    await ctx.message.delete()
    embed = discord.Embed(title="📢 SERVER ELANI", description=mesaj, color=0xff9900)
    await ctx.send(embed=embed)

@bot.command(name="anket")
async def anket(ctx, *, soru):
    await ctx.message.delete()
    msg = await ctx.send(embed=discord.Embed(title="📊 ANKET", description=soru, color=0x0099ff))
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# ---- Əyləncə & Zarafat Əmrləri ----
@bot.command(name="zarafat")
async def zarafat(ctx):
    zarafatlar = [
        "Məktəbdə müəllim şagirdə deyir: 'De görüm hara gedirsən?' Şagird: 'Evə müəllim, onsuz da dərs bitdi!'",
        "Kompüter donanda niyə pəncərədən baxmır? Çünki ekran çərçivəsində qalır! 😂",
        "İnternetim o qədər zəifdir ki, Google-da axtarış verəndən sonra qocalıb ölürəm."
    ]
    await ctx.send(f"🤖 {random.choice(zarafatlar)}")

@bot.command(name="sevgi")
async def sevgi(ctx, *, kishi: str):
    await ctx.send(f"❤️ **{ctx.author.name}** ilə **{kishi}** uyğunluğu: **%{random.randint(40, 100)}** 🥰")

@bot.command(name="hacklə")
async def hackle(ctx, member: discord.Member):
    await ctx.send(f"💻 {member.mention} hack olunur... IP: `192.168.0.5` | Şifrə: `yenilmez_123` 🕶️")

@bot.command(name="mənasız")
async def menasiz(ctx):
    await ctx.send(f"🧠 Fəlsəfə: {random.choice(['Su içmək sağlamlığa xeyirlidir.', 'Əgər saatda 60 km gedirsənsə, 1 saata 60 km getmisən.'])}")

@bot.command(name="ayıp")
async def ayip(ctx):
    await ctx.send(f"😳 Ayıp ayıp, {ctx.author.mention}!")

@bot.command(name="tiryaki")
async def tiryaki(ctx):
    await ctx.send("🚬 Çəkmə qardaş, ciyərlərinə yazığın gəl!")

@bot.command(name="falbax")
async def falbax(ctx):
    await ctx.send(f"🔮 Falın: {random.choice(['Bu həftə cibin pul dolacaq.', 'Qarşıdan böyük uğur gəlir.'])}")

@bot.command(name="dava")
async def dava(ctx, *, kimle):
    await ctx.send(f"🥊 {ctx.author.mention} və **{kimle}** arasında dava başladı! 💥")

@bot.command(name="kral")
async def kral(ctx):
    await ctx.send(f"👑 Bu serverin əsl kralı **{ctx.author.name}**-dir!")

@bot.command(name="zarat")
async def zarat(ctx):
    await ctx.send(f"🎲 Zər: **{random.randint(1, 6)}**")

@bot.command(name="yazitura")
async def yazitura(ctx):
    await ctx.send(f"🪙 Nəticə: **{random.choice(['Yazı', 'Tərəf'])}**")

@bot.command(name="məsləhət")
async def meslehet(ctx):
    await ctx.send(f"💡 Məsləhət: {random.choice(['Yuxun gəlirsə yat.', 'Hər zaman özün ol.'])}")

# ---- Məlumat Əmrləri ----
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Gecikmə: `{round(bot.latency * 1000)}ms`")

@bot.command(name="seviye")
async def seviye(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = user_xp.get(member.id, {"xp": 0, "level": 1})
    await ctx.send(f"📈 {member.mention} səviyyəsi: **{data['level']} / 10000** (XP: {data['xp']})")

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if token:
        bot.run(token)
            
