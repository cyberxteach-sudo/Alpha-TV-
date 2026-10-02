FROM python:3.10-slim

# System tools install
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    dpkg \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

# Cloudflared install
RUN wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb \
    && dpkg -i cloudflared-linux-amd64.deb \
    && rm cloudflared-linux-amd64.deb

WORKDIR /app
COPY . /app

# Run Server, Tunnel, and Stream together
CMD python3 server.py & cloudflared tunnel --url http://localhost:8080 > tunnel.log 2>&1 & sleep 5 && python3 stream.py
