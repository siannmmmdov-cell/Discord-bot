import discord
from discord.ext import commands
import time
from datetime import timedelta
import random
import os
from flask import Flask
from threading import Thread

# ==========================================
# --- 1. RENDER ÜÇÜN DİNAMİK PORTLU FLASK ---
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Yenilmez OS v600 Elite aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# ==========================================
# --- 2. BOTUN SAZLANMALARI VƏ INTENTS ---
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True

bot = commands.Bot(command_prefix="r?", intents=intents)

# Yalnız sənin ID-n (Master Sahib)
SAHIB_ID = 641014966312501259

# Güclü Anti-Spam Bazası
spam_records = {}
SPAM_THRESHOLD = 3      
SPAM_WINDOW = 3.5       

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f" [X] YENILMEZ OS v600 ELITE MASTER AKTİVDİR!")
    print(f" [X] Bot Adı: {bot.user.name}")
    print(f" [X] Sahib ID: {SAHIB_ID}")
    print(f"==================================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Elite Control 🛡️"))


# ==========================================
# --- 3. GÜCLÜ ANTİ-SPAM QORUNMASI ---
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.guild_permissions.administrator or message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    current_time = time.time()
    author_id = message.author.id

    if author_id not in spam_records:
        spam_records[author_id] = {"count": 1, "last_time": current_time, "warns": 0}
    else:
        data = spam_records[author_id]
        if current_time - data["last_time"] < SPAM_WINDOW:
            data["count"] += 1
            data["last_time"] = current_time
            
            if data["count"] >= SPAM_THRESHOLD:
                try:
                    await message.delete()
                except:
                    pass

                data["warns"] += 1
                if data["warns"] == 1:
                    try:
                        await message.channel.send(f"⚠️ {message.author.mention}, spam etmə!", delete_after=4)
                    except:
                        pass
                elif data["warns"] >= 2:
                    try:
                        await message.author.timeout(timedelta(minutes=5), reason="Spam")
                        await message.channel.send(f"🔇 {message.author.mention}, 5 dəqiqəlik mute!", delete_after=5)
                    except:
                        pass
                return
        else:
            data["count"] = 1
            data["last_time"] = current_time

    await bot.process_commands(message)


# ==========================================
# --- 4. BÜTÜN EMOJİLƏR VƏ GIF-LƏR SİSTEMİ ---
# ==========================================
EMOJI_VE_GIF_GRUPLARI = {
    # Ağlama / Üzüntü qrupu (😭 və bənzərləri)
    "😭": {
        "oxsarlar": ["😢", "😿", "💧", "🥺", "💔"],
        "gif": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif"
    },
    "😢": {
        "oxsarlar": ["😭", "😿", "💧", "🥺"],
        "gif": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif"
    },
    "🥺": {
        "oxsarlar": ["😭", "😢", "👉👈", "🥺"],
        "gif": "https://media.giphy.com/media/2u11zpzwyMTy8/giphy.gif"
    },

    # Gülüş qrupu (🤣, 😂 və s.)
    "🤣": {
        "oxsarlar": ["😂", "😆", "💀", "😹", "🗿"],
        "gif": "https://media.giphy.com/media/10kABVynhynGYU/giphy.gif"
    },
    "😂": {
        "oxsarlar": ["🤣", "😆", "💀", "😹", "🗿"],
        "gif": "https://media.giphy.com/media/10kABVynhynGYU/giphy.gif"
    },
    "💀": {
        "oxsarlar": ["🤣", "😂", "🗿", "🔥", "💯"],
        "gif": "https://media.giphy.com/media/8xs8YIlngpbijhn5Li/giphy.gif"
    },

    # At / Heyvan / Sərt qrup (🐎 və s.)
    "🐎": {
        "oxsarlar": ["🦄", "🐴", "⚡", "🔥", "🐾"],
        "gif": "https://media.giphy.com/media/12bjQ7ujukBKCKbW5e/giphy.gif"
    },
    "🦄": {
        "oxsarlar": ["🐎", "🐴", "✨", "💫"],
        "gif": "https://media.giphy.com/media/12bjQ7ujukBKCKbW5e/giphy.gif"
    },

    # Od / Aura / Güc qrupu (🔥, ⚡)
    "🔥": {
        "oxsarlar": ["⚡", "💀", "👑", "💯", "💥"],
        "gif": "https://media.giphy.com/media/19JSJ5ucu91R5D7a3w/giphy.gif"
    },
    "⚡": {
        "oxsarlar": ["🔥", "💀", "⭐", "💥", "⚡"],
        "gif": "https://media.giphy.com/media/l0HlRnAWXxn0MhOBK/giphy.gif"
    },

    # Ürək / Sevgi qrupu (❤️)
    "❤️": {
        "oxsarlar": ["💖", "💘", "💓", "🖤", "✨"],
        "gif": "https://media.giphy.com/media/3ohhwkKBcKzPA4zYUE/giphy.gif"
    },
    "💖": {
        "oxsarlar": ["❤️", "💘", "💓", "✨"],
        "gif": "https://media.giphy.com/media/3ohhwkKBcKzPA4zYUE/giphy.gif"
    },

    # Əsəb / Döyüş / Silah qrupu 😡, 🤬, ⚔️
    "😡": {
        "oxsarlar": ["🤬", "💢", "👊", "🔥", "💀"],
        "gif": "https://media.giphy.com/media/8US6ERbtKbVfC/giphy.gif"
    },
    "⚔️": {
        "oxsarlar": ["🛡️", "🔥", "💀", "🏆", "⚡"],
        "gif": "https://media.giphy.com/media5/26ufdipQqU2lhNA4g/giphy.gif"
    }
}

@bot.event
async def on_raw_reaction_add(payload):
    # Yalnız sənin ID-ni yoxlayır (Sənə özəldir)
    if payload.user_id != SAHIB_ID:
        return
    
    if payload.guild_id is None:
        return

    channel = bot.get_channel(payload.channel_id)
    if not channel:
        return

    try:
        message = await channel.fetch_message(payload.message_id)
    except:
        return

    emoji_str = str(payload.emoji)

    # Əgər basdığın emoji qruplarda mövcuddursa
    if emoji_str in EMOJI_VE_GIF_GRUPLARI:
        grup_data = EMOJI_VE_GIF_GRUPLARI[emoji_str]
        
        # 1. Oxşar emojiləri avtomatik basır
        for oxsar in grup_data["oxsarlar"]:
            try:
                await message.add_reaction(oxsar)
            except:
                pass
        
        # 2. Uyğun GIF-i mesaja cavab olaraq (və ya kanala) atır
        try:
            await channel.send(f"Aura GIF ({emoji_str}): {grup_data['gif']}")
        except:
            pass


# ==========================================
# --- 5. MASTER SAHİB PANELİ ---
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu panel yalnız botun sahibinə məxsusdur!")
        return

    embed = discord.Embed(
        title="💀 YENİLMEZ OS // ELITE MASTER PANEL v600",
        description="Serverin idarəetmə mərkəzi və bütün emojilər/gif sistemləri aktivdir:",
        color=0x050505
    )
    embed.add_field(
        name="👑 1. Sizin Xüsusi Sahib Əmrləriniz", 
        value="• `r?elan [mətn]` — Rəsmi elan\n• `r?anket [sual]` — Səsvermə anketi\n• `r?cekilis [hədiyyə]` — Çəkiliş", 
        inline=False
    )
    embed.add_field(
        name="🔊 2. Səs Sistemi İdarəsi", 
        value="• `r?join` — Səsə qoşular\n• `r?leave` — Səsindən çıxar", 
        inline=False
    )
    embed.add_field(
        name="🛡️ 3. Moderasiya & Təhlükəsizlik", 
        value="• `r?sil`, `r?mute`, `r?ban`, `r?kick`, `r?lock`, `r?unlock`", 
        inline=False
    )
    embed.add_field(
        name="⚔️ 4. Auralı Oyunlar", 
        value="• `r?duel`, `r?coinflip`, `r?hacker`, `r?kasa`", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS Elite - All Rights Reserved 2026")
    await ctx.send(embed=embed)


# ==========================================
# --- 6. ÜMUMI VƏ SƏS ƏMRLƏRİ ---
# ==========================================
@bot.command(name="salam")
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}. Sistem tam gücdə işləyir. 🏴‍☠️")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"⚡ Ping: **{round(bot.latency * 1000)}ms**")

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("⚠️ Əvvəlcə səs kanalına qoşulmalısan!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"🔊 Bağlandım səs kanalına: **{channel.name}** 🎙️")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Səs kanalından ayrıldım.")
    else:
        await ctx.send("⚠️ Onsuz da heç bir səs kanalında deyiləm!")


# ==========================================
# --- 7. SAHİBƏ ÖZƏL: ELAN, ANKET, ÇƏKİLİŞ ---
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 RƏSMİ SERVER ELANI", description=elan_metni, color=0x050505)
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("📢")

@bot.command(name="anket")
async def anket(ctx, *, anket_suali: str):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 YENİ ANKET / SƏSVERMƏ", description=anket_suali, color=0x050505)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, *, hediyye: str):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.message.delete()
    embed = discord.Embed(title="🎉 BÖYÜK ÇƏKİLİŞ", description=f"Hədiyyə: **{hediyye}**", color=0x050505)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎁")


# ==========================================
# --- 8. MODERASİYA & OYUNLAR ---
# ==========================================
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, say: int = 5):
    await ctx.message.delete()
    await ctx.channel.purge(limit=say)

@bot.command(name="duel")
async def duel(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("⚠️ `r?duel @istifadəçi` yazmalısan!")
        return
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ Döyüş başladı! Qalib: **{kazanan.name}** 🏆")

@bot.command(name="coinflip")
async def coinflip(ctx, secim: str = None):
    if not secim:
        await ctx.send("⚠️ `r?coinflip yazi` və ya `tura` seç")
        return
    netice = random.choice(["yazı", "tura"])
    if secim.lower() == netice:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Qazandın! 😎")
    else:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Uduzdun!")

@bot.command(name="hacker")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip = f"{random.randint(40, 200)}.{random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}"
    await ctx.send(f"💻 **{target.name}** IP: `{ip}` | Sızma uğurludur 🕵️‍♂️")

@bot.command(name="kasa")
async def kasa(ctx):
    qazanc = random.randint(100, 5000)
    await ctx.send(f"💎 Xəzinə açıldı! Qənimət: **{qazanc} AZN**, {ctx.author.mention}!")


# ==========================================
# --- 9. İŞƏ SALMA ---
# ==========================================
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
    
