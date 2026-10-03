FROM python:3.10-slim

# প্রয়োজনীয় প্যাকেজ ও FFmpeg ইনস্টল
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    dpkg \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

# Cloudflared ইনস্টল
RUN wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb \
    && dpkg -i cloudflared-linux-amd64.deb \
    && rm cloudflared-linux-amd64.deb

WORKDIR /app
COPY . /app

# স্থায়ী টোকেন দিয়ে ক্লাউডফ্লেয়ার টানেল চালু করা
CMD python3 server.py & cloudflared tunnel run --token eyJhIjoiNTNkNzcwNDNmNmE1OWMyYzU5YmJkNDYyYTJhOGUyZjEiLCJ0IjoiM2JjNjFiMzEtMjQzZC00NWJmLWJhZGUtOTQ4MTU0MDZiNzg4IiwicyI6IlpXUTFPVFkyT1dVdE9EY3hZUzAwTnpCakxXRmhPREV0WXpBNE9HRTJOMlEzWlRCbCJ9 > tunnel.log 2>&1 & sleep 5 && python3 stream.py
