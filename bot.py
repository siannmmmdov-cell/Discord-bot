import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Sənin səs kanalının İD-si
VOICE_CHANNEL_ID = 1541243631896232026

@bot.event
async def on_ready():
    print(f"{bot.user} uğurla onlayn oldu!")
    
    # Səs kanalına qoşulma hissəsi
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                await channel.connect()
                print("Uğurla səs kanalına qoşuldu və qalır!")
        except Exception as e:
            print(f"Səs xətası: {e}")
    else:
        print("Səs kanalı tapılmadı, ID-ni yoxla!")

# Serveri qorumaq üçün: Kənar bot gələndə avtomatik qovmaq (Anti-Raid)
@bot.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.ban(reason="İcazəsiz bot əlavə edildi - Server Qoruması")
            print(f"İcazəsiz bot ban olundu: {member.name}")
        except Exception as e:
            print(e)

# Sadə əmrlər və cavablar
@bot.command()
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}! Server tam qorunur və mən onlaynam! 🛡️")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 Gecikmə: {round(bot.latency * 1000)}ms")

# Tokeni Render-də Environment Variables hissəsindən oxuyur
bot.run(os.environ.get("DISCORD_TOKEN"))
