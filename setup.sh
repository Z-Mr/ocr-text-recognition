#!/usr/bin/env bash
#
# setup.sh —— OCR 项目一键环境搭建脚本
# 功能：安装 Python 3.11（如果不存在）、创建虚拟环境、安装依赖
#

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON_VERSION="3.11"

echo "============================================"
echo "  OCR 文字识别项目 - 环境初始化"
echo "============================================"

# ── 1. 检查是否已有兼容的 Python 版本 ──────────────────────────────────────

find_python() {
    # 按优先级查找 python3.11 或 python3.12
    for ver in 3.11 3.12; do
        for candidate in \
            "python$ver" \
            "/opt/homebrew/bin/python$ver" \
            "/usr/local/bin/python$ver" \
            "/Library/Frameworks/Python.framework/Versions/$ver/bin/python3"; do
            if command -v "$candidate" &>/dev/null || [ -x "$candidate" ]; then
                echo "$candidate"
                return 0
            fi
        done
    done
    return 1
}

PYTHON_BIN=$(find_python || true)

if [ -z "$PYTHON_BIN" ]; then
    echo ""
    echo "[!] 未找到 Python 3.11 或 3.12，PaddlePaddle 暂不支持 Python 3.13+"
    echo ""
    echo "请选择安装方式："
    echo "  1) 通过 Homebrew 安装 Python 3.11（推荐，需要已安装 Homebrew）"
    echo "  2) 手动安装（从 python.org 下载 Python 3.11）"
    echo ""
    read -p "请输入选项 [1/2] (默认 1): " choice
    choice=${choice:-1}

    if [ "$choice" = "1" ]; then
        echo "正在通过 Homebrew 安装 Python 3.11..."
        if ! command -v brew &>/dev/null; then
            echo "[错误] 未检测到 Homebrew，请先安装 Homebrew："
            echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            exit 1
        fi
        brew install python@3.11
        PYTHON_BIN="/opt/homebrew/bin/python3.11"
        echo "Python 3.11 安装完成！"
    else
        echo "请从以下地址下载并安装 Python 3.11："
        echo "  https://www.python.org/downloads/"
        echo "安装完成后，重新运行本脚本。"
        exit 1
    fi
fi

echo "[✓] 使用 Python: $PYTHON_BIN ($($PYTHON_BIN --version))"

# ── 2. 创建虚拟环境 ────────────────────────────────────────────────────────

if [ -d "$VENV_DIR" ]; then
    echo "[i] 虚拟环境已存在，跳过创建"
else
    echo "正在创建虚拟环境..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
    echo "[✓] 虚拟环境已创建: $VENV_DIR"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# ── 3. 安装依赖 ──────────────────────────────────────────────────────────────

echo "正在安装依赖（首次安装可能需要几分钟，使用清华镜像源加速）..."
pip install --upgrade pip -q -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r "$PROJECT_DIR/requirements.txt"

echo ""
echo "============================================"
echo "  环境初始化完成！"
echo ""
echo "  启动项目请运行："
echo "    source .venv/bin/activate"
echo "    python app.py"
echo ""
echo "  或直接运行: ./run.sh"
echo "============================================"
