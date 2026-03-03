import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio
import random
from datetime import datetime, timezone
import openai
import os
import asyncio
from discord.app_commands import Transformer
from typing import List
from datetime import timedelta
	
    
KISS_GIFS = [
    "https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif",
    "https://media.giphy.com/media/bGm9FuBCGg4SY/giphy.gif",
    "https://media.giphy.com/media/11k3oaUjSlFR4I/giphy.gif",                    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWFrZ3ZxZnptNXRjNzNvaDl2anpjOHN1amUxc2M2cXBwZHpxcGw3NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gTLfgIRwAiWOc/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3oweDJ5dTZ2NmpneWV1OHdtcHR5d2k4bzY3YWZmam96YnhpZ3BmcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/MQVpBqASxSlFu/giphy.gif"
]

HUG_GIFS = [
    "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
    "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3oweDJ5dTZ2NmpneWV1OHdtcHR5d2k4bzY3YWZmam96YnhpZ3BmcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/2A75Y6NodD38I/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3oweDJ5dTZ2NmpneWV1OHdtcHR5d2k4bzY3YWZmam96YnhpZ3BmcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IRUb7GTCaPU8E/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3oweDJ5dTZ2NmpneWV1OHdtcHR5d2k4bzY3YWZmam96YnhpZ3BmcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QFPoctlgZ5s0E/giphy.gif"
]

FUCK_GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWo4ejN1Y3c4bHpueG40cHRibWphdDdlYzc3eml1cGp2ZXh4N2JodCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/TH3Ry9XemzL2/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YXlzaHQwZGhjbmc4cmdrMHVlcDU5amdtNHJuNWFxY3I3eWtwMmJkdSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/12f5R5Ix3S3ZbW/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTd1Mm8yc2NnMWYxOWV3ZTF0MmZ0d2thYTVmdnRjZjU3dG9pemxwaCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/MwtHY03ldRPgc/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTd1Mm8yc2NnMWYxOWV3ZTF0MmZ0d2thYTVmdnRjZjU3dG9pemxwaCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/gKc0n2MdnezJK/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTd1Mm8yc2NnMWYxOWV3ZTF0MmZ0d2thYTVmdnRjZjU3dG9pemxwaCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/svAVUj69hK5a0/giphy.gif",
 "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTd1Mm8yc2NnMWYxOWV3ZTF0MmZ0d2thYTVmdnRjZjU3dG9pemxwaCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IsIyvk7zftw4H2C1Kz/giphy.gif"
]

openai.api_key = os.getenv("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")

timestamp = datetime.now(timezone.utc)

TOKEN = "INSERT YOUR BOT'S TOKEN"

intents = discord.Intents.all()
intents.message_content = True  # Required for most commands
# No special intent needed for DMs, but make sure it's in intents
bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------
# Moderation logs (live)
# ----------------------
# Structure: {user_id: [list of actions]}
# ----------------------
# Live moderation logs
# ----------------------
mod_logs: dict[int, list[dict]] = {}

def log_action(user: discord.Member, action_type: str, reason: str, moderator: discord.User, duration: str | None = None):
    """Append a moderation action to the logs"""
    if user.id not in mod_logs:
        mod_logs[user.id] = []
    mod_logs[user.id].append({
        "type": action_type,
        "reason": reason,
        "moderator": str(moderator),
        "timestamp": datetime.utcnow(),
        "duration": duration
    })

# ---------------- DATABASE ----------------

def load_db():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_db():
    with open("data.json", "w") as f:
        json.dump(db, f, indent=4)

db = load_db()

def get_data(guild):
    gid = str(guild.id)

    if gid not in db:
        db[gid] = {
            "warns": {},
            "banned_words": [],
            "autorole": None,
            "welcome_channel": None,
            "staff_roles": [],
            "afk": {}  # 👈 added AFK here
        }

    # In case AFK didn't exist in older database versions
    if "afk" not in db[gid]:
        db[gid]["afk"] = {}

    return db[gid]

async def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are creative, funny and short in responses."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.9
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"

# ---------------- EMBED ----------------

def embed(title, desc, color=discord.Color.blurple()):
    e = discord.Embed(title=title, description=desc, color=color)
    e.timestamp = datetime.utcnow()
    return e

# ---------------- STAFF CHECK ----------------

def is_staff(member, guild):
    data = get_data(guild)
    if member.guild_permissions.administrator:
        return True
    for role in member.roles:
        if role.id in data["staff_roles"]:
            return True
    return False

def staff_only():
    async def predicate(interaction: discord.Interation):
        if not is_staff(interaction.user, interaction.guild):
            await interaction.response.send_message("❌ You are not staff.", ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)

# ---------------- DM PENALTY ----------------

async def send_dm(member: discord.Member, title: str, reason: str, author: discord.User, action: str, duration: str | None = None):
    guild = member.guild
    embed = discord.Embed(
        title=title,
        description=f"Reason: {reason}",
        color=action_color(action),
        timestamp=discord.utils.utcnow()
    )
    embed.set_author(name=str(author), icon_url=author.display_avatar.url)
    if duration:
        embed.add_field(name="Duration", value=duration)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        print(f"⚠️ Cannot DM {member}: DMs closed or blocked.")

async def send_server(interaction: discord.Interaction, title: str, reason: str, member: discord.Member, author: discord.User, action: str, duration: str | None = None):
    guild = interaction.guild
    embed = discord.Embed(
        title=title,
        description=f"Reason: {reason}",
        color=action_color(action),
        timestamp=discord.utils.utcnow()
    )
    embed.set_author(name=str(author), icon_url=author.display_avatar.url)
    if duration:
        embed.add_field(name="Duration", value=duration)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    await interaction.followup.send(embed=embed)
    
def calculate_duration(amount: int | None, unit: str | None):
    # If no amount is provided, return None -> indefinite mute
    if amount is None or unit is None:
        return None

    unit = unit.lower()
    if unit == "minutes":
        return timedelta(minutes=amount)
    if unit == "hours":
        return timedelta(hours=amount)
    if unit == "days":
        return timedelta(days=amount)

    raise ValueError(f"Unknown time unit: {unit}")
    
def action_color(action: str):
    colors = {
        "warn": discord.Color.orange(),
        "unwarn": discord.Color.green(),
        "mute": discord.Color.dark_grey(),
        "unmute": discord.Color.green(),
        "kick": discord.Color.dark_orange(),
        "ban": discord.Color.red(),
        "unban": discord.Color.green(),
        "timeout": discord.Color.dark_blue(),
        "untimeout": discord.Color.green(),
    }
    return colors.get(action, discord.Color.blurple())

async def send_embed(member: discord.Member, title: str, reason: str, author: discord.User, action: str, duration: str | None = None):
    guild = member.guild
    embed = discord.Embed(
        title=title,
        description=f"Reason: {reason}",
        color=action_color(action),
        timestamp=discord.utils.utcnow()
    )
    embed.set_author(name=str(author), icon_url=author.display_avatar.url)
    if duration:
        embed.add_field(name="Duration", value=duration)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        print(f"Cannot DM {member}")    

async def get_mute_role(guild: discord.Guild) -> discord.Role:
    """Return the Muted role, creating it if it doesn't exist, and lock channels."""
    role = discord.utils.get(guild.roles, name="Muted")
    if not role:
        role = await guild.create_role(name="Muted")
        for channel in guild.channels:
            try:
                await channel.set_permissions(role, send_messages=False, speak=False)
            except Exception:
                pass
    return role
async def mod_embed(
    action: str,
    member: discord.Member,
    staff: discord.Member,
    reason: str,
    duration: str = None
):

    now = datetime.now(timezone.utc)
    unix = int(now.timestamp())

    # Fetch full guild to make sure banner is available
    guild = member.guild

    embed = discord.Embed(
        title=f"{action} | {member.name}",
        color=discord.Color.red(),
        timestamp=now
    )

    # Top section
    embed.add_field(name="🧊 User", value=member.mention, inline=True)
    embed.add_field(name="🛡 Staff", value=staff.mention, inline=True)
    embed.add_field(
        name="⏳ Duration",
        value=duration if duration else "Permanent",
        inline=True
    )

    # Reason
    embed.add_field(name="📄 Reason", value=reason, inline=False)

    # Extra info
    embed.add_field(name="🌍 Server", value=guild.name, inline=True)
    embed.add_field(
        name="🕒 Issued",
        value=f"<t:{unix}:F>\n<t:{unix}:R>",
        inline=True
    )
    embed.add_field(name="🆔 User ID", value=str(member.id), inline=True)

    # Use server icon as thumbnail
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    # Use server banner as main image
    if guild.banner:
        embed.set_image(url=guild.banner.url)

    embed.set_footer(text=f"{guild.name} • Moderation System")

    return embed


async def action_embed_persistent(interaction: discord.Interaction, target: discord.Member, action_name: str, gifs: list):
    if target.id == interaction.user.id:
        await interaction.response.send_message("You can't do this to yourself! 🤪", ephemeral=True)
        return

    data = get_data(interaction.guild)
    user_id = str(interaction.user.id)
    target_id = str(target.id)

    # Ensure user_action dict exists
    if "actions" not in data:
        data["actions"] = {}
    if user_id not in data["actions"]:
        data["actions"][user_id] = {}
    if target_id not in data["actions"][user_id]:
        data["actions"][user_id][target_id] = {}
    if action_name not in data["actions"][user_id][target_id]:
        data["actions"][user_id][target_id][action_name] = 0

    # Increment count
    data["actions"][user_id][target_id][action_name] += 1
    times = data["actions"][user_id][target_id][action_name]

    save_db()

    # Pick random gif
    gif = random.choice(gifs)

    # Embed
    embed = discord.Embed(
        title=f"💖 {interaction.user.display_name} just {action_name} {target.display_name}!",
        description=f"🎉 This happened **{times} time{'s' if times > 1 else ''}** between them!",
        color=discord.Color.random(),
        timestamp=datetime.now(timezone.utc)
    )
    embed.set_image(url=gif)
    embed.set_footer(text="Anime vibes incoming ✨")

    # This await MUST be inside the async function
    await interaction.response.send_message(embed=embed)
    
# -----------------------
# /kiss
# -----------------------
@bot.tree.command(name="kiss", description="Give someone a kiss 💋")
@app_commands.describe(target="Who do you want to kiss?")
async def kiss(interaction: discord.Interaction, target: discord.Member):
    await action_embed_persistent(interaction, target, "kissed", KISS_GIFS)

# -----------------------
# /hug
# -----------------------
@bot.tree.command(name="hug", description="Hug someone 🤗")
@app_commands.describe(target="Who do you want to hug?")
async def hug(interaction: discord.Interaction, target: discord.Member):
    await action_embed_persistent(interaction, target, "hugged", HUG_GIFS)

# -----------------------
# /fuck
# -----------------------
@bot.tree.command(name="fuck", description="…yeah, do the thing 😏")
@app_commands.describe(target="Who do you want to do the thing with?")
async def fuck(interaction: discord.Interaction, target: discord.Member):
    await action_embed_persistent(interaction, target, "fucked", FUCK_GIFS)   
    
@bot.tree.command(name="actionstats", description="See who’s spreading the most anime vibes 😏💖")
async def actionstats(interaction: discord.Interaction):
    data = get_data(interaction.guild)

    if "actions" not in data or not data["actions"]:
        await interaction.response.send_message("No actions have been done yet! 😴", ephemeral=True)
        return

    # Build stats per user
    user_totals = {}  # {user_id: {"kissed": 0, "hugged": 0, "fucked": 0}}
    for user_id, targets in data["actions"].items():
        if user_id not in user_totals:
            user_totals[user_id] = {"kissed": 0, "hugged": 0, "fucked": 0}
        for target_id, actions in targets.items():
            for action_name, count in actions.items():
                if action_name not in user_totals[user_id]:
                    user_totals[user_id][action_name] = 0
                user_totals[user_id][action_name] += count

    # Sort users by total actions
    sorted_users = sorted(user_totals.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # Create embed
    embed = discord.Embed(
        title="📊 Anime Action Leaderboard",
        description="Who’s making everyone blush the most? 😏💖",
        color=discord.Color.random(),
        timestamp=datetime.now(timezone.utc)
    )
    embed.set_footer(text="Keep spreading those anime vibes!")

    # Add fields per top 10 users
    for user_id, counts in sorted_users[:10]:
        member = interaction.guild.get_member(int(user_id))
        if member:
            embed.add_field(
                name=member.display_name,
                value=f"💋 Kissed: {counts.get('kissed', 0)}\n🤗 Hugged: {counts.get('hugged', 0)}\n😏 Fucked: {counts.get('fucked', 0)}",
                inline=False
            )

    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="testembed", description="Just a test embed with timestamp")
async def testembed(interaction: discord.Interaction):

    # Defer first (optional)
    await interaction.response.defer()

    # Create the embed
    e = discord.Embed(
        title="📝 Test Embed",
        description="This is an example embed with a timestamp.",
        color=discord.Color.blurple()
    )

    # Add the timestamp
    e.timestamp = datetime.now(timezone.utc)

    # Send the embed
    await interaction.followup.send(embed=e)
    

@bot.tree.command(name="afk", description="Set your AFK status")
@app_commands.describe(reason="Reason for being AFK")
async def afk(interaction: discord.Interaction, reason: str = "AFK"):

    data = get_data(interaction.guild)
    user_id = str(interaction.user.id)

    # Remove previous AFK if exists
    if user_id in data["afk"]:
        del data["afk"][user_id]

    # Save AFK data
    data["afk"][user_id] = {
        "reason": reason,
        "since": datetime.now(timezone.utc).isoformat(),
        "old_nick": interaction.user.nick
    }
    save_db()

    # Try changing nickname
    try:
        if not interaction.user.display_name.startswith("[AFK]"):
            await interaction.user.edit(nick=f"[AFK] {interaction.user.display_name}")
    except discord.Forbidden:
        print(f"Cannot change nickname for {interaction.user} – check role hierarchy & permissions")
    except Exception as e:
        print(f"Failed to change nickname: {e}")

    # Cute embed
    e = discord.Embed(
        title="🌙 You are now AFK",
        description=f"📝 **Reason:** {reason}\n\nMain character has left the scene.",
        color=discord.Color.purple()
    )
    e.set_thumbnail(url=interaction.user.display_avatar.url)
    e.set_footer(text="I will protect your reputation while you're gone.")
    e.timestamp = datetime.now(timezone.utc)

    await interaction.response.send_message(embed=e)

# -----------------------
# on_message event
# -----------------------
@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    data = get_data(message.guild)
    user_id = str(message.author.id)

    # ====== Remove AFK if user talks ======
    if user_id in data["afk"]:
        afk_data = data["afk"][user_id]

        # Handle old AFK string format
        if isinstance(afk_data, str):
            afk_data = {
                "reason": afk_data,
                "since": datetime.now(timezone.utc).isoformat(),
                "old_nick": None
            }
            data["afk"][user_id] = afk_data
            save_db()

        old_nick = afk_data.get("old_nick")
        since = datetime.fromisoformat(afk_data["since"])
        now = datetime.now(timezone.utc)

        duration = now - since

        days = duration.days
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60

        # Format duration nicely
        time_parts = []
        if days > 0: time_parts.append(f"{days}d")
        if hours > 0: time_parts.append(f"{hours}h")
        if minutes > 0: time_parts.append(f"{minutes}m")
        if seconds > 0: time_parts.append(f"{seconds}s")
        time_string = " ".join(time_parts)

        # Remove AFK
        del data["afk"][user_id]
        save_db()

        # Restore nickname
        try:
            if old_nick != message.author.nick:
                await message.author.edit(nick=old_nick)
        except discord.Forbidden:
            print(f"Cannot restore nickname for {message.author}")
        except Exception as e:
            print(f"Failed to restore nickname: {e}")

        e = discord.Embed(
            title="👋 Welcome back!",
            description=f"⏳ You were AFK for **{time_string}**.\nHope the adventure was worth it.",
            color=discord.Color.green()
        )
        e.set_thumbnail(url=message.author.display_avatar.url)
        e.set_footer(text="Spotlight is back on you.")
        e.timestamp = now

        await message.reply(embed=e)

    # ====== Notify if mentioned users are AFK ======
    for user in message.mentions:
        uid = str(user.id)
        if uid in data["afk"]:
            afk_data = data["afk"][uid]

            # Handle old format
            if isinstance(afk_data, str):
                afk_data = {
                    "reason": afk_data,
                    "since": datetime.now(timezone.utc).isoformat(),
                    "old_nick": None
                }
                data["afk"][uid] = afk_data
                save_db()

            reason = afk_data.get("reason", "AFK")
            since = datetime.fromisoformat(afk_data.get("since", datetime.now(timezone.utc).isoformat()))
            now = datetime.now(timezone.utc)
            duration = now - since

            days = duration.days
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60

            time_parts = []
            if days > 0: time_parts.append(f"{days}d")
            if hours > 0: time_parts.append(f"{hours}h")
            if minutes > 0: time_parts.append(f"{minutes}m")

            time_string = " ".join(time_parts) if time_parts else "just now"

            e = discord.Embed(
                title="💤 They are AFK",
                description=(
                    f"{user.mention} is currently away.\n\n"
                    f"📝 **Reason:** {reason}\n"
                    f"⏳ AFK for: **{time_string}**"
                ),
                color=discord.Color.blurple()
            )
            e.set_thumbnail(url=user.display_avatar.url)
            e.set_footer(text="Patience. They will return.")
            e.timestamp = now

            await message.reply(embed=e)

    await bot.process_commands(message)
    

# ---------------------
# ---------------- STAFF ROLE ----------------

@bot.tree.command(name="setstaffrole")
@app_commands.describe(roles="One or more role mentions (e.g., @Mod @Admin)")
async def setstaffrole(interaction: discord.Interaction, roles: str):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

    if not roles:
        return await interaction.response.send_message(
            "⚠️ Please provide at least one role to add.", ephemeral=True
        )

    # Parse role mentions from the input string
    role_mentions = roles.split()
    added = []
    data = get_data(interaction.guild)

    for mention in role_mentions:
        # Extract role ID from mention (e.g., <@&123456789> -> 123456789)
        role_id_str = mention.strip("<@&>")
        if not role_id_str.isdigit():
            continue

        role_id = int(role_id_str)
        role = interaction.guild.get_role(role_id)

        if role and role.id not in data["staff_roles"]:
            data["staff_roles"].append(role.id)
            added.append(role)

    save_db()

    if added:
        role_str = ", ".join(r.mention for r in added)
        await interaction.response.send_message(
            embed=embed("👮 Staff Role(s) Added", role_str)
        )
    else:
        await interaction.response.send_message(
            "ℹ️ All the roles you provided are already staff roles.",
            ephemeral=True
        )

# ---------------- WARN ----------------


@bot.tree.command(name="setautorole")
@app_commands.describe(roles="One or more role mentions to add (e.g., @Member @Verified)")
async def setautorole(interaction: discord.Interaction, roles: str):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

    if not roles:
        return await interaction.response.send_message(
            "⚠️ Please provide at least one role to add.", ephemeral=True
        )

    # Parse role mentions from the input string
    role_mentions = roles.split()
    added = []
    data = get_data(interaction.guild)

    # Initialize auto_roles list if it doesn't exist
    if "auto_roles" not in data:
        data["auto_roles"] = []

    for mention in role_mentions:
        # Extract role ID from mention (e.g., <@&123456789> -> 123456789)
        role_id_str = mention.strip("<@&>")
        if not role_id_str.isdigit():
            continue

        role_id = int(role_id_str)
        role = interaction.guild.get_role(role_id)

        if role and role.id not in data["auto_roles"]:
            data["auto_roles"].append(role.id)
            added.append(role)

    save_db()

    if added:
        role_str = ", ".join(r.mention for r in added)
        await interaction.response.send_message(
            embed=embed("✅ Auto Role(s) Added", f"These roles will be given to new members:\n{role_str}")
        )
    else:
        await interaction.response.send_message(
            "ℹ️ All the roles you provided are already auto roles.",
            ephemeral=True
        )


@bot.tree.command(name="removeautorole")
@app_commands.describe(roles="One or more role mentions to remove")
async def removeautorole(interaction: discord.Interaction, roles: str):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

    if not roles:
        return await interaction.response.send_message(
            "⚠️ Please provide at least one role to remove.", ephemeral=True
        )

    role_mentions = roles.split()
    removed = []
    data = get_data(interaction.guild)

    if "auto_roles" not in data:
        data["auto_roles"] = []

    for mention in role_mentions:
        role_id_str = mention.strip("<@&>")
        if not role_id_str.isdigit():
            continue

        role_id = int(role_id_str)
        role = interaction.guild.get_role(role_id)

        if role and role.id in data["auto_roles"]:
            data["auto_roles"].remove(role.id)
            removed.append(role)

    save_db()

    if removed:
        role_str = ", ".join(r.mention for r in removed)
        await interaction.response.send_message(
            embed=embed("🗑️ Auto Role(s) Removed", role_str)
        )
    else:
        await interaction.response.send_message(
            "ℹ️ None of the provided roles were in the auto roles list.",
            ephemeral=True
        )


@bot.tree.command(name="listautoroles")
@app_commands.describe()
async def listautoroles(interaction: discord.Interaction):
    """List all auto roles configured for this server"""
    data = get_data(interaction.guild)
    auto_roles = data.get("auto_roles", [])

    if not auto_roles:
        return await interaction.response.send_message(
            "ℹ️ No auto roles configured for this server.",
            ephemeral=True
        )

    roles = [interaction.guild.get_role(role_id) for role_id in auto_roles]
    roles = [r for r in roles if r is not None]

    if not roles:
        return await interaction.response.send_message(
            "ℹ️ No valid auto roles found (roles may have been deleted).",
            ephemeral=True
        )

    role_str = "\n".join(r.mention for r in roles)
    await interaction.response.send_message(
        embed=embed("📋 Auto Roles", f"These roles will be given to new members:\n\n{role_str}")
    )


@bot.event
async def on_member_join(member: discord.Member):
    """Give new members the auto roles"""
    data = get_data(member.guild)
    auto_roles = data.get("auto_roles", [])

    if not auto_roles:
        return

    roles = [member.guild.get_role(role_id) for role_id in auto_roles]
    roles = [r for r in roles if r is not None]  # Remove None values for deleted roles

    if roles:
        await member.add_roles(*roles)
# ----------------------
# KICK COMMAND
# ----------------------
@bot.tree.command(name="kick")
@staff_only()
@app_commands.describe(member="Member to kick", reason="Reason")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await interaction.response.defer()
    try:
        await member.kick(reason=reason)
        log_action(member, "kick", reason, interaction.user)
        await send_dm(member, "⛔ You have been kicked", reason, interaction.user, "kick")
        await send_server(interaction, f"⛔ {member} has been kicked", reason, member, interaction.user, "kick")
    except discord.Forbidden:
        await interaction.followup.send(f"⚠️ I cannot kick {member.mention}. Check my permissions.")

# ----------------------
# BAN / UNBAN
# ----------------------
@bot.tree.command(name="ban")
@staff_only()
@app_commands.describe(member="Member to ban", reason="Reason")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await interaction.response.defer()
    try:
        await member.ban(reason=reason)
        log_action(member, "ban", reason, interaction.user)
        await send_dm(member, "⛔ You have been banned", reason, interaction.user, "ban")
        await send_server(interaction, f"⛔ {member} has been banned", reason, member, interaction.user, "ban")
    except discord.Forbidden:
        await interaction.followup.send(f"⚠️ I cannot ban {member.mention}. Check my permissions.")

@bot.tree.command(name="unban")
@staff_only()
@app_commands.describe(user_id="User ID to unban", reason="Reason")
async def unban(interaction: discord.Interaction, user_id: int, reason: str = "No reason provided"):
    await interaction.response.defer()
    user = await bot.fetch_user(user_id)
    try:
        await interaction.guild.unban(user, reason=reason)
        log_action(user, "unban", reason, interaction.user)
        await send_dm(user, "✅ You have been unbanned", reason, interaction.user, "unban")
        await send_server(interaction, f"✅ {user} has been unbanned", reason, user, interaction.user, "unban")
    except discord.Forbidden:
        await interaction.followup.send(f"⚠️ I cannot unban user {user_id}. Check my permissions.")

# ----------------------
# TIMEOUT / UNTIMEOUT
# ----------------------
@bot.tree.command(name="timeout")
@staff_only()
@app_commands.describe(member="Member to timeout", amount="Duration", unit="minutes / hours / days", reason="Reason")
@app_commands.choices(unit=[
    app_commands.Choice(name="Minutes", value="minutes"),
    app_commands.Choice(name="Hours", value="hours"),
    app_commands.Choice(name="Days", value="days")
])
async def timeout(interaction: discord.Interaction, member: discord.Member, amount: int, unit: app_commands.Choice[str], reason: str = "No reason provided"):
    await interaction.response.defer()
    duration_value = unit.value
    duration_delta = calculate_duration(amount, duration_value)
    until = discord.utils.utcnow() + duration_delta if duration_delta else None
    try:
        await member.edit(timed_out_until=until, reason=reason)
        formatted_duration = f"{amount} {duration_value}" if duration_delta else None
        log_action(member, "timeout", reason, interaction.user, duration=formatted_duration)
        await send_dm(member, "⏱ You have been timed out", reason, interaction.user, "timeout", formatted_duration)
        await send_server(interaction, f"⏱ {member} timed out", reason, member, interaction.user, "timeout", formatted_duration)

        # Auto-untimeout after duration
        if duration_delta:
            await asyncio.sleep(duration_delta.total_seconds())
            await member.edit(timed_out_until=None)
            log_action(member, "untimeout", "Timeout duration ended", bot.user)
            await send_dm(member, "⏮ Your timeout has ended", "Duration ended", bot.user, "untimeout")
            await send_server(interaction, f"⏮ {member} timeout ended", "Duration ended", member, bot.user, "untimeout")
    except discord.Forbidden:
        await interaction.followup.send(f"⚠️ Cannot timeout {member.mention}. Check my permissions.")

@bot.tree.command(name="untimeout")
@staff_only()
@app_commands.describe(member="Member to remove timeout from", reason="Reason")
async def untimeout(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await interaction.response.defer()
    try:
        await member.edit(timed_out_until=None, reason=reason)
        log_action(member, "untimeout", reason, interaction.user)
        await send_dm(member, "⏮ Your timeout has been removed", reason, interaction.user, "untimeout")
        await send_server(interaction, f"⏮ {member} timeout removed", reason, member, interaction.user, "untimeout")
    except discord.Forbidden:
        await interaction.followup.send(f"⚠️ Cannot remove timeout from {member.mention}. Check my permissions.")
        
@bot.tree.command(name="warn")
@staff_only()
@app_commands.describe(member="Member to warn", reason="Reason for warning")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await interaction.response.defer()

    # Log the warning
    log_action(member, "warn", reason, interaction.user)

    # Count current warnings
    user_warns = [w for w in mod_logs.get(member.id, []) if w["type"] == "warn"]

    # DM & server notification
    await send_dm(member, "⚠️ You have been warned", reason, interaction.user, "warn")
    await send_server(interaction, f"⚠️ {member} warned", reason, member, interaction.user, "warn")

    # Auto-kick at 3 warnings
    if len(user_warns) >= 3:
        try:
            await member.kick(reason="Reached 3 warnings")
            log_action(member, "kick", "Auto-kick after 3 warnings", interaction.user)
            await send_dm(member, "⛔ You have been kicked", "Reached 3 warnings", interaction.user, "kick")
            await send_server(interaction, f"⛔ {member} auto-kicked for 3 warnings", "Reached 3 warnings", member, interaction.user, "kick")
        except discord.Forbidden:
            await interaction.followup.send(f"⚠️ I cannot kick {member.mention}. Check my permissions.")
@bot.tree.command(name="unwarn")
@staff_only()
@app_commands.describe(member="Member to remove a warning from", reason="Reason for unwarn")
async def unwarn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await interaction.response.defer()

    # Get all warnings for this member
    user_warns = [w for w in mod_logs.get(member.id, []) if w["type"] == "warn"]

    if not user_warns:
        await interaction.followup.send(f"⚠️ {member} has no warnings to remove.")
        return

    # Remove the latest warning
    latest_warn = user_warns[-1]
    mod_logs[member.id].remove(latest_warn)

    # Log the unwarn action
    log_action(member, "unwarn", reason, interaction.user)

    # Notify user and server
    await send_dm(member, "✅ A warning has been removed", reason, interaction.user, "unwarn")
    await send_server(interaction, f"✅ {member} has been unwarned", reason, member, interaction.user, "unwarn")            
            
@bot.tree.command(name="userinfo", description="Get info about a user")
@app_commands.describe(member="Member")
async def userinfo(interaction: discord.Interaction, member: discord.Member):

    embed = discord.Embed(title="👤 User Info", color=discord.Color.blurple())
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

    embed.add_field(name="🆔 ID", value=member.id)
    embed.add_field(name="📅 Joined", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="🎂 Created", value=member.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="🎭 Roles", value=", ".join([role.mention for role in member.roles[1:]]) or "None", inline=False)
    embed.add_field(name="🤖 Bot?", value="Yes" if member.bot else "No")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="Get a user's avatar")
@app_commands.describe(member="Member")
async def avatar(interaction: discord.Interaction, member: discord.Member):

    embed = discord.Embed(title=f"🖼 {member}'s Avatar")
    embed.set_image(url=member.display_avatar.url)

    await interaction.response.send_message(embed=embed)   
    
# ----------------------
# REPORT COMMAND
# ----------------------
@bot.tree.command(name="report")
@staff_only()
@app_commands.describe(member="Member to generate report for")
async def report(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    logs = mod_logs.get(member.id, [])

    if not logs:
        await interaction.followup.send(f"✅ {member} has no penalties.")
        return

    # Separate by type
    sections = {"warn": [], "cmute": [], "cunmute": [], "timeout": [], "untimeout": [], "kick": [], "ban": [], "unban": []}
    for log in logs:
        if log["type"] in sections:
            sections[log["type"]].append(log)

    embed = discord.Embed(
        title=f"📋 Penalty Report for {member}",
        color=discord.Color.orange(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)

    for action, items in sections.items():
        if not items:
            continue
        lines = []
        for i, p in enumerate(items, start=1):
            line = f"**Reason:** {p['reason']}\n**Moderator:** {p['moderator']}\n**Date:** {p['timestamp'].strftime('%Y-%m-%d %H:%M')}"
            if p.get("duration"):
                line += f"\n**Duration:** {p['duration']}"
            lines.append(f"{i}. {line}")
        embed.add_field(name=action.upper(), value="\n\n".join(lines), inline=False)

    await interaction.followup.send(embed=embed)

@bot.tree.command(name="stats", description="Bot and server stats")
async def stats(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(title="📊 Server & Bot Stats", color=discord.Color.green())

    embed.add_field(name="🏠 Server", value=guild.name)
    embed.add_field(name="👥 Members", value=guild.member_count)
    embed.add_field(name="💬 Channels", value=len(guild.channels))
    embed.add_field(name="🎭 Roles", value=len(guild.roles))
    embed.add_field(name="🤖 Bot Ping", value=f"{round(bot.latency * 1000)}ms")
    embed.add_field(name="🗓 Created", value=guild.created_at.strftime("%Y-%m-%d"))

    await interaction.response.send_message(embed=embed)
# ---------------- TIMEOUT ----------------


# ---------------- ADDBOT (Embedded) ----------------

@bot.tree.command(name="addbot", description="Get the bot invite link")
async def addbot(interaction: discord.Interaction):
    CLIENT_ID = bot.user.id  # auto-detect your bot ID
    permissions = 8  # full admin, change if needed
    scopes = "bot%20applications.commands"
    invite_link = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&permissions={permissions}&scope={scopes}"

    embed_msg = discord.Embed(
        title="🤖 Add Me to Your Server!",
        description=f"Click below to invite me safely:\n[Invite Me]({invite_link}) This bot is made by legitkair0 or jxst_kairo on IG.",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed_msg.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

    try:
        await interaction.user.send(embed=embed_msg)
        await interaction.response.send_message("📬 I've DM'd you the invite link!", ephemeral=True)
    except:
        # fallback in the channel if DM fails
        await interaction.response.send_message(
            f"❌ I couldn't DM you. Here's the link: {invite_link}",
            ephemeral=True
        )
# ---------------- LOCK ----------------

@bot.tree.command(name="lock")
@staff_only()
async def lock(interaction: discord.Interaction):
    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message(embed=embed("🔒 Locked", interaction.channel.mention))

@bot.tree.command(name="unlock")
@staff_only()
async def unlock(interaction: discord.Interaction):
    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message(embed=embed("🔓 Unlocked", interaction.channel.mention))

# ---------------- CLEAR ----------------

@bot.tree.command(name="clear")
@staff_only()
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(embed=embed("🧹 Cleared", f"{len(deleted)} messages removed."))

# ---------------- SLOWMODE ----------------

@bot.tree.command(name="slowmode")
@staff_only()
async def slowmode(interaction: discord.Interaction, seconds: int):
    await interaction.channel.edit(slowmode_delay=seconds)
    await interaction.response.send_message(embed=embed("🐢 Slowmode Set", f"{seconds}s"))

# ---------------- HELP ----------------

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embed(
        "📖 Help Menu",
        """
👮 Moderation:
/warn
/kick
/ban
/unban
/timeout
/untimeout
/lock
/unlock
/clear
/slowmode
/cmute
/cunmute
/vmute
/vunmute

⚙️ Setup:
/setstaffrole
/setautorole 
/removeautorole
/listautoroles

🤡 Fun:
-

👅 Freaky:
/kiss
/hug
/fuck
/actionstats

ℹ️ Info:
/addbot
/help
/userinfo
/stats
/avatar
/afk
/report
"""
    ), ephemeral=True)

# ---------------- READY ----------------
db = {}  # Simplified; you can replace with your JSON load/save functions

@bot.event
async def on_ready():
    await bot.tree.sync()
    for guild_id in db:
        db[guild_id]["afk"] = {}  # 3.x way
    print("Bot ready. AFK cleared.")
bot.run(TOKEN)
