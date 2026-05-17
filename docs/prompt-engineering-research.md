# Prompt Engineering 深度研究 — 语义理解提升

> 目标：提升场景需求分析器从自然语言场景描述到结构化需求 + Mermaid 图表的语义理解质量。
> 日期：2026-05-16

---

## 一、已安装的 Agent Skills

| Skill | 安装量 | 用途 |
|-------|--------|------|
| `jwynia/agent-skills@requirements-analysis` | 1.9K | 需求质量诊断框架（5 种问题状态） |
| `softaworks/agent-toolkit@mermaid-diagrams` | 4.0K | Mermaid 图表语法深度参考 |
| `davila7/claude-code-templates@mermaid-diagram-specialist` | 861 | 图表类型选择决策矩阵 + 语法+样式 |
| **可考虑安装：** | | |
| `oakoss/agent-skills@prompt-engineering` | 37 | 高级 prompt 设计原则 |
| `davila7/claude-code-templates@rag-engineer` | 369 | RAG 上下文注入策略 |

---

## 二、学术论文参考

### 1. A Systematic Survey of Prompt Engineering (arXiv 2402.07927)
- 44+ prompt 技术分类体系
- **RaR (Rephrase and Respond)**: 先复述查询再回答，减少语义误解
- **CoVe (Chain-of-Verification)**: 生成后逐条验证正确性
- **Self-Consistency**: 多次采样取一致结果
- **LogiCoT**: 逻辑链推理 + reductio ad absurdum 验证
- **CoS (Chain-of-Symbol)**: 用符号表示空间关系，减少自然语言歧义
- **Active-Prompt**: 基于不确定性采样选择示例

### 2. Semantic Mastery: Enhancing LLMs with NLU (arXiv 2504.00409)
- 语义解析 + 结构化知识图谱集成
- 对比学习减少幻觉
- 混合符号-神经方法解决歧义和不一致

### 3. STROT Framework (arXiv 2505.01636)
- 结构化提示 + 反馈驱动的迭代修正循环
- Schema introspection → 动态上下文构建 → 结构化 prompt → 执行反馈 → 修正

### 4. MermaidSeqBench (NeurIPS 2025, IBM Research)
- 首个 LLM→Mermaid 时序图评估基准
- 6 维评分：语法正确性、Mermaid 专用、逻辑流、完整性、激活处理、错误处理
- 评测结果：Qwen 2.5-7B 在所有 6 个维度均优于同级别 Llama 3.1-8B 和 Granite 3.3-8B
- 方法：人工种子集 → LLM 合成扩展 → 规则变异增强

### 5. Google Prompt Engineering Whitepaper (2024)
- Gemini 模型特定最佳实践
- 指令放置位置影响（primacy/recency bias）
- 结构化输出的分隔符策略

---

## 三、公开资源

- **Awesome-Prompt-Engineering** (GitHub promptslab, 17K+ stars): 最全目录
- **Prompt Engineering Guide** (promptingguide.ai): 系统化教程
- **fladdict/llmermaid** (GitHub 76 stars): Mermaid 流程图驱动 LLM 流程控制

---

## 四、可落地的 8 个改进方向

### 方向 1: Rephrase-and-Respond（语义对齐）
**原理**: 让模型先用自己的话复述用户场景，确认理解后再提取需求（arXiv RaR 技术）
**预期收益**: 捕获 15%+ 语义误解
**改动量**: 小 — 在 SYSTEM_PROMPT 开头加一段复述指令

### 方向 2: Chain-of-Verification（自校验）
**原理**: 需求生成后，模型逐条检查每项需求在原始场景中是否有对应依据
**预期收益**: 减少 40-60% 幻觉（论文数据）
**改动量**: 中 — 需要两阶段 prompt 或追加校验步骤

### 方向 3: 指令层次结构
**原理**: 将平铺规则改为 MUST / SHOULD / MAY 三层，减少规则冲突
**预期收益**: 提高规则遵循一致性
**改动量**: 小 — 重新组织 prompt 结构

### 方向 4: Few-shot 推理链示例
**原理**: 加入完整场景→分析过程→输出的推理链示例
**预期收益**: 提高输出结构和质量的一致性
**改动量**: 中 — 需要设计高质量示例

### 方向 5: Chain-of-Draft（压缩推理）
**原理**: 先做极简场景要素提取（角色、流程、数据、约束），再生成 JSON
**预期收益**: 减少长上下文注意力稀释
**改动量**: 小 — 在输出格式前加一段推理指引

### 方向 6: 领域识别注入（类 RAG）
**原理**: 分析前让模型识别业务领域（电商/医疗/金融等），激活领域知识
**预期收益**: 提高领域特定分析的准确性
**改动量**: 小 — 一条额外指令

### 方向 7: Self-Consistency（多候选聚合）
**原理**: 多次采样取一致性最高的输出
**预期收益**: 提高 10-20% 准确率
**改动量**: 大 — 需要修改推理流程，多次调用后聚合

### 方向 8: 约束条件显式化
**原理**: 明确要求模型标记"不确定"的假设，不编造未提及的功能
**预期收益**: 减少幻觉型功能需求
**改动量**: 小 — 两条额外规则

---

## 五、推荐实施路径

| 优先级 | 方向 | 难度 | 预期收益 | 实施建议 |
|--------|------|------|----------|----------|
| P0 | 方向 1 RaR | 低 | 高 | 先做，改动最小 |
| P0 | 方向 3 层次结构 | 低 | 中 | 和方向 1 一起改 |
| P1 | 方向 4 Few-shot | 中 | 高 | 需要设计示例 |
| P1 | 方向 8 约束显式化 | 低 | 中 | 顺带加入 |
| P2 | 方向 2 CoVe | 中 | 高 | 两阶段架构 |
| P2 | 方向 6 领域识别 | 低 | 中 | 单条指令 |
| P3 | 方向 5 CoD | 低 | 低 | 可做可不做 |
| P3 | 方向 7 Self-Consistency | 高 | 中 | 需改推理流程 |

---

## 六、模型端考量

### 6.1 当前模型
- Qwen2.5-1.5B-Instruct — 中文最强，推荐主力
- Gemma-2-2B-it — 结构化输出稳定
- Phi-3-mini-3.8B — 能力最强但最慢

### 6.2 MermaidSeqBench 结论
Qwen 2.5 在 Mermaid 生成任务上表现最好：
| 维度 | Qwen2.5-7B | Llama3.1-8B | Granite3.3-8B |
|------|-----------|-------------|---------------|
| 综合评分(DeepSeek Judge) | 87.5 | 87.8 | 83.2 |
| 语法正确性 | 91.3 | 92.0 | 87.0 |
| 逻辑流 | 87.2 | 87.4 | 83.0 |
| 错误处理 | 81.7 | 81.8 | 77.0 |

→ Qwen2.5 在 1.5B 小模型上理应继续保持这一优势

### 6.3 WebLLM v0.2.83 可用参数（关键发现）

根据 WebLLM API 文档，`engine.chat.completions.create()` 支持以下参数：

当前代码已配置的参数（已验证生效）：

| 参数 | 当前值 | 说明 | 理由 |
|------|--------|------|------|
| **temperature** | **0.2** | 已配置 ✅ | 需求分析需要确定性输出，低温度减少幻觉；结构化任务推荐 0.1-0.3 |
| **top_p** | **0.9** | 已配置 ✅ | 保持适度多样性但不发散 |
| **max_tokens** | **4096** | 已配置 ✅ | Mermaid 代码 + 中文描述易超 2048 |

当前未配置但可用的参数（未来可调）：

| 参数 | 建议值 | 理由 |
|------|--------|------|
| **frequency_penalty** | 0.0 | 结构化输出不需要惩罚 |
| **presence_penalty** | 0.0 | 同上 |
| **repetition_penalty** | 1.0 | 默认值已适用于结构化输出 |
| **stop** | 无 | JSON 完成时自然停止 |
| **response_format** | `{type:'json_object'}` | 如模型支持，可强制 JSON 输出 |

#### 参数传入位置

当前代码中 `analyzer.html:437` 和 `useWebLLM.ts:83` 均已传入：

```javascript
const reply = await engine.chat.completions.create({
  messages: [...],
  temperature: 0.2,
  max_tokens: 4096,
  top_p: 0.9,
});
```

#### Qwen2.5 官方推荐参数（来自 Hugging Face generation_config）
- **非推理模式**: temperature=0.7, top_p=0.8, top_k=20
- **推理模式**: temperature=0.6, top_p=0.95, top_k=20, min_p=0
- **结构化抽取任务**: 建议 temperature=0.1-0.3（社区实践 + WebLLM API 支持）
- **presence_penalty**: 0-2（用于减少重复，但结构化输出中建议 0）

### 6.4 当前方案的限制与改进

| 限制 | 说明 | 改进方案 |
|------|------|----------|
| **单次生成** | 无重试/回退机制 | 解析失败后可重试 1-2 次（低 temperature 确保一致性） |
| **response_format 未利用** | WebLLM 支持 structured output | 设为 response_format: {type:'json_object'}（如模型支持） |

### 6.5 未来模型升级路径
| 方案 | 优势 | 代价 |
|------|------|------|
| Qwen2.5-7B（更大模型） | 更强理解+生成能力 | 下载量 ~5GB，浏览器可能 OOM |
| 切换至 Qwen3 系列 | 更新架构，中文更强 | 需等 web-llm 支持 |
| Ollama 本地推理 | 绕开 WebGPU，支持更大模型 | 需要用户安装 Ollama |

---

## 七、GitHub 深度研究来源

### Round 1: Prompt 技术
- **RaR (Rephrase and Respond)**: https://github.com/uclaml/Rephrase-and-Respond — UCLA 官方代码
  - One-step RaR: 单一 prompt 中完成复述+回答
  - Two-step RaR: 先用一个 LLM 复述，再传入另一个 LLM 回答
  - 与 CoT 互补，可叠加使用
- **CoVe (Chain-of-Verification)**: https://github.com/KalyanKS-NLP/Prompt-Engineering-Techniques-Hub
  - 4 阶段：基线回答 → 验证问题生成 → 独立验证 → 最终答案
  - 减少 40-60% 幻觉（论文数据）
- **Structured Output 实践**: https://github.com/vishvaRam/Structured-Output-Examples-for-LLMs
  - Qwen 通过 Outlines/Pydantic 实现结构化输出
  - 多框架实现（LangChain, vLLM, Ollama）

### Round 2: 模型端
- **WebLLM API Reference**: https://webllm.mlc.ai/docs/user/api_reference.html
  - GenerationConfig 支持 temperature, top_p, max_tokens, stop, frequency_penalty, presence_penalty, repetition_penalty
  - 可在 chat.completions.create() 中直接传入
- **Qwen2.5 Technical Report**: https://arxiv.org/abs/2412.15115
  - 18T tokens 预训练，post-training 改进结构化输出和指令遵循
  - 推荐 temperature=0.7, top_p=0.8（通用）
- **Qwen3 推荐参数**: https://muxup.com/2025q2/recommended-llm-parameter-quick-reference
  - 思考模式：temp=0.6, top_p=0.95, top_k=20
  - 非思考模式：temp=0.7, top_p=0.8, top_k=20
