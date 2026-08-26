#!/bin/bash
# scene-req-to-demo: 一键执行 pipeline
# 用法: ./run.sh '场景描述'
# 示例: ./run.sh '综合看板中央区域显示管辖图&数据分析图'

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/assets/scripts" && pwd)"
SCENE="${1:?用法: $0 '场景描述'}"

echo "=== scene-req-to-demo v0.0.3 ==="
echo "场景: $SCENE"
echo ""

# Step 1: 生成 JSON（这里需要手动构建，或用 LLM 辅助）
if [ ! -f ./output/merged.json ] && [ ! -f /tmp/srt-input.json ]; then
    echo "请先准备 ./output/merged.json 或 /tmp/srt-input.json（参考 SKILL.md 的 schema）"
    echo "或在此对话中让我帮你生成。"
    exit 1
fi
INPUT="./output/merged.json"
[ -f "$INPUT" ] || INPUT="/tmp/srt-input.json"

# Step 2: 验证
echo "--- analyze.py ---"
python3 "$SCRIPT_DIR/analyze.py" < "$INPUT"

# Step 3: 验证 anchors
echo ""
echo "--- validate-anchors.py ---"
python3 "$SCRIPT_DIR/validate-anchors.py" < "$INPUT"

# Step 4: 生成产物（双轨 Demo）
echo ""
echo "--- render-markdown.py ---"
python3 "$SCRIPT_DIR/render-markdown.py" --output-dir ./output < "$INPUT"

echo ""
echo "--- render-demo.py (约束版) ---"
python3 "$SCRIPT_DIR/render-demo.py" --output-dir ./output < "$INPUT"

echo ""
echo "=== 完成 ==="
ls -la ./output/*.md ./output/*.html 2>/dev/null | head -10
