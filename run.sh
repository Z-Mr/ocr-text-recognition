#!/usr/bin/env bash
#
# run.sh —— 启动 OCR Web 界面
#

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

# 激活虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "[错误] 虚拟环境不存在，请先运行: bash setup.sh"
    exit 1
fi

source "$VENV_DIR/bin/activate"

echo "正在启动 OCR Web 界面..."
echo "浏览器将自动打开，或访问: http://127.0.0.1:7860"
echo "按 Ctrl+C 停止服务"
echo ""

python "$PROJECT_DIR/app.py"
