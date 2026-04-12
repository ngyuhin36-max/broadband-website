"""
YouTube Shorts 影片生成器 V2
最平1000M寬頻排名 - 有圖案 + 語音旁白
"""

import sys, io, os, tempfile, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip
import numpy as np
from gtts import gTTS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
FPS = 24


def get_font(size, bold=False):
    """Get Chinese font."""
    if bold:
        paths = ["C:/Windows/Fonts/msjhbd.ttc", "C:/Windows/Fonts/msyhbd.ttc"]
    else:
        paths = ["C:/Windows/Fonts/msjh.ttc", "C:/Windows/Fonts/msyh.ttc"]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)


def make_tts(text, filename):
    """Generate TTS audio file."""
    tts = gTTS(text=text, lang='yue')
    filepath = os.path.join(tempfile.gettempdir(), filename)
    tts.save(filepath)
    return filepath


def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_icon_wifi(draw, cx, cy, size, color):
    """Draw a WiFi-like icon."""
    for i in range(3):
        r = size - i * (size // 3)
        bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.arc(bbox, start=225, end=315, fill=color, width=max(4, size // 8))
    dot_r = max(4, size // 10)
    draw.ellipse([cx - dot_r, cy - dot_r + size // 4, cx + dot_r, cy + dot_r + size // 4], fill=color)


def draw_icon_dollar(draw, cx, cy, size, color):
    """Draw a dollar sign icon."""
    font = get_font(size)
    draw.text((cx - size // 3, cy - size // 2), "$", fill=color, font=font)


def draw_icon_speed(draw, cx, cy, size, color):
    """Draw a speed gauge icon."""
    bbox = [cx - size, cy - size, cx + size, cy + size]
    draw.arc(bbox, start=180, end=360, fill=color, width=max(4, size // 6))
    # Needle
    angle_rad = math.radians(250)
    nx = cx + int(size * 0.7 * math.cos(angle_rad))
    ny = cy + int(size * 0.7 * math.sin(angle_rad))
    draw.line([(cx, cy), (nx, ny)], fill=color, width=max(3, size // 8))


def draw_icon_star(draw, cx, cy, size, color):
    """Draw a star icon."""
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = size if i % 2 == 0 else size * 0.4
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=color)


def draw_icon_check(draw, cx, cy, size, color):
    """Draw a checkmark icon."""
    draw.line([(cx - size, cy), (cx - size // 3, cy + size * 0.7)], fill=color, width=max(5, size // 4))
    draw.line([(cx - size // 3, cy + size * 0.7), (cx + size, cy - size * 0.5)], fill=color, width=max(5, size // 4))


def draw_icon_crown(draw, cx, cy, size, color):
    """Draw a crown icon."""
    points = [
        (cx - size, cy + size // 2),
        (cx - size, cy - size // 3),
        (cx - size // 2, cy),
        (cx, cy - size // 2),
        (cx + size // 2, cy),
        (cx + size, cy - size // 3),
        (cx + size, cy + size // 2),
    ]
    draw.polygon(points, fill=color)


def draw_price_bar(draw, x, y, width, height, fill_ratio, bar_color, bg_color=(80, 80, 80)):
    """Draw a horizontal progress/price bar."""
    draw.rounded_rectangle([x, y, x + width, y + height], radius=height // 2, fill=bg_color)
    fill_width = int(width * fill_ratio)
    if fill_width > height:
        draw.rounded_rectangle([x, y, x + fill_width, y + height], radius=height // 2, fill=bar_color)


# ========== SLIDE BUILDERS ==========

def build_slide_intro():
    """Slide 1: Eye-catching intro."""
    img = Image.new('RGB', (WIDTH, HEIGHT), (20, 20, 60))
    draw = ImageDraw.Draw(img)

    # Decorative circles
    for i in range(8):
        cx = (i * 200 + 50) % WIDTH
        cy = 200 + (i * 300) % 600
        r = 30 + i * 10
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40 + i * 5, 40 + i * 8, 100 + i * 10))

    # Top badge
    draw_rounded_rect(draw, [290, 350, 790, 430], 40, (255, 70, 70))
    font_badge = get_font(48, bold=True)
    draw.text((340, 358), "2026年最新排名", fill=(255, 255, 255), font=font_badge)

    # Main title
    font_title = get_font(96, bold=True)
    draw.text((140, 500), "香港最平", fill=(255, 255, 255), font=font_title)

    font_title2 = get_font(110, bold=True)
    draw.text((100, 630), "1000M寬頻", fill=(255, 220, 50), font=font_title2)

    font_sub = get_font(80, bold=True)
    draw.text((220, 780), "係邊間？", fill=(255, 255, 255), font=font_sub)

    # Speed icon
    draw_icon_speed(draw, 540, 1050, 120, (255, 220, 50))

    # Bottom text
    font_bottom = get_font(42)
    draw.text((200, 1250), "1000Mbps 光纖入屋月費比較", fill=(180, 180, 220), font=font_bottom)

    # WiFi icons decoration
    draw_icon_wifi(draw, 150, 1500, 50, (100, 130, 230))
    draw_icon_wifi(draw, 930, 1500, 50, (100, 130, 230))

    # Brand
    draw_rounded_rect(draw, [250, 1650, 830, 1730], 20, (102, 126, 234))
    font_brand = get_font(44, bold=True)
    draw.text((290, 1660), "broadbandhk.com 出品", fill=(255, 255, 255), font=font_brand)

    return img


def build_slide_isp(rank, name, name_en, price, color, is_cheapest=False):
    """Build an ISP ranking slide."""
    bg_color = (25, 25, 65) if not is_cheapest else (15, 60, 30)
    img = Image.new('RGB', (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)

    # Rank badge
    badge_color = (255, 70, 70) if not is_cheapest else (255, 200, 0)
    badge_text_color = (255, 255, 255) if not is_cheapest else (30, 30, 30)
    draw.ellipse([400, 120, 680, 400], fill=badge_color)
    font_rank_num = get_font(140, bold=True)
    # Center the rank number
    rank_text = str(rank)
    bbox = font_rank_num.getbbox(rank_text)
    rx = 540 - (bbox[2] - bbox[0]) // 2
    ry = 190
    draw.text((rx, ry), rank_text, fill=badge_text_color, font=font_rank_num)

    # Rank label
    font_rank_label = get_font(36)
    label = "最平！" if is_cheapest else f"第{rank}名"
    lbbox = font_rank_label.getbbox(label)
    lx = 540 - (lbbox[2] - lbbox[0]) // 2
    draw.text((lx, 340), label, fill=badge_text_color, font=font_rank_label)

    if is_cheapest:
        draw_icon_crown(draw, 540, 90, 50, (255, 200, 0))

    # ISP name
    font_name = get_font(88, bold=True)
    nbbox = font_name.getbbox(name)
    nx = (WIDTH - (nbbox[2] - nbbox[0])) // 2
    draw.text((nx, 480), name, fill=(255, 255, 255), font=font_name)

    # ISP English name
    font_name_en = get_font(40)
    enbbox = font_name_en.getbbox(name_en)
    enx = (WIDTH - (enbbox[2] - enbbox[0])) // 2
    draw.text((enx, 590), name_en, fill=(150, 150, 200), font=font_name_en)

    # Divider line
    draw.line([(200, 670), (880, 670)], fill=(60, 60, 120), width=2)

    # Speed label
    font_speed_label = get_font(44)
    draw.text((180, 720), "速度", fill=(150, 150, 200), font=font_speed_label)
    font_speed = get_font(56, bold=True)
    draw.text((180, 780), "1000Mbps 光纖入屋", fill=(255, 255, 255), font=font_speed)

    # Speed icon
    draw_icon_speed(draw, 900, 760, 50, color)

    # Price section
    draw_rounded_rect(draw, [100, 900, 980, 1150], 30, (40, 40, 90) if not is_cheapest else (30, 80, 40))

    font_price_label = get_font(44)
    draw.text((180, 930), "每月月費", fill=(180, 180, 220), font=font_price_label)

    font_dollar = get_font(36)
    draw.text((180, 1010), "HK$", fill=(180, 180, 220), font=font_dollar)

    price_color = (255, 100, 100) if not is_cheapest else (100, 255, 100)
    font_price = get_font(120, bold=True)
    draw.text((310, 960), price, fill=price_color, font=font_price)

    font_per = get_font(40)
    draw.text((700, 1040), "起/月", fill=(180, 180, 220), font=font_per)

    # Price bar comparison
    prices_map = {"$128": 0.5, "$148": 0.6, "$158": 0.65, "$168": 0.7, "$198": 0.85}
    fill = prices_map.get(price, 0.5)
    draw_price_bar(draw, 150, 1220, 780, 30, fill, color)
    font_bar_label = get_font(30)
    draw.text((150, 1260), "平", fill=(100, 255, 100), font=font_bar_label)
    draw.text((870, 1260), "貴", fill=(255, 100, 100), font=font_bar_label)

    # Features
    features = ["光纖入屋", "免安裝費", "24個月合約"]
    font_feat = get_font(38)
    for i, feat in enumerate(features):
        y = 1340 + i * 60
        draw_icon_check(draw, 200, y + 18, 15, (100, 255, 100))
        draw.text((240, y), feat, fill=(200, 200, 230), font=font_feat)

    # Bottom CTA
    if is_cheapest:
        draw_rounded_rect(draw, [150, 1600, 930, 1700], 30, (255, 200, 0))
        font_cta = get_font(48, bold=True)
        draw.text((220, 1618), "全港最平 1000M！", fill=(30, 30, 30), font=font_cta)
    else:
        draw_rounded_rect(draw, [250, 1620, 830, 1700], 25, (60, 60, 120))
        font_cta = get_font(40)
        draw.text((340, 1635), "繼續睇排名 ▶", fill=(180, 180, 220), font=font_cta)

    # WiFi decoration
    draw_icon_wifi(draw, 100, 150, 40, (50, 50, 100))
    draw_icon_wifi(draw, 980, 150, 40, (50, 50, 100))

    return img


def build_slide_summary():
    """Summary comparison slide."""
    img = Image.new('RGB', (WIDTH, HEIGHT), (20, 20, 60))
    draw = ImageDraw.Draw(img)

    # Title
    font_title = get_font(72, bold=True)
    draw.text((200, 100), "1000M 月費排名", fill=(255, 255, 255), font=font_title)

    # Divider
    draw.line([(100, 200), (980, 200)], fill=(60, 60, 120), width=2)

    # ISP list with bars
    isps = [
        ("1", "中國移動", "$128起", (0, 200, 80), 0.45),
        ("2", "有線寬頻", "$148起", (0, 150, 200), 0.55),
        ("3", "和記寬頻", "$158起", (100, 100, 200), 0.60),
        ("4", "香港寬頻", "$168起", (200, 100, 50), 0.65),
        ("5", "網上行",   "$198起", (180, 50, 50), 0.80),
    ]

    font_num = get_font(52, bold=True)
    font_name = get_font(48, bold=True)
    font_price = get_font(44, bold=True)

    for i, (num, name, price, color, ratio) in enumerate(isps):
        y = 280 + i * 230

        # Rank circle
        circle_color = (255, 200, 0) if i == 0 else (80, 80, 140)
        draw.ellipse([80, y, 160, y + 80], fill=circle_color)
        num_color = (30, 30, 30) if i == 0 else (255, 255, 255)
        draw.text((105, y + 8), num, fill=num_color, font=font_num)

        # Name
        draw.text((190, y + 10), name, fill=(255, 255, 255), font=font_name)

        # Price
        p_color = (100, 255, 100) if i == 0 else (255, 180, 180)
        draw.text((680, y + 10), price, fill=p_color, font=font_price)

        # Bar
        draw_price_bar(draw, 190, y + 80, 760, 24, ratio, color)

        if i == 0:
            draw_icon_crown(draw, 60, y + 20, 25, (255, 200, 0))
            draw_icon_star(draw, 950, y + 40, 20, (255, 200, 0))

    # Bottom note
    font_note = get_font(32)
    draw.text((150, 1480), "* 以上價格為大約參考，實際以供應商報價為準", fill=(120, 120, 160), font=font_note)

    # CTA
    draw_rounded_rect(draw, [150, 1580, 930, 1680], 30, (102, 126, 234))
    font_cta = get_font(48, bold=True)
    draw.text((220, 1598), "想知邊間最啱你？", fill=(255, 255, 255), font=font_cta)

    draw_rounded_rect(draw, [150, 1720, 930, 1820], 30, (37, 211, 102))
    font_wa = get_font(44, bold=True)
    draw.text((200, 1740), "WhatsApp 免費格價查詢", fill=(255, 255, 255), font=font_wa)

    return img


def build_slide_outro():
    """Final CTA slide."""
    img = Image.new('RGB', (WIDTH, HEIGHT), (102, 126, 234))
    draw = ImageDraw.Draw(img)

    # Decorative elements
    for i in range(6):
        cx = 100 + i * 180
        draw.ellipse([cx - 60, 100, cx + 60, 220], fill=(120, 145, 240))
    for i in range(6):
        cx = 100 + i * 180
        draw.ellipse([cx - 40, 1700, cx + 40, 1780], fill=(120, 145, 240))

    # WiFi icon big
    draw_icon_wifi(draw, 540, 500, 150, (255, 255, 255))

    # Brand
    font_brand = get_font(80, bold=True)
    draw.text((110, 720), "broadbandhk.com", fill=(255, 255, 255), font=font_brand)

    # Tagline
    font_tag = get_font(52)
    draw.text((180, 860), "免費寬頻格價比較平台", fill=(220, 230, 255), font=font_tag)

    # Divider
    draw.line([(200, 960), (880, 960)], fill=(150, 170, 255), width=2)

    # Features
    features = [
        "比較全港5大寬頻供應商",
        "免費格價 無隱藏收費",
        "專人跟進 即日安排",
    ]
    font_feat = get_font(44)
    for i, f in enumerate(features):
        y = 1020 + i * 70
        draw_icon_check(draw, 170, y + 20, 18, (255, 255, 255))
        draw.text((220, y), f, fill=(255, 255, 255), font=font_feat)

    # WhatsApp CTA
    draw_rounded_rect(draw, [150, 1300, 930, 1420], 35, (37, 211, 102))
    font_wa = get_font(52, bold=True)
    draw.text((200, 1325), "WhatsApp: 5228 7541", fill=(255, 255, 255), font=font_wa)

    # Call CTA
    draw_rounded_rect(draw, [150, 1480, 930, 1600], 35, (255, 70, 70))
    font_call = get_font(48, bold=True)
    draw.text((230, 1500), "致電查詢: 2330 8372", fill=(255, 255, 255), font=font_call)

    return img


def main():
    print("=== 生成影片：最平1000M寬頻排名 ===\n")

    # Step 1: Generate TTS audio for each slide
    print("Step 1: 生成語音旁白...")
    narrations = [
        ("n01.mp3", "香港最平嘅一千兆寬頻係邊間？等我幫你排名！"),
        ("n02.mp3", "第五名，網上行，月費大約一百九十八蚊起"),
        ("n03.mp3", "第四名，香港寬頻，月費大約一百六十八蚊起"),
        ("n04.mp3", "第三名，和記寬頻，月費大約一百五十八蚊起"),
        ("n05.mp3", "第二名，有線寬頻，月費大約一百四十八蚊起"),
        ("n06.mp3", "第一名！最平！中國移動，月費大約一百二十八蚊起！"),
        ("n07.mp3", "以上就係五大供應商嘅排名，想知邊間最啱你，即刻上 broadbandhk.com 免費格價！"),
        ("n08.mp3", "broadbandhk.com，免費寬頻格價比較，WhatsApp 五二二八七五四一，歡迎隨時查詢！"),
    ]

    audio_files = []
    for filename, text in narrations:
        filepath = make_tts(text, filename)
        audio_files.append(filepath)
        print(f"  {filename} OK")

    # Step 2: Generate slide images
    print("\nStep 2: 生成圖像...")

    slides_data = [
        ("intro", build_slide_intro()),
        ("isp5", build_slide_isp(5, "網上行", "Netvigator / PCCW", "$198", (180, 50, 50))),
        ("isp4", build_slide_isp(4, "香港寬頻", "HKBN", "$168", (200, 100, 50))),
        ("isp3", build_slide_isp(3, "和記寬頻", "HGC", "$158", (100, 100, 200))),
        ("isp2", build_slide_isp(2, "有線寬頻", "i-Cable", "$148", (0, 150, 200))),
        ("isp1", build_slide_isp(1, "中國移動", "China Mobile", "$128", (0, 200, 80), is_cheapest=True)),
        ("summary", build_slide_summary()),
        ("outro", build_slide_outro()),
    ]

    for name, img in slides_data:
        print(f"  {name} OK ({img.size})")

    # Step 3: Combine into video with audio
    print("\nStep 3: 合併影片...")

    clips = []
    for i, ((name, img), audio_path) in enumerate(zip(slides_data, audio_files)):
        # Get audio duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration + 0.5  # Add 0.5s padding

        # Create image clip
        img_array = np.array(img)
        video_clip = ImageClip(img_array).with_duration(duration)

        # Add audio
        video_clip = video_clip.with_audio(audio_clip)
        clips.append(video_clip)
        print(f"  Slide {i+1}: {duration:.1f}s")

    print("\nStep 4: Rendering...")
    final = concatenate_videoclips(clips, method="compose")
    total_duration = sum(c.duration for c in clips)
    print(f"  Total duration: {total_duration:.1f}s")

    output_path = os.path.join(OUTPUT_DIR, "最平1000M寬頻排名_廣東話版.mp4")
    final.write_videofile(
        output_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        preset='ultrafast',
        threads=4,
    )

    final.close()
    for c in clips:
        c.close()

    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n=== 完成！===")
    print(f"影片: {output_path}")
    print(f"大小: {file_size:.1f} MB")
    print(f"時長: {total_duration:.1f} 秒")


if __name__ == "__main__":
    main()
