# 版本归档

每次修改 analyzer.html 时，保存该版本的 snap 到本目录，方便回溯与对比。

| 文件 | 大小 | 说明 |
|------|------|------|
| analyzer-v0.1.0.html | 31KB | 初始版本：基础流程图生成 |
| analyzer-v0.2.0.html | 32KB | System Prompt 升级 |
| analyzer-v1.1.0.html | 41KB | 国内镜像源 + 文档 |
| analyzer-v2.0.0.html | 45KB | 多图表类型支持（流程图/时序图/类图/状态图/ERD） |
| analyzer-v2.1.0.html | 49KB | 版本信息 + 更新说明展示 |
| analyzer-v2.2.0-working.html | 78KB | 当前工作版本（含所有未提交的修复） |
| analyzer-v2.3.0.html | 80KB | 铁路信号领域增强（CBTC/TACS 知识注入 + 测试集 31 场景） |
| analyzer-v2.3.1.html | 82KB | requirementDiagram 支持 + 降级生成 + 小模型风险提示 |
| analyzer-v2.3.2.html | 83KB | [FIX] genRequirement 改用 l.push+join('\n') 真正换行符而非字面量 \n |
| analyzer-v2.3.3.html | 84KB | 新增"新标签页"按钮：全屏新 tab 打开 Mermaid 图 |
| analyzer-v2.3.4.html | 84KB | 上下布局：左右→上下，split-pane 移除 max-height |

## 当前版本 v2.3.4 包含的改动

- **布局改为上下排列**：需求报告在上、Mermaid 图在下，解决左右布局图太窄的问题
  - `.split` 改为 `flex-direction: column`，移除 `max-height: 70vh` 约束
  - `.split-div` 从竖线改为横线
  - analyzer.html + AnalysisResult.vue 同步修改
  - 移除响应式断点（768px），始终纵向排列

## 使用方式

需要回退时，把对应 .html 复制为项目根目录的 analyzer.html 即可：

```bash
cp versions/analyzer-v2.0.0.html analyzer.html
```
