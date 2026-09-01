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

bot = commands.Bot(command_prefix="r?", intents=intents)

SAHIB_ID = 641014966312501259

user_xp = {}
spam_takip = {}
interaction_spam = {}
warn_sistemi = {}

@bot.event
async def on_ready():
    print(f"Bot ise dusdu: {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="r?bot | Aktivdir 👑"))
    stats_update.start()
    voice_xp_loop.start()

@bot.event
async def on_reaction_add(reaction, user):
    if user.id == SAHIB_ID:
        try:
            await reaction.message.add_reaction(reaction.emoji)
        except:
            pass

@bot.event
async def on_member_join(member):
    kanal = discord.utils.get(member.guild.text_channels, name="gelen-geden") or member.guild.system_channel
    if kanal:
        embed = discord.Embed(title="🎉 Yeni Uzv!", description=f"Salam {member.mention}, xos geldin! Uzv sayi: **{member.guild.member_count}**", color=0x00ff88)
        await kanal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    kanal = discord.utils.get(member.guild.text_channels, name="gelen-geden") or member.guild.system_channel
    if kanal:
        await kanal.send(f"👋 **{member.name}** serverden ayrildi.")

@bot.event
async def on_interaction(interaction):
    if interaction.user.id == SAHIB_ID:
        return
    
    uid = interaction.user.id
    sindi = time.time()
    if uid not in interaction_spam:
        interaction_spam[uid] = []
    
    interaction_spam[uid] = [t for t in interaction_spam[uid] if sindi - t < 4]
    interaction_spam[uid].append(sindi)
    
    if len(interaction_spam[uid]) >= 4:
        try:
            await interaction.response.send_message("⚠️ Çox sürətli əmr yazırsan, spam etdiyinə görə dayandırıldı!", ephemeral=True)
            return
        except:
            pass

@tasks.loop(minutes=10)
async def stats_update():
    for guild in bot.guilds:
        try:
            toplam = guild.member_count
            online = sum(1 for m in guild.members if m.status != discord.Status.offline)
            ses = sum(len(vc.members) for vc in guild.voice_channels)
            for ch in guild.channels:
                if "Uzv:" in ch.name: 
                    await ch.edit(name=f"📊 Uzv: {toplam}")
                elif "Onlayn:" in ch.name: 
                    await ch.edit(name=f"🟢 Onlayn: {online}")
                elif "Ses:" in ch.name: 
                    await ch.edit(name=f"🔊 Ses: {ses}")
        except: 
            pass

@tasks.loop(minutes=1)
async def voice_xp_loop():
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if len(vc.members) > 1:
                for m in vc.members:
                    if m.bot: 
                        continue
                    if m.id not in user_xp: 
                        user_xp[m.id] = {"xp": 0, "level": 1}
                    user_xp[m.id]["xp"] += 15
                    
                    while user_xp[m.id]["xp"] >= user_xp[m.id]["level"] * 100:
                        user_xp[m.id]["xp"] -= user_xp[m.id]["level"] * 100
                        user_xp[m.id]["level"] += 1

@bot.event
async def on_message(message):
    if message.author.bot: 
        return

    aid = message.author.id
    sindi = time.time()
    if aid not in user_xp: 
        user_xp[aid] = {"xp": 0, "level": 1}
    
    user_xp[aid]["xp"] += 15
    
    while user_xp[aid]["xp"] >= user_xp[aid]["level"] * 100:
        user_xp[aid]["xp"] -= user_xp[aid]["level"] * 100
        user_xp[aid]["level"] += 1
        try: 
            await message.channel.send(f"🎉 Tebrikler {message.author.mention}, Seviyye **{user_xp[aid]['level']}** oldun!")
        except: 
            pass

    if aid != SAHIB_ID:
        if aid not in spam_takip: 
            spam_takip[aid] = []
        spam_takip[aid] = [t for t in spam_takip[aid] if sindi - t < 4]
        spam_takip[aid].append(sindi)
        if len(spam_takip[aid]) >= 5:
            try:
                await message.channel.purge(limit=6)
                await message.author.timeout(discord.utils.utcnow() + discord.timedelta(minutes=3), reason="Spam")
                await message.channel.send(f"⚠️ {message.author.mention}, spam etdiyin ucun 3 deqiqelik mute aldin!", delete_after=5)
                spam_takip[aid] = []
                return
            except: 
                pass

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Cox tez-tez yazirsan! {round(error.retry_after, 1)} saniye sonra yoxla.", delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Eskik arqument! Emri tam yaz.", delete_after=6)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu emr ucun selahiyyetin catmir!", delete_after=6)
    else:
        pass

class TicketKapat(discord.ui.View):
    @discord.ui.button(label="🔒 Ticketi Bagla", style=discord.ButtonStyle.danger, custom_id="t_kapat")
    async def kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Kanal silinir...", ephemeral=False)
        await asyncio.sleep(5)
        try: 
            await interaction.channel.delete()
        except: 
            pass

class TicketAc(discord.ui.View):
    @discord.ui.button(label="🎫 Ticket Ac", style=discord.ButtonStyle.success, custom_id="t_ac")
    async def ac(self, interaction: discord.Interaction, button: discord.ui.Button):
        g, author = interaction.guild, interaction.user
        overwrites = {
            g.default_role: discord.PermissionOverwrite(view_channel=False),
            author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            g.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
        }
        ch = await g.create_text_channel(f"ticket-{author.name}", overwrites=overwrites)
        await ch.send(f"Salam {author.mention}, destek buradadir.", view=TicketKapat())
        await interaction.response.send_message(f"✅ Kanal acildi: {ch.mention}", ephemeral=True)

@bot.command(name="bot")
async def bot_komanda(ctx):
    if ctx.author.id != SAHIB_ID: 
        return
    
    embed1 = discord.Embed(title="👑 YENILMEZ v6000 - Emr Paneli (Hisse 1)", description="Idareetme ve Moderasiya emrleri:", color=0xffa200)
    embed1.add_field(name="👑 Sahib & Idareetme", value=(
        "`r?bot` - Emr panelini acir\n"
        "`r?ticketyarat` - Destek ticket sistemi yaradir\n"
        "`r?elan` - Serverde elan verir\n"
        "`r?anket` - Sesverme anketi acir\n"
        "`r?cekilis` - Hediyye cekilisi basladir\n"
        "`r?duyuru` - Qısa duyuru atir\n"
        "`r?bakim` - Baxim rejimini deyisir\n"
        "`r?slowmode` - Kanala yavas mod qoyur\n"
        "`r?sayac` - Uzv sayini gosterir\n"
        "`r?rolver` / `r?rolal` - Rol verir ve ya alir\n"
        "`r?botdurdur` - Botu tamamiyle baglayir"
    ), inline=False)
    
    embed1.add_field(name="🛡️ Moderasiya", value=(
        "`r?sil` - Yazilan miqdarda mesaj silir\n"
        "`r?mute` / `r?unmute` - Istifadeciye ses qadagasi qoyur\n"
        "`r?ban` / `r?unban` - Istifadecini banlayir\n"
        "`r?kick` - Istifadecini serverden qovur\n"
        "`r?nuke` - Kanali tamamilə sifirlayir\n"
        "`r?warn` / `r?warnings` - Xeberdarliq verir ve baxir\n"
        "`r?temizlewarn` - Xeberdarliqlari silir\n"
        "`r?lock` / `r?unlock` - Kanali kilidleyir ve acir"
    ), inline=False)

    embed2 = discord.Embed(title="👑 YENILMEZ v6000 - Emr Paneli (Hisse 2)", description="Statistika ve Eylence emrleri:", color=0x00aaff)
    embed2.add_field(name="📊 Statistika & Melumat", value=(
        "`r?server` - Server haqqinda melumat verir\n"
        "`r?userinfo` - Istifadeci profiline baxir\n"
        "`r?botinfo` - Bot haqqinda melumat\n"
        "`r?ping` - Botun internet gecikmesini olcdu\n"
        "`r?online` - Onlayn istifadeci sayi\n"
        "`r?level` - Seviyye ve XP melumatina baxir\n"
        "`r?rolbilgi` - Rol haqda melumat verir\n"
        "`r?kanalbilgi` - Cari kanal haqda melumat\n"
        "`r?boosters` - Serveri boost edenler\n"
        "`r?avatar` - Istifadecinin avatarini gosterir\n"
        "`r?banner` - Istifadecinin bannerini gosterir\n"
        "`r?emojisay` - Serverdeki emojilerin sayi\n"
        "`r?servericon` - Serverin seklini gosterir"
    ), inline=False)

    embed2.add_field(name="🎮 Oyunlar & Eylence", value=(
        "`r?duel` - Rastgele duel atir\n"
        "`r?coinflip` - Yazi-tura atir\n"
        "`r?slot` - Kazino oyunu oynayir\n"
        "`r?iq` - IQ dereceni olcdu\n"
        "`r?baliq` - Baliq tutma oyunu\n"
        "`r?hava` - Hava proqnozunu gosterir\n"
        "`r?hesabla` - Riyazi emeliyyat aparir\n"
        "`r?tassaxla` - Zer atir\n"
        "`r?sec` - Secim etdiresen\n"
        "`r?8ball` - Sehrli kureye sual ver\n"
        "`r?sevgi` - Sevgi faizini olcdu\n"
        "`r?hackle` - Zarafatla hackleyir\n"
        "`r?soz` - Maraqli sozler deyir\n"
        "`r?cat` - Pisik fakti paylasir\n"
        "`r?joke` - Zarafat danisir\n"
        "`r?cmk` - Das-kagiz-qayci oynayir\n"
        "`r?ters` - Metni tersine cevirir\n"
        "`r?sohbet` - Botla sohbet edir\n"
        "`r?date` - Bu gunki tarixi gosterir"
    ), inline=False)

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)

@bot.command(name="ticketyarat")
@commands.cooldown(1, 10, commands.BucketType.user)
async def ticketyarat(ctx):
    try: 
        await ctx.message.delete()
    except: 
        pass
    await ctx.send(embed=discord.Embed(title="🎫 Destek Paneli", description="Asagidaki duymeye basaraq ticket acin.", color=0x00aaff), view=TicketAc())

@bot.command(name="elan")
async def elan(ctx, *, m="Elan metni yoxdur"):
    if ctx.author.id != SAHIB_ID: 
        return
    try: 
        await ctx.message.delete()
    except: 
        pass
    await ctx.send(embed=discord.Embed(title="📢 ELAN", description=m, color=0xffaa00))

@bot.command(name="anket")
async def anket(ctx, *, s="Anket suali yoxdur"):
    if ctx.author.id != SAHIB_ID: 
        return
    try: 
        await ctx.message.delete()
    except: 
        pass
    msg = await ctx.send(embed=discord.Embed(title="📊 ANKET", description=s, color=0x00ffcc))
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, sure: str = "1m", *, odul: str = "Hediyye"):
    if ctx.author.id != SAHIB_ID: 
        return
    try: 
        await ctx.message.delete()
    except: 
        pass
    try:
        b, s = sure[-1], int(sure[:-1])
        sn = s * (1 if b=='s' else 60 if b=='m' else 3600 if b=='h' else 86400)
    except: 
        sn = 60
    msg = await ctx.send(embed=discord.Embed(title="🎉 CEKILIS", description=f"Odul: **{odul}**", color=0xff0055))
    await msg.add_reaction("🎉")
    await asyncio.sleep(sn)
    try:
        yeni = await ctx.channel.fetch_message(msg.id)
        users = [u async for r in yeni.reactions if str(r.emoji) == "🎉" async for u in r.users() if not u.bot]
        if users: 
            qalib = random.choice(users)
            await ctx.channel.send(f"🏆 Qalib: {qalib.mention}! Odul: **{odul}**")
        else: 
            await ctx.channel.send("❌ Qosulan olmadi.")
    except: 
        pass

@bot.command(name="duyuru")
async def duyuru(ctx, *, m="Duyuru"):
    if ctx.author.id != SAHIB_ID: 
        return
    try: 
        await ctx.message.delete()
    except: 
        pass
    await ctx.send(f"🔔 **DUYURU:** {m}")

@bot.command(name="bakim")
async def bakim(ctx, d="aciq"):
    if ctx.author.id != SAHIB_ID: 
        return
    await ctx.send(f"🛠️ Baxim rejimi: **{d}**")

@bot.command(name="slowmode")
async def slowmode(ctx, saniye: int = 0):
    if ctx.author.id != SAHIB_ID: 
        return
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Yavas mod **{saniye}** san oldu!")

@bot.command(name="sayac")
async def sayac(ctx):
    if ctx.author.id != SAHIB_ID: 
        return
    await ctx.send(f"📊 Uzv sayi: **{ctx.guild.member_count}**")

@bot.command(name="rolver")
async def rolver(ctx, m: discord.Member, r: discord.Role):
    if ctx.author.id != SAHIB_ID: 
        return
    await m.add_roles(r)
    await ctx.send(f"✅ {m.mention} - **{r.name}** verildi!")

@bot.command(name="rolal")
async def rolal(ctx, m: discord.Member, r: discord.Role):
    if ctx.author.id != SAHIB_ID: 
        return
    await m.remove_roles(r)
    await ctx.send(f"❌ {m.mention} - **{r.name}** alindi!")

@bot.command(name="botdurdur")
async def botdurdur(ctx):
    if ctx.author.id != SAHIB_ID: 
        return
    await ctx.send("🛑 Bot dayandirilir...")
    await bot.close()

@bot.command(name="sil")
async def sil(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID: 
        return
    await ctx.channel.purge(limit=amount + 1)

@bot.command(name="mute")
async def mute(ctx, m: discord.Member):
    if ctx.author.id != SAHIB_ID: 
        return
    r = discord.utils.get(ctx.guild.roles, name="Muted") or await ctx.guild.create_role(name="Muted")
    await m.add_roles(r)
    await ctx.send(f"🔇 {m.mention} muted!")

@bot.command(name="unmute")
async def unmute(ctx, m: discord.Member):
    if ctx.author.id != SAHIB_ID: 
        return
    r = discord.utils.get(ctx.guild.roles, name="Muted")
    if r: 
        await m.remove_roles(r)
    await ctx.send(f"🔊 {m.mention} unmuted!")

@bot.command(name="ban")
async def ban(ctx, m: discord.Member, *, r="Sebeb gosterilmeyib"):
    if ctx.author.id != SAHIB_ID: 
        return
    await m.ban(reason=r)
    await ctx.send(f"🔨 {m.name} banlandi!")

@bot.command(name="unban")
async def unban(ctx, *, name=""):
    if ctx.author.id != SAHIB_ID: 
        return
    for entry in await ctx.guild.bans():
        if entry.user.name.lower() in name.lower():
            await ctx.guild.unban(entry.user)
            await ctx.send(f"🔓 Unban: {entry.user.name}")
            return
    await ctx.send("❌ Istifadeci tapilmadi.")

@bot.command(name="kick")
async def kick(ctx, m: discord.Member, *, r="Sebeb yoxdur"):
    if ctx.author.id != SAHIB_ID: 
        return
    await m.kick(reason=r)
    await ctx.send(f"👢 Kick: {m.name}")

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID: 
        return
    pos = ctx.channel.position
    yeni = await ctx.channel.clone()
    await ctx.channel.delete()
    await yeni.edit(position=pos)
    await yeni.send("💥 Kanal sifirlandi!")

@bot.command(name="warn")
async def warn(ctx, m: discord.Member, *, sebep="Yoxdur"):
    if ctx.author.id != SAHIB_ID: 
        return
    if m.id not in warn_sistemi: 
        warn_sistemi[m.id] = []
    warn_sistemi[m.id].append(sebep)
    await ctx.send(f"⚠️ {m.mention} xeberdarliq aldi! Toplam: {len(warn_sistemi[m.id])}")

@bot.command(name="warnings")
async def warnings(ctx, m: discord.Member = None):
    t = m or ctx.author
    await ctx.send(f"📌 {t.name} warn sayi: **{len(warn_sistemi.get(t.id, []))}**")

@bot.command(name="temizlewarn")
async def temizlewarn(ctx, m: discord.Member):
    if ctx.author.id != SAHIB_ID: 
        return
    warn_sistemi[m.id] = []
    await ctx.send(f"✨ {m.mention} warnlari sifirlandi!")

@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.id != SAHIB_ID: 
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal kilidlendi!")

@bot.command(name="unlock")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID: 
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal acildi!")

@bot.command(name="botinfo")
async def botinfo(ctx): 
    await ctx.send("🤖 **YENILMEZ v6000** | Python & Discord.py")

@bot.command(name="server")
async def server(ctx): 
    await ctx.send(f"🏰 Server: {ctx.guild.name} | Uzv: {ctx.guild.member_count}")

@bot.command(name="userinfo")
async def userinfo(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(f"👤 Istifadeci: {u.name} | ID: {u.id}")

@bot.command(name="ping")
async def ping(ctx): 
    await ctx.send(f"🏓 Gecikme: {round(bot.latency * 1000)}ms")

@bot.command(name="online")
async def online(ctx): 
    await ctx.send(f"🟢 Onlayn: {sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)}")

@bot.command(name="level")
async def level(ctx, m: discord.Member = None):
    t = m or ctx.author
    d = user_xp.get(t.id, {"xp": 0, "level": 1})
    await ctx.send(f"⭐ {t.name} | Seviyye: {d['level']} | XP: {d['xp']}")

@bot.command(name="rolbilgi")
async def rolbilgi(ctx, r: discord.Role): 
    await ctx.send(f"🛡️ Rol: {r.name} | Uzv: {len(r.members)}")

@bot.command(name="kanalbilgi")
async def kanalbilgi(ctx): 
    await ctx.send(f"📁 Kanal: {ctx.channel.name}")

@bot.command(name="boosters")
async def boosters(ctx):
    bs = ctx.guild.premium_subscribers
    if bs:
        boost_names = ", ".join([b.name for b in bs])
        await ctx.send(f"🚀 Boost verenler: {boost_names}")
    else:
        await ctx.send("Boost yoxdur.")

@bot.command(name="avatar")
async def avatar(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(u.display_avatar.url)

@bot.command(name="banner")
async def banner(ctx, m: discord.Member = None):
    try:
        u = await bot.fetch_user((m or ctx.author).id)
        if u.banner:
            await ctx.send(u.banner.url)
        else:
            await ctx.send("Banner yoxdur.")
    except: 
        await ctx.send("Banner tapilmadi.")

@bot.command(name="emojisay")
async def emojisay(ctx): 
    await ctx.send(f"😀 Emoji sayi: {len(ctx.guild.emojis)}")

@bot.command(name="servericon")
async def servericon(ctx): 
    if ctx.guild.icon:
        await ctx.send(ctx.guild.icon.url)
    else:
        await ctx.send("Ikon yoxdur.")

@bot.command(name="duel")
async def duel(ctx, m: discord.Member = None):
    target = m.mention if m else "Dost"
    secim = random.choice([ctx.author.mention, target])
    await ctx.send(f"⚔️ Duel qalibi: {secim}!")

@bot.command(name="coinflip")
async def coinflip(ctx): 
    netice = random.choice(['Yazi 🪙', 'Tura 👑'])
    await ctx.send(f"🎲 Netice: {netice}")

@bot.command(name="slot")
async def slot(ctx):
    e = ["🍎", "🍋", "🍒", "7️⃣", "💎"]
    a, b, c = random.choice(e), random.choice(e), random.choice(e)
    durum = "🎉 UDDUNUZ!" if a == b == c else "❌ Uduzdunuz!"
    await ctx.send(f"🎰 [{a} | {b} | {c}]\n{durum}")

@bot.command(name="iq")
async def iq(ctx, m: discord.Member = None):
    t = m or ctx.author
    sayi = random.randint(50, 160)
    await ctx.send(f"🧠 {t.name} IQ seviyyesi: {sayi}")

@bot.command(name="baliq")
async def baliq(ctx): 
    baliqlar = ['🐟 Baliq', '🐠 Qizil Baliq', '🦈 Akula', '👞 Basmaq']
    tutulan = random.choice(baliqlar)
    await ctx.send(f"🎣 Tutdun: {tutulan}")

@bot.command(name="hava")
async def hava(ctx, *, s="Baki"): 
    derece = random.randint(18, 35)
    await ctx.send(f"🌤️ Hava ({s}): {derece}°C")

@bot.command(name="hesabla")
async def hesabla(ctx, *, i="2+2"):
    try: 
        netice = eval(i)
        await ctx.send(f"🧮 Netice: {netice}")
    except: 
        await ctx.send("❌ Riyazi xeta!")

@bot.command(name="tassaxla")
async def tassaxla(ctx): 
    zer = random.randint(1, 6)
    await ctx.send(f"🎲 Zer: {zer}")

@bot.command(name="sec")
async def sec(ctx, *, l="Beli, Xeyir"): 
    secim = random.choice(l.split(',')).strip()
    await ctx.send(f"🎯 Secimim: {secim}")

@bot.command(name="8ball")
async def eightball(ctx, *, s="Sual"): 
    cavablar = ['Beli', 'Xeyir', 'Belke de', 'Mutleq']
    cavab = random.choice(cavablar)
    await ctx.send(f"🔮 Sehrli kure: {cavab}")

@bot.command(name="sevgi")
async def sevgi(ctx, m: discord.Member = None):
    target = m.mention if m else "Kimse"
    faiz = random.randint(10, 100)
    await ctx.send(f"❤️ {ctx.author.mention} ve {target} uygunlugu: %{faiz}")

@bot.command(name="hackle")
async def hackle(ctx, m: discord.Member = None):
    target = m.mention if m else "Dost"
    await ctx.send(f"💻 {target} ugurla hacklendi! Parol: `12345`")

@bot.command(name="soz")
async def soz(ctx): 
    sozler = ['Ugur qetiyyetlidir.', 'Daim ireli!', 'Zehmet cekmeden hec ne olmur.']
    secilen_soz = random.choice(sozler)
    await ctx.send(f"📜 Soz: {secilen_soz}")

@bot.command(name="cat")
async def cat(ctx): 
    await ctx.send("🐱 Pisik fakti: Omrunun 70 faizini yatmaqla kecirirler.")

@bot.command(name="joke")
async def joke(ctx): 
    await ctx.send("🎭 Zarafat: - Muellim, asagidan yazin basa dusmurem. - Asagi yer yoxdur!")

@bot.command(name="cmk")
async def cmk(ctx): 
    secimler = ['Das 🪨', 'Kagiz 📄', 'Qayci ✂️']
    secim = random.choice(secimler)
    await ctx.send(f"🎮 Das-Kagiz-Qayci: {secim}")

@bot.command(name="ters")
async def ters(ctx, *, yazi="Salam"): 
    await ctx.send(yazi[::-1])

@bot.command(name="sohbet")
async def sohbet(ctx): 
    await ctx.send("💬 Nesesen, qardas? Isler nece gedir?")

@bot.command(name="date")
async def date(ctx):
    bugun = time.strftime("%d.%m.%Y")
    await ctx.send(f"📅 Bu gun: {bugun}")

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if token: 
        bot.run(token)
        
