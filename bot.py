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
    return "Yenilmez OS v500 Elite aktivdir!"

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
intents.reactions = True  # Reaksiyaları oxumaq üçün vacibdir

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
    print(f" [X] YENILMEZ OS v500 ELITE MASTER AKTİVDİR!")
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
# --- 4. SƏNƏ ÖZƏL AVTO-REAKSİYA (JOY) SİSTEMİ ---
# ==========================================
@bot.event
async def on_raw_reaction_add(payload):
    # Yalnız sənin ID-ni yoxlayır (Yalnız sənə özəldir!)
    if payload.user_id != SAHIB_ID:
        return
    
    # Botun öz mesajıdısa və ya istənilən mesajdısa
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

    # Əgər atdığın emoji gülməli/joy tiplidirsə (🤣, 😂, 😆, 💀 və s.)
    gulmeli_emojiler = ["🤣", "😂", "😆", "💀", "😹"]
    
    if emoji_str in gulmeli_emojiler:
        # Sənin basdığın emojidən əlavə, avtomatik digər oxşar joy emojilərini də basır
        for e in gulmeli_emojiler:
            if e != emoji_str:
                try:
                    await message.add_reaction(e)
                except:
                    pass


# ==========================================
# --- 5. MASTER SAHİB PANELİ (TÜND QARA FON) ---
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu panel yalnız botun sahibinə məxsusdur!")
        return

    embed = discord.Embed(
        title="💀 YENİLMEZ OS // ELITE MASTER PANEL v500",
        description="Serverin idarəetmə mərkəzi və xüsusi səlahiyyətli əmrlər siyahısı:",
        color=0x050505  # Dərin qara fon effekti
    )
    embed.add_field(
        name="👑 1. Sizin Xüsusi Sahib Əmrləriniz (Özəl)", 
        value="• `r?elan [mətn]` — Rəsmi elan atır (@everyone)\n• `r?anket [sual]` — Serverdə səsvermə anket açır\n• `r?cekilis [hədiyyə]` — Avtomatik çəkiliş başladır", 
        inline=False
    )
    embed.add_field(
        name="🔊 2. Səs Sistemi İdarəsi", 
        value="• `r?join` — Səs kanalına qoşular\n• `r?leave` — Səs kanalından ayrılar", 
        inline=False
    )
    embed.add_field(
        name="🛡️ 3. Sərt Moderasiya & Təhlükəsizlik", 
        value="• `r?sil [say]` — Mesajları təmizləyər\n• `r?mute [@istifadəçi]` — İstifadəçini susdurar\n• `r?unmute [@istifadəçi]` — Mute qaldırar\n• `r?ban [@istifadəçi]` — Serverdən qovar\n• `r?kick [@istifadəçi]` — Atar\n• `r?lock` / `r?unlock` — Kanalı bağlar/açar", 
        inline=False
    )
    embed.add_field(
        name="⚔️ 4. Auralı Oyunlar & Sistemlər", 
        value="• `r?duel [@istifadəçi]` — Bəhsə girmə / 1v1 döyüş\n• `r?coinflip [yazı/tura]` — Pul atma oyunu\n• `r?hacker [@istifadəçi]` — Gizli IP sızma simulyasiyası\n• `r?kasa` — Gizli server xəzinəsini yoxlama", 
        inline=False
    )
    embed.add_field(
        name="📊 5. Sistem & Profil Məlumatları", 
        value="• `r?ping` — Botun anlıq gecikməsi\n• `r?avatar [@istifadəçi]` — Şəkil çəkmə\n• `r?serverbilgi` — Server statları", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS Elite - All Rights Reserved 2026")
    await ctx.send(embed=embed)


# ==========================================
# --- 6. ÜMUMI ƏMRLƏR ---
# ==========================================
@bot.command(name="salam")
async def salam(ctx):
    await ctx.send(f"Aleykum salam, {ctx.author.mention}. Sistem tam gücdə işləyir. 🏴‍☠️")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"⚡ Ping: **{round(bot.latency * 1000)}ms**")


# ==========================================
# --- 7. SƏS KANALI İDARƏSİ ---
# ==========================================
@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("⚠️ Əvvəlcə hər hansı bir səs kanalına qoşulmalısan!")
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
# --- 8. SƏHİBƏ ÖZƏL: ELAN, ANKET, ÇƏKİLİŞ ---
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız botun sahibi işlədə bilər!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 RƏSMİ SERVER ELANI", description=elan_metni, color=0x050505)
    embed.set_footer(text=f"Elan edən Sahib: {ctx.author.name}")
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("📢")

@bot.command(name="anket")
async def anket(ctx, *, anket_suali: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmr yalnız sahibə özəldir!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 YENİ ANKET / SƏSVERMƏ", description=anket_suali, color=0x050505)
    embed.set_footer(text=f"Anket sahibi: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, *, hediyye: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmr yalnız sahibə özəldir!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="🎉 BÖYÜK ÇƏKİLİŞ", description=f"Hədiyyə: **{hediyye}**\n\nQatılmaq üçün aşağıdakı emojiye 🎁 bas!", color=0x050505)
    embed.set_footer(text="Çəkiliş Sistemi")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎁")


# ==========================================
# --- 9. MODERASİYA ---
# ==========================================
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
    await ctx.send(f"🔇 {member.mention} {dakika} dəqiqə mute olundu.")

@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute_cmd(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} üçün mute qaldırıldı.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} ban olundu!")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} qovuldu!")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal kilitləndi!")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı!")


# ==========================================
# --- 10. AURALİ & ELİT OYUNLAR ---
# ==========================================
@bot.command(name="duel")
async def duel(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("⚠️ Duel etmək üçün kimsəni etiketləməlisən: `r?duel @istifadəçi`")
        return
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ Gərgin döyüş başladı!\n🔥 Qalib gələn tərəf: **{kazanan.name}** oldu! 🏆")

@bot.command(name="coinflip")
async def coinflip(ctx, secim: str = None):
    if not secim:
        await ctx.send("⚠️ Seçim etməlisən: `r?coinflip yazi` və ya `r?coinflip tura`")
        return
    netice = random.choice(["yazı", "tura"])
    if secim.lower() == netice:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Təbriklər, qazandın! 😎")
    else:
        await ctx.send(f"🪙 Nəticə: **{netice}**. Uduzdun, bəxtini yenidən sına!")

@bot.command(name="hacker")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip = f"{random.randint(40, 200)}.{random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}"
    await ctx.send(f"💻 **{target.name}** sisteminə sızıldı! IP: `{ip}` | Əməliyyat uğurludur 🕵️‍♂️")

@bot.command(name="kasa")
async def kasa(ctx):
    qazanc = random.randint(100, 5000)
    await ctx.send(f"💎 Serverin gizli xəzinə kassası açıldı! İçindən **{qazanc} AZN** dəyərində qənimət çıxdı, {ctx.author.mention}!")


# ==========================================
# --- 11. MƏLUMAT VƏ PROFİL ---
# ==========================================
@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name} - Avatar", color=0x050505)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="serverbilgi")
async def serverbilgi(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 {guild.name} - Server Statistikası", color=0x050505)
    embed.add_field(name="👥 Üzvlər", value=guild.member_count, inline=True)
    embed.add_field(name="👑 Sahib", value=guild.owner, inline=True)
    embed.add_field(name="📅 Yaradılış", value=str(guild.created_at.date()), inline=True)
    await ctx.send(embed=embed)


# ==========================================
# --- 12. İŞƏ SALMA ---
# ==========================================
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
    
