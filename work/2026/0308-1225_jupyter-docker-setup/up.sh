#!/bin/bash
# キーチェーンからキーを取得
export TS_AUTHKEY=$(security find-generic-password -a "$USER" -s "TailscaleAuthKey" -w 2>/dev/null)

if [ -z "$TS_AUTHKEY" ]; then
    echo "Error: 'TailscaleAuthKey' not found in Keychain."
    echo "Please run: security add-generic-password -a \"$USER\" -s \"TailscaleAuthKey\" -w \"your-ts-key\""
    exit 1
fi

# Jupyter Tokenもキーチェーンまたはランダム生成に変更可能だが、まずは固定トークンを使用
# export JUPYTER_TOKEN="secure-token-here"

docker compose up -d
