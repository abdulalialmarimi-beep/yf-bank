        data["total_lost"] += (bet - winnings)
        text = f"😢 خسرت **${bet - winnings:,}**"
        color = C_ORANGE
    else:
        data["balance"] -= bet
        data["total_lost"] += bet
        data["losses"] += 1
        text = f"💀 خسرت كل شيء! **-${bet:,}**"
    
    data["games_played"] += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)
    
    embed = emb(f"🎡 عجلة الحظ — {label}", text, color)
    embed.add_field(name="💵 الرهان", value=f"${bet:,}", inline=True)
    embed.add_field(name="📈 المضاعف", value=f"x{mult}", inline=True)
    embed.add_field(name="💰 الأرباح", value=f"${winnings:,}", inline=True)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=False)
    if new_ach:
        embed.add_field(name="🎉 إنجاز جديد!", value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]), inline=False)
    await msg.edit(content=None, embed=embed)

# ─── BLACKJACK ───────────────────────────────────────────────

@bot.tree.command(name="blackjack", description="بلاك جاك 21!")
@app_commands.describe(bet="مبلغ الرهان ($100 - $10,000)")
async def blackjack_cmd(interaction: discord.Interaction, bet: int):
    data = get_user(bot.db, str(interaction.user.id))
    if bet < 100 or bet > 10000:
        await interaction.response.send_message("❌ الرهان: $100 - $10,000!", ephemeral=True); return
    if data["balance"] < bet:
        await interaction.response.send_message("❌ رصيدك لا يكفي!", ephemeral=True); return
    
    suits = ["♠️", "♥️", "♦️", "♣️"]
    cards = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    
    def draw():
        return (random.choice(list(cards.keys())), random.choice(suits))
    
    def hand_value(hand):
        val = sum(cards[c[0]] for c in hand)
        aces = sum(1 for c in hand if c[0] == "A")
        while val > 21 and aces > 0:
            val -= 10
            aces -= 1
        return val
    
    player = [draw(), draw()]
    dealer = [draw(), draw()]
    
    embed = emb("🃏 بلاك جاك", f"رهانك: **${bet:,}**", C_GREEN)
    embed.add_field(name="يدك", value=f"{' '.join([c[0]+c[1] for c in player])} = **{hand_value(player)}**", inline=False)
    embed.add_field(name="الديلر", value=f"{dealer[0][0]}{dealer[0][1]} ❓", inline=False)
    
    view = discord.ui.View()
    hit_btn = discord.ui.Button(label="🃏 Hit", style=discord.ButtonStyle.primary)
    stand_btn = discord.ui.Button(label="🛑 Stand", style=discord.ButtonStyle.danger)
    
    async def hit_cb(i: discord.Interaction):
        if i.user.id != interaction.user.id:
            await i.response.send_message("❌ مو دورك!", ephemeral=True); return
        player.append(draw())
        pv = hand_value(player)
        if pv > 21:
            data["balance"] -= bet; data["total_lost"] += bet; data["losses"] += 1
            data["games_played"] += 1; data["total_gambled"] += bet
            save_db(bot.db)
            e = emb("💥 انفجرت!", f"يدك: {' '.join([c[0]+c[1] for c in player])} = **{pv}**\nخسرت **${bet:,}**", C_RED)
            e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
            await i.response.edit_message(embed=e, view=None)
        else:
            e = emb("🃏 بلاك جاك", f"رهانك: **${bet:,}**", C_GREEN)
            e.add_field(name="يدك", value=f"{' '.join([c[0]+c[1] for c in player])} = **{pv}**", inline=False)
            e.add_field(name="الديلر", value=f"{dealer[0][0]}{dealer[0][1]} ❓", inline=False)
            await i.response.edit_message(embed=e)
    
    async def stand_cb(i: discord.Interaction):
        if i.user.id != interaction.user.id:
            await i.response.send_message("❌ مو دورك!", ephemeral=True); return
        while hand_value(dealer) < 17:
            dealer.append(draw())
        dv = hand_value(dealer); pv = hand_value(player)
        
        if dv > 21 or pv > dv:
            win = bet * 2
            data["balance"] += bet; data["total_earned"] += bet; data["wins"] += 1
            text = f"🎉 فزت بـ **${win:,}**!"; color = C_GREEN
        elif pv < dv:
            data["balance"] -= bet; data["total_lost"] += bet; data["losses"] += 1
            text = f"😢 الديلر فاز! خسرت **${bet:,}**"; color = C_RED
        else:
            text = f"🤝 تعادل! استردت **${bet:,}**"; color = C_BLUE
        
        data["games_played"] += 1; data["total_gambled"] += bet
        new_ach = check_achievements(data)
        save_db(bot.db)
        
        e = emb(f"🃏 النتيجة — {text}", "", color)
        e.add_field(name="يدك", value=f"{' '.join([c[0]+c[1] for c in player])} = **{pv}**", inline=False)
        e.add_field(name="الديلر", value=f"{' '.join([c[0]+c[1] for c in dealer])} = **{dv}**", inline=False)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        if new_ach:
            e.add_field(name="🎉 إنجاز جديد!", value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]))
        await i.response.edit_message(embed=e, view=None)
    
    hit_btn.callback = hit_cb
    stand_btn.callback = stand_cb
    view.add_item(hit_btn); view.add_item(stand_btn)
    await interaction.response.send_message(embed=embed, view=view)

# ─── CRASH ─────────────────────────────────────────────────────

@bot.tree.command(name="crash", description="تكس — اطلع قبل ما ينهار!")
@app_commands.describe(bet="مبلغ الرهان ($50 - $5,000)")
async def crash_cmd(interaction: discord.Interaction, bet: int):
    data = get_user(bot.db, str(interaction.user.id))
    if bet < 50 or bet > 5000:
        await interaction.response.send_message("❌ الرهان: $50 - $5,000!", ephemeral=True); return
    if data["balance"] < bet:
        await interaction.response.send_message("❌ رصيدك لا يكفي!", ephemeral=True); return
    
    multiplier = 1.0
    crash_point = random.uniform(1.1, 5.0)
    
    embed = emb("📈 تكس", f"رهان: **${bet:,}**\nالمضاعف: **x{multiplier:.2f}**\nاضغط **Cash Out**!", C_ORANGE)
    view = discord.ui.View()
    cash_btn = discord.ui.Button(label="💰 Cash Out", style=discord.ButtonStyle.success)
    
    async def cash_cb(i: discord.Interaction):
        if i.user.id != interaction.user.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
        winnings = int(bet * multiplier)
        data["balance"] += winnings - bet; data["total_earned"] += winnings - bet; data["wins"] += 1
        data["games_played"] += 1; data["total_gambled"] += bet
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb(f"🎉 Cash Out! x{multiplier:.2f}", f"ربحت **${winnings:,}**", C_GREEN)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        if new_ach:
            e.add_field(name="🎉 إنجاز جديد!", value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]))
        await i.response.edit_message(embed=e, view=None)
    
    cash_btn.callback = cash_cb
    view.add_item(cash_btn)
    msg = await interaction.response.send_message(embed=embed, view=view)
    
    for _ in range(50):
        await asyncio.sleep(0.5)
        multiplier += random.uniform(0.05, 0.3)
        if multiplier >= crash_point:
            data["balance"] -= bet; data["total_lost"] += bet; data["losses"] += 1
            data["games_played"] += 1; data["total_gambled"] += bet
            save_db(bot.db)
            e = emb(f"💥 انهار عند x{crash_point:.2f}!", f"خسرت **${bet:,}**", C_RED)
            e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
            await msg.edit(embed=e, view=None)
            return
        embed = emb("📈 تكس", f"رهان: **${bet:,}**\nالمضاعف: **x{multiplier:.2f}**\nاضغط **Cash Out**!", C_ORANGE)
        await msg.edit(embed=embed)
    
    # Auto cash out at max
    winnings = int(bet * multiplier)
    data["balance"] += winnings - bet; data["total_earned"] += winnings - bet; data["wins"] += 1
    data["games_played"] += 1; data["total_gambled"] += bet
    save_db(bot.db)
    e = emb(f"🎉 وصلت للحد الأقصى! x{multiplier:.2f}", f"ربحت **${winnings:,}**", C_GREEN)
    e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    await msg.edit(embed=e, view=None)

# ─── ROB ─────────────────────────────────────────────────────────

@bot.tree.command(name="rob", description="سرق مستخدم!")
@app_commands.describe(user="الضحية")
async def rob_cmd(interaction: discord.Interaction, user: discord.User):
    if user.id == interaction.user.id:
        await interaction.response.send_message("❌ ما تقدر تسرق نفسك!", ephemeral=True); return
    data = get_user(bot.db, str(interaction.user.id))
    victim = get_user(bot.db, str(user.id))
    
    if victim["balance"] < 500:
        await interaction.response.send_message("❌ الضحية فقير! ما عنده فلوس!", ephemeral=True); return
    if data.get("protection") and datetime.fromisoformat(data["protection_expires"]) > datetime.now():
        await interaction.response.send_message("❌ عندك حماية! ما تقدر تسرق!", ephemeral=True); return
    
    chance = 0.45
    if victim["balance"] > data["balance"] * 2:
        chance -= 0.15
    if data["properties"].get("cars", 0) > 0:
        chance += 0.05
    
    data["rob_attempts"] += 1
    if random.random() < chance:
        stolen = random.randint(int(victim["balance"] * 0.05), int(victim["balance"] * 0.25))
        victim["balance"] -= stolen; data["balance"] += stolen
        data["total_earned"] += stolen; data["rob_success"] += 1
        text = f"🎉 سرقت **${stolen:,}** من {user.mention}!"
        color = C_GREEN
    else:
        fine = random.randint(500, 2000)
        data["balance"] -= fine; data["total_lost"] += fine; data["rob_failed"] += 1
        text = f"❌ تم القبض عليك! دفعت غرامة **${fine:,}**"
        color = C_RED
    
    new_ach = check_achievements(data)
    save_db(bot.db)
    embed = emb("🦹 سرقة", text, color)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    if new_ach:
        embed.add_field(name="🎉 إنجاز جديد!", value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]))
    await interaction.response.send_message(embed=embed)

# ─── MARRY ───────────────────────────────────────────────────────

@bot.tree.command(name="marry", description="تزوج مستخدم!")
@app_commands.describe(user="شريك حياتك")
async def marry_cmd(interaction: discord.Interaction, user: discord.User):
    if user.id == interaction.user.id:
        await interaction.response.send_message("❌ ما تقدر تتزوج نفسك!", ephemeral=True); return
    if user.bot:
        await interaction.response.send_message("❌ ما تقدر تتزوج بوت!", ephemeral=True); return
    
    data = get_user(bot.db, str(interaction.user.id))
    partner = get_user(bot.db, str(user.id))
    
    if data["married_to"] is not None:
        await interaction.response.send_message("❌ أنت متزوج! طلق الأول بالأمر `/divorce`", ephemeral=True); return
    if partner["married_to"] is not None:
        await interaction.response.send_message("❌ الشخص متزوج!", ephemeral=True); return
    
    embed = emb("💍 عرض زواج!", f"{interaction.user.mention} يعرض الزواج على {user.mention}!\nالمهر: **$5,000**", C_PINK)
    view = discord.ui.View()
    yes_btn = discord.ui.Button(label="💍 نعم!", style=discord.ButtonStyle.success)
    no_btn = discord.ui.Button(label="❌ لا", style=discord.ButtonStyle.danger)
    
    async def yes_cb(i: discord.Interaction):
        if i.user.id != user.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        if data["balance"] < 5000:
            await i.response.send_message("❌ فلوسك ما تكفي للمهر!", ephemeral=True); return
        
        data["balance"] -= 5000; partner["balance"] += 5000
        data["married_to"] = str(user.id); partner["married_to"] = str(interaction.user.id)
        data["married_since"] = datetime.now().isoformat(); partner["married_since"] = data["married_since"]
        data["dowry"] = 5000; partner["dowry"] = 5000
        new_ach = check_achievements(data)
        save_db(bot.db)
        
        e = emb("💍 زواج ناجح!", f"{interaction.user.mention} ❤️ {user.mention}\nمبروك! 🎉", C_PINK)
        if new_ach:
            e.add_field(name="🎉 إنجاز جديد!", value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]))
        await i.response.edit_message(embed=e, view=None)
    
    async def no_cb(i: discord.Interaction):
        if i.user.id != user.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        await i.response.edit_message(embed=emb("💔 رفض!", f"{user.mention} رفض عرض {interaction.user.mention}!", C_RED), view=None)
    
    yes_btn.callback = yes_cb; no_btn.callback = no_cb
    view.add_item(yes_btn); view.add_item(no_btn)
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="divorce", description="طلق شريكك!")
async def divorce_cmd(interaction: discord.Interaction):
    data = get_user(bot.db, str(interaction.user.id))
    if data["married_to"] is None:
        await interaction.response.send_message("❌ أنت مو متزوج!", ephemeral=True); return
    
    partner_id = data["married_to"]
    partner = get_user(bot.db, partner_id)
    
    if data.get("last_divorce"):
        last = datetime.fromisoformat(data["last_divorce"])
        if datetime.now() - last < timedelta(hours=24):
            await interaction.response.send_message("❌ لازم تنتظر 24 ساعة بعد آخر طلاق!", ephemeral=True); return
    
    embed = emb("💔 طلاق", f"متأكد تبي تطلق؟\nراح تخسر نصف مهرك (${data['dowry']//2:,})", C_RED)
    view = discord.ui.View()
    yes_btn = discord.ui.Button(label="💔 نعم، طلق", style=discord.ButtonStyle.danger)
    
    async def yes_cb(i: discord.Interaction):
        if i.user.id != interaction.user.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        
        loss = data["dowry"] // 2
        data["balance"] -= loss; partner["balance"] += loss
        data["divorce_count"] += 1; data["last_divorce"] = datetime.now().isoformat()
        data["married_to"] = None; partner["married_to"] = None
        data["married_since"] = None; partner["married_since"] = None
        save_db(bot.db)
        
        e = emb("💔 تم الطلاق!", f"{interaction.user.mention} طلق {partner_id}\nخسر **${loss:,}**", C_RED)
        await i.response.edit_message(embed=e, view=None)
    
    yes_btn.callback = yes_cb
    view.add_item(yes_btn)
    await interaction.response.send_message(embed=embed, view=view)

# ─── PROPERTIES ──────────────────────────────────────────────────

@bot.tree.command(name="properties", description="اشترِ ممتلكات!")
async def properties_cmd(interaction: discord.Interaction):
    data = get_user(bot.db, str(interaction.user.id))
    embed = emb("🏢 ممتلكات — عائلة يونان", "استثمر وأربح دخل سلبي!", C_GOLD)
    for key, prop in PROPERTIES.items():
        owned = data["properties"].get(key, 0)
        embed.add_field(name=f"{prop['icon']} {prop['name']} (تمتلك: {owned})", 
                       value=f"السعر: **${prop['price']:,}**\nالدخل: **${prop['income']:,}/يوم**\n{prop['desc']}", inline=True)
    
    view = discord.ui.View()
    for key, prop in PROPERTIES.items():
        btn = discord.ui.Button(label=f"شراء {prop['name']}", emoji=prop['icon'], style=discord.ButtonStyle.primary)
        async def make_cb(k, p):
            async def cb(i: discord.Interaction):
                if i.user.id != interaction.user.id:
                    await i.response.send_message("❌ مو لك!", ephemeral=True); return
                d = get_user(bot.db, str(i.user.id))
                if d["balance"] < p["price"]:
                    await i.response.send_message("❌ فلوسك ما تكفي!", ephemeral=True); return
                d["balance"] -= p["price"]
                d["properties"][k] = d["properties"].get(k, 0) + 1
                save_db(bot.db)
                await i.response.edit_message(embed=emb(f"✅ اشتريت {p['name']}!", f"رصيدك: ${d['balance']:,}", C_GREEN))
            return cb
        btn.callback = make_cb(key, prop)
        view.add_item(btn)
    await interaction.response.send_message(embed=embed, view=view)

# ─── TRANSFER ────────────────────────────────────────────────────

@bot.tree.command(name="transfer", description="حول فلوس لمستخدم")
@app_commands.describe(user="المستلم", amount="المبلغ")
async def transfer_cmd(interaction: discord.Interaction, user: discord.User, amount: int):
    if user.id == interaction.user.id:
        await interaction.response.send_message("❌ ما تقدر تحول لنفسك!", ephemeral=True); return
    if amount < 100:
        await interaction.response.send_message("❌ الحد الأدنى $100!", ephemeral=True); return
    
    data = get_user(bot.db, str(interaction.user.id))
    target = get_user(bot.db, str(user.id))
    
    if data["balance"] < amount:
        await interaction.response.send_message("❌ رصيدك لا يكفي!", ephemeral=True); return
    
    data["balance"] -= amount; target["balance"] += amount
    data["gifts_sent"] += 1; target["gifts_received"] += 1
    save_db(bot.db)
    
    embed = emb("💸 تحويل ناجح!", f"{interaction.user.mention} → {user.mention}\nالمبلغ: **${amount:,}**", C_GREEN)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    await interaction.response.send_message(embed=embed)

# ─── HELP ────────────────────────────────────────────────────────

@bot.tree.command(name="help", description="قائمة الأوامر")
async def help_cmd(interaction: discord.Interaction):
    embed = emb("📖 دليل YF BANK — عائلة يونان", "أقوى بوت اقتصادي في ديسكورد!", C_GOLD)
    cmds = [
        ("💳 /balance", "عرض رصيدك وممتلكاتك"),
        ("🎁 /daily", "المكافأة اليومية"),
        ("🏆 /top", "أغنى المستخدمين"),
        ("📊 /market", "سوق الموارد الحي"),
        ("🎮 /games", "قائمة الألعاب"),
        ("🎰 /slots", "آلة الحظ"),
        ("🎡 /wheel", "عجلة الحظ"),
        ("🃏 /blackjack", "بلاك جاك 21"),
        ("📈 /crash", "تكس — اطلع قبل الانهيار"),
        ("🦹 /rob", "سرق مستخدم"),
        ("💍 /marry", "تزوج مستخدم"),
        ("💔 /divorce", "طلق شريكك"),
        ("🏢 /properties", "اشترِ ممتلكات"),
        ("💸 /transfer", "حول فلوس"),
    ]
    for name, desc in cmds:
        embed.add_field(name=name, value=desc, inline=False)
    embed.add_field(name="💡 نصيحة", value="استخدم `/daily` كل يوم وبني سلسلة للمكافآت الإضافية!", inline=False)
    await interaction.response.send_message(embed=embed)

# ─── EVENTS ───────────────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"✅ YF BANK Online! {bot.user.name} ({bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Synced {len(synced)} commands")
    except Exception as e:
        print(f"❌ Sync error: {e}")

# ─── RUN ─────────────────────────────────────────────────────────

bot.run(BOT_TOKEN)
                    
