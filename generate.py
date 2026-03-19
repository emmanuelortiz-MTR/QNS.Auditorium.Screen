import json
import os
import shutil
import sys
import re

CONFIG_FILE = "config.json"
STATIC_SRC = "static"
OUTPUT_DIR = "output"

def log_error_and_exit(msg):
    print(f"❌ {msg}")
    sys.exit(1)

# ---------- Helper to convert Google Drive link ----------
def google_drive_embed(url):
    patterns = [
        r'/file/d/([^/]+)',
        r'id=([^&]+)',
        r'drive\.google\.com.*?[?&]id=([^&]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return f'https://drive.google.com/file/d/{match.group(1)}/preview'
    return url  # fallback

# ---------- Load config ----------
if not os.path.exists(CONFIG_FILE):
    log_error_and_exit(f"{CONFIG_FILE} not found!")

try:
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
except json.JSONDecodeError as e:
    log_error_and_exit(f"Invalid JSON in {CONFIG_FILE}: {e}")

# ---------- Prepare output ----------
shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Copy static files if the folder exists
if os.path.exists(STATIC_SRC):
    shutil.copytree(STATIC_SRC, os.path.join(OUTPUT_DIR, "static"))
else:
    print("⚠️  Warning: 'static/' folder not found – no media will be copied.")

# ---------- HTML templates (same as before) ----------
INDEX_TEMPLATE = """..."""  # (keep your existing template strings)
STEP_TEMPLATE = """..."""
CONGRATS_TEMPLATE = """..."""

# ---------- Generate index ----------
options_html = ""
for opt in config.get("options", []):
    first_step = f"{opt['id']}_step1.html"
    options_html += f'<a href="{first_step}" class="button">{opt["title"]}</a><br>'

with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
    f.write(INDEX_TEMPLATE.format(options_html=options_html))

# ---------- Generate steps ----------
for opt in config.get("options", []):
    steps = opt.get("steps", [])
    total = len(steps)
    if total == 0:
        print(f"⚠️  Warning: No steps for option '{opt.get('id')}'")

    for i, step in enumerate(steps, start=1):
        # Determine media
        if "video_url" in step:
            embed_url = google_drive_embed(step["video_url"])
            media = f'<iframe src="{embed_url}" allow="autoplay; encrypted-media" allowfullscreen title="{step.get("alt", "Video")}"></iframe>'
        elif "video" in step:
            media = f'<video controls alt="{step.get("alt", "")}"><source src="static/videos/{step["video"]}" type="video/mp4">Your browser does not support the video tag.</video>'
        elif "image" in step:
            media = f'<img src="static/images/{step["image"]}" alt="{step.get("alt", "")}">'
        else:
            media = ""  # no media

        # Navigation
        prev_link = f'<a href="{opt["id"]}_step{i-1}.html" class="button">⬅ Previous</a>' if i > 1 else ""
        if i < total:
            next_link = f'<a href="{opt["id"]}_step{i+1}.html" class="button">Next ➔</a>'
        else:
            next_link = f'<a href="{opt["id"]}_congrats.html" class="button">Finish ➔</a>'

        filename = f"{opt['id']}_step{i}.html"
        page = STEP_TEMPLATE.format(
            option_title=opt["title"],
            step_num=i,
            total_steps=total,
            instruction=step.get("instruction", ""),
            media=media,
            prev_link=prev_link,
            next_link=next_link
        )
        with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
            f.write(page)

    # Congrats page
    congrats_file = f"{opt['id']}_congrats.html"
    with open(os.path.join(OUTPUT_DIR, congrats_file), "w") as f:
        f.write(CONGRATS_TEMPLATE.format(message=opt["title"].lower()))

print("✅ Site generated successfully!")
