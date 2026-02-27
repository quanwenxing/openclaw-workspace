#!/usr/bin/env python3
"""
send_discord_message.py
Send a message to a Discord channel.

Usage:
    DISCORD_BOT_TOKEN="YOUR_TOKEN" python3 send_discord_message.py --channel-id 1473508792929882142 --message "Hello!"
"""

import os
import sys
import argparse

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("ERROR: discord.py not installed. Run: pip3 install discord.py", file=sys.stderr)
    sys.exit(1)


async def send_message(channel_id: int, message_text: str):
    """Send a message to Discord channel."""
    
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.guilds = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(channel_id)
            if not channel:
                try:
                    channel = await client.fetch_channel(channel_id)
                except Exception as e:
                    print(f"ERROR: Could not access channel {channel_id}: {e}", file=sys.stderr)
                    await client.close()
                    sys.exit(1)
            
            await channel.send(message_text)
            print(f"Message sent to channel {channel_id}", file=sys.stderr)
            
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
        finally:
            await client.close()
    
    await client.start(token)


def main():
    parser = argparse.ArgumentParser(description="Send message to Discord channel")
    parser.add_argument("--channel-id", type=int, required=True, help="Discord channel ID")
    parser.add_argument("--message", type=str, required=True, help="Message text to send")
    args = parser.parse_args()
    
    import asyncio
    asyncio.run(send_message(args.channel_id, args.message))


if __name__ == "__main__":
    main()
