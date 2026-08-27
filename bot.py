import discord
from discord.ext import commands
import time
from datetime import timedelta
import random
import asyncio
import os
from flask import Flask
from threading import Thread

# ==========================================
# --- 1. RENDER ÜÇÜN DİNAMİK PORTLU FLASK ---
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Yenilmez OS v1500 Monster aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# ==========================================
# --- 2. BOT SAZLANMALARI VƏ INTENTS ---
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True          
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.presences = True 

bot = commands.Bot(command_prefix="r?", intents=intents)

# Yalnız sənin ID-n (Master Sahib)
SAHIB_ID = 641014966312501259

spam_records = {}
SPAM_WINDOW = 4.0       
start_time = time.time()

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f" [X] YENILMEZ OS v1500 MONSTER MASTER AKTİVDİR!")
    print(f" [X] Bot Adı: {bot.user.name}")
    print(f" [X] Sahib ID: {SAHIB_ID}")
    print(f"==================================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Elite Control 🛡️"))


# ==========================================
# --- 3. AVTO-ANTİ-RAID & BOT QORUNMASI ---
# ==========================================
@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.guild.ban(member, reason="İznsiz kənar bot girişi / Raid cəhdi")
            return
        except:
            pass


# ==========================================
# --- 4. TƏHLÜKƏSİZLİK & LİNK/SPAM BLOKU ---
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.guild_permissions.administrator or message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    content_lower = message.content.lower()

    if "discord.gg/" in content_lower or "discord.com/invite/" in content_lower or "http://" in content_lower or "https://" in content_lower:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, serverdə reklam və link paylaşmaq qadağandır!", delete_after=5)
            await message.author.timeout(timedelta(minutes=10), reason="Serverdə Link/Reklam Paylaşımı")
        except:
            pass
        return

    current_time = time.time()
    author_id = message.author.id

    if author_id not in spam_records:
        spam_records[author_id] = {"last_time": current_time, "warns": 0}
    else:
        data = spam_records[author_id]
        if current_time - data["last_time"] < SPAM_WINDOW:
            data["last_time"] = current_time
            try:
                await message.delete()
            except:
                pass

            data["warns"] += 1
            if data["warns"] >= 2:
                try:
                    await message.author.timeout(timedelta(minutes=5), reason="Spam")
                    await message.channel.send(f"🔇 {message.author.mention}, spam etdiyin üçün mute olundun!", delete_after=5)
                    data["warns"] = 0 
                except:
                    pass
            return
        else:
            data["last_time"] = current_time

    await bot.process_commands(message)


# ==========================================
# --- 5. EMOJİLƏRƏ BASANDA FƏRQLİ REAKSİYA ---
# ==========================================
EMOJI_GRUPLARI = {
    "🤣": ["😂", "😆", "💀", "😹"],
    "😂": ["🤣", "😆", "💀", "😹"],
    "💀": ["🤣", "😂", "🗿", "🔥"],
    "🔥": ["⚡", "💀", "👑", "💯", "💥"],
    "❤️": ["💖", "💘", "💓", "🖤", "🔥"],
    "⚔️": ["🛡️", "🔥", "💀", "🏆", "⚡"]
}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
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
    hedef_emojiler = EMOJI_GRUPLARI.get(emoji_str, ["🔥", "💀", "⚡", "👑"])

    for oxsar in hedef_emojiler:
        if oxsar != emoji_str:
            try:
                await message.add_reaction(oxsar)
            except:
                pass


# ==========================================
# --- 6. MASTER SAHİB PANELİ (v1500) ---
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu panel yalnız botun sahibinə məxsusdur!")
        return

    embed = discord.Embed(
        title="💀 YENİLMEZ OS // ELITE MASTER PANEL v1500",
        description="Serverin idarəetmə mərkəzi, xüsusi sahib əmrləri və sistemlər:",
        color=0x050505
    )
    embed.add_field(
        name="👑 1. Yalnız Sənin Edə Biləcəyin Sahib Əmrlərin (Özəl)", 
        value="• `r?elan [mətn]` — @everyone ilə rəsmi elan atır\n• `r?anket [sual]` — Serverdə səsvermə anket açır\n• `r?cekilis [vaxt] [hədiyyə]` — Avtomatik vaxtlı çəkiliş başladır", 
        inline=False
    )
    embed.add_field(
        name="📊 2. Server & Məlumat Sistemləri", 
        value="• `r?server` — Server haqqında ətraflı məlumat\n• `r?userinfo [@istifadəçi]` — İstifadəçi haqqında dərin məlumat\n• `r?botinfo` — Botun işləmə müddəti", 
        inline=False
    )
    embed.add_field(
        name="🛡️ 3. Sərt Moderasiya & Təhlükəsizlik", 
        value="• `r?sil [say]` — Mesajları təmizləyər\n• `r?mute / r?unmute` — Susdurma əməliyyatları\n• `r?ban / r?kick` — Qovma əməliyyatları\n• `r?lock / r?unlock` — Kanalı bağlar/açar", 
        inline=False
    )
    embed.add_field(
        name="⚔️ 4. Oyunlar & Əyləncə", 
        value="• `r?duel [@istifadəçi]` — 1v1 döyüş\n• `r?coinflip [yazı/tura]` — Qəpik atma\n• `r?slot` — Slot maşını oyunu\n• `r?hacker [@istifadəçi]` — IP simulyasiyası", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS Elite - All Rights Reserved 2026")
    await ctx.send(embed=embed)


# ==========================================
# --- 7. SAHİBƏ ÖZƏL ƏMRLƏR (YALNIZ SƏN EDƏ BİLƏRSƏN) ---
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız botun sahibi işlədə bilər!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 RƏSMİ SERVER ELANI", description=elan_metni, color=0x050505)
    embed.set_footer(text=f"Elan edən: {ctx.author.name}")
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("📢")

@bot.command(name="anket")
async def anket(ctx, *, anket_suali: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız botun sahibi işlədə bilər!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 YENİ ANKET / SƏSVERMƏ", description=anket_suali, color=0x050505)
    embed.set_footer(text=f"Anket sahibi: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, vaxt_str: str, *, hediyye: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız botun sahibi işlədə bilər!")
        return
    await ctx.message.delete()

    saniye = 0
    try:
        if vaxt_str.endswith("s"): saniye = int(vaxt_str[:-1])
        elif vaxt_str.endswith("m"): saniye = int(vaxt_str[:-1]) * 60
        elif vaxt_str.endswith("h"): saniye = int(vaxt_str[:-1]) * 3600
        elif vaxt_str.endswith("d"): saniye = int(vaxt_str[:-1]) * 86400
        else:
            await ctx.send("⚠️ Vaxt formatı səhvdir! Məsələn: `r?cekilis 3d Nitro`")
            return
    except:
        return

    embed = discord.Embed(title="🎉 BÖYÜK AVTO-ÇƏKİLİŞ", description=f"Hədiyyə: **{hediyye}**\n\nQatılmaq üçün 🎁 emojisinə bas!", color=0x050505)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎁")

    await asyncio.sleep(saniye)
    try:
        msg = await ctx.channel.fetch_message(msg.id)
    except:
        return

    istirakcilar = []
    for reaction in msg.reactions:
        if str(reaction.emoji) == "🎁":
            async for user in reaction.users():
                if not user.bot: istirakcilar.append(user)
            break

    if not istirakcilar:
        await ctx.send("🎉 Çəkiliş bitdi. Heç kim qatılmadı!")
        return

    kazanan = random.choice(istirakcilar)
    win_embed = discord.Embed(title="🏆 ÇƏKİLİŞ QALİBİ!", description=f"Hədiyyə: **{hediyye}**\nTəbriklər, {kazanan.mention}! 🎉", color=0x050505)
    await ctx.send(embed=win_embed)


# ==========================================
# --- 8. MƏLUMAT & MODERASİYA ƏMRLƏRİ ---
# ==========================================
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"⚡ Ping: **{round(bot.latency * 1000)}ms**")

@bot.command(name="botinfo")
async def botinfo(ctx):
    uptime = str(timedelta(seconds=int(time.time() - start_time)))
    embed = discord.Embed(title="🤖 Bot Statusu", color=0x050505)
    embed.add_field(name="İşləmə Müddəti", value=uptime, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 İstifadəçi — {member.name}", color=0x050505)
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=str(member.id), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="server")
async def server_info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🛡️ {guild.name}", color=0x050505)
    embed.add_field(name="Üzv Sayı", value=str(guild.member_count), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, say: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=say)
    await ctx.send(f"🧹 {len(deleted)} mesaj silindi.", delete_after=3)

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute_cmd(ctx, member: discord.Member, dakika: int = 5):
    await member.timeout(timedelta(minutes=dakika))
    await ctx.send(f"🔇 {member.mention} {dakika} dəqiqəlik mute olundu.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} ban olundu!")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal kilidləndi!")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı!")


# ==========================================
# --- 9. OYUNLAR & ƏYLƏNCƏ ---
# ==========================================
@bot.command(name="duel")
async def duel(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("⚠️ Kimsəni etiketləməlisən: `r?duel @istifadəçi`")
        return
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ Döyüş bitdi! Qalib: **{kazanan.name}** 🏆")

@bot.command(name="coinflip")
async def coinflip(ctx, secim: str = None):
    if not secim:
        await ctx.send("⚠️ Seçim et: `r?coinflip yazı` və ya `r?coinflip tura`")
        return
    netice = random.choice(["yazı", "tura"])
    if secim.lower() == netice:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Qazandın! 😎")
    else:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Uduzdun!")

@bot.command(name="slot")
async def slot(ctx):
    simvol = ["🍎", "🍋", "🍒", "💎", "7️⃣"]
    r1, r2, r3 = random.choice(simvol), random.choice(simvol), random.choice(simvol)
    if r1 == r2 == r3:
        await ctx.send(f"🎰 | {r1} | {r2} | {r3} |\n🎉 Təbriklər, Jackpot vurdun!")
    else:
        await ctx.send(f"🎰 | {r1} | {r2} | {r3} |\n😢 Uduzdun!")

@bot.command(name="hacker")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip = f"{random.randint(40, 200)}.{random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}"
    await ctx.send(f"💻 **{target.name}** sisteminə sızıldı! IP: `{ip}` 🕵️‍♂️")


# ==========================================
# --- 10. İŞƏ SALMA ---
# ==========================================
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
        
