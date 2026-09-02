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
TICKET_KANAL_ID = 0  # Bura öz kanal ID-ni yazarsan

user_xp = {}
spam_takip = {}
interaction_span = {}
warn_sistemi = {}

@bot.event
async def on_ready():
    print(f"Bot Ise dusdu: {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="r?bot | Aktifdir 👑"))
    state_update.start()
    voice_xp_loop.start()

@bot.event
async def on_reaction_add(reaction, user):
    if user.id == SAHIB_ID:
        try:
            await reaction.message.add_reaction(reaction.emoji)
        except:
            pass

@bot.event
async def on_interaction(interaction):
    if interaction.user.id == SAHIB_ID:
        return

    uid = interaction.user.id
    sindi = time.time()
    if uid not in interaction_span:
        interaction_span[uid] = []

    interaction_span[uid] = [t for t in interaction_span[uid] if sindi - t < 4]
    interaction_span[uid].append(sindi)

    if len(interaction_span[uid]) >= 4:
        try:
            await interaction.response.send_message("⚠️ Çok suretli emr yazırsan, bpde etdiyinə görə dayandırıldı.", ephemeral=True)
            return
        except:
            pass

@tasks.loop(minutes=10)
async def state_update():
    for guild in bot.guilds:
        try:
            toplam = guild.member_count
            online = sum(1 for m in guild.members if m.status != discord.Status.offline)
            ses = sum(len(vc.members) for vc in guild.voice_channels)
            for ch in guild.channels:
                if "Uv" in ch.name:
                    await ch.edit(name=f"👥 Uye: {toplam}")
                elif "Online" in ch.name:
                    await ch.edit(name=f"🟢 Online: {online}")
                elif "Ses" in ch.name:
                    await ch.edit(name=f"🔊 Ses: {ses}")
        except:
            pass

@tasks.loop(minutes=2)
async def voice_xp_loop():
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if len(vc.members) > 1:
                for m in vc.members:
                    if m.bot:
                        continue
                    if m.id not in user_xp:
                        user_xp[m.id] = {"xp": 0, "level": 1}
                    user_xp[m.id]["xp"] += 10
                    
                    gerekli_xp = user_xp[m.id]["level"] * 100
                    if user_xp[m.id]["xp"] >= gerekli_xp:
                        user_xp[m.id]["xp"] -= gerekli_xp
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
    gerekli_xp = user_xp[aid]["level"] * 100
    if user_xp[aid]["xp"] >= gerekli_xp:
        user_xp[aid]["xp"] -= gerekli_xp
        user_xp[aid]["level"] += 1
        try:
            await message.channel.send(f"🎉 Tebrikler {message.author.mention}, Seviyye **{user_xp[aid]['level']}** oldun!")
        except:
            pass

    if aid != SAHIB_ID:
        if aid not in spam_takip:
            span_takip_list = []
        else:
            span_takip_list = spam_takip[aid]

        span_takip_list = [t for t in span_takip_list if sindi - t < 4]
        span_takip_list.append(sindi)
        spam_takip[aid] = span_takip_list

        if len(span_takip_list) >= 5:
            try:
                await message.channel.purge(limit=1)
                await message.author.timeout(discord.utils.utcnow() + discord.timedelta(minutes=3), reason="Span")
                await message.channel.send(f"⚠️ {message.author.mention}, spam etdiyin ucun 3 deqiqelik mute aldın!", delete_after=5)
            except:
                pass
            return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Cox tez-tez yazırsan! {round(error.retry_after, 1)} saniye sonra yoxla.", delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Eskik argument! Ecri tam yaz.", delete_after=5)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu emr ucun selahiyyetin catmır", delete_after=5)
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
        
        kategori = discord.utils.get(g.categories, name="TICKETLER")
        if not kategori:
            kategori = await g.create_category("TICKETLER")

        overwrites = {
            g.default_role: discord.PermissionOverwrite(view_channel=False),
            author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            g.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
        }
        
        ch = await g.create_text_channel(f"ticket-{author.name}", category=kategori, overwrites=overwrites)
        await ch.send(f"Salam {author.mention}, destek buradadir.", view=TicketKapat())
        await interaction.response.send_message(f"✅ Kanal acildi: {ch.mention}", ephemeral=True)

@bot.command(name="bot")
async def bot_komanda(ctx):
    if ctx.author.id != SAHIB_ID:
        return

    embed = discord.Embed(title="✨ YENILMEZ v6000 - Enr Paneli (Hisse 1)", description="Idareetme ve Moderasıya emrleri:", color=0x00ffcc)
    embed.add_field(name="👑 Sahib & Idareetme", value=(
        "`r?bot` - Ekr panelini acir\n"
        "`r?ticketyarat` - Destek ticket sistemi yaradir\n"
        "`r?elan` - Serverde elan veriris\n"
        "`r?anket` - Sesverme anketi acirin\n"
        "`r?cekilis` - Hediye cekilisi basladir\n"
        "`r?duyuru` - Qisa duyuru acir\n"
        "`r?bakin` - Baxis rejimini deyisirin\n"
        "`r?slowmode` - Kanala yavas mod qoyuyur\n"
        "`r?sayac` - Uye sayini gosterir\n"
        "`r?rolver` - Rol verir ve ya alir\n"
        "`r?botdurdur` - Botu tamamiyle baglayir"
    ), inline=False)
    
    embed.add_field(name="🛠️ Moderasıya", value=(
        "`r?sil` - Yazilare miqdara mesaj silir\n"
        "`r?mute` - Istifadeciye ses qadagasi qoyur\n"
        "`r?unmute` - Istifadecini baxlayire\n"
        "`r?kick` - Istifadecini serverden qovur\n"
        "`r?warn` - Kanali tamamiyle sifirlayir\n"
        "`r?warnings` - Keberdarliq verir ve hazir\n"
        "`r?temizlewarn` - Keberdarliqlari silir\n"
        "`r?lock` - Kanali kilidleyir ve acir"
    ), inline=False)

    embed2 = discord.Embed(title="✨ YENILMEZ v6000 - Enr Paneli (Hisse 2)", description="Statistika ve Eylence emrleri:", color=0x00ffcc)
    embed2.add_field(name="📊 Statistika & Melumat", value=(
        "`r?server` - Server haqqinda melumat veririn\n"
        "`r?userinfo` - Istifadeci profiline baxirin\n"
        "`r?botinfo` - Bot haqqinda melumat\n"
        "`r?ping` - Botun internat gecikmesini olcduir\n"
        "`r?online` - Onlayn istifadeci sayirin\n"
        "`r?level` - Seviyye ve XP melumatina baxirin\n"
        "`r?rolbilgi` - Rol haqqinda melumat veririn\n"
        "`r?kanalbilgi` - Cari kanal haqda melumat\n"
        "`r?boosters` - Serveri Boost edenlerin\n"
        "`r?avatar` - Istifadecinin avatarini gosterir\n"
        "`r?banner` - Istifadecinin bannerini gosterir\n"
        "`r?emojisay` - Serverdeki emojilerin sayin\n"
        "`r?servericon` - Serverin seklini gosterir"
    ), inline=False)

    embed2.add_field(name="🎮 Oyunlar & Eylence", value=(
        "`r?duel` - Rastgele duel atirin\n"
        "`r?coinflip` - Yazi-tura atirin\n"
        "`r?slot` - Kazino oyunu oynayir\n"
        "`r?iq` - IQ derecemi olcduvu\n"
        "`r?baliq` - Baliq tutma oyunvu\n"
        "`r?hava` - Hava proqnozunu gosteririn\n"
        "`r?hesabla` - Riyazi emeliyyat aparirin\n"
        "`r?tassaxla` - Zer atirin\n"
        "`r?sec` - Secim etdirenesin\n"
        "`r?8ball` - Sehrli kureye sual verin\n"
        "`r?sevgi` - Sevgi faizini olduu\n"
        "`r?hackle` - Zarafatla hackleyin\n"
        "`r?soz` - Maraqli sozler deyirin\n"
        "`r?cat` - Pisik fakti paylasirin\n"
        "`r?joke` - Zarafat danisirin\n"
        "`r?qsk` - Das-Kagiz-Qayci oynayirin\n"
        "`r?ters` - Metni tersine cevireirin\n"
        "`r?sohbet` - Botla sohbet edirin\n"
        "`r?date` - Bu gunki tarixi gosterir"
    ), inline=False)

    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)

@bot.command(name="ticketyarat")
@commands.cooldown(1, 10, commands.BucketType.user)
async def ticketyarat(ctx):
    if TICKET_KANAL_ID != 0 and ctx.channel.id != TICKET_KANAL_ID:
        return await ctx.send(f"❌ Bu komanda yalnız təyin olunmuş dəstək kanalında işləyə bilər!", delete_after=5)
    
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(embed=discord.Embed(title="🎫 Destek Paneli", description="Asagidaki duymeye basaraq ticket acin.", color=0x00aaff), view=TicketAc())

@bot.command(name="elan")
async def elan(ctx, *, s="Elan metni yoxdur"):
    if ctx.author.id != SAHIB_ID:
        return
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(embed=discord.Embed(title="📢 ELAN", description=s, color=0xff0000))

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
async def cekilis(ctx, sure: str = "1m", odul: str = "Hediye"):
    if ctx.author.id != SAHIB_ID:
        return
    try:
        await ctx.message.delete()
    except:
        pass
    
    try:
        b, s = sure[:-1], int(sure[-1])
        sn = s * (1 if b == 's' else 60 if b == 'm' else 3600 if b == 'h' else 86400)
    except:
        sn = 60

    msg = await ctx.send(embed=discord.Embed(title="🎉 CEKILIS", description=f"Odul: **{odul}**", color=0xff0055))
    await msg.add_reaction("🎉")
    await asyncio.sleep(sn)

    try:
        yeni = await ctx.channel.fetch_message(msg.id)
        users = [u async for r in yeni.reactions if str(r.emoji) == "🎉" for u in r.users() if not u.bot]
        if users:
            qalib = random.choice(users)
            await ctx.channel.send(f"🏆 Qalib: {qalib.mention}! Odul: **{odul}**")
        else:
            await ctx.channel.send("❌ Qosulan olmadi.")
    except:
        pass

@bot.command(name="duyuru")
async def duyuru(ctx, *, e="Duyuru"):
    if ctx.author.id != SAHIB_ID:
        return
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(f"🔔 DUYURU: **{e}**")

@bot.command(name="bakin")
async def bakin(ctx, d="aciq"):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.send(f"🔧 Baxis rejimi: **{d}**")

@bot.command(name="slowmode")
async def slowmode(ctx, saniye: int = 0):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Yavas mod **{saniye}** san oldu.")

@bot.command(name="sayac")
async def sayac(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.send(f"👥 Uye sayi: **{ctx.guild.member_count}**")

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
    await ctx.channel.purge(limit=amount)

@bot.command(name="mute")
async def mute(ctx, m: discord.Member, n="Sebeb yoxdur"):
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
    async for entry in ctx.guild.bans():
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
    await ctx.send(f"⚠️ {t.name} warn sayi: {len(warn_sistemi.get(t.id, []))}")

@bot.command(name="temizlewarn")
async def temizlewarn(ctx, m: discord.Member):
    if ctx.author.id != SAHIB_ID:
        return
    warn_sistemi[m.id] = []
    await ctx.send(f"✅ {m.mention} warnlari sifirlandi!")

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
    await ctx.send("🤖 YENILMEZ v6000 | Python & Discord.py")

@bot.command(name="server")
async def server(ctx):
    await ctx.send(f"🏰 Server: {ctx.guild.name} | Uye: {ctx.guild.member_count}")

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
    await ctx.send(f"🛡️ Rol: {r.name} | Uye: {len(r.members)}")

@bot.command(name="kanalbilgi")
async def kanalbilgi(ctx):
    await ctx.send(f"📺 Kanal: {ctx.channel.name}")

@bot.command(name="boosters")
async def boosters(ctx):
    bs = ctx.guild.premium_subscribers
    if bs:
        boost_names = ", ".join([b.name for b in bs])
        await ctx.send(f"🚀 Boost verenler: {boost_names}")
    else:
        await ctx.send("❌ Boost yoxdur.")

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
            await ctx.send("❌ Banner yoxdur.")
    except:
        await ctx.send("❌ Banner tapilmadi.")

@bot.command(name="emojisay")
async def emojisay(ctx):
    await ctx.send(f"😀 Emojilerin sayi: {len(ctx.guild.emojis)}")

@bot.command(name="servericon")
async def servericon(ctx):
    if ctx.guild.icon:
        await ctx.send(ctx.guild.icon.url)
    else:
        await ctx.send("❌ Ikon yoxdur.")

@bot.command(name="duel")
async def duel(ctx, m: discord.Member = None):
    target = m.mention if m else "Dost"
    secim = random.choice([ctx.author.mention, target])
    await ctx.send(f"⚔️ Duel qalibi: {secim}!")

@bot.command(name="coinflip")
async def coinflip(ctx):
    netice = random.choice(["Yazi 🪙", "Tura 👑"])
    await ctx.send(f"🪙 Netice: {netice}")

@bot.command(name="slot")
async def slot(ctx):
    e = ['🍎', '🍌', '🍒', '💎', '🔔']
    a, b, c = random.choice(e), random.choice(e), random.choice(e)
    durum = "🎉 UDUDUNUZ!" if a == b == c else "❌ Uduzdunuz."
    await ctx.send(f"slot: | {a} | {b} | {c} |\n{durum}")

@bot.command(name="iq")
async def iq(ctx, m: discord.Member = None):
    t = m or ctx.author
    sayi = random.randint(50, 160)
    await ctx.send(f"🧠 {t.name} IQ seviyyesi: {sayi}")

@bot.command(name="baliq")
async def baliq(ctx):
    baliqlar = ['🐟 Baliq', '💎 Qizil Baliq', '🦈 Akula', '🦐 Basqaq']
    tutulan = random.choice(baliqlar)
    await ctx.send(f"🎣 Tuttun: {tutulan}!")

@bot.command(name="hava")
async def hava(ctx, s="Baki"):
    derece = random.randint(10, 35)
    await ctx.send(f"🌤️ Hava ({s}): {derece}°C")

@bot.command(name="hesabla")
async def hesabla(ctx, *, t="2+2"):
    try:
        netice = eval(t)
        await ctx.send(f"🧮 Netice: {netice}")
    except:
        await ctx.send("❌ Riyazi xeta!")

@bot.command(name="tassaxla")
async def tassaxla(ctx):
    zer = random.randint(1, 6)
    await ctx.send(f"🎲 Zer: {zer}")

@bot.command(name="sec")
async def sec(ctx, *, l="Beli, Xeyir"):
    secim = random.c
