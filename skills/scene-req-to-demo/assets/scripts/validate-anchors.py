#!/usr/bin/env python3
"""
validate-anchors.py — Phase 3 合并后验证

Usage:
    cat merged-result.json | python3 validate-anchors.py

Input (stdin JSON):
    {
      "analysis": { ... full skill output schema ... },
      "previous_scenes": [...]  # optional, for cross-scene dedup
    }

Output (stdout JSON):
    {
      "status": "ok" | "warnings" | "errors",
      "checks": {
        "5_anchors_per_fr": "ok" | "warning: ...missing",
        "6_section_completeness": "ok" | "warning: ...",
        "batch_dedup": "ok" | "warning: overlapping FRs ...",
        "demo_readiness": "ok" | "warning: <3 FRs",
        "cove_consistency": "ok" | "warning: ...",
        "safety_and_acceptance": "ok" | "warning: ...",
        "configurable_distribution": "ok" | "warning: ...",
        "gap_discipline": "ok" | "warning: ..."
      },
      "errors": [...],
      "warnings": [...],
      "summary": "..."
    }
"""
import json
import sys


REQUIRED_ANCHORS = ["uiLocation", "dataSource", "configurable", "defaultState", "example"]
REQUIRED_SECTIONS = {
    "businessContext": ["proposer", "problemLevel", "currentState", "targetLevel", "expectedBenefit"],
    "functionalRequirements": ["id", "name", "description", "priority", "uiLocation", "dataSource", "configurable", "defaultState", "example"],
}


def check_anchors(analysis):
    errors = []
    warnings = []
    frs = analysis.get("requirements", {}).get("functionalRequirements", [])
    if not frs:
        errors.append("No functionalRequirements found")
        return errors, warnings

    for fr in frs:
        fid = fr.get("id", "?")
        for anchor in REQUIRED_ANCHORS:
            val = fr.get(anchor)
            if val is None:
                errors.append(f"{fid}: missing anchor '{anchor}'")
            elif isinstance(val, str) and val.strip() in ("", "待明确"):
                warnings.append(f"{fid}: anchor '{anchor}' is placeholder")
        # priority enum check
        if fr.get("priority") not in ("high", "medium", "low"):
            errors.append(f"{fid}: invalid priority '{fr.get('priority')}'")

    # FR count
    if len(frs) < 2:
        warnings.append(f"Only {len(frs)} FR — Demo will be sparse (recommend ≥3)")
    if len(frs) > 6:
        warnings.append(f"{len(frs)} FRs — exceeds recommended max (6)")

    return errors, warnings


def check_six_sections(analysis):
    errors = []
    warnings = []
    req = analysis.get("requirements", {})

    if not req.get("mainRequirement"):
        errors.append("missing mainRequirement")

    if not req.get("systemBoundary"):
        warnings.append("missing systemBoundary — should describe what's in/out of scope")

    if "interfaces" not in req:
        warnings.append("missing interfaces field — should be [] if none")
    if "dataRequirements" not in req:
        warnings.append("missing dataRequirements field — should be [] if none")

    if not req.get("nonFunctionalRequirements"):
        warnings.append("missing nonFunctionalRequirements — should label each as 【硬性约束】or【假设】")

    # Layers
    layers = req.get("layers", {})
    for layer in ("business", "user", "system"):
        if layer not in layers or not layers[layer]:
            warnings.append(f"missing layers.{layer}")

    return errors, warnings


def check_batch_dedup(analysis, previous_scenes):
    warnings = []
    if not previous_scenes:
        return warnings

    current_fr_names = {
        fr.get("name"): fr.get("id")
        for fr in analysis.get("requirements", {}).get("functionalRequirements", [])
    }

    overlapping = []
    for prev in previous_scenes:
        for pfr in prev.get("functionalRequirements", []):
            pname = pfr.get("name")
            if pname in current_fr_names:
                overlapping.append({
                    "name": pname,
                    "current_id": current_fr_names[pname],
                    "from_scene": prev.get("scene_summary", "")[:50],
                })
    if overlapping:
        warnings.append(f"{len(overlapping)} FR(s) overlap with previous scenes — consider merging or renaming")

    return warnings


def check_cove_consistency(analysis):
    """Light CoVe: hallucination / omission / over-decomposition checks."""
    warnings = []
    req = analysis.get("requirements", {})
    frs = req.get("functionalRequirements", [])
    main_req = req.get("mainRequirement", {})

    # Each FR should trace back to mainRequirement
    if not main_req.get("description"):
        warnings.append("mainRequirement description empty — FRs cannot be traced")

    # Over-decomposition: detect UI-step language
    ui_step_kws = ["显示", "点击", "打开", "刷新", "跳转", "切换", "弹出"]
    for fr in frs:
        desc = fr.get("description", "")
        if desc.startswith("点击") or desc.startswith("显示"):
            warnings.append(f"{fr.get('id')}: description looks like UI step, not business capability")

    # Each priority: roughly 60% high, 30% medium, 10% low is healthy
    if frs:
        high_pct = sum(1 for fr in frs if fr.get("priority") == "high") / len(frs)
        if high_pct > 0.8:
            warnings.append(f"{int(high_pct*100)}% FRs are high priority — consider re-prioritizing")

    return warnings


def check_demo_readiness(analysis):
    """Check if merged result has enough material for a meaningful Demo."""
    warnings = []
    frs = analysis.get("requirements", {}).get("functionalRequirements", [])
    if len(frs) < 3:
        warnings.append(f"Only {len(frs)} FR — Demo will be sparse. Consider batch-collecting more scenes.")
    return warnings


def check_safety_and_acceptance(analysis):
    """Validate safetyRelevance + acceptanceCriteria fields (P1 FR extension)."""
    warnings = []
    frs = analysis.get("requirements", {}).get("functionalRequirements", [])

    has_safety_field = any("safetyRelevance" in fr for fr in frs)
    has_ac_field = any("acceptanceCriteria" in fr for fr in frs)

    if frs and not has_safety_field:
        warnings.append("no FR carries 'safetyRelevance' — mark each FR as 安全相关/非安全相关 (drives Demo safety banner)")
    if frs and not has_ac_field:
        warnings.append("no FR carries 'acceptanceCriteria' — add testable acceptance criteria per FR")

    for fr in frs:
        fid = fr.get("id", "?")
        sr = fr.get("safetyRelevance")
        if sr is not None and sr not in ("安全相关", "非安全相关"):
            warnings.append(f"{fid}: safetyRelevance should be '安全相关' or '非安全相关', got '{sr}'")
        # safety FR should not promise a concrete UI as its deliverable
        if sr == "安全相关":
            loc = fr.get("uiLocation", "")
            if any(w in loc for w in ("页面", "界面", "弹窗", "大屏")):
                warnings.append(f"{fid}: 安全相关 FR 的 uiLocation 指向界面 — 安全系统无操作前端，应为逻辑阐述（实际界面由非安全系统提供）")
    return warnings


def check_configurable_distribution(analysis):
    """WorkBuddy P1-5: configurable 防摆设 — 全是 true 提示复核."""
    warnings = []
    frs = analysis.get("requirements", {}).get("functionalRequirements", [])
    if len(frs) >= 3:
        true_pct = sum(1 for fr in frs if fr.get("configurable") is True) / len(frs)
        if true_pct >= 1.0:
            warnings.append("100% FRs configurable=true — 复核是否有固定逻辑应为 false（可加 configReason 说明）")
    return warnings


def check_gap_discipline(analysis):
    """GAP 纪律: 量化指标无来源标注 → 提示标 [假设]/[GAP]，防编造."""
    import re
    warnings = []
    req = analysis.get("requirements", {})
    frs = req.get("functionalRequirements", [])
    nfrs = req.get("nonFunctionalRequirements", [])

    # 量化指标模式：响应时间/百分比/次数/THR 等
    metric_re = re.compile(r"(≤|>=?|＜|＞|<|>)\s*\d|(\d+(\.\d+)?\s*(%|％|s|秒|ms|毫秒|次|条|个))|10⁻|10\^-")

    def scan(text, where):
        if not isinstance(text, str):
            return
        if metric_re.search(text) and "[假设]" not in text and "[GAP]" not in text and "【假设】" not in text:
            warnings.append(f"{where}: 含量化指标但未标 [假设]/[GAP] — 无依据的数值禁止编造，请标注来源或标 [假设]")

    for fr in frs:
        scan(fr.get("description", ""), f"{fr.get('id', '?')}.description")
        scan(fr.get("example", ""), f"{fr.get('id', '?')}.example")
    for i, nfr in enumerate(nfrs, 1):
        scan(nfr, f"NFR-{i}")

    # 去重：同类提示只保留前若干条
    return warnings[:6]


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "errors": [f"Invalid JSON: {e}"]}, ensure_ascii=False))
        sys.exit(1)

    analysis = input_data.get("analysis")
    if not analysis:
        print(json.dumps({"status": "error", "errors": ["missing 'analysis' field"]}, ensure_ascii=False))
        sys.exit(1)

    all_errors = []
    all_warnings = []
    checks = {}

    e, w = check_anchors(analysis)
    all_errors.extend(e)
    all_warnings.extend(w)
    checks["5_anchors_per_fr"] = "ok" if not e else f"errors: {len(e)}"

    e, w = check_six_sections(analysis)
    all_errors.extend(e)
    all_warnings.extend(w)
    checks["6_section_completeness"] = "ok" if not e else f"errors: {len(e)}"

    w = check_batch_dedup(analysis, input_data.get("previous_scenes", []))
    all_warnings.extend(w)
    checks["batch_dedup"] = "ok" if not w else f"{len(w)} overlaps"

    w = check_cove_consistency(analysis)
    all_warnings.extend(w)
    checks["cove_consistency"] = "ok" if not w else f"{len(w)} issues"

    w = check_demo_readiness(analysis)
    all_warnings.extend(w)
    checks["demo_readiness"] = "ok" if not w else f"{len(w)} notes"

    w = check_safety_and_acceptance(analysis)
    all_warnings.extend(w)
    checks["safety_and_acceptance"] = "ok" if not w else f"{len(w)} notes"

    w = check_configurable_distribution(analysis)
    all_warnings.extend(w)
    checks["configurable_distribution"] = "ok" if not w else f"{len(w)} notes"

    w = check_gap_discipline(analysis)
    all_warnings.extend(w)
    checks["gap_discipline"] = "ok" if not w else f"{len(w)} notes"

    if all_errors:
        status = "errors"
    elif all_warnings:
        status = "warnings"
    else:
        status = "ok"

    result = {
        "status": status,
        "checks": checks,
        "errors": all_errors,
        "warnings": all_warnings,
        "summary": f"{status.upper()}: {len(all_errors)} errors, {len(all_warnings)} warnings",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if status != "errors" else 1)


if __name__ == "__main__":
    main()
