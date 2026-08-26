#!/usr/bin/env python3
"""
build-creative.py — Phase 4b 创意版 Demo 组装 + 冒烟测试

把"机械活"从 LLM 手里摘掉：
- LLM 只写带 `<!--__INJECT_VUE__-->` 占位符的 HTML（不必手写 164KB Vue 内联）
- 本脚本注入 `vendor/vue.global.prod.js` 运行时，产出完全自包含单文件
- 自动对所有内联 <script> 跑 `node --check` 冒烟测试，有错大声报错，禁止静默出货

Usage:
    python3 build-creative.py --input creative-template.html --output ./output/<标题>-creative.html
    cat creative-template.html | python3 build-creative.py --output ./output/<标题>-creative.html

Placeholder:
    在 HTML 中需要引入 Vue 的位置写一行： <!--__INJECT_VUE__-->

Exit codes:
    0 — 组装成功且冒烟测试通过（或无 node 时降级通过并告警）
    1 — 冒烟测试发现语法错误（不产出文件）
    2 — 输入缺少占位符 / 文件不存在
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
VENDOR_DIR = SCRIPT_DIR / "vendor"
PLACEHOLDER = "<!--__INJECT_VUE__-->"


def load_vue() -> str:
    vue_path = VENDOR_DIR / "vue.global.prod.js"
    return vue_path.read_text(encoding="utf-8")


def extract_inline_scripts(html: str) -> list:
    """Extract inline <script> bodies (exclude external src scripts)."""
    scripts = []
    for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.DOTALL):
        body = m.group(1).strip()
        if body:
            scripts.append(body)
    return scripts


def smoke_test(html: str) -> tuple:
    """Run node --check on concatenated inline scripts. Returns (passed, message)."""
    scripts = extract_inline_scripts(html)
    if not scripts:
        return True, "no inline scripts to check"

    if shutil.which("node") is None:
        return True, "WARNING: node not found — skipped JS syntax check (install Node for smoke test)"

    combined = "\n;\n".join(scripts)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(combined)
        tmp = Path(f.name)
    try:
        proc = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            return False, proc.stderr.strip() or "node --check failed"
        return True, f"node --check passed ({len(scripts)} inline script block(s))"
    except subprocess.TimeoutExpired:
        return False, "node --check timed out"
    finally:
        tmp.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Build self-contained creative Demo + smoke test")
    parser.add_argument("--input", help="HTML template with <!--__INJECT_VUE__--> placeholder (default: stdin)")
    parser.add_argument("--output", required=True, help="Output path for self-contained HTML")
    parser.add_argument("--skip-smoke", action="store_true", help="Skip node --check (not recommended)")
    args = parser.parse_args()

    if args.input:
        in_path = Path(args.input)
        if not in_path.exists():
            print(f"Error: input not found: {args.input}", file=sys.stderr)
            sys.exit(2)
        template = in_path.read_text(encoding="utf-8")
    else:
        template = sys.stdin.read()

    if PLACEHOLDER not in template:
        print(f"Error: placeholder '{PLACEHOLDER}' not found in input. "
              f"LLM 必须在需要引入 Vue 的位置写该占位符。", file=sys.stderr)
        sys.exit(2)

    vue_js = load_vue()
    html = template.replace(PLACEHOLDER, "<script>" + vue_js + "</script>")

    # Smoke test BEFORE writing output (fail loud, never silent-ship)
    if not args.skip_smoke:
        passed, msg = smoke_test(html)
        if not passed:
            print("❌ 冒烟测试失败（node --check）— 未产出文件，请修复内联 JS 语法：", file=sys.stderr)
            print(msg, file=sys.stderr)
            sys.exit(1)
        print(f"✓ smoke: {msg}", file=sys.stderr)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
