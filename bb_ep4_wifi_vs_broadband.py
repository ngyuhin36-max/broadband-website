"""
寬頻教室HK EP4：WiFi 同寬頻有咩分別？好多人搞混！
1920x1080 Full HD, 24fps
Python PIL slides + edge-tts 廣東話配音 + moviepy 合片
"""

import sys
import io
import os
import asyncio
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, CompositeAudioClip
)
import numpy as np
import edge_tts

# ========== 設定 ==========
WIDTH = 1920
HEIGHT = 1080
FPS = 24
VOICE = "zh-HK-HiuGaaiNeural"  # 廣東話女聲

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SLIDE_DIR = os.path.join(SCRIPT_DIR, "bb_ep4_slides")
VOICE_DIR = os.path.join(SCRIPT_DIR, "bb_ep4_voiceover")
OUTPUT_DIR = SCRIPT_DIR

os.makedirs(SLIDE_DIR, exist_ok=True)
os.makedirs(VOICE_DIR, exist_ok=True)


def get_font(size, bold=False):
    """搵中文字體"""
    if bold:
        paths = ["C:/Windows/Fonts/msjhbd.ttc", "C:/Windows/Fonts/msyhbd.ttc"]
    else:
        paths = ["C:/Windows/Fonts/msjh.ttc", "C:/Windows/Fonts/msyh.ttc"]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)


def draw_rounded_rect(draw, xy, radius, fill):
    """畫圓角矩形"""
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_icon_wifi(draw, cx, cy, size, color):
    """畫WiFi圖示"""
    for i in range(3):
        r = size - i * (size // 3)
        bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.arc(bbox, start=225, end=315, fill=color, width=max(4, size // 8))
    dot_r = max(4, size // 10)
    draw.ellipse([cx - dot_r, cy - dot_r + size // 4, cx + dot_r, cy + dot_r + size // 4], fill=color)


def draw_icon_cable(draw, cx, cy, size, color):
    """畫網線圖示"""
    # Cable body
    draw.rounded_rectangle(
        [cx - size // 2, cy - size // 3, cx + size // 2, cy + size // 3],
        radius=8, fill=color
    )
    # Connector tab
    draw.rectangle(
        [cx - size // 4, cy - size // 3 - size // 6, cx + size // 4, cy - size // 3],
        fill=color
    )
    # Lines on cable
    for i in range(3):
        lx = cx - size // 4 + i * (size // 4)
        draw.line([(lx, cy - size // 5), (lx, cy + size // 5)], fill=(255, 255, 255), width=2)


def draw_icon_router(draw, cx, cy, size, color):
    """畫Router圖示"""
    # Router body
    draw.rounded_rectangle(
        [cx - size, cy - size // 3, cx + size, cy + size // 3],
        radius=10, fill=color
    )
    # Antennas
    draw.line([(cx - size // 2, cy - size // 3), (cx - size // 2 - 10, cy - size)], fill=color, width=4)
    draw.line([(cx + size // 2, cy - size // 3), (cx + size // 2 + 10, cy - size)], fill=color, width=4)
    # Lights
    for i in range(3):
        lx = cx - size // 2 + i * (size // 2)
        draw.ellipse([lx - 5, cy - 8, lx + 5, cy + 8], fill=(100, 255, 100))


def draw_icon_globe(draw, cx, cy, size, color):
    """畫地球圖示（代表互聯網）"""
    draw.ellipse([cx - size, cy - size, cx + size, cy + size], outline=color, width=3)
    draw.arc([cx - size, cy - size, cx + size, cy + size], 0, 360, fill=color, width=3)
    draw.ellipse([cx - size // 2, cy - size, cx + size // 2, cy + size], outline=color, width=2)
    draw.line([(cx - size, cy), (cx + size, cy)], fill=color, width=2)


def draw_check(draw, x, y, size, color):
    """畫剔號"""
    draw.line([(x, y), (x + size // 3, y + size // 2)], fill=color, width=max(3, size // 5))
    draw.line([(x + size // 3, y + size // 2), (x + size, y - size // 4)], fill=color, width=max(3, size // 5))


def draw_cross(draw, x, y, size, color):
    """畫交叉"""
    draw.line([(x, y - size // 3), (x + size, y + size // 3)], fill=color, width=max(3, size // 5))
    draw.line([(x, y + size // 3), (x + size, y - size // 3)], fill=color, width=max(3, size // 5))


def center_text(draw, text, font, y, fill, width=WIDTH):
    """置中文字"""
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, fill=fill, font=font)


# ========== SLIDE 定義 ==========

def slide_01_intro():
    """開場：WiFi 同寬頻有咩分別？"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (20, 25, 60))
    draw = ImageDraw.Draw(img)

    # 背景裝飾
    for i in range(12):
        cx = 100 + (i * 170) % WIDTH
        cy = 100 + (i * 130) % HEIGHT
        r = 20 + i * 3
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(30, 35, 75))

    # 頂部標籤
    draw_rounded_rect(draw, [660, 80, 1260, 140], 30, (255, 70, 70))
    font_badge = get_font(38, bold=True)
    draw.text((700, 88), "寬頻教室HK EP4", fill=(255, 255, 255), font=font_badge)

    # 主標題
    font_title = get_font(90, bold=True)
    center_text(draw, "WiFi 同寬頻", font_title, 220, (255, 255, 255))

    font_title2 = get_font(90, bold=True)
    center_text(draw, "有咩分別？", font_title2, 330, (255, 220, 50))

    # 副標題
    font_sub = get_font(52)
    center_text(draw, "好多人搞混！今集幫你搞清楚", font_sub, 470, (180, 190, 230))

    # 左邊：WiFi圖示
    draw_icon_wifi(draw, 550, 700, 100, (100, 200, 255))
    font_label = get_font(44, bold=True)
    draw.text((490, 820), "WiFi", fill=(100, 200, 255), font=font_label)

    # VS
    font_vs = get_font(72, bold=True)
    center_text(draw, "VS", font_vs, 680, (255, 100, 100))

    # 右邊：寬頻（網線）圖示
    draw_icon_cable(draw, 1370, 700, 80, (255, 180, 50))
    font_label2 = get_font(44, bold=True)
    draw.text((1310, 820), "寬頻", fill=(255, 180, 50), font=font_label2)

    # 底部品牌
    draw_rounded_rect(draw, [660, 960, 1260, 1030], 20, (102, 126, 234))
    font_brand = get_font(36, bold=True)
    draw.text((700, 970), "broadbandhk.com 出品", fill=(255, 255, 255), font=font_brand)

    return img


def slide_02_what_is_broadband():
    """寬頻係咩？"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (25, 50, 80))
    draw = ImageDraw.Draw(img)

    # 標題
    draw_rounded_rect(draw, [60, 40, 500, 120], 20, (255, 180, 50))
    font_tag = get_font(48, bold=True)
    draw.text((100, 50), "寬頻係咩？", fill=(30, 30, 30), font=font_tag)

    # 主要解釋
    font_main = get_font(56, bold=True)
    draw.text((100, 180), "寬頻 = 你屋企條上網線路", fill=(255, 255, 255), font=font_main)

    font_desc = get_font(42)
    draw.text((100, 270), "由電訊公司（ISP）拉到你屋企嘅實體線路", fill=(180, 200, 230), font=font_desc)
    draw.text((100, 330), "好似水喉一樣，負責將互聯網「送到」你屋企", fill=(180, 200, 230), font=font_desc)

    # 圖解：ISP -> 光纖 -> 你屋企
    y_mid = 520
    # ISP
    draw_rounded_rect(draw, [150, y_mid - 50, 400, y_mid + 50], 15, (102, 126, 234))
    font_box = get_font(36, bold=True)
    draw.text((190, y_mid - 20), "電訊公司", fill=(255, 255, 255), font=font_box)
    draw_icon_globe(draw, 280, y_mid + 100, 30, (150, 180, 255))

    # 箭頭線
    draw.line([(400, y_mid), (750, y_mid)], fill=(255, 220, 50), width=6)
    font_arrow = get_font(30)
    draw.text((500, y_mid - 40), "光纖/銅線", fill=(255, 220, 50), font=font_arrow)

    # Router
    draw_rounded_rect(draw, [750, y_mid - 50, 1050, y_mid + 50], 15, (80, 160, 80))
    draw.text((810, y_mid - 20), "你屋企", fill=(255, 255, 255), font=font_box)
    draw_icon_router(draw, 900, y_mid + 110, 40, (100, 200, 100))

    # 箭頭線2
    draw.line([(1050, y_mid), (1350, y_mid)], fill=(100, 200, 255), width=6)
    draw.text((1120, y_mid - 40), "上網！", fill=(100, 200, 255), font=font_arrow)

    # 裝置
    draw_rounded_rect(draw, [1350, y_mid - 50, 1750, y_mid + 50], 15, (150, 80, 150))
    draw.text((1380, y_mid - 20), "手機/電腦", fill=(255, 255, 255), font=font_box)

    # 重點
    draw_rounded_rect(draw, [100, 750, 1820, 870], 20, (40, 65, 100))
    font_key = get_font(44, bold=True)
    draw.text((140, 770), "重點：", fill=(255, 220, 50), font=font_key)
    font_key2 = get_font(42)
    draw.text((320, 775), "寬頻 = 實體連接，由供應商拉線到你屋企，冇寬頻就上唔到網", fill=(255, 255, 255), font=font_key2)

    # 底部
    font_ep = get_font(28)
    draw.text((1550, 1030), "寬頻教室HK EP4", fill=(120, 140, 170), font=font_ep)

    return img


def slide_03_what_is_wifi():
    """WiFi係咩？"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (20, 35, 70))
    draw = ImageDraw.Draw(img)

    # 標題
    draw_rounded_rect(draw, [60, 40, 500, 120], 20, (100, 200, 255))
    font_tag = get_font(48, bold=True)
    draw.text((100, 50), "WiFi係咩？", fill=(30, 30, 30), font=font_tag)

    # 主要解釋
    font_main = get_font(56, bold=True)
    draw.text((100, 180), "WiFi = 無線訊號", fill=(255, 255, 255), font=font_main)

    font_desc = get_font(42)
    draw.text((100, 270), "由你屋企嘅 Router（路由器）發出嘅無線電波", fill=(180, 200, 230), font=font_desc)
    draw.text((100, 330), "等你嘅手機、平板、電腦可以「無線」上網", fill=(180, 200, 230), font=font_desc)

    # 圖解：Router -> WiFi訊號 -> 裝置
    y_mid = 530
    # Router
    draw_rounded_rect(draw, [200, y_mid - 60, 550, y_mid + 60], 15, (80, 160, 80))
    font_box = get_font(36, bold=True)
    draw.text((270, y_mid - 20), "Router", fill=(255, 255, 255), font=font_box)
    draw_icon_router(draw, 380, y_mid + 120, 40, (100, 200, 100))

    # WiFi 訊號波紋
    draw_icon_wifi(draw, 850, y_mid, 100, (100, 200, 255))
    font_wifi = get_font(30)
    draw.text((790, y_mid + 110), "WiFi訊號", fill=(100, 200, 255), font=font_wifi)

    # 裝置們
    devices = ["📱手機", "💻電腦", "📺電視"]
    font_dev = get_font(36, bold=True)
    for i, dev in enumerate(devices):
        dy = y_mid - 80 + i * 80
        draw_rounded_rect(draw, [1200, dy - 25, 1700, dy + 25], 12, (60, 80, 130))
        draw.text((1220, dy - 18), dev, fill=(255, 255, 255), font=font_dev)

    # 連接線
    for i in range(3):
        dy = y_mid - 80 + i * 80
        draw.line([(950, y_mid), (1200, dy)], fill=(100, 200, 255), width=2)

    # 重點
    draw_rounded_rect(draw, [100, 760, 1820, 880], 20, (35, 50, 90))
    font_key = get_font(44, bold=True)
    draw.text((140, 780), "重點：", fill=(100, 200, 255), font=font_key)
    font_key2 = get_font(42)
    draw.text((320, 785), "WiFi 只係 Router 發出嘅無線訊號，唔等於寬頻本身！", fill=(255, 255, 255), font=font_key2)

    # 底部
    font_ep = get_font(28)
    draw.text((1550, 1030), "寬頻教室HK EP4", fill=(120, 140, 170), font=font_ep)

    return img


def slide_04_analogy():
    """生活比喻：水喉 vs 花灑"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (30, 30, 65))
    draw = ImageDraw.Draw(img)

    # 標題
    draw_rounded_rect(draw, [60, 40, 700, 120], 20, (200, 100, 255))
    font_tag = get_font(48, bold=True)
    draw.text((100, 50), "一個比喻你就明！", fill=(255, 255, 255), font=font_tag)

    # 左邊：寬頻 = 水喉
    draw_rounded_rect(draw, [80, 180, 900, 500], 25, (40, 60, 100))
    font_title = get_font(52, bold=True)
    draw.text((120, 200), "寬頻 = 水喉", fill=(255, 180, 50), font=font_title)
    font_desc = get_font(38)
    draw.text((120, 280), "• 由水務署（ISP）拉到你屋企", fill=(220, 230, 255), font=font_desc)
    draw.text((120, 340), "• 冇水喉 = 冇水用", fill=(220, 230, 255), font=font_desc)
    draw.text((120, 400), "• 水喉越粗 = 上網越快", fill=(220, 230, 255), font=font_desc)

    # 右邊：WiFi = 花灑
    draw_rounded_rect(draw, [1020, 180, 1840, 500], 25, (30, 55, 95))
    draw.text((1060, 200), "WiFi = 花灑", fill=(100, 200, 255), font=font_title)
    draw.text((1060, 280), "• 將水（數據）噴出嚟", fill=(220, 230, 255), font=font_desc)
    draw.text((1060, 340), "• 冇花灑都有水（用網線）", fill=(220, 230, 255), font=font_desc)
    draw.text((1060, 400), "• 花灑壞咗唔代表冇水", fill=(220, 230, 255), font=font_desc)

    # 下方重點框
    draw_rounded_rect(draw, [80, 570, 1840, 750], 25, (60, 30, 30))
    font_big = get_font(50, bold=True)
    center_text(draw, "所以WiFi慢 ≠ 寬頻慢", font_big, 590, (255, 100, 100))
    font_sub = get_font(40)
    center_text(draw, "可能只係你個Router太舊或者擺錯位！", font_sub, 670, (255, 200, 200))

    # 底部tips
    draw_rounded_rect(draw, [80, 820, 1840, 1000], 20, (25, 45, 75))
    font_tip = get_font(38, bold=True)
    draw.text((120, 840), "💡 小貼士", fill=(255, 220, 50), font=font_tip)
    font_tip2 = get_font(36)
    draw.text((120, 900), "想知係Router問題定寬頻問題？用網線直接插電腦測速就知！", fill=(200, 210, 240), font=font_tip2)

    font_ep = get_font(28)
    draw.text((1550, 1030), "寬頻教室HK EP4", fill=(120, 140, 170), font=font_ep)

    return img


def slide_05_comparison():
    """對比表：寬頻 vs WiFi"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (20, 25, 55))
    draw = ImageDraw.Draw(img)

    # 標題
    font_title = get_font(56, bold=True)
    center_text(draw, "寬頻 vs WiFi 對比", font_title, 40, (255, 255, 255))
    draw.line([(200, 110), (1720, 110)], fill=(80, 100, 150), width=2)

    # 表格
    headers = ["", "寬頻", "WiFi"]
    rows = [
        ["類型", "實體線路", "無線訊號"],
        ["提供者", "電訊公司(ISP)", "你屋企Router"],
        ["連接方式", "光纖/銅線入屋", "無線電波"],
        ["收費", "每月交月費", "免費（Router買斷）"],
        ["冇咗會點", "完全上唔到網", "可以用網線上網"],
        ["速度受咩影響", "Plan速度/線路質素", "Router/距離/障礙物"],
    ]

    col_x = [100, 520, 1220]
    font_header = get_font(44, bold=True)
    font_cell = get_font(38)

    # Header row
    y = 150
    draw_rounded_rect(draw, [80, y - 10, 1840, y + 60], 10, (60, 70, 120))
    for i, h in enumerate(headers):
        color = (255, 180, 50) if i == 1 else (100, 200, 255) if i == 2 else (200, 200, 200)
        draw.text((col_x[i], y), h, fill=color, font=font_header)

    # Data rows
    for r, row in enumerate(rows):
        y = 240 + r * 120
        bg = (35, 40, 75) if r % 2 == 0 else (28, 33, 65)
        draw_rounded_rect(draw, [80, y - 10, 1840, y + 90], 10, bg)

        for c, cell in enumerate(row):
            if c == 0:
                draw.text((col_x[c], y + 10), cell, fill=(180, 190, 220), font=font_header)
            else:
                color = (255, 240, 220) if c == 1 else (200, 230, 255)
                draw.text((col_x[c], y + 10), cell, fill=color, font=font_cell)
                if c == 1:
                    # 小黃點
                    draw.ellipse([col_x[c] - 25, y + 22, col_x[c] - 10, y + 37], fill=(255, 180, 50))
                else:
                    # 小藍點
                    draw.ellipse([col_x[c] - 25, y + 22, col_x[c] - 10, y + 37], fill=(100, 200, 255))

    font_ep = get_font(28)
    draw.text((1550, 1030), "寬頻教室HK EP4", fill=(120, 140, 170), font=font_ep)

    return img


def slide_06_common_mistakes():
    """常見誤解"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (50, 20, 30))
    draw = ImageDraw.Draw(img)

    # 標題
    draw_rounded_rect(draw, [60, 40, 650, 120], 20, (255, 70, 70))
    font_tag = get_font(48, bold=True)
    draw.text((100, 50), "3個常見誤解！", fill=(255, 255, 255), font=font_tag)

    mistakes = [
        {
            "wrong": "❌「我裝咗WiFi就有上網」",
            "right": "✅ WiFi要有寬頻先用到，冇寬頻WiFi就連唔到網",
        },
        {
            "wrong": "❌「WiFi慢就係寬頻公司嘅問題」",
            "right": "✅ 好多時係Router太舊、太遠、或者有障礙物",
        },
        {
            "wrong": "❌「換咗寬頻Plan就WiFi一定快」",
            "right": "✅ 如果Router只支援100M，換1000M Plan都冇用",
        },
    ]

    font_wrong = get_font(40, bold=True)
    font_right = get_font(38)

    for i, m in enumerate(mistakes):
        y = 180 + i * 280
        # 錯誤
        draw_rounded_rect(draw, [80, y, 1840, y + 70], 15, (80, 30, 30))
        draw.text((120, y + 10), m["wrong"], fill=(255, 150, 150), font=font_wrong)
        # 正確
        draw_rounded_rect(draw, [80, y + 85, 1840, y + 230], 15, (25, 60, 40))
        draw.text((120, y + 100), m["right"], fill=(150, 255, 150), font=font_right)

    font_ep = get_font(28)
    draw.text((1550, 1030), "寬頻教室HK EP4", fill=(120, 140, 170), font=font_ep)

    return img


def slide_07_what_to_do():
    """點樣Check係邊個問題？"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (20, 40, 60))
    draw = ImageDraw.Draw(img)

    # 標題
    draw_rounded_rect(draw, [60, 40, 900, 120], 20, (50, 180, 100))
    font_tag = get_font(48, bold=True)
    draw.text((100, 50), "上網慢？3步搵出原因", fill=(255, 255, 255), font=font_tag)

    steps = [
        {
            "num": "Step 1",
            "title": "用網線直接接電腦",
            "desc": "繞過WiFi，直接測試寬頻速度",
            "color": (102, 126, 234),
        },
        {
            "num": "Step 2",
            "title": "去 speedtest.net 測速",
            "desc": "記低下載同上載速度",
            "color": (50, 180, 100),
        },
        {
            "num": "Step 3",
            "title": "比較有線同WiFi速度",
            "desc": "差好遠 → Router問題｜都慢 → 寬頻問題",
            "color": (255, 140, 50),
        },
    ]

    font_num = get_font(44, bold=True)
    font_title = get_font(48, bold=True)
    font_desc = get_font(36)

    for i, step in enumerate(steps):
        y = 180 + i * 250
        # 步驟圓形
        draw.ellipse([100, y, 200, y + 100], fill=step["color"])
        # Step number
        draw.text((115, y + 15), step["num"][-1], fill=(255, 255, 255), font=get_font(52, bold=True))

        # 內容
        draw_rounded_rect(draw, [240, y, 1840, y + 200], 20, (35, 55, 80))
        draw.text((280, y + 20), step["title"], fill=(255, 255, 255), font=font_title)
        draw.text((280, y + 90), step["desc"], fill=(180, 200, 230), font=font_desc)

        # Step label
        draw.text((280, y + 150), step["num"], fill=step["color"], font=get_font(28, bold=True))

    # 底部總結
    draw_rounded_rect(draw, [100, 950, 1820, 1030], 15, (40, 60, 90))
    font_sum = get_font(38, bold=True)
    center_text(draw, "搵到原因，先至可以對症下藥！", font_sum, 965, (255, 220, 100))

    return img


def slide_08_summary():
    """總結"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (25, 25, 60))
    draw = ImageDraw.Draw(img)

    # 標題
    font_title = get_font(64, bold=True)
    center_text(draw, "今集重點", font_title, 50, (255, 255, 255))
    draw.line([(400, 130), (1520, 130)], fill=(80, 100, 150), width=2)

    points = [
        ("1", "寬頻 = 實體線路（由ISP提供）", (255, 180, 50)),
        ("2", "WiFi = 無線訊號（由Router發出）", (100, 200, 255)),
        ("3", "冇寬頻 = 冇得上網", (255, 100, 100)),
        ("4", "WiFi慢 ≠ 寬頻慢，要分開檢查", (100, 255, 150)),
    ]

    font_num = get_font(48, bold=True)
    font_point = get_font(44)

    for i, (num, text, color) in enumerate(points):
        y = 180 + i * 130
        draw.ellipse([150, y, 220, y + 70], fill=color)
        bbox = font_num.getbbox(num)
        nx = 185 - (bbox[2] - bbox[0]) // 2
        draw.text((nx, y + 5), num, fill=(30, 30, 30), font=font_num)
        draw.text((260, y + 10), text, fill=(240, 240, 255), font=font_point)

    # 下一集預告
    draw_rounded_rect(draw, [100, 740, 1820, 900], 25, (40, 50, 90))
    font_next = get_font(40, bold=True)
    draw.text((140, 760), "📺 下一集預告", fill=(255, 220, 100), font=font_next)
    font_next_title = get_font(44, bold=True)
    draw.text((140, 830), "EP5：點解屋企WiFi會慢？5個常見原因", fill=(255, 255, 255), font=font_next_title)

    # CTA
    draw_rounded_rect(draw, [500, 940, 1420, 1030], 25, (102, 126, 234))
    font_cta = get_font(42, bold=True)
    center_text(draw, "Like + Subscribe 寬頻教室HK", font_cta, 955, (255, 255, 255))

    return img


def slide_09_outro():
    """結尾 CTA"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (102, 126, 234))
    draw = ImageDraw.Draw(img)

    # 裝飾
    for i in range(10):
        cx = 80 + i * 200
        draw.ellipse([cx - 40, 50, cx + 40, 130], fill=(120, 145, 240))
        draw.ellipse([cx - 30, 950, cx + 30, 1010], fill=(120, 145, 240))

    # WiFi icon
    draw_icon_wifi(draw, 960, 250, 120, (255, 255, 255))

    # Brand
    font_brand = get_font(72, bold=True)
    center_text(draw, "寬頻教室HK", font_brand, 400, (255, 255, 255))

    font_tag = get_font(44)
    center_text(draw, "免費寬頻知識・廣東話教學", font_tag, 500, (220, 230, 255))

    # Divider
    draw.line([(500, 570), (1420, 570)], fill=(170, 190, 255), width=2)

    # CTA items
    ctas = [
        "👍 Like 呢條片",
        "🔔 Subscribe 寬頻教室HK",
        "💬 留言話我知你想學咩",
    ]
    font_cta = get_font(44, bold=True)
    for i, cta in enumerate(ctas):
        y = 620 + i * 70
        center_text(draw, cta, font_cta, y, (255, 255, 255))

    # Website
    draw_rounded_rect(draw, [500, 870, 1420, 950], 30, (37, 211, 102))
    font_wa = get_font(44, bold=True)
    center_text(draw, "broadbandhk.com", font_wa, 885, (255, 255, 255))

    return img


# ========== 配音文稿 ==========

NARRATIONS = [
    {
        "file": "ep4_01_intro.mp3",
        "text": "WiFi同寬頻，好多人以為係同一樣嘢，但其實完全唔同！今集寬頻教室就幫你搞清楚。",
    },
    {
        "file": "ep4_02_broadband.mp3",
        "text": "首先，寬頻係咩呢？簡單嚟講，寬頻就係由電訊公司拉到你屋企嘅一條實體線路。"
               "好似水喉咁，負責將互聯網嘅數據傳送到你屋企。冇咗寬頻，你就完全上唔到網。",
    },
    {
        "file": "ep4_03_wifi.mp3",
        "text": "咁WiFi又係咩呢？WiFi其實只係你屋企個Router發出嘅無線訊號。"
               "佢嘅作用係將寬頻嘅數據，透過無線電波傳送到你嘅手機、電腦同平板。"
               "所以WiFi本身唔等於上網，佢要靠寬頻先至有用。",
    },
    {
        "file": "ep4_04_analogy.mp3",
        "text": "如果你仲係覺得混亂，可以咁樣諗。寬頻就好似水喉，由水務署拉到你屋企。"
               "而WiFi就好似花灑，負責將水噴出嚟。冇咗水喉，花灑就冇水出。"
               "但花灑壞咗，你仲可以直接用水喉。所以，WiFi慢唔一定代表寬頻慢。",
    },
    {
        "file": "ep4_05_comparison.mp3",
        "text": "我哋嚟比較一下。寬頻係實體線路，由電訊公司提供，要每月交月費。"
               "WiFi係無線訊號，由你屋企嘅Router發出，唔使額外交費。"
               "冇咗寬頻就完全上唔到網，但冇咗WiFi你仲可以用網線上網。",
    },
    {
        "file": "ep4_06_mistakes.mp3",
        "text": "好多人有三個常見誤解。第一，以為裝咗WiFi就有上網，其實冇寬頻WiFi就連唔到網。"
               "第二，以為WiFi慢就一定係寬頻公司嘅問題，但好多時只係Router太舊或者擺錯位。"
               "第三，以為換咗更快嘅寬頻Plan，WiFi就一定快，但如果Router只支援100M，換1000M Plan都冇用。",
    },
    {
        "file": "ep4_07_steps.mp3",
        "text": "如果你覺得上網慢，可以用三步搵出原因。"
               "第一步，用網線直接接電腦，繞過WiFi。"
               "第二步，去speedtest點net測速，記低下載同上載速度。"
               "第三步，比較有線同WiFi嘅速度。如果差好遠，就係Router問題。如果都慢，就係寬頻問題。",
    },
    {
        "file": "ep4_08_summary.mp3",
        "text": "今集重點：寬頻係實體線路，WiFi係無線訊號。冇寬頻就冇得上網。WiFi慢唔等於寬頻慢，要分開檢查。"
               "下一集我哋會講，點解屋企WiFi會慢，五個常見原因，記得訂閱寬頻教室HK！",
    },
    {
        "file": "ep4_09_outro.mp3",
        "text": "多謝你睇完呢條片！如果覺得有用，記得Like同Subscribe寬頻教室HK。"
               "想了解更多寬頻知識，可以去broadbandhk.com。我哋下集見！",
    },
]


# ========== 主程式 ==========

async def generate_tts(text, filepath):
    """用 edge-tts 生成廣東話配音"""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filepath)


async def generate_all_tts():
    """生成所有配音檔案"""
    for narration in NARRATIONS:
        filepath = os.path.join(VOICE_DIR, narration["file"])
        if os.path.exists(filepath):
            print(f"  [跳過] {narration['file']} 已存在")
            continue
        print(f"  生成 {narration['file']}...")
        await generate_tts(narration["text"], filepath)
        print(f"  [完成] {narration['file']}")


def generate_all_slides():
    """生成所有slides圖片"""
    slide_funcs = [
        ("slide_01_intro.png", slide_01_intro),
        ("slide_02_broadband.png", slide_02_what_is_broadband),
        ("slide_03_wifi.png", slide_03_what_is_wifi),
        ("slide_04_analogy.png", slide_04_analogy),
        ("slide_05_comparison.png", slide_05_comparison),
        ("slide_06_mistakes.png", slide_06_common_mistakes),
        ("slide_07_steps.png", slide_07_what_to_do),
        ("slide_08_summary.png", slide_08_summary),
        ("slide_09_outro.png", slide_09_outro),
    ]

    images = []
    for filename, func in slide_funcs:
        filepath = os.path.join(SLIDE_DIR, filename)
        img = func()
        img.save(filepath)
        images.append((filename, filepath))
        print(f"  [完成] {filename}")

    return images


def build_video(slides, audio_dir):
    """合併slides同配音做影片"""
    clips = []

    for i, ((slide_name, slide_path), narration) in enumerate(zip(slides, NARRATIONS)):
        audio_path = os.path.join(audio_dir, narration["file"])

        # 讀取音頻長度
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration + 0.8  # 每張slide加0.8秒停頓

        # 建立圖片clip
        img_clip = ImageClip(slide_path).set_duration(duration)

        # 加入音頻
        img_clip = img_clip.set_audio(audio_clip)
        clips.append(img_clip)

        print(f"  Slide {i+1}: {slide_name} ({duration:.1f}s)")

    print("\n合併影片中...")
    final = concatenate_videoclips(clips, method="compose")
    total_duration = final.duration

    output_path = os.path.join(OUTPUT_DIR, "bb_ep4_wifi_vs_broadband.mp4")
    print(f"輸出: {output_path}")

    final.write_videofile(
        output_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        threads=4,
        bitrate='5000k',
    )

    final.close()
    for c in clips:
        c.close()

    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"完成！")
    print(f"影片: {output_path}")
    print(f"大小: {file_size:.1f} MB")
    print(f"時長: {total_duration:.1f} 秒")
    print(f"{'='*50}")

    return output_path


def generate_thumbnail():
    """生成縮圖"""
    img = Image.new('RGB', (1280, 720), (20, 25, 60))
    draw = ImageDraw.Draw(img)

    # 背景裝飾
    draw_rounded_rect(draw, [0, 0, 640, 720], 0, (25, 50, 80))
    draw_rounded_rect(draw, [640, 0, 1280, 720], 0, (20, 35, 70))

    # 左邊：寬頻
    font_big = get_font(100, bold=True)
    draw.text((100, 200), "寬頻", fill=(255, 180, 50), font=font_big)
    draw_icon_cable(draw, 320, 400, 60, (255, 180, 50))

    # VS
    draw.ellipse([570, 280, 710, 420], fill=(255, 70, 70))
    font_vs = get_font(72, bold=True)
    draw.text((600, 310), "VS", fill=(255, 255, 255), font=font_vs)

    # 右邊：WiFi
    draw.text((770, 200), "WiFi", fill=(100, 200, 255), font=font_big)
    draw_icon_wifi(draw, 960, 400, 80, (100, 200, 255))

    # 底部
    draw_rounded_rect(draw, [200, 520, 1080, 640], 25, (255, 70, 70))
    font_bottom = get_font(56, bold=True)
    draw.text((240, 540), "好多人搞混！你分到嗎？", fill=(255, 255, 255), font=font_bottom)

    # EP標籤
    draw_rounded_rect(draw, [50, 30, 350, 100], 15, (102, 126, 234))
    font_ep = get_font(40, bold=True)
    draw.text((80, 40), "寬頻教室 EP4", fill=(255, 255, 255), font=font_ep)

    thumb_path = os.path.join(OUTPUT_DIR, "bb_ep4_thumbnail.png")
    img.save(thumb_path)
    print(f"縮圖: {thumb_path}")
    return thumb_path


def main():
    print("=" * 50)
    print("寬頻教室HK EP4：WiFi 同寬頻有咩分別？")
    print("=" * 50)

    # Step 1: 生成配音
    print("\n📢 Step 1: 生成廣東話配音...")
    asyncio.run(generate_all_tts())

    # Step 2: 生成Slides
    print("\n🎨 Step 2: 生成Slides圖片...")
    slides = generate_all_slides()

    # Step 3: 生成縮圖
    print("\n🖼️ Step 3: 生成縮圖...")
    generate_thumbnail()

    # Step 4: 合併影片
    print("\n🎬 Step 4: 合併影片...")
    build_video(slides, VOICE_DIR)

    print("\n🎉 EP4 製作完成！")


if __name__ == "__main__":
    main()
