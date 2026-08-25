import discord
from discord.ext import commands
import os
import asyncio
from datetime import timedelta
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "Bot işləyir!"

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
    print(f"🤖 Bot aktivdir: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".yardim | Panel"))

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="🛠️ Server İdarəetmə Paneli",
        description="Bütün əmrlər **`.`** ilə işləyir, Ruhum:",
        color=discord.Color.blue()
    )
    embed.add_field(name="🧹 `.sil [say]`", value="Mesajları təmizləyir.", inline=False)
    embed.add_field(name="🏓 `.ping`", value="Gecikməni yoxlayır.", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Gecikmə: **{latency}ms**")

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 **{amount}** ədəd mesaj silindi!", delete_after=3)

keep_alive()

token = os.environ.get("DISCORD_TOKEN_2")
if token:
    bot.run(token)

