#!/bin/bash
# ── Git 代理自动配置 ──
# 用法: bash git_proxy_setup.sh
# 自动检测 SDKDNS 代理端口并配置 git

echo "🔍 正在扫描代理端口..."

# SDKDNS 的代理进程名
PID=$(tasklist //FI "IMAGENAME eq com.vortex.helper.exe" //FO CSV 2>/dev/null \
    | tail -1 | cut -d, -f2 | tr -d '"' | tr -d ' ')

if [ -z "$PID" ]; then
    echo "❌ 未找到 com.vortex.helper.exe（梯子可能没开）"
    exit 1
fi

# 查它监听的端口（排除 39797 内部端口）
PORT=$(netstat -ano | grep "$PID" | grep LISTENING \
    | grep -v "39797" | awk '{print $2}' | cut -d: -f2 | head -1)

if [ -z "$PORT" ]; then
    echo "❌ 未找到外部监听端口"
    exit 1
fi

echo "✓ 找到代理: 127.0.0.1:$PORT"

# 配 git
git config --global http.proxy "http://127.0.0.1:$PORT"
git config --global https.proxy "http://127.0.0.1:$PORT"

echo "✓ Git 代理已设为 127.0.0.1:$PORT"
echo ""
echo "当前代理配置:"
git config --global --list | grep proxy
