# OCR 文字识别系统

基于 PaddleOCR 3.x + Gradio 构建的本地 OCR 文字识别工具，支持中英文混合识别，提供 Web 界面进行图片文字提取。

## 功能特性

- 中英文混合文字识别
- 拖拽上传图片或使用剪贴板粘贴
- 识别结果可视化（绿色框标注文字区域）
- 纯文本输出，可直接复制
- 详细识别结果表格（含置信度）
- 完全本地运行，无需联网（首次需下载模型）

## 环境要求

- Python 3.11 或 3.12（PaddlePaddle 暂不支持 3.13+）
- macOS / Linux / Windows
- 约 500MB 磁盘空间（模型 + 依赖）

## 快速开始

### 1. 一键初始化环境

```bash
bash setup.sh
```

该脚本会自动完成以下操作：

- 检测并安装兼容的 Python 版本（3.11/3.12）
- 创建虚拟环境（`.venv/`）
- 使用清华镜像源安装所有依赖

### 2. 启动服务

```bash
bash run.sh
```

浏览器会自动打开 `http://127.0.0.1:7860`。

### 3. 开始识别

1. 在左侧上传区域拖入图片，或从剪贴板粘贴
2. 点击「开始识别」按钮
3. 右侧查看标注结果图，下方查看识别文本和详细置信度

## 项目结构

```
OCR-project/
├── app.py              # Gradio Web 界面入口
├── ocr_engine.py       # OCR 核心引擎（封装 PaddleOCR 3.x）
├── requirements.txt    # Python 依赖列表
├── setup.sh            # 一键环境初始化脚本
├── run.sh              # 一键启动脚本
├── models/             # 本地模型文件（首次运行后自动缓存）
│   ├── PP-LCNet_x1_0_doc_ori/       # 文档方向分类模型
│   ├── PP-LCNet_x1_0_textline_ori/  # 文本行方向分类模型
│   ├── PP-OCRv5_server_det/         # 文字检测模型
│   ├── PP-OCRv5_server_rec/         # 文字识别模型
│   └── UVDoc/                       # 文档去弯曲模型
├── .gitignore          # Git 忽略规则
└── README.md           # 本文档
```

## 技术栈

| 组件 | 说明 |
|------|------|
| PaddleOCR 3.x | 百度出品的 OCR 引擎，含文字检测（PP-OCRv5）、方向分类、文字识别三个子模型 |
| PaddlePaddle | 深度学习框架，PaddleOCR 的运行时依赖 |
| Gradio 6.x | Web UI 框架，提供图片上传、文本展示等交互组件 |
| Pillow | 图像处理库，用于绘制识别标注框 |

## 常见问题

### Q: 首次识别很慢？

如果项目 `models/` 目录下已有模型文件，启动几乎是即时的。若模型文件缺失，PaddleOCR 会自动从 ModelScope 下载（约 200MB），下载完成后后续使用无需再下载。

### Q: pip 安装依赖失败？

国内网络访问 PyPI 可能超时，setup.sh 已默认使用清华镜像源。如仍失败，可手动指定：

```bash
source .venv/bin/activate
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
```

### Q: 标注图上的中文显示为方块？

系统缺少中文字体时会回退到默认字体。macOS 通常自带苹方字体（PingFang），Linux 可安装文泉驿或 Noto CJK 字体。

### Q: 识别准确率不高？

- 确保图片中文字清晰、对比度足够
- 倾斜角度较大的文字可能需要先做预处理
- 手写体识别效果不如印刷体

## 模型管理

项目内置了 `models/` 目录存放所有子模型，引擎启动时会优先读取本地模型，无需联网下载。模型来源说明：

- **自动获取**：首次启动时，PaddleOCR 会自动从 ModelScope 下载模型（约 200MB）到 `~/.paddlex/official_models/`
- **本地化**：运行 `setup.sh` 时会自动将缓存的模型拷贝到项目 `models/` 目录
- **手动拷贝**：如需在无网络环境部署，将 `models/` 目录整体拷贝到目标机器的项目目录下即可

## 离线使用

本项目支持完全离线运行。模型和所有依赖均存放于项目本地目录（`models/` 和 `.venv/`），无需联网即可完成文字识别。

## License

MIT
