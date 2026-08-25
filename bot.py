import discord
from discord.ext import commands
import os
import asyncio
from datetime import timedelta
from flask import Flask
import threading

# Render üçün veb-server (yaşıl olması üçün)
app = Flask('')

@app.route('/')
def home():
    return "Köməkçi Bot işləyir!"

def run_server():
    app.run(host='0.0.0.0', port=8081)

def keep_alive():
    t = threading.Thread(target=run_server)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 KÖMƏKÇİ VƏ MODERASİYA BOTU aktivdir: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".yardim | İdarəetmə Paneli"))

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="🛠️ Server İdarəetmə və Moderasiya Paneli",
        description="Bütün əmrlər **`.`** prefiksi ilə işləyir, Ruhum:",
        color=discord.Color.blue()
    )
    embed.add_field(name="🧹 `.sil [say]`", value="Göstərilən miqdarda mesajı təmizləyir.", inline=False)
    embed.add_field(name="🔨 `.ban [@istifadəçi] [səbəb]`", value="Qayda pozanı serverdən uzaqlaşdırır.", inline=False)
    embed.add_field(name="⏳ `.mute [@istifadəçi] [dəqiqə]`", value="İstifadəçini müvəqqəti susdurur.", inline=False)
    embed.add_field(name="🏓 `.ping`", value="Botun anlıq gecikmə sürətini ölçür.", inline=False)
    embed.add_field(name="👤 `.userinfo [@istifadəçi]`", value="İstifadəçi haqqında ətraflı məlumat verir.", inline=False)
    embed.set_footer(text="Ruhum üçün maksimum funksiyalarla hazırdır.")
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

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    embed = discord.Embed(title=f"👤 İstifadəçi Məlumatı - {member.name}", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="İstifadəçi Adı", value=member.mention, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Serverə Qoşulma tarixi", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    await ctx.send(embed=embed)

# Serveri işə salırıq
keep_alive()

token = os.environ.get("DISCORD_TOKEN_2")
if token:
    bot.run(token)
              
