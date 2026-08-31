import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
import time
from flask import Flask
from threading import Thread

# --- KÜÇÜK FLASK SERVER (Render üçün) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot onlayndır!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ----------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="r?", intents=intents)

# 👑 SƏNİN DİSCORD İD-N 👑
SAHIB_ID = 1391781251390451713

# Yaddaş Sistemləri
ticket_span_kontrol = {}
user_xp = {}
spam_takip = {}

@bot.event
async def on_ready():
    print(f"🔥 Bot uğurla işə düşdü: {bot.user.name} 🔥")
    await bot.change_presence(activity=discord.Game(name="r?yardim | DEADAZE v5000 👑"))
    stats_update.start()
    voice_xp_loop.start()

# ==============================================================================
# 👋 1. AVTO XOŞ GƏLDİN VƏ VİDALAŞMA SİSTEMİ
# ==============================================================================

@bot.event
async def on_member_join(member):
    kanal = discord.utils.get(member.guild.text_channels, name="gələn-gedən")
    if not kanal:
        kanal = member.guild.system_channel
    
    if kanal:
        embed = discord.Embed(
            title="🎉 Serverimizə Yeni Üzv Qoşuldu!",
            description=f"Salam {member.mention}! Xoş gəldin, səninlə birlikdə **{member.guild.member_count}** nəfər olduq! 🚀",
            color=0x00ff88
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await kanal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    kanal = discord.utils.get(member.guild.text_channels, name="gələn-gedən")
    if not kanal:
        kanal = member.guild.system_channel
    
    if kanal:
        embed = discord.Embed(
            title="👋 Aramızdan Biri Ayrıldı",
            description=f"**{member.name}** serverdən ayrıldı. Yolu açıq olsun! 🥀",
            color=0xff3333
        )
        await kanal.send(embed=embed)

# ==============================================================================
# 📊 3. CANLI STATİSTİKA KANALLARI (SİSTEMİ)
# ==============================================================================

@tasks.loop(minutes=10)
async def stats_update():
    for guild in bot.guilds:
        try:
            toplam_uye = guild.member_count
            online_uye = sum(1 for m in guild.members if m.status != discord.Status.offline)
            sesde_olanlar = sum(len(vc.members) for vc in guild.voice_channels)

            for channel in guild.channels:
                if "Üzv:" in channel.name or "Onlayn:" in channel.name or "Səs:" in channel.name:
                    if "Üzv:" in channel.name:
                        await channel.edit(name=f"📊 Üzv: {toplam_uye}")
                    elif "Onlayn:" in channel.name:
                        await channel.edit(name=f"🟢 Onlayn: {online_uye}")
                    elif "Səs:" in channel.name:
                        await channel.edit(name=f"🔊 Səs: {sesde_olanlar}")
        except Exception as e:
            print(f"Statistika yenilənmə xətası: {e}")

# ==============================================================================
# 🎙️ 4. SƏS KANALINDA XP (VOICE XP) QAZANMA SİSTEMİ
# ==============================================================================

@tasks.loop(minutes=1)
async def voice_xp_loop():
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if len(vc.members) > 1:
                for member in vc.members:
                    if member.bot:
                        continue
                    
                    author_id = member.id
                    if author_id not in user_xp:
                        user_xp[author_id] = {"xp": 0, "level": 1}
                    
                    user_xp[author_id]["xp"] += 15
                    gerekli_xp = user_xp[author_id]["level"] * 100

                    if user_xp[author_id]["xp"] >= gerekli_xp:
                        user_xp[author_id]["level"] += 1
                        user_xp[author_id]["xp"] = 0
                        try:
                            if guild.system_channel:
                                await guild.system_channel.send(f"🎉 Təbriklər {member.mention}! Səs kanalında aktiv olduğuna görə səviyyə yüksəldin: **Səviyyə {user_xp[author_id]['level']}** 🎙️🚀")
                        except:
                            pass

# ==============================================================================
# 🛡️ AĞILLI SPAM, XP VƏ GÜLÜŞ SİSTEMİ
# ==============================================================================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    gulus_sozleri = ["xd", "asds", "guly", "kara", "hf", "latifə", "😂", "🤣", "💀", "😹", "😆"]
    if any(g in message.content.lower() for g in gulus_sozleri):
        try:
            gulmeli_emojiler = ["😂", "🤣", "💀", "😹", "😆", "🫠"]
            secilenler = random.sample(gulmeli_emojiler, 3)
            for emj in secilenler:
                await message.add_reaction(emj)
        except:
            pass

    author_id = message.author.id
    sindi = time.time()

    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}
    
    user_xp[author_id]["xp"] += 10
    gerekli_xp = user_xp[author_id]["level"] * 100

    if user_xp[author_id]["xp"] >= gerekli_xp:
        user_xp[author_id]["level"] += 1
        user_xp[author_id]["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Yeni səviyyəyə yüksəldin: **Səviyyə {user_xp[author_id]['level']}** 🚀")
        except:
            pass

    if author_id != SAHIB_ID:
        if author_id not in spam_takip:
            spam_takip[author_id] = []
        
        spam_takip[author_id] = [t for t in spam_takip[author_id] if sindi - t < 3]
        spam_takip[author_id].append(sindi)

        if len(spam_takip[author_id]) >= 9:
            try:
                await message.delete()
                muteli_vaxt = discord.utils.utcnow() + discord.timedelta(seconds=30)
                await message.author.timeout(muteli_vaxt, reason="Həddindən artıq spam / random atmaq")
                await message.channel.send(f"⚠️ {message.author.mention}, həddindən artıq spam/random yazdığın üçün 30 saniyəlik vaxt aşımı (mute) aldın!", delete_after=5)
                return
            except Exception as e:
                print(f"Spam cəza xətası: {e}")

    await bot.process_commands(message)

# ==============================================================================
# ✨ EMOJI MIRROR
# ==============================================================================

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id != SAHIB_ID:
        return
    
    try:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.add_reaction(payload.emoji)
    except Exception as e:
        print(f"Reaction xətası: {e}")

# ==============================================================================
# 👑 YARDIM VƏ BÜTÜN MƏLUMAT KOMANDALARI
# ==============================================================================

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(
        title="👑 MASTER PANEL v5000 (Bütün Komutlar)",
        description="Bütün gücləndirilmiş əmrlər və onların açıqlamaları:",
        color=0xffa200
    )
    
    sahib_desc = (
        "`r?elan` - Serverdə xüsusi elan paylaşırsan.\n"
        "`r?anket` - Səsvermə anketi yaradırsan.\n"
        "`r?cekilis [vaxt] [ödül]` - Avtomatik çəkiliş başladır (Məs: `r?cekilis 2d Nitro`).\n"
        "`r?duyuru` - Rəsmi duyuru elan edirsən.\n"
        "`r?bakim` - Botu baxım rejiminə alırsan.\n"
        "`r?ticket` - Sənin üçün avtomatik dəstək kanalı yaradır."
    )
    embed.add_field(name="👑 Sahib & İdarəetmə Komutları", value=sahib_desc, inline=False)

    kanal_desc = (
        "`r?gizle` / `r?goster` - Yazı kanalını gizlədir/açır.\n"
        "`r?sesgizle` / `r?sesgoster` - Səs kanalını bağlayır/açır."
    )
    embed.add_field(name="🛡️ Kanal İdarəsi Komutları", value=kanal_desc, inline=False)

    stat_desc = (
        "`r?server` - Server məlumatı.\n"
        "`r?userinfo` - İstifadəçi məlumatı.\n"
        "`r?botinfo` - Bot versiyası.\n"
        "`r?ping` - Gecikməni ölçür.\n"
        "`r?level` - Səviyyəni göstərir."
    )
    embed.add_field(name="📋 Məlumat & Statistika Komutları", value=stat_desc, inline=False)

    mod_desc = (
        "`r?sil` - Mesaj silir.\n"
        "`r?mute` / `r?unmute` - Səssizləşdirir/açır.\n"
        "`r?ban` / `r?kick` - Banlayır/qovur.\n"
        "`r?nuke` - Kanalı sıfırlayır."
    )
    embed.add_field(name="🛠️ Moderasiya Komutları", value=mod_desc, inline=False)

    oyun_desc = (
        "`r?duel`, `r?coinflip`, `r?slot`, `r?iq`, `r?balıq` - Əyləncə oyunları."
    )
    embed.add_field(name="🎮 Əyləncə Komutları", value=oyun_desc, inline=False)

    embed.set_footer(text="DEADAZE Security Systems | v5000 Pro Max")
    await ctx.send(embed=embed)

@bot.command(name="botinfo")
async def botinfo(ctx):
    await ctx.send("🤖 **Bot Sürümü:** `v5000 Ultra Pro Max` | Python & Discord.py ⚡")

@bot.command(name="server")
async def server(ctx):
    g = ctx.guild
    await ctx.send(f"🏰 **Server:** {g.name} | **Üzv:** {g.member_count} | **Yaradılma:** {g.created_at.strftime('%d.%m.%Y')}")

@bot.command(name="userinfo")
async def userinfo(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(f"👤 **İstifadəçi:** {u.name} | **ID:** {u.id} | **Qoşuldu:** {u.joined_at.strftime('%d.%m.%Y')}")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Gecikmə: **{round(bot.latency * 1000)}ms** ⚡")

@bot.command(name="online")
async def online(ctx):
    c = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 **Aktiv (Onlayn) Üzv sayı:** {c}")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Bakı"):
    await ctx.send(f"🌤️ **{seher}** üçün hava istiliyi: **{random.randint(18, 35)}°C** (Günəşli ☀️)")

@bot.command(name="hesabla")
async def hesabla(ctx, *, islem: str):
    try:
        netice = eval(islem)
        await ctx.send(f"🧮 **Nəticə:** `{netice}` ✅")
    except:
        await ctx.send("❌ Xəta! Doğru riyazi əməliyyat daxil et ⚠️")

@bot.command(name="level")
async def level(ctx, m: discord.Member = None):
    target = m or ctx.author
    if target.id in user_xp:
        lvl = user_xp[target.id]["level"]
        xp = user_xp[target.id]["xp"]
        await ctx.send(f"⭐ **{target.name}** | Səviyyə: **{lvl}** 🏆 | XP: **{xp}** ⚡")
    else:
        await ctx.send(f"⭐ **{target.name}** hələ XP qazanmayıb! (Səviyyə 1) 🚀")

# ==============================================================================
# 👑 SAHİB & AVTO TAYMERLİ ÇƏKİLİŞ SİSTEMİ
# ==============================================================================

@bot.command(name="elan")
async def elan(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 ELAN", description=metin, color=0xffaa00)
    await ctx.send(embed=embed)

@bot.command(name="anket")
async def anket(ctx, *, soru: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 ANKET", description=soru, color=0x00ffcc)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, sure: str, *, odul: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()

    saniye = 0
    try:
        birim = sure[-1]
        sayi = int(sure[:-1])
        if birim == 's':
            saniye = sayi
        elif birim == 'm':
            saniye = sayi * 60
        elif birim == 'h':
            saniye = sayi * 3600
        elif birim == 'd':
            saniye = sayi * 86400
        else:
            await ctx.send("❌ Vaxt formatı səhvdir! Məsələn: `30s`, `10m`, `2h`, `2d` yaz.", delete_after=10)
            return
    except:
        await ctx.send("❌ Xəta! Nümunə istifadə: `r?cekilis 2d Promo Nitro`", delete_after=10)
        return

    embed = discord.Embed(
        title="🎉 HƏDİYYƏ ÇƏKİLİŞİ 🎉",
        description=f"Ödül: **{odul}**\nSüre: **{sure}**\n\nQatılmaq üçün aşağıdakı 🎉 emojisinə bas!",
        color=0xff0055
    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")

    await asyncio.sleep(saniye)

    try:
        yeni_msg = await ctx.channel.fetch_message(msg.id)
        users = []
        for reaction in yeni_msg.reactions:
            if str(reaction.emoji) == "🎉":
                async for user in reaction.users():
                    if not user.bot:
                        users.append(user)
        
        if len(users) > 0:
            kazanan = random.choice(users)
            await ctx.channel.send(f"🏆 **ÇƏKİLİŞ BİTDİ!** 🎉\nÖdül: **{odul}**\nTəbriklər {kazanan.mention}! Qazandın! 🎁👑")
        else:
            await ctx.channel.send(f"❌ **{odul}** çəkilişinə heç kim qoşulmadığı üçün qalib seçilmədi!")
    except Exception as e:
        print(f"Çəkiliş xətası: {e}")

@bot.command(name="duyuru")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"🔔 **DUYURU:** {metin}")

@bot.command(name="bakim")
async def bakim(ctx, durum: str = "açıq"):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send(f"🛠️ Baxım rejimi: **{durum}** olaraq dəyişdirildi! ⚠️")

# ==============================================================================
# 🛡️ KANAL GİZLƏMƏ KOMUTLARI
# ==============================================================================

@bot.command(name="gizle")
async def gizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🔒 Kanal uğurla gizlədildi! 👁️‍🗨️")

@bot.command(name="goster")
async def goster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🔓 Kanal hamı üçün göstərildi! ✅")

@bot.command(name="sesgizle")
async def sesgizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=False)
    await ctx.send("🔴 Səs kanalı girişə bağlandı! 🚫")

@bot.command(name="sesgoster")
async def sesgoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=True)
    await ctx.send("🟢 Səs kanalı girişə açıldı! 🟢")

# ==============================================================================
# 🛠️ MODERASİYA, ROL VƏ İDARƏ KOMUTLARI
# ==============================================================================

@bot.command(name="sil")
async def sil(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 {amount} ədəd mesaj silindi! ✨", delete_after=3)

@bot.command(name="mute")
async def mute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for c in ctx.guild.channels:
            await c.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.mention} səssizləşdirildi! 🔴")

@bot.command(name="unmute")
async def unmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role: await member.remove_roles(role)
    await ctx.send(f"🔊 {member.mention} səsi açıldı! 🟢")

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} banlandı! 🔴")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} qovuldu! ⚡")

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID: return
    pos = ctx.channel.position
    yeni = await ctx.channel.clone(reason="Nuke olundu")
    await ctx.channel.delete()
    await yeni.edit(position=pos)
    await yeni.send("💥 Kanal sıfırlandı və yenidən quruldu! 🔥🚀")

# ==============================================================================
# 🎮 OYUNLAR & ƏYLƏNCƏ KOMUTLARI
# ==============================================================================

@bot.command(name="duel")
async def duel(ctx, member: discord.Member):
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ **{ctx.author.name}** vs **{member.name}** dueli başladı! 🏆 Qalib: {kazanan.mention}!")

@bot.command(name="coinflip")
async def coinflip(ctx):
    res = random.choice(["Yazı 🪙", "Tura 👑"])
    await ctx.send(f"🎲 Nəticə: **{res}**")

@bot.command(name="slot")
async def slot(ctx):
    emojis = ["🍎", "🍋", "🍒", "7️⃣", "💎"]
    a, b, c = random.choice(emojis), random.choice(emojis), random.choice(emojis)
    msg = f"🎰 [{a} | {b} | {c}]\n"
    msg += "🎉 UDDUNUZ! 💎" if a == b == c else "❌ Uduzdunuz, yenidən cəhd edin!"
    await ctx.send(msg)

@bot.command(name="iq")
async def iq(ctx, m: discord.Member = None):
    target = m or ctx.author
    await ctx.send(f"🧠 **{target.name}** IQ Səviyyəsi: **{random.randint(50, 160)}**")

@bot.command(name="balıq")
async def balıq(ctx):
    fishes = ["🐟 Balıq", "🐠 Qızıl Balıq", "🦈 Akula", "👞 Köhnə Başmaq"]
    await ctx.send(f"🎣 Tutduğun əşya: **{random.choice(fishes)}**")

# ==============================================================================
# 🎫 BİRBAŞA r?ticket YAZANDA KANAL YARADAN SİSTEM
# ==============================================================================

class TicketKapatView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket-i Bağla", emoji="🔒", style=discord.ButtonStyle.red, custom_id="ticket_kapat_buton")
    async def ticket_kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Dəstək kanalı 3 saniyəyə silinir...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()

@bot.command(name="ticket")
async def ticket(ctx):
    await ctx.message.delete()  # İstifadəçinin yazdığı r?ticket mesajını silir ki, kanal təmiz qalsın
    guild = ctx.guild
    author = ctx.author
    sindi = time.time()

    if author.id != SAHIB_ID:
        if author.id not in ticket_span_kontrol:
            ticket_span_kontrol[author.id] = []
        ticket_span_kontrol[author.id] = [t for t in ticket_span_kontrol[author.id] if sindi - t < 30]
        ticket_span_kontrol[author.id].append(sindi)
        if len(ticket_span_kontrol[author.id]) >= 3:
            await ctx.send(f"⚠️ {author.mention}, çox sürətli ticket açmağa çalışırsan!", delete_after=5)
            return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
    }

    channel = awai
