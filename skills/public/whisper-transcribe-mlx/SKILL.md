---
name: whisper-transcribe-mlx
description: ローカル環境でWhisper(MLX)を使って音声文字起こしを行うスキル。ユーザーが音声/動画ファイルの書き起こし、議事録化、字幕化、内容確認を依頼したとき、またはDiscord/Telegramで音声メッセージを受信して内容確認が必要なときに使う。macOS Apple Silicon + uv + Python環境で `uv run python transcribe.py audio.mp3 mlx-community/whisper-small-mlx` の形で実行し、結果を返す。
---

# whisper-transcribe-mlx

## 目的
ローカル実行で音声ファイルを安全に文字起こしする。

## 前提チェック
1. 作業ディレクトリを `~/.openclaw/mlx-whisper` にする。
2. 以下が使えることを確認する。
   - `uv`
   - `python`
   - `ffmpeg`（mlx-whisperが内部利用）
3. 入力ファイル（例: `audio.mp3`）が存在することを確認する。

## 基本コマンド
```bash
uv run python transcribe.py audio.mp3 mlx-community/whisper-small-mlx
```

## 実行手順
1. 入力ファイルの存在確認。
2. 文字起こしコマンド実行。
3. 標準出力の転記テキストをそのまま返す。
4. 必要なら日本語で要点要約を追加する（ユーザーが求めた場合のみ）。

## Discord/Telegram音声受信時の運用
1. 音声添付を受信したら、まずこのスキルで文字起こしを実行する。
2. 推測補完せず、文字起こし結果ベースで内容確認・応答を行う。
3. 文字起こしが失敗した場合は、失敗理由を短く伝えて再送/再試行を提案する。

## 失敗時の切り分け
- `FileNotFoundError: ffmpeg`:
  - `brew install ffmpeg` を実行し、再試行する。
- 入力ファイルがない:
  - ファイルパスを確認して再指定を依頼する。
- モデル取得失敗/通信失敗:
  - ネットワーク状態を確認し、再試行する。

## 返答方針
- まず書き起こし結果を提示する。
- 不明瞭箇所は推測で補完しない。
- 要約・整形は依頼があれば追加する。