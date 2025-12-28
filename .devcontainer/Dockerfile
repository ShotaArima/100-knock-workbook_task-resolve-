FROM ghcr.io/astral-sh/uv:bookworm-slim

WORKDIR /workspaces

ENV DEBIAN_FRONTEND=noninteractive

# OSパッケージのインストール（これなら動きます）
RUN apt-get update && \
    apt-get install -y --no-install-recommends git build-essential pkg-config && \
    rm -rf /var/lib/apt/lists/*

# uvの設定（オプション: グローバルにインストールせずプロジェクトごとの仮想環境を優先）
ENV UV_LINK_MODE=copy