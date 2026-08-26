#!/usr/bin/env python3
"""
analyze.py — Phase 1 场景分析入口

依据 Anthropic Agent Skills 的 progressive disclosure 模式：
- 脚本代码不进入 LLM context，仅 input/output JSON
- LLM 只负责"理解场景语义 + 选择结构"，校验/格式化由脚本完成

Usage:
    echo '{"scene": "..."}' | python3 analyze.py [--domain] [--output-format json|text]

Input (stdin JSON):
    {
      "scene": "自然语言场景描述",
      "scene_index": 1,  # optional, for batch collection
      "previous_scenes": [   # optional, for deduplication hints
        {"scene": "...", "summary": "..."}
      ]
    }

Output (stdout JSON):
    {
      "status": "ok" | "needs_clarification" | "duplicate_detected",
      "analysis": {
        "businessContext": {...},
        "requirements": {
          "title": "...",
          "mainRequirement": {...},
          "systemBoundary": "...",
          "stakeholders": [...],
          "functionalRequirements": [
            { 5 anchors + priority }
          ],
          "dataFlows": [...],
          "interfaces": [...],
      "dataRequirements": [...],
      "nonFunctionalRequirements": [...]
    },
      "notes": "..."   # optional clarification questions or duplicate warnings
    }

LLM Usage Notes (for the model invoking this script):
    1. Read scene text from stdin JSON
    2. Use analysis-prompt.md (assets/analysis-prompt.md) as GUIDANCE — do NOT
       paste its contents into context. Use it as a checklist for what to extract.
    3. Produce the `analysis` object with ALL 5 anchors per FR
    4. Call this script via shell exec OR return the analysis object directly
       (the LLM acts as the analyzer; this script is for validation/rendering)
"""
import json
import sys
import re
from pathlib import Path


# Domain keywords for railway/CBTC detection (lightweight — full glossary in domain-railway.md)
DOMAIN_KEYWORDS = [
    "铁路", "信号", "联锁", "进路", "道岔", "闭塞", "轨道电路",
    "CBTC", "TACS", "ZC", "VOBC", "DCS", "OC", "MA", "移动闭塞",
    "地铁", "城轨", "调度", "行车", "列控", "SIL", "T2T", "信号机", "轨旁",
]


def detect_domain(scene: str) -> dict:
    """Detect if scene contains railway/signal domain keywords."""
    hits = [kw for kw in DOMAIN_KEYWORDS if kw in scene]
    return {
        "matched": bool(hits),
        "keywords": hits,
        "needs_domain_rul": len(hits) > 0,
    }


def basic_quality_check(analysis: dict) -> dict:
    """Validate analysis structure. Returns errors + warnings."""
    errors = []
    warnings = []

    # businessContext
    bc = analysis.get("businessContext", {})
    for field in ["proposer", "problemLevel", "currentState", "targetLevel", "expectedBenefit"]:
        if not bc.get(field):
            errors.append(f"businessContext.{field} missing")

    # mainRequirement
    if not analysis.get("requirements", {}).get("mainRequirement"):
        errors.append("requirements.mainRequirement missing")

    # functionalRequirements
    frs = analysis.get("requirements", {}).get("functionalRequirements", [])
    if not (2 <= len(frs) <= 6):
        errors.append(f"functionalRequirements count {len(frs)} not in [2, 6]")

    # 5 anchors per FR
    required_anchors = ["uiLocation", "dataSource", "configurable", "defaultState", "example"]
    for fr in frs:
        for anchor in required_anchors:
            val = fr.get(anchor)
            # Distinguish missing (None) from valid False (e.g., configurable=false is valid)
            if val is None:
                errors.append(f"{fr.get('id', '?')} missing anchor: {anchor}")
            elif isinstance(val, str) and val.strip() in ("", "待明确"):
                warnings.append(f"{fr.get('id', '?')} anchor '{anchor}' is placeholder")

    # priority valid
    valid_priorities = {"high", "medium", "low"}
    for fr in frs:
        if fr.get("priority") not in valid_priorities:
            errors.append(f"{fr.get('id', '?')} invalid priority: {fr.get('priority')}")

    # interface/dataRequirements empty arrays (must be present)
    req = analysis.get("requirements", {})
    if "interfaces" not in req:
        warnings.append("interfaces missing — should be [] if none")
    if "dataRequirements" not in req:
        warnings.append("dataRequirements missing — should be [] if none")

    return {"errors": errors, "warnings": warnings}


def is_duplicate(new_analysis: dict, previous_scenes: list) -> dict:
    """Light duplicate detection by FR name overlap."""
    if not previous_scenes:
        return {"is_duplicate": False, "overlapping_frs": []}

    new_fr_names = {fr["name"] for fr in new_analysis.get("requirements", {}).get("functionalRequirements", [])}
    overlapping = []
    for prev in previous_scenes:
        prev_summary = prev.get("summary", "")
        prev_frs = prev.get("functionalRequirements", [])
        for fr_name in new_fr_names:
            for pfr in prev_frs:
                if pfr.get("name") == fr_name:
                    overlapping.append({"name": fr_name, "in_prev_scene": prev_summary[:60]})
    return {
        "is_duplicate": len(overlapping) > 0,
        "overlapping_frs": overlapping,
    }


def render_text_output(result: dict) -> str:
    """Human-readable per-scene confirmation text (the 'Phase 1 short version' shown to user)."""
    if result["status"] == "needs_clarification":
        return f"❌ 需要澄清: {result.get('notes', '请补充信息')}"

    a = result.get("analysis", {})
    req = a.get("requirements", {})
    bc = a.get("businessContext", {})

    lines = []
    lines.append(f"【需求名称】{req.get('title', '未命名系统')}")
    lines.append("")
    lines.append(f"【总体需求】{req.get('mainRequirement', {}).get('name', '')}：{req.get('mainRequirement', {}).get('description', '')}")
    lines.append("")
    lines.append("【功能需求】")

    frs = req.get("functionalRequirements", [])
    for i, fr in enumerate(frs, 1):
        prio_label = {"high": "高优", "medium": "中优", "low": "低优"}[fr.get("priority", "medium")]
        lines.append(f"  {fr.get('id', f'FR-{i}')} {fr.get('name', '')}（{prio_label}）")
        lines.append(f"   {fr.get('description', '')}")
        cfg = "支持按项目配置" if fr.get("configurable") else "固定逻辑"
        lines.append(f"   位置：{fr.get('uiLocation', '待明确')}；数据：{fr.get('dataSource', '待明确')}；{cfg}，{fr.get('defaultState', '待明确')}。")
        lines.append(f"   例如：{fr.get('example', '待明确')}")
        lines.append("")

    lines.append(f"（共 {len(frs)} 项）")

    if result.get("notes"):
        lines.append("")
        lines.append(f"备注：{result['notes']}")

    return "\n".join(lines)


def main():
    output_format = "json"
    args = sys.argv[1:]
    if "--output-format" in args:
        idx = args.index("--output-format")
        output_format = args[idx + 1]

    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        result = {"status": "error", "error": f"Invalid JSON input: {e}"}
        print(json.dumps(result, ensure_ascii=False) if output_format == "json" else f"Error: {e}")
        sys.exit(1)

    scene = input_data.get("scene", "").strip()
    if not scene:
        result = {"status": "error", "error": "scene is empty"}
        print(json.dumps(result, ensure_ascii=False) if output_format == "json" else "Error: scene is empty")
        sys.exit(1)

    # Pre-check: domain detection
    domain_info = detect_domain(scene)
    # Length/complexity check
    is_complex = len(scene) > 50 or any(
        kw in scene for kw in ["同时", "此外", "并且", "另外", "以及", "且", "不但", "而且", "不仅", "还有"]
    )

    # The LLM is expected to produce the analysis object.
    # This script's role is:
    # 1. Validate the LLM-produced analysis (errors/warnings)
    # 2. Detect domain
    # 3. Detect duplicates across scenes
    # 4. Render text output for human confirmation

    analysis = input_data.get("analysis")
    if not analysis:
        # LLM has not yet produced — return instructions for LLM
        result = {
            "status": "needs_llm_analysis",
            "domain_info": domain_info,
            "is_complex_scene": is_complex,
            "instructions": "LLM: analyze the scene using assets/analysis-prompt.md as guidance. Produce a JSON object conforming to the schema. Then call this script with the analysis in the input.",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2) if output_format == "json" else str(result))
        return

    # Validate
    qc = basic_quality_check(analysis)
    if qc["errors"]:
        result = {
            "status": "needs_correction",
            "errors": qc["errors"],
            "warnings": qc["warnings"],
            "domain_info": domain_info,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2) if output_format == "json" else str(result))
        sys.exit(1)

    # Duplicate check
    dup = is_duplicate(analysis, input_data.get("previous_scenes", []))

    result = {
        "status": "ok" if not dup["is_duplicate"] else "duplicate_detected",
        "domain_info": domain_info,
        "is_complex_scene": is_complex,
        "duplicate_info": dup,
        "warnings": qc["warnings"],
        "analysis": analysis,
    }

    if output_format == "text":
        print(render_text_output(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
