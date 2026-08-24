import os
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot qoruma rejimində işləyir: {client.user}')

@client.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.ban(reason="Icazesiz bot elave olundu! Anti-Raid qorumasi.")
            print(f"Tehlukeli bot qovuldu: {member.name}")
        except:
            pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == '!salam':
        await message.channel.send('Aleykum salam! Server 24/7 qorunur! 🛡️')

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
