"""
YouTube Shorts 影片生成器
生成寬頻相關的短影片（1080x1920, 60秒內）
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from moviepy import (
    TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import tempfile

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Video settings (YouTube Shorts = 9:16)
WIDTH = 1080
HEIGHT = 1920
FPS = 24


def find_chinese_font():
    """Find a Chinese-capable font on Windows."""
    font_paths = [
        "C:/Windows/Fonts/msjh.ttc",      # Microsoft JhengHei
        "C:/Windows/Fonts/msjhbd.ttc",     # Microsoft JhengHei Bold
        "C:/Windows/Fonts/msyh.ttc",       # Microsoft YaHei
        "C:/Windows/Fonts/msyhbd.ttc",     # Microsoft YaHei Bold
        "C:/Windows/Fonts/mingliu.ttc",    # MingLiU
        "C:/Windows/Fonts/simsun.ttc",     # SimSun
        "C:/Windows/Fonts/kaiu.ttf",       # DFKai-SB
        "C:/Windows/Fonts/arial.ttf",      # Fallback
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return fp
    return None


def create_text_image(text, font_path, font_size, color, max_width=900):
    """Create a text image using PIL for Chinese text support."""
    font = ImageFont.truetype(font_path, font_size)

    # Word wrap for Chinese text
    lines = []
    current_line = ""
    for char in text:
        test_line = current_line + char
        bbox = font.getbbox(test_line)
        if bbox[2] > max_width and current_line:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)

    # Calculate total height
    line_height = font_size + 10
    total_height = line_height * len(lines)
    img_width = max_width + 40

    # Create image
    img = Image.new('RGBA', (img_width, total_height + 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y = 10
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (img_width - text_width) // 2
        draw.text((x, y), line, fill=color, font=font)
        y += line_height

    return np.array(img)


def make_slide(text, font_path, font_size, text_color, bg_color, duration=4, subtitle=None, sub_size=36):
    """Create a single slide with text on colored background."""
    # Background
    bg = ColorClip(size=(WIDTH, HEIGHT), color=bg_color).with_duration(duration)

    clips = [bg]

    # Main text image
    text_img = create_text_image(text, font_path, font_size, text_color, max_width=900)
    text_clip = (
        ColorClip(size=(text_img.shape[1], text_img.shape[0]), color=(0, 0, 0, 0))
        .with_duration(duration)
    )

    # Convert PIL image to video clip
    from moviepy import ImageClip
    main_clip = (
        ImageClip(text_img)
        .with_duration(duration)
        .with_position(("center", HEIGHT // 2 - text_img.shape[0] // 2 - 100))
    )
    clips.append(main_clip)

    # Subtitle
    if subtitle:
        sub_img = create_text_image(subtitle, font_path, sub_size, (220, 220, 220), max_width=850)
        sub_clip = (
            ImageClip(sub_img)
            .with_duration(duration)
            .with_position(("center", HEIGHT // 2 + text_img.shape[0] // 2 - 50))
        )
        clips.append(sub_clip)

    return CompositeVideoClip(clips, size=(WIDTH, HEIGHT)).with_duration(duration)


def make_video(slides_data, filename, outro_text="broadbandhk.com"):
    """Create a complete video from slides."""
    font_path = find_chinese_font()
    if not font_path:
        print("ERROR: No Chinese font found!")
        return

    print(f"  Using font: {font_path}")
    slides = []

    for i, slide in enumerate(slides_data):
        print(f"  Generating slide {i+1}/{len(slides_data)}...")
        s = make_slide(
            text=slide['text'],
            font_path=font_path,
            font_size=slide.get('font_size', 72),
            text_color=slide.get('text_color', (255, 255, 255)),
            bg_color=slide.get('bg_color', (30, 30, 80)),
            duration=slide.get('duration', 4),
            subtitle=slide.get('subtitle'),
            sub_size=slide.get('sub_size', 40),
        )
        slides.append(s)

    # Outro slide
    outro = make_slide(
        text=outro_text,
        font_path=font_path,
        font_size=64,
        text_color=(255, 255, 255),
        bg_color=(102, 126, 234),
        duration=3,
        subtitle="免費寬頻格價比較 | WhatsApp: 5228 7541",
        sub_size=36,
    )
    slides.append(outro)

    print("  Combining slides...")
    final = concatenate_videoclips(slides, method="compose")

    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"  Rendering video: {filepath}")
    final.write_videofile(
        filepath,
        fps=FPS,
        codec='libx264',
        audio=False,
        preset='ultrafast',
        threads=4,
    )
    print(f"  Done! {filepath}\n")
    final.close()


# ========== VIDEO DEFINITIONS ==========

VIDEOS = [
    {
        "filename": "01_最平寬頻邊間.mp4",
        "slides": [
            {"text": "香港最平寬頻\n係邊間？", "font_size": 80, "bg_color": (220, 50, 50), "duration": 3},
            {"text": "第5名\n有線寬頻", "subtitle": "100M 約$88起/月", "font_size": 72, "bg_color": (40, 40, 100), "duration": 3},
            {"text": "第4名\n和記寬頻", "subtitle": "100M 約$98起/月", "font_size": 72, "bg_color": (40, 60, 100), "duration": 3},
            {"text": "第3名\n香港寬頻", "subtitle": "100M 約$108起/月", "font_size": 72, "bg_color": (40, 80, 100), "duration": 3},
            {"text": "第2名\n網上行", "subtitle": "100M 約$128起/月", "font_size": 72, "bg_color": (40, 100, 100), "duration": 3},
            {"text": "第1名 最平！\n中國移動", "subtitle": "100M 約$78起/月", "font_size": 72, "bg_color": (0, 150, 50), "duration": 4},
            {"text": "想知邊間\n最適合你？", "subtitle": "broadbandhk.com 免費格價", "font_size": 72, "bg_color": (102, 126, 234), "duration": 3},
        ]
    },
    {
        "filename": "02_WiFi慢一招即救.mp4",
        "slides": [
            {"text": "WiFi慢到\n想掟Router？", "font_size": 80, "bg_color": (200, 50, 50), "duration": 3},
            {"text": "試吓呢5招", "subtitle": "唔使換Plan都可以快返", "font_size": 80, "bg_color": (50, 50, 120), "duration": 3},
            {"text": "第1招\nRouter擺屋中間", "subtitle": "唔好塞入櫃！", "font_size": 64, "bg_color": (30, 100, 150), "duration": 4},
            {"text": "第2招\n遠離微波爐", "subtitle": "微波爐會干擾WiFi訊號", "font_size": 64, "bg_color": (30, 120, 130), "duration": 4},
            {"text": "第3招\n每星期重啟Router", "subtitle": "清除暫存，速度即回", "font_size": 64, "bg_color": (30, 140, 110), "duration": 4},
            {"text": "第4招\n用5GHz頻段", "subtitle": "設定入面揀5GHz，快好多", "font_size": 64, "bg_color": (30, 160, 90), "duration": 4},
            {"text": "第5招\n加Mesh WiFi", "subtitle": "屋企大就要用Mesh", "font_size": 64, "bg_color": (30, 180, 70), "duration": 4},
            {"text": "試完仲係慢？", "subtitle": "可能真係要升級Plan了", "font_size": 72, "bg_color": (102, 126, 234), "duration": 3},
        ]
    },
    {
        "filename": "03_寬頻約滿蝕錢.mp4",
        "slides": [
            {"text": "寬頻約滿\n唔轉台？", "font_size": 80, "bg_color": (180, 30, 30), "duration": 3},
            {"text": "你每年\n蝕緊幾千蚊！", "font_size": 80, "bg_color": (220, 50, 50), "text_color": (255, 255, 0), "duration": 3},
            {"text": "約滿後\n自動續約月費", "subtitle": "通常比新客貴 30-50%", "font_size": 64, "bg_color": (60, 30, 30), "duration": 4},
            {"text": "轉台客優惠", "subtitle": "供應商最想搶嘅就係你", "font_size": 64, "bg_color": (30, 60, 30), "duration": 4},
            {"text": "每年可以\n慳$2,000-$4,000", "font_size": 72, "bg_color": (0, 150, 50), "text_color": (255, 255, 255), "duration": 4},
            {"text": "3步搞掂轉台", "font_size": 72, "bg_color": (50, 50, 130), "duration": 2},
            {"text": "①\n格價比較", "subtitle": "至少比較3間供應商", "font_size": 72, "bg_color": (60, 60, 140), "duration": 3},
            {"text": "②\n簽新約", "subtitle": "話佢知你係轉台客", "font_size": 72, "bg_color": (70, 70, 150), "duration": 3},
            {"text": "③\n等新寬頻裝好", "subtitle": "新舊銜接，唔會斷網", "font_size": 72, "bg_color": (80, 80, 160), "duration": 3},
        ]
    },
    {
        "filename": "04_100M_vs_1000M.mp4",
        "slides": [
            {"text": "100M vs 1000M", "subtitle": "你真係需要咁快？", "font_size": 80, "bg_color": (50, 50, 130), "duration": 3},
            {"text": "100M 夠用嗎？", "font_size": 72, "bg_color": (80, 80, 40), "duration": 2},
            {"text": "瀏覽網頁 ✓\n睇YouTube ✓\n社交媒體 ✓", "subtitle": "1-2人用：100M夠", "font_size": 56, "bg_color": (30, 100, 30), "duration": 5},
            {"text": "500M 適合", "font_size": 72, "bg_color": (80, 80, 40), "duration": 2},
            {"text": "Netflix 4K ✓\nWFH視像會議 ✓\n3-4部裝置 ✓", "subtitle": "一般家庭首選", "font_size": 56, "bg_color": (30, 80, 130), "duration": 5},
            {"text": "1000M 適合", "font_size": 72, "bg_color": (80, 80, 40), "duration": 2},
            {"text": "打機低延遲 ✓\n大量下載 ✓\n5部裝置以上 ✓", "subtitle": "重度用家/多人家庭", "font_size": 56, "bg_color": (130, 30, 80), "duration": 5},
            {"text": "結論：\n大部分人\n500M已經夠用", "font_size": 64, "bg_color": (0, 150, 50), "duration": 4},
        ]
    },
    {
        "filename": "05_寬頻Sales秘密.mp4",
        "slides": [
            {"text": "寬頻Sales\n唔會同你講\n嘅3件事", "font_size": 72, "bg_color": (150, 30, 30), "duration": 3},
            {"text": "第1件事", "font_size": 80, "bg_color": (50, 50, 130), "duration": 2},
            {"text": "合約期越長\n月費越平", "subtitle": "但你會被綁死24-36個月", "font_size": 64, "bg_color": (60, 60, 140), "duration": 5},
            {"text": "第2件事", "font_size": 80, "bg_color": (50, 50, 130), "duration": 2},
            {"text": "「免安裝費」\n其實計咗入月費", "subtitle": "羊毛出在羊身上", "font_size": 64, "bg_color": (60, 60, 140), "duration": 5},
            {"text": "第3件事", "font_size": 80, "bg_color": (50, 50, 130), "duration": 2},
            {"text": "轉台客永遠\n比續約客平", "subtitle": "所以約滿一定要格價！", "font_size": 64, "bg_color": (60, 60, 140), "duration": 5},
            {"text": "想知最真實價格？", "subtitle": "broadbandhk.com 免費幫你格", "font_size": 64, "bg_color": (102, 126, 234), "duration": 3},
        ]
    },
    {
        "filename": "06_搬屋寬頻攻略.mp4",
        "slides": [
            {"text": "搬屋\n寬頻點搞？", "font_size": 80, "bg_color": (50, 100, 150), "duration": 3},
            {"text": "5步搞掂", "subtitle": "唔使煩", "font_size": 80, "bg_color": (30, 30, 80), "duration": 2},
            {"text": "Step 1\n搬屋前1個月\n開始格價", "font_size": 64, "bg_color": (40, 70, 120), "duration": 4},
            {"text": "Step 2\n查新地址覆蓋", "subtitle": "邊間供應商有得揀", "font_size": 64, "bg_color": (50, 80, 130), "duration": 4},
            {"text": "Step 3\n比較新Plan", "subtitle": "趁機轉台可以慳更多", "font_size": 64, "bg_color": (60, 90, 140), "duration": 4},
            {"text": "Step 4\n預約安裝日", "subtitle": "搬入去即有WiFi用", "font_size": 64, "bg_color": (70, 100, 150), "duration": 4},
            {"text": "Step 5\n取消舊合約", "subtitle": "確認冇尾數冇罰款", "font_size": 64, "bg_color": (80, 110, 160), "duration": 4},
            {"text": "搬屋寬頻\n交畀我哋搞！", "subtitle": "broadbandhk.com 免費跟進", "font_size": 64, "bg_color": (102, 126, 234), "duration": 3},
        ]
    },
    {
        "filename": "07_公屋寬頻點揀.mp4",
        "slides": [
            {"text": "公屋寬頻\n點揀好？", "font_size": 80, "bg_color": (50, 50, 130), "duration": 3},
            {"text": "公屋通常有\n2-3間供應商", "subtitle": "唔係間間都有得揀", "font_size": 64, "bg_color": (40, 60, 100), "duration": 4},
            {"text": "網上行\n覆蓋最廣", "subtitle": "大部分公屋都有", "font_size": 64, "bg_color": (0, 80, 150), "duration": 4},
            {"text": "香港寬頻\n性價比高", "subtitle": "經常有轉台優惠", "font_size": 64, "bg_color": (150, 50, 0), "duration": 4},
            {"text": "中國移動\n最平！", "subtitle": "公屋入門首選", "font_size": 64, "bg_color": (0, 130, 60), "duration": 4},
            {"text": "貼士：\n先查你屋邨覆蓋\n再格價比較", "font_size": 64, "bg_color": (130, 50, 130), "duration": 4},
        ]
    },
    {
        "filename": "08_Router擺位教學.mp4",
        "slides": [
            {"text": "Router擺呢度\n速度快一倍", "font_size": 72, "bg_color": (180, 50, 50), "duration": 3},
            {"text": "❌ 錯誤擺法", "font_size": 80, "bg_color": (150, 30, 30), "duration": 2},
            {"text": "塞入電視櫃\n放喺角落\n貼住牆壁", "subtitle": "訊號會被阻擋", "font_size": 64, "bg_color": (100, 30, 30), "duration": 5},
            {"text": "✓ 正確擺法", "font_size": 80, "bg_color": (30, 130, 30), "duration": 2},
            {"text": "放高位\n擺屋中間\n周圍冇遮擋", "subtitle": "訊號可以均勻覆蓋全屋", "font_size": 64, "bg_color": (30, 100, 30), "duration": 5},
            {"text": "遠離呢啲嘢", "font_size": 72, "bg_color": (130, 100, 0), "duration": 2},
            {"text": "微波爐\n魚缸\n鏡子\n金屬物件", "subtitle": "全部會干擾WiFi訊號", "font_size": 64, "bg_color": (100, 80, 0), "duration": 5},
            {"text": "試吓移動Router\n可能即刻快返！", "font_size": 64, "bg_color": (102, 126, 234), "duration": 3},
        ]
    },
    {
        "filename": "09_點樣測WiFi速度.mp4",
        "slides": [
            {"text": "你屋企WiFi\n有幾快？", "subtitle": "教你自己測", "font_size": 80, "bg_color": (50, 50, 150), "duration": 3},
            {"text": "Step 1\n開手機瀏覽器", "font_size": 64, "bg_color": (40, 60, 120), "duration": 3},
            {"text": "Step 2\n去 speedtest.net", "subtitle": "或者 fast.com", "font_size": 64, "bg_color": (50, 70, 130), "duration": 4},
            {"text": "Step 3\n撳「開始測試」", "subtitle": "等30秒就有結果", "font_size": 64, "bg_color": (60, 80, 140), "duration": 4},
            {"text": "點睇結果？", "font_size": 72, "bg_color": (70, 70, 30), "duration": 2},
            {"text": "下載速度\n>50Mbps = 合格\n>200Mbps = 良好\n>500Mbps = 極速", "font_size": 56, "bg_color": (30, 100, 60), "duration": 6},
            {"text": "如果速度\n唔達標", "subtitle": "可能係Router問題或者要升級Plan", "font_size": 64, "bg_color": (150, 50, 50), "duration": 4},
        ]
    },
    {
        "filename": "10_光纖入屋vs到樓.mp4",
        "slides": [
            {"text": "光纖入屋\nvs\n光纖到樓", "subtitle": "有咩分別？", "font_size": 72, "bg_color": (50, 50, 130), "duration": 3},
            {"text": "光纖入屋\nFTTH", "font_size": 72, "bg_color": (0, 130, 80), "duration": 2},
            {"text": "光纖直接\n拉到你屋企", "subtitle": "速度最快最穩定", "font_size": 64, "bg_color": (0, 110, 70), "duration": 5},
            {"text": "光纖到樓\nFTTB", "font_size": 72, "bg_color": (130, 80, 0), "duration": 2},
            {"text": "光纖只到大廈機房\n再用銅線入屋", "subtitle": "速度會有損耗", "font_size": 64, "bg_color": (110, 70, 0), "duration": 5},
            {"text": "點分？\n問供應商：\n「係咪FTTH？」", "subtitle": "記住要問清楚", "font_size": 64, "bg_color": (50, 50, 130), "duration": 5},
            {"text": "揀Plan要睇\n接駁方式！", "subtitle": "broadbandhk.com 幫你查", "font_size": 64, "bg_color": (102, 126, 234), "duration": 3},
        ]
    },
]


def main():
    font = find_chinese_font()
    if not font:
        print("ERROR: Cannot find Chinese font!")
        return

    print(f"Font: {font}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Videos to generate: {len(VIDEOS)}\n")

    for i, video in enumerate(VIDEOS):
        print(f"[{i+1}/{len(VIDEOS)}] Generating: {video['filename']}")
        try:
            make_video(video['slides'], video['filename'])
        except Exception as e:
            print(f"  ERROR: {e}\n")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
