"""
OCR 核心引擎 —— 基于 PaddleOCR 3.x 封装文字识别功能
支持中英文混合识别，包含文字检测、方向分类、文字识别等子模型
"""

from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import logging
import numpy as np


class OCREngine:
    """OCR 识别引擎，封装 PaddleOCR 3.x 的初始化与推理逻辑"""

    def __init__(self, lang: str = "ch"):
        """
        初始化 OCR 引擎

        参数:
            lang: 识别语言，"ch" 表示中英混合，"en" 表示纯英文
        """
        self.ocr = PaddleOCR(lang=lang)

    def recognize(self, image_path: str) -> list[dict]:
        """
        识别图片中的文字

        参数:
            image_path: 图片文件路径

        返回:
            识别结果列表，每项包含 text（文字）、confidence（置信度）、box（位置框）
        """
        results = self.ocr.predict(image_path)

        if not results:
            return []

        detections = []
        for res in results:
            texts = res.get("rec_texts", [])
            scores = res.get("rec_scores", [])
            polys = res.get("rec_polys", [])

            for i in range(len(texts)):
                box = polys[i].tolist() if hasattr(polys[i], "tolist") else list(polys[i])
                detections.append({
                    "text": texts[i],
                    "confidence": round(float(scores[i]), 4) if i < len(scores) else 0.0,
                    "box": box,
                })

        return detections

    def get_full_text(self, image_path: str) -> str:
        """
        识别图片并返回纯文本（按行拼接）

        参数:
            image_path: 图片文件路径

        返回:
            识别出的完整文本字符串
        """
        detections = self.recognize(image_path)
        lines = [d["text"] for d in detections]
        return "\n".join(lines)

    def draw_results(self, image_path: str, detections: list[dict] | None = None) -> np.ndarray:
        """
        在原图上绘制识别结果（文字框和文字内容）

        参数:
            image_path: 原始图片路径
            detections: 识别结果列表，为 None 时自动调用 recognize

        返回:
            绘制了标注框的图像（numpy 数组）
        """
        if detections is None:
            detections = self.recognize(image_path)

        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        # 尝试加载支持中文的字体，找不到则回退到默认字体
        font = None
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for fp in font_paths:
            try:
                font = ImageFont.truetype(fp, 18)
                break
            except FileNotFoundError:
                continue
            except OSError as e:
                logging.warning(f"字体文件 {fp} 加载失败: {e}")
                continue

        if font is None:
            logging.warning("未找到可用的中文字体，标注图片中的中文可能无法正常显示")

        for det in detections:
            text = det["text"]
            conf = det["confidence"]

            # 绘制四边形框（用线段逐边绘制，兼容各版本 Pillow）
            pts = [(int(p[0]), int(p[1])) for p in det["box"]]
            for i in range(4):
                p1 = pts[i]
                p2 = pts[(i + 1) % 4]
                draw.line([p1, p2], fill=(0, 255, 0), width=2)

            # 在框上方标注文字和置信度
            label = f"{text} ({conf:.2f})"
            x, y = pts[0]
            if font:
                draw.text((x, y - 22), label, fill=(255, 0, 0), font=font)
            else:
                draw.text((x, y - 22), label, fill=(255, 0, 0))

        return np.array(img)
