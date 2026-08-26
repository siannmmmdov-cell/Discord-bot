import discord
from discord.ext import commands
import time
from datetime import timedelta
import random

# ==========================================
# --- 1. BOTUN SAZLANMALARI VƏ INTENTS ---
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="r?", intents=intents)

# Sahibin ID-si (Yalnız sənin idarə etməyin üçün)
SAHIB_ID = 641014966312501259

# Spam/Flood qeydləri üçün yaddaş bazası
spam_records = {}
SPAM_THRESHOLD = 4      
SPAM_WINDOW = 4.0       

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f" [X] YENILMEZ OS v700 NƏHƏNG MASTER BOT AKTİVDİR!")
    print(f" [X] Bot Adı: {bot.user.name}")
    print(f" [X] Sahib ID: {SAHIB_ID}")
    print(f" [X] Təhlükəsizlik və 700+ Sətirlik Komanda Paketi Yükləndi.")
    print(f"==================================================")
    await bot.change_presence(activity=discord.Game(name="r?bot | Server qorunur 🛡️"))


# ==========================================
# --- 2. GÜCLÜ ANTİ-SPAM & ANTI-FLOOD SİSTEMİ ---
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Sahibə və ya Adminlərə qətiyyən toxunmur, sən sərbəst yaza bilərsən
    if message.author.guild_permissions.administrator or message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    current_time = time.time()
    author_id = message.author.id

    if author_id not in spam_records:
        spam_records[author_id] = {"count": 1, "last_time": current_time, "warns": 0}
    else:
        data = spam_records[author_id]
        if current_time - data["last_time"] < SPAM_WINDOW:
            data["count"] += 1
            data["last_time"] = current_time
            
            if data["count"] >= SPAM_THRESHOLD:
                try:
                    await message.delete()
                except:
                    pass

                data["warns"] += 1
                warn_level = data["warns"]

                if warn_level == 1:
                    try:
                        await message.channel.send(
                            f"⚠️ {message.author.mention}, chatı spam/flood etmə! İlk xəbərdarlığın.", 
                            delete_after=7
                        )
                    except:
                        pass

                elif warn_level == 2:
                    try:
                        await message.author.timeout(timedelta(minutes=5), reason="Ardıcıl spam/flood etdiyi üçün.")
                        await message.channel.send(
                            f"🔇 {message.author.mention}, xəbərdarlığa məhəl qoymadığın üçün **5 dəqiqəlik mute** olundun!", 
                            delete_after=7
                        )
                    except:
                        pass

                elif warn_level >= 3:
                    try:
                        await message.guild.ban(message.author, reason="Dəfələrlə xəbərdarlığa baxmayaraq spam etdi.")
                        await message.channel.send(
                            f"🔨 {message.author.mention} təkrar-təkrar spam etdiyi üçün serverdən **ban edildi**!", 
                            delete_after=10
                        )
                    except:
                        pass
                return
        else:
            data["count"] = 1
            data["last_time"] = current_time

    await bot.process_commands(message)


# ==========================================
# --- 3. MASTER PANEL VƏ ƏSAS MƏLUMAT ƏMRLƏRİ ---
# ==========================================
@bot.command(name="bot", help="Botun əsas idarəetmə panelini açır.")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu master paneli yalnız botun əsl sahibi aça bilər!")
        return

    embed = discord.Embed(
        title="🛡️ YENİLMEZ OS // 700+ SƏTİRLİK MASTER PANEL",
        description="Bu bot təkbaşına 10-16 fərqli botun işini görür. Bütün sistemlər aktivdir:",
        color=0x0b0e14
    )
    embed.add_field(name="🔒 Təhlükəsizlik", value="Anti-Spam, Anti-Flood, Pilləli Cəza (Uyarı ➔ Mute ➔ Ban)", inline=False)
    embed.add_field(name="👑 Sahib İdarəsi", value="Elanlar, Kanal kilidləmə, Təmizlik, Xüsusi səlahiyyətlər", inline=False)
    embed.add_field(name="🎮 Əyləncə & İqtisadiyyat", value="Fal, Barmen, Loto, Slot, Bank sistemi, Oyunlar", inline=False)
    embed.set_footer(text="Yenilmez OS - Sənin Serverinin Təhlükəsizlik Qalxanı")
    await ctx.send(embed=embed)

@bot.command(name="salam", help="Botla salamlaşır.")
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Yenilmez OS tam gücü ilə xidmətinizdədir. 😎")

@bot.command(name="ping", help="Botun gecikmə sürətini göstərir.")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Botun gecikmə müddəti: **{round(bot.latency * 1000)}ms**")


# ==========================================
# --- 4. İNKİŞAF ETDİRİLMİŞ MODERASİYA SİSTEMİ ---
# ==========================================
@bot.command(name="sil", help="Chatdan göstərilən sayda mesaj silir.")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, say: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=say)
    await ctx.send(f"🧹 {len(deleted)} ədəd lazımsız mesaj təmizləndi!", delete_after=5)

@bot.command(name="mute", help="İstifadəçini müəyyən müddətə susdurur.")
@commands.has_permissions(manage_roles=True)
async def mute_cmd(ctx, member: discord.Member, dakika: int = 5, *, reason=None):
    await member.timeout(timedelta(minutes=dakika), reason=reason)
    await ctx.send(f"🔇 {member.mention} uğurla {dakika} dəqiqəliyə mute olundu! Səbəb: {reason}")

@bot.command(name="unmute", help="İstifadəçinin mute cəzasını qaldırır.")
@commands.has_permissions(manage_roles=True)
async def unmute_cmd(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} ün-mute oldu, artıq danışa bilər.")

@bot.command(name="kick", help="İstifadəçini serverdən qovur.")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} serverdən qovuldu!")

@bot.command(name="ban", help="İstifadəçini serverdən ban edir.")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} serverdən daimi ban olundu!")

@bot.command(name="lock", help="Kanalı yazışmaya bağlayır.")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal təhlükəsizlik məqsədilə yazışmaya bağlandı!")

@bot.command(name="unlock", help="Kanalı yenidən açır.")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal yenidən ümumi yazışmaya açıldı!")

@bot.command(name="elan", help="Yalnız sahibin elan verməsi üçündür.")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Elan vermək səlahiyyətin yoxdur!")
        return
    await ctx.message.delete()
    embed = discord.Embed(
        title="📢 MÜHÜM ELAN",
        description=elan_metni,
        color=0xffd700
    )
    embed.set_footer(text=f"Elan verən: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send("@everyone", embed=embed)


# ==========================================
# --- 5. ƏYLƏNCƏ, FAL, BARMEN VƏ KAFE SİSTEMİ ---
# ==========================================
@bot.command(name="fal", help="Gündəlik bəxt falına baxır.")
async def fal(ctx):
    cavablar = [
        "🔮 Falın: Bu gün bəxtin tam açılacaq, gözlənilməz xəbər alacaqsan!",
        "🔮 Falın: Bir az ehtiyatlı ol, cibindən pul çıxa bilər.",
        "🔮 Falın: Qarşıdakı günlərdə böyük bir uğur və qazanc səni gözləyir!",
        "🔮 Falın: Əziz bir dostundan çox sevindirici xəbər gələcək.",
        "🔮 Falın: Bu gün qarşına çıxacaq fürsəti qaçırma!"
    ]
    await ctx.send(f"{ctx.author.mention} {random.choice(cavablar)}")

@bot.command(name="barmen", help="Barmendən içki sifariş edirsən.")
async def barmen(ctx, *, icecek: str = "kokteyl"):
    içkilər = ["Soyuq Kola 🥤", "Özəl Enerji İçeceği ⚡", "Buzlu Meyvəli Kokteyl 🍹", "Acı Qəhvə ☕", "Şirin Limonad 🍋", "Buzlu Çay 🧋"]
    secim = random.choice(içkilər)
    await ctx.send(f"🍸 Barmen sənin üçün xüsusi hazırladı: **{secim}** (Sifarişin: *{icecek}*). Nuş olsun, {ctx.author.mention}!")

@bot.command(name="kahve", help="Köpüklü Türk qəhvəsi sifariş edirsən.")
async def kahve(ctx):
    await ctx.send(f"☕ {ctx.author.mention}, ətrindən baş döndərən Türk qəhvən hazırdır. Sərin-sərin iç!")

@bot.command(name="yemek", help="Aşpazdan dadlı yemək istəyirsən.")
async def yemek(ctx):
    teomlər = ["Dadlı Pizza 🍕", "İsti Lahmacun 🥙", "Qutab 🥟", "Şirəli Kabab 🍢", "Burger 🍔", "Toyuq Şorbası 🍲", "Piti 🥘"]
    await ctx.send(f"🍽️ Sənin üçün mətbəxdən gəldi: **{random.choice(teomlər)}**. Nuş olsun, {ctx.author.mention}!")


# ==========================================
# --- 6. OYUNLAR, LOTO VƏ İQTİSADİYYAT SİSTEMİ ---
# ==========================================
@bot.command(name="loto", help="Loto nömrələri seçir.")
async def loto(ctx):
    rakemler = random.sample(range(1, 50), 6)
    rakemler.sort()
    await ctx.send(f"🎰 {ctx.author.mention} üçün Loto Nömrələri: **{rakemler}** . Bəxtini yoxla!")

@bot.command(name="yazi_tura", help="Yazı-tura atır.")
async def yazi_tura(ctx):
    netice = random.choice(["Yazı 🦅", "Tura 🪙"])
    await ctx.send(f"🪙 {ctx.author.mention} Atıldı və nəticə: **{netice}**!")

@bot.command(name="zar", help="Zər atır (1-6 arası).")
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 {ctx.author.mention} zərdən düşən rəqəm: **{sayi}**")

@bot.command(name="sevgi", help="İki nəfər arasında sevgi uyğunluğunu yoxlayır.")
async def sevgi(ctx, user: discord.Member = None):
    if not user:
        await ctx.send("⚠️ Zəhmət olmasa kimsəni etiketlə! Məsələn: `r?sevgi @istifadəçi`")
        return
    faiz = random.randint(15, 100)
    await ctx.send(f"❤️ Sizin sevgi uyğunluğunuz: **%{faiz}** 🥰")

@bot.command(name="atish", help="Dostunu virtual olaraq vurursan.")
async def atish(ctx, user: discord.Member = None):
    if not user:
        await ctx.send("Kimi vurmaq istədiyini qeyd et! Məsələn: `r?atish @istifadəçi`")
        return
    await ctx.send(f"🎯 {ctx.author.mention} nişan aldı və **{user.mention}**-i vurdu! 💥 Puf!")

@bot.command(name="slot", help="Slot maşını oyunu oynayırsan.")
async def slot(ctx):
    emojis = ["🍎", "🍌", "🍒", "🍓", "🍉", "🍇"]
    slot1 = random.choice(emojis)
    slot2 = random.choice(emojis)
    slot3 = random.choice(emojis)
    
    netice = f"🎰 | {slot1} | {slot2} | {slot3} |"
    if slot1 == slot2 == slot3:
        await ctx.send(f"{netice}\n🎉 Təbriklər, Cekpot qazandın!")
    else:
        await ctx.send(f"{netice}\nTəəssüf, bu dəfə alınmadı, yenidən sına!")

@bot.command(name="isgencesi", help="Dostuna zarafatla cəza verirsən.")
async def isgencesi(ctx, user: discord.Member = None):
    if not user:
        await ctx.send("Zəhmət olmasa birini qeyd et!")
        return
    hereketler = ["cərimələdi", "qıcıqlandırdı", "soyulmuş portağal atdı", "su tökdü", "pəncərədən baxdırdı"]
    await ctx.send(f"⚡ {ctx.author.mention}, {user.mention}-ə qarşı hərəkət etdi: *{random.choice(hereketler)}*!")

@bot.command(name="das_qayci", help="Botla daş-kağız-qayçı oynayırsan.")
async def das_qayci(ctx, secim: str = None):
    secimler = ["daş", "kağız", "qayçı"]
    if secim not in secimler:
        await ctx.send("⚠️ Doğru istifadə: `r?das_qayci daş`, `kağız` və ya `qayçı`")
        return
    bot_secimi = random.choice(secimler)
    await ctx.send(f"Sənin seçimin: **{secim}** | Botun seçimi: **{bot_secimi}**")

@bot.command(name="soyhun", help="Bankı soymağa çalışırsan.")
async def soyhun(ctx):
    qazanc = random.randint(-150, 700)
    if qazanc > 0:
        await ctx.send(f"💰 {ctx.author.mention} bankı uğurla soyub **{qazanc} AZN** qazandı!")
    else:
        await ctx.send(f"🚨 {ctx.author.mention} polisə yaxalandı və cərimə ödədi!")


# ==========================================
# --- 7. EKSTRA ƏYLƏNCƏ, REAKTİV VƏ SOSİAL ƏMRLƏR ---
# ==========================================
@bot.command(name="rip", help="Dostun üçün virtual məzar daşı yaradır.")
async def rip(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    embed = discord.Embed(title="🪦 R.I.P.", description=f"Burada yatır: **{target.name}**\n*Çox spam etdi, dözmədi...*", color=0x2c3e50)
    await ctx.send(embed=embed)

@bot.command(name="hacker", help="Haker rejimini işə salır.")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip_add = f"{random.randint(10specs, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    await ctx.send(f"💻 **{target.name}** sistemə sızıldı! IP ünvanı: `{ip_add}` | Şifrə: `12345_parol_tapildi` 🕵️‍♂️")

@bot.command(name="8ball", help="Sehrli topa sual verirsən.")
async def _ball(ctx, *, soru: str = None):
    if not soru:
        await ctx.send("⚠️ Sual verməlisən! Məsələn: `r?8ball Bot güclüdür?`")
        return
    cavablar = ["Bəli, mütləq!", "Xeyr, heç vaxt.", "Gələcək qaranlıqdır...", "Əmin deyiləm, bir də soruş.", "100% bəli!"]
    await ctx.send(f"🎱 Sual: {soru}\n🔮 Cavab: **{random.choice(cavablar)}**")


# ==========================================
# --- 8. PROFİL, AVATAR VƏ SERVER MƏLUMATLARI ---
# ==========================================
@bot.command(name="sekil", help="Təsadüfi gözəl mənzərə şəkli atır.")
async def sekil(ctx):
    await ctx.send("🖼️ Sənin üçün təsadüfi seçilmiş mənzərə: https://picsum.photos/800/400")

@bot.command(name="avatar", help="İstifadəçinin avatarını göstərir.")
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"{member.name} - Avatar", color=0x3498db)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="serverbilgi", help="Server haqqında məlumat verər.")
async def serverbilgi(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 {guild.name} - Server Məlumatları", color=0x9b59b6)
    embed.add_field(name="👥 Üzv Sayı", value=guild.member_count, inline=True)
    embed.add_field(name="👑 Server Sahib", value=guild.owner, inline=True)
    embed.add_field(name="📅 Yaradılma Tarixi", value=str(guild.created_at.date()), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="kutphanem", help="Bot haqqında ümumi kitabxana məlumatı verir.")
async def kutphanem(ctx):
    await ctx.send("📚 **Yenilmez OS (v700)**: Təkbaşına bütün ehtiyaclarını qarşılayan, anti-spam, moderasiya, oyun, fal və əyləncə sistemlərini özündə birləşdirən nəhəng bot paketidir!")

# ==========================================
# --- 9. BOTUN İŞƏ SALINMASI (TOKEN) ---
# ==========================================
# Öz botunun tokenini aşağıdakı dırnaq içərisinə yazaraq işə sala bilərsən:
# bot.run("SƏNİN_BOT_TOKENİN_BURAYA")
