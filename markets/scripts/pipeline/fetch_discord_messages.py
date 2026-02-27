#!/usr/bin/env python3
"""
fetch_discord_messages.py
Fetch latest messages from a Discord channel and output as JSON Lines.

Usage:
    DISCORD_BOT_TOKEN="YOUR_TOKEN" python3 fetch_discord_messages.py --channel-id 1473508792929882142 --limit 40

Output:
    JSON Lines format, one message per line:
    {"message_id": "...", "author": "...", "text": "...", "timestamp": "..."}
"""

import os
import sys
import json
import argparse

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("ERROR: discord.py not installed. Run: pip3 install discord.py", file=sys.stderr)
    sys.exit(1)


async def fetch_messages(channel_id: int, limit: int):
    """Fetch messages from Discord channel and output as JSON Lines."""
    
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
                # Try fetching via REST API
                try:
                    channel = await client.fetch_channel(channel_id)
                except Exception as e:
                    print(f"ERROR: Could not access channel {channel_id}: {e}", file=sys.stderr)
                    await client.close()
                    sys.exit(1)
            
            print(f"Fetching {limit} messages from #{channel.name} (ID: {channel.id})", file=sys.stderr)
            
            async for message in channel.history(limit=limit):
                if message.content:  # Only messages with text content
                    msg_data = {
                        "message_id": str(message.id),
                        "author": str(message.author),
                        "author_id": str(message.author.id),
                        "text": message.content,
                        "timestamp": message.created_at.isoformat()
                    }
                    print(json.dumps(msg_data, ensure_ascii=False))
            
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
        finally:
            await client.close()
    
    await client.start(token)


def main():
    parser = argparse.ArgumentParser(description="Fetch Discord messages as JSON Lines")
    parser.add_argument("--channel-id", type=int, required=True, help="Discord channel ID")
    parser.add_argument("--limit", type=int, default=40, help="Number of messages to fetch")
    args = parser.parse_args()
    
    import asyncio
    asyncio.run(fetch_messages(args.channel_id, args.limit))


if __name__ == "__main__":
    main()
