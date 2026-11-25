#!/usr/bin/env python3
"""
Video Renderer for "The 10-Second AI Data Cleaner"
Creates a slideshow-style tutorial video using PIL + ffmpeg.
"""

from PIL import Image, ImageDraw, ImageFont
import subprocess
from pathlib import Path

WORKDIR = Path("/Users/sayandas/Projects/ai-data-cleaner-video")
OUTPUT_VIDEO = WORKDIR / "ai_data_cleaner_tutorial.mp4"
THUMBNAIL = WORKDIR / "thumbnail.png"

WIDTH, HEIGHT = 1920, 1080
FPS = 30

BG_DARK = "#0d1117"
BG_MID = "#161b22"
FG_BLUE = "#58a6ff"
FG_RED = "#f97583"
FG_GREEN = "#7ee787"
FG_PURPLE = "#d2a8ff"
FG_ORANGE = "#ffa657"
FG_YELLOW = "#d29922"
FG_WHITE = "#e6edf3"
FG_GRAY = "#8b949e"

SLIDES = [
    {
        "name": "title",
        "lines": [
            ("The 10-Second AI Data Cleaner", FG_BLUE, 72, True),
            ("Stop Fixing CSVs Manually", FG_WHITE, 48, False),
            ("", FG_WHITE, 24, False),
            ("Inspect → Fix → Verify Pipeline", FG_GREEN, 40, True),
            ("Python + Pandas + LLM Patterns", FG_GRAY, 32, False),
        ],
        "bg": BG_DARK,
        "duration": 6
    },
    {
        "name": "hook",
        "lines": [
            ("THE PROBLEM:", FG_RED, 56, True),
            ("40-row customer export", FG_WHITE, 40, False),
            ("", FG_WHITE, 20, False),
            ("• 20 country variants (US, USA, United States...)", FG_ORANGE, 36, False),
            ("• Mixed dates: 2023-01-15, 2023/03/10, -", FG_ORANGE, 36, False),
            ("• Spend: 1250.50, 890.00, -, N/A", FG_ORANGE, 36, False),
            ("• 20 duplicate rows silently corrupting totals", FG_ORANGE, 36, False),
            ("", FG_WHITE, 20, False),
            ("4 hours of VLOOKUPs vs 10 seconds of code", FG_GREEN, 44, True),
        ],
        "bg": BG_MID,
        "duration": 8
    },
    {
        "name": "framework",
        "lines": [
            ("THE 3-TIER PIPELINE:", FG_BLUE, 56, True),
            ("", FG_WHITE, 20, False),
            ("1️⃣  PARSE     →  Load raw, detect dtypes, flag anomalies", FG_WHITE, 38, False),
            ("2️⃣  NORMALIZE →  LLM-assisted category mapping", FG_WHITE, 38, False),
            ("   (20 country variants → 6 canonical)", FG_GRAY, 32, False),
            ("3️⃣  VALIDATE  →  Pandas schema guards, verification log", FG_WHITE, 38, False),
            ("   human review", FG_WHITE, 38, False),
        ],
        "bg": BG_MID,
        "duration": 8
    },
    {
        "name": "code_1",
        "lines": [
            ("STEP 2: DUPLICATE AUDIT", FG_PURPLE, 52, True),
            ("", FG_WHITE, 16, False),
            ("dup_mask = df.duplicated(subset=['customer_id'], keep=False)", FG_GREEN, 30, False),
            ("dup_count = dup_mask.sum()", FG_GREEN, 30, False),
            ("df = df.drop_duplicates(subset=['customer_id'], keep='first')", FG_GREEN, 30, False),
            ("", FG_WHITE, 16, False),
            ("✓ Removed 20 duplicate rows", FG_GREEN, 36, True),
        ],
        "bg": BG_DARK,
        "duration": 7
    },
    {
        "name": "code_2",
        "lines": [
            ("STEP 3: SPEND CLEANUP (don't zero financials!)", FG_PURPLE, 52, True),
            ("", FG_WHITE, 16, False),
            ("df['total_spend'] = df['total_spend'].replace({", FG_GREEN, 30, False),
            ("    '-': np.nan, 'N/A': np.nan})", FG_GREEN, 30, False),
            ("df['total_spend'] = pd.to_numeric(df['total_spend'],", FG_GREEN, 30, False),
            ("    errors='coerce')", FG_GREEN, 30, False),
            ("", FG_WHITE, 16, False),
            ("✓ 7 dashes → NaN (preserved for review)", FG_GREEN, 36, True),
        ],
        "bg": BG_DARK,
        "duration": 7
    },
    {
        "name": "code_3",
        "lines": [
            ("STEP 4: MIXED DATE PARSING", FG_PURPLE, 52, True),
            ("", FG_WHITE, 16, False),
            ("df[col] = df[col].replace('-', np.nan)", FG_GREEN, 30, False),
            ("df[col] = pd.to_datetime(df[col],", FG_GREEN, 30, False),
            ("    format='mixed', dayfirst=False,", FG_GREEN, 30, False),
            ("    errors='coerce')", FG_GREEN, 30, False),
            ("", FG_WHITE, 16, False),
            ("✓ Handles YYYY-MM-DD, YYYY/MM/DD, -", FG_GREEN, 36, True),
        ],
        "bg": BG_DARK,
        "duration": 7
    },
    {
        "name": "code_4",
        "lines": [
            ("STEP 5: COUNTRY NORMALIZATION", FG_PURPLE, 52, True),
            ("", FG_WHITE, 16, False),
            ("COUNTRY_MAP = {", FG_GREEN, 30, False),
            ("    'usa': 'United States',", FG_GREEN, 30, False),
            ("    'uk': 'United Kingdom',", FG_GREEN, 30, False),
            ("    'deutschland': 'Germany',", FG_GREEN, 30, False),
            ("    ...  # 20 variants → 6 canonical", FG_GRAY, 28, False),
            ("}", FG_GREEN, 30, False),
            ("df['country_clean'] = df['country'].str.lower().map(COUNTRY_MAP)", FG_GREEN, 30, False),
            ("", FG_WHITE, 16, False),
            ("✓ 20 variants → 6 clean categories", FG_GREEN, 36, True),
        ],
        "bg": BG_DARK,
        "duration": 7
    },
    {
        "name": "edge_cases",
        "lines": [
            ("EDGE CASES & HALLUCINATION GUARDS", FG_ORANGE, 52, True),
            ("", FG_WHITE, 20, False),
            ("🛡️  Pydantic / JSON Schema validation", FG_WHITE, 38, False),
            ("🛡️  Never zero financial nulls → keep NaN", FG_WHITE, 38, False),
            ("🛡️  Preserve unmatched categories for review", FG_WHITE, 38, False),
            ("🛡️  Structured cleaning log (Markdown)", FG_WHITE, 38, False),
            ("🛡️  Row-count sanity checks", FG_WHITE, 38, False),
            ("", FG_WHITE, 20, False),
            ("Human-in-the-loop = production safety", FG_GREEN, 42, True),
        ],
        "bg": BG_MID,
        "duration": 8
    },
    {
        "name": "results",
        "lines": [
            ("RESULTS: 40 rows → 20 clean rows", FG_GREEN, 56, True),
            ("", FG_WHITE, 20, False),
            ("✅ 20 duplicate IDs removed", FG_GREEN, 38, False),
            ("✅ 7 spend dashes → NaN (not zero!)", FG_GREEN, 38, False),
            ("✅ 20 mixed dates parsed to ISO format", FG_GREEN, 38, False),
            ("✅ 20 country variants → 6 canonical", FG_GREEN, 38, False),
            ("✅ 20 phones normalized to E.164", FG_GREEN, 38, False),
            ("✅ Verification log generated", FG_GREEN, 38, False),
            ("", FG_WHITE, 20, False),
            ("Ready for next month's batch 🔁", FG_BLUE, 42, True),
        ],
        "bg": BG_MID,
        "duration": 8
    },
    {
        "name": "cta",
        "lines": [
            ("GET THE CODE:", FG_BLUE, 64, True),
            ("", FG_WHITE, 30, False),
            ("github.com/TaskToFlow/ai-data-cleaner", FG_WHITE, 44, False),
            ("", FG_WHITE, 30, False),
            ("• cleaner.py (full pipeline)", FG_GRAY, 36, False),
            ("• customers_messy.csv (sample data)", FG_GRAY, 36, False),
            ("• cleaning_report.md (auto-generated)", FG_GRAY, 36, False),
            ("", FG_WHITE, 30, False),
            ("What would YOU clean next?", FG_ORANGE, 44, True),
            ("", FG_WHITE, 20, False),
            ("Task to Flow  •  Practical AI Workflows", FG_GRAY, 32, False),
        ],
        "bg": BG_DARK,
        "duration": 8
    },
]


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_font(size, bold=False):
    font_paths = [
        "/System/Library/Fonts/Monaco.dfont",
        "/System/Library/Fonts/Menlo.ttc",
        "/Library/Fonts/Monaco.dfont",
        "/System/Library/Fonts/Courier New.ttf",
    ]
    for path in font_paths:
        try:
            if bold:
                return ImageFont.truetype(path, size, index=1 if path.endswith('.ttc') else 0)
            return ImageFont.truetype(path, size, index=0 if path.endswith('.ttc') else 0)
        except Exception:
            continue
    return ImageFont.load_default()


def render_slide(slide, output_path):
    img = Image.new('RGB', (WIDTH, HEIGHT), slide['bg'])
    draw = ImageDraw.Draw(img)

    line_heights = []
    for text, color, size, bold in slide['lines']:
        font = get_font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        line_heights.append(bbox[3] - bbox[1] + 10)

    total_height = sum(line_heights)
    start_y = (HEIGHT - total_height) // 2

    y = start_y
    for (text, color, size, bold), lh in zip(slide['lines'], line_heights):
        if not text:
            y += lh
            continue
        font = get_font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, y), text, font=font, fill=color)
        y += lh

    img.save(output_path)
    return True


def create_video():
    print("🎬 Rendering slides with PIL...")

    slide_images = []
    for i, slide in enumerate(SLIDES):
        img_path = WORKDIR / f"slide_{i:02d}_{slide['name']}.png"
        print(f"  Slide {i+1}/{len(SLIDES)}: {slide['name']} ({slide['duration']}s)")

        if render_slide(slide, img_path):
            slide_images.append((img_path, slide['duration']))
        else:
            print(f"    ⚠️ Failed to render {slide['name']}")

    if not slide_images:
        print("❌ No slides rendered")
        return False

    print(f"\n🎞️  Stitching {len(slide_images)} slides into video...")

    concat_file = WORKDIR / "concat.txt"
    with open(concat_file, "w") as f:
        for img_path, duration in slide_images:
            f.write(f"file '{img_path}'\nduration {duration}\n")
        f.write(f"file '{slide_images[-1][0]}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-vf", f"fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-pix_fmt", "yuv420p",
        str(OUTPUT_VIDEO)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Video created: {OUTPUT_VIDEO}")
        dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                   "-of", "default=noprint_wrappers=1:nokey=1", str(OUTPUT_VIDEO)]
        dur_result = subprocess.run(dur_cmd, capture_output=True, text=True)
        if dur_result.returncode == 0:
            print(f"   Duration: {float(dur_result.stdout.strip()):.1f}s")
        return True
    else:
        print(f"❌ Video render failed: {result.stderr}")
        return False


def create_thumbnail():
    print("\n🖼️  Creating thumbnail with PIL...")

    img = Image.new('RGB', (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    left_bg = Image.new('RGB', (WIDTH//2, HEIGHT), "#2d1b1b")
    img.paste(left_bg, (0, 0))

    right_bg = Image.new('RGB', (WIDTH//2, HEIGHT), "#1b2d1b")
    img.paste(right_bg, (WIDTH//2, 0))

    draw.line([(WIDTH//2, 0), (WIDTH//2, HEIGHT)], fill=FG_YELLOW, width=4)

    left_x = 100
    y = 150
    for text, color, size, bold in [
        ("MESSY DATA", FG_RED, 72, True),
        ("", FG_WHITE, 20, False),
        ("country: USA, US, United States...", FG_ORANGE, 32, False),
        ("date: 2023-01-15, 2023/03/10, -", FG_ORANGE, 32, False),
        ("spend: 1250.50, -, N/A", FG_ORANGE, 32, False),
        ("duplicates: 20 rows", FG_RED, 32, False),
    ]:
        if not text:
            y += size + 10
            continue
        font = get_font(size, bold)
        draw.text((left_x, y), text, font=font, fill=color)
        y += size + 15

    right_x = WIDTH//2 + 100
    y = 150
    for text, color, size, bold in [
        ("CLEAN OUTPUT", FG_GREEN, 72, True),
        ("", FG_WHITE, 20, False),
        ("country: United States", FG_GREEN, 32, False),
        ("date: 2023-03-10", FG_GREEN, 32, False),
        ("spend: 1250.50", FG_GREEN, 32, False),
        ("duplicates: 0", FG_GREEN, 32, False),
    ]:
        if not text:
            y += size + 10
            continue
        font = get_font(size, bold)
        draw.text((right_x, y), text, font=font, fill=color)
        y += size + 15

    title_font = get_font(48, True)
    title = "10-Second AI Data Cleaner"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((WIDTH - title_w)//2, HEIGHT - 100), title, font=title_font, fill=FG_YELLOW)

    img.save(THUMBNAIL)
    print(f"✅ Thumbnail created: {THUMBNAIL}")
    return True


if __name__ == "__main__":
    success = create_video()
    create_thumbnail()

    if success:
        print(f"\n🎉 Production complete!")
        print(f"   Video: {OUTPUT_VIDEO}")
        print(f"   Thumbnail: {THUMBNAIL}")
    else:
        print("\n❌ Production failed")
        exit(1)