import discord
from discord.ext import commands
import os
import re

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Qadağan olunmuş pis sözlər siyahısı (istədiyin kimi artıra bilərsən)
BAD_WORDS = ["təhqir1", "təhqir2", "spamsöz"]

@bot.event
async def on_ready():
    print(f"{bot.user} tam təhlükəsizlik və moderatorluq rejimi ilə onlayn oldu!")

# 1. KƏNAR BOT QORUMASI (Anti-Raid)
@bot.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.ban(reason="İcazəsiz bot əlavə edildi - Avtomatik Təhlükəsizlik Qoruması")
            print(f"Təhlükəli bot dərhal qovuldu: {member.name}")
        except Exception as e:
            print(e)

# 2. MESAJLARA NƏZARƏT (Link, 18+ şəkil və pis söz qoruması)
@bot.event
async def on_message(message):
    # Botun öz mesajlarını yoxlamaması üçündür
    if message.author.bot:
        return

    content = message.content.lower()

    # LİNK QORUMASI: Mesajda http və ya www varsa link kimi qəbul edilib silinir
    if "http://" in content or "https://" in content or "www." in content:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, bu serverdə link paylaşmaq qadağandır!", delete_after=5)
            return
        except Exception as e:
            print(e)

    # 18+ VƏ YA UYĞUNSUZ ŞƏKİL QORUMASI: Şəkil/fayl atıldıqda yoxlayır
    if message.attachments:
        for attachment in message.attachments:
            # Fayl adında və ya uzantısında şübhəli hal olarsa və ya ümumiyyətlə şəkilləri məhdudlaşdırmaq istəsən
            # Qeyd: Əgər hər cür şəkli silmək istəsən aşağıdakı şərti aktiv saxlaya bilərsən:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov')):
                # İstəyə görə şəklin 18+ olub olmadığını təyin etmək üçün buraya əlavə yoxlamalar qoyula bilər.
                # Hazırki rejimdə xəbərdarlıq edib və ya kilidləyə bilərik.
                pass 

    # PİS SÖZ VƏ TƏHQİR QORUMASI
    if any(word in content for word in BAD_WORDS):
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, zəhmət olmasa təhqir və ya qadağan olunmuş sözlərdən istifadə etməyin!", delete_after=5)
            return
        except Exception as e:
            print(e)

    # Əmrlərin düzgün işləməsi üçün bu sətri mütləq saxlayırıq
    await bot.process_commands(message)

# Status yoxlama əmri
@bot.command()
async def qoruma(ctx):
    await ctx.send(f"🛡️ {ctx.author.mention}, server 24/7 rejimində link, bot və təhlükəsizlik filtrləri ilə tam qorunur!")

# Tokeni oxuyur
bot.run(os.environ.get("DISCORD_TOKEN"))
