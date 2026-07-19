import os
import time
import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# Keyword mapping
keywords = {
 "mtacc": "mtaccmobilelegends.com.txt",
    "garena": "garena_accounts.txt",
    "mobilelegends.com": "ml.txt",
    "garena.com": "garena.txt",
    "sso.garena.com": "sso_garena.txt",
    "authgop.garena.com/universal/oauth": "ghost_link.txt",
    "authgop": "authgop.txt",
    "authgop.garena.com/oauth/login": "elite_access.txt",
    "auth.garena.com/ui/login": "paldo_entry.txt",
    "auth.garena.com/oauth/login": "auth_point.txt",
    "sso.garena.com/universal/login": "uni_link.txt",
    "sso.garena.com/ui/register": "reg_link.txt",
    "100082.connect.garena.com": "100082.txt",
    "mobilelegends.com": "mobilelegends.txt",
    "mtacc.mobilelegends.com": "MTACC.txt",
    "play.mobilelegends.com": "PLAY.ML.txt",
    "m.mobilelegends.com": "ML.M.txt",
    "Codashop.com": "codashop.txt",
    "Valorant": "valorant.txt",
    "Vivamax": "VIV.txt",
    "Paypal": "paypal.txt",
    "Spotify": "spotify.txt",
    "gaslite": "gaslite.txt",
    "riotgames": "riotgames.txt",
    "OnlyFans": "onlyfans.txt",
    "miniclip": "8BALL.txt",
    "clashofclan": "clashofclan.txt",
    "Pornhub": "p.txt",
    "Amazon": "Amazon.txt",
    "100055": "100055.txt",
    "bilibili": "bilibili.txt",
    "Halo": "halo.txt",
    "tiktok": "tiktok.txt",
    "LOL2": "LOL.txt",
    "Honkai": "honkai.txt",
    "FIFA": "fifa.txt",
    "Fortnite": "fortnite.txt",
    "Genshin": "genshin.txt",
    "Apex": "apex.txt",
    "google": "google.txt",
    ".com": ".com.txt",
    "Minecraft": "minecraft.txt",
    "Steam": "steam.txt",
    "EpicGames": "epicgames.txt",
    "playstatiom": "psn.txt",
    "Xbox": "xbox.txt",
    "Twitch": "twitch.txt",
    "Discord": "discord.txt",
    "Snapchat": "snapchat.txt",
    "Tiktok": "tiktok.txt",
    "Twitter": "twitter.txt",
    "Instagram": "instagram.txt",
    "LinkedIn": "linked.txt",
    "uber": "ubereats.txt",
    "SpotifyPremium": "spotifyPrem.txt",
    "HBOMax": "hbomax.txt",
    "Crunchyroll": "crunchyroll.txt",
    "Disney+": "disney.txt",
    "YouTube": "youtube.txt",
    "GoogleDrive": "googledrive.txt",
    "Dropbox": "dropbox.txt",
    "OneDrive": "onedrive.txt",
    "SoundCloud": "soundcloud.txt",
    "Deezer": "deezer.txt",
    "Telegram": "telegram.txt",
    "Signal": "signal.txt",
    "Reddit": "reddit.txt",
    "miniclip": "8ball.txt",
    "WeChat": "wechat.txt",
    "WhatsApp": "whatsapp.txt",
    "Skype": "skype.txt",
    "Zoom": "zoom.txt",
    "Slack": "slack.txt",
    "Pinterest": "pinterest.txt",
    "Ebay": "ebay.txt",
    "Shopee": "shopee.txt",
    "Lazada": "lazada.txt",
    "AliExpress": "aliexpress.txt",
    "Github": "github.txt",
    "Temu": "temu.txt",
    "brawlstar": "brawlstar.txt",
    "Freefire": "freefire.txt",
    "crossfire": "cf.txt",
    "gaslite": "gaslite.txt",
    "100080": "100080.txt",
    "100054": "100054.txt",
    "100072": "100072.txt",
    "Freefire": "freefire.txt",
    "telegram": "tg.txt",
    "roblox": "roblox.txt"
    # [Your full keywords dict here – keep unchanged]
}

input_file = input("📂 Enter the input file name (e.g., Vince.txt): ").strip()
output_folder = "kupallala"
os.makedirs(output_folder, exist_ok=True)

output_files = {
    k: open(os.path.join(output_folder, fname), "w", encoding="utf-8", buffering=65536)
    for k, fname in keywords.items()
}

line_count = defaultdict(int)
start_time = time.time()
start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

lowered_keywords = [(k.lower(), k) for k in keywords]
buffers = defaultdict(list)
buffer_limit = 1000
executor = ThreadPoolExecutor(max_workers=4)

def flush_buffer(key):
    if buffers[key]:
        output_files[key].writelines(buffers[key])
        buffers[key].clear()

def update_status_display(total_lines):
    elapsed = time.time() - start_time
    lines_per_sec = total_lines / elapsed if elapsed > 0 else 0

    print("\033c", end="")  # Clear screen ANSI way
    print("\033[1;36m=== Real-time Keyword Extractor ===\033[0m")
    print(f"\033[93mStarted at:\033[0m {start_date}")
    print(f"\033[93mTotal lines:\033[0m {total_lines}")
    print(f"\033[93mLines/sec:\033[0m {lines_per_sec:.2f}")
    print("\n\033[1;33m>> Keyword Matches:\033[0m")

    for i, (keyword, count) in enumerate(sorted(line_count.items(), key=lambda x: x[1], reverse=True)[:15], 1):
        print(f"  \033[92m{i}. {keyword.upper()} [{keywords[keyword]}] = {count}\033[0m")

try:
    print("\n\033[1;36m🔄 Processing... Writing full matched lines by keyword...\033[0m\n")
    total = 0

    with open(input_file, "r", encoding="utf-8", errors="ignore") as infile:
        for line in infile:
            total += 1
            clean_line = line.strip()
            lower_line = clean_line.lower()

            for key_lower, original_key in lowered_keywords:
                if key_lower in lower_line:
                    buffers[original_key].append(clean_line + "\n")
                    line_count[original_key] += 1

                    if len(buffers[original_key]) >= buffer_limit:
                        executor.submit(flush_buffer, original_key)

            if total % 2000 == 0:
                update_status_display(total)

    # Final buffer flush
    for key in buffers:
        executor.submit(flush_buffer, key)

    executor.shutdown(wait=True)
    update_status_display(total)
    print(f"\n\033[92m✔ Done! {total} lines processed.\033[0m")
    print(f"\033[94mFiles saved in '{output_folder}'\033[0m\n")

except Exception as e:
    print(f"\033[91m[!] Error: {e}\033[0m")

finally:
    for f in output_files.values():
        f.close()