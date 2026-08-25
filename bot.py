import discord
from discord.ext import commands
import os
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "Bot aktivdir!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_server).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"BOT AKTİVDİR: {bot.user.name}")

@bot.command(name="yardim")
async def yardim(ctx):
    await ctx.send("Salam Ruhum! Bot aktivdir. Əmrlər: .sil, .ping")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! Gecikmə: {round(bot.latency * 1000)}ms")

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{amount} ədəd mesaj silindi!", delete_after=3)

token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("XƏTA: Token tapılmadı!")
    
