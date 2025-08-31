import discord
from discord.ext import commands
from model import detect_bullying, academic_bullying_check
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # required for mentions

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Ignore bot’s own messages and system messages
    # if message.author == bot.user or message.is_system():
    #     return

    print(f"Message from {message.author}: {message.content}")

    text = message.content
    is_bullying, score, label = detect_bullying(text)
    is_academic = academic_bullying_check(text)

    if is_bullying or is_academic:
        if message.guild:  # Only in servers
            review_channel = discord.utils.get(message.guild.text_channels, name='review-channel')
            if review_channel:
                flag_msg = (
                    f"🚨 **Flagged Message** 🚨\n"
                    f"👤 User: {message.author.mention}\n"
                    f"💬 Content: {text}\n"
                    f"📌 Type: {label}, Score: {score}\n"
                    f"🔗 [Jump to Message]({message.jump_url})"
                )
                await review_channel.send(flag_msg)
        
        # DM support message to mentioned users
        for mention in message.mentions:
            if mention != message.author and mention != bot.user:
                try:
                    support_msg = (
                        "⚠️ A potential issue was detected in a message mentioning you.\n"
                        "You can report anonymously here: [school link]\n"
                        "Resources: [helpline]\n"
                        "Stay safe ❤️"
                    )
                    await mention.send(support_msg)
                except discord.Forbidden:
                    print(f"Could not DM {mention} (DMs disabled).")

    # Important: let commands still work
    await bot.process_commands(message)

# Load token from .env
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

if not token:
    raise ValueError("❌ No DISCORD_TOKEN found in .env file")

bot.run(token)
