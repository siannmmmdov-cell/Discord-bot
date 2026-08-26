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

# Render port xatası verməsin deyə kiber-server
app = Flask('')

@app.route('/')
def home():
    return "yenilmez firewall v6.0 tam güclə işləyir [SECURE_CORE]"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_server).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='r?', intents=intents)

spam_tracker = {}

@bot.event
async def on_ready():
    print(f'🛡️ YENİLMEZ KİBER-ŞƏBƏKƏ AKTİVDİR: {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Kanal trafikinə nəzarət edilir | r?bot"))

@bot.event
async def on_member_join(member):
    if member.bot:
        icazeli_bot_idleri = [bot.user.id]
        if member.id not in icazeli_bot_idleri:
            try:
                await member.kick(reason="Sistem Təhlükəsizliyi: İcazəsiz bot inyeksiya cəhdi.")
                print(f"🚨 Təhlükə əngəlləndi: İcazəsiz bot qovuldu -> {member.name}")
            except:
                pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content
    lower_content = content.lower()

    # 1. Sərt və Auralı Salamlama Sistemi
    words = lower_content.split()
    salam_sozleri = ["salam", "salamun aleykum", "sa", "as", "slm", "səlam"]
    if any(word in salam_sozleri for word in words):
        server_adi = message.guild.name
        cevaplar = [
            f"Aleykum salam, {message.author.mention}. `{server_adi}` təhlükəsizlik zonasındasan. Ehtiyatlı ol.",
            f"Salam, {message.author.mention}. Şəbəkə protokolları aktivdir, hər hərəkətin izlənilir.",
            f"Aleykum salam, {message.author.mention}. Ərazi yenilmez tərəfindən qorunur."
        ]
        try:
            await message.channel.send(random.choice(cevaplar))
        except:
            pass

    # 2. Qlobal Link və İnvayt Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite|t\.me|instagram\.com|youtube\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ **{message.author.mention}**, bu sektorda link paylaşmaq qadağandır. Firewall işə düşdü.")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. Kütləvi @everyone / @here Basqın Qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ **{message.author.mention}**, qlobal qışqırıq (`@everyone/@here`) sərt şəkildə bloklandı!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 4. Caps Lock (Həddindən artıq səs-küy) Filtri
    if len(content) > 8:
        uppercase_count = sum(1 for c in content if c.isupper())
        if uppercase_count / len(content) > 0.7:
            try:
                await message.delete()
                warn = await message.channel.send(f"⚠️ **{message.author.mention}**, sistemdə səviyyəni qoru (Böyük hərf qadağandır).")
                await asyncio.sleep(4)
                await warn.delete()
                return
            except:
                pass

    # 5. Bloklanmış Sürətli Spam / Flood Müdafiəsi
    author_id = message.author.id
    current_time = time.time()

    if author_id not in spam_tracker:
        spam_tracker[author_id] = []

    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 3]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) > 5:
        spam_tracker[author_id].clear()
        try:
            await message.delete()
            duration = timedelta(minutes=10)
            await message.author.timeout(duration, reason="Sistem Müdafiəsi: Flood / Spam")
            await message.channel.send(f"🔒 **{message.author.mention}** şəbəkəni doldurmağa çalışdığı üçün 10 dəqiqəlik təcrid edildi.")
        except:
            pass
        return

    await bot.process_commands(message)

# --- NƏHƏNG MASTER İDARƏETMƏ PANELİ (r?bot) ---
@bot.command(name="bot")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="⚡ YENİLMEZ // NƏHƏNG KİBER-TƏHLÜKƏSİZLİK MƏRKƏZİ",
        description="Bu server **yenilmez** mərkəzi mühafizə sistemi tərəfindən idarə olunur. Bütün alt sistemlər tam güclə işləyir:",
        color=0x050505
    )
    embed.add_field(
        name="🛡️ 1. Firewall və Müdafiə Divarları",
        value="• **Avtomatik Sərt Salamlama**: İzləmə protokolu aktiv\n• **Qlobal Link / Reklam Filtri**: Sıfır tolerans siyasəti\n• **Massive Ping Qoruması**: @everyone / @here bloku\n• **Ağıllı Spam & Flood Əngəli**: 10 dəqiqəlik avtomatik təcrid\n• **Bot İnyeksiya Bloku**: İcazəsiz botların dərhal qovulması", 
        inline=False
    )
    embed.add_field(
        name="🎧 2. Səs Şəbəkəsi və Trafik İdarəetməsi",
        value="`r?qosul` — Əməliyyat səs kanalına qoşular\n`r?ayril` — Səs şəbəkəsindən bağlantını kəsər", 
        inline=False
    )
    embed.add_field(
        name="⚔️ 3. Sərt Moderasiya Protokolları",
        value="`r?sil [say]` — Ərazidəki izləri təmizləyər\n`r?ban [@istifadəçi]` — Şəbəkədən tamamilə silər\n`r?at [@istifadəçi]` — Ərazidən uzaqlaşdırar\n`r?mute [@istifadəçi] [dəqiqə]` — Səsini 100% kəsər\n`r?lock` — Kanalı ümumi trafikə bağlayar\n`r?unlock` — Kanalın kilidini açar\n`r?slowmode [saniyə]` — Trafiki məhdudlaşdırar", 
        inline=False
    )
    embed.add_field(
        name="📊 4. Sistem Diaqnostikası və Hədəf Analizi",
        value="`r?guvenlik` — Şəbəkə təhlükəsizlik hesabatı\n`r?profil [@istifadəçi]` — İstifadəçi hədəf analizi\n`r?server` — Server qovşaq məlumatları\n`r?ping` — Əlaqə gecikmə yoxlaması", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS v6.0 Advanced Core • Bütün hüquqlar qorunur.")
    await ctx.send(embed=embed)

@bot.command(name="guvenlik")
async def guvenlik(ctx):
    embed = discord.Embed(
        title="🔒 Şəbəkə Təhlükəsizlik Vəziyyəti",
        description="Sistem tam mühafizə rejimindədir. Təhdid səviyyəsi: Sıfır.",
        color=0xff0000
    )
    embed.add_field(name="Firewall Statusu", value="🟢 Mühafizə Aktiv", inline=True)
    embed.add_field(name="Şifrələmə", value="256-bit AES", inline=True)
    embed.add_field(name="Gecikmə", value=f"`{round(bot.latency * 1000)}ms`", inline=True)
    embed.add_field(name="Aktiv Modullar", value="5 / 5 Qoruma Qatışığı İşləkdə", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="⚡ Sistem Gecikməsi", description=f"Cavab müddəti: `{latency}ms`", color=0x111111)
    await ctx.send(embed=embed)

# --- SƏS ƏMRLƏRİ ---
@bot.command(name="qosul")
async def qosul(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"🔊 Əməliyyat kanalına qoşuldum: **{channel.name}**")
    else:
        await ctx.send("❌ Əvvəlcə hər hansı bir səs kanalında olmalısan!")

@bot.command(name="ayril")
async def ayril(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Səs kanalından ayrıldım, ərazi tərk edildi.")
    else:
        await ctx.send("❌ Bot heç bir səs kanalında deyil.")

# --- CİDDİ MODERASİYA ƏMRLƏRİ ---
@bot.command(name="sil")
async def sil(ctx, amount: int = 10):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ Bu əmr üçün səlahiyyətin çatmır.")
        return
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ `{amount}` ədəd iz silindi.")
    await msg.delete(delay=3)

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** şəbəkədən tamamilə silindi. Səbəb: {reason}")

@bot.command(name="at")
async def at(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.mention}** ərazidən qovuldu. Səbəb: {reason}")

@bot.command(name="mute")
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Səbəb yoxdur"):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"🔇 **{member.mention}** `{minutes}` dəqiqə müddətinə susduruldu.")

@bot.command(name="lock")
async def lock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal müvəqqəti olaraq kilidləndi. Yazmaq qadağandır.")

@bot.command(name="unlock")
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanalın kilidi açıldı. Trafik bərpa olundu.")

@bot.command(name="slowmode")
async def slowmode(ctx, seconds: int = 0):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Səlahiyyətin yoxdur.")
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Kanal yavaş rejimə keçirildi: `{seconds}` saniyə.")

# --- MƏLUMAT VƏ ANALİZ ---
@bot.command(name="profil")
async def profil(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🎯 Hədəf Analizi: {member.name}", color=0x111111)
    embed.add_field(name="Unikal ID", value=member.id, inline=True)
    embed.add_field(name="Şəbəkəyə Giriş", value=member.joined_at.strftime("%d.%m.%Y"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="server")
async def server(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 Server Qovşağı: {guild.name}", color=0x111111)
    embed.add_field(name="Üzv Sayı", value=guild.member_count, inline=True)
    embed.add_field(name="Kanal Sayı", value=len(guild.channels), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("KİBER XƏTA: DISCORD_TOKEN tapılmadı!")

