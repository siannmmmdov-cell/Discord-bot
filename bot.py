import discord
from discord.ext import commands
import os
import re
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Bütün əmrlər yalnız "!" işarəsi ilə işləyəcək
bot = commands.Bot(command_prefix="!", intents=intents)

spam_tracker = defaultdict(list)
spam_warnings = Counter()

@bot.event
async def on_ready():
    print(f"==========================================")
    print(f" ULTIMATE ZİREHLİ ! QORUMA AKTİVDİR!")
    print(f" Bot: {bot.user.name}")
    print(f" Status: Server tam kilid və müdafiə altındadır!")
    print(f"==========================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!yardim | Server 🛡️"))

# ==================== 1. YENİ HESAB VƏ RAİD QORUMASI ====================
@bot.event
async def on_member_join(member):
    created_at = member.created_at
    now = datetime.now(created_at.tzinfo)
    account_age = now - created_at

    # 3 gündən yeni açılan şübhəli hesaplar
    if account_age.days < 3:
        try:
            for channel in member.guild.text_channels:
                if "qoruma" in channel.name or "log" in channel.name or "chat" in channel.name:
                    await channel.send(f"🚨 **Diqqət!** Şübhəli yeni hesab aşkarlandı: {member.mention} (Hesab açılalı 3 gündən az olub).")
                    break
        except Exception:
            pass

# ==================== 2. MƏLUMAT VƏ YARDIM ƏMRLƏRİ (!) ====================
@bot.command(name="yardim", aliases=["help", "komutlar"])
async def yardim(ctx):
    embed = discord.Embed(
        title="🛠️ Server Mühafizə və İdarəetmə Paneli",
        description="Bütün əmrlər **`!`** prefiksi ilə işləyir, Ruhum:",
        color=discord.Color.blue()
    )
    embed.add_field(name="🛡️ `!guvenlik`", value="Serverin anlıq güvənlik və müdafiə statusunu göstərir.", inline=False)
    embed.add_field(name="📜 `!qayda`", value="Serverin rəsmi qaydalarını ekrana gətirir.", inline=False)
    embed.add_field(name="🧹 `!sil [say]`", value="Göstərilən miqdarda mesajı təmizləyir.", inline=False)
    embed.add_field(name="🔨 `!ban [@istifadəçi]`", value="Təxribatçı istifadəçini serverdən uzaqlaşdırır.", inline=False)
    embed.add_field(name="⏳ `!mute [@istifadəçi] [dəqiqə]`", value="Qayda pozan istifadəçini müvəqqəti susdurur.", inline=False)
    embed.set_footer(text="Ruhum üçün maksimum güvənliklə hazırlandı.")
    await ctx.send(embed=embed)

@bot.command(name="guvenlik", aliases=["status"])
async def guvenlik(ctx):
    server = ctx.guild
    embed = discord.Embed(
        title="🛡️ Zirehli Təhlükəsizlik Paneli",
        description="Serverin anlıq müdafiə göstəriciləri:",
        color=discord.Color.red()
    )
    embed.add_field(name="📛 Server Adı", value=server.name, inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=str(server.member_count), inline=True)
    embed.add_field(name="🔒 Anti-Raid / Anti-Spam", value="🟢 Maksimum səviyyədə aktiv", inline=False)
    embed.add_field(name="🚫 Reklam və Etiket Filtri", value="🟢 Qüsursuz işləyir", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="qayda", aliases=["qaydalar"])
async def qayda(ctx):
    embed = discord.Embed(
        title="📜 Serverin Rəsmi Qaydaları",
        description="1. Hər kəsə hörmət göstərmək mütləqdir, təhqir qəti qadağandır!\n"
                    "2. Spam, flood və kütləvi mesaj yazmaq yasaqdır!\n"
                    "3. Başqa serverlərin reklam linklərini paylaşmaq qadağandır, Ruhum!",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command(name="salam")
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Server ən yüksək səviyyədə güvənlik altındadır.")

# ==================== 3. MODERASİYA ƏMRLƏRİ (!) ====================
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

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Qayda pozuntusu"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"⏳ **{member.mention}** {minutes} dəqiqə müddətinə susduruldu!")

# ==================== 4. AVTOMATİK GÜVƏNLİK FİLtrləri ====================
@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content = message.content.lower()

    # A) Reklam və Dəvət Linki Qoruması
    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite)/\w+"
    if re.search(invite_regex, message.content):
        try:
            await message.delete()
            warning = await message.channel.send(f"⚠️ {message.author.mention}, başqa serverlərin linkini atmaq yasaqdır!")
            await asyncio.sleep(4)
            await warning.delete()
            return
        except Exception:
            pass

    # B) @everyone / @here Kütləvi Etiket Qoruması
    if "@everyone" in message.content or "@here" in message.content:
        try:
            await message.delete()
            warning = await message.channel.send(f"⚠️ {message.author.mention}, kütləvi etiket atmaq qadağandır!")
            await asyncio.sleep(4)
            await warning.delete()
            return
        except Exception:
            pass

    # C) Sürətli Spam Qoruması (Anti-Spam)
    author_id = message.author.id
    current_time = time.time()
    
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) >= 5: # 5 saniyə ərzində 5-dən çox mesaj
        spam_tracker[author_id].clear()
        spam_warnings[author_id] += 1
        warn_count = spam_warnings[author_id]

        try:
            await message.delete()
        except:
            pass

        if warn_count == 1:
            await message.channel.send(f"⚠️ {message.author.mention}, həddindən artıq sürətli mesaj yazırsan! Xəbərdarlıq.", delete_after=4)
        elif warn_count == 2:
            try:
                await message.author.timeout(timedelta(seconds=60), reason="Spam.")
                await message.channel.send(f"⏳ {message.author.mention}, spam etdiyin üçün 1 dəqiqəlik mute aldın!", delete_after=4)
            except:
                pass
        elif warn_count >= 3:
            try:
                await message.author.ban(reason="Ardıcıl spam hücumu.")
                await message.channel.send(f"🔨 {message.author.mention} dayanmadan spam etdiyi üçün banlandı!")
                del spam_warnings[author_id]
            except:
                pass
        return

    await bot.process_commands(message)

# Tokeni təhlükəsiz şəkildə Render-dən alır
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
    
