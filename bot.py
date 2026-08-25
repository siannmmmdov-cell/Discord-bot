import discord
from discord.ext import commands
import os
import re
import time
import asyncio
from datetime import timedelta
from collections import defaultdict, Counter

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

spam_tracker = defaultdict(list)
spam_warnings = Counter()

@bot.event
async def on_ready():
    print(f"🛡️ ULTRA GÜVƏNLİK BOTU (Bot 1) aktivdir: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!guvenlik | Server +100000 Zirehli 🔒"))

@bot.command(name="guvenlik", aliases=["status"])
async def guvenlik(ctx):
    embed = discord.Embed(
        title="🔒 +100000 Zirehli Güvənlik Paneli",
        description="Serverin aktiv müdafiə sistemləri, Ruhum:",
        color=discord.Color.red()
    )
    embed.add_field(name="🛡️ Anti-Spam / Anti-Raid", value="🟢 Aktiv (Sərt rejim)", inline=False)
    embed.add_field(name="🚫 Reklam / Dəvət Linkləri", value="🟢 Avtomatik silinir", inline=False)
    embed.add_field(name="⚠️ @everyone / @here Etiketləri", value="🟢 Bloklanıb", inline=False)
    embed.add_field(name="🔠 Caps Lock (Böyük Hərf) Filtri", value="🟢 Aktiv", inline=False)
    embed.set_footer(text="Ruhum üçün xüsusi olaraq maksimum güvənlə hazırdır.")
    await ctx.send(embed=embed)

@bot.command(name="qayda")
async def qayda(ctx):
    embed = discord.Embed(
        title="📜 Serverin Rəsmi Qaydaları",
        description="1. Hər kəsə qarşı hörmətli olmaq mütləqdir!\n"
                    "2. Spam, flood və lazımsız mesajlar qəti qadağandır!\n"
                    "3. Başqa serverlərin linkini və ya reklamını atmaq birbaşa cəzalandırılır, Ruhum!",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

# Güvənlik Filtri (Avtomatik işləyir)
@bot.event
async def on_message(message):
    if message.author.bot or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    # 1. Reklam və Link Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite)/\w+"
    if re.search(invite_regex, message.content):
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə reklam linki paylaşmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 2. @everyone və @here Qoruması
    if "@everyone" in message.content or "@here" in message.content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, kütləvi etiket atmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. Caps Lock (Həddindən artıq böyük hərf) Qoruması
    if len(message.content) > 8:
        uppercase_count = sum(1 for c in message.content if c.isupper())
        if uppercase_count / len(message.content) > 0.7:
            try:
                await message.delete()
                warn = await message.channel.send(f"⚠️ {message.author.mention}, böyük hərflə yazmaq qadağandır!")
                await asyncio.sleep(4)
                await warn.delete()
                return
            except:
                pass

    # 4. Sürətli Spam Qoruması
    author_id = message.author.id
    current_time = time.time()
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) >= 4:
        spam_tracker[author_id].clear()
        spam_warnings[author_id] += 1
        try:
            await message.delete()
        except:
            pass
        
        warn_count = spam_warnings[author_id]
        if warn_count == 1:
            await message.channel.send(f"⚠️ {message.author.mention}, zəhmət olmasa spam etmə!", delete_after=4)
        elif warn_count >= 2:
            try:
                await message.author.timeout(timedelta(minutes=3), reason="Ardıcıl spam hücumu.")
                await message.channel.send(f"⏳ {message.author.mention}, spam səbəbilə 3 dəqiqəlik mute aldın!", delete_after=4)
            except:
                pass
        return

    await bot.process_commands(message)

token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: DISCORD_TOKEN tapılmadı!")
            
