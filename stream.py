import json
import subprocess
import time
import os

playlist_file = "playlist.json"

user_agent = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"
logo_path = "logo.png"

channel_name = "ALPHA TV"
notice_file = "notice.txt"
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
        print(f"\n[+] Streaming Movie {idx+1}/{len(urls)} with Notice File...")
        print(f"[*] URL: {url}")
        
        # textfile অপশন ব্যবহারের ফলে @, (), & সহ যেকোনো স্পেশাল ক্যারেক্টার মসৃণভাবে শো করবে
        filter_complex = (
            f"[1:v]scale=110:-1[logo];"
            f"[0:v][logo]overlay=main_w-overlay_w-20:20[v1];"
            f"[v1]drawtext=fontfile='{font_path}':text='{channel_name}':fontcolor=yellow:fontsize=32:"
            f"shadowcolor=black@0.9:shadowx=2:shadowy=2:"
            f"x=30:y=30[v2];"
            f"[v2]drawtext=fontfile='{font_path}':textfile='{notice_file}':fontcolor=cyan:fontsize=26:"
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
