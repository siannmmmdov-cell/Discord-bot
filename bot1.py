import discord
from discord.ext import commands
import os
import asyncio
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# İkinci bot "." (nöqtə) prefiksi ilə işləyir
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 KÖMƏKÇİ VƏ MODERASİYA BOTU aktivdir: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".yardim | İdarəetmə Paneli 🛠️"))

@bot.command(name="yardim", aliases=["help"])
async def yardim(ctx):
    embed = discord.Embed(
        title="🛠️ Server İdarəetmə və Moderasiya Paneli",
        description="Bütün əmrlər **`.`** prefiksi ilə işləyir, Ruhum:",
        color=discord.Color.blue()
    )
    embed.add_field(name="🧹 `.sil [say]`", value="Göstərilən miqdarda mesajı təmizləyir.", inline=False)
    embed.add_field(name="🔨 `.ban [@istifadəçi]`", value="Təxribatçı istifadəçini serverdən banlayır.", inline=False)
    embed.add_field(name="⏳ `.mute [@istifadəçi] [dəqiqə]`", value="Qayda pozan istifadəçini susdurur.", inline=False)
    embed.add_field(name="🏓 `.ping`", value="Botun anlıq gecikmə sürətini ölçür.", inline=False)
    embed.set_footer(text="Ruhum üçün xüsusi olaraq hazırlandı.")
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Gecikmə sürəti: **{latency}ms**")

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Uğurla **{amount}** ədəd mesaj təmizləndi!")
    await asyncio.sleep(3)
    try:
        await msg.delete()
    except:
        pass

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Səbəb göstərilməyib"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member.mention}** serverdən ban olundu!\n📜 Səbəb: `{reason}`")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5, *, reason="Qayda pozuntusu"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"⏳ **{member.mention}** {minutes} dəqiqə müddətinə susduruldu!")

token = os.environ.get("DISCORD_TOKEN_2")
bot.run(token)
