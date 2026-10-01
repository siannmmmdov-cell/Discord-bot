import os
from collections import defaultdict
import re
from threading import Thread
import time
import discord
from discord.ext import commands
from flask import Flask

# --- RENDER PORT XƏTASININ QARŞISINI ALMAQ ÜÇÜN FLASK SERVER ---
app = Flask('')


@app.route('/')
def home():
  return 'DİABLOS Bot aktivdir!'


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


# --- DİSCORD BOT AYARLARI ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.webhooks = True
intents.guilds = True
intents.moderation = True

bot = commands.Bot(command_prefix='!', help_command=None, intents=intents)

# Sahib ID-si
OWNER_ID = 641014966312501259

anti_spam_status = {}
user_message_counts = defaultdict(list)
user_last_message = {}
ban_action_counts = defaultdict(list)

caps_warnings = defaultdict(int)
long_text_warnings = defaultdict(int)


def clean_text(text):
  text = text.lower()
  replacements = {
      '4': 'a',
      '@': 'a',
      '3': 'e',
      '1': 'i',
      '!': 'i',
      '0': 'o',
      '5': 's',
      '$': 's',
      '7': 't',
      '+': 't',
      '8': 'b',
      '9': 'g',
  }
  for char, replacement in replacements.items():
    text = text.replace(char, replacement)
  return text.replace(' ', '')


@bot.event
async def on_ready():
  activity = discord.Activity(
      type=discord.ActivityType.watching, name='DİABLOS Təhlükəsizlik 🛡️'
  )
  await bot.change_presence(activity=activity)
  print(f'DİABLOS Təhlükəsizlik Botu tam aktivdir: {bot.user}')


# --- SAXTA HESAB VƏ BOT QORUNMASI ---
@bot.event
async def on_member_join(member):
  try:
    now = discord.utils.utcnow()
    account_age = (now - member.created_at).total_seconds()

    if account_age < 86400 and not member.avatar:
      await member.kick(
          reason='DİABLOS Anti-Bot: Şübhəli / Yeni yaradılmış saxta hesab.'
      )
  except:
    pass


# --- 1. WEBHOOK QORUNMASI ---
@bot.event
async def on_webhooks_update(channel):
  try:
    webhooks = await channel.webhooks()
    for webhook in webhooks:
      if webhook.user and webhook.user.id != OWNER_ID:
        await webhook.delete(
            reason=f'{channel.guild.name}: Sahibindən başqasına webhook yaratmaq qadağandır!'
        )
  except:
    pass


# --- 2. KANAL YARADILMASI QORUNMASI ---
@bot.event
async def on_guild_channel_create(channel):
  try:
    async for entry in channel.guild.audit_logs(
        limit=1, action=discord.AuditLogAction.channel_create
    ):
      if entry.user and entry.user.id != OWNER_ID:
        await channel.delete(
            reason=f'{channel.guild.name}: Sahibindən başqasına kanal açmaq qadağandır!'
        )
  except:
    pass


# --- 3. ROL YARADILMASI QORUNMASI ---
@bot.event
async def on_guild_role_create(role):
  try:
    async for entry in role.guild.audit_logs(
        limit=1, action=discord.AuditLogAction.role_create
    ):
      if entry.user and entry.user.id != OWNER_ID:
        await role.delete(
            reason=f'{role.guild.name}: Sahibindən başqasına rol açmaq qadağandır!'
        )
  except:
    pass


# --- 4. ANTI-NUKE QORUNMASI ---
@bot.event
async def on_member_ban(guild, user):
  try:
    async for entry in guild.audit_logs(
        limit=1, action=discord.AuditLogAction.ban
    ):
      actor = entry.user
      if actor and actor.id != bot.user.id and actor.id != OWNER_ID:
        current_time = time.time()
        ban_action_counts[actor.id].append(current_time)

        ban_action_counts[actor.id] = [
            t for t in ban_action_counts[actor.id] if current_time - t < 10
        ]
        if len(ban_action_counts[actor.id]) > 3:
          member = guild.get_member(actor.id)
          if member:
            try:
              await member.ban(reason=f'{guild.name}: Anti-Nuke: İcazəsiz kütləvi ban!')
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

  # Zərərli link və fırıldaqçılıq qoruması
  dangerous_patterns = ['discord-gift', 'free-nitro', 'steam-nitro', 'dlcord.gg']
  if any(pattern in cleaned for pattern in dangerous_patterns):
    try:
      await message.delete()
      duration = discord.utils.utcnow() + discord.timedelta(minutes=10)
      await message.author.timeout(
          duration, reason='DİABLOS: Zərərli / Phishing link paylaşımı.'
      )
      await message.channel.send(
          f'{message.author.mention}, zərərli link paylaşdığın üçün 10 dəqiqəlik timmout aldın!'
      )
      return
    except:
      pass

  # Kütləvi etiketləmə qoruması
  if message.mention_everyone or len(message.mentions) > 3:
    try:
      await message.delete()
      await message.channel.send(
          f'{message.author.mention}, yavaş yaz, kütləvi etiketləmək qadağandır!'
      )
      return
    except:
      pass

  # Çox uzun mesaj qoruması (150 simvoldan çox)
  if len(content) > 150:
    try:
      await message.delete()
      long_text_warnings[message.author.id] += 1
      count = long_text_warnings[message.author.id]

      if count >= 3:
        long_text_warnings[message.author.id] = 0
        duration = discord.utils.utcnow() + discord.timedelta(minutes=5)
        await message.author.timeout(duration, reason='Həddindən artıq uzun mesaj spamı.')
        await message.channel.send(
            f'{message.author.mention}, həddindən artıq uzun mesaj yazdığın üçün 5 dəqiqəlik timmout aldın!'
        )
      else:
        await message.channel.send(
            f'{message.author.mention}, zəhmət olmasa bu qədər uzun dastan yazma! ({count}/3)'
        )
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
        await message.author.timeout(duration, reason='Caps Lock Spam.')
        await message.channel.send(
            f'{message.author.mention}, qışqıraraq yazdığın üçün 5 dəqiqəlik timmout aldın.'
        )
      else:
        await message.channel.send(
            f'{message.author.mention}, zəhmət olmasa Caps Lock-u söndür! ({count}/3)'
        )
      return
    except:
      pass

  # Link Qoruması
  if any(domain in cleaned for domain in ['discord.gg/', 'http://', 'https://', 't.me/', 'discord.com/invite']):
    try:
      await message.delete()
      await message.channel.send(
          f'{message.author.mention}, başqa serverin linkini atmaq qadağandır!'
      )
      return
    except:
      pass

  # Təkrar Mesaj Spam Qoruması
  author_id = message.author.id
  current_time = time.time()

  if author_id not in user_message_counts:
    user_message_counts[author_id] = []

  last_msg = user_last_message.get(author_id, ('', 0))
  if last_msg[0] == content and current_time - last_msg[1] < 4:
    try:
      await message.delete()
      await message.channel.send(
          f'{message.author.mention}, eyni mesajı təkrar spam etmə!'
      )
      return
    except:
      pass

  user_last_message[author_id] = (content, current_time)

  # Sürətli Mesaj Spamı
  user_message_counts[author_id] = [
      t for t in user_message_counts[author_id] if current_time - t < 3
  ]
  user_message_counts[author_id].append(current_time)

  if len(user_message_counts[author_id]) > 5:
    try:
      await message.delete()
      await message.channel.send(
          f'{message.author.mention}, çox sürətli yazırsan, bir az yavaş ol.'
      )
      return
    except:
      pass

  await bot.process_commands(message)


# --- KOMANDALAR (YALNIZ SAHİB ÜÇÜN) ---


@bot.command(name='yardim', aliases=['help'])
async def yardim(ctx):
  if ctx.author.id != OWNER_ID:
    return

  embed = discord.Embed(
      title='🛡️ DİABLOS Təhlükəsizlik Sistemi',
      description="Serverin nizam-intizamını qoru.",
      color=0x2b2d31,
  )
  embed.add_field(
      name='🔗 Dəvət Linki', value='`/url` - Serverin dəvət linkini göstərir.', inline=False
  )
  embed.add_field(
      name='🛡️ Anti-Spam', value='`/antispam enable / disable` - Mühafizəni idarə edir.', inline=False
  )
  embed.add_field(
      name='🔒 Kanal Kilidi', value='`/lock / unlock` - Kanalı yazışmaya bağlayır/açır.', inline=False
  )
  embed.add_field(
      name='🧹 Mesaj Təmizliyi', value='`/sil [say]` - Mesajları təmizləyir.', inline=False
  )
  embed.add_field(
      name='📊 Server Bilgisi', value='`/serverbilgisi` - Server haqqında məlumat verir.', inline=False
  )
  embed.add_field(
      name='🏓 Gecikmə', value='`/ping` - Botun sürətini yoxlayır.', inline=False
  )
  embed.set_footer(text=f'{ctx.guild.name} • DİABLOS Security Systems')
  await ctx.send(embed=embed)


@bot.command(name='antispam')
async def antispam(ctx, status: str):
  if ctx.author.id != OWNER_ID:
    return

  guild_id = ctx.guild.id
  if status.lower() == 'enable':
    anti_spam_status[guild_id] = True
    await ctx.send(f'✅ {ctx.guild.name}: Təhlükəsizlik sistemi aktivləşdirildi.')
  elif status.lower() == 'disable':
    anti_spam_status[guild_id] = False
    await ctx.send(f'⚠️ {ctx.guild.name}: Təhlükəsizlik sistemi söndürüldü.')
  else:
    await ctx.send("❌ İstifadə qaydası: `!antispam enable` və ya `!antispam disable`")


@bot.command(name='lock')
async def lock(ctx):
  if ctx.author.id != OWNER_ID:
    return

  try:
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(
        f'🔒 Bu kanal ({ctx.guild.name}) təhlükəsizlik protokolu ilə kilidləndi.',
        delete_after=5,
    )
  except:
    pass


@bot.command(name='unlock')
async def unlock(ctx):
  if ctx.author.id != OWNER_ID:
    return

  try:
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(
        f'🔓 Kanalın kilidi açıldı, ({ctx.guild.name}) sakinləri yenidən yaza bilərsiniz.',
        delete_after=5,
    )
  except:
    pass


@bot.command(name='url')
async def server_url(ctx):
  if ctx.author.id != OWNER_ID:
    return

  if ctx.guild.vanity_url_code:
    try:
      vanity = await ctx.guild.vanity_invite()
      await ctx.send(
          f'🔗 {ctx.guild.name} Dəvət Linki: **discord.gg/{vanity.code}** (İstifadə: {vanity.uses})'
      )
    except:
      await ctx.send(
          f'🔗 {ctx.guild.name} Dəvət Linki: **discord.gg/{ctx.guild.vanity_url_code}**'
      )
  else:
    await ctx.send(f'❌ {ctx.guild.name} Serverinin xüsusi (vanity) linki yoxdur.')


@bot.command(name='sil', aliases=['təmizlə'])
async def sil_komanda(ctx, limit: int = 5):
  if ctx.author.id != OWNER_ID:
    return

  try:
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=limit)
    await ctx.send(
        f'🧹 **{len(deleted)}** ədəd mesaj təmizləndi.', delete_after=1
    )
  except:
    pass


@bot.command(name='ping')
async def ping(ctx):
  if ctx.author.id != OWNER_ID:
    return

  latency = round(bot.latency * 1000)
  await ctx.send(f'🏓 Pong! Botun gecikmə sürəti: **{latency}ms**')


@bot.command(name='serverbilgisi')
async def serverbilgisi(ctx):
  if ctx.author.id != OWNER_ID:
    return

  guild = ctx.guild
  embed = discord.Embed(title=f'📊 {guild.name} - Server Məlumatı', color=0x2b2d31)
  embed.add_field(
      name='👑 Server Sahib(ə)si', value=f'{guild.owner}', inline=True
  )
  embed.add_field(name='👥 Üzv Sayı', value=guild.member_count, inline=True)
  embed.add_field(
      name='📅 Yaradılma Tarixi',
      value=guild.created_at.strftime('%d.%m.%Y'),
      inline=True,
  )
  await ctx.send(embed=embed)


@bot.command(name='ban')
async def ban(ctx, member: discord.Member, *, reason='Göstərilməyib'):
  if ctx.author.id != OWNER_ID:
    return

  try:
    await member.ban(reason=reason)
    await ctx.send(f'🔨 **{member}** serverdən uzaqlaşdırıldı. Səbəb: **{reason}**')
  except:
    pass


@bot.command(name='kick')
async def kick(ctx, member: discord.Member, *, reason='Göstərilməyib'):
  if ctx.author.id != OWNER_ID:
    return

  try:
    await member.kick(reason=reason)
    await ctx.send(f'👢 **{member}** serverdən qovuldu. Səbəb: **{reason}**')
  except:
    pass


if __name__ == '__main__':
  keep_alive()
  bot.run(os.environ.get('DISCORD_TOKEN'))
        
