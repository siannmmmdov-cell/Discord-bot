import discord
from discord.ext import commands
import os
import re
import time
import asyncio
from datetime import datetime, timedelta
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
    print(f"🛡️ GÜVƏNLİK BOTU (Bot 1) aktivdir: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!guvenlik | Server Qorunur 🔒"))

@bot.command(name="guvenlik", aliases=["status"])
async def guvenlik(ctx):
    embed = discord.Embed(
        title="🔒 +100000 Zirehli Güvənlik Paneli",
        description="Bot 1 tərəfindən idarə olunan mühafizə sistemləri:",
        color=discord.Color.red()
    )
    embed.add_field(name="🛡️ Anti-Spam / Anti-Raid", value="🟢 Aktiv (Sərt rejim)", inline=False)
    embed.add_field(name="🚫 Reklam / Link Filtri", value="🟢 Avtomatik silmə aktiv", inline=False)
    embed.add_field(name="⚠️ Kütləvi Etiket (@everyone)", value="🟢 Bloklanıb", inline=False)
    embed.set_footer(text="Ruhum üçün xüsusi güvəndədir.")
    await ctx.send(embed=embed)

@bot.command(name="qayda")
async def qayda(ctx):
    await ctx.send("📜 **Server Qaydaları:**\n1. Hörmətsizlik yasaqdır!\n2. Spam və flood etmək qəti qadağandır!\n3. Reklam linki atmaq birbaşa cəzalandırılır, Ruhum!")

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
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə reklam və dəvət linki paylaşmaq qadağandır!")
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

    # 3. Sürətli Spam Qoruması (+100000 Güvənlik)
    author_id = message.author.id
    current_time = time.time()
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) >= 4: # 5 saniyə ərzində 4 mesajdan çox
        spam_tracker[author_id].clear()
        spam_warnings[author_id] += 1
        try:
            await message.delete()
        except:
            pass
        
        warn_count = spam_warnings[author_id]
        if warn_count == 1:
            await message.channel.send(f"⚠️ {message.author.mention}, spam etməyi dayandır!", delete_after=4)
        elif warn_count >= 2:
            try:
                await message.author.timeout(timedelta(minutes=2), reason="Ardıcıl spam hücumu.")
                await message.channel.send(f"⏳ {message.author.mention}, spam səbəbilə 2 dəqiqəlik mute aldın!", delete_after=4)
            except:
                pass
        return

    await bot.process_commands(message)

token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
          
