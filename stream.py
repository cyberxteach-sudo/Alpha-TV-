import subprocess
import time

urls = [
    "https://ftp.ctgfun.com/English/2073.2024.1080p.WEBRip.x264%20%5BDDN%5D/2073.2024.1080p.WEBRip.x264%20%5BDDN%5D.mp4",
    "https://ftp.ctgfun.com/English/28.Years.Later.2025.1080p.WEBRip.x264%20%5BDDN%5D/28.Years.Later.2025.1080p.WEBRip.x264%20%5BDDN%5D.mp4",
    "https://ftp.ctgfun.com/English/28.Years.Later.The.Bone.Temple.2026.1080p.WEBRip.x264%20%5BDDN%5D/28.Years.Later.The.Bone.Temple.2026.1080p.WEBRip.x264%20%5BDDN%5D.mp4.mp4",
    "https://ftp.ctgfun.com/English/72%20Hours%20%282026%29%201080p%20WEBRip%20x264%20ESub%20%5BDDN%5D/72%20Hours%20%282026%29%201080p%20WEBRip%20x264%20ESub%20%5BDDN%5D.mp4",
    "https://ftp.ctgfun.com/English/A%20Great%20Awakening%20%282026%29%201080p%20WEBRip%20x264%20ESub%20%5BDDN%5D/A%20Great%20Awakening%20%282026%29%201080p%20WEBRip%20x264%20ESub%20%5BDDN%5D.mp4"
]

user_agent = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\nReferer: https://ftp.ctgfun.com/\r\n"
logo_path = "logo.png"

while True:
    for idx, url in enumerate(urls):
        print(f"\n[+] Streaming Movie {idx+1}/{len(urls)} with Logo...")
        
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
