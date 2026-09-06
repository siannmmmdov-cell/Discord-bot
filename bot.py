# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
import time
import re
from flask import Flask
from threading import Thread

# ==========================================
# RENDER ÜÇÜN HƏMİŞƏAKTİV (KEEP-ALIVE) SERVERİ
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "V80000 Ultra Bot Online və Aktivdir!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# DİSCORD İNTENTS VƏ BOTUN TƏRİFİ
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.webhooks = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# SAHİB VƏ TƏHLÜKƏSİZLİK TƏNZİMLƏMƏLƏRİ
# ==========================================
SAHIB_ID = 64101498631250250  
ICAZELI_BOTLAR = [SAHIB_ID] 

user_xp = {}
spam_takip = {}
auto_role_name = "Üzv"

# ==========================================
# BOT HAZIR OLDUqda İŞLƏYƏN FUNKSİYA
# ==========================================
@bot.event
async def on_ready():
    print(f"==========================================")
    print(f" V80000 Ultra Qoruma Sistemi Aktivləşdi!")
    print(f" Botun Adı: {bot.user.name}")
    print(f" ID: {bot.user.id}")
    print(f"==========================================")
    await bot.change_presence(activity=discord.Game(name="!bot | V80000 Ultra Qoruma"))

# ==========================================
# YENİ ÜZV QOŞULANDA VƏ BOT QORUMASI
# ==========================================
@bot.event
async def on_member_join(member):
    if member.bot:
        if member.id in ICAZELI_BOTLAR:
            return
        
        sahib_isvi = False
        try:
            await asyncio.sleep(1.5)
            async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.bot_add):
                if entry.target.id == member.id:
                    if entry.user.id == SAHIB_ID:
                        sahib_isvi = True
                    break
        except:
            pass

        if not sahib_isvi:
            try:
                await member.ban(reason="V80000 Təhlükəsizlik: İcazəsiz kənar bot bloklandı!")
                return
            except:
                pass
        return

    try:
        role = discord.utils.get(member.guild.roles, name=auto_role_name)
        if role:
            await member.add_roles(role)
    except:
        pass

    channel = member.guild.system_channel
    if channel:
        try:
            embed = discord.Embed(
                title="✨ Serverimizə Xoş Gəldin!",
                description=f"Salam {member.mention}! Aramızda görməyimizə çox şadıq.\n\n🛡️ Serverimiz V80000 Ultra Təhlükəsizlik sistemi ilə qorunur.",
                color=0x00FFCC
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"{member.guild.name} Ailəsi")
            await channel.send(embed=embed)
        except:
            pass

# ==========================================
# MESAJ NƏZARƏTİ VƏ QURTULUŞ QAYDALARI
# ==========================================
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # --- /yenilmez olan mesajlara qətiyyən toxunmur ---
    if "/yenilmez" in message.content:
        await bot.process_commands(message)
        return

    # --- Webhook və Tətbiq/Tag (UYG) spamlarının dərhal silinməsi ---
    if message.webhook_id is not None:
        try:
            await message.delete()
            return
        except:
            pass

    if message.author.bot:
        if message.author.id == SAHIB_ID:
            pass
        else:
            return

    icerik = message.content
    icerik_lower = icerik.lower().strip()
    
    # --- SALAM Kəlməsinə Avtomatik Cavab ---
    if icerik_lower in ["salam", "salamun aleykum", "sa", "slm", "as"]:
        try:
            await message.reply(f"Salam, xoş gəldin {message.author.mention}! 🤝 Necəsən?")
        except:
            pass

    # Sahiblərə və adminlərə məhdudiyyət yoxdur
    if message.author.id == SAHIB_ID or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    sindi = time.time()

    # --- REKLAM, LİNK VƏ /tag QORUMASI ---
    if "discord.gg/" in icerik_lower or "discord.com/invite/" in icerik_lower or "gg/" in icerik_lower or "http://" in icerik_lower or "https://" in icerik_lower or icerik_lower.startswith("/tag"):
        try:
            await message.delete()
            await message.guild.ban(message.author, reason="V80000: Reklam, link və ya icazəsiz tag qadağandır!")
            return
        except:
            pass

    # --- SPAM / FLOOD QORUMASI (1-ci, 2-ci xəbərdarlıq, 3-cü də 15 saniyə timeout) ---
    if author_id not in spam_takip:
        spam_takip[author_id] = []

    spam_takip[author_id] = [t for t in spam_takip[author_id] if sindi - t < 5]
    spam_takip[author_id].append(sindi)

    spam_sayi = len(spam_takip[author_id])

    if spam_sayi == 2:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, diqqətli ol, spam/flood etmə!", delete_after=4)
        except:
            pass
        return
    elif spam_sayi == 3:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, son xəbərdarlıq! Bir dənsə cəza alacaqsan.", delete_after=4)
        except:
            pass
        return
    elif spam_sayi > 3:
        try:
            await message.delete()
            duration = discord.utils.utcnow() + discord.timedelta(seconds=15)
            await message.author.timeout(duration, reason="Spam / Flood etdiyinə görə 15 saniyəlik zaman aşımı.")
            await message.channel.send(f"🔇 {message.author.mention}, spam/flood etdiyin üçün 15 saniyəlik zaman aşımı (mute) aldın!", delete_after=5)
        except:
            pass
        return

    # --- SONSUZ XP VƏ LEVEL SİSTEMİ ---
    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}

    user_xp[author_id]["xp"] += 15
    gerekli_xp = user_xp[author_id]["level"] * 100

    if user_xp[author_id]["xp"] >= gerekli_xp:
        user_xp[author_id]["xp"] -= gerekli_xp
        user_xp[author_id]["level"] += 1
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın! Yeni sonsuz səviyyən: **{user_xp[author_id]['level']}**")
        except:
            pass

    await bot.process_commands(message)

# ==========================================
# BÖYÜK 70+ KOMUT VƏ İDARƏETMƏ PANELİ (!bot)
# ==========================================
@bot.command(name="bot")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="🤖 V80000 ULTRA TƏHLÜKƏSİZLİK & MODERASİYA",
        description="Server Təhlükəsizliyi və əsas amirlər paneli:",
        color=0xFF0000
    )
    embed.add_field(name="!ban", value="İstifadəçini serverdən qəti ban edər.", inline=True)
    embed.add_field(name="!unban", value="İstifadəçinin banını açar.", inline=True)
    embed.add_field(name="!kick", value="İstifadəçini serverdən qovar.", inline=True)
    embed.add_field(name="!mute", value="İstifadəçini müvəqqəti səssizləşdirər.", inline=True)
    embed.add_field(name="!unmute", value="Səssizliyi dərhal qaldırar.", inline=True)
    embed.add_field(name="!clear", value="Mesajları kütləvi şəkildə təmizləyər.", inline=True)
    embed.add_field(name="!nuke", value="Kanalı sıfırdan təmizləyib yeniləyər.", inline=True)
    embed.add_field(name="!lock / !unlock", value="Kanalı yazışmaya bağlar / açar.", inline=True)

    embed2 = discord.Embed(
        title="📁 KANAL VƏ ROL İDARƏSİ",
        description="Kanalların və rolların idarə edilməsi:",
        color=0x00FF00
    )
    embed2.add_field(name="!createchannel / !createvoice", value="Yeni kanal yaradar.", inline=True)
    embed2.add_field(name="!deletechannel", value="Kanalı silər.", inline=True)
    embed2.add_field(name="!hide / !reveal", value="Kanalı gizlədar / göstərər.", inline=True)
    embed2.add_field(name="!giverole / !takerole", value="Rol verər / alar.", inline=True)
    embed2.add_field(name="!createrole / !deleterole", value="Rol yaradar / silər.", inline=True)

    embed3 = discord.Embed(
        title="⭐ ÜMUMİ VƏ ŞƏXSİ KOMUTLAR",
        description="Hər kəsin işlədə biləcəyi əmrlər:",
        color=0x0000FF
    )
    embed3.add_field(name="!ping", value="Botun şəbəkə gecikməsini ölçər.", inline=True)
    embed3.add_field(name="!level", value="Sonsuz XP və level sistemini göstərər.", inline=True)
    embed3.add_field(name="!userinfo", value="İstifadəçi haqqında ətraflı məlumat.", inline=True)
    embed3.add_field(name="!avatar", value="İstifadəçinin avatarını böyük göstərər.", inline=True)

    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)

# ==========================================
# SAHİB VƏ MODERASİYA ƏMRLƏRİ BLoku
# ==========================================
@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID:
        return
    await member.ban(reason=reason)
    await ctx.send(f"✅ {member.mention} serverdən ban edildi.")

@bot.command(name="unban")
async def unban(ctx, *, member_name):
    if ctx.author.id != SAHIB_ID:
        return
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name.lower() == member_name.lower():
            await ctx.guild.unban(user)
            await ctx.send(f"✅ {user.mention} ban-dan çıxarıldı.")
            return

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID:
        return
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} serverdən qovuldu.")

@bot.command(name="mute")
async def mute(ctx, member: discord.Member, minutes: int = 5):
    if ctx.author.id != SAHIB_ID:
        return
    duration = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
    await member.timeout(duration)
    await ctx.send(f"🔇 {member.mention} {minutes} dəqiqəlik mute-ləndi.")

@bot.command(name="unmute")
async def unmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID:
        return
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} mute-dən çıxarıldı.")

@bot.command(name="clear")
async def clear(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@bot.command(name="createchannel")
async def createchannel(ctx, *, isim):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"📁 **{isim}** adlı mətn kanalı yaradıldı.")

@bot.command(name="createvoice")
async def createvoice(ctx, *, isim):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.guild.create_voice_channel(isim)
    await ctx.send(f"🔊 **{isim}** adlı səs kanalı yaradıldı.")

@bot.command(name="deletechannel")
async def deletechannel(ctx, channel: discord.TextChannel = None):
    if ctx.author.id != SAHIB_ID:
        return
    channel = channel or ctx.channel
    await channel.delete()

@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal yazışmaya açıldı.")

@bot.command(name="hide")
async def hide(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🙈 Bu kanal hamıdan gizlətildi.")

@bot.command(name="reveal")
async def reveal(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🐵 Bu kanal yenidən hər kəsə göstərildi.")

@bot.command(name="slowmode")
async def slowmode(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Kanalın yavaş modu {seconds} saniyə edildi.")

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID:
        return
    kanal = ctx.channel
    konum = kanal.position
    yeni_kanal = await kanal.clone(reason="Nuke əmri ilə sıfırlandı")
    await kanal.delete()
    await yeni_kanal.edit(position=konum)
    await yeni_kanal.send("💥 Kanal uğurla nuke olundu, hər şey sıfırdan başladı!")

@bot.command(name="giverole")
async def giverole(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID:
        return
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} istifadəçisinə **{role.name}** rolu verildi.")

@bot.command(name="takerole")
async def takerole(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID:
        return
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} istifadəçisindən **{role.name}** rolu alındı.")

@bot.command(name="createrole")
async def createrole(ctx, *, rol_adi):
    if ctx.author.id != SAHIB_ID:
        return
    await ctx.guild.create_role(name=rol_adi)
    await ctx.send(f"✨ **{rol_adi}** adlı yeni rol yaradıldı.")

@bot.command(name="deleterole")
async def deleterole(ctx, role: discord.Role):
    if ctx.author.id != SAHIB_ID:
        return
    await role.delete()
    await ctx.send(f"🗑️ **{role.name}** rolu silindi.")

# ==========================================
# ÜMUMİ VƏ İSTİFADƏÇİ KOMUTLARI
# ==========================================
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Gecikmə: {round(bot.latency * 1000)}ms")

@bot.command(name="level")
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = user_xp.get(member.id, {"xp": 0, "level": 1})
    await ctx.send(f"⭐ {member.mention} sonsuz səviyyəsi: **{data['level']}** (Qalan XP: {data['xp']})")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"İstifadəçi Məlumatı - {member.name}", color=0x3498DB)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Qoşulma Tarixi", value=member.joined_at.strftime("%d-%m-%Y") if member.joined_at else "Bilinmir", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0xFF00FF)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

# ==========================================
# BAŞLANĞIC (MAIN) İŞLƏDİCİ
# ==========================================
if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get("TOKEN"))
                        
