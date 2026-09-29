import discord
from discord.ext import commands
import re
import time
import os
from collections import defaultdict
from flask import Flask
from threading import Thread

# --- RENDER PORT XƏTASINI ARADAN QALDIRMAQ ÜÇÜN FLASK SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "BELARUSYA Bot aktivdir!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# -------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.webhooks = True
intents.guilds = True
intents.moderation = True

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

# Sənin ID-n
OWNER_ID = 641014966312501259

anti_spam_status = {}
user_message_counts = {}
user_last_message = {}
ban_action_counts = defaultdict(list)

caps_warnings = defaultdict(int)
long_text_warnings = defaultdict(int)

def clean_text(text):
    text = text.lower()
    replacements = {
        '1': 'i', 'İ': 'i', 'l': 'i', 'ı': 'i', '3': 'e', 'Ə': 'e', '4': 'a', '0': 'a',
        'O': 'o', '5': 's', '$': 's', '7': 't', '+': 't', '8': 'b', '9': 'g'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text.replace(" ", "")

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="BELARUSYA : @yardim")
    await bot.change_presence(activity=activity)
    print(f"BELARUSYA Təhlükəsizlik Botu tam aktivdir: {bot.user}")

# --- 1. İNSİZ WEBHOOK QORUMASI ---
@bot.event
async def on_webhooks_update(channel):
    try:
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            if webhook.user and webhook.user.id != OWNER_ID:
                await webhook.delete(reason=f"{channel.guild.name}: Sahibindən başqasına WebHook yaratmaq qadağandır!")
    except:
        pass

# --- 2. İNSİZ KANAL YARADILMASI QORUMASI ---
@bot.event
async def on_guild_channel_create(channel):
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
            if entry.user and entry.user.id != OWNER_ID:
                await channel.delete(reason=f"{channel.guild.name}: Sahibindən başqasına kanal açmaq qadağandır!")
    except:
        pass

# --- 3. İNSİZ ROL YARADILMASI QORUMASI ---
@bot.event
async def on_guild_role_create(role):
    try:
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            if entry.user and entry.user.id != OWNER_ID:
                await role.delete(reason=f"{role.guild.name}: Sahibindən başqasına rol açmaq qadağandır!")
    except:
        pass

# --- 4. ANİ-NUKE (Kütləvi ban qoruması) ---
@bot.event
async def on_member_ban(guild, user):
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            actor = entry.user
            if actor and actor.id != bot.user.id and actor.id != OWNER_ID:
                current_time = time.time()
                ban_action_counts[actor.id].append(current_time)
                
                ban_action_counts[actor.id] = [t for t in ban_action_counts[actor.id] if current_time - t < 10]
                if len(ban_action_counts[actor.id]) > 3:
                    member = guild.get_member(actor.id)
                    if member:
                        try:
                            await member.ban(reason=f"{guild.name} Anti-Nuke: İcazəsiz kütləvi ban!")
                        except:
                            pass
    except:
        pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.guild:
        return

    guild_id = message.guild.id

    if guild_id and not anti_spam_status.get(guild_id, True):
        await bot.process_commands(message)
        return

    content = message.content
    cleaned = clean_text(content)

    if message.author.id == OWNER_ID:
        await bot.process_commands(message)
        return

    # Kütləvi etiketləmə qoruması
    if message.mention_everyone or len(message.mentions) > 3:
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, yavaş yaz, kütləvi etiketləmə qadağandır!")
            return
        except:
            pass

    # Çox Uzunluqdan Artıq Yazı Qoruması (150 simvoldan çox)
    if len(content) > 150:
        try:
            await message.delete()
            long_text_warnings[message.author.id] += 1
            count = long_text_warnings[message.author.id]

            if count >= 3:
                long_text_warnings[message.author.id] = 0
                duration = discord.utils.utcnow() + discord.timedelta(minutes=5)
                await message.author.timeout(duration, reason="Həddindən artıq uzun mesaj spamı.")
                await message.channel.send(f"{message.author.mention}, həddindən artıq uzun mesaj yazdığın üçün 5 dəqiqəlik dincəl.")
            else:
                await message.channel.send(f"{message.author.mention}, zəhmət olmasa bu qədər uzun dastan yazma! ({count}/3)")
            return
        except:
            pass

    # Caps Lock Qoruması
    if len(content) > 10 and sum(1 for c in content if c.isupper()) / len(content) > 0.7:
        try:
            await message.delete()
            caps_warnings[message.author.id] += 1
            count = caps_warnings[message.author.id]

            if count >= 3:
                caps_warnings[message.author.id] = 0
                duration = discord.utils.utcnow() + discord.timedelta(minutes=5)
                await message.author.timeout(duration, reason="Caps Lock spamı.")
                await message.channel.send(f"{message.author.mention}, qışqıraraq yazdığın üçün 5 dəqiqəlik timeout aldın.")
            else:
                await message.channel.send(f"{message.author.mention}, zəhmət olmasa kapsları (Caps Lock) söndür! ({count}/2)")
            return
        except:
            pass

    # Link Qoruması
    if any(domain in cleaned for domain in ["discord.gg", "http://", "https://", "t.me", "discord.com/invite"]):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, başqa serverin linkini atmaq qadağandır!")
            return
        except:
            pass

    # Təkrar Mesaj Spam Qoruması
    author_id = message.author.id
    current_time = time.time()

    if author_id not in user_message_counts:
        user_message_counts[author_id] = []

    last_msg = user_last_message.get(author_id, ("", 0))
    if last_msg[0] == content and current_time - last_msg[1] < 4:
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, eyni mesajı təkrar spam etmə!")
            return
        except:
            pass

    user_last_message[author_id] = (content, current_time)

    # Sürətli Flood Qoruması
    user_message_counts[author_id] = [t for t in user_message_counts[author_id] if current_time - t < 3]
    user_message_counts[author_id].append(current_time)

    if len(user_message_counts[author_id]) > 5:
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, çox sürətli yazırsan, bir az yavaş ol.")
            return
        except:
            pass

    await bot.process_commands(message)

# --- KOMANDALAR (YALNIZ SƏNİN ÜÇÜN İŞLƏYİR) ---

@bot.command(name="yardim", aliases=["help"])
async def yardim(ctx):
    if ctx.author.id != OWNER_ID:
        return

    embed = discord.Embed(title="🛡️ Təhlükəsizlik Sistemi", description="Serverin nizam-intizamını qoru", color=0x2b2d31)
    embed.add_field(name="🔗 Davət Linki", value="!url - Serverin dəvət linkini göstərir.", inline=False)
    embed.add_field(name="🛡️ Anti-Spam", value="!antispam enable / disable - Məhafizəni idarə edir.", inline=False)
    embed.add_field(name="🔒 Kanal Kilidi", value="!lock / !unlock - Kanalı yazışmaya bağlayır/açır.", inline=False)
    embed.add_field(name="🧹 Mesaj Təmizliyi", value="!sil [say] - Mesajları təmizləyir.", inline=False)
    embed.add_field(name="📊 Server Bilgisi", value="!serverbilgisi - Server haqqında məlumat verir.", inline=False)
    embed.add_field(name="🏓 Gecikmə", value="!ping - Botun sürətini yoxlayır.", inline=False)
    embed.set_footer(text=f"{ctx.guild.name} Security Systems")
    await ctx.send(embed=embed)

@bot.command(name="antispam")
async def antispam(ctx, status: str):
    if ctx.author.id != OWNER_ID:
        return

    guild_id = ctx.guild.id
    if status.lower() == "enable":
        anti_spam_status[guild_id] = True
        await ctx.send(f"⚠ {ctx.guild.name} Təhlükəsizlik sistemi aktivləşdirildi.")
    elif status.lower() == "disable":
        anti_spam_status[guild_id] = False
        await ctx.send(f"⚠️ {ctx.guild.name} Təhlükəsizlik sistemi söndürüldü.")
    else:
        await ctx.send("⚠️ İstifadə qaydası: `!antispam enable` və ya `!antispam disable`")

@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.id != OWNER_ID:
        return

    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"🔒 **Bu kanal ({ctx.guild.name}) təhlükəsizlik protokolu ilə kilidləndi.**", delete_after=5)

@bot.command(name="unlock")
async def unlock(ctx):
    if ctx.author.id != OWNER_ID:
        return

    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"🔓 **Kanalın kilidi açıldı, {ctx.guild.name} sakinləri yenidən yazışa bilərsiniz.**", delete_after=5)

@bot.command(name="url")
async def server_url(ctx):
    if ctx.author.id != OWNER_ID:
        return

    if ctx.guild.vanity_url_code:
        try:
            vanity = await ctx.guild.vanity_invite()
            await ctx.send(f"🔗 **{ctx.guild.name} Dəvət Linki:** discord.gg/{vanity.code} (İstifadə: {vanity.uses})")
        except:
            await ctx.send(f"🔗 **{ctx.guild.name} Dəvət Linki:** discord.gg/{ctx.guild.vanity_url_code}")
    else:
        await ctx.send(f"❌ **{ctx.guild.name}** Serverinin xüsusi (vanity) linki yoxdur.")

@bot.command(name="sil", aliases=["təmizlə"])
async def sil_komanda(ctx, limit: int = 5):
    if ctx.author.id != OWNER_ID:
        return

    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=limit)
    await ctx.send(f"🧹 **{len(deleted)}** ədəd mesaj təmizləndi.", delete_after=3)

@bot.command(name="ping")
async def ping(ctx):
    if ctx.author.id != OWNER_ID:
        return

    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Botun gecikmə sürəti: **{latency}ms**")

@bot.command(name="serverbilgisi")
async def serverbilgisi(ctx):
    if ctx.author.id != OWNER_ID:
        return

    guild = ctx.guild
    embed = discord.Embed(title=f"📊 {guild.name} - Server Məlumatı", color=0x2b2d31)
    embed.add_field(name="👑 Server Sahibçisi", value=guild.owner, inline=True)
    embed.add_field(name="👥 Üzv Sayı", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Yaradılma Tarixi", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != OWNER_ID:
        return

    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member}** serverdən uzaqlaşdırıldı. Səbəb: **{reason}**")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if ctx.author.id != OWNER_ID:
        return

    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member}** serverdən qovuldu. Səbəb: **{reason}**")

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))
    
