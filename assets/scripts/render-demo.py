#!/usr/bin/env python3
"""
render-demo.py — Phase 4 输出业务系统前端原型 Demo HTML (混合方案)

生成业务系统框架：一个页面承载所有 FR，FR 间协作关系体现在界面布局中。
LLM 可通过 SKILL.md 指令补充交互细节。

Usage:
    cat input.json | python3 render-demo.py --output-dir ./output

Input (stdin JSON):
    { "analysis": { ... full skill output ... } }

Output: stdout 或 ./output/<title>.html
"""
import json
import sys
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
VENDOR_DIR = SCRIPT_DIR / "vendor"


def load_vue() -> str:
    vue_path = VENDOR_DIR / "vue.global.prod.js"
    return vue_path.read_text(encoding="utf-8")


DESIGN_TOKENS_CSS = """
:root {
  --bg-primary: #0a1e3c;
  --bg-card: #132a4a;
  --bg-card-hover: #1a3658;
  --bg-header: #0d2445;
  --bg-sidebar: #0e2a4e;
  --bg-input: #1a3658;
  --border: #1e4a7a;
  --text-primary: #e0f0ff;
  --text-secondary: #7a9ab8;
  --text-muted: #4a6a8a;
  --accent-cyan: #00d4ff;
  --status-red: #ff3b30;
  --status-orange: #ff9500;
  --status-yellow: #ffcc00;
  --status-blue: #007aff;
  --status-green: #34c759;
  --radius-md: 8px;
  --shadow-card: 0 4px 24px rgba(0,0,0,0.4);
  --shadow-glow: 0 0 20px rgba(0,212,255,0.15);
}
* { box-sizing: border-box; }
body { margin:0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang SC',sans-serif; background:var(--bg-primary); color:var(--text-primary); line-height:1.7; font-size:14px; }
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--bg-primary); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
.proto-header { display:flex; align-items:center; justify-content:space-between; padding:10px 20px; background:var(--bg-header); border-bottom:1px solid var(--border); position:sticky; top:0; z-index:100; }
.proto-header h1 { font-size:16px; font-weight:700; margin:0; color:var(--text-primary); }
.proto-header .ver { font-size:10px; background:var(--accent-cyan); color:#001a2e; padding:2px 8px; border-radius:4px; margin-left:10px; font-weight:600; }
.proto-header .user-info { font-size:11px; color:var(--text-muted); }
.proto-toolbar { display:flex; align-items:center; gap:8px; flex-wrap:wrap; background:var(--bg-card); border-bottom:1px solid var(--border); padding:8px 20px; }
.proto-toolbar select { background:var(--bg-input); border:1px solid var(--border); border-radius:6px; color:var(--text-primary); font-size:12px; padding:5px 10px; }
.proto-toolbar .sep { width:1px; height:20px; background:var(--border); margin:0 4px; }
.proto-toolbar .label { font-size:11px; color:var(--text-muted); }
.proto-main { max-width:1400px; margin:0 auto; padding:16px; }
.proto-card { background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-md); padding:16px 18px; margin-bottom:16px; }
.proto-card-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.proto-card-title { font-size:13px; font-weight:600; color:var(--text-secondary); }
.proto-list-item { display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:12px; color:var(--text-secondary); }
.proto-list-item:last-child { border-bottom:none; }
.proto-status-dot { width:6px; height:6px; border-radius:50%; flex-shrink:0; }
.proto-footer { text-align:center; padding:16px; font-size:11px; color:var(--text-muted); border-top:1px solid var(--border); margin-top:16px; }
/* ===== 两段式：需求范围视图 + 整体效果示意 ===== */
.section-head { display:flex; align-items:center; gap:10px; margin:20px 0 12px; }
.section-head .section-tag { font-size:11px; font-weight:700; padding:3px 10px; border-radius:5px; background:var(--accent-cyan); color:#001a2e; }
.section-head .section-name { font-size:14px; font-weight:700; color:var(--text-primary); }
.section-head .section-desc { font-size:11px; color:var(--text-muted); }
.zone-grid { display:grid; gap:12px; }
.zone-card { background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-md); padding:12px; height:178px; display:flex; flex-direction:column; overflow:hidden; }
.zone-card .zone-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; flex-shrink:0; }
.zone-card .zone-name { font-size:12px; font-weight:600; color:var(--text-primary); }
.zone-card .zone-type { font-size:9px; color:var(--text-muted); border:1px solid var(--border); padding:1px 6px; border-radius:4px; }
.zone-active { border-color:var(--accent-cyan); box-shadow:0 0 0 1px var(--accent-cyan) inset; }
.zone-active .zone-name { color:var(--accent-cyan); }
.zone-placeholder { border-style:dashed; opacity:0.62; background:transparent; }
.zone-placeholder .zone-name { color:var(--text-muted); }
.zone-fr { font-size:11px; color:var(--text-secondary); padding:5px 8px; background:var(--bg-primary); border-radius:5px; margin-bottom:5px; border-left:2px solid var(--accent-cyan); }
.zone-fr b { color:var(--text-primary); display:block; font-size:11px; }
.zone-empty-note { font-size:11px; color:var(--text-muted); text-align:center; padding:14px 6px; }
.legend { display:flex; gap:18px; align-items:center; margin-top:12px; font-size:11px; color:var(--text-secondary); flex-wrap:wrap; }
.legend .lg-item { display:flex; align-items:center; gap:6px; }
.legend .lg-sw { width:14px; height:14px; border-radius:3px; border:1px solid var(--border); }
.note-strip { font-size:11px; color:var(--text-muted); background:var(--bg-card); border:1px solid var(--border); border-radius:6px; padding:6px 12px; margin-bottom:12px; }
/* 拟真生产级模板（下段效果示意用，数据为示意） */
.pd-table { width:100%; border-collapse:collapse; font-size:10px; }
.pd-table th,.pd-table td { text-align:left; padding:4px 6px; border-bottom:1px solid rgba(255,255,255,0.06); color:var(--text-secondary); }
.pd-table th { color:var(--text-muted); font-weight:600; }
.pd-table td b { color:var(--text-primary); font-weight:600; }
.pd-bars { display:flex; align-items:flex-end; gap:5px; height:70px; padding:4px 2px; }
.pd-bars .b { flex:1; border-radius:3px 3px 0 0; min-height:3px; }
.pd-kanban-mini { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; }
.pd-kanban-mini .kcol { background:var(--bg-primary); border:1px solid var(--border); border-radius:5px; padding:5px; min-height:52px; }
.pd-kanban-mini .kcol .kt { font-size:9px; color:var(--text-muted); margin-bottom:4px; }
.pd-kanban-mini .kcard { font-size:9px; background:var(--bg-card); border:1px solid var(--border); border-radius:3px; padding:3px 5px; margin-bottom:3px; color:var(--text-secondary); }
.pd-alarm-list { display:flex; flex-direction:column; gap:5px; }
.pd-alarm-list .arow { display:flex; align-items:center; gap:6px; font-size:10px; color:var(--text-secondary); padding:4px 7px; background:var(--bg-primary); border-radius:5px; }
.pd-tree-mini { display:flex; flex-direction:column; gap:3px; font-size:10px; }
.pd-tree-mini .tgrp { color:var(--text-muted); font-weight:600; font-size:9px; margin-top:3px; }
.pd-tree-mini .tleaf { color:var(--text-secondary); padding:2px 6px 2px 12px; }
.pd-station { height:80px; border-radius:6px; background:linear-gradient(180deg,rgba(0,212,255,0.05),transparent); display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden; }
.pd-station .rail { position:absolute; left:8%; right:8%; height:3px; border-radius:2px; }
.pd-station .stn { position:absolute; width:8px; height:8px; border-radius:50%; background:var(--status-green); border:2px solid var(--bg-card); }
.pd-diagram { height:80px; position:relative; background:repeating-linear-gradient(0deg,transparent,transparent 15px,rgba(255,255,255,0.04) 16px); border-radius:6px; }
.pd-curve { height:80px; position:relative; }
.pd-curve svg { width:100%; height:100%; }
.pd-kpi-mini { display:grid; grid-template-columns:1fr 1fr; gap:6px; }
.pd-kpi-mini .kc { background:var(--bg-primary); border:1px solid var(--border); border-radius:5px; padding:6px 8px; }
.pd-kpi-mini .kc .kl { font-size:9px; color:var(--text-muted); }
.pd-kpi-mini .kc .kv { font-size:15px; font-weight:700; color:var(--text-primary); margin-top:2px; }
.safety-banner { display:flex; align-items:center; gap:10px; padding:8px 20px; background:rgba(255,149,0,0.12); border-bottom:1px solid var(--status-orange); color:var(--status-orange); font-size:12px; font-weight:600; position:sticky; top:0; z-index:200; }
.safety-banner .icon { font-size:16px; }
.safety-banner .sub { font-weight:400; color:var(--text-secondary); font-size:11px; }
.safety-corner { position:fixed; right:12px; bottom:12px; background:var(--status-orange); color:#001a2e; font-size:10px; font-weight:700; padding:4px 10px; border-radius:6px; z-index:300; opacity:0.92; }
"""


# Strong, safety-specific hints (used only as FALLBACK when FRs carry no
# explicit safetyRelevance). Deliberately excludes weak words like 进路/道岔/闭塞/防护
# that also appear in non-safety ATS/CTC/monitoring contexts.
STRONG_SAFETY_HINTS = [
    "联锁", "敌对进路", "接近锁闭", "锁闭", "故障导向安全", "故障-安全", "故障安全",
    "SIL", "移动授权", "防护包络", "安全包络", "ATP", "ZC", "VOBC", "TACS",
    "移动闭塞", "超速防护", "安全相关", "安全完整性",
]


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


def detect_safety(analysis: dict) -> bool:
    """True if the requirement is safety-critical (no real frontend → banner + 阐述图).

    Priority: trust explicit per-FR `safetyRelevance` marking first. Only fall back
    to strong keyword detection when NO FR carries the field (legacy/manual JSON).
    This prevents ATS/CTC scenes (which mention 进路/道岔) from being mis-flagged."""
    req = analysis.get("requirements", {})
    frs = req.get("functionalRequirements", [])
    marks = [fr.get("safetyRelevance") for fr in frs if fr.get("safetyRelevance")]
    if marks:
        # Explicit marking present → authoritative: safety iff any FR is 安全相关
        return any(m == "安全相关" for m in marks)
    # Fallback: strong safety keywords on title + FR text
    text = req.get("title", "") + " " + " ".join(
        (fr.get("name", "") or "") + " " + (fr.get("description", "") or "") for fr in frs
    )
    return any(h in text for h in STRONG_SAFETY_HINTS)


def detect_subsystem(analysis: dict) -> str:
    """Classify the requirement into a non-safety subsystem for layout adaptation.
    Returns: ats | ctc | monitoring | iom | general. (safety handled by detect_safety.)"""
    keywords = {
        "ats": ["ATS", "列车自动监控", "自动监控", "行车指挥", "调度员", "运行图", "时刻表",
                 "车次号", "自动排路", "站场图", "运行线", "扣车", "跳停", "行车调度", "调度大屏"],
        "ctc": ["CTC", "调度集中", "TDCS", "调度监督", "调度命令", "集中控制", "遥控",
                 "车次号跟踪", "调度所", "车站子系统"],
        "monitoring": ["MSS", "集中监测", "微机监测", "监测子系统", "维护支持", "监测终端",
                 "动作电流", "转辙机电流", "轨道电压", "灯丝", "电缆绝缘", "波形回放", "曲线",
                 "设备监测", "状态监测", "模拟量", "开关量", "回放"],
        "iom": ["IOM", "智能运维", "综合运维", "运维管理", "设备台账", "检修", "维修", "工单",
                 "巡检", "检修计划", "备件", "库存", "健康评价", "健康管理", "PHM", "故障预测"],
    }
    req = analysis.get("requirements", {})
    frs = req.get("functionalRequirements", [])
    parts = [req.get("title", "")]
    for fr in frs:
        parts.extend([fr.get("name", ""), fr.get("description", ""),
                      fr.get("uiLocation", ""), fr.get("dataSource", "")])
    text = " ".join(p for p in parts if p)
    scores = {}
    for sub, kws in keywords.items():
        hits = sum(1 for k in kws if k in text)
        if hits:
            scores[sub] = hits
    if not scores:
        return "general"
    return max(scores, key=lambda s: scores[s])


# Per-subsystem context: user role label + toolbar filter HTML.
# Deliberately avoids国铁-specific "段/车间/工班" hierarchy unless fitting.
SUBSYSTEM_META = {
    "ats": {
        "role": "行车调度员",
        "badge": "ATS · 调度指挥",
        "toolbar": [
            ("线路", ["1号线", "2号线", "3号线"]),
            ("车站", ["全部", "A站", "B站", "C站"]),
            ("时间", ["今日", "本周", "本月"]),
        ],
    },
    "ctc": {
        "role": "列车调度员",
        "badge": "CTC · 调度集中",
        "toolbar": [
            ("区段", ["全区段", "甲站—乙站", "乙站—丙站"]),
            ("显示", ["实际运行图", "计划运行图", "对比"]),
            ("时间", ["今日", "本班", "本周"]),
        ],
    },
    "monitoring": {
        "role": "信号检修工",
        "badge": "MSS · 集中监测",
        "toolbar": [
            ("设备类型", ["全部", "转辙机", "轨道电路", "信号机"]),
            ("车站", ["全部", "A站", "B站"]),
            ("时间", ["实时", "近24小时", "近7天"]),
        ],
    },
    "iom": {
        "role": "运维管理员",
        "badge": "IOM · 智能运维",
        "toolbar": [
            ("专业", ["全部", "信号", "通信", "供电"]),
            ("状态", ["全部", "待处理", "处理中", "已闭环"]),
            ("时间", ["本月", "本季度", "本年"]),
        ],
    },
    "general": {
        "role": "业务用户",
        "badge": "业务系统",
        "toolbar": [
            ("范围", ["全部"]),
            ("时间", ["今日", "本周", "本月"]),
        ],
    },
}


def _toolbar_html(meta: dict) -> str:
    """Build toolbar selects from subsystem meta (no hardcoded国铁 hierarchy)."""
    parts = []
    for label, options in meta["toolbar"]:
        opts = "".join(f'<option value="{o}">{o}</option>' for o in options)
        parts.append(
            f'<span class="label">{label}：</span>'
            f'<select>{opts}</select><div class="sep"></div>'
        )
    parts.append('<span class="label">数据模拟 · 非真实数据</span>')
    return "\n  ".join(parts)


def _layout_safety(frs):
    """阐述图: 中央承载各安全功能阐述卡片(逐条展示锚点). 单栏, 突出逻辑而非界面."""
    cards = []
    for fr in frs:
        ac = fr.get("acceptanceCriteria", "")
        ac_html = f'<div style="margin-top:8px;font-size:12px;color:var(--status-green);">✅ 验收准则：{ac}</div>' if ac else ""
        cards.append(f'''<div class="proto-card">
  <div class="proto-card-header"><div class="proto-card-title">{fr.get("id","")} · {fr.get("name","")}</div>
  <span class="ver" style="background:var(--status-orange);">安全相关</span></div>
  <div style="font-size:13px;color:var(--text-primary);">{fr.get("description","")}</div>
  <div style="margin-top:10px;font-size:12px;color:var(--text-secondary);">逻辑位置：{fr.get("uiLocation","")}　|　数据来源：{fr.get("dataSource","")}</div>
  {ac_html}
</div>''')
    main = "\n".join(cards) if cards else '<div class="proto-bigview"><span class="icon">🛡️</span>安全功能阐述区</div>'
    return f'<div style="max-width:900px;margin:0 auto;">{main}</div>'


# 各子系统功能区拓扑（分区→type→关键词），用于 FR 语义落位 + 效果视图拟真。
# 依据 ATS(IEEE1474) / CTC / 信号集中监测(CSM) / 智能运维 标准化系统的功能组成。
ZONE_TAXONOMY = {
    "ats": [
        {"name": "站场图/线路图显示", "type": "stationmap", "keywords": ["站场", "线路图", "站场图", "显示", "占用", "光带", "区间", "信号机状态"]},
        {"name": "列车跟踪/车次号", "type": "list", "keywords": ["列车跟踪", "车次号", "车次", "跟踪", "列车位置"]},
        {"name": "运行图/时刻表", "type": "diagram", "keywords": ["运行图", "时刻表", "运行线", "计划图", "实际图"]},
        {"name": "进路控制", "type": "list", "keywords": ["进路", "控制", "触发", "排路", "进路办理", "自动排路"]},
        {"name": "运行调整", "type": "list", "keywords": ["调整", "扣车", "跳停", "折返", "限速", "运行调整"]},
        {"name": "报警/事件", "type": "alarm", "keywords": ["报警", "告警", "事件", "异常", "预警"]},
        {"name": "统计报表", "type": "chart", "keywords": ["统计", "报表", "分析", "指标", "正点率"]},
    ],
    "ctc": [
        {"name": "站场表示", "type": "stationmap", "keywords": ["站场", "站场表示", "显示", "占用", "区间"]},
        {"name": "实际/计划运行图", "type": "diagram", "keywords": ["运行图", "实际图", "计划图", "时距图", "运行线"]},
        {"name": "进路控制", "type": "list", "keywords": ["进路", "控制", "试排", "进路办理"]},
        {"name": "调度命令", "type": "table", "keywords": ["调度命令", "命令", "下达", "签收"]},
        {"name": "车次号跟踪", "type": "list", "keywords": ["车次号", "跟踪", "车次"]},
        {"name": "报警/设备状态", "type": "alarm", "keywords": ["报警", "告警", "设备状态", "异常"]},
    ],
    "monitoring": [
        {"name": "设备导航树", "type": "tree", "keywords": ["设备树", "导航", "设备", "车站", "系统"]},
        {"name": "实时监测", "type": "list", "keywords": ["实时", "监测", "状态", "模拟量", "开关量", "在线"]},
        {"name": "特性曲线分析", "type": "curve", "keywords": ["曲线", "动作电流", "电流", "电压", "特性", "波形", "灯丝"]},
        {"name": "报警管理", "type": "alarm", "keywords": ["报警", "告警", "异常", "分级", "越限"]},
        {"name": "回放/历史查询", "type": "curve", "keywords": ["回放", "历史", "查询", "波形回放"]},
        {"name": "报表统计", "type": "table", "keywords": ["报表", "统计", "分析", "日报", "月报", "分路不良"]},
    ],
    "iom": [
        {"name": "设备台账", "type": "table", "keywords": ["台账", "设备清单", "资产", "设备信息", "台账管理"]},
        {"name": "健康管理", "type": "kpi", "keywords": ["健康", "评价", "评分", "健康度", "PHM", "健康管理"]},
        {"name": "故障预测", "type": "chart", "keywords": ["故障预测", "预测", "趋势", "频发", "故障分析"]},
        {"name": "维修工单", "type": "kanban", "keywords": ["工单", "维修", "检修", "派工", "闭环", "工单管理"]},
        {"name": "巡检/检修计划", "type": "table", "keywords": ["巡检", "计划", "检修计划", "排程", "计划管理"]},
        {"name": "备件库存", "type": "table", "keywords": ["备件", "库存", "缺件", "库存预警", "备件管理"]},
        {"name": "统计大屏", "type": "kpi", "keywords": ["统计", "大屏", "报表", "指标", "综合展示"]},
        {"name": "施工卡控", "type": "table", "keywords": ["施工", "卡控", "登销记", "施工管理"]},
    ],
    "general": [
        {"name": "指标概览", "type": "kpi", "keywords": ["指标", "概览", "统计", "汇总"]},
        {"name": "功能列表", "type": "list", "keywords": ["列表", "查询", "管理", "维护"]},
        {"name": "数据表格", "type": "table", "keywords": ["表格", "明细", "记录"]},
        {"name": "统计图表", "type": "chart", "keywords": ["图表", "趋势", "分析"]},
    ],
}

TYPE_LABEL = {"stationmap": "站场图", "diagram": "时距图", "curve": "曲线", "chart": "图表",
              "table": "表格", "list": "列表", "kpi": "指标", "kanban": "看板",
              "alarm": "报警", "tree": "设备树"}


def _fr_text(fr):
    return " ".join(str(fr.get(k, "") or "") for k in ("name", "description", "uiLocation", "dataSource"))


def _match_frs_to_zones(frs, zones):
    """按语义把 FR 落位到分区（尽力匹配）。返回 {zone_idx: [fr,...]} 与未匹配 FR 列表。"""
    placed = {i: [] for i in range(len(zones))}
    unmatched = []
    for fr in frs:
        text = _fr_text(fr)
        best_idx, best_score = None, 0
        for i, zone in enumerate(zones):
            score = sum(1 for kw in zone["keywords"] if kw in text)
            if score > best_score:
                best_idx, best_score = i, score
        if best_idx is not None and best_score > 0:
            placed[best_idx].append(fr)
        else:
            unmatched.append(fr)
    # 未匹配 FR 兜底放入第一个分区（避免丢失），并标记
    if unmatched and zones:
        placed[0].extend(unmatched)
    return placed


def _prod_stationmap():
    dots = "".join(f'<span class="stn" style="left:{p}%;"></span>' for p in (18, 38, 58, 78))
    return (f'<div class="pd-station"><span class="rail" style="top:40%;background:var(--status-red);"></span>'
            f'<span class="rail" style="top:60%;background:var(--status-green);"></span>{dots}</div>')


def _prod_diagram():
    return ('<div class="pd-diagram"><svg viewBox="0 0 200 80" preserveAspectRatio="none">'
            '<polyline points="0,70 40,55 90,40 140,28 200,15" fill="none" stroke="var(--accent-cyan)" stroke-width="2"/>'
            '<polyline points="0,60 50,58 100,45 150,40 200,30" fill="none" stroke="var(--status-orange)" stroke-width="1.5" stroke-dasharray="4 3"/>'
            '</svg></div>')


def _prod_curve():
    return ('<div class="pd-curve"><svg viewBox="0 0 200 80" preserveAspectRatio="none">'
            '<path d="M0,60 C30,20 50,20 70,55 S120,70 150,40 S190,30 200,45" fill="none" stroke="var(--status-green)" stroke-width="2"/>'
            '<line x1="0" y1="18" x2="200" y2="18" stroke="var(--status-red)" stroke-width="1" stroke-dasharray="3 3"/>'
            '</svg></div>')


def _prod_chart():
    bars = "".join(f'<div class="b" style="height:{h}%;background:{c};"></div>'
                   for h, c in [(45, "var(--accent-cyan)"), (70, "var(--status-green)"),
                                (55, "var(--status-orange)"), (85, "var(--status-blue)"),
                                (38, "var(--status-yellow)"), (62, "var(--accent-cyan)")])
    return f'<div class="pd-bars">{bars}</div>'


def _prod_table():
    return ('<table class="pd-table"><tr><th>名称</th><th>状态</th><th>数值</th></tr>'
            '<tr><td><b>对象 A</b></td><td>正常</td><td>—</td></tr>'
            '<tr><td><b>对象 B</b></td><td>正常</td><td>—</td></tr>'
            '<tr><td><b>对象 C</b></td><td>注意</td><td>—</td></tr></table>')


def _prod_list():
    return ('<div style="display:flex;flex-direction:column;gap:5px;">'
            '<div class="proto-list-item"><span class="proto-status-dot" style="background:var(--status-green)"></span><span style="flex:1;">条目 A</span></div>'
            '<div class="proto-list-item"><span class="proto-status-dot" style="background:var(--status-green)"></span><span style="flex:1;">条目 B</span></div>'
            '<div class="proto-list-item"><span class="proto-status-dot" style="background:var(--status-orange)"></span><span style="flex:1;">条目 C</span></div></div>')


def _prod_kpi():
    return ('<div class="pd-kpi-mini">'
            '<div class="kc"><div class="kl">指标 A</div><div class="kv">92.4</div></div>'
            '<div class="kc"><div class="kl">指标 B</div><div class="kv">18</div></div>'
            '<div class="kc"><div class="kl">指标 C</div><div class="kv">5</div></div>'
            '<div class="kc"><div class="kl">指标 D</div><div class="kv">98.6%</div></div></div>')


def _prod_kanban():
    return ('<div class="pd-kanban-mini">'
            '<div class="kcol"><div class="kt">待派</div><div class="kcard">工单 1</div></div>'
            '<div class="kcol"><div class="kt">处理中</div><div class="kcard">工单 2</div><div class="kcard">工单 3</div></div>'
            '<div class="kcol"><div class="kt">已闭环</div><div class="kcard">工单 4</div></div></div>')


def _prod_alarm():
    return ('<div class="pd-alarm-list">'
            '<div class="arow"><span class="proto-status-dot" style="background:var(--status-red)"></span>一级报警 · 示意</div>'
            '<div class="arow"><span class="proto-status-dot" style="background:var(--status-orange)"></span>二级报警 · 示意</div>'
            '<div class="arow"><span class="proto-status-dot" style="background:var(--status-yellow)"></span>预警 · 示意</div></div>')


def _prod_tree():
    return ('<div class="pd-tree-mini">'
            '<div class="tgrp">A 站</div><div class="tleaf">├ 联锁</div><div class="tleaf">├ 转辙机</div>'
            '<div class="tgrp">B 站</div><div class="tleaf">├ 轨道电路</div><div class="tleaf">└ 信号机</div></div>')


PROD_BUILDERS = {"stationmap": _prod_stationmap, "diagram": _prod_diagram, "curve": _prod_curve,
                 "chart": _prod_chart, "table": _prod_table, "list": _prod_list, "kpi": _prod_kpi,
                 "kanban": _prod_kanban, "alarm": _prod_alarm, "tree": _prod_tree}


def _scope_view(frs, zones, cols):
    """上段：需求范围视图——整体架构全标出，FR 落位高亮，其余标非本次范围。"""
    placed = _match_frs_to_zones(frs, zones)
    cards = []
    for i, zone in enumerate(zones):
        zfrs = placed.get(i, [])
        tlabel = TYPE_LABEL.get(zone["type"], zone["type"])
        if zfrs:
            fr_html = "".join(
                f'<div class="zone-fr"><b>{fr.get("id","")} {fr.get("name","")}</b>'
                f'{(fr.get("description","") or "")[:40]}</div>' for fr in zfrs)
            cards.append(f'<div class="zone-card zone-active"><div class="zone-head">'
                         f'<span class="zone-name">{zone["name"]}</span><span class="zone-type">{tlabel}</span></div>'
                         f'{fr_html}</div>')
        else:
            cards.append(f'<div class="zone-card zone-placeholder"><div class="zone-head">'
                         f'<span class="zone-name">{zone["name"]}</span><span class="zone-type">{tlabel}</span></div>'
                         f'<div class="zone-empty-note">— 非本次需求范围 —</div></div>')
    legend = ('<div class="legend">'
              '<span class="lg-item"><span class="lg-sw" style="border-color:var(--accent-cyan);background:rgba(0,212,255,0.15);"></span>本次需求落位</span>'
              '<span class="lg-item"><span class="lg-sw" style="border-style:dashed;opacity:0.6;"></span>非本次需求范围</span>'
              '<span class="lg-item" style="color:var(--text-muted);">落位为语义尽力匹配，供评审参考</span></div>')
    return f'<div class="zone-grid" style="grid-template-columns:repeat({cols},1fr)">{"".join(cards)}</div>{legend}'


def _effect_view(zones, cols):
    """下段：整体效果示意——全分区按 type 拟真渲染（示意数据），呈现生产级观感。"""
    cards = []
    for zone in zones:
        builder = PROD_BUILDERS.get(zone["type"], _prod_list)
        tlabel = TYPE_LABEL.get(zone["type"], zone["type"])
        cards.append(f'<div class="zone-card"><div class="zone-head">'
                     f'<span class="zone-name">{zone["name"]}</span><span class="zone-type">{tlabel}</span></div>'
                     f'{builder()}</div>')
    note = '<div class="note-strip">🎨 整体效果示意：以下为全功能区的生产级观感示意，数据均为模拟，仅用于呈现"整页做出来大致长什么样"，非本次需求交付内容。</div>'
    return f'{note}<div class="zone-grid" style="grid-template-columns:repeat({cols},1fr)">{"".join(cards)}</div>'


def _layout_two_tier(frs, zones):
    """非安全子系统：上段需求范围视图 + 下段整体效果示意。上下两段用相同列数+统一分区高度，保证严格对齐便于对比。"""
    cols = min(4, max(1, len(zones)))
    scope = _scope_view(frs, zones, cols)
    effect = _effect_view(zones, cols)
    return (f'<div class="section-head"><span class="section-tag">上</span>'
            f'<span class="section-name">需求范围视图</span>'
            f'<span class="section-desc">整体布局架构 · 本次需求落位 · 其余标范围</span></div>{scope}'
            f'<div class="section-head"><span class="section-tag" style="background:var(--status-blue);">下</span>'
            f'<span class="section-name">整体效果示意</span>'
            f'<span class="section-desc">生产级观感 · 全分区拟真 · 数据为示意</span></div>{effect}')


def render_demo(analysis: dict, css_override: str = "") -> str:
    vue_js = load_vue()
    req = analysis.get("requirements", {})
    frs = req.get("functionalRequirements", [])
    title = req.get("title", "业务系统")

    # Subsystem routing: safety → 阐述图; otherwise two-tier (scope + effect).
    is_safety = detect_safety(analysis)
    subsystem = "safety" if is_safety else detect_subsystem(analysis)
    meta = SUBSYSTEM_META.get(subsystem, SUBSYSTEM_META["general"])

    safety_banner = """<div class="safety-banner">
  <span class="icon">⚠️</span>
  <span>安全功能阐述图 · 实际安全系统无操作前端界面</span>
  <span class="sub">— 本页仅用于需求评审与理解，非产品界面交付物</span>
</div>""" if is_safety else ""
    safety_corner = '<div class="safety-corner">安全阐述图 · 非真实界面</div>' if is_safety else ""

    css_block = DESIGN_TOKENS_CSS
    if css_override:
        css_block += "\n/* === Reference Page Override === */\n" + css_override

    toolbar_html = _toolbar_html(meta)
    if is_safety:
        main_html = _layout_safety(frs)
    else:
        zones = ZONE_TAXONOMY.get(subsystem, ZONE_TAXONOMY["general"])
        main_html = _layout_two_tier(frs, zones)

    body_template = f"""<div id="app">
{safety_banner}
<header class="proto-header">
  <div style="display:flex;align-items:center;">
    <h1>{{{{ title }}}}</h1>
    <span class="ver">PROTOTYPE</span>
  </div>
  <div class="user-info">当前用户：{meta['role']}　|　{meta['badge']}</div>
</header>
<div class="proto-toolbar">
  {toolbar_html}
</div>
<div class="proto-main">
{main_html}
</div>
<footer class="proto-footer">scene-req-to-demo v0.0.5 · {meta['badge']} · 布局适配：{subsystem}</footer>
{safety_corner}
</div>"""

    vue_logic = f"""const DATA = {json.dumps(analysis, ensure_ascii=False)};
const {{ createApp, ref }} = Vue;
createApp({{
  setup() {{
    const title = ref(DATA.requirements.title);
    return {{ title }};
  }}
}}).mount('#app');"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — 业务系统原型</title>
<script>{vue_js}</script>
<style>{css_block}</style>
</head>
<body class="theme-dark-blue">
{body_template}
<script>{vue_logic}</script>
</body>
</html>
"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Render Demo HTML prototype")
    parser.add_argument("--output-dir", help="Output directory (auto-name by title)")
    parser.add_argument("--css-file", help="Custom CSS file to override default theme (Mode B: style copy)")
    parser.add_argument("--suffix", default="", help="Filename suffix, e.g. --suffix=-constrained (use = when value starts with -)")
    args = parser.parse_args()

    css_override = ""
    if args.css_file:
        css_path = Path(args.css_file)
        if css_path.exists():
            css_override = css_path.read_text(encoding="utf-8")
        else:
            print(f"Warning: CSS file not found: {args.css_file}", file=sys.stderr)

    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    analysis = input_data.get("analysis")
    if not analysis:
        print("Error: missing 'analysis' field", file=sys.stderr)
        sys.exit(1)

    html_text = render_demo(analysis, css_override=css_override)

    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        title = analysis.get("requirements", {}).get("title", "未命名")
        title = title.replace(" ", "")
        suffix = args.suffix or ""
        out_path = _avoid_collision(out_dir / f"{title}{suffix}.html")
        out_path.write_text(html_text, encoding="utf-8")
        fr_count = len(analysis.get("requirements", {}).get("functionalRequirements", []))
        if detect_safety(analysis):
            tag, layout = "安全阐述图", "safety"
        else:
            layout = detect_subsystem(analysis)
            tag = "业务原型"
        print(f"✓ 约束版 Demo [{tag}] 布局适配={layout} · 覆盖 {fr_count} 项 FR", file=sys.stderr)
        print(str(out_path))
    else:
        print(html_text)


if __name__ == "__main__":
    main()
