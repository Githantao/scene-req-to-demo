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

## 当前版本 v2.2.0 包含的修复

- 复制按钮（onCopyFr / onCopyMainReq 已添加 return）
- 图表下拉菜单（diagramOptions / onDiagramTypeChange 已添加 return）
- 重复 getGeneratedMermaid 删除
- 重复 genSequence / genClass / genState / genEr 删除
- genSequence 多干系人轮询（as.length*2 + i%as.length）
- MermaidDiagram.vue originalType 修复（props.diagramType → requirements.diagramType）

## 使用方式

需要回退时，把对应 .html 复制为项目根目录的 analyzer.html 即可：

```bash
cp versions/analyzer-v2.0.0.html analyzer.html
```
