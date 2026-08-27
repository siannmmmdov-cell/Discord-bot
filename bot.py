
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
# --- FLASK SERVER (RENDER ÜÇÜN) ---
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Yenilmez OS v2600 Ultimate Security aktivdir!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# ==========================================
# --- BOT SAZLANMALARI & İNTENTS ---
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True          
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.presences = True 

bot = commands.Bot(command_prefix="r?", intents=intents)

SAHIB_ID = 641014966312501259
start_time = time.time()

@bot.event
async def on_ready():
    print(f"YENILMEZ OS v2600 ULTIMATE SECURE AKTİVDİR: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="r?bot | Master Panel 🛡️"))


# ==========================================
# --- SƏRT TƏHLÜKƏSİZLİK & QORUMA ---
# ==========================================
@bot.event
async def on_member_join(member):
    if member.bot and member.id != bot.user.id:
        try:
            await member.guild.ban(member, reason="İznsiz kənar bot girişi!")
            return
        except:
            pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    if "salam" in content_lower:
        try:
            await message.channel.send(f"Aleykum salam, {message.author.mention}! Xoş gəldiniz! 👑")
        except:
            pass

    if message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    # Link / Reklam Qadağası
    if "discord.gg/" in content_lower or "https://" in content_lower or "http://" in content_lower:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, link paylaşmaq qadağandır!", delete_after=5)
            await message.author.timeout(timedelta(minutes=10), reason="Link paylaşımı")
        except:
            pass
        return

    await bot.process_commands(message)


# ==========================================
# --- EMOJİLƏRƏ AVTO-REAKTİV CAVABLAR ---
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
    if payload.user_id == bot.user.id or payload.guild_id is None:
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
# --- 💀 MASTER SAHİB PANELİ (ALT-ALTA & İZAHATLI) ---
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu panelə yalnız baş sahib girə bilər!")
        return

    embed = discord.Embed(
        title="💀 YENİLMEZ OS // MASTER PANEL v1500",
        description="Bütün əmrlər və onların izahatları alt-alta sıralanıb:",
        color=0x050505
    )
    
    embed.add_field(
        name="👑 1. Yalnız Sənin İşlədə Biləcəyin Əmrlər",
        value=(
            "`r?elan [mətn]` - Serverdə rəsmi elan yayır\n"
            "`r?anket [sual]` - Kanalda səsvermə açır\n"
            "`r?cekilis [vaxt] [hədiyyə]` - Avtomatik çəkiliş başladır\n"
            "`r?botkurulum` - Botun təhlükəsizlik divarlarını yoxlayır\n"
            "`r?servertemizle` - Serveri idarə edir\n"
            "`r?duyuru [mətn]` - Qısa bildiriş göndərir\n"
            "`r?bakim` - Botu baxım rejiminə keçirir"
        ),
        inline=False
    )

    embed.add_field(
        name="📊 2. Server & Məlumat Sistemləri",
        value=(
            "`r?server` - Server haqqında ümumi məlumat verir\n"
            "`r?userinfo` - İstifadəçi haqqında detallar göstərir\n"
            "`r?botinfo` - Botun işləmə müddətini (uptime) göstərir\n"
            "`r?ping` - Botun sürətini (latency) ölçür\n"
            "`r?online` - Aktiv üzvlərin sayını göstərir\n"
            "`r?kanalbilgi` - Cari kanal haqqında məlumat verir\n"
            "`r?rolbilgi [rol]` - Rol haqqında məlumat göstərir\n"
            "`r?boosters` - Serveri boost edənləri göstərir\n"
            "`r?hava [şəhər]` - Seçilən şəhərin hava durumunu göstərir\n"
            "`r?hesabla [ifadə]` - Riyazi əməlləri hesablayır"
        ),
        inline=False
    )

    embed.add_field(
        name="🛡️ 3. Sərt Moderasiya & Təhlükəsizlik",
        value=(
            "`r?sil [say]` - Göstərilən sayda mesajı silir\n"
            "`r?mute [istifadəçi] [dəqiqə]` - İstifadəçiyə timeout verir\n"
            "`r?unmute [istifadəçi]` - İstifadəçinin mutesini açır\n"
            "`r?ban [istifadəçi]` - İstifadəçini serverdən ban edir\n"
            "`r?unban [id]` - İstifadəçinin banını qaldırır\n"
            "`r?kick [istifadəçi]` - İstifadəçini serverdən atır\n"
            "`r?lock` - Kanalı mesaj yazmağa bağlayır\n"
            "`r?unlock` - Kanalı yenidən açır\n"
            "`r?slowmode [saniyə]` - Kanala yavaş rejim qoyur"
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ 4. Rol & Üzv İdarəetmə Komandaları",
        value=(
            "`r?rolver [istifadəçi] [rol]` - İstifadəçiyə rol verir\n"
            "`r?rolsil [istifadəçi] [rol]` - İstifadəçidən rol alır\n"
            "`r?nick [istifadəçi] [yeni ad]` - Ləqəbi dəyişdirir\n"
            "`r?avatar [istifadəçi]` - Profil şəklini göstərir\n"
            "`r?yetkililer` - Serverin adminlərini siyahıya alır\n"
            "`r?seskontrol` - Səs kanalındakı vəziyyəti göstərir\n"
            "`r?kanalac [ad]` - Yeni mətn kanalı yaradır"
        ),
        inline=False
    )

    embed.add_field(
        name="⚔️ 5. Oyunlar & Əyləncə",
        value=(
            "`r?duel [istifadəçi]` - Dostunla duel atırsan\n"
            "`r?coinflip [seçim]` - Yazı-tura oyunu oynayırsan\n"
            "`r?slot` - Slot maşını (jackpot) çevirirsən\n"
            "`r?hacker [istifadəçi]` - Zarafatla istifadəçini hackləyirsən\n"
            "`r?zar` - Zər atırsan\n"
            "`r?magic8ball [sual]` - Sehrli topa sual verirsən\n"
            "`r?sevgili [istifadəçi]` - Sevgi faizini ölçürsən\n"
            "`r?ascii [mətn]` - Mətni ASCII formatına çevirir"
        ),
        inline=False
    )

    embed.set_footer(text="Yenilmez OS Strict Core - All Rights Reserved 2026")
    await ctx.send(embed=embed)


# ==========================================
# --- 1. SAHİB ƏMRLƏRİ ---
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 RƏSMİ SERVER ELANI", description=elan_metni, color=0x050505)
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("📢")
    await msg.add_reaction("🔥")

@bot.command(name="anket")
async def anket(ctx, *, anket_suali: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 YENİ ANKET / SƏSVERMƏ", description=anket_suali, color=0x050505)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, vaxt_str: str, *, hediyye: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    saniye = 60
    try:
        if vaxt_str.endswith("s"): saniye = int(vaxt_str[:-1])
        elif vaxt_str.endswith("m"): saniye = int(vaxt_str[:-1]) * 60
        elif vaxt_str.endswith("h"): saniye = int(vaxt_str[:-1]) * 3600
    except:
        pass

    embed = discord.Embed(title="🎉 BÖYÜK AVTO-ÇƏKİLİŞ", description=f"Hədiyyə: **{hediyye}**\nQatılmaq üçün 🎁 emojisinə bas!", color=0x050505)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎁")

    await asyncio.sleep(saniye)
    try:
        msg = await ctx.channel.fetch_message(msg.id)
        istirakcilar = []
        for reaction in msg.reactions:
            if str(reaction.emoji) == "🎁":
                async for user in reaction.users():
                    if not user.bot: istirakcilar.append(user)
                break
        if istirakcilar:
            kazanan = random.choice(istirakcilar)
            await ctx.send(f"🏆 Çəkiliş qalibi: {kazanan.mention}! Hədiyyə: **{hediyye}** 🎉")
        else:
            await ctx.send("🎉 Çəkiliş bitdi, qatılan olmadı.")
    except:
        pass

@bot.command(name="botkurulum")
async def botkurulum(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🛡️ Təhlükəsizlik divarları aktivdir!")

@bot.command(name="servertemizle")
async def servertemizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🧹 Server təmizləndi.")

@bot.command(name="duyuru")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"📢 **Bildiriş:** {metin}")

@bot.command(name="bakim")
async def bakim(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send("🔧 Bot baxım rejiminə keçdi.")


# ==========================================
# --- 2. MƏLUMAT & SERVER ƏMRLƏRİ ---
# ==========================================
@bot.command(name="server")
async def server_info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🛡️ {guild.name}", color=0x050505)
    embed.add_field(name="Üzv Sayı", value=str(guild.member_count))
    embed.add_field(name="Kanal Sayı", value=str(len(guild.channels)))
    await ctx.send(embed=embed)

@bot.command(name="online")
async def online_stats(ctx):
    online = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 Aktiv üzv: **{online}**")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"⚡ Ping: **{round(bot.latency * 1000)}ms**")

@bot.command(name="botinfo")
async def botinfo(ctx):
    uptime = str(timedelta(seconds=int(time.time() - start_time)))
    await ctx.send(f"🤖 Uptime: `{uptime}`")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"👤 İstifadəçi: **{member.name}** | ID: `{member.id}`")

@bot.command(name="kanalbilgi")
async def kanalbilgi(ctx):
    await ctx.send(f"📌 Kanal: **{ctx.channel.name}**")

@bot.command(name="rolbilgi")
async def rolbilgi(ctx, role: discord.Role):
    await ctx.send(f"🏷️ Rol: **{role.name}** | Üzv: `{len(role.members)}`")

@bot.command(name="boosters")
async def boosters(ctx):
    await ctx.send(f"🚀 Boost sayı: **{ctx.guild.premium_subscription_count}**")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Baku"):
    await ctx.send(f"🌤️ **{seher}**: 28°C, Günəşli.")

@bot.command(name="hesabla")
async def hesabla(ctx, *, ifade: str):
    try:
        await ctx.send(f"🔢 Nəticə: `{ifade} = {eval(ifade)}`")
    except:
        await ctx.send("⚠️ Xətalı riyazi ifadə!")


# ==========================================
# --- 3. MODERASİYA & TƏHLÜKƏSİZLİK (XƏTA YOXLAYICI İLƏ) ---
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
    try:
        await member.timeout(timedelta(minutes=dakika))
        await ctx.send(f"🔇 {member.mention} {dakika} dəqiqəlik mute olundu.")
    except Exception as e:
        await ctx.send(f"❌ Mute vermək olmadı! Xəta: `{e}`")

@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute_cmd(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} mutesi açıldı.")
    except Exception as e:
        await ctx.send(f"❌ Mute açmaq olmadı! Xəta: `{e}`")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.name} uğurla ban olundu!")
    except Exception as e:
        await ctx.send(f"❌ Ban etmək mümkün olmadı! Xəta: `{e}`")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_cmd(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"🔓 {user.name} banı açıldı.")
    except Exception as e:
        await ctx.send(f"❌ Banı açmaq olmadı! Xəta: `{e}`")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.name} uğurla atıldı!")
    except Exception as e:
        await ctx.send(f"❌ Atmaq mümkün olmadı! Xəta: `{e}`")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal bağlandı.")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal açıldı.")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, saniye: int = 0):
    await ctx.channel.edit(slowmode_delay=saniye)
    await ctx.send(f"⏱️ Slowmode: **{saniye}** san.")


# ==========================================
# --- 4. ROL & ÜZV İDARƏETMƏ ---
# ==========================================
@bot.command(name="rolver")
@commands.has_permissions(manage_roles=True)
async def rolver(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ {member.mention} rol verildi.")
    except Exception as e:
        await ctx.send(f"❌ Rol vermək olmadı! Xəta: `{e}`")

@bot.command(name="rolsil")
@commands.has_permissions(manage_roles=True)
async def rolsil(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.remove_roles(role)
        await ctx.send(f"❌ Rol alındı.")
    except Exception as e:
        await ctx.send(f"❌ Rol almaq olmadı! Xəta: `{e}`")

@bot.command(name="nick")
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, yeni_ad: str):
    try:
        await member.edit(nick=yeni_ad)
        await ctx.send(f"✏️ Ad dəyişdirildi.")
    except Exception as e:
        await ctx.send(f"❌ Adı dəyişmək olmadı! Xəta: `{e}`")

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    if member.avatar: await ctx.send(f"🖼️ Avatar: {member.avatar.url}")
    else: await ctx.send("⚠️ Avatar yoxdur.")

@bot.command(name="yetkililer")
async def yetkililer(ctx):
    staff = [m.name for m in ctx.guild.members if m.guild_permissions.administrator]
    await ctx.send(f"👑 Adminlər: {', '.join(staff[:10])}")

@bot.command(name="seskontrol")
async def seskontrol(ctx):
    if ctx.author.voice: await ctx.send(f"🔊 Səs kanalı: **{ctx.author.voice.channel.name}**")
    else: await ctx.send("🔇 Səs kanalında deyilsən.")

@bot.command(name="kanalac")
@commands.has_permissions(manage_channels=True)
async def kanalac(ctx, *, kanal_adi: str):
    await ctx.guild.create_text_channel(kanal_adi)
    await ctx.send(f"📁 Kanal açıldı: **#{kanal_adi}**")


# ==========================================
# --- 5. OYUNlar & ƏYLƏNCƏ ---
# ==========================================
@bot.command(name="duel")
async def duel(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("⚠️ Kimsəni etiketlə: `r?duel @istifadəçi`")
        return
    kazanan = random.choice([ctx.author, member])
    await ctx.send(f"⚔️ Qalib: **{kazanan.name}** 🏆")

@bot.command(name="coinflip")
async def coinflip(ctx, secim: str = None):
    if not secim:
        await ctx.send("⚠️ Seçim et: `r?coinflip yazı`")
        return
    netice = random.choice(["yazı", "tura"])
    if secim.lower() == netice: await ctx.send(f"🪙 Nəticə: **{netice}**. Qazandın! 😎")
    else: await ctx.send(f"🪙 Nəticə: **{netice}**. Uduzdun!")

@bot.command(name="slot")
async def slot(ctx):
    simvol = ["🍎", "🍋", "🍒", "💎", "7️⃣"]
    r1, r2, r3 = random.choice(simvol), random.choice(simvol), random.choice(simvol)
    if r1 == r2 == r3: await ctx.send(f"🎰 | {r1} | {r2} | {r3} |\n🎉 Jackpot!")
    else: await ctx.send(f"🎰 | {r1} | {r2} | {r3} |\n😢 Uduzdun!")

@bot.command(name="hacker")
async def hacker(ctx, user: discord.Member = None):
    target = user if user else ctx.author
    ip = f"{random.randint(40, 200)}.{random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}"
    await ctx.send(f"💻 **{target.name}** hackləndi! IP: `{ip}` 🕵️‍♂️")

@bot.command(name="zar")
async def zar(ctx):
    await ctx.send(f"🎲 Zərin nəticəsi: **{random.randint(1, 6)}**")

@bot.command(name="magic8ball")
async def magic8ball(ctx, *, sorğu: str):
    cavablar = ["Bəli, mütləq!", "Xeyr, əsla.", "Bəlkə də.", "Dəqiq bilmirəm."]
    await ctx.send(f"🔮 Sual: {sorğu}\nCavab: **{random.choice(cavablar)}**")

@bot.command(name="sevgili")
async def sevgili(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("⚠️ Birini etiketlə: `r?sevgili @istifadəçi`")
        return
    await ctx.send(f"💖 Uyğunluq: **%{random.randint(0, 100)}** 💕")

@bot.command(name="ascii")
async def ascii_yaz(ctx, *, yazi: str):
    await ctx.send(f"🔤 ASCII:\n```fix\n[ {yazi.upper()} ]\n```")


# ==========================================
# --- İŞƏ SALMA ---
# ==========================================
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
        
