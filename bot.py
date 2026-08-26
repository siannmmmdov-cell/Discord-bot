import discord
from discord.ext import commands
import os
import re
import time
import asyncio
import random
from datetime import timedelta
from flask import Flask
import threading

# Render port xətası verməsin deyə veb-server
app = Flask('')

@app.route('/')
def home():
    return "Kral Bot aktivdir və serveri qoruyur!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_server).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Əmrlər nida (!) ilə başlayır
bot = commands.Bot(command_prefix="!", intents=intents)

# Spam və flood izləmə sistemləri
spam_tracker = {}
spam_warnings = {}

@bot.event
async def on_ready():
    print(f"👑 KRAL BOT AKTİVDİR VƏ QORUYUR: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Server Qorunur | !yardim"))

# --- +1000000 GÜVƏNLİK, SALAMLAMA VƏ QORUMA SİSTEMİ ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Adminlərə qoruma qadağaları şamil olunmur
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content
    lower_content = content.lower()

    # 1. Salamlaşma Sistemi (Kim salam verəndə bot cavab verir)
    salam_sozleri = ["salam", "salamun aleykum", "sa", "as", "heykəl", "hey", "merhaba", "sabahın xeyir", "axşamınız xeyir"]
    if any(s in lower_content for s in salam_sozleri) and len(lower_content) < 25:
        cevaplar = [
            f"Aleykum salam, {message.author.mention}! Xoş gəldin, necəsən? 👋",
            f"Salam, {message.author.mention}! Gecən xeyrə qalsın ya da günün gözəl keçsin! 👑",
            f"Aleykum salam, qaqaş! Bot sənin xidmətindədir. 🤖"
        ]
        try:
            await message.channel.send(random.choice(cevaplar))
        except:
            pass

    # 2. Reklam, Link və Discord Dəvəti Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite|t\.me|instagram\.com|tiktok\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə reklam və link atmaq qəti qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. @everyone / @here Spam Qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, @everyone və ya @here atmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 4. Həddindən artıq Böyük Hərf (Caps Lock) Qoruması (>70%)
    if len(content) > 8:
        uppercase_count = sum(1 for c in content if c.isupper())
        if uppercase_count / len(content) > 0.7:
            try:
                await message.delete()
                warn = await message.channel.send(f"⚠️ {message.author.mention}, çoxlu böyük hərf (Caps Lock) istifadə etmək qadağandır!")
                await asyncio.sleep(4)
                await warn.delete()
                return
            except:
                pass

    # 5. Sürətli Flood / Spam Qoruması (5 dəfə eyni sözü yazanda və ya ardıcıl tez mesaj atanda)
    author_id = message.author.id
    current_time = time.time()
    
    if author_id not in spam_tracker:
        spam_tracker[author_id] = []
    
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 6]
    spam_tracker[author_id].append(current_time)

    # 5 və ya daha çox mesaj qısa müddətdə gələrsə
    if len(spam_tracker[author_id]) >= 5:
        spam_tracker[author_id].clear()
        if author_id not in spam_warnings:
            spam_warnings[author_id] = 0
        spam_warnings[author_id] += 1
        
        try:
            await message.delete()
        except:
            pass

        if spam_warnings[author_id] >= 1:
            try:
                await message.author.timeout(timedelta(minutes=3), reason="Flood / Spam qoruması")
                await message.channel.send(f"⏳ {message.author.mention}, çoxlu flood/spam yazdığın üçün 3 dəqiqəlik **zaman aşımı (timeout)** aldın!")
            except:
                pass
        return

    await bot.process_commands(message)

# --- İDARƏETMƏ VƏ PANEL ƏMRLƏRİ ---
@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="👑 Kral Bot - İdarəetmə və Təhlükəsizlik Paneli",
        description="Server tam güvənlik altındadır, qaqaş! Bütün əmrlər `!` ilə işləyir:",
        color=discord.Color.gold()
    )
    embed.add_field(name="🛡️ Güvənlik və Qoruma", value="• Avtomatik Salamlama sistemi\n• Reklam/Link qoruması\n• @everyone qoruması\n• Caps Lock qoruması\n• 5 mesaj flood qoruması + Zaman aşımı (Timeout)", inline=False)
    embed.add_field(name="🧹 Moderasiya", value="• `!sil [say]` - Mesajları təmizləyir\n• `!ban [@istifadəçi]` - Ban edir\n• `!mute [@istifadəçi] [dəqiqə]` - Susdurur\n• `!sunucukoru` - Qoruma statusunu yoxlayır", inline=False)
    embed.add_field(name="🎮 Oyunlar və Əyləncə", value="• `!ping` - Gecikməni yoxlayır\n• `!zar` - Zər atır\n• `!zarafat` - Lətifələr deyir\n• `!yaziqtura` - Yazı-Tura oyunu oynayır\n• `!sayish` - Əyləncəli sayma oyunu", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="sunucukoru")
async def sunucukoru(ctx):
    embed = discord.Embed(
        title="🛡️ Sunucu Qoruma Statusu",
        description="Server hazırda **Kral Bot** tərəfindən 7/24 tam qoruma altındadır!",
        color=discord.Color.blue()
    )
    embed.add_field(name="Status", value="✅ Aktiv və İşlək", inline=True)
    embed.add_field(name="Qorunan Sahələr", value="Link, Reklam, Flood, Caps Lock, Everyone", inline=True)
    embed.set_footer(text="Gecə-gündüz serverin güvəndədir!")
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Botun gecikmə sürəti: **{latency}ms**", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 **{amount}** ədəd mesaj təmizləndi!", delete_after=3)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** serverdən ban olundu! Səbəb: *{reason}*")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Qayda pozuntusu"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"⏳ **{member.mention}** {minutes} dəqiqə müddətinə susduruldu!")

# --- OYUNLAR ---
@bot.command(name="zar")
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 Zər atıldı və düşən rəqəm: **{sayi}**!")

@bot.command(name="yaziqtura")
async def yaziqtura(ctx):
    netice = random.choice(["Yazı 🪙", "Tura 🦅"])
    await ctx.send(f"🎲 Pul atıldı... Nəticə: **{netice}**!")

@bot.command(name="zarafat")
async def zarafat(ctx):
    zarafatlar = [
        "Müəllim şagirdə: — De görüm, Su nişanı nədir? Şagird: — Suya basdırdığımız möhür müəllim? 😄",
        "İki dənə dəli kosmosdan gəlir, biri deyir: 'Ay nə gözəl yer idi, amma havanı heç bəyənmədim.' 🚀",
        "– Ana, ata niyə göydə uçur? – Lal ol, uje hündürdən atma özünü!",
        "İnternetim o qədər yavaşdır ki, 'Google' axtarışa verəndə cavabını gələn il öyrənəcəm."
    ]
    await ctx.send(random.choice(zarafatlar))

token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
    @bot.command(name="salam")
async def salam_cmd(ctx):
    
    @bot.command(name="salam")
async def salam_cmd(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Xoş gəldin, qaqaş! 👋")

@bot.command(name="sa")
async def sa_cmd(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Necəsən? 👑")

@bot.command(name="slm")
async def slm_cmd(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Xoş gördük! 🤖")

    
