import json
import os
import shutil
import re
from pathlib import Path

# ---------- Configuration ----------
CONFIG_FILE = "config.json"
STATIC_SRC = "static"
OUTPUT_DIR = "output"
TEMPLATES_DIR = "templates"   # optional

# ---------- Helper to convert Google Drive share link to embed URL ----------
def google_drive_embed(url):
    # Extract file ID from various Google Drive URL formats
    patterns = [
        r'/file/d/([^/]+)',          # /file/d/1ABCxyz123
        r'id=([^&]+)',                # ?id=1ABCxyz123
        r'drive\.google\.com.*?[?&]id=([^&]+)'  # other variations
    ]
    file_id = None
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            file_id = match.group(1)
            break
    if file_id:
        return f'https://drive.google.com/file/d/{file_id}/preview'
    else:
        # Not a Google Drive link – return as-is (risky, but user can embed anything)
        return url

# ---------- Load config ----------
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

# ---------- Prepare output ----------
shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Copy static files (if any)
if os.path.exists(STATIC_SRC):
    shutil.copytree(STATIC_SRC, os.path.join(OUTPUT_DIR, "static"))

# ---------- HTML templates (same as before, but iframe style added) ----------
INDEX_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projector Guide</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; }}
        .button {{ display: inline-block; padding: 1rem 2rem; margin: 1rem 0; background: #007bff; color: white; text-decoration: none; border-radius: 8px; }}
        img, video, iframe {{ max-width: 100%; height: auto; margin: 1rem 0; }}
        iframe {{ width: 100%; height: 340px; border: none; }}
        .nav {{ margin-top: 2rem; }}
        .nav a {{ margin-right: 1rem; }}
    </style>
</head>
<body>
    <h1>So you want to operate the Auditorium Main Projector?</h1>
    {options_html}
</body>
</html>
"""

STEP_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Step {step_num} of {total_steps} – {option_title}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; }}
        .button {{ display: inline-block; padding: 1rem 2rem; margin: 1rem 0; background: #007bff; color: white; text-decoration: none; border-radius: 8px; }}
        img, video, iframe {{ max-width: 100%; height: auto; margin: 1rem 0; }}
        iframe {{ width: 100%; height: 340px; border: none; }}
        .nav {{ margin-top: 2rem; }}
        .nav a {{ margin-right: 1rem; }}
    </style>
</head>
<body>
    <h1>{option_title}</h1>
    <p><strong>Step {step_num} of {total_steps}</strong></p>
    <p>{instruction}</p>
    {media}
    <div class="nav">
        {prev_link}
        {next_link}
        <a href="index.html">🏠 Home</a>
    </div>
</body>
</html>
"""

CONGRATS_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congratulations!</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; text-align: center; }}
        .button {{ display: inline-block; padding: 1rem 2rem; margin: 1rem 0; background: #28a745; color: white; text-decoration: none; border-radius: 8px; }}
    </style>
</head>
<body>
    <h1>🎉 Good job! 🎉</h1>
    <p>You have successfully {message}.</p>
    <a href="index.html" class="button">Start another task</a>
</body>
</html>
"""

# ---------- Generate index ----------
options_html = ""
for opt in config["options"]:
    first_step = f"{opt['id']}_step1.html"
    options_html += f'<a href="{first_step}" class="button">{opt["title"]}</a><br>'

with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
    f.write(INDEX_TEMPLATE.format(options_html=options_html))

# ---------- Generate steps for each option ----------
for opt in config["options"]:
    steps = opt["steps"]
    total = len(steps)

    for i, step in enumerate(steps, start=1):
        # Determine media type and generate appropriate HTML
        if "video_url" in step:
            embed_url = google_drive_embed(step["video_url"])
            media = f'<iframe src="{embed_url}" allow="autoplay; encrypted-media" allowfullscreen title="{step.get("alt", "Video")}"></iframe>'
        elif "video" in step:
            media = f'<video controls alt="{step.get("alt", "")}"><source src="static/videos/{step["video"]}" type="video/mp4">Your browser does not support the video tag.</video>'
        else:
            media = f'<img src="static/images/{step["image"]}" alt="{step.get("alt", "")}">'

        # Previous / Next links
        prev_link = f'<a href="{opt["id"]}_step{i-1}.html" class="button">⬅ Previous</a>' if i > 1 else ""
        next_link = ""
        if i < total:
            next_link = f'<a href="{opt["id"]}_step{i+1}.html" class="button">Next ➔</a>'
        else:
            next_link = f'<a href="{opt["id"]}_congrats.html" class="button">Finish ➔</a>'

        filename = f"{opt['id']}_step{i}.html"
        page = STEP_TEMPLATE.format(
            option_title=opt["title"],
            step_num=i,
            total_steps=total,
            instruction=step["instruction"],
            media=media,
            prev_link=prev_link,
            next_link=next_link
        )
        with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
            f.write(page)

    # Congratulations page for this option
    congrats_file = f"{opt['id']}_congrats.html"
    congrats_html = CONGRATS_TEMPLATE.format(
        message=opt["title"].lower()
    )
    with open(os.path.join(OUTPUT_DIR, congrats_file), "w") as f:
        f.write(congrats_html)

print(f"✅ Site generated in '{OUTPUT_DIR}/'")
