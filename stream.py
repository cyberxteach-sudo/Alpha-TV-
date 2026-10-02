import json
import subprocess
import time
import os

playlist_file = "playlist.json"
user_agent = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"

# Logo & Text Assets
logo_left_path = "logo.png"    # Left Logo
logo_right_path = "logo1.png"  # Right Logo
notice_file = "notice.txt"
font_path = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"

# HLS Output Directory Isolation
output_dir = "hls"
os.makedirs(output_dir, exist_ok=True)

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
        print(f"\n[+] Streaming Movie {idx+1}/{len(urls)}...")
        print(f"[*] URL: {url}")
        
        # Dual Logo + Marquee Filter Complex
        # Left Logo: scale=200, y=0 (top edge)
        # Right Logo: scale=240, y=10
        filter_complex = (
            f"[1:v]scale=200:-1[logo_left];"
            f"[2:v]scale=240:-1[logo_right];"
            f"[0:v][logo_left]overlay=20:0[v1];"
            f"[v1][logo_right]overlay=main_w-overlay_w-20:10[v2];"
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
            os.path.join(output_dir, 'live.m3u8')
        ]
        
        try:
            subprocess.run(ffmpeg_cmd)
        except Exception as e:
            print(f"[-] Error on Movie {idx+1}: {e}")
            time.sleep(2)
          
