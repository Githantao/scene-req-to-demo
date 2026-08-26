#!/usr/bin/env python3
"""
render-markdown.py — Phase 4 输出 Markdown 六段式需求文档

Usage:
    # 标准：输出到 stdout
    cat input.json | python3 render-markdown.py > output.md

    # 自动命名：输出到指定目录，按 title 命名
    cat input.json | python3 render-markdown.py --output-dir ./output

Input (stdin JSON):
    { "analysis": { ... full skill output ... } }

Output: stdout 或 ./output/<title>.md
"""
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path


PRIORITY_LABELS = {"high": "高优", "medium": "中优", "low": "低优"}

SAFETY_HINTS = [
    "联锁", "进路", "道岔", "闭塞", "防护", "故障导向安全", "故障-安全", "SIL",
    "移动授权", "防护包络", "ATP", "ZC", "VOBC", "安全相关", "接近锁闭", "敌对进路",
]


def detect_safety(analysis: dict) -> bool:
    """True if any FR is safety-critical."""
    req = analysis.get("requirements", {})
    frs = req.get("functionalRequirements", [])
    if any(fr.get("safetyRelevance") == "安全相关" for fr in frs):
        return True
    text = req.get("title", "") + " " + " ".join(
        (fr.get("name", "") or "") + " " + (fr.get("description", "") or "") for fr in frs
    )
    return any(h in text for h in SAFETY_HINTS)


def _avoid_collision(out_path: Path) -> Path:
    """If target exists, append -2, -3, ... to avoid overwriting (P1-8)."""
    if not out_path.exists():
        return out_path
    stem, suffix = out_path.stem, out_path.suffix
    n = 2
    while True:
        cand = out_path.with_name(f"{stem}-{n}{suffix}")
        if not cand.exists():
            return cand
        n += 1


def render_markdown(analysis: dict) -> str:
    bc = analysis.get("businessContext", {})
    req = analysis.get("requirements", {})
    frs = req.get("functionalRequirements", [])
    layers = req.get("layers", {})

    high = sum(1 for fr in frs if fr.get("priority") == "high")
    medium = sum(1 for fr in frs if fr.get("priority") == "medium")
    low = sum(1 for fr in frs if fr.get("priority") == "low")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    md = []
    md.append(f"# {req.get('title', '未命名系统')}需求文档")
    md.append("")
    md.append(f"> 生成时间：{now} | 图表类型：{req.get('diagramType', 'flowchart')} | Skill: scene-req-to-demo v0.0.5")
    md.append("")

    if detect_safety(analysis):
        md.append("> ⚠️ **安全功能需求声明**：本文档含安全苛求功能（联锁/防护类）。")
        md.append("> 相关 FR 为**安全侧逻辑阐述**，安全系统本身无操作前端界面；")
        md.append("> 文中/Demo 中出现的界面元素仅用于阐述与评审，实际操作界面由非安全系统（ATS/CTC 等）承载。")
        md.append("")

    md.append("---")
    md.append("")

    # Section 1: Business background
    md.append("## 一、业务背景及目标")
    md.append("")
    md.append("### 提出方")
    md.append("")
    md.append(bc.get("proposer", "待明确"))
    md.append("")
    md.append("### 问题层级")
    md.append("")
    md.append(bc.get("problemLevel", "待明确"))
    md.append("")
    md.append("### 现状痛点")
    md.append("")
    md.append(bc.get("currentState", "待明确"))
    md.append("")
    md.append("### 解决层级")
    md.append("")
    md.append(bc.get("targetLevel", "待明确"))
    md.append("")
    md.append("### 预期成效")
    md.append("")
    md.append(bc.get("expectedBenefit", "待明确"))
    md.append("")
    md.append("---")
    md.append("")

    # Section 2: Overall requirement
    main_req = req.get("mainRequirement", {})
    md.append("## 二、总体需求")
    md.append("")
    md.append(f"> **{main_req.get('name', '未命名')}**")
    md.append(">")
    md.append(f"> {main_req.get('description', '待明确')}")
    md.append("")
    md.append(f"**系统边界**：{req.get('systemBoundary', '待明确')}")
    md.append("")
    stakeholders = req.get("stakeholders", [])
    md.append(f"**干系人**：{'、'.join(stakeholders) if stakeholders else '待明确'}")
    md.append("")
    md.append("### 三层需求")
    md.append("")
    md.append("| 层级 | 内容 |")
    md.append("|------|------|")
    b = layers.get("business", {})
    md.append(f"| 🏢 业务层 | **目标**：{b.get('goal', '待明确')} · **价值**：{b.get('value', '待明确')} |")
    u = layers.get("user", {})
    md.append(f"| 👤 用户层 | **场景**：{u.get('scenario', '待明确')} · **痛点**：{'；'.join(u.get('painPoints', [])) or '待明确'} |")
    s = layers.get("system", {})
    md.append(f"| ⚙️ 系统层 | **职责**：{s.get('summary', '待明确')} |")
    md.append("")
    md.append("---")
    md.append("")

    # Section 3: Functional requirements
    md.append("## 三、功能需求")
    md.append("")
    md.append(f"> 共 {len(frs)} 项功能，{high} 项高优 / {medium} 项中优 / {low} 项低优")
    md.append("")
    for fr in frs:
        prio_label = PRIORITY_LABELS.get(fr.get("priority"), "中优")
        sr = fr.get("safetyRelevance")
        sr_badge = f" `{sr}`" if sr else ""
        md.append(f"### {fr.get('id', '?')} {fr.get('name', '')} `{prio_label}`{sr_badge}")
        md.append("")
        md.append(fr.get("description", "待明确"))
        md.append("")
        cfg = "支持按项目配置" if fr.get("configurable") else "固定逻辑"
        md.append("| 锚点 | 内容 |")
        md.append("|------|------|")
        md.append(f"| 📍 页面位置 | {fr.get('uiLocation', '待明确')} |")
        md.append(f"| 🔗 数据来源 | {fr.get('dataSource', '待明确')} |")
        md.append(f"| ⚙️ 配置方式 | {cfg} |")
        md.append(f"| 🔘 默认状态 | {fr.get('defaultState', '待明确')} |")
        md.append(f"| 💡 示例 | {fr.get('example', '待明确')} |")
        if fr.get("acceptanceCriteria"):
            md.append(f"| ✅ 验收准则 | {fr.get('acceptanceCriteria')} |")
        md.append("")
    md.append("---")
    md.append("")

    # Section 4: Interfaces
    md.append("## 四、接口需求")
    md.append("")
    interfaces = req.get("interfaces", [])
    if interfaces:
        for it in interfaces:
            md.append(f"- {it}")
    else:
        md.append("无。")
        md.append("")
        md.append("> 本系统暂无外部接口依赖。")
    md.append("")
    md.append("---")
    md.append("")

    # Section 5: Data requirements
    md.append("## 五、数据需求")
    md.append("")
    data_reqs = req.get("dataRequirements", [])
    if data_reqs:
        for d in data_reqs:
            md.append(f"- {d}")
    else:
        md.append("无。")
    md.append("")
    md.append("**数据流**：")
    md.append("")
    md.append("| 来源 | 目标 | 数据 | 类型 |")
    md.append("|------|------|------|------|")
    for df in req.get("dataFlows", []):
        md.append(f"| {df.get('from', '?')} | {df.get('to', '?')} | {df.get('data', '?')} | {df.get('type', 'input')} |")
    md.append("")
    md.append("---")
    md.append("")

    # Section 6: Non-functional requirements
    md.append("## 六、非功能性需求")
    md.append("")
    nfrs = req.get("nonFunctionalRequirements", [])
    if nfrs:
        for n in nfrs:
            md.append(f"- {n}")
    else:
        md.append("无明确约束。")
        md.append("")
        md.append("> 建议后续补充性能/安全/可用性要求。")
    md.append("")
    md.append("> 标注说明：【硬性约束】为必须满足的条件，【假设】为待验证的前提")
    md.append("")
    md.append("---")
    md.append("")

    # Appendix A: Mermaid diagram
    md.append("## 附录 A：流程图")
    md.append("")
    md.append(f"> 图表类型：`{req.get('diagramType', 'flowchart')}`")
    md.append("")
    md.append("```mermaid")
    md.append(analysis.get("mermaidCode", "flowchart TD\n  A[待分析] --> B[开始]"))
    md.append("```")
    md.append("")
    md.append("---")
    md.append("")

    # Appendix B: JSON
    md.append("## 附录 B：结构化数据")
    md.append("")
    md.append("<details>")
    md.append("<summary>点击展开 JSON</summary>")
    md.append("")
    md.append("```json")
    md.append(json.dumps(analysis, ensure_ascii=False, indent=2))
    md.append("```")
    md.append("")
    md.append("</details>")
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"*本文档由 scene-req-to-demo 自动生成 | 渲染：Mermaid 11*")
    md.append("")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Render Markdown requirement doc")
    parser.add_argument("--output-dir", help="Output directory (auto-name by title)")
    args = parser.parse_args()

    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    analysis = input_data.get("analysis")
    if not analysis:
        print("Error: missing 'analysis' field", file=sys.stderr)
        sys.exit(1)

    md_text = render_markdown(analysis)

    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        title = analysis.get("requirements", {}).get("title", "未命名")
        title = title.replace(" ", "")
        out_path = _avoid_collision(out_dir / f"{title}.md")
        out_path.write_text(md_text, encoding="utf-8")
        fr_count = len(analysis.get("requirements", {}).get("functionalRequirements", []))
        safety = "含安全声明" if detect_safety(analysis) else "通用"
        print(f"✓ Markdown 需求文档 [{safety}] 覆盖 {fr_count} 项 FR", file=sys.stderr)
        print(str(out_path))
    else:
        print(md_text)


if __name__ == "__main__":
    main()
