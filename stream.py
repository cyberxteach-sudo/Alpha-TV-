import json
import subprocess
import time
import os

# playlist.json থেকে গ্লোবাল লিঙ্ক লোড করার লজিক
playlist_file = "playlist.json"

if os.path.exists(playlist_file):
    with open(playlist_file, "r") as f:
        urls = json.load(f)
else:
    print("[-] Error: playlist.json file not found!")
    urls = []

user_agent = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"
logo_path = "logo.png"

while True:
    if not urls:
        print("[-] No URLs found in playlist.json. Retrying in 10 seconds...")
        time.sleep(10)
        continue

    for idx, url in enumerate(urls):
        print(f"\n[+] Streaming Movie {idx+1}/{len(urls)} with Logo...")
        print(f"[*] URL: {url}")
        
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-re',
            '-tls_verify', '0',
            '-headers', user_agent,
            '-i', url,
            '-i', logo_path,
            '-filter_complex', '[1:v]scale=130:-1[logo];[0:v][logo]overlay=20:20',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-c:a', 'copy',
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
      
