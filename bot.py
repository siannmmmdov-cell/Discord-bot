import discord
from discord.ext import commands
import os
import re
import time
from datetime import timedelta
from collections import defaultdict, Counter

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Spam və təhlükəsizlik izləmə lüğətləri
spam_tracker = defaultdict(list)
spam_warnings = Counter()

@bot.event
async def on_ready():
    print(f"==========================================")
    print(f" Zirehli Qoruma Botu Aktivləşdi!")
    print(f" Botun Adı: {bot.user.name}")
    print(f" ID: {bot.user.id}")
    print(f" Status: Server tam təhlükəsizlik altındadır!")
    print(f"==========================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Ruhumun Serverini 🛡️"))

# ==================== GÜVƏNLİK VƏ STATUS KOMUTLARI ====================

@bot.command(name="guvenlik", aliases=["güvənlik", "status"])
async def guvenlik(ctx):
    server = ctx.guild
    verification = str(server.verification_level).upper()
    
    embed = discord.Embed(
        title="🛡️ Server Güvənlik və Müdafiə Hesabatı",
        description="Botumuz tərəfindən serverin anlıq təhlükəsizlik vəziyyəti:",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="📛 Server Adı", value=server.name, inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=str(server.member_count), inline=True)
    embed.add_field(name="🔒 Doğrulama Səviyyəsi", value=verification, inline=True)
    embed.add_field(name="🤖 Mühafizə Sistemi", value="🟢 Aktiv (Anti-Spam, Anti-Link, Anti-Mention)", inline=False)
    embed.set_footer(text="Ruhum üçün xüsusi olaraq hazırlanmışdır.")
    await ctx.send(embed=embed)

@bot.command(name="salam")
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Server tam güvənlik altındadır, xoş gəldin!")

# ==================== MODERASİYA KOMUTLARI ====================

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Uğurla **{amount}** ədəd mesaj təmizləndi!")
    await asyncio.sleep(3) if 'asyncio' in globals() else None
    try:
        await msg.delete()
    except:
        pass

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** serverdən ban olundu!\n📜 Səbəb: `{reason}`")

@bot.command(name="mute", aliases=["timeout"])
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Qayda pozuntusu"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"⏳ **{member.mention}** {minutes} dəqiqə müddətinə susduruldu (timeout)!")

@bot.command(name="kilid")
@commands.has_permissions(manage_channels=True)
async def kilid(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"🔒 **{ctx.channel.mention}** kanalı mesaj yazılması üçün kilidləndi!")

@bot.command(name="ac", aliases=["aç"])
@commands.has_permissions(manage_channels=True)
async def ac(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"🔓 **{ctx.channel.mention}** kanalının kilidi açıldı!")

# ==================== AVTOMATİK QORUMA SİSTEMİ (ANTİ-SPAM & LİNK) ====================

@bot.event
async def on_message(message):
    # Botların öz mesajlarını yox sayırıq
    if message.author.bot:
        await bot.process_commands(message)
        return

    # Adminlərə heç bir qadağa tətbiq olunmur
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content

    # 1. Dəvət Linki və Reklam Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite)/\w+"
    if re.search(invite_regex, content):
        try:
            await message.delete()
            warning = await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə başqa yerlərin dəvət linkini/reklam atmaq qəti qadağandır!")
            await asyncio.sleep(5)
            await warning.delete()
            return
        except Exception:
            pass

    # 2. @everyone / @here kütləvi etiketləmə qoruması
    if "@everyone" in content or "@here" in content:
        try:
            await message.delete()
            warning = await message.channel.send(f"⚠️ {message.author.mention}, kütləvi etiket (`@everyone` / `@here`) atmaq qadağandır!")
            await asyncio.sleep(5)
            await warning.delete()
            return
        except Exception:
            pass

    # 3. Sürətli Spam Qoruması (Anti-Spam Engine)
    author_id = message.author.id
    current_time = time.time()
    
    # Son 5 saniyə içindəki mesajları izləyirik
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    # Əgər 5 saniyə ərzində 6-dan çox mesaj atarsa spam sayılır
    if len(spam_tracker[author_id]) >= 6:
        spam_tracker[author_id].clear()
        spam_warnings[author_id] += 1
        warn_count = spam_warnings[author_id]

        try:
            await message.delete()
        except:
            pass

        if warn_count == 1:
            await message.channel.send(f"⚠️ {message.author.mention}, həddindən artıq sürətli mesaj yazırsan! **1-ci Xəbərdarlıq**.", delete_after=5)
        elif warn_count == 2:
            try:
                await message.author.timeout(timedelta(seconds=30), reason="Spam etmək səbəbilə avtomatik mute.")
                await message.channel.send(f"⏳ {message.author.mention}, spam etdiyin üçün **30 saniyəlik** zaman aşımına (mute) salındın!", delete_after=5)
            except:
                pass
        elif warn_count >= 3:
            try:
                await message.author.ban(reason="Ardıcıl və qarşısıalınmaz spam hücumu.")
                await message.channel.send(f"🔨 {message.author.mention}, ardıcıl spam qaydasını pozduğu üçün serverdən **banlandı!**")
                del spam_warnings[author_id]
            except:
                pass
        return

    # Komutların işləməsi üçün vacibdir
    await bot.process_commands(message)

# Token birbaşa daxil edilib (Heç bir əlavə ayara ehtiyac yoxdur)
bot.run("MTU0MDMzMjI2NzgyNDQ4ODQ1MA.G8IEhC.1dXBFpEbTx_wCtrNLv-OCuSST73vxLL4-WV32c")
            
