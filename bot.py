import discord
from discord.ext import commands
import re
import time
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="#", help_command=None, intents=intents)

anti_spam_status = {}
user_message_counts = {}
user_last_message = {}

def clean_text(text):
    text = text.lower()
    replacements = {
        '1': 'i', '!': 'i', '|': 'i', '3': 'e', '4': 'a', '@': 'a',
        '0': 'o', '5': 's', '$': 's', '7': 't', '+': 't', '8': 'b'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text, text.replace(" ", "")

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="BELARUSYA | #yardim")
    await bot.change_presence(activity=activity)
    print(f"BELARUSYA Qoruma Botu aktivdir: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    guild_id = message.guild.id if message.guild else None
    
    if guild_id and not anti_spam_status.get(guild_id, True):
        await bot.process_commands(message)
        return

    content = message.content
    cleaned, cleaned_no_space = clean_text(content)

    if not message.author.guild_permissions.administrator:
        # Link qoruması
        if any(domain in cleaned_no_space for domain in ["discord.gg", "http://", "https://", "t.me", "discord.com/invite"]):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, BELARUSYA serverində link paylaşmaq qadağandır!", delete_after=4)
                return
            except:
                pass

        # Həqiqi Spam / Flood qoruması (normal söhbətə toxunmur)
        author_id = message.author.id
        current_time = time.time()
        
        if author_id not in user_message_counts:
            user_message_counts[author_id] = []

        last_msg = user_last_message.get(author_id, ("", 0))
        if last_msg[0] == content and current_time - last_msg[1] < 4:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, eyni mesajı təkrar spam etmə!", delete_after=3)
                return
            except:
                pass
        user_last_message[author_id] = (content, current_time)

        user_message_counts[author_id] = [t for t in user_message_counts[author_id] if current_time - t < 3]
        user_message_counts[author_id].append(current_time)

        if len(user_message_counts[author_id]) > 6:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, zəhmət olmasa bir az yavaş yaz.", delete_after=3)
                return
            except:
                pass

    await bot.process_commands(message)

# --- CİDDİ VƏ SƏLİQƏLİ KOMUTLAR ---

@bot.command(name="yardim", aliases=["help"])
async def yardim(ctx):
    embed = discord.Embed(title="🛡️ BELARUSYA — Təhlükəsizlik və İdarəetmə", description="Serverin nizam-intizamını qoruyan rəsmi sistem.", color=0x2b2d31)
    embed.add_field(name="🔗 Dəvət Linki", value="`#url` - Serverin xüsusi linkini göstərir.", inline=False)
    embed.add_field(name="⚙️ Anti-Spam", value="`#antispam enable / disable` - Sistemi idarə edir.", inline=False)
    embed.add_field(name="🧹 Mesaj Təmizliyi", value="`#sil [say]` - Göstərilən qədər mesajı silir.", inline=False)
    embed.add_field(name="📊 Server Bilgi", value="`#serverbilgi` - Server haqqında məlumat verir.", inline=False)
    embed.add_field(name="🏓 Gecikmə", value="`#ping` - Botun cavab sürətini ölçür.", inline=False)
    embed.set_footer(text="BELARUSYA Security Systems")
    await ctx.send(embed=embed)

@bot.command(name="antispam")
@commands.has_permissions(administrator=True)
async def antispam(ctx, status: str):
    guild_id = ctx.guild.id
    if status.lower() == "enable":
        anti_spam_status[guild_id] = True
        await ctx.send("🛡️ **BELARUSYA Anti-Spam sistemi aktivləşdirildi.**")
    elif status.lower() == "disable":
        anti_spam_status[guild_id] = False
        await ctx.send("⚠️ **BELARUSYA Anti-Spam sistemi söndürüldü.**")
    else:
        await ctx.send("İstifadə qaydası: `#antispam enable` və ya `#antispam disable`")

@bot.command(name="url")
async def server_url(ctx):
    if ctx.guild.vanity_url_code:
        try:
            vanity = await ctx.guild.vanity_invite()
            await ctx.send(f"🔗 **BELARUSYA Dəvət Linki:** discord.gg/{vanity.code} (İstifadə: {vanity.uses})")
        except:
            await ctx.send(f"🔗 **BELARUSYA Dəvət Linki:** discord.gg/{ctx.guild.vanity_url_code}")
    else:
        await ctx.send(f"🔗 **BELARUSYA Serveri**")

@bot.command(name="sil", aliases=["temizle"])
@commands.has_permissions(manage_messages=True)
async def sil(ctx, limit: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=limit)
    await ctx.send(f"🧹 {len(deleted)} ədəd mesaj təmizləndi.", delete_after=3)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Botun gecikmə sürəti: **{latency}ms**")

@bot.command(name="serverbilgi")
async def serverbilgi(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"📊 {guild.name} — Server Məlumatı", color=0x2b2d31)
    embed.add_field(name="👑 Server Sahibçisi", value=guild.owner, inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Yaradılma Tarixi", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member}** serverdən uzaqlaşdırıldı. Səbəb: {reason}")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member}** serverdən qovuldu. Səbəb: {reason}")

bot.run(os.getenv("DISCORD_TOKEN"))
  
