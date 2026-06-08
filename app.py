"""
OCR Web 界面 —— 基于 Gradio 构建
功能：上传图片 → 识别文字 → 展示标注图 + 文本结果 + 详细信息表格
"""

import gradio as gr
import tempfile
import threading
import os

from ocr_engine import OCREngine


# ── 全局 OCR 引擎（延迟初始化，线程安全）────────────────────────────────────────
_engine: OCREngine | None = None
_engine_lock = threading.Lock()


def get_engine() -> OCREngine:
    global _engine
    if _engine is None:
        with _engine_lock:
            if _engine is None:
                print("正在初始化 OCR 引擎（首次启动需要下载模型，请稍候）...")
                _engine = OCREngine(lang="ch")
                print("OCR 引擎初始化完成！")
    return _engine


# ── 核心处理函数 ──────────────────────────────────────────────────────────────

def process_image(image):
    """
    处理上传的图片，返回三个输出：
    1. 标注了识别框的图片
    2. 纯文本结果
    3. 详细结果表格
    """
    if image is None:
        return None, "请先上传图片", []

    # 将上传的图片保存到临时文件
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        image.save(tmp_path)

        engine = get_engine()

        # 执行识别
        detections = engine.recognize(tmp_path)

        if not detections:
            return image, "未检测到文字，请确认图片中包含清晰文字。", []

        # 绘制标注图
        annotated_img = engine.draw_results(tmp_path, detections)

        # 拼接纯文本
        full_text = "\n".join(d["text"] for d in detections)

        # 构建详细表格数据
        table_data = []
        for i, d in enumerate(detections, 1):
            table_data.append([
                i,
                d["text"],
                f"{d['confidence']:.2%}",
            ])

        return annotated_img, full_text, table_data

    finally:
        # 清理临时文件
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ── Gradio 界面构建 ───────────────────────────────────────────────────────────

def build_ui() -> gr.Blocks:
    with gr.Blocks(
        title="OCR 文字识别",
    ) as demo:
        gr.Markdown("# 📝 OCR 文字识别系统\n上传文档或截图，自动识别中英文文字")

        with gr.Row():
            # 左列：图片输入 + 标注输出
            with gr.Column():
                input_image = gr.Image(
                    label="上传图片",
                    type="pil",
                    height=400,
                    sources=["upload", "clipboard"],
                )
                recognize_btn = gr.Button("🔍 开始识别", variant="primary", size="lg")

            # 右列：标注结果图
            with gr.Column():
                output_image = gr.Image(label="识别标注结果", height=400)

        # 文本结果区域
        with gr.Row():
            with gr.Column():
                text_output = gr.Textbox(
                    label="识别文本",
                    lines=10,
                    placeholder="识别到的文字将显示在这里...",
                )

        # 详细表格
        detail_table = gr.Dataframe(
            headers=["序号", "识别文字", "置信度"],
            label="详细识别结果",
            interactive=False,
            wrap=True,
        )

        # 绑定按钮点击事件（点击按钮后开始识别）
        recognize_btn.click(
            fn=process_image,
            inputs=[input_image],
            outputs=[output_image, text_output, detail_table],
        )

    return demo


# ── 入口 ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo = build_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        theme=gr.themes.Soft(),
    )
