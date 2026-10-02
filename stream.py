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

# স্ক্রোলিং নোটিশ টেক্সট (আপনার সুবিধামত পরিবর্তন করুন)
notice_text = "Welcome to Alpha TV Live Stream! Enjoy HD Movies 24/7."

# Ubuntu সার্ভারের ফ্রি ফন্ট পাথ
font_path = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"

while True:
    if not urls:
        print("[-] No URLs found in playlist.json. Retrying in 10 seconds...")
        time.sleep(10)
        continue

    for idx, url in enumerate(urls):
        print(f"\n[+] Streaming Movie {idx+1}/{len(urls)} with Logo & Scrolling Text...")
        print(f"[*] URL: {url}")
        
        # Filter Complex:
        # ১. ডান কোণে লোগো সেটআপ (overlay=main_w-overlay_w-20:20)
        # ২. নিচে কালো স্লাইড ব্যাকগ্রাউন্ডে ডান থেকে বামে স্ক্রোলিং টেক্সট
        filter_complex = (
            f"[1:v]scale=130:-1[logo];"
            f"[0:v][logo]overlay=main_w-overlay_w-20:20[v1];"
            f"[v1]drawtext=fontfile='{font_path}':text='{notice_text}':fontcolor=white:fontsize=28:"
            f"box=1:boxcolor=black@0.6:boxborderw=10:"
            f"x='w-mod(max(t-2\\,0)*150\\,w+text_w)':y=h-th-20[outv]"
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
      
