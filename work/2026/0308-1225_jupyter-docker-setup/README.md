# Jupyter Docker Setup with Tailscale

## 概要
Macホスト環境を汚さずに、Dockerコンテナ内でJupyter Notebookを動作させ、Tailscale経由で外部アクセスを可能にする。

## 構成
- **Jupyter**: jupyter/datascience-notebook
- **Tailscale**: tailscale/tailscale (Sidecar mode)
- **Persistence**: `./notebooks` をマウント
