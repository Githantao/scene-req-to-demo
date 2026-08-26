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
body.theme-light-blue {
  --bg-primary: #e8eef6; --bg-card: #ffffff; --bg-card-hover: #f0f5ff;
  --text-primary: #1a3248; --text-secondary: #5a7a96; --text-muted: #8a9ab0;
  --border: #c5d9f0; --shadow-card: 0 4px 24px rgba(0,0,0,0.08);
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
.proto-tabs { display:flex; gap:0; }
.proto-tab { padding:4px 12px; font-size:11px; color:var(--text-muted); cursor:pointer; border:1px solid var(--border); background:transparent; transition:all 0.2s; }
.proto-tab:first-child { border-radius:6px 0 0 6px; }
.proto-tab:last-child { border-radius:0 6px 6px 0; }
.proto-tab.active { background:var(--accent-cyan); color:#001a2e; border-color:var(--accent-cyan); font-weight:600; }
.proto-view { min-height:240px; display:flex; align-items:center; justify-content:center; border:1px solid var(--border); border-radius:var(--radius-md); background:var(--bg-primary); }
.proto-view-placeholder { text-align:center; color:var(--text-muted); font-size:13px; }
.proto-view-placeholder .icon { font-size:32px; margin-bottom:8px; display:block; }
.proto-chart { height:180px; display:flex; align-items:end; gap:6px; padding:8px 4px; }
.proto-bar-group { flex:1; display:flex; flex-direction:column; align-items:center; gap:4px; }
.proto-bar { width:100%; border-radius:4px 4px 0 0; transition:height 0.6s ease; min-height:2px; }
.proto-bar-label { font-size:10px; color:var(--text-muted); }
.proto-bar-value { font-size:10px; font-weight:600; color:var(--text-secondary); }
.proto-grid { display:grid; gap:14px; }
.proto-grid-sidebar { grid-template-columns:1fr 300px; }
@media (max-width:900px) { .proto-grid-sidebar { grid-template-columns:1fr; } }
.proto-sidebar-card { background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-md); padding:14px; }
.proto-sidebar-title { font-size:11px; font-weight:600; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px; }
.proto-list-item { display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:12px; color:var(--text-secondary); }
.proto-list-item:last-child { border-bottom:none; }
.proto-status-dot { width:6px; height:6px; border-radius:50%; flex-shrink:0; }
.proto-footer { text-align:center; padding:16px; font-size:11px; color:var(--text-muted); border-top:1px solid var(--border); margin-top:16px; }
"""


def analyze_fr_roles(frs):
    """Analyze FRs to determine their roles in the UI."""
    roles = {"views": [], "switcher": None, "global_filter": None, "other": []}
    for fr in frs:
        fr_name = fr.get("name", "")
        fr_desc = fr.get("description", "")
        fr_loc = fr.get("uiLocation", "")
        # Match on FR name + description (not uiLocation, which may contain false positives)
        match_text = fr_name + " " + fr_desc
        name_text = fr_name
        if any(k in name_text for k in ["切换", "Tab", "tab"]) or (
            "切换" in name_text and "显示" not in name_text
        ):
            roles["switcher"] = fr
        elif any(k in name_text for k in ["层级", "权限", "过滤"]) or (
            "全局" in fr_loc and "过滤" in name_text
        ):
            roles["global_filter"] = fr
        elif any(k in name_text for k in ["显示", "渲染", "展示"]) or (
            "图" in name_text and "切换" not in name_text
        ):
            roles["views"].append(fr)
        else:
            roles["other"].append(fr)
    return roles


def render_demo(analysis: dict, css_override: str = "") -> str:
    vue_js = load_vue()
    req = analysis.get("requirements", {})
    frs = req.get("functionalRequirements", [])
    title = req.get("title", "业务系统")
    json_str = json.dumps(analysis, ensure_ascii=False)
    roles = analyze_fr_roles(frs)

    view_names = [v.get("name", f"视图{i+1}") for i, v in enumerate(roles["views"])]
    view_names_json = json.dumps(view_names, ensure_ascii=False)

    # CSS: default tokens + optional override from reference page
    css_block = DESIGN_TOKENS_CSS
    if css_override:
        css_block += "\n/* === Reference Page Override === */\n" + css_override

    vue_template = f"""<div id="app">
<header class="proto-header">
  <div style="display:flex;align-items:center;">
    <h1>{{{{ title }}}}</h1>
    <span class="ver">PROTOTYPE</span>
  </div>
  <div class="user-info">当前用户：段调度员张三 | 角色：段级</div>
</header>
<div class="proto-toolbar">
  <span class="label">用户层级：</span>
  <select v-model="selectedLevel">
    <option value="段">段级</option>
    <option value="车间">车间级</option>
    <option value="工班">工班级</option>
  </select>
  <div class="sep"></div>
  <span class="label">时间范围：</span>
  <select v-model="selectedTime">
    <option value="today">今日</option>
    <option value="week">本周</option>
    <option value="month">本月</option>
  </select>
  <div class="sep"></div>
  <span class="label">数据模拟 · 非真实数据</span>
</div>
<div class="proto-main">
  <div class="proto-grid proto-grid-sidebar">
    <div class="proto-card">
      <div class="proto-card-header">
        <div class="proto-card-title">中央区域</div>
        <div class="proto-tabs">
          <div v-for="(name, i) in viewNames" :key="i"
               class="proto-tab" :class="activeView === i ? 'active' : ''"
               @click="activeView = i">
            {{{{ name }}}}
          </div>
        </div>
      </div>
      <div v-for="(name, i) in viewNames" :key="'view-'+i" v-show="activeView === i" class="proto-view">
        <div v-if="i === 0" class="proto-view-placeholder">
          <span class="icon">🗺️</span>
          <div>{{{{ name }}}}</div>
          <div style="font-size:11px;margin-top:4px;">管辖范围：全段5条线路 · 28个车站</div>
        </div>
        <div v-else-if="i === 1" style="width:100%;padding:12px;">
          <div class="proto-chart">
            <div v-for="(d,j) in chartData" :key="j" class="proto-bar-group">
              <div class="proto-bar-value">{{{{ d.value }}}}</div>
              <div class="proto-bar" :style="{{height: (d.value / maxVal * 100) + '%', background: d.color}}"></div>
              <div class="proto-bar-label">{{{{ d.label }}}}</div>
            </div>
          </div>
        </div>
        <div v-else class="proto-view-placeholder">
          <span class="icon">📊</span>
          <div>{{{{ name }}}}</div>
        </div>
      </div>
    </div>
    <div>
      <div class="proto-sidebar-card" style="margin-bottom:14px;">
        <div class="proto-sidebar-title">设备运用概况</div>
        <div class="proto-list-item" v-for="(item, i) in sideStats" :key="i">
          <span class="proto-status-dot" :style="{{background: item.color}}"></span>
          <span style="flex:1;">{{{{ item.name }}}}</span>
          <span style="font-weight:600;color:var(--text-primary);">{{{{ item.value }}}}</span>
        </div>
      </div>
      <div class="proto-sidebar-card">
        <div class="proto-sidebar-title">快捷操作</div>
        <div class="proto-list-item" v-for="(action, i) in actions" :key="i">
          <span>{{{{ action }}}}</span>
        </div>
      </div>
    </div>
  </div>
</div>
<footer class="proto-footer">scene-req-to-demo v0.0.3 · 业务系统前端原型</footer>
</div>"""

    vue_logic = f"""const DATA = {json_str};
const VIEW_NAMES = {view_names_json};
const {{ createApp, ref, computed }} = Vue;
createApp({{
  setup() {{
    const title = ref(DATA.requirements.title);
    const activeView = ref(0);
    const selectedLevel = ref('段');
    const selectedTime = ref('today');
    const viewNames = ref(VIEW_NAMES);
    const chartData = ref([
      {{ label: '转辙机', value: 63, color: 'var(--accent-cyan)' }},
      {{ label: '信号机', value: 45, color: 'var(--status-green)' }},
      {{ label: '轨道电路', value: 38, color: 'var(--status-orange)' }},
      {{ label: '应答器', value: 52, color: 'var(--status-blue)' }},
      {{ label: '联锁设备', value: 28, color: 'var(--status-yellow)' }},
      {{ label: '列控设备', value: 35, color: 'var(--accent-cyan)' }}
    ]);
    const maxVal = computed(() => Math.max(...chartData.value.map(d => d.value)));
    const sideStats = ref([
      {{ name: '所辖设备总数', value: '286台', color: 'var(--accent-cyan)' }},
      {{ name: '本月运用总次数', value: '1,842次', color: 'var(--status-green)' }},
      {{ name: '异常告警', value: '3条', color: 'var(--status-red)' }},
      {{ name: '在线率', value: '98.6%', color: 'var(--status-green)' }}
    ]);
    const actions = ref(['导出报表', '全屏显示', '切换主题']);
    return {{ title, activeView, selectedLevel, selectedTime, viewNames, chartData, maxVal, sideStats, actions }};
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
{vue_template}
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
        out_path = out_dir / f"{title}{suffix}.html"
        out_path.write_text(html_text, encoding="utf-8")
        print(str(out_path))
    else:
        print(html_text)


if __name__ == "__main__":
    main()
