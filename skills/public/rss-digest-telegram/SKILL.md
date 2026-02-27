---
name: rss-digest-telegram
description: 固定RSS(OPML)から更新記事を集約し、日本語サマリーを作成してTelegramへ送る。朝8時運用（前日分集計）と夜8時運用（前回実行以降の差分）を実行するときに使う。重複排除とソースごと最大2件の制限が必要な定期レポート作成で使う。
---

# RSS Digest Telegram

Run the digest script, rewrite each picked item into concise Japanese (1 line), then send to Telegram.

## Inputs

- Skill dir: `/Users/username/.openclaw/workspace/skills/public/rss-digest-telegram`
- OPML (fixed list): `/Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/references/blog-feeds.opml`
- State file: `/Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/state/digest-state.json`
- Output file: `/Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/state/latest-report.txt`

## Run

Morning run (08:00 JST, previous day window):

```bash
python3 /Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/scripts/build_digest.py \
  --mode morning \
  --opml /Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/references/blog-feeds.opml \
  --state /Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/state/digest-state.json \
  --output /Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/state/latest-report.txt
```

Evening run (20:00 JST, diff since previous run):

```bash
python3 /Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/scripts/build_digest.py \
  --mode evening \
  --opml /Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/references/blog-feeds.opml \
  --state /Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/state/digest-state.json \
  --output /Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/state/latest-report.txt
```

## Deliver

1. Read `/Users/username/.openclaw/workspace/skills/public/rss-digest-telegram/state/latest-report.txt`.
2. Reformat the report before sending:
   - Keep only picked sources/items from the script output.
   - Rewrite each item as Japanese summary in 1 line: `・見出し — 要点（日本語）`
   - Preserve `出典:` URL for every item.
3. Send text with `message` tool:
   - `action=send`
   - `channel=telegram`
   - `target=435506838`
   - `message=<日本語レポート>`

If the report text is too long, split into multiple messages in order.

## Guardrails

- Keep only sources with updates.
- Enforce max 2 items per source (script already applies it).
- Keep URLs for each item (`出典:` line).
- Use Japanese for all summaries and headings.
- Do not add speculation.
