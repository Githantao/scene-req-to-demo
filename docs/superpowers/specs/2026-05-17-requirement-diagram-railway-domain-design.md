# 设计方案：requirementDiagram 支持 + 铁路信号领域增强

> 日期：2026-05-17
> 状态：草稿
> 版本：v2.3.0 候选

---

## 一、背景与动机

### 1.1 当前能力（v2.2.0）

- 支持 5 种 Mermaid 图表类型：flowchart / sequenceDiagram / classDiagram / stateDiagram-v2 / erDiagram
- System Prompt 包含通用需求分析规则 + 图表选择规则
- 铁路信号领域有独立测试集（`docs/test-dataset-railway-signal.md`）但未融入 System Prompt
- Prompt 改进已有研究文档（`docs/prompt-engineering-research.md`）但尚未落地

### 1.2 两个方向的关联

- **requirementDiagram**：适合安全苛求系统（如铁路信号）的需求追溯，能表达 FR ↔ NFR ↔ 系统元素之间的 satisfies/derives/verifies 关系
- **铁路信号领域增强**：在 System Prompt 中加入领域术语和联锁逻辑约束，提升对联锁/列控场景的分析准确性
- 两者结合能形成差异化竞争力：**专门针对安全苛求系统的需求分析工具**

---

## 二、方向 A：requirementDiagram 支持

### 2.1 Mermaid requirementDiagram 语法概况

基于 Mermaid v11+ `requirementDiagram` 类型：

| 元素类型 | 关键字 | 用途 |
|----------|--------|------|
| 需求 | `requirement` | 通用需求 |
| 功能需求 | `functionalRequirement` | 功能需求 |
| 性能需求 | `performanceRequirement` | NFR 性能类 |
| 接口需求 | `interfaceRequirement` | 接口定义 |
| 物理需求 | `physicalRequirement` | 硬件/部署 |
| 设计约束 | `designConstraint` | 硬性约束 |

每项需求可配置：

| 属性 | 可选值 |
|------|--------|
| `risk` | Low / Medium / High |
| `verifymethod` | Analysis / Inspection / Test / Demonstration |

关系类型：

| 关系 | 语义 | 映射场景 |
|------|------|----------|
| `contains` | 包含 | FR 包含子 FR |
| `copies` | 复制 | 跨系统复用需求 |
| `derives` | 派生 | FR 从 mainRequirement 派生 |
| `satisfies` | 满足 | 系统元素满足需求 |
| `verifies` | 验证 | 测试用例验证需求 |
| `refines` | 细化 | NFR 细化方向 |
| `traces` | 追溯 | 跨层追溯 |

### 2.2 适用场景

requirementDiagram **不与现有 5 种图表竞争**，而是适用于以下场景：

- 需求数量多（6+ 条 FR）、需要展示 FR 之间/FR 与系统元素之间的追溯关系
- 安全苛求系统（铁路信号、航空航天、医疗设备）需要展示需求→验证的完整链路
- 用户需要 SysML 风格的需求管理可视化

### 2.3 选择规则（新增提示词）

在 System Prompt 图表类型规则中追加第 6 条：

```
6. requirementDiagram — 安全苛求系统需求追溯、FR/NFR/系统元素关系展示、SysML 风格需求管理
   语法：requirementDiagram，requirement 定义需求，element 定义系统元素，
         satisfies/derives/verifies 表示关系
   适用：铁路信号/航空航天/医疗设备等安全领域，需求数量多需追溯的场景
```

选择优先级也应更新为含 requirementDiagram 的版本。

### 2.4 降级生成

当 LLM 未输出 requirementDiagram 代码但用户切换到此类型时，`generateMermaidForType` 需要新增 `generateRequirementDiagram()` 函数。

输出格式示例：

```mermaid
requirementDiagram
    functionalRequirement mainReq {
        id: FR-0
        text: "站内进路建立与锁闭控制"
        risk: High
        verifymethod: Test
    }
    functionalRequirement fr1 {
        id: FR-1
        text: "道岔转换与锁闭管理"
        risk: High
        verifymethod: Test
    }
    functionalRequirement fr2 {
        id: FR-2
        text: "敌对进路冲突检测"
        risk: High
        verifymethod: Test
    }
    element cbi {
        type: "计算机联锁系统"
        docref: "CBI-FS-001"
    }
    mainReq -derives-> fr1
    mainReq -derives-> fr2
    cbi -satisfies-> mainReq
    cbi -satisfies-> fr1
    cbi -satisfies-> fr2
```

### 2.5 改动范围

| 文件 | 改动 |
|------|------|
| `src/utils/prompt.ts` | 图表选择规则追加第 6 条 requirementDiagram |
| `src/utils/mermaidGenerator.ts` | 新增 `generateRequirementDiagram()` + `getDiagramOptions()` 追加 |
| `src/utils/parser.ts` | `generateFallbackMermaid()` 追加 requirementDiagram 分支 |
| `src/types/index.ts` | （无需改动，已支持任意 diagramType） |
| `src/components/MermaidDiagram.vue` | 检查 `validateMermaid` 是否接受 `requirementDiagram` 开头 |
| `src/components/AnalysisResult.vue` | 类型下拉选项追加 requirementDiagram |
| `analyzer.html` | `DIAGRAM_TYPES` 追加，`getGeneratedMermaid`/`genRequirement`/`generateFallbackMermaid` 新增 |
| `src/components/RequirementsReport.vue` | （无需改动） |
| `src/App.vue` | `diagramLabel` 映射追加 |

---

## 三、方向 B：铁路信号领域增强

### 3.1 增强内容

在 System Prompt 中追加以下三个模块：

#### 3.1.1 领域术语附录

```
铁路信号领域术语：
- 联锁 (Interlocking)：信号机/道岔/进路之间的安全制约关系
- 进路 (Route)：列车在站内运行的径路，由信号机防护
- 道岔 (Turnout)：列车转向设备，定位/反位两种状态
- 信号机 (Signal)：防护进路的信号设备，开放/关闭两种状态
- 轨道电路 (Track Circuit)：检测区段占用/空闲的设备
- 区段 (Section)：轨道电路划分的基本单元
- 闭塞 (Block)：保证列车运行安全间隔的技术
- 接近锁闭 (Approach Locking)：列车接近时锁闭进路防止取消
- 敌对进路 (Conflicting Route)：与已建立进路冲突的其他进路
- 故障导向安全 (Fail-Safe)：设备故障时输出安全侧
```

#### 3.1.2 联锁场景分析指南

```
联锁/列控系统需求分析特殊规则：
1. 进路生命周期三阶段：建立（条件检查→道岔动作→锁闭→信号开放）、
   保持（接近锁闭+敌对锁闭）、释放（分段解锁/延时解锁）
2. SIL 4 约束：安全苛求功能必须考虑冗余架构（2×2取2/三取二）
   和独立安全校验，危险失效率 THR ≤ 10⁻⁹/h
3. 接口一致性：CBI/RBC/TCC/CTC 子系统间接口数据必须状态一致，
   通信故障考虑降级处理
4. 降级模式覆盖：正常+降级（通信中断/轨道故障/道岔失表）+
   应急（引导进路/紧急关闭）三种场景
5. 时序图选择优先级提升：涉及多系统条件验证和联锁逻辑检查时
   （如进路建立条件检查、CBI/TCC/RBC 多系统交互），在选择规则中
   将 sequenceDiagram 优先级排在 flowchart 之前
```

#### 3.1.3 信号基础设备 IOM（输入/输出模块）

```
IOM（输入输出模块/采集驱动板）领域知识：
- CBI 系统中 IOM 承担联锁逻辑层与室外现场设备之间的物理接口：
  - 采集板（输入板）：读取信号机灯丝状态、道岔表示、轨道电路占用/空闲等
  - 驱动板（输出板）：控制信号机点灯、道岔转辙机转动、继电器励磁/失磁等
  - 安全型 IOM 采用双通道比较（2取2）架构，单板故障导向安全侧
- 故障模式：
  - 采集板故障可能导致漏采/误采，驱动板故障可能导致漏驱/误动
  - 典型故障：继电器接点粘连、光耦击穿、保险丝熔断、电源模块失效
  - 信号设备故障侵入分析：IOM 为安全关键设备与环境的分界点
- SIL 约束：IOM 必须满足 SIL 4 要求，具备自主故障检测和诊断能力
```

#### 3.1.4 MMS/CSM（信号集中监测系统）

```
MMS/CSM（信号集中监测系统，原微机监测系统）领域知识：
- 电务系统的"黑匣子"，TB/T 2496-2018 系列标准规范
- 监测对象：
  - 电源屏电压/电流、轨道电路特性（分路/残压/相位）、转辙机动作电流曲线
  - 信号机点灯回路（主灯丝/副灯丝状态）、电缆绝缘电阻、防雷元件状态
  - CBI/CBI间通信状态、CTC/TCC接口状态
- 核心功能：
  - 实时报警：设备故障即时弹出报警（灯丝断丝、轨道电路异常、道岔转换超时）
  - 历史回放：可回放任意时刻的站场状态（故障溯源依据）
  - 趋势分析：监测量的长期变化趋势（如道岔动作电流逐渐升高→机械卡阻预警）
  - 电气特性分析：轨道电路分路残压分析、道岔动作功率曲线诊断
- 接口系统：与 CBI、CTC、TCC 等子系统通信获取监测数据
- 智能运维升级方向：CSM 数据 + AI 分析 → PHM 预测性维护
```

#### 3.1.5 智能运维与 PHM（故障预测与健康管理）

```
智能运维/PHM（故障预测与健康管理）领域知识：
- 标准 T/CITSA 23-2022《城市轨道交通信号智能综合运维系统技术规范》
- 技术栈：IoT 传感器 + 边缘计算 + 大数据平台 + AI/ML 算法
- 系统架构：
  - 感知层：智能传感器（振动/温度/电流/电压/图像）、既有 CSM 数据接入
  - 数据层：多源数据融合（CBI日志、转辙机曲线、轨道电路特性、信号机监测、CTC数据）
  - 分析层：故障诊断（知识图谱/规则引擎）、故障预测（时序模型/机器学习）
  - 决策层：维修决策优化（RCM 分析/备件预测/维修排程）
- 典型场景：
  - 道岔 PHM：基于动作电流曲线分析转辙机退化趋势，提前预测卡阻/断相
  - 轨道电路 PHM：分路残压趋势分析预测分路不良
  - 信号机 PHM：点灯回路电流监测预测灯泡寿命
  - 电源 PHM：电源模块老化趋势预测
- RAMS 闭环：PHM 数据反馈给设计部门优化可靠性设计（RAMS—可靠性、可用性、可维护性、安全性）
```

#### 3.1.7 CBTC（基于通信的列车控制系统）领域知识

```
CBTC（Communication-Based Train Control）领域知识：
- 核心架构：ATS（自动列车监督）+ ATO（自动列车运行）+ ATP（自动列车防护）
  + DCS（数据通信系统）+ ZC（区域控制器）+ VOBC（车载控制器）
- ATS（自动列车监督）：运行图管理、列车追踪、自动调整运行计划、
  进路自动设置、调度员人机界面
- ATO（自动列车运行）：自动驾驶、精准停车、牵引/制动曲线计算、
  区间运行时间优化、折返自动控制
- ATP（自动列车防护）：超速防护、移动授权（MA）计算、紧急制动
  命令、车门/屏蔽门联动安全校验、退行防护
- ZC（区域控制器/轨旁ATP）：
  - 接收列车位置报告，计算移动授权（MA）
  - 管理轨道占用逻辑（虚拟区段替代物理轨道电路）
  - 计算安全防护包络（最不利位置原则）
  - 后备模式下生成固定闭塞MA
- VOBC（车载控制器）：
  - 多传感器融合定位：测速电机+雷达+应答器+加速度计
  - 定位不确定性管理：滑行/空转检测与补偿
  - 超速防护曲线计算（紧急制动/常用制动/允许速度三层）
  - 向ZC发送位置报告（周期通常200-500ms）
- DCS（数据通信系统）：
  - 冗余无线网络（LTE-M / Wi-Fi 双网冗余）
  - 车地通信切换（AP间无缝漫游，切换时间≤100ms）
  - 安全通信协议（RSSP-I/RSSP-II，带时间戳+序列号+MAC校验）
- 移动闭塞原理：
  - 无固定区段划分，MA基于前车尾部的安全防护包络
  - 追踪间隔可压缩至90秒以下（设计值90s，实际运营110-120s）
  - 安全制动模型：N+2冗余，最不利条件下单程制动+反应时间+安全余量
- 定位技术：
  - 主用：测速电机+应答器校正（绝对位置参考点）
  - 辅助：雷达（多普勒测速）+加速度计（坡度补偿）
  - 定位误差管理：Δpos = 测距误差 + 滑行/空转累计误差 + 应答器校准误差
  - 硬定位复位点：应答器组、车站停车点对位、ZEI（零速积分初始）
- 运行模式：
  - CAM（完全自动驾驶模式）：ATO自动驾驶，无需司机操作
  - ATO模式：司机监督，ATO控制牵引/制动
  - ATP模式（IATPM/限速模式）：ATP防护，司机人工驾驶
  - 限制模式（限制人工驾驶）：≤25km/h，司机负责全部
  - 非限制模式（非限制人工驾驶）：无ATP防护，纯人工
  - RM（蠕动模式）：极低速（≤5km/h），用于紧急对位/故障恢复
- 门安全联锁：
  - 列车停准停稳→ 开门允许 → 站台屏蔽门与列车门对齐→ 联动开启
  - 门关闭锁紧检测 → 站台屏蔽门闭锁 → ZC允许发车 → 牵引使能
  - 列车启动后若任一门未锁紧→ 触发紧急制动
```

#### 3.1.8 TACS（列车自主控制系统）领域知识

```
TACS（Train Autonomous Control System，列车自主控制系统）领域知识：
- 核心理念：以列车为中心（Train-Centric），列车自主计算MA，
  轨旁设备（OC/目标控制器）仅执行控制命令
- 与CBTC的本质区别：
  - CBTC：ZC计算MA → 发给VOBC → VOBC执行防护
  - TACS：VOBC自主计算MA（通过T2T通信获取前车位置），
    OC目标控制器接收列车命令执行道岔/信号控制
- 系统架构：
  - 车载自主决策单元（VADU/VTDC）：融合定位+安全计算+MA自主推算
  - 目标控制器（OC/OMC）：轨旁节点，接收列车命令驱动道岔/屏蔽门
  - 轨旁资源管理器（TRM/RC）：管理道岔/区段等轨旁资源互斥访问
  - 列车调度管理器（TSM/TSR）：全局运行调度与冲突解决
  - T2T通信模块（T2T Link）：列车间直接通信（LTE-V/5G NR-V2X）
- T2T（Train-to-Train）通信：
  - 车车直接通信，时延 ≤ 20ms（典型值）
  - 交换信息：列车ID、位置、速度、方向、MA请求、紧急状态
  - 无需轨旁中继，提升系统韧性和响应速度
- 资源管理模型：
  - 轨旁资源（道岔、区段、站台）由列车按需申请+释放
  - 资源状态：空闲→预占→锁定→使用→释放
  - 冲突检测分布式完成：TSM进行全局优化，局部冲突T2T协商解决
- 全电子联锁替代趋势：
  - 取消传统CBI（计算机联锁），由OC/目标控制器直接驱动道岔
  - OC安全等级SIL 4，通过电子控制单元实现道岔转换和锁闭
  - 联锁逻辑从集中式（CBI）变为分布式（TSM+OC+T2T协同）
- 运行场景差异：
  - 进路建立：列车发送资源请求→TSM分配→OC执行转换→列车确认→自主MA计算
  - 折返作业：列车自主检测折返轨空闲→T2T通知反向列车→自主折返
  - 备用模式：保留ZC后备（降级为传统CBTC模式）或降级为固定闭塞
- TACS优势：
  - 追踪间隔进一步压缩（理论≤80秒）
  - 减少轨旁设备（无需ZC、部分联锁柜），降低全生命周期成本
  - 系统韧性强（T2T通信+分布式决策，单点故障影响范围小）
  - 折返效率提升（车载自主折返流程）
- 国内TACS方案：
  - 中国通号：TACS系统（基于LTE-M的T2T+OC方案）
  - 铁科院：CBTC/TACS混合演进方案（保留ZC同时支持T2T增强）
  - 各城轨公司试点：深圳、上海、北京等城市陆续开展TACS工程试点
- 安全原则：
  - ATP功能仍在车载保存（不因架构变化降低安全等级）
  - 分布式联锁逻辑必须等价于集中式联锁的安全约束
  - 资源冲突由TSM确保互斥，T2T通信增加交叉验证
  - T2T通信失效时的降级路径：TSM集中仲裁模式→ZC后备模式→限制人工
```

#### 3.1.9 CBTC/TACS 运行场景分析指引（提示词专用）

```
CBTC/TACS系统需求分析特殊规则（适用于 prompt 工程）：
1. 子系统交互识别：CBTC场景优先识别ATS/ATO/ATP/ZC/VOBC的交互边界，
   交互密集型场景（MA更新、位置报告、门联锁）自动触发sequenceDiagram选择
2. 移动闭塞关键要素：MA计算依赖前车位置+线路数据+安全包络，
   所有MA相关FR必须包含"安全防护包络"和"最不利位置偏移"的描述
3. 定位可信度管理：每项涉及定位的FR必须覆盖定位误差来源
   （滑行/空转、应答器漏读、轮径磨损）和安全冗余处理
4. TACS分布式逻辑：T2T通信+资源申请→分配→锁定→释放周期，
   资源管理FR必须包含冲突检测和互斥访问的TSM仲裁机制
5. 降级模式全覆盖：CBTC需覆盖3级以上降级路径
   （CAM→ATPM→RM→限制人工），列出每种模式的安全防护手段
6. 折返场景时序优先：折返作业涉及多系统交互
   （VOBC/ATS/OC/ZC/T2T），sequenceDiagram优先级高于flowchart
7. 门安全联锁不可分割：列车门+屏蔽门联动是单原子FR，
   不可分解为"开门/关门/发车"等多个FR
8. SIL约束追溯：ZC、VOBC、OC、T2T安全功能均标注SIL 4，
   DCS通信标注SIL 2（传输通道）或SIL 4（安全应用层）
9. CBTC/TACS场景测试集建议（见测试计划扩展）
```

### 3.2 输出 schema 扩展（可选）

考虑在 `Requirements` 接口中新增可选字段 `silLevel` 和 `domain`：

```typescript
interface Requirements {
  // ... existing fields
  domain?: string  // 自动识别的业务领域：railway-signal/general/medical/aviation
}
```

在 System Prompt 中要求 LLM 识别场景所属领域，填入 `domain` 字段，触发对应领域规则。

### 3.3 改动范围

| 文件 | 改动 |
|------|------|
| `src/utils/prompt.ts` | `SYSTEM_PROMPT` 追加术语附录 + 联锁规则 + SIL 约束 + CBTC/TACS 领域知识（~400 行新内容） |
| `src/types/index.ts` | 可选新增 `domain?: string` 字段 |
| `src/utils/parser.ts` | 解析 `domain` 字段 |
| `analyzer.html` | `SYSTEM_PROMPT` 同步追加相同内容 |
| `src/components/RequirementsReport.vue` | 可选展示 `domain` 徽标 |
| `analyzer.html` 模板 | 可选展示 `domain` 徽标 |
| `CONTEXT.md` | 更新 v2.3.0 记录 |

---

## 四、技术评估

### 4.1 requirementDiagram 可行性

| 方面 | 评估 |
|------|------|
| Mermaid.js 版本 | v11+ 已支持，CDN 的 mermaid@11 无需升级 |
| LLM 生成质量 | 需要 prompt 示例引导，Qwen2.5-1.5B 的 capacity 可能不足——复杂 requirementDiagram 含多个 element+关系，1.5B 模型可能输出格式错误。建议设此类型为 "API only" 或做降级兜底 |
| 降级生成 | 从 FR/NFR/stakeholders 数据可以机械生成基本 requirementDiagram，但关系链质量取决于 FR 之间的派生关系 |
| 风险 | 小模型输出格式不稳定 → 降级到机械生成即可 |

### 4.2 铁路信号领域增强可行性

| 方面 | 评估 |
|------|------|
| Prompt 长度 | 约 +200 行/1500 tokens，在 max_tokens=4096 范围内 |
| 通用场景影响 | 领域术语对非铁路场景应无负面效果（LLM 会忽略不相关指令） |
| 效果验证 | 可用测试集 TC-001~TC-014 逐条验证 FR 质量和图表类型匹配度 |
| 风险 | 低——纯 prompt 改动，不影响现有功能 |

### 4.3 推荐实施顺序

1. **先做方向 B（铁路信号领域增强）** — 纯 prompt 改动，风险低，收益直接可测
2. **再做方向 A（requirementDiagram）** — 需要新增代码 + 降级生成逻辑

---

## 五、测试计划

### 5.1 铁路信号增强验证

使用现有测试集 TC-001~TC-014 进行 A/B 对比：

| 指标 | 当前基线 | 目标值 |
|------|----------|--------|
| 联锁术语使用准确性 | 待测 | ≥ 90% 术语正确 |
| FR 覆盖关键系统能力比例 | 待测 | ≥ 80% |
| 图表类型匹配度 | 待测 | ≥ 85% |
| sequenceDiagram 在联锁场景的选择率 | 待测 | ≥ 60%（联锁多条件验证场景） |

### 5.2 requirementDiagram 验证

- 测试 requirementDiagram 在 Mermaid.js v11 上的渲染正确性
- 验证降级生成函数在无 LLM 输出时是否可用
- 检查 LLM（Qwen2.5-1.5B）是否能输出合法 requirementDiagram 语法

### 5.3 CBTC/TACS 场景验证（扩展测试集 TC-015~TC-031）

新增 CBTC/TACS 测试用例，验证领域知识注入后的分析效果：

| 编号 | 场景 | 预期图表类型 | 预期 FR 数量 | 关键验证点 |
|------|------|-------------|-------------|-----------|
| TC-015 | 移动闭塞条件下列车追踪运行 | sequenceDiagram | 4-6 | MA更新、定位误差、安全包络 |
| TC-016 | CBTC 门安全联锁（列车门+屏蔽门联动） | sequenceDiagram | 3-4 | 门联锁原子FR、发车使能条件 |
| TC-017 | 列车定位失效降级处理 | stateDiagram-v2 | 3-5 | 定位传感器融合、应答器校正、降级模式转换 |
| TC-018 | ATS 运行图自动调整与进路自动设置 | flowchart | 4-5 | ATS/联锁接口、运行图冲突检测 |
| TC-019 | TACS 列车自主折返 | sequenceDiagram | 4-6 | T2T通信、资源申请释放、折返时序 |
| TC-020 | CBTC→TACS 混合系统切换 | flowchart | 3-4 | 架构切换、ZC后备模式、降级一致性 |
| TC-021 | ZC 越区切换（MA 连续性保持） | sequenceDiagram | 4-5 | ZC间安全协议、MA预计算、超时惰行 |
| TC-022 | CBTC 驾驶模式切换 | stateDiagram-v2 | 4-6 | CAM↔ATPM↔RM↔EUM四态转换、升级恢复验证 |
| TC-023 | 车辆段列车唤醒与休眠 | flowchart | 4-5 | DCS漫游、初始定位、ZC注册、状态保存 |
| TC-024 | 轮径磨损与定位误差校准 | flowchart | 4-5 | 三级偏差阈值、安全包络自适应、应答器校准 |
| TC-025 | 站台列车越过停车窗控制 | sequence+flow | 4-5 | 回退授权、越限禁止回退、乘客疏散与跳停 |
| TC-026 | TACS 列车唤醒与 T2T 网络初始化 | sequenceDiagram | 4-5 | 纯TACS初始化、TSM资源域分配、OC后备 |
| TC-027 | 交叉冲突资源死锁与 TSM 仲裁 | sequenceDiagram | 4-6 | 冲突检测、优先级仲裁、替代路径规划 |
| TC-028 | TACS 列车灵活编组（虚拟连挂） | sequenceDiagram | 4-6 | T2T编组协商、CACC跟驰、制动能力校验、解编 |
| TC-029 | TACS 全自动无人驾驶（UTO/GoA4） | sequence+flow | 4-6 | ODS障碍物检测、远程处置、烟火疏散 |
| TC-030 | TACS 车站联锁接口交互 | sequenceDiagram | 4-5 | TSM↔CBI双模型一致性比对、进路降级 |
| TC-031 | ATS全局调度：CBTC+TACS混跑时刻表 | flowchart | 4-5 | 双制式时刻表、双通道指令分发 |

| 新增指标 | 说明 | 目标值 |
|----------|------|--------|
| CBTC 子系统识别率 | 是否正确识别 ATS/ATO/ATP/ZC/VOBC 角色 | ≥ 85% |
| TACS 资源管理 FR 完整性 | 资源申请→分配→锁定→释放周期覆盖率 | ≥ 80% |
| 降级模式覆盖度 | CAM→ATPM→RM→限制人工的完整降级链 | ≥ 3/4 级 |
| T2T 通信场景的 sequenceDiagram 选择率 | 应高于 flowchart | ≥ 70% |
| 虚拟编组识别率 | T2T编组协商+制动校验+CACC是否正确识别 | ≥ 80% |
| GoA 等级匹配率 | 自动驾驶等级与场景匹配 | ≥ 85% |
| 包络安全偏移覆盖率 | MA/资源 FR 含最不利位置偏移描述 | ≥ 90% |

---

## 六、实施工作量估计

| 模块 | 文件 | 估计行数 | 复杂度 |
|------|------|----------|--------|
| Prompt 术语+规则（含联锁/IOM/MMS/智能运维） | prompt.ts, analyzer.html | ~300 行 | 低 |
| CBTC/TACS 领域知识补充（含 prompt 规则） | prompt.ts, analyzer.html | ~150 行 | 低 |
| requirementDiagram 降级生成 | mermaidGenerator.ts, analyzer.html | ~60 行 | 中 |
| DIAGRAM_TYPES 扩展 | MermaidDiagram.vue, AnalysisResult.vue, analyzer.html | ~15 行 | 低 |
| 类型 + 解析扩展 | types/index.ts, parser.ts | ~10 行 | 低 |
| UI 展示（domain/SIL） | RequirementsReport.vue | ~20 行 | 低 |
| 测试验证（含 CBTC/TACS 新增 TC-015~TC-020） | 手动运行测试集 | — | 中 |

合计：~550 行新增代码，主要为 prompt 和降级生成。
