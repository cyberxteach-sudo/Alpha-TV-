import json
import subprocess
import time
import os

playlist_file = "playlist.json"

user_agent = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"

# দুটি লোগোর পাথ
logo_left_path = "logo.png"    # বাম পাশের লোগো
logo_right_path = "logo1.png"  # ডান পাশের লোগো

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
        print(f"\n[+] Streaming Movie {idx+1}/{len(urls)} with Dual Logos...")
        print(f"[*] URL: {url}")
        
        # Dual Logo + Marquee Filter Complex:
        # [1:v] = logo.png (Left)
        # [2:v] = logo1.png (Right)
        filter_complex = (
            f"[1:v]scale=110:-1[logo_left];"
            f"[2:v]scale=110:-1[logo_right];"
            f"[0:v][logo_left]overlay=20:20[v1];"
            f"[v1][logo_right]overlay=main_w-overlay_w-20:20[v2];"
            f"[v2]drawtext=fontfile='{font_path}':textfile='{notice_file}':fontcolor=cyan:fontsize=26:"
            f"shadowcolor=black@0.9:shadowx=2:shadowy=2:"
            f"x='w-mod(max(t-2\\,0)*140\\,w+text_w)':y=h-th-25[outv]"
        )

        ffmpeg_cmd = [
            'ffmpeg', '-y', '-re',
            '-tls_verify', '0',
            '-headers', user_agent,
            '-i', url,
            '-i', logo_left_path,
            '-i', logo_right_path,
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
      
