#!/bin/bash
# scripts/agent-wrapper.sh
# claude-codex-collab skill resource
# Usage: ./agent-wrapper.sh <claude|codex> "<prompt>" [options]

AGENT=$1
PROMPT=$2
OPTS=$3

if [ "$AGENT" = "claude" ]; then
    # Claude Code: Use --print for non-interactive mode
    /Users/username/.local/bin/claude -p "$PROMPT" --permission-mode bypassPermissions $OPTS
elif [ "$AGENT" = "codex" ]; then
    # Codex CLI: Use 'exec' subcommand for non-interactive mode
    /opt/homebrew/bin/codex exec "$PROMPT" $OPTS
else
    echo "Unknown agent: $AGENT"
    exit 1
fi
