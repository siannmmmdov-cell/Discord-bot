import discord
from discord.ext import commands
import os
import re
import time
from collections import defaultdict, Counter

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

spam_tracker = defaultdict(list)
spam_warnings = Counter()

@bot.event
async def on_ready():
    print(f"Birinci Bot aktivdir: {bot.user}")

@bot.command()
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Server tam güvənlik altındadır, xoş gəldin, Ruhum!")

@bot.command()
async def guvendeymiki(ctx):
    server = ctx.guild
    verification = str(server.verification_level).upper()
    await ctx.send(
        f"🛡️ **Möhkəm Güvənlik Hesabatı:**\n"
        f"- Sunucu Adı: {server.name}\n"
        f"- Doğrulama Səviyyəsi: {verification}\n"
        f"- Üzv Sayı: {server.member_count}\n"
        f"🟢 *Status: Bütün qoruma sistemləri aktivdir!*"
    )

@bot.command()
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Uğurla {amount} ədəd mesaj təmizləndi!", delete_after=3)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} serverdən ban olundu! Səbəb: {reason}")

@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    invite_regex = r"(https?://)?(www\.)?(discord\.(gg|io|me|li|club)|discordapp\.com/invite)/\w+"
    if re.search(invite_regex, message.content):
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, başqa yerlərin dəvət linkini atmaq qadağandır!", delete_after=5)
            return
        except Exception:
            pass

    if "@everyone" in message.content or "@here" in message.content:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, hər kəsi etiketləmək qadağandır!", delete_after=5)
            return
        except Exception:
            pass

    author_id = message.author.id
    current_time = time.time()
    
    spam_tracker[author_id] = [t for t in spam_tracker[author_id] if current_time - t < 5]
    spam_tracker[author_id].append(current_time)

    if len(spam_tracker[author_id]) >= 7:
        spam_tracker[author_id].clear()
        spam_warnings[author_id] += 1
        warning_count = spam_warnings[author_id]

        try:
            await message.delete()
        except Exception:
            pass

        if warning_count == 1:
            await message.channel.send(f"⚠️ {message.author.mention}, həddindən artıq sürətli mesaj yazırsan! İlk xəbərdarlıq.", delete_after=6)
        elif warning_count == 2:
            try:
                from datetime import timedelta
                await message.author.timeout(timedelta(seconds=10), reason="Spam (10 saniyəlik mute).")
                await message.channel.send(f"⏳ {message.author.mention}, 10 saniyəlik zaman aşımına salındın!", delete_after=6)
            except Exception:
                pass
        elif warning_count >= 3:
            try:
                await message.author.ban(reason="Spam qaydasını 3 dəfə pozdu.")
                await message.channel.send(f"🔨 {message.author.mention} ardıcıl spam etdiyi üçün banlandı!")
                del spam_warnings[author_id]
            except Exception:
                pass
        return

    await bot.process_commands(message)

# Birinci botun tokeni (Render-də DISCORD_TOKEN yazılan yer üçündür)
bot.run(os.environ.get("DISCORD_TOKEN"))
    
