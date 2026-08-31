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

# 👑 SƏNİN SƏHİH DİSCORD İD-N 👑
SAHIB_ID = 641014966312501259

# 🎯 TICKET ÜÇÜN XÜSUSİ KANALIN ID-Sİ
XUSUSI_KANAL_ID = 1544056308787974294 

ticket_span_kontrol = {}
user_xp = {}
spam_takip = {}

@bot.event
async def on_ready():
    print(f"🔥 Bot uğurla işə düşdü: {bot.user.name} 🔥")
    await bot.change_presence(activity=discord.Game(name="r?bot | YENİLMEZ v6000 👑"))
    stats_update.start()
    voice_xp_loop.start()

# ==============================================================================
# 👋 XOŞ GƏLDİN VƏ VİDALAŞMA
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
# 📊 CANLI STATİSTİKA VƏ XP LOOPLARI
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
            print(f"Statistika xətası: {e}")

@tasks.loop(minutes=1)
async def voice_xp_loop():
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if len(vc.members) > 1:
                for member in vc.members:
                    if member.bot: continue
                    if member.id not in user_xp:
                        user_xp[member.id] = {"xp": 0, "level": 1}
                    user_xp[member.id]["xp"] += 15
                    if user_xp[member.id]["xp"] >= user_xp[member.id]["level"] * 100:
                        user_xp[member.id]["level"] += 1
                        user_xp[member.id]["xp"] = 0

# ==============================================================================
# 🛡️ MESAJ, GÜLÜŞ (EMOJI) VƏ SPAM NƏZARƏTİ
# ==============================================================================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Gülüş sözlərinə emoji atma sistemi (Yalnız SƏNƏ aid)
    if message.author.id == SAHIB_ID:
        gulus_sozleri = ["xd", "asds", "guly", "kara", "hf", "latifə", "😂", "🤣", "💀", "😹", "😆"]
        if any(g in message.content.lower() for g in gulus_sozleri):
            try:
                for emj in random.sample(["😂", "🤣", "💀", "😹", "😆", "🫠"], 3):
                    await message.add_reaction(emj)
            except:
                pass

    author_id = message.author.id
    sindi = time.time()

    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}
    user_xp[author_id]["xp"] += 10
    if user_xp[author_id]["xp"] >= user_xp[author_id]["level"] * 100:
        user_xp[author_id]["level"] += 1
        user_xp[author_id]["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}! Səviyyə yüksəldin: **Səviyyə {user_xp[author_id]['level']}** 🚀")
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
                await message.author.timeout(muteli_vaxt, reason="Spam / random")
                await message.channel.send(f"⚠️ {message.author.mention}, həddindən artıq spam yazdığın üçün 30 san mute aldın!", delete_after=5)
                return
            except:
                pass

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id != SAHIB_ID:
        return
    try:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.add_reaction(payload.emoji)
    except:
        pass

# ==============================================================================
# 🎫 TICKET SİSTEMİ (DÜYMƏLİ)
# ==============================================================================

class TicketKapatView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Ticketi Bağla", style=discord.ButtonStyle.danger, custom_id="ticket_kapat_btn")
    async def ticket_kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Bu ticket kanalı 5 saniyə ərzində silinəcək...", ephemeral=False)
        await asyncio.sleep(5)
        try:
            await interaction.channel.delete()
        except:
            pass

class TicketBaslatView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Ticket Aç", style=discord.ButtonStyle.success, custom_id="ticket_ac_btn")
    async def ticket_ac(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        author = interaction.user

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
        }

        channel = await guild.create_text_channel(f"ticket-{author.name.lower()}", overwrites=overwrites)
        embed = discord.Embed(
            title="📩 Dəstək Mərkəzi", 
            description=f"Salam {author.mention}! Səlahiyyətlilər qısa zamanda sizinlə maraqlanacaq.\n\nTicketi bağlamaq üçün aşağıdakı düyməyə basın.", 
            color=0x00ff00
        )
        await channel.send(embed=embed, view=TicketKapatView())
        await interaction.response.send_message(f"✅ Ticket kanalın yaradıldı: {channel.mention}", ephemeral=True)

# ==============================================================================
# 👑 SAHİB ƏMRLƏRİ (Yalnız Sənin İşlədə Biləcəklərin)
# ==============================================================================

@bot.command(name="bot")
async def bot_komanda(ctx):
    if ctx.author.id != SAHIB_ID: return
    embed = discord.Embed(
        title="👑 YENİLMEZ v6000 - Əmr və Məlumat Mərkəzi",
        description="Botun bütün gücləndirilmiş imkanları:",
        color=0xffa200
    )
    embed.add_field(name="👑 Sahib Komutları", value="`r?elan`, `r?anket`, `r?cekilis`, `r?duyuru`, `r?bakim`, `r?ticketpanel`", inline=False)
    embed.add_field(name="🛡️ Kanal İdarəsi", value="`r?gizle`, `r?goster`, `r?sesgizle`, `r?sesgoster`", inline=False)
    embed.add_field(name="📋 Statistika", value="`r?server`, `r?userinfo`, `r?botinfo`, `r?ping`, `r?online`, `r?level`", inline=False)
    embed.add_field(name="🛠️ Moderasiya", value="`r?sil`, `r?mute`, `r?unmute`, `r?ban`, `r?kick`, `r?nuke`", inline=False)
    embed.add_field(name="🎮 Əyləncə", value="`r?duel`, `r?coinflip`, `r?slot`, `r?iq`, `r?balıq`, `r?hava`, `r?hesabla`", inline=False)
    embed.set_footer(text="YENİLMEZ Security Systems")
    await ctx.send(embed=embed)

@bot.command(name="ticketpanel")
async def ticketpanel(ctx):
    if ctx.author.id != SAHIB_ID: return
    if ctx.channel.id != XUSUSI_KANAL_ID:
        await ctx.message.delete()
        await ctx.send(f"❌ Bu komandanı yalnız <#{XUSUSI_KANAL_ID}> kanalında işlədə bilərsən!", delete_after=5)
        return
    
    await ctx.message.delete()
    embed = discord.Embed(
        title="🎫 Dəstək Paneli",
        description="Aşağıdakı **'Ticket Aç'** düyməsinə basaraq dəstək xətti yarada bilərsiniz.",
        color=0x00aaff
    )
    await ctx.send(embed=embed, view=TicketBaslatView())

@bot.command(name="elan")
async def elan(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(embed=discord.Embed(title="📢 ELAN", description=metin, color=0xffaa00))

@bot.command(name="anket")
async def anket(ctx, *, soru: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    msg = await ctx.send(embed=discord.Embed(title="📊 ANKET", description=soru, color=0x00ffcc))
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="cekilis")
async def cekilis(ctx, sure: str, *, odul: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    try:
        birim = sure[-1]
        sayi = int(sure[:-1])
        saniye = sayi * (1 if birim=='s' else 60 if birim=='m' else 3600 if birim=='h' else 86400)
    except:
        await ctx.send("❌ Vaxt formatı səhvdir! (Məs: `2d`, `10m`)", delete_after=5)
        return

    msg = await ctx.send(embed=discord.Embed(title="🎉 ÇƏKİLİŞ", description=f"Ödül: **{odul}**\n🎉 emojisinə bas qatıl!", color=0xff0055))
    await msg.add_reaction("🎉")
    await asyncio.sleep(saniye)

    try:
        yeni_msg = await ctx.channel.fetch_message(msg.id)
        users = [u async for r in yeni_msg.reactions if str(r.emoji) == "🎉" async for u in r.users() if not u.bot]
        if users:
            await ctx.channel.send(f"🏆 Qalib: {random.choice(users).mention}! Ödül: **{odul}** 🎁")
        else:
            await ctx.channel.send(f"❌ {odul} çəkilişinə qoşulan olmadı.")
    except:
        pass

@bot.command(name="duyuru")
async def duyuru(ctx, *, metin: str):
    if ctx.author.id != SAHIB_ID: return
    await ctx.message.delete()
    await ctx.send(f"🔔 **DUYURU:** {metin}")

@bot.command(name="bakim")
async def bakim(ctx, durum: str = "açıq"):
    if ctx.author.id != SAHIB_ID: return
    await ctx.send(f"🛠️ Baxım rejimi: **{durum}**")

@bot.command(name="gizle")
async def gizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🔒 Kanal gizlədildi!")

@bot.command(name="goster")
async def goster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("🔓 Kanal açıldı!")

@bot.command(name="sesgizle")
async def sesgizle(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=False)
    await ctx.send("🔴 Səs kanalı bağlandı!")

@bot.command(name="sesgoster")
async def sesgoster(ctx):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.set_permissions(ctx.guild.default_role, connect=True)
    await ctx.send("🟢 Səs kanalı açıldı!")

@bot.command(name="sil")
async def sil(ctx, amount: int = 5):
    if ctx.author.id != SAHIB_ID: return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 {amount} mesaj silindi!", delete_after=3)

@bot.command(name="mute")
async def mute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted") or await ctx.guild.create_role(name="Muted")
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.mention} səssizləşdirildi!")

@bot.command(name="unmute")
async def unmute(ctx, member: discord.Member):
    if ctx.author.id != SAHIB_ID: return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role: await member.remove_roles(role)
    await ctx.send(f"🔊 {member.mention} səsi açıldı!")

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} banlandı!")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != SAHIB_ID: return
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.name} qovuldu!")

@bot.command(name="nuke")
async def nuke(ctx):
    if ctx.author.id != SAHIB_ID: return
    pos = ctx.channel.position
    yeni = await ctx.channel.clone()
    await ctx.channel.delete()
    await yeni.edit(position=pos)
    await yeni.send("💥 Kanal sıfırlandı!")

# ==============================================================================
# 🎮 HAMININ İŞLƏDƏ BİLƏCƏYİ ÜMUMİ ƏMRLƏR (Oyunlar, Statistika və s.)
# ==============================================================================

@bot.command(name="botinfo")
async def botinfo(ctx):
    await ctx.send("🤖 **Bot Sürümü:** `YENİLMEZ v6000` | Python & Discord.py ⚡")

@bot.command(name="server")
async def server(ctx):
    g = ctx.guild
    await ctx.send(f"🏰 **Server:** {g.name} | **Üzv:** {g.member_count}")

@bot.command(name="userinfo")
async def userinfo(ctx, m: discord.Member = None):
    u = m or ctx.author
    await ctx.send(f"👤 **İstifadəçi:** {u.name} | **ID:** {u.id}")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Gecikmə: **{round(bot.latency * 1000)}ms** ⚡")

@bot.command(name="online")
async def online(ctx):
    c = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
    await ctx.send(f"🟢 **Onlayn Üzv sayı:** {c}")

@bot.command(name="hava")
async def hava(ctx, *, seher: str = "Bakı"):
    await ctx.send(f"🌤️ **{seher}**: **{random.randint(18, 35)}°C** (Günəşli ☀️)")

@bot.command(name="hesabla")
async def hesabla(ctx, *, islem: str):
    try:
        await ctx.send(f"🧮 **Nəticə:** `{eval(islem)}` ✅")
    except:
        await ctx.send("❌ Xəta! Doğru riyazi əməliyyat daxil et ⚠️")

@bot.command(name="level")
async def level(ctx, m: discord.Member = None):
    target = m or ctx.author
    if target.id in user_xp:
        d = user_xp[target.id]
        await ctx.send(f"⭐ **{target.name}** | Səviyyə: **{d['level']}** 🏆 | XP: **{d['xp']}**")
    else:
        await ctx.send(f"⭐ **{target.name}** hələ XP qazanmayıb! (Səviyyə 1)")

@bot.command(name="duel")
async def duel(ctx, member: discord.Member):
    await ctx.send(f"⚔️ Duel qalibi: {random.choice([ctx.author, member]).mention}!")

@bot.command(name="coinflip")
async def coinflip(ctx):
    await ctx.send(f"🎲 Nəticə: **{random.choice(['Yazı 🪙', 'Tura 👑'])}**")

@bot.command(name="slot")
async def slot(ctx):
    e = ["🍎", "🍋", "🍒", "7️⃣", "💎"]
    a, b, c = random.choice(e), random.choice(e), random.choice(e)
    msg = f"🎰 [{a} | {b} | {c}]\n" + ("🎉 UDDUNUZ!" if a == b == c else "❌ Uduzdunuz!")
    await ctx.send(msg)

@bot.command(name="iq")
async def iq(ctx, m: discord.Member = None):
    await ctx.send(f"🧠 **{(m or ctx.author).name}** IQ: **{random.randint(50, 160)}**")

@bot.command(name="balıq")
async def balıq(ctx):
    await ctx.send(f"🎣 Tutdun: **{random.choice(['🐟 Balıq', '🐠 Qızıl Balıq', '🦈 Akula', '👞 Başmaq'])}**")

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ Token tapılmadı!")
        
