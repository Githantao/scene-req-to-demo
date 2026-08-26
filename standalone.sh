#!/bin/bash
# scene-req-to-demo: 独立执行脚本（不依赖 agent skill 机制）
# 用法:
#   ./standalone.sh <input.json>          # 单场景
#   ./standalone.sh <merged.json>         # 已合并的多场景
#
# 示例:
#   ./standalone.sh ./output/综合看板.json
#   ./standalone.sh ./output/merged.json

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/assets/scripts" && pwd)"
INPUT="${1:?用法: $0 <input.json>}"
OUTPUT_DIR="./output"

if [ ! -f "$INPUT" ]; then
    echo "错误: 文件不存在 $INPUT"
    echo ""
    echo "请先准备 JSON 文件。参考 $SCRIPT_DIR/README.md 的 schema。"
    echo "或在 AI agent 对话中描述场景，让 agent 生成 JSON。"
    exit 1
fi

echo "=== scene-req-to-demo v0.0.3 ==="
echo "输入: $INPUT"
echo "输出目录: $OUTPUT_DIR"
echo ""

# Phase 1: 分析验证
echo "--- Phase 1: analyze.py ---"
RESULT=$(python3 "$SCRIPT_DIR/analyze.py" < "$INPUT")
STATUS=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['status'])")
echo "$RESULT" | python3 -c "
import json, sys
r = json.load(sys.stdin)
print(f'  status: {r[\"status\"]}')
if r.get('warnings'):
    for w in r['warnings']:
        print(f'  warning: {w}')
"
if [ "$STATUS" = "needs_correction" ]; then
    echo "  ✗ 需要修正 JSON 后重新运行"
    exit 1
fi

# Phase 3: 锚点验证
echo ""
echo "--- Phase 3: validate-anchors.py ---"
python3 "$SCRIPT_DIR/validate-anchors.py" < "$INPUT" | python3 -c "
import json, sys
r = json.load(sys.stdin)
print(f'  status: {r[\"status\"]}')
for k, v in r['checks'].items():
    print(f'    {k}: {v}')
"

# Phase 4: 渲染产物（路径由脚本控制）
echo ""
echo "--- Phase 4: render-markdown.py ---"
MD_PATH=$(python3 "$SCRIPT_DIR/render-markdown.py" --output-dir "$OUTPUT_DIR" < "$INPUT")
echo "  ✓ $MD_PATH ($(wc -c < "$MD_PATH" | tr -d ' ') bytes)"

echo ""
echo "--- Phase 4: render-demo.py ---"
HTML_PATH=$(python3 "$SCRIPT_DIR/render-demo.py" --output-dir "$OUTPUT_DIR" < "$INPUT")
echo "  ✓ $HTML_PATH ($(wc -c < "$HTML_PATH" | tr -d ' ') bytes)"

echo ""
echo "=== 完成 ==="
echo "  Markdown: $MD_PATH"
echo "  Demo: $HTML_PATH (双击 Chrome 打开)"
