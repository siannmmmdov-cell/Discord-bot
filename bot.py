import discord
from discord.ext import commands
import os
import re
import time
from collections import defaultdict, Counter

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# İkinci bot üçün prefiks nöqtə (.) olur
bot = commands.Bot(command_prefix=".", intents=intents)

# Spam və xəbərdarlıq izləmə sistemləri
spam_tracker = defaultdict(list)
spam_warnings = Counter()

@bot.event
async def on_ready():
    print(f"İkinci Ağır Mühafizə Botu işə düşdü, Ruhum: {bot.user}")

# 1. Ətraflə Durum Komutu
@bot.command()
async def durum(ctx):
    server = ctx.guild
    await ctx.send(
        f"🔒 **İkinci Mühafizə Sistemi (Ruhum üçün Hesabat):**\n"
        f"- Sunucu: {server.name}\n"
        f"- Toplam Kanal: {len(server.channels)}\n"
        f"- Toplam Rol: {len(server.roles)}\n"
        f"- Üzv Sayı: {server.member_count}\n"
        f"🛡️ *Status: 2-ci qat qoruma tam aktivdir!*"
    )

# 2. Qaydalar Komutu
@bot.command()
async def qayda(ctx):
    await ctx.send(
        f"📜 **Serverin Əsas Qaydaları:**\n"
        f"1. Heç bir halda reklam və dəvət linki atmaq olmaz!\n"
        f"2. Flood və ya ardıcıl spam etmək qadağandır!\n"
        f"3. Caps Lock (böyük hərflərlə qışqıraraq yazmaq) yasaqdır!\n"
        f"4. Hörmətsizlik dərhal cəzalandırılır, Ruhum!"
    )

# 3. Ping / Gecikmə Komutu
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Botun gecikmə sürəti: **{latency}ms**")

# 4. Çoxtərəfli Qoruma və Filtrləmə Sistemi (Automod)
@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

    # Adminlərə qoruma filtrləri tətbiq olunmur
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content

    # A) Reklam / Dəvət Linki Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite)/\w+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, bu ikinci qatda reklam linki atmaq qəti qadağandır!", delete_after=5)
            return
        except Exception:
            pass

    # B) Qadağan Olunmuş Sözlər Filtri
    qadagan_sozler = ["pissoz1", "pissoz2", "koylu"] # İstədiyin sözləri bura əlavə edə bilərsən
    if any(soz in content.lower() for soz in qadagan_sozler):
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, bu sözü və ya ifadəni işlətmək yasaqdır!", delete_after=5)
            return
        except Exception:
            pass

    # C) Həddindən Artıq Böyük Hərf (Anti-Caps Lock) Qoruması
    if len(content) > 10:
        biyuk_herf_sayi = sum(1 for c in content if c.isupper())
        if (biyuk_herf_sayi / len(content)) > 0.7: # Əgər mətnin 70%-dən çoxu böyük hərflərdirsə
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, zəhmət olmasa Caps Lock-u söndür, qışqıraraq yazmaq qadağandır!", delete_after=5)
                return
            except Exception:
                pass

    # D) Flood / Spam Qoruması (7 mesaj və ya sürətli təkrar)
    author_id = message.author.id
    current_time = time.time()
    
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) >= 7:
        spam_tracker[author_id].clear()
        spam_warnings[author_id] += 1
        warn_count = spam_warnings[author_id]

        try:
            await message.delete()
        except Exception:
            pass

        if warn_count == 1:
            await message.channel.send(f"⚠️ {message.author.mention}, ikinci qoruma sistemi: Sürətli mesaj (spam) xəbərdarlığı!", delete_after=5)
        elif warn_count == 2:
            try:
                from datetime import timedelta
                await message.author.timeout(timedelta(seconds=15), reason="İkinci qat: Spam etdiyi üçün 15 saniyəlik timeout.")
                await message.channel.send(f"⏳ {message.author.mention}, təkrar spam etdiyin üçün 15 saniyəlik zaman aşımına salındın!", delete_after=5)
            except Exception:
                pass
        elif warn_count >= 3:
            try:
                await message.author.ban(reason="İkinci qat: Ardıcıl spam qaydasını pozduğu üçün banlandı.")
                await message.channel.send(f"🔨 {message.author.mention}, spamda israr etdiyin üçün serverdən uzaqlaşdırıldın!")
                del spam_warnings[author_id]
            except Exception:
                pass
        return

    await bot.process_commands(message)

# İkinci botun tokeni
bot.run(os.environ.get("DISCORD_TOKEN_2"))
