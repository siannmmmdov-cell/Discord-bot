import discord
import re
import time
from collections import defaultdict
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.webhooks = True

client = discord.Client(intents=intents)

# İstifadəçilərin sürətli mesajlarını izləmək üçün
user_message_history = defaultdict(list)

@client.event
async def on_ready():
    print(f"Professional Təhlükəsizlik Botu işə düşdü: {client.user}")

@client.event
async def on_message(message):
    # Botların öz mesajlarını yoxlamasın
    if message.author.bot:
        return

    content = message.content
    lower_content = content.lower()
    author_id = message.author.id
    current_time = time.time()

    # İcazə verilən əmrlər (Whitelist): /hypertalk, /play, /sunucuadi və s.
    if lower_content.startswith(("/hypertalk", "/play", "/sunucuadi", "!play", "!hypertalk")):
        return

    is_threat = False

    # 1. Simvol dəyişikliyi ilə edilən spamlar (məsələn: /tanrizim və s.)
    cleaned_content = re.sub(r'[\s_\-\.\+\/\*\\#@]', '', lower_content)
    bad_words = ["tanrizim"] 
    for word in bad_words:
        if word in cleaned_content:
            is_threat = True
            break

    # 2. Reklam qoruması (İcazəsiz linklər)
    if ("discord.gg/" in lower_content or "discord.com/invite/" in lower_content or "https://" in lower_content):
        if not message.author.guild_permissions.administrator:
            is_threat = True

    # 3. 400 sətirlik və ya həddindən uzun floodlar
    if message.content.count("\n") > 3 or len(content) > 400:
        is_threat = True

    # 4. Ağıllı təkrar / spam qoruması (Atv botları kimi - tez-tez təkrarlanan eyni mesajlar)
    history = user_message_history[author_id]
    history = [item for item in history if current_time - item['time'] < 4]
    same_content_count = sum(1 for item in history if item['content'] == lower_content)
    
    if same_content_count >= 3:  
        is_threat = True
    
    history.append({'content': lower_content, 'time': current_time})
    user_message_history[author_id] = history

    # Əgər təhlükə aşkarlandısa
    if is_threat:
        try:
            await message.delete()
            warning = await message.channel.send(f"{message.author.mention}, spam, təkrarlanan mesajlar və ya reklam qəti qadağandır!")
            await warning.delete(delay=3)
        except Exception as e:
            print(f"Xəta: {e}")

# 5. Anti-Webhook (Webhook yaradılmasının qarşısı alınır)
@client.event
async def on_webhooks_update(channel):
    try:
        webhooks = await channel.webhooks()
        for webhook in webhook:
            await webhook.delete(reason="Təhlükəsizlik: Vebhook yaratmaq qadağandır!")
    except Exception as e:
        print(f"Webhook xətası: {e}")

# 6. Anti-Bot (Serverə iznsiz bot gələndə ban edir)
@client.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.guild.ban(member, reason="Təhlükəsizlik: Serverə iznsiz bot girişinə icazə verilmir!")
        except Exception as e:
            print(f"Bot ban edilərkən xəta: {e}")

# Tokeni birbaşa koda yazmırıq ki, Discord banlamasın. 
# Əsas bot.py faylına import edərək və ya gizli mühitdən oxudaraq işlədəcəksən.
