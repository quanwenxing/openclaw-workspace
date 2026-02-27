#!/bin/bash
#
# sync_discord_insights.sh
# Sync manual Discord insights into ledger (cron-compatible)
#
# Usage: Add to crontab, e.g.:
#   */15 * * * * /Users/username/.openclaw/workspace/markets/scripts/pipeline/sync_discord_insights.sh
#

set -e

# --- Configuration ---
DISCORD_CHANNEL_ID="1473508792929882142"
INGEST_SCRIPT="/Users/username/.openclaw/workspace/markets/scripts/pipeline/ingest_manual_discord_event.py"
ROOT_DIR="/Users/username/.openclaw/workspace"
TEMP_MESSAGES="/tmp/discord_messages_$$.jsonl"
INGESTED_COUNT=0
INGESTED_FILE="/tmp/discord_ingested_count_$$.txt"

echo "0" > "$INGESTED_FILE"

# --- Step 1: Fetch messages from Discord ---
# YOU MUST IMPLEMENT THIS: Replace the command below with your actual Discord fetch script.
# The fetch script should output JSON Lines format with fields: message_id, author, text
#
# Example using a Python script with discord.py:
#   DISCORD_BOT_TOKEN="YOUR_TOKEN" python3 /path/to/fetch_discord_messages.py --channel-id "$DISCORD_CHANNEL_ID" --limit 40 > "$TEMP_MESSAGES"
#

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fetching messages from Discord channel ${DISCORD_CHANNEL_ID}..."

# === REPLACE THIS BLOCK WITH YOUR ACTUAL DISCORD FETCH COMMAND ===
# Example:
# export DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN"
# python3 /Users/username/.openclaw/workspace/markets/scripts/pipeline/fetch_discord_messages.py \
#     --channel-id "$DISCORD_CHANNEL_ID" \
#     --limit 40 \
#     > "$TEMP_MESSAGES"
#
# For now, this placeholder will fail - you MUST implement the fetch:
echo "ERROR: Discord fetch command not implemented. Edit this script and replace the fetch block." >&2
exit 1
# === END REPLACE BLOCK ===

# Check if messages were fetched
if [ ! -s "$TEMP_MESSAGES" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No messages fetched or file empty. Exiting."
    rm -f "$TEMP_MESSAGES" "$INGESTED_FILE"
    exit 0
fi

# --- Step 2 & 3: Process messages containing #インサイト分析 ---
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Processing messages for #インサイト分析..."

while IFS= read -r message_json; do
    [ -z "$message_json" ] && continue
    
    # Check if message contains the target hashtag
    if echo "$message_json" | jq -e '.text | contains("#インサイト分析")' > /dev/null 2>&1; then
        MESSAGE_ID=$(echo "$message_json" | jq -r '.message_id')
        AUTHOR=$(echo "$message_json" | jq -r '.author')
        TEXT=$(echo "$message_json" | jq -r '.text')
        SOURCE_URL="discord://${DISCORD_CHANNEL_ID}/${MESSAGE_ID}"

        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Processing message ${MESSAGE_ID} by ${AUTHOR}..."
        
        # Run ingest script (handles dedupe internally)
        if python3 "$INGEST_SCRIPT" \
            --root "$ROOT_DIR" \
            --message-id "$MESSAGE_ID" \
            --author "$AUTHOR" \
            --text "$TEXT" \
            --source-url "$SOURCE_URL"; then
            # Increment count (atomic via file to work across subshell)
            COUNT=$(cat "$INGESTED_FILE")
            echo $((COUNT + 1)) > "$INGESTED_FILE"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Ingested message ${MESSAGE_ID}"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Warning: Ingest script returned non-zero for ${MESSAGE_ID}"
        fi
    fi
done < "$TEMP_MESSAGES"

INGESTED_COUNT=$(cat "$INGESTED_FILE")

# --- Step 4 & 5: Send update if new items were ingested ---
if [ "$INGESTED_COUNT" -gt 0 ]; then
    UPDATE_MESSAGE="📊 Manual Discord insights sync completed. ${INGESTED_COUNT} new item(s) ingested to ledger."
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ${UPDATE_MESSAGE}"
    
    # YOU MUST IMPLEMENT THIS: Send update back to Discord
    # Example using a Python script or CLI tool:
    #   python3 /path/to/send_discord_message.py --channel-id "$DISCORD_CHANNEL_ID" --message "$UPDATE_MESSAGE"
    #
    # === REPLACE THIS BLOCK WITH YOUR ACTUAL DISCORD SEND COMMAND ===
    echo "NOTE: Update message ready but send command not implemented. Edit this script."
    echo "Message to send: ${UPDATE_MESSAGE}"
    # === END REPLACE BLOCK ===
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new items ingested. No update sent."
fi

# Cleanup
rm -f "$TEMP_MESSAGES" "$INGESTED_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync complete."
exit 0
