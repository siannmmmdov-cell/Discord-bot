import discord
from discord.ext import commands
import time
from datetime import timedelta
import os
from flask import Flask
from threading import Thread

# ==========================================
# --- 1. RENDER ÜÇÜN DİNAMİK PORTlu FLASK ---
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Yenilmez OS Security v1500 aktivdir!"

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
intents.bans = True
intents.moderation = True

bot = commands.Bot(command_prefix="r?", intents=intents)

# Yalnız sənin ID-n (Master Sahib)
SAHIB_ID = 641014966312501259

spam_records = {}
SPAM_WINDOW = 4.0       

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f" [X] YENILMEZ OS v1500 SECURITY MASTER AKTİVDİR!")
    print(f" [X] Bot Adı: {bot.user.name}")
    print(f" [X] Sahib ID: {SAHIB_ID}")
    print(f"==================================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="r?bot | Server Security 🛡️"))


# ==========================================
# --- 3. AVTO-ANTİ-RAID & BOT QORUNMASI ---
# ==========================================
@bot.event
async def on_member_join(member):
    # Əgər serverə kənar bot girərsə dərhal qov
    if member.bot and member.id != bot.user.id:
        try:
            await member.guild.ban(member, reason="Təhlükəsizlik: İnsiz kənar bot girişi aşkarlandı!")
            return
        except:
            pass


# ==========================================
# --- 4. SƏRT TƏHLÜKƏSİZLİK & REKLAM BLOKU ---
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Sahib və Adminlərə qadağalar şamil olunmur
    if message.author.guild_permissions.administrator or message.author.id == SAHIB_ID:
        await bot.process_commands(message)
        return

    content_lower = message.content.lower()

    # Reklam, Discord dəvəti və ya kənar link qadağası
    if "discord.gg/" in content_lower or "discord.com/invite/" in content_lower or "http://" in content_lower or "https://" in content_lower:
        try:
            await message.delete()
            await message.channel.send(f"🚨 {message.author.mention}, bu serverdə link və reklam paylaşmaq qəti qadağandır!", delete_after=5)
            await message.author.timeout(timedelta(minutes=15), reason="Server Təhlükəsizliyi: Link/Reklam Paylaşımı")
        except:
            pass
        return

    # Spam və Flood qorunması
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
            if data["warns"] == 1:
                try:
                    await message.channel.send(f"⚠️ {message.author.mention}, zəhmət olmasa spam etməyin!", delete_after=4)
                except:
                    pass
            elif data["warns"] >= 2:
                try:
                    await message.author.timeout(timedelta(minutes=10), reason="Anti-Spam Təhlükəsizlik Sistemi")
                    await message.channel.send(f"🔇 {message.author.mention}, ardıcıl spam etdiyiniz üçün 10 dəqiqəlik mute olundunuz!", delete_after=5)
                    data["warns"] = 0 
                except:
                    pass
            return
        else:
            data["last_time"] = current_time
            if data["warns"] > 0:
                data["warns"] -= 1

    await bot.process_commands(message)


# ==========================================
# --- 5. MASTER SAHİB & TƏHLÜKƏSİZLİK PANELİ ---
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu panel yalnız baş sahibə məxsusdur!")
        return

    embed = discord.Embed(
        title="🛡️ YENİLMEZ OS // SECURITY MASTER PANEL v1500",
        description="Serverin təhlükəsizlik mərkəzi və sərt müdafiə əmrləri siyahısı:",
        color=0x0f0f0f
    )
    embed.add_field(
        name="👑 1. Sahib & İdarəetmə Əmrləri", 
        value="• `r?elan [mətn]` — @everyone ilə rəsmi server elanı atır\n• `r?anket [sual]` — Serverdə rəsmi səsvermə açır\n• `r?cekilis [vaxt] [hədiyyə]` — Avtomatik təhlükəsiz çəkiliş", 
        inline=False
    )
    embed.add_field(
        name="📊 2. Server & Auditoriya Məlumatı", 
        value="• `r?server` — Serverin təhlükəsizlik və üzv statusu\n• `r?userinfo [@istifadəçi]` — İstifadəçinin qeydiyyat və profil yoxlanışı\n• `r?botinfo` — Botun sistem aktivliyi", 
        inline=False
    )
    embed.add_field(
        name="🔊 3. Səs Kanalı İdarəsi", 
        value="• `r?join` — Səs kanalına qoşular\n• `r?leave` — Səs kanalından ayrılar", 
        inline=False
    )
    embed.add_field(
        name="🛡️ 4. Sərt Təhlükəsizلىk & Moderasiya", 
        value="• `r?sil [say]` — Mesajları kütləvi təmizləyər\n• `r?mute [@istifadəçi] [dəqiqə]` — İstifadəçini susdurar\n• `r?unmute [@istifadəçi]` — Mute cəzasını qaldırar\n• `r?warn [@istifadəçi] [səbəb]` — Rəsmi xəbərdarlıq verər\n• `r?ban [@istifadəçi]` — Serverdən daimi uzaqlaşdırar\n• `r?kick [@istifadəçi]` — Serverdən atar\n• `r?lock / r?unlock` — Kanalı kilidləyər / açar\n• `r?slowmode [saniyə]` — Çata axın qorunması qoyar", 
        inline=False
    )
    embed.set_footer(text="Yenilmez OS Security Core - All Rights Reserved 2026")
    await ctx.send(embed=embed)


# ==========================================
# --- 6. MƏLUMAT VƏ STATUS ƏMRLƏRİ ---
# ==========================================
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"⚡ Sistem Gecikməsi (Ping): **{round(bot.latency * 1000)}ms**")

@bot.command(name="botinfo")
async def botinfo(ctx):
    embed = discord.Embed(title="🛡️ Təhlükəsizlik Botu Statusu", color=0x0f0f0f)
    embed.add_field(name="Sistem Versiyası", value="v1500 Security Master", inline=True)
    embed.add_field(name="Qorunan Serverlər", value=str(len(bot.guilds)), inline=True)
    embed.set_footer(text="Yenilmez OS Security")
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
    roles_str = ", ".join(roles) if roles else "Rol yoxdur"
    
    embed = discord.Embed(title=f"👤 Təhlükəsizlik Yoxlanışı — {member.name}", color=0x0f0f0f)
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="İstifadəçi ID", value=str(member.id), inline=True)
    embed.add_field(name="Serverə Qoşulma", value=f"<t:{int(member.joined_at.timestamp())}:R>", inline=True)
    embed.add_field(name="Aktiv Rolları", value=roles_str, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="server", aliases=["serverinfo", "bilgi"])
async def server_info(ctx):
    guild = ctx.guild
    online_count = sum(1 for m in guild.members if m.status == discord.Status.online)
    
    embed = discord.Embed(title=f"🛡️ {guild.name} — Təhlükəsizlik Hesabatı", color=0x0f0f0f)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="👑 Baş Sahib", value=f"{guild.owner.mention if guild.owner else 'Naməlum'}", inline=True)
    embed.add_field(name="👥 Toplam Üzv", value=f"**{guild.member_count}** nəfər", inline=True)
    embed.add_field(name="🟢 Online Üzvlər", value=str(online_count), inline=True)
    embed.set_footer(text=f"Yoxlayan: {ctx.author.name}")
    await ctx.send(embed=embed)


# ==========================================
# --- 7. SƏS KANALI İDARƏSİ ---
# ==========================================
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
    await ctx.send(f"🔊 Səs kanalına qoşuldum: **{channel.name}**")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 Səs kanalından ayrıldım.")
    else:
        await ctx.send("⚠️ Onsuz da heç bir səs kanalında deyiləm!")


# ==========================================
# --- 8. SAHİBƏ ÖZƏL: ELAN, ANKET, ÇƏKİLİŞ ---
# ==========================================
@bot.command(name="elan")
async def elan(ctx, *, elan_metni: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Yalnız baş sahib bu əmri işlədə bilər!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📢 RƏSMİ SERVER ELANI", description=elan_metni, color=0x0f0f0f)
    embed.set_footer(text=f"Elan edən: {ctx.author.name}")
    msg = await ctx.send("@everyone", embed=embed)
    await msg.add_reaction("📢")

@bot.command(name="anket")
async def anket(ctx, *, anket_suali: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Yalnız baş sahib bu əmri işlədə bilər!")
        return
    await ctx.message.delete()
    embed = discord.Embed(title="📊 RƏSMİ SƏSVERMƏ / ANKET", description=anket_suali, color=0x0f0f0f)
    embed.set_footer(text=f"Anket sahibi: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, vaxt_str: str, *, hediyye: str):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Yalnız baş sahib bu əmri işlədə bilər!")
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
        await ctx.send("⚠️ Düzgün daxil edin!")
        return

    embed = discord.Embed(title="🎉 RƏSMİ SERVER ÇƏKİLİŞİ", description=f"Hədiyyə: **{hediyye}**\n\nQatılmaq üçün 🎁 emojisinə basın!\n⏳ Müddət: **{vaxt_str}**", color=0x0f0f0f)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎁")

    import asyncio
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

    import random
    kazanan = random.choice(istirakcilar)
    win_embed = discord.Embed(title="🏆 ÇƏKİLİŞ QALİBİ!", description=f"Hədiyyə: **{hediyye}**\nTəbriklər, {kazanan.mention}! 🎉", color=0x0f0f0f)
    await ctx.send(embed=win_embed)


# ==========================================
# --- 9. MODERASİYA & MÜDAFİƏ ƏMRLƏRİ ---
# ==========================================
@bot.command(name="sil")
@commands.has_permissions(manage_messages=True)
async def sil(ctx, say: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=say)
    await ctx.send(f"🧹 Təhlükəsizlik: {len(deleted)} mesaj təmizləndi.", delete_after=3)

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute_cmd(ctx, member: discord.Member, dakika: int = 5):
    await member.timeout(timedelta(minutes=dakika))
    await ctx.send(f"🔇 {member.mention} {dakika} dəqiqə müddətinə susduruldu.")

@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute_cmd(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} istifadəçisinin susdurulma cəzası qaldırıldı.")

@bot.command(name="warn")
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, sebeb="Göstərilməyib"):
    await ctx.message.delete()
    await ctx.send(f"⚠️ {member.mention}, rəsmi xəbərdarlıq aldınız! Səbəb: **{sebeb}**")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, saniye: int = 0):
    await ctx.channel.edit(slowmode_delay=saniye)
    if saniye == 0:
        await ctx.send("⏱️ Çat üçün yavaş rejim (Slowmode) söndürüldü.")
    else:
        await ctx.send(f"⏱️ Çat üçün yavaş rejim **{saniyə} saniyə** olaraq aktivləşdirildi.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} serverdən daimi olaraq ban olundu! Səbəb: {reason}")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} serverdən uzaqlaşdırıldı! Səbəb: {reason}")

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Təhlükəsizlik: Bu kanal yazışmalara bağlanıldı!")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Təhlükəsizlik: Bu kanal yenidən yazışmalara açıldı!")


# ==========================================
# --- 10. İŞƏ SALMA ---
# ==========================================
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
    
