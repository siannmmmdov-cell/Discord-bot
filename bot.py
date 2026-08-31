import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
import time
from flask import Flask
from threading import Thread

# --- KÜÇÜK FLASK SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot onlayndır!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="r?", intents=intents)

# 👑 SƏNİN DİSCORD İD-N 👑
SAHIB_ID = 641014966312501259

# 🎯 TICKET KANAL ID-Sİ
XUSUSI_KANAL_ID = 1544056308787974294 

user_xp = {}
spam_takip = {}
warn_sistemi = {}

@bot.event
async def on_ready():
    print(f"🔥 Bot işə düşdü: {bot.user.name} 🔥")
    await bot.change_presence(activity=discord.Game(name="r?bot | 70+ Əmr Aktivdir 👑"))
    stats_update.start()
    voice_xp_loop.start()

# --- GƏLƏN / GEDƏN ---
@bot.event
async def on_member_join(member):
    kanal = discord.utils.get(member.guild.text_channels, name="gələn-gedən") or member.guild.system_channel
    if kanal:
        embed = discord.Embed(title="🎉 Yeni Üzv!", description=f"Salam {member.mention}, xoş gəldin! Üzv sayı: **{member.guild.member_count}**", color=0x00ff88)
        await kanal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    kanal = discord.utils.get(member.guild.text_channels, name="gələn-gedən") or member.guild.system_channel
    if kanal:
        await kanal.send(f"👋 **{member.name}** serverdən ayrıldı.")

# --- STATİSTİKA & XP ---
@tasks.loop(minutes=10)
async def stats_update():
    for guild in bot.guilds:
        try:
            toplam = guild.member_count
            online = sum(1 for m in guild.members if m.status != discord.Status.offline)
            ses = sum(len(vc.members) for vc in guild.voice_channels)
            for ch in guild.channels:
                if "Üzv:" in ch.name: await ch.edit(name=f"📊 Üzv: {toplam}")
                elif "Onlayn:" in ch.name: await ch.edit(name=f"🟢 Onlayn: {online}")
                elif "Səs:" in ch.name: await ch.edit(name=f"🔊 Səs: {ses}")
        except: pass

@tasks.loop(minutes=1)
async def voice_xp_loop():
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if len(vc.members) > 1:
                for m in vc.members:
                    if m.bot: continue
                    if m.id not in user_xp: user_xp[m.id] = {"xp": 0, "level": 1}
                    user_xp[m.id]["xp"] += 15
                    if user_xp[m.id]["xp"] >= user_xp[m.id]["level"] * 100:
                        user_xp[m.id]["level"] += 1
                        user_xp[m.id]["xp"] = 0

# --- MESAJ NƏZARƏTİ & SPAM ---
@bot.event
async def on_message(message):
    if message.author.bot: return

    if message.author.id == SAHIB_ID:
        if any(g in message.content.lower() for g in ["xd", "asds", "guly", "kara", "hf", "latifə", "😂", "🤣", "💀"]):
            try:
                for emj in random.sample(["😂", "🤣", "💀", "😹", "😆", "🫠"], 3):
                    await message.add_reaction(emj)
            except: pass

    aid = message.author.id
    sindi = time.time()
    if aid not in user_xp: user_xp[aid] = {"xp": 0, "level": 1}
    user_xp[aid]["xp"] += 10
    if user_xp[aid]["xp"] >= user_xp[aid]["level"] * 100:
        user_xp[aid]["level"] += 1
        user_xp[aid]["xp"] = 0
        try: 
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, Səviyyə **{user_xp[aid]['level']}**!")
        except: 
            pass

    if aid != SAHIB_ID:
        if aid not in spam_takip: spam_takip[aid] = []
        spam_takip[aid] = [t for t in spam_takip[aid] if sindi - t < 3]
        spam_takip[aid].append(sindi)
        if len(spam_takip[aid]) >= 9:
            try:
                await message.delete()
                await message.author.timeout(discord.utils.utcnow() + discord.timedelta(seconds=30), reason="Spam")
                await message.channel.send(f"⚠️ {message.author.mention}, spama görə 30 san mute aldın!", delete_after=5)
                return
            except: pass

    await bot.process_commands(message)

# --- TICKET SİSTEMİ ---
class TicketKapat(discord.ui.View):
    @discord.ui.button(label="🔒 Ticketi Bağla", style=discord.ButtonStyle.danger, custom_id="t_kapat")
    async def kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Kanal 5 saniyəyə silinir...", ephemeral=False)
        await asyncio.sleep(5)
        try: await interaction.channel.delete()
        except: pass

class TicketAc(discord.ui.View):
    @discord.ui.button(label="🎫 Ticket Aç", style=discord.ButtonStyle.success, custom_id="t_ac")
    async def ac(self, interaction: discord.Interaction, button: discord.ui.Button):
        g, author = interaction.guild, interaction.user
        overwrites = {
            g.default_role: discord.PermissionOverwrite(view_channel=False),
            author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            g.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
        }
        ch = await g.create_text_channel(f"ticket-{author.name}", overwrites=overwrites)
        await ch.send(f"Salam {author.mention}, dəstək buradadır.", view=TicketKapat())
        await interaction.response.send_message(f"✅ Kanal açıldı: {ch.mention}", ephemeral=True)

# ==============================================================================
# 👑 `r?bot` - 70+ KOMUT MƏLUMAT MƏRKƏZİ
# ==============================================================================
@bot.command(name="bot")
async def bot_komanda(ctx):
    if ctx.author.id != SAHIB_ID: return
    
    embed1 = discord.Embed(
        title="👑 YENİLMEZ v6000 - Əmr Məlumatları (Hissə 1)",
        description="Botdakı bütün sahib və moderasiya əmrləri:",
        color=0xffa200
    )
    embed1.add_field(name="👑 Sahib Əmrləri", value=(
        "`r?bot` - Bütün əmrlər panelini açır.\n"
        "`r?ticketpanel` - Xüsusi kanalda ticket açma düyməsi yaradır.\n"
        "`r?elan` - Serverdə xüsusi elan mətni yayımlayır.\n"
        "`r?anket` - 👍/👎 reaksiyalı anket qurur.\n"
        "`r?cekilis` - Vaxtlı hədiyyə çəkilişi başladır.\n"
        "`r?duyuru` - Rəsmi duyuru mesajı göndərir.\n"
        "`r?bakim` - Baxım rejimini dəyişir.\n"
        "`r?slowmode` - Chatda yavaş mod tənzimləyir.\n"
        "`r?sayac` - Üzv hədəf sayğacını yeniləyir.\n"
        "`r?rolver` - İstifadəçiyə istəപ്പെli rolu verir.\n"
        "`r?rolal` - İstifadəçidən rolu geri alır.\n"
        "`r?botdurdur` - Botu təhlükəsiz şəkildə dayandırır."
    ), inline=False)
    
    embed1.add_field(name="🛡️ Moderasiya Əmrləri", value=(
        "`r?sil` - Kanaldakı mesajları toplu təmizləyir.\n"
        "`r?mute` - İstifadəçinin səsini müvəqqəti alır.\n"
        "`r?unmute` - İstifadəçinin səs qadağasını qaldırır.\n"
        "`r?ban` - İstifadəçini serverdən tamamilə banlayır.\n"
        "`r?unban` - Banlanmış istifadəçinin qadağasını açır.\n"
        "`r?kick` - İstifadəçini serverdən qovur.\n"
        "`r?nuke` - Kanalı tamamilə sıfırlayıb təzələyir.\n"
        "`r?warn` - İstifadəçiyə xəbərdarlıq verir.\n"
        "`r?warnings` - İstifadəçinin xəbərdarlıq sayına baxır.\n"
        "`r?temizlewarn` - Xəbərdarlıqları tamamilə sıfırlayır.\n"
        "`r?lock` - Kanalı yazışmaya bağlayır.\n"
        "`r?unlock` - Kanalı yenidən yazışmaya açır."
    ), inline=False)

    embed2 = discord.Embed(
        title="👑 YENİLMEZ v6000 - Əmr Məlumatları (Hissə 2)",
        description="Statistika və əyləncə əmrləri:",
        color=0x00aaff
    )
    embed2.add_field(name="📊 Statistika & Məlumat Əmrləri", value=(
        "`r?server` - Serverin ümumi məlumatlarını göstərir.\n"
        "`r?userinfo` - İstifadəçinin profil məlumatını verir.\n"
        "`r?botinfo` - Botun texniki versiyasını göstərir.\n"
        "`r?ping` - İnternet gecikmə sürətini (ms) yoxlayır.\n"
        "`r?online` - Onlayn üzvlərin dəqiq sayını göstərir.\n"
        "`r?level` - Cari səviyyə və XP dəyərini göstərir.\n"
        "`r?rolbilgi` - Rol haqqında ətraflı məlumat verir.\n"
        "`r?kanalbilgi` - Kanalın ID və növünü göstərir.\n"
        "`r?boosters` - Serverə boost verənləri siyahılayır.\n"
        "`r?avatar` - İstifadəçinin profil şəklini böyük açır.\n"
        "`r?banner` - İstifadəçinin banner şəklini göstərir.\n"
        "`r?emojisay` - Serverdəki toplam emoji sayını göstərir.\n"
        "`r?servericon` - Serverin ikon şəklini atır.\n"
        "`r?botping` - Botun daxili cavab sürətini yoxlayır."
    ), inline=False)

    embed2.add_field(name="🎮 Oyunlar & Əyləncə Əmrləri", value=(
        "`r?duel` - Dostunla virtual duel oyununa girirsən.\n"
        "`r?coinflip` - Yazı-tura ataraq bəxtini sınayırsan.\n"
        "`r?slot` - Slot kazino oyunu oynayırsan.\n"
        "`r?iq` - Zarafatla IQ səviyyənizi ölçür.\n"
        "`r?balıq` - Virtual olaraq balıq tutma simulyasiyası.\n"
        "`r?hava` - Şəhər hava proqnozunu öyrənirsən.\n"
        "`r?hesabla` - Bot vasitəsilə riyazi hesablamalar aparırsan.\n"
        "`r?tassaxla` - Zər atma oyunu oynayırsan.\n"
        "`r?sec` - Verilən seçimlər arasında bot seçim edir.\n"
        "`r?8ball` - Sehrli cavab kürəsinə sual verirsən.\n"
        "`r?sevgi` - İki nəfər arasında sevgi faizini hesablayır.\n"
        "`r?hackle` - Zarafatla dostunu hackləmə simulyasiyası.\n"
        "`r?soz` - Motivasiyaedici dəyərli sözlər göndərir.\n"
        "`r?cat` - Maraqlı pişik faktları bölüşür.\n"
        "`r?joke` - Birbirindən gülməli zarafatlar edir.\n"
        "`r?cmk` - Daş, kağız, qayçı oyunu oynayır.\n"
        "`r?ters` - Yazdığın mətni tərsinə çevirir."
    ), inline=False)

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)

# ==============================================================================
# SAHİB ƏMRLƏRİ
# ==============================================================================
@bot.command(name="ticketpanel")
async def ticketpanel(ctx):
    if ctx.author.id != SAHIB_ID or ctx.channel.id != XUSUSI_KANAL_ID: return
    await ctx.message.delete()
    await ctx.send(embed=discord.Embed(title="🎫 Dəstək Paneli", description="Aşağıdakı düyməyə basaraq ticket açın.", color=0x00aaff), view=TicketAc())

@bot.command(name="elan")
async def elan(ctx, *, m):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(embed=discord.Embed(title="📢 ELAN", description=m, color=0xffaa00))

@bot.command(name="anket")
async def anket(ctx, *, s):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    msg = await ctx.send(embed=discord.Embed(title="📊 ANKET", description=s, color=0x00ffcc))
    await msg.add_reaction("👍"); await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, sure: str, *, odul: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    try:
        b, s = sure[-1], int(sure[:-1])
        sn = s * (1 if b=='s' else 60 if b=='m' else 3600 if b=='h' else 86400)
    except: return
    msg = await ctx.send(embed=discord.Embed(title="🎉 ÇƏKİLİŞ", description=f"Ödül: **{odul}**", color=0xff0055))
    await msg.add_reaction("🎉")
    await asyncio.sleep(sn)
    try:
        yeni = await ctx.channel.fetch_message(msg.id)
        users = [u async for r in yeni.reactions if str(r.emoji) == "🎉" async for u in r.users() if not u.bot]
        if users: await ctx.channel.send(f"🏆 Qalib: {random.choice(users).mention}! Ödül: **{odul}**")
        else: await ctx.channel.send("❌ Qoşulan olmadı.")
    except: pass

@bot.command(name="duyuru")
async def duyuru(ctx, *, m):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"🔔 **DUYURU:** {m}")

@bot.command(name="bakim")
async def bakim(ctx, d="açıq"):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send(f"🛠️ Baxım rejimi: **{d}**")

@bot.command(name="slowmode")
async def slowmode(ctx, saniye: int):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Yavaş mod **{saniye}** san oldu!")

@bot.command(name="sayac")
async def sayac(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send(f"📊 Üzv sayı: **{ctx.guild.member_count}**")

@bot.command(name="rolver")
async def rolver(ctx, m: discord.Member, r: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await m.add_roles(r); await ctx.send(f"✅ {m.mention} - **{r.name}** verildi!")

@bot.command(name="rolal")
async def rolal(ctx, m: discord.Member, r: discord.Role):
    if ctx.author.id != SAHIB_ID: return
    await m.remove_roles(r); await ctx.send(f"❌ {m.mention} - **{r.name}** alındı!")

@bot.command(name="botdurdur")
async def botdurdur(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🛑 Bot dayandırılır...")
    await bot.close()

# ==============================================================================
# MODERASİYA ƏMRLƏRİ
# ==============================================================================
@bot.command(name="sil")
async def sil(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.purge(limit=amount + 1)

@bot.command(name="mute")
async def mute(ctx, m: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    r = discord.utils.get(ctx.guild.roles, name="Muted") or await ctx.guild.create_role(name="Muted")
    await m.add_roles(r); await ctx.send(f"🔇 {m.mention} muted!")

@bot.command(name="unmute")
async def unmute(ctx, m: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    r = discord.utils.get(ctx.guild.roles, name="Muted")
    if r: await m.remove_roles(r)
    await ctx.send(f"🔊 {m.mention} unmuted!")

@bot.command(name="ban")
async def ban(ctx, m: discord.Member, *, r=None):
    if ctx.author.id != SAHIB_ID: return
    await m.ban(reason=r); await ctx.send(f"🔨 {m.name} banlandı!")

@bot.command(name="unban")
async def unban(ctx, *, name):
    if ctx.author.id != SAHIB_ID: return
    for entry in await ctx.guild.bans():
        if entry.user.name == name:
            await ctx.guild.unban(entry.user)
            await ctx.send(f"🔓 Unban: {entry.user.name}")
            return

@bot.command(name="kick")
async def kick(ctx, m: discord.Member, *, r=None):
    if ctx.author.id != SAHIB_ID: return
    await m.kick(reason=r); await ctx.send(f"👢 Kick: {m.name}")

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID: return
    pos = ctx.channel.position
    yeni = await ctx.channel.clone()
    await ctx.channel.delete()
    await yeni.edit(position=pos)
    await yeni.send("💥 Kanal sıfırlandı!")

@bot.command(name="warn")
async def warn(ctx, m: discord.Member, *, sebep="Yoxdur"):
    if ctx.author.id != SAHIB_ID: return
    if m.id not in warn_sistemi: warn_sistemi[m.id] = []
    warn_sistemi[m.id].append(sebep)
    await ctx.send(f"⚠️ {m.mention} xəbərdarlıq aldı! Toplam: {len(warn_sistemi[m.id])}")

@bot.command(name="warnings")
async def warnings(ctx, m: discord.Member):
    await ctx.send(f"📌 {m.name} warn sayı: **{len(warn_sistemi.get(m.id, []))}**")

@bot.command(name="temizlewarn")
async def temizlewarn(ctx, m: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    warn_sistemi[m.id] = []
    await ctx.send(f"✨ {m.mention} warnları sıfırlandı!")

@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal kilidləndi!")

@bot.command(name="unlock")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı!")

# ==============================================================================
# STATİSTİKA & MƏLUMAT (HAMI ÜÇÜN)
# ==============================================================================
@bot.command(name="botinfo")
async def botinfo(ctx): await ctx.send("🤖 **YENİLMEZ v6000** | Python & Discord.py")
@bot.command(name="server")
async def server(ctx): await ctx.send(f"🏰 Server: {ctx.guild.name} | Üzv: {ctx.guild.member_count}")
@bot.command(name="userinfo")
async def userinfo(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(f"👤 {u.name} | ID: {u.id}")
@bot.command(name="ping")
async def ping(ctx): await ctx.send(f"🏓 {round(bot.latency * 1000)}ms")
@bot.command(name="online")
async def online(ctx): await ctx.send(f"🟢 Onlayn: {sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)}")
@bot.command(name="level")
async def level(ctx, m: discord.Member = None):
    t = m or ctx.author
    d = user_xp.get(t.id, {"xp": 0, "level": 1})
    await ctx.send(f"⭐ {t.name} | Səviyyə: {d['level']} | XP: {d['xp']}")
@bot.command(name="rolbilgi")
async def rolbilgi(ctx, r: discord.Role): await ctx.send(f"🛡️ Rol: {r.name} | Üzv: {len(r.members)}")
@bot.command(name="kanalbilgi")
async def kanalbilgi(ctx): await ctx.send(f"📁 Kanal: {ctx.channel.name}")
@bot.command(name="boosters")
async def boosters(ctx):
    bs = ctx.guild.premium_subscribers
    await ctx.send(f"🚀 Boost verənlər: {', '.join([b.name for b in bs])}" if bs else "Boost yoxdur.")
@bot.command(name="avatar")
async def avatar(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(u.display_avatar.url)
@bot.command(name="banner")
async def banner(ctx, m: discord.Member = None):
    u = await bot.fetch_user((m or ctx.author).id)
    await ctx.send(u.banner.url if u.banner else "Banner yoxdur.")
@bot.command(name="emojisay")
async def emojisay(ctx): await ctx.send(f"😀 Emoji sayı: {len(ctx.guild.emojis)}")
@bot.command(name="servericon")
async def servericon(ctx): await ctx.send(ctx.guild.icon.url if ctx.guild.icon else "İkon yoxdur.")
@bot.command(name="botping")
async def botping(ctx): await ctx.send(f"⚡ Bot daxili gecikmə: {round(bot.latency * 1000)}ms")

# ==============================================================================
# OYUNLAR & ƏYLƏNCƏ (HAMI ÜÇÜN)
# ==============================================================================
@bot.command(name="duel")
async def duel(ctx, m: discord.Member): await ctx.send(f"⚔️ Duel qalibi: {random.choice([ctx.author, m]).mention}!")
@bot.command(name="coinflip")
async def coinflip(ctx): await ctx.send(f"🎲 {random.choice(['Yazı 🪙', 'Tura 👑'])}")
@bot.command(name="slot")
async def slot(ctx):
    e = ["🍎", "🍋", "🍒", "7️⃣", "💎"]
    a, b, c = random.choice(e), random.choice(e), random.choice(e)
    await ctx.send(f"🎰 [{a} | {b} | {c}]\n" + ("🎉 UDDUNUZ!" if a==b==c else "❌ Uduzdunuz!"))
@bot.command(name="iq")
async def iq(ctx, m: discord.Member = None): await ctx.send(f"🧠 IQ: {random.randint(50, 160)}")
@bot.command(name="balıq")
async def balıq(ctx): await ctx.send(f"🎣 Tutdun: {random.choice(['🐟 Balıq', '🐠 Qızıl Balıq', '🦈 Akula', '👞 Başmaq'])}")
@bot.command(name="hava")
async def hava(ctx, *, s="Bakı"): await ctx.send(f"🌤️ {s}: {random.randint(18, 35)}°C")
@bot.command(name="hesabla")
async def hesabla(ctx, *, i):
    try: await ctx.send(f"🧮 {eval(i)}")
    except: await ctx.send("❌ Xəta!")
@bot.command(name="tassaxla")
async def tassaxla(ctx): await ctx.send(f"🎲 Zər: {random.randint(1, 6)}")
@bot.command(name="sec")
async def sec(ctx, *, l): await ctx.send(f"🎯 Seçimim: {random.choice(l.split(',')).strip()}")
@bot.command(name="8ball")
async def eightball(ctx, *, s): await ctx.send(f"🔮 {random.choice(['Bəli', 'Xeyir', 'Bəlkə'])}")
@bot.command(name="sevgi")
async def sevgi(ctx, m: discord.Member): await ctx.send(f"❤️ Uyğunluq: %{random.randint(10, 100)}")
@bot.command(name="hackle")
async def hackle(ctx, m: discord.M
