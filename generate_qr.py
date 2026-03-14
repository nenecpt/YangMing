import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont
import os

BASE_URL = "https://nenecpt.github.io/YangMing"
OUT_DIR = r"C:\Projects\YangMing\qrcodes"
os.makedirs(OUT_DIR, exist_ok=True)

configs = [
    {"url": f"{BASE_URL}/zh.html", "label": "中文版 Chinese", "filename": "qr_zh.png", "color": "#1a3a5c"},
    {"url": f"{BASE_URL}/ja.html", "label": "日本語版 Japanese", "filename": "qr_ja.png", "color": "#1a3a5c"},
    {"url": f"{BASE_URL}/en.html", "label": "English Version", "filename": "qr_en.png", "color": "#1a3a5c"},
    {"url": f"{BASE_URL}/",        "label": "選擇語言 Select Language", "filename": "qr_all.png", "color": "#1a3a5c"},
]

for cfg in configs:
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=3)
    qr.add_data(cfg["url"])
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        fill_color=cfg["color"],
        back_color="white"
    ).convert("RGB")

    qr_w, qr_h = img.size
    padding = 30
    label_h = 60
    canvas_w = qr_w + padding * 2
    canvas_h = qr_h + padding * 2 + label_h

    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    canvas.paste(img, (padding, padding))

    draw = ImageDraw.Draw(canvas)

    # 底部金色橫線
    draw.line([(padding, qr_h + padding + 10), (canvas_w - padding, qr_h + padding + 10)], fill="#c9a84c", width=2)

    # 標籤文字
    try:
        font = ImageFont.truetype("msyh.ttc", 18)
    except:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), cfg["label"], font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_x = (canvas_w - text_w) // 2
    text_y = qr_h + padding + 20
    draw.text((text_x, text_y), cfg["label"], fill="#1a3a5c", font=font)

    # 頂部文字
    top_label = "台北陽明扶輪社 49週年"
    try:
        font_small = ImageFont.truetype("msyh.ttc", 12)
    except:
        font_small = ImageFont.load_default()
    top_bbox = draw.textbbox((0, 0), top_label, font=font_small)
    top_w = top_bbox[2] - top_bbox[0]

    out_path = os.path.join(OUT_DIR, cfg["filename"])
    canvas.save(out_path, quality=95)
    print(f"✓ {cfg['filename']} -> {cfg['url']}")

print(f"\n全部完成！QR Code 已儲存至 {OUT_DIR}")
