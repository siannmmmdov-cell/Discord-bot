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
    return "Bot onlayndır!"

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

bot = commands.Bot(command_prefix="r?", intents=intents)

SAHIB_ID = 641014966312501259
XUSUSI_KANAL_ID = 1544056308787974294 

user_xp = {}
spam_takip = {}
warn_sistemi = {}

@bot.event
async def on_ready():
    print(f"🔥 Bot işə düşdü: {bot.user.name} 🔥")
    await bot.change_presence(activity=discord.Game(name="r?bot | 80+ Əmr Aktivdir 👑"))
    stats_update.start()
    voice_xp_loop.start()

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Səhv və ya tapılmayan əmrlərdə bot çökməsin, səssiz ötürsün
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Əksik arqument! Əmri düzgün istifadə etdiyindən əmin ol. (Məsələn: `r?mute @istifadəçi`)", delete_after=6)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu əmri işlətmək üçün yetərli səlahiyyətin yoxdur!", delete_after=6)
    else:
        print(f"Xəta baş verdi: {error}")

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

@bot.command(name="bot")
async def bot_komanda(ctx):
    if ctx.author.id != SAHIB_ID: return
    
    embed1 = discord.Embed(
        title="👑 YENİLMEZ v6000 - Genişləndirilmiş Panel (Hissə 1)",
        description="Bütün əmrlər tam aktiv və qorunur:",
        color=0xffa200
    )
    embed1.add_field(name="👑 Sahib & İdarəetmə", value=(
        "`r?bot` - Əmr panelini açır.\n"
        "`r?ticketpanel` - Ticket sistemi qurur.\n"
        "`r?elan` - Elan verir.\n"
        "`r?anket` - Səsvermə açır.\n"
        "`r?cekilis` - Çəkiliş başladır.\n"
        "`r?duyuru` - Rəsmi duyuru atır.\n"
        "`r?bakim` - Baxım rejimi.\n"
        "`r?slowmode` (və ya r?yavas) - Yavaş mod.\n"
        "`r?sayac` - Üzv sayğacını yeniləyir.\n"
        "`r?rolver` / `r?rolal` - Rol əməliyyatları.\n"
        "`r?botdurdur` - Botu bağlayır."
    ), inline=False)
    
    embed1.add_field(name="🛡️ Moderasiya & Qoruma", value=(
        "`r?sil` - Mesaj silir.\n"
        "`r?mute` / `r?unmute` - Səs qadağası.\n"
        "`r?ban` / `r?unban` - Ban əməliyyatları.\n"
        "`r?kick` - Serverdən qovur.\n"
        "`r?nuke` - Kanalı yeniləyir.\n"
        "`r?warn` / `r?warnings` - Xəbərdarlıqlar.\n"
        "`r?temizlewarn` - Warn silir.\n"
        "`r?lock` / `r?unlock` - Kilidləmə."
    ), inline=False)

    embed2 = discord.Embed(
        title="👑 YENİLMEZ v6000 - Genişləndirilmiş Panel (Hissə 2)",
        description="Statistika, İnfo və Əyləncə:",
        color=0x00aaff
    )
    embed2.add_field(name="📊 Statistika & Məlumat", value=(
        "`r?server` - Server bilgiləri.\n"
        "`r?userinfo` - İstifadəçi profili.\n"
        "`r?botinfo` - Bot versiyası.\n"
        "`r?ping` / `r?botping` - Gecikmə.\n"
        "`r?online` - Onlayn sayı.\n"
        "`r?level` - XP və səviyyə.\n"
        "`r?rolbilgi` / `r?kanalbilgi` - Detallar.\n"
        "`r?boosters` - Boost edənlər.\n"
        "`r?avatar` / `r?banner` - Şəkillər.\n"
        "`r?emojisay` / `r?servericon` - İkon və emojilər."
    ), inline=False)

    embed2.add_field(name="🎮 Oyunlar & Əyləncə (80+ Əmr)", value=(
        "`r?duel` - Duel at.\n"
        "`r?coinflip` - Yazı-tura.\n"
        "`r?slot` - Kazino.\n"
        "`r?iq` - IQ ölç.\n"
        "`r?balıq` - Balıq tut.\n"
        "`r?hava` - Hava proqnozu.\n"
        "`r?hesabla` - Riyaziyyat.\n"
        "`r?tassaxla` - Zər at.\n"
        "`r?sec` - Seçim etdir.\n"
        "`r?8ball` - Sehrli kürə.\n"
        "`r?sevgi` - Sevgi ölç.\n"
        "`r?hackle` - Zarafat hack.\n"
        "`r?soz` / `r?cat` / `r?joke` - Maraqlı sözlər.\n"
        "`r?cmk` - Daş-kağız-qayçı.\n"
        "`r?ters` - Mətni tərsinə çevir.\n"
        "`r?rozet` / `r?sohbet` / `r?tarix` - Əlavə əyləncələr."
    ), inline=False)

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)

@bot.command(name="ticketpanel")
async def ticketpanel(ctx):
    if ctx.author.id != SAHIB_ID: return
    try: await ctx.message.delete()
    except: pass
    await ctx.send(embed=discord.Embed(title="🎫 Dəstək Paneli", description="Aşağıdakı düyməyə basaraq ticket açın.", color=0x00aaff), view=TicketAc())

@bot.command(name="ticket")
async def ticket_alias(ctx):
    await ctx.invoke(bot.get_command('ticketpanel'))

@bot.command(name="elan")
async def elan(ctx, *, m="Elan mətni yoxdur"):
    if ctx.author.id != SAHIB_ID: return
    try: await ctx.message.delete()
    except: pass
    await ctx.send(embed=discord.Embed(title="📢 ELAN", description=m, color=0xffaa00))

@bot.command(name="anket")
async def anket(ctx, *, s="Anket sualı yoxdur"):
    if ctx.author.id != SAHIB_ID: return
    try: await ctx.message.delete()
    except: pass
    msg = await ctx.send(embed=discord.Embed(title="📊 ANKET", description=s, color=0x00ffcc))
    await msg.add_reaction("👍"); await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, sure: str = "1m", *, odul: str = "Hədiyyə"):
    if ctx.author.id != SAHIB_ID: return
    try: await ctx.message.delete()
    except: pass
    try:
        b, s = sure[-1], int(sure[:-1])
        sn = s * (1 if b=='s' else 60 if b=='m' else 3600 if b=='h' else 86400)
    except: sn = 60
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
async def duyuru(ctx, *, m="Duyuru"):
    if ctx.author.id != SAHIB_ID: return
    try: await ctx.message.delete()
    except: pass
    await ctx.send(f"🔔 **DUYURU:** {m}")

@bot.command(name="bakim")
async def bakim(ctx, d="açıq"):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send(f"🛠️ Baxım rejimi: **{d}**")

@bot.command(name="slowmode")
async def slowmode(ctx, saniye: int = 0):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Yavaş mod **{saniye}** san oldu!")

@bot.command(name="yavas")
async def yavas_alias(ctx, saniye: int = 0):
    await ctx.invoke(bot.get_command('slowmode'), saniye=saniye)

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
async def ban(ctx, m: discord.Member, *, r="Səbəb göstərilməyib"):
    if ctx.author.id != SAHIB_ID: return
    await m.ban(reason=r); await ctx.send(f"🔨 {m.name} banlandı!")

@bot.command(name="unban")
async def unban(ctx, *, name=""):
    if ctx.author.id != SAHIB_ID: return
    for entry in await ctx.guild.bans():
        if entry.user.name.lower() in name.lower():
            await ctx.guild.unban(entry.user)
            await ctx.send(f"🔓 Unban: {entry.user.name}")
            return
    await ctx.send("❌ İstifadəçi tapılmadı.")

@bot.command(name="kick")
async def kick(ctx, m: discord.Member, *, r="Səbəb yoxdur"):
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
async def warnings(ctx, m: discord.Member = None):
    t = m or ctx.author
    await ctx.send(f"📌 {t.name} warn sayı: **{len(warn_sistemi.get(t.id, []))}**")

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
    try:
        u = await bot.fetch_user((m or ctx.author).id)
        await ctx.send(u.banner.url if u.banner else "Banner yoxdur.")
    except: await ctx.send("Banner tapılmadı.")

@bot.command(name="emojisay")
async def emojisay(ctx): await ctx.send(f"😀 Emoji sayı: {len(ctx.guild.emojis)}")

@bot.command(name="servericon")
async def servericon(ctx): await ctx.send(ctx.guild.icon.url if ctx.guild.icon else "İkon yoxdur.")

@bot.command(name="botping")
async def botping(ctx): await ctx.send(f"⚡ Bot daxili gecikmə: {round(bot.latency * 1000)}ms")

@bot.command(name="duel")
async def duel(ctx, m: discord.Member = None):
    target = m.mention if m else "Dost"
    await ctx.send(f"⚔️ Duel qalibi: {random.choice([ctx.author.mention, target])}!")

@bot.command(name="coinflip")
async def coinflip(ctx): await ctx.send(f"🎲 {random.choice(['Yazı 🪙', 'Tura 👑'])}")

@bot.command(name="slot")
async def slot(ctx):
    e = ["🍎", "🍋", "🍒", "7️⃣", "💎"]
    a, b, c = random.choice(e), random.choice(e), random.choice(e)
    await ctx.send(f"🎰 [{a} | {b} | {c}]\n" + ("🎉 UDDUNUZ!" if a==b==c else "❌ Uduzdunuz!"))

@bot.command(name="iq")
async def iq(ctx, m: discord.Member = None):
    t = m or ctx.author
    await ctx.send(f"🧠 {t.name} IQ səviyyəsi: {random.randint(50, 160)}")

@bot.command(name="balıq")
async def baliq(ctx): await ctx.send(f"🎣 Tutdun: {random.choice(['🐟 Balıq', '🐠 Qızıl Balıq', '🦈 Akula', '👞 Başmaq'])}")

@bot.command(name="hava")
async def hava(ctx, *, s="Bakı"): await ctx.send(f"🌤️ {s}: {random.randint(18, 35)}°C")

@bot.command(name="hesabla")
async def hesabla(ctx, *, i="2+2"):
    try: await ctx.send(f"🧮 Nəticə: {eval(i)}")
    except: await ctx.send("❌ Riyazi xəta!")

@bot.command(name="tassaxla")
async def tassaxla(ctx): await ctx.send(f"🎲 Zər: {random.randint(1, 6)}")

@bot.command(name="sec")
async def sec(ctx, *, l="Bəli, Xeyir"): 
    await ctx.send(f"🎯 Seçimim: {random.choice(l.split(',')).strip()}")

@bot.command(name="8ball")
async def eightball(ctx, *, s="Sual"): 
    await ctx.send(f"🔮 {random.choice(['Bəli', 'Xeyir', 'Bəlkə də', 'Mütləq'])}")

@bot.command(name="sevgi")
async def sevgi(ctx, m: discord.Member = None):
    target = m.mention if m else "Kimsə"
    await ctx.send(f"❤️ {ctx.author.mention} və {target} uyğunluğu: %{random.randint(10, 100)}")

@bot.command(name="hackle")
async def hackle(ctx, m: discord.Member = None):
    target = m.mention if m else "Dost"
    await ctx.send(f"💻 {target} uğurla hackləndi! Parol: `12345`")

@bot.command(name="soz")
async def soz(ctx): 
    await ctx.send(f"📜 {random.choice(['Uğur qətiyyətlidir.', 'Həlak olmamaq üçün daim irəli!', 'Zəhmət çəkmədən balıq tutulmaz.'])}")

@bot.command(name="cat")
async def cat(ctx): await ctx.send("🐱 Pişik faktı: Ömrünün 70 faizini yatmaqla keçirirlər.")

@bot.command(name="joke")
async def joke(ctx): await ctx.send("🎭 - Müəllim, zəhmət olmasa aşağıdan yazın, başa düşmürəm.\n- Aşağı yer yoxdur, uşağım!")

@bot.command(name="cmk")
async def cmk(ctx): await ctx.send(f"🎮 Daş-Kağız-Qayçı: {random.choice(['Daş 🪨', 'Kağız 📄', 'Qayçı ✂️'])}")

@bot.command(name="ters")
async def ters(ctx, *, yazi="Salam"): await ctx.send(yazi[::-1])

@bot.command(name="sohbet")
async def sohbet(ctx): await ctx.send("💬 Necəsən, qardaş? İşlər necə gedir?")

@bot.command(name="rozet")
async def rozet(ctx): await ctx.send("🏆 Sən bu serverin əfsanəvi sahibisən!")

@bot.command(name="tarix")
async def tarix(ctx): await ctx.send(f"📅 Bu gün: {time.s
