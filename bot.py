import discord
from discord.ext import commands
import os
import re
import time
from datetime import timedelta
from flask import Flask
import threading

# Flask serveri (Render port xətası verməsin deyə avtomatik port)
app = Flask('')

@app.route('/')
def home():
    return "Güvənlik Botu aktivdir!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_server).start()

# Bot icazələri (Intents)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=".", intents=intents)

# Güvənlik üçün izləmə lüğətləri
spam_tracker = {}
spam_warnings = {}

@bot.event
async def on_ready():
    print(f"🛡️ GÜVƏNLİK BOTU +100000 AKTİVDİR: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Server Qorunur | .yardim"))

# --- GÜVƏNLİK FİLTRLƏRİ (AVTOMATİK İŞLƏYİR) ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Adminlərə güvənlik qadağaları şamil olunmur
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content

    # 1. Reklam və Link Qoruması (.gg, discord.com və s.)
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite|t\.me|instagram\.com)/\S+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə reklam və link atmaq qəti qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 2. @everyone və @here Spam Qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warn = await message.channel.send(f"⚠️ {message.author.mention}, @everyone və ya @here atmaq qadağandır!")
            await asyncio.sleep(4)
            await warn.delete()
            return
        except:
            pass

    # 3. Həddindən artıq Böyük Hərf (Caps Lock) Qoruması (>70%)
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

    # 4. Sürətli Spam Qoruması (Flood)
    author_id = message.author.id
    current_time = time.time()
    
    if author_id not in spam_tracker:
        spam_tracker[author_id] = []
    
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) >= 4:
        spam_tracker[author_id].clear()
        if author_id not in spam_warnings:
            spam_warnings[author_id] = 0
        spam_warnings[author_id] += 1
        
        try:
            await message.delete()
        except:
            pass

        warn_count = spam_warnings[author_id]
        if warn_count == 1:
            await message.channel.send(f"⚠️ {message.author.mention}, spam etməyi dayandır, yoxsa cəza alacaqsan!")
        elif warn_count >= 2:
            try:
                duration = timedelta(minutes=3)
                await message.author.timeout(duration, reason="Çox sürətli spam (Flood)")
                await message.channel.send(f"⏳ {message.author.mention}, spam yazdığı üçün 3 dəqiqəlik timeout (susdurulma) aldı!")
            except:
                pass
        return

    await bot.process_commands(message)

# --- BOT ƏMRLƏRİ ---
@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="🛡️ Güvənlik və İdarəetmə Paneli (+100000)",
        description="Server tam qoruma altındadır, Ruhum:",
        color=discord.Color.red()
    )
    embed.add_field(name="🧹 `.sil [say]`", value="Mesajları təmizləyir.", inline=False)
    embed.add_field(name="🔨 `.ban [@istifadəçi]`", value="Qayda pozanı banlayır.", inline=False)
    embed.add_field(name="⏳ `.mute [@istifadəçi] [dəqiqə]`", value="İstifadəçini susdurur.", inline=False)
    embed.add_field(name="🏓 `.ping`", value="Botun sürətini ölçür.", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Gecikmə: **{latency}ms** (Güvənlik sistemi işləkdir)")

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 **{amount}** mesaj təmizləndi!", delete_after=3)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Təhlükəli davranış"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** serverdən uzaqlaşdırıldı!")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Qayda pozuntusu"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"⏳ **{member.mention}** {minutes} dəqiqəlik timeout aldı!")

# Token oxuma hissəsi (İkinci token üçün)
token = os.environ.get("DISCORD_TOKEN_2")
if token:
    bot.run(token)
            
