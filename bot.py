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

app = Flask('')

@app.route('/')
def home():
    return "Bot online!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.reactions = True
intents.webhooks = True

bot = commands.Bot(command_prefix="!", intents=intents)

SAHIB_ID = 64101498631250250  
ICAZELI_BOTLAR = [SAHIB_ID] 

user_xp = {}
spam_takip = {}
auto_role_name = "Üzv"

@bot.event
async def on_ready():
    print(f"V6700 Ultra Qoruma Aktivləşdi! {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="!bot | V6700 Qoruma"))

@bot.event
async def on_member_join(member):
    if member.bot:
        if member.id in ICAZELI_BOTLAR:
            print(f"İcazəli bot qoşuldu: {member.name}")
            return

        sahib_isvi = False
        try:
            await asyncio.sleep(1.5)
            async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.bot_add):
                if entry.target.id == member.id:
                    if entry.user.id == SAHIB_ID:
                        sahib_isvi = True
                    break
        except Exception as e:
            print(f"Audit log xətası: {e}")

        if not sahib_isvi:
            try:
                await member.ban(reason="V6700 Təhlükəsizlik: İcazəsiz bot bloklandı!")
                print(f"İcazəsiz bot banlandı: {member.name}")
                return
            except:
                pass
        return

    # Avtomatik Rol Verilməsi
    try:
        role = discord.utils.get(member.guild.roles, name=auto_role_name)
        if role:
            await member.add_roles(role)
    except:
        pass

    # Səviyyəli və Düzgün Xoş Gəldin Mesajı
    channel = member.guild.system_channel
    if channel:
        try:
            embed = discord.Embed(
                title="✨ Serverimizə Xoş Gəldin!",
                description=f"Salam {member.mention}! Aramızda görməyimizə çox şadıq.\n\n🛡️ Serverimiz V6700 Təhlükəsizlik sistemi ilə qorunur.",
                color=0x00FFCC
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"{member.guild.name} Ailəsi")
            await channel.send(embed=embed)
        except:
            pass

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.bot:
        if message.author.id == SAHIB_ID:
            pass
        else:
            return

    # Sahib və ya Administratorlar rahat yaza bilər
    if message.author.id == SAHIB_ID or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    sindi = time.time()
    icerik = message.content
    icerik_lower = icerik.lower()

    # --- KƏSKİN REKLAM VƏ LİNK QORUMASI ---
    if "discord.gg/" in icerik_lower or "discord.com/invite/" in icerik_lower or "gg/" in icerik_lower or "http://" in icerik_lower or "https://" in icerik_lower:
        try:
            await message.delete()
            await message.guild.ban(message.author, reason="V6700: Reklam və Link atmaq qadağandır!")
            print(f"Reklamçı banlandı: {message.author.name} -> {icerik}")
            return
        except Exception as e:
            print(f"Ban xətası: {e}")
            pass

    # --- SPAM QORUMASI ---
    if author_id not in spam_takip:
        spam_takip[author_id] = []

    spam_takip[author_id] = [t for t in spam_takip[author_id] if sindi - t < 4]
    spam_takip[author_id].append(sindi)

    if len(spam_takip[author_id]) > 3:
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, çox sürətli mesaj yazırsan (Spam etmə)!", delete_after=5)
        except:
            pass
        return

    # --- XP VƏ LEVEL SİSTEMİ ---
    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}

    user_xp[author_id]["xp"] += 15
    gerekli_xp = user_xp[author_id]["level"] * 100 + 100

    if user_xp[author_id]["xp"] >= gerekli_xp:
        user_xp[author_id]["xp"] -= gerekli_xp
        user_xp[author_id]["level"] += 1
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın! Yeni səviyyən: **{user_xp[author_id]['level']}**")
        except:
            pass

    await bot.process_commands(message)

# --- BOTUN KOMUT MENYUSU (!bot) ---

@bot.command(name="bot")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="🤖 V6700 TƏHLÜKƏSİZLİK & MODERASİYA",
        description="Server Təhlükəsizliyi üçün əsas amirlər:",
        color=0xFF0000
    )
    embed.add_field(name="!ban", value="İstifadəçini ban edər.", inline=True)
    embed.add_field(name="!unban", value="İstifadəçinin banını açar.", inline=True)
    embed.add_field(name="!kick", value="İstifadəçini serverdən qovar.", inline=True)
    embed.add_field(name="!mute", value="İstifadəçini müvəqqəti səssizləşdirər.", inline=True)
    embed.add_field(name="!unmute", value="Səssizliyi qaldırar.", inline=True)
    embed.add_field(name="!clear", value="Mesajları kütləvi təmizləyər.", inline=True)
    embed.add_field(name="!nuke", value="Kanalı sıfırdan təmizləyər.", inline=True)
    embed.add_field(name="!lock / !unlock", value="Kanalı bağlar / açar.", inline=True)

    embed2 = discord.Embed(
        title="📁 KANAL VƏ ROL İDARƏSİ",
        description="Kanalların və rolların idarə edilməsi:",
        color=0x00FF00
    )
    embed2.add_field(name="!createchannel / !createvoice", value="Kanal açar.", inline=True)
    embed2.add_field(name="!deletechannel", value="Kanalı silər.", inline=True)
    embed2.add_field(name="!hide / !reveal", value="Kanalı gizlədar / göstərər.", inline=True)
    embed2.add_field(name="!giverole / !takerole", value="Rol verər / alar.", inline=True)
    embed2.add_field(name="!createrole / !deleterole", value="Rol yaradar / silər.", inline=True)

    embed3 = discord.Embed(
        title="⭐ ÜMUMİ VƏ ŞƏXSİ KOMUTLAR",
        description="Hər kəsin işlədə biləcəyi əmrlər:",
        color=0x0000FF
    )
    embed3.add_field(name="!ping", value="Botun gecikməsini ölçər.", inline=True)
    embed3.add_field(name="!level", value="XP və level göstərər.", inline=True)
    embed3.add_field(name="!userinfo", value="İstifadəçi məlumatı.", inline=True)
    embed3.add_field(name="!avatar", value="Avatarı göstərər.", inline=True)

    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)

# --- YALNIZ SƏNİN İŞLƏDƏ BİLƏCƏYİN RİSQLİ VƏ MODERASİYA ƏMRLƏRİ ---

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await member.ban(reason=reason)
    await ctx.send(f"✅ {member.mention} serverdən ban edildi.")

@bot.command(name="unban")
async def unban(ctx, *, member_name):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name.lower() == member_name.lower():
            await ctx.guild.unban(user)
            await ctx.send(f"✅ {user.mention} ban-dan çıxarıldı.")
            return
    await ctx.send("❌ Bu adla ban edilmiş istifadəçi tapılmadı.")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} serverdən qovuldu.")

@bot.command(name="mute")
async def mute(ctx, member: discord.Member, minutes: int = 5):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    duration = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
    await member.timeout(duration)
    await ctx.send(f"🔇 {member.mention} {minutes} dəqiqəlik mute-ləndi.")

@bot.command(name="unmute")
async def unmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} mute-dən çıxarıldı.")

@bot.command(name="clear")
async def clear(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 {len(deleted)} ədəd mesaj təmizləndi.", delete_after=3)

@bot.command(name="createchannel")
async def createchannel(ctx, *, isim):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"📁 **{isim}** adlı mətn kanalı yaradıldı.")

@bot.command(name="createvoice")
async def createvoice(ctx, *, isim):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.guild.create_voice_channel(isim)
    await ctx.send(f"🔊 **{isim}** adlı səs kanalı yaradıldı.")

@bot.command(name="deletechannel")
async def deletechannel(ctx, channel: discord.TextChannel = None):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    channel = channel or ctx.channel
    await channel.delete()

@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
async def unlock(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal yazışmaya açıldı.")

@bot.command(name="hide")
async def hide(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🙈 Bu kanal hamıdan gizlətildi.")

@bot.command(name="reveal")
async def reveal(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🐵 Bu kanal yenidən hər kəsə göstərildi.")

@bot.command(name="slowmode")
async def slowmode(ctx, seconds: int):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Kanalın yavaş modu {seconds} saniyə edildi.")

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    kanal = ctx.channel
    konum = kanal.position
    yeni_kanal = await kanal.clone(reason="Nuke əmri ilə sıfırlandı")
    await kanal.delete()
    await yeni_kanal.edit(position=konum)
    await yeni_kanal.send("💥 Kanal uğurla nuke olundu, hər şey sıfırdan başladı!")

@bot.command(name="rename")
async def rename(ctx, *, yeni_ad):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.channel.edit(name=yeni_ad)
    await ctx.send(f"✏️ Kanalın adı dəyişdirildi: **{yeni_ad}**")

@bot.command(name="giverole")
async def giverole(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} istifadəçisinə **{role.name}** rolu verildi.")

@bot.command(name="takerole")
async def takerole(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} istifadəçisindən **{role.name}** rolu alındı.")

@bot.command(name="createrole")
async def createrole(ctx, *, rol_adi):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await ctx.guild.create_role(name=rol_adi)
    await ctx.send(f"✨ **{rol_adi}** adlı yeni rol yaradıldı.")

@bot.command(name="deleterole")
async def deleterole(ctx, role: discord.Role):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    await role.delete()
    await ctx.send(f"🗑️ **{role.name}** rolu silindi.")

@bot.command(name="lockall")
async def lockall(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        except:
            pass
    await ctx.send("🔒 Bütün serverdəki mətn kanalları yazışmaya bağlandı.")

@bot.command(name="unlockall")
async def unlockall(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu komutu yalnız botun sahibi işlədə bilər!")
        return
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        except:
            pass
    await ctx.send("🔓 Bütün serverdəki mətn kanalları yazışmaya açıldı.")

# --- HƏR KƏSİN İŞLƏDƏ BİLƏCƏYİ NORMAL KOMUTLAR ---

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Gecikmə: {round(bot.latency * 1000)}ms")

@bot.command(name="level")
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = user_xp.get(member.id, {"xp": 0, "level": 1})
    await ctx.send(f"⭐ {member.mention} səviyyəsi: **{data['level']}** (XP: {data['xp']})")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"İstifadəçi Məlumatı - {member.name}", color=0x3498DB)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Qoşulma tarixi", value=member.joined_at.strftime("%d-%m-%Y"), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0xFF00FF)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get("TOKEN"))
    
