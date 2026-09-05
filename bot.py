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

bot = commands.Bot(command_prefix='r?', intents=intents)

SAHIB_ID = 64101498631250250
TOXUNULMAZ_BOTLAR = [651095740390834176, 689766089567109158] # Security və Erensi
user_xp = {}
spam_takip = {}
uyari_sayi = {}
son_gosulmalar = []
auto_role_name = "Üzv"

@bot.event
async def on_ready():
    print(f'YENİLMEZ Bot Aktivləşdi! ({bot.user.name})')
    await bot.change_presence(activity=discord.Game(name="r?bot | Profesyonel Koruma"))

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if user.id == SAHIB_ID:
        try:
            await reaction.message.add_reaction(son_gosulmalar)
        except:
            pass

@bot.event
async def on_member_join(member):
    global son_gosulmalar
    sindi = time.time()
    son_gosulmalar.append(sindi)
    son_gosulmalar = [t for t in son_gosulmalar if sindi - t < 30]

    if len(son_gosulmalar) >= 5:
        try:
            await member.guild.edit(verification_level=discord.VerificationLevel.high)
            print("Kütləvi bot hücumu (Raid) aşkarlandı, server təhlükəsizlik rejiminə keçirildi.")
        except:
            pass

    channel = member.guild.system_channel
    if channel:
        try:
            await channel.send(f'Salam, {member.mention}! Xoş gəldin, aramıza qatıldığın üçün şadıq.')
        except:
            pass

    try:
        role = discord.utils.get(member.guild.roles, name=auto_role_name)
        if role:
            await member.add_roles(role)
    except:
        pass

# --- WEBHOOK QORUMASI ---
@bot.event
async def on_webhooks_update(channel):
    try:
        webhooks = await channel.webhooks()
        for wh in webhooks:
            await wh.delete()
    except Exception as e:
        print(f"Webhook silinərkən xəta: {e}")
# -------------------------

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # İstisna olunan botlara (Security və Erensi) toxunmuruq
    if message.author.id in TOXUNULMAZ_BOTLAR:
        await bot.process_commands(message)
        return

    if message.author.bot or "discord.gg/" in message.content.lower() or "discord.com/invite/" in message.content.lower() or "http" in message.content.lower():
        try:
            await message.delete()
        except:
            pass
        return

    if message.author.id == SAHIB_ID or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    author_id = message.author.id
    sindi = time.time()
    icerik = message.content
    icerik_lower = icerik.lower()

    qeribo_simvol_sayi = len(re.findall(r'[^a-zA-Z0-9\s]', icerik))
    if qeribo_simvol_sayi > 30:
        try:
            await message.delete()
            return
        except:
            pass

    if author_id not in spam_takip:
        spam_takip[author_id] = []
    
    spam_takip[author_id] = [t for t in spam_takip[author_id] if sindi - t < 5]
    spam_takip[author_id].append(sindi)

    if len(spam_takip[author_id]) >= 5:
        try:
            await message.delete()
            if author_id not in uyari_sayi:
                uyari_sayi[author_id] = 0
            uyari_sayi[author_id] += 1

            if uyari_sayi[author_id] == 1:
                await message.channel.send(f"⚠️ {message.author.mention}, zəhmət olmasa spam etmə!")
            elif uyari_sayi[author_id] >= 2:
                await message.channel.send(f"🚨 {message.author.mention}, təkrar spam etdiyin üçün təmizləndi!")
        except:
            pass
        return

    if icerik_lower in ["salam", "salamlar", "sa", "aleykümsalam", "hi"]:
        try:
            await message.channel.send(f"👋 Salam, {message.author.mention}! Xoş gəldin.")
        except:
            pass

    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}

    user_xp[author_id]["xp"] += 15
    gerekli_xp = user_xp[author_id]["level"] * 300 + 200

    if user_xp[author_id]["xp"] >= gerekli_xp:
        user_xp[author_id]["xp"] -= gerekli_xp
        user_xp[author_id]["level"] += 1
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Səviyyə atladın: **{user_xp[author_id]['level']}** oldu! 🚀")
        except:
            pass

    await bot.process_commands(message)

@bot.command(name="bot")
async def bot_panel(ctx):
    embed = discord.Embed(
        title="🛡️ YENİLMEZ - TƏHLÜKƏSİZLİK & MODERASİYA",
        description="Server təhlükəsizliyi üçün əsas əmrlər:",
        color=0xFF0000
    )
    embed.add_field(name="r?ban / r?unban", value="İstifadəçini ban edir / açır.", inline=True)
    embed.add_field(name="r?kick", value="İstifadəçini serverdən qovur.", inline=True)
    embed.add_field(name="r?mute / r?unmute", value="Zaman aşımı verir / qaldırır.", inline=True)
    embed.add_field(name="r?warn", value="İstifadəçini xəbərdar edir.", inline=True)
    embed.add_field(name="r?clear", value="Mesajları kütləvi təmizləyir.", inline=True)
    embed.add_field(name="r?lock / r?unlock", value="Bütün serveri kilidləyir/açır.", inline=True)

    embed2 = discord.Embed(
        title="📁 YENİLMEZ - KANAL VƏ SIFIRLAMA İDARƏSİ",
        description="Kanalların idarə edilməsi, nuke və təmizlənməsi:",
        color=0x00FF90
    )
    embed2.add_field(name="r?createchannel / r?createvoice", value="Kanal yaradır.", inline=True)
    embed2.add_field(name="r?deletechannel", value="Cari kanalı silir.", inline=True)
    embed2.add_field(name="r?hide / r?reveal", value="Kanalı gizlədir/göstərir.", inline=True)
    embed2.add_field(name="r?slowmode", value="Kanalda yavaş rejimi tənzimləyir.", inline=True)
    embed2.add_field(name="r?nuke", value="Kanalı sıfırdan yaradır.", inline=True)
    embed2.add_field(name="r?rename", value="Kanalın adını dəyişdirir.", inline=True)

    embed3 = discord.Embed(
        title="👑 YENİLMEZ - ROL VƏ İSTİFADƏÇİ İDARƏSİ",
        description="Rolların verilməsi və istifadəçi məlumatları:",
        color=0x0099FF
    )
    embed3.add_field(name="r?giverole / r?takerole", value="Rol verir və ya alır.", inline=True)
    embed3.add_field(name="r?createrole / r?deleterole", value="Rol yaradır və ya silir.", inline=True)
    embed3.add_field(name="r?userinfo", value="İstifadəçinin haqqında məlumat.", inline=True)
    embed3.add_field(name="r?avatar", value="İstifadəçinin profil şəklini göstərir.", inline=True)
    embed3.add_field(name="r?botinfo", value="Botun sistem məlumatlarını göstərir.", inline=True)

    embed4 = discord.Embed(
        title="🌟 YENİLMEZ - XÜSUSİ ALƏTLƏR, ÇƏKİLİŞ & XP",
        description="Banner, səsvermə, çəkiliş və səviyyə sistemləri:",
        color=0xFFD700
    )
    embed4.add_field(name="r?embed <başlıq> | <mətini>", value="Özəl embed mesajı göndərir.", inline=False)
    embed4.add_field(name="r?suggestion <təklif>", value="Təklif paneli yaradır.", inline=False)
    embed4.add_field(name="r?serverlock", value="Serveri yeni qoşulmalara qapadır.", inline=False)
    embed4.add_field(name="r?serverinfo", value="Serverin bütün detallarını göstərir.", inline=False)
    embed4.add_field(name="r?ping", value="Botun gecikmə sürətini ölçür.", inline=False)
    embed4.add_field(name="r?level", value="XP və level göstərir.", inline=False)
    embed4.add_field(name="r?announcement", value="Serverdə rəsmi elan atır.", inline=False)
    embed4.add_field(name="r?serverbanner", value="İstifadəçi/server banneri.", inline=False)
    embed4.add_field(name="r?poll <sual>", value="Avtomatik reaksiyalı səsvermə.", inline=False)
    embed4.add_field(name="r?say <mesaj>", value="Yazdığın mətni botun dilindən yazar.", inline=False)
    embed4.add_field(name="r?cekilis <gün> <hədiyyə>", value="Çəkiliş başladar.", inline=False)
    embed4.set_footer(text="YENİLMEZ Bot © 2026 | Bütün funksiyalar tam təhlükəsizdir.")

    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} serverdən ban edildi!")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name.lower() == member_name.lower():
            await ctx.guild.unban(user)
            await ctx.send(f"✅ {user.mention} ban-dan çıxarıldı.")
            return
    await ctx.send("❌ Bu adda ban edilmiş istifadəçi tapılmadı.")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} serverdən qovuldu!")

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, minutes: int = 5):
    await member.timeout(discord.utils.utcnow() + discord.timedelta(minutes=minutes))
    await ctx.send(f"🔇 {member.mention} {minutes} dəqiqəlik mute-ləndi!")

@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} mute-dən çıxarıldı.")

@bot.command(name="warn")
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    await ctx.send(f"⚠️ {member.mention} xəbərdar edildi! Səbəb: {reason}")

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 {len(deleted)} dənə mesaj təmizləndi!", delete_after=3)

@bot.command(name="createchannel")
@commands.has_permissions(manage_channels=True)
async def createchannel(ctx, *, isim):
    await ctx.guild.create_text_channel(isim)
    await ctx.send(f"✅ `{isim}` adlı mətn kanalı yaradıldı.")

@bot.command(name="createvoice")
@commands.has_permissions(manage_channels=True)
async def createvoice(ctx, *, isim):
    await ctx.guild.create_voice_channel(isim)
    await ctx.send(f"🔊 `{isim}` adlı səs kanalı yaradıldı.")

@bot.command(name="deletechannel")
@commands.has_permissions(manage_channels=True)
async def deletechannel(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.delete()

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal yazışmaya açıldı.")

@bot.command(name="hide")
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🙈 Bu kanal hamıdan gizlədildi.")

@bot.command(name="reveal")
@commands.has_permissions(manage_channels=True)
async def reveal(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🐵 Bu kanal yenidən hər kəsə göstərildi.")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Kanalın yavaş modu `{seconds}` saniyə edildi.")

@bot.command(name="nuke")
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    kanal = ctx.channel
    konum = kanal.position
    yeni_kanal = await kanal.clone(reason="Nuke əmri ilə sıfırlandı")
    await kanal.delete()
    await yeni_kanal.edit(position=konum)
    await yeni_kanal.send("💥 Kanal uğurla nuke olundu, hər şey sıfırdan başladı!")

@bot.command(name="rename")
@commands.has_permissions(manage_channels=True)
async def rename(ctx, *, yeni_ad):
    await ctx.channel.edit(name=yeni_ad)
    await ctx.send(f"✏️ Kanalın adı dəyişdirildi: `{yeni_ad}`")

@bot.command(name="giverole")
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} istifadəçisinə `{role.name}` rolu verildi.")

@bot.command(name="takerole")
@commands.has_permissions(manage_roles=True)
async def takerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ {member.mention} istifadəçisindən `{role.name}` rolu alındı.")

@bot.command(name="createrole")
@commands.has_permissions(manage_roles=True)
async def createrole(ctx, *, rol_adi):
    await ctx.guild.create_role(name=rol_adi)
    await ctx.send(f"✅ `{rol_adi}` adlı yeni rol yaradıldı.")

@bot.command(name="deleterole")
@commands.has_permissions(manage_roles=True)
async def deleterole(ctx, role: discord.Role):
    await role.delete()
    await ctx.send(f"🗑️ `{role.name}` rolu silindi.")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 İstifadəçi Məlumatı: {member.name}", color=0x00FFCC)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Qoşulma Tarixi", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name} - Avatar", color=0xFF00FF)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="botinfo")
async def botinfo(ctx):
    embed = discord.Embed(title="🤖 YENİLMEZ Bot Sistem Məlumatı", color=0x3498DB)
    embed.add_field(name="Yaradıcı / Sahib", value="<@64101498631250250>", inline=True)
    embed.add_field(name="Server Sayı", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Status", value="Aktiv & Qorumalı 🛡️", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="lockall")
@commands.has_permissions(administrator=True)
async def lockall(ctx):
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        except:
            pass
    await ctx.send("🔒 Bütün serverdəki mətn kanalları yazışmaya bağlandı.")

@bot.command(name="unlockall")
@commands.has_permissions(administrator=True)
async def unlockall(ctx):
    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        except:
            pass
    await ctx.send("🔓 Bütün serverdəki mətn kanalları yazışmaya açıldı.")

@bot.command(name="serverlock")
@commands.has_permissions(administrator=True)
async def serverlock(ctx):
    await ctx.guild.edit(verification_level=discord.VerificationLevel.high)
    await ctx.send("🛡️ Server təhlükəsizlik rejiminə keçirildi.")

@bot.command(name="embed")
@commands.has_permissions(manage_messages=True)
async def custom_embed(ctx, *, text):
    await ctx.message.delete()
    if "|" in text:
        title, desc = text.split("|", 1)
        embed = discord.Embed(title=title.strip(), description=desc.strip(), color=0x00FFCC)
    else:
        embed = discord.Embed(description=text, color=0x00FFCC)
    await ctx.send(embed=embed)

@bot.command(name="suggestion")
async def suggestion(ctx, *, teklif):
    await ctx.message.delete()
    embed = discord.Embed(title="💡 YENİ TƏKLİF", description=teklif, color=0xF1C40F)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="serverbanner")
async def serverbanner(ctx):
    guild = ctx.guild
    if guild.banner:
        embed = discord.Embed(title=f"🖼️ {guild.name} - Server Banneri", color=0x9B59B6)
        embed.set_image(url=guild.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Bu serverin xüsusi banner şəkli yoxdur.")

@bot.command(name="poll")
@commands.has_permissions(manage_messages=True)
async def poll(ctx, *, soru):
    await ctx.message.delete()
    embed = discord.Embed(title="📊 ANKET / SƏSVERMƏ", description=soru, color=0x3498DB)
    embed.set_footer(text=f"Anketi yaradan: {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="say")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, mesaj):
    await ctx.message.delete()
    await ctx.send(mesaj)

@bot.command(name="cekilis", aliases=["çəkiliş"])
@commands.has_permissions(manage_guild=True)
async def cekilis(ctx, zaman_gun: int, *, odul):
    await ctx.message.delete()
    saniye = zaman_gun * 86400

    embed = discord.Embed(
        title="🎉 YENİ ÇƏKİLİŞ! 🎉",
        description=f"Hədiyyə: **{odul}**\n\nQatılmaq üçün aşağıdakı reaksiyaya toxun! 🎉\nBitmə müddəti: **{zaman_gun} gün**",
        color=0x91E53
    )
    embed.set_footer(text=f"Çəkilişi təşkil edən: {ctx.author.name}")
    
    mesaj = await ctx.send(embed=embed)
    await mesaj.add_reaction("🎉")

    await asyncio.sleep(saniye)

    try:
        yeni_mesaj = await ctx.channel.fetch_message(mesaj.id)
        reaksiya = discord.utils.get(yeni_mesaj.reactions, emoji="🎉")

        if reaksiya:
            istikracilar = [user async for user in reaksiya.users() if not user.bot]

            if istikracilar:
                qalib = random.choice(istikracilar)
                await ctx.send(f"🎉 Təbriklər {qalib.mention}! **{odul}** çəkilişinin qalibi oldun! 🏆")
            else:
                await ctx.send("❌ Çəkilişə heç kim qoşulmadığı üçün qalib seçilmədi.")
        else:
            await ctx.send("❌ Çəkiliş zamanı xəta baş verdi.")
    except Exception as e:
        await ctx.send(f"❌ Çəkiliş nəticələnərkən xəta yarandı: {e}")

@bot.command(name="serverinfo")
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} - Server Statistikası", color=0x3498DB)
    embed.add_field(name="Üzv Sayı", value=guild.member_count, inline=True)
    embed.add_field(name="Kanal Sayı", value=len(guild.channels), inline=True)
    embed.add_field(name="Rol Sayı", value=len(guild.roles), inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Gecikmə: {round(bot.latency * 1000)}ms")

@bot.command(name="level")
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = user_xp.get(member.id, {"xp": 0, "level": 1})
    await ctx.send(f"⭐ {member.mention} səviyyəsi: **{data['level']}** (XP: {data['xp']})")

@bot.command(name="announcement")
@commands.has_permissions(administrator=True)
async def announcement(ctx, *, mesaj):
    await ctx.message.delete()
    e
