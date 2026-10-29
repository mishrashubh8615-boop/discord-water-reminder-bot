import logging
import os
from pathlib import Path

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv


PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env", override=True)


def required_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not set. Add it to .env.")
    return value


def reminder_minutes() -> int:
    try:
        value = int(os.getenv("WATER_REMINDER_MINUTES", "60"))
    except ValueError as error:
        raise RuntimeError("WATER_REMINDER_MINUTES must be a whole number.") from error
    if value <= 0:
        raise RuntimeError("WATER_REMINDER_MINUTES must be greater than zero.")
    return value


TOKEN = required_setting("DISCORD_TOKEN")
WATER_CHANNEL_ID = int(required_setting("WATER_CHANNEL_ID"))
WATER_REMINDER_MINUTES = reminder_minutes()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="*", intents=intents)


@bot.event
async def on_ready():
    logger.info("Ready as %s", bot.user)
    if not water_reminder.is_running():
        water_reminder.start()


@bot.event
async def on_member_join(member: discord.Member):
    try:
        await member.send(f"Welcome to the server, {member.name}!")
    except discord.Forbidden:
        logger.warning("Could not send a welcome DM to %s", member)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if "shit" in message.content.lower():
        try:
            await message.delete()
            await message.channel.send(
                f"Please avoid that language, {message.author.mention}."
            )
        except discord.Forbidden:
            logger.warning("Missing permission to moderate messages in %s", message.channel)

    await bot.process_commands(message)


@bot.command()
async def hello(ctx: commands.Context):
    await ctx.send(f"Hello {ctx.author.mention}!")


@tasks.loop(minutes=WATER_REMINDER_MINUTES)
async def water_reminder():
    channel = bot.get_channel(WATER_CHANNEL_ID)
    if channel is None:
        logger.warning("Water reminder channel %s was not found.", WATER_CHANNEL_ID)
        return

    try:
        await channel.send("💧 Water reminder! Take a break and drink some water.")
    except discord.Forbidden:
        logger.warning("Missing permission to send reminders in %s", channel)
    except discord.HTTPException as error:
        logger.warning("Could not send a water reminder: %s", error)


@water_reminder.before_loop
async def before_water_reminder():
    await bot.wait_until_ready()


@bot.command()
async def water(ctx: commands.Context):
    await ctx.send("💧 Remember to drink water and stay hydrated!")


if __name__ == "__main__":
    bot.run(TOKEN, log_level=logging.INFO)
