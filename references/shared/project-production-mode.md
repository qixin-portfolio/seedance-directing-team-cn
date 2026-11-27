# AI 影视生产模式

当用户在做连续项目、短片、广告片或长片，而不是单条试验 Prompt 时，切换到**生产模式**。

## 生产闭环

`SCRIPT / BRIEF → DIRECTING COUNCIL → ASSET PREP → ASSET STRESS TEST → INPUT DESIGN GATE → SCENE MAP LOCK → SHOT CARD → (生成门) → WRITER → AUDITOR → GENERATE → CANDIDATE REVIEW → SELECTS / WORKBENCH PATCH / CONTROLLED EXPERIMENT → APPROVED → LEDGER / LEARNING`

| 阶段 | 导演层负责 | 执行层负责 |
|---|---|---|
| DIRECTING COUNCIL | 总导演契约、表演谱、镜内生态、摄影设计（[导演组](../director/role-council.md)） | 版本/平台预判、可行性提醒 |
| ASSET PREP / STRESS TEST | 角色表演档案、尺度与光线契约 | Canonical Descriptor、状态资产、压力测试 |
| INPUT DESIGN GATE | 判断哪些状态必须先被看见 | Layout / Shot State Plate、Reference Role、`INPUT_READY` |
| SCENE MAP LOCK | master、主观视点、blocking states | SCENE GEOGRAPHY LOCK 文本 |
| SHOT CARD | GOAL / TASK / DRAMATURGY / 镜内任务 | 首帧需求、素材职责 |
| WRITER | 提示词导演编译 | Compact / 15-Block / 多镜头分镜 |
| AUDITOR / REVIEW | 角色意见、P0/P1/P2、过保修废 | Auditor（BLOCKER/WARNING/NOTE）、故障来源、编辑/重抽/PATCH |
| CANDIDATE / SELECTS / EXPERIMENT | 总导演裁决可用区间 | 候选评分、Selects Manifest、控制变量实验 |
| LEDGER / LEARNING | 场记三本账、知识卡 | 版本日志、O 类参数 `valid_as_of` |

## 阶段门禁

- **ASSET PREP**：人物、场景、道具先有稳定资产；关键身份建立 Canonical Descriptor。
- **ASSET STRESS TEST**：静图好看不等于视频可用；在真实镜头条件下验证。
- **INPUT DESIGN GATE**：检查身份、空间、动作路径和第 0 帧物理状态是否可读；必要时先补 Layout Plate 或 Shot State Plate，达到 `INPUT_READY` 后再写正式 Prompt。见 [输入设计与预演](../seedance/input-design-and-previs.md)。
- **SCENE MAP LOCK**：先锁场景地理、空间锚点、摄影轴线和方向规则。
- **SHOT CARD**：镜头先有导演意图、人物任务、戏剧变化、blocking 和 edit hook；复杂物理动作再补力量来源、传力路径、承受对象反应、稳定终态与必要 coverage，见 [物理动作](../director/physical-action-design.md)。
- **生成门**：导演组档在 WRITER 前需要用户明确授权；标准档跳过。
- **WRITER**：生成 Compact、Production 15-Block 或多镜头分镜。
- **AUDITOR**：只检查，不重新创作；发现矛盾后指定应返修区块。
- **GENERATE / CANDIDATE REVIEW**：先声明 FINAL SHOT 或 MATERIAL SEQUENCE，再按身份、空间、动作、物理、摄影、表演声音和可剪性评估候选。
- **SELECTS**：记录候选任务 ID、可用 IN–OUT、叙事功能和区间外失败；用户确认后标记 `SELECT_APPROVED`。
- **CONTROLLED EXPERIMENT**：预先声明保持不变项和唯一变量；不得同时修改模型、Prompt、参考图、时长和机位后归因。见 [生成实验与 Selects](generation-experiments-and-selects.md)。
- **WORKBENCH**：只修改失败区块，保留已工作的部分。
- **APPROVED**：只有用户明确说“锁定这个版本”“标记为 APPROVED”或“后续沿用这一版”才锁定，见 [连续性](continuity.md#4-approved-锁定)。

## 什么时候不启用

用户只要一个简单 4–15 秒单镜、一次局部编辑或一次提示词优化时，不强迫进入完整生产模式；仍使用轻量路由。

## 可选摄影预演支路

需 Blender 控制的镜头在 SHOT CARD 内完成 [摄影决策](../director/cinematography-direction.md)，进入 [Blender 交接、预演与审查](../director/blender-camera-previs.md)，再复查 INPUT DESIGN GATE 并进入 WRITER。初次 Input Gate 可先记录待补预演；完整生成就绪状态须在输入可读后确认。已有预演从检查/继承开始，简单镜头跳过此支路。
