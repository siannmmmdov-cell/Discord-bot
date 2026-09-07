import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
import time
import re
from datetime import timedelta
from flask import Flask
from threading import Thread

# SAHİBİN İD-Sİ
SAHIB_ID = 641014966312501259

# RENDER KEEPER (KEEP-ALIVE)
app = Flask('')

@app.route('/')
def home():
    return "V80000 Ultra Bot Online və Aktivdir!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# DİSCORD İNTENTS
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.webhooks = True

bot = commands.Bot(command_prefix="!", intents=intents)

# SİSTEM DƏYİŞƏNLƏRİ VƏ İZLƏMƏ LÜĞƏTLƏRİ
user_xp = {}
spam_takip = {}
spam_sayaci = {}

# BOT HAZIR OLANDA
@bot.event
async def on_ready():
    print(f'----------------------------------------')
    print(f' V80000 Ultra Qoruma Sistemi Aktivləşdi!')
    print(f' Botun Adı: {bot.user.name}')
    print(f' ID: {bot.user.id}')
    print(f'----------------------------------------')
    await bot.change_presence(activity=discord.Game(name="!bot | V80000 Ultra Qoruma"))

# YENİ ÜZV QOŞULANDA
@bot.event
async def on_member_join(member):
    if member.bot:
        return
    try:
        await member.send(f"Salam {member.name}, serverə xoş gəldin! Qaydaları oxumağı unutma.")
    except:
        pass

# GÜCLÜ TƏHLÜKƏSİZLİK FİLTRİ (.GG LİNKLƏRİ VƏ PROQRESSİV SPAM QORUMASI)
@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

    # Sahibə qarşı heç bir qoruma və məhdudiyyət işləməsin
    if message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    simdi = time.time()
    icerik = message.content.lower()

    # 1. .GG VƏ DƏVƏT LİNKİ QADAĞASI
    if ".gg/" in icerik or "discord.gg/" in icerik:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə dəvət linki (`.gg`) paylaşmaq qadağandır!")
            await asyncio.sleep(5)
            await warn.delete()
            return
        except:
            pass

    # 2. PROQRESSİV SPAM QORUMASI
    if author_id not in spam_takip:
        spam_takip[author_id] = []
    if author_id not in spam_sayaci:
        spam_sayaci[author_id] = 0

    # Son 3 saniyəlik mesajları təmizlə
    spam_takip[author_id] = [t for t in spam_takip[author_id] if simdi - t < 3]
    spam_takip[author_id].append(simdi)

    # Əgər qısa müddətdə həddindən artıq mesaj atıbsa
    if len(spam_takip[author_id]) > 4:
        try:
            await message.delete()
            spam_sayaci[author_id] += 1

            if spam_sayaci[author_id] == 1:
                warn = await message.channel.send(f"⚠️ {message.author.mention}, spam basma oğlan, dayan!")
                await asyncio.sleep(5)
                await warn.delete()
            else:
                await message.author.timeout(timedelta(seconds=60), reason="Ardıcıl spam")
                warn = await message.channel.send(f"🔇 {message.author.mention}, təkrar spam etdiyin üçün 1 dəqiqəlik zaman aşımına atıldın!")
                await asyncio.sleep(5)
                await warn.delete()
                spam_sayaci[author_id] = 0
            return
        except:
            pass

    await bot.process_commands(message)

# ==========================================
# İDARƏETMƏ VƏ PANEL KOMUTU (!bot)
# ==========================================

@bot.command(name="bot")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="🛡️ V80000 ULTRA İDARƏETMƏ VƏ KOMUT PANELİ",
        description="Botun içindəki bütün sistemlər və kateqoriyalar aşağıdakılardır:",
        color=discord.Color.dark_red()
    )
    embed.add_field(
        name="🛡️ 1. Təhlükəsizlik Sistemləri", 
        value="• **Anti-.GG Link:** Dəvət linklərini avtomatik silir.\n• **Anti-Spam:** Ardıcıl mesajları dayandırır və timeout verir.\n• **Sahib Qoruması:** Səni bütün məhdudiyyətlərdən qoruyur.", 
        inline=False
    )
    embed.add_field(
        name="⚙️ 2. Panel və Məlumat Komutları", 
        value="`!bot`, `!ping`, `!serverinfo`, `!userinfo`, `!avatar`, `!uptime`, `!developer`, `!version`, `!rules`, `!support`", 
        inline=False
    )
    embed.add_field(
        name="🔨 3. Sahib və Moderasiya Əmrləri", 
        value="`!lock`, `!unlock`, `!hide`, `!reveal`, `!hideall`, `!revealall`, `!slowmode`, `!nuke`, `!ban`, `!kick`, `!clear`, `!say`, `!createtext`, `!createvoice`", 
        inline=False
    )
    embed.add_field(
        name="🎮 4. Əyləncə və Oyun Komutları", 
        value="`!roll`, `!coinflip`, `!iq`, `!gay`, `!handsome`, `!love`, `!hack`, `!wasted`, `!rip`, `!slap`, `!hug`, `!kiss`, `!kill`, `!cat`, `!dog`, `!ascii`, `!reverse`, `!upper`, `!lower`, `!afk`, `!weather`, `!poll`, `!reminder`, `!fact`, `!quote`, `!8ball`, `!calc`, `!joke`, `!rps`", 
        inline=False
    )
    embed.add_field(
        name="⚡ 5. Dinamik Modullar", 
        value="`!modul1`-dən `!modul30`-ə qədər xüsusi əlavə modullar mövcuddur.", 
        inline=False
    )
    embed.set_footer(text="V80000 Security Systems © 2026 | Bütün hüquqlar qorunur.")
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    lat = round(bot.latency * 1000)
    await ctx.send(f"pong! 🏓 Gecikmə müddəti: **{lat}ms**")

@bot.command(name="serverinfo")
async def serverinfo(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"📊 {g.name} - Server Məlumatları", color=discord.Color.blue())
    embed.add_field(name="Sahib", value=g.owner, inline=True)
    embed.add_field(name="Üzv Sayı", value=g.member_count, inline=True)
    embed.add_field(name="Kanal Sayı", value=len(g.channels), inline=True)
    embed.add_field(name="Rol Sayı", value=len(g.roles), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"👤 {m.name} haqqında", color=m.color)
    embed.add_field(name="ID", value=m.id, inline=True)
    embed.add_field(name="Qoşulduğu tarix", value=m.joined_at.strftime("%Y-%m-%d"), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {m.name} - Avatar", color=discord.Color.purple())
    embed.set_image(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="uptime")
async def uptime(ctx):
    await ctx.send("⚡ Bot fasiləsiz və stabil şəkildə işləyir!")

@bot.command(name="developer")
async def developer(ctx):
    await ctx.send("👨‍💻 Bu bot xüsusi olaraq sahib üçün kodlanmışdır.")

@bot.command(name="version")
async def version(ctx):
    await ctx.send("📌 Bot Versiyası: **V80000 Ultra Pro**")

@bot.command(name="rules")
async def rules(ctx):
    await ctx.send("📜 Server qaydaları: Hörmət çərçivəsindən çıxmaq, spam və link atmaq qəti qadağandır!")

@bot.command(name="support")
async def support(ctx):
    await ctx.send("🛠️ Dəstək üçün sahibə müraciət edin.")

# ==========================================
# SAHİB VƏ MODERASİYA ƏMRLƏRİ
# ==========================================

@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal yazışmaya açıldı.")

@bot.command(name="hide")
async def hide(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🙈 Bu kanal hamıdan gizlətildi.")

@bot.command(name="reveal")
async def reveal(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🐵 Bu kanal yenidən hər kəsə göstərildi.")

@bot.command(name="hideall")
async def hideall(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        except:
            pass
    await ctx.send("🙈 Serverdəki bütün kanallar hamıdan gizlətildi!")

@bot.command(name="revealall")
async def revealall(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        except:
            pass
    await ctx.send("🐵 Serverdəki bütün kanallar yenidən hər kəsə göstərildi!")

@bot.command(name="slowmode")
async def slowmode(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Kanalın yavaş modu {seconds} saniyə edildi.")

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    position = ctx.channel.position
    new_channel = await ctx.channel.clone(reason="Nuke əmri icra olundu")
    await ctx.channel.delete()
    await new_channel.edit(position=position)
    await new_channel.send("💥 Kanal sıfırlandı və təmizləndi!")

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID:
        return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} serverdən ban edildi! Səbəb: {reason}")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != SAHIB_ID:
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} serverdən atıldı! Səbəb: {reason}")

@bot.command(name="clear")
async def clear(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 {amount} mesaj təmizləndi.")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name="say")
async def say(ctx, *, text):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.message.delete()
    await ctx.send(text)

@bot.command(name="createtext")
async def createtext(ctx, *, isim):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"📁 `{isim}` adlı mətn kanalı yaradıldı.")

@bot.command(name="createvoice")
async def createvoice(ctx, *, isim):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.guild.create_voice_channel(isim)
    await ctx.send(f"🔊 `{isim}` adlı səs kanalı yaradıldı.")

# ==========================================
# ƏYLƏNCƏ VƏ OYUN KOMUTLARI
# ==========================================

@bot.command(name="roll")
async def roll(ctx):
    await ctx.send(f"🎲🎲 Zər atıldı: **{random.randint(1, 6)}**")

@bot.command(name="coinflip")
async def coinflip(ctx):
    res = random.choice(["Yazı", "Pər"])
    await ctx.send(f"🪙 Qəpik atıldı: **{res}**")

@bot.command(name="iq")
async def iq(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🧠 {m.name} - IQ Səviyyəsi: **{random.randint(40, 200)}**")

@bot.command(name="gay")
async def gay(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🏳️‍🌈 {m.name} - Oranı: **%{random.randint(0, 100)}**")

@bot.command(name="handsome")
async def handsome(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"😎 {m.name} - Yakışıklılıq: **%{random.randint(50, 100)}**")

@bot.command(name="love")
async def love(ctx, member1: discord.Member, member2: discord.Member):
    await ctx.send(f"❤️ {member1.name} ilə {member2.name} uyğunluğu: **%{random.randint(10, 100)}**")

@bot.command(name="hack")
async def hack(ctx, member: discord.Member):
    await ctx.send(f"💻 {member.name} sistemə sızıldı... Şifrə oğurlandı: `12345_qonaq`")

@bot.command(name="wasted")
async def wasted(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"💀 {m.mention} yaşaya bilmədi... WASTED!")

@bot.command(name="rip")
async def rip(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"⚰️ R.I.P {m.mention}. Məkanı cənnət olsun.")

@bot.command(name="slap")
async def slap(ctx, member: discord.Member):
    await ctx.send(f"👋 {ctx.author.mention}, {member.mention} üzünə şillə vurdu!")

@bot.command(name="hug")
async def hug(ctx, member: discord.Member):
    await ctx.send(f"🤗 {ctx.author.mention}, {member.mention} qucaqladı!")

@bot.command(name="kiss")
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"💋 {ctx.author.mention}, {member.mention} öpdü!")

@bot.command(name="kill")
async def kill(ctx, member: discord.Member):
    await ctx.send(f"🔪 {ctx.author.mention}, {member.mention} məhv etdi!")

@bot.command(name="cat")
async def cat(ctx):
    await ctx.send("🐱 https://cataas.com/cat")

@bot.command(name="dog")
async def dog(ctx):
    await ctx.send("🐶 https://placedog.net/500")

@bot.command(name="ascii")
async def ascii_art(ctx, *, text):
    await ctx.send(f"```text\n{text}\n```")

@bot.command(name="reverse")
async def reverse(ctx, *, text):
    await ctx.send(text[::-1])

@bot.command(name="upper")
async def upper(ctx, *, text):
    await ctx.send(text.upper())

@bot.command(name="lower")
async def lower(ctx, *, text):
    await ctx.send(text.lower())

@bot.command(name="afk")
async def afk(ctx, *, reason="Mövcud deyil"):
    await ctx.send(f"💤 {ctx.author.mention} AFK rejiminə keçdi. Səbəb: {reason}")

@bot.command(name="weather")
async def weather(ctx, *, city="Bakı"):
    await ctx.send(f"🌤️ {city} şəhərində hava günəşli və 24°C-dir.")

@bot.command(name="poll")
async def poll(ctx, *, question):
    msg = await ctx.send(f"📊 **SORĞU:** {question}")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="reminder")
async def reminder(ctx, time_sec: int, *, msg):
    await ctx.send(f"⏰ Xatırladıcı quruldu! {time_sec} saniyə sonra xəbər verəcəyəm.")
    await asyncio.sleep(time_sec)
    await ctx.send(f"🔔 Xatırladıcı vaxtıdır, {ctx.author.mention}: {msg}")

@bot.command(name="fact")
async def fact(ctx):
    facts = [
        "Dünyadakı ağacların sayı ulduzların sayından çoxdur.",
        "Su donanda həcmi genişlənir.",
        "Bal heç vaxt xarab olmur."
    ]
    await ctx.send(f"💡 Maraqlı fakt: {random.choice(facts)}")

@bot.command(name="quote")
async def quote(ctx):
    quotes = [
        "Hər şey mümkündür, sadəcə inanmaq lazımdır.",
        "Vaxt hər şeyin dərmanıdır.",
        "Zirvəyə gedən yollar tikənlərlə doludur."
    ]
    await ctx.send(f"📜 Sitat: *{random.choice(quotes)}*")

@bot.command(name="8ball")
async def eight_ball(ctx, *, question):
    answers = ["Bəli", "Xeyir", "Əmin deyiləm", "Mütləq bəli", "Heç vaxt"]
    await ctx.send(f"🎱 Cavab: **{random.choice(answers)}**")

@bot.command(name="calc")
async def calc(ctx, *, expression):
    try:
        res = eval(expression)
        await ctx.send(f"🧮 Nəticə: **{res}**")
    except:
        pass

@bot.command(name="joke")
async def joke(ctx):
    jokes = [
        "Kompyuter niyə soyuqdəymə oldu? Çünki pəncərəni açıq qoymuşdu!",
        "Temirçi niyə yuxuladı? Çünki zindan döyülürdü."
    ]
    await ctx.send(f"😂 Zarafat: {random.choice(jokes)}")

@bot.command(name="rps")
async def rps(ctx, choice: str):
    choices = ["daş", "kağız", "qayçı"]
    bot_choice = random.choice(choices)
    cho = choice.lower()
    if cho not in choices:
        await ctx.send("Zəhmət olmasa seç: daş, kağız və ya qayçı")
        return
    if cho == bot_choice:
        res = "Heç-heçə!"
    elif (cho == "daş" and bot_choice == "qayçı") or (cho == "kağız" and bot_choice == "daş") or (cho == "qayçı" and bot_choice == "kağız"):
        res = "Sən qazandın!"
    else:
        res = "Mən qazandım!"
    await ctx.send(f"Sənin seçimin: **{cho}** | Mənim seçimin: **{bot_choice}** -> **{res}**")

# ==========================================
# DİNAMİK ƏLAVƏ MODULLAR
# ==========================================

for i in range(1, 31):
    @bot.command(name=f"modul{i}")
    async def dynamic_cmd(ctx, num=i):
        await ctx.send(f"⚙️ V80000 Əlavə Xüsusi Modul #{num} aktiv və işləkdir.")

# BOTU İŞƏ SALMAQ
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    
