# Discord Water Reminder Bot

A Discord bot with welcome messages, simple word moderation, and scheduled water reminders.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your bot token and channel ID.
4. In the Discord Developer Portal, enable **Message Content Intent** and **Server Members Intent**.
5. Start the bot:

   ```powershell
   python main.py
   ```

## Commands

- `*hello` — greets the sender.
- `*water` — sends a water reminder.

## Required server permissions

- View Channels
- Send Messages
- Read Message History
- Manage Messages

Never commit or share `.env`; it contains your bot token.

## Demo
https://discord.com/oauth2/authorize?client_id=1563585239060844564&permissions=84992&integration_type=0&scope=bot+applications.commands
## Test Server
https://discord.gg/zNHhn3jXHH
