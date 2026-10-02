import json
import subprocess
import time
import os

playlist_file = "playlist.json"

user_agent = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"
logo_path = "logo.png"

channel_name = "ALPHA TV"

# ঠিক ২০ শব্দের স্ক্রোলিং নোটিশ
notice_text = "Welcome to Alpha TV! Streaming non-stop HD movies 24/7. Join our official Telegram channel for updates and requests: \\@cyberxteech"
font_path = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"

while True:
    if os.path.exists(playlist_file):
        with open(playlist_file, "r") as f:
            urls = json.load(f)
    else:
        urls = []

    if not urls:
        print("[-] No URLs found in playlist.json. Retrying in 10 seconds...")
        time.sleep(10)
        continue

    for idx, url in enumerate(urls):
        print(f"\n[+] Streaming Movie {idx+1}/{len(urls)} with 20-word Marquee...")
        print(f"[*] URL: {url}")
        
        filter_complex = (
            f"[1:v]scale=120:-1[logo];"
            f"[0:v][logo]overlay=main_w-overlay_w-20:20[v1];"
            f"[v1]drawtext=fontfile='{font_path}':text='{channel_name}':fontcolor=white:fontsize=22:"
            f"shadowcolor=black@0.8:shadowx=2:shadowy=2:"
            f"x=main_w-text_w-20:y=110[v2];"
            f"[v2]drawtext=fontfile='{font_path}':text='{notice_text}':fontcolor=cyan:fontsize=28:"
            f"shadowcolor=black@0.9:shadowx=2:shadowy=2:"
            f"x='w-mod(max(t-2\\,0)*140\\,w+text_w)':y=h-th-25[outv]"
        )

        ffmpeg_cmd = [
            'ffmpeg', '-y', '-re',
            '-tls_verify', '0',
            '-headers', user_agent,
            '-i', url,
            '-i', logo_path,
            '-filter_complex', filter_complex,
            '-map', '[outv]',
            '-map', '0:a?',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'hls',
            '-hls_time', '2',
            '-hls_list_size', '10',
            '-hls_flags', 'delete_segments+omit_endlist',
            'live.m3u8'
        ]
        
        try:
            subprocess.run(ffmpeg_cmd)
        except Exception as e:
            print(f"[-] Error on Movie {idx+1}: {e}")
            time.sleep(2)
      
