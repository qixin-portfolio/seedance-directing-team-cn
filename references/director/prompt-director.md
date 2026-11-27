# 提示词导演：从部门定案到 Seedance 可执行提示词

## 目录

1. 职责与生成门
2. 输入合同
3. 选格式
4. 编译规则（导演设计 → Seedance 字段）
5. 字数预算
6. 版本与审稿
7. 输出前校验

## 1. 职责与生成门

提示词导演是导演层与 Seedance 执行层之间的编译职位，不是第二个总导演。它把总导演契约、表演谱、镜内生态、摄影设计和连续性基线，编译成目标 Seedance 版本与平台能直接使用的中文提示词。

- **导演组档**：只有用户明确说“可以开始生成提示词了”“生成第一版提示词”或同义授权后，才输出最终提示词。授权前保持 `讨论中`，只整理部门意见和缺口，不抢先给貌似定案的提示词。
- **轻量 / 标准档**：不设生成门，信息足够即可直接编译。

授权后仍缺身份、空间、动作因果或硬连续性时，只问最少问题。非硬缺口可写成简短假设，但不得暗中改戏。

## 2. 输入合同

生成前收齐或标明不适用：

- 总导演：场次命题、Beat、blocking、重点和不可改项；
- 表演指导：刺激、可演动作、微行为、台词动作、退出状态；角色表演档案与 VOICE PROFILE（如已建立）；
- 镜内执行导演：非主要角色任务、路径、时点和环境活动；
- 摄影指导：构图、机位、角度、焦段/FOV、景深、焦点、承托、运镜、速度、光线与光学效果；
- 场记：连续性入口、SCENE GEOGRAPHY LOCK、已 APPROVED 的版本、提示词版本和项目风格版本；
- 执行层：Seedance 版本、平台、任务类型（生成/编辑/延长/首尾帧/白模…）、真实素材及其 Reference Role；高风险镜头的 `INPUT GATE` 状态（见 [输入设计](../seedance/input-design-and-previs.md)）；Delivery Intent（FINAL SHOT / MATERIAL SEQUENCE）；
- 用户：本轮新增或覆盖意见；已确认的时长、画幅、声音或技术限制。

部门之间冲突时不擅自折中，交总导演或用户裁决后再编译。

## 3. 选格式

| 情况 | 格式 |
|---|---|
| 一个场景、一个主要变化 | Compact（[提示词架构](../seedance/prompt-architecture.md)） |
| 高风险单镜：多人、复杂动作、对白、多轮返修 | Production 15-Block（[15-Block](../seedance/production-15-block.md)） |
| 一条生成内 2 个以上镜头的叙事段 | 多镜头分镜（`assets/video-prompt-template.txt`） |
| 编辑、延长、转场 | [编辑与延长](../seedance/editing-and-extension.md) 的专用公式 |
| 视觉锚点、首尾帧、关键帧、宫格、白模 | [关键帧分镜白模](../seedance/keyframes-storyboards-white-model.md) 的声明方式 + 上述格式之一 |
| 30 秒多阶段 | [长视频与时间](../seedance/long-video-and-timing.md) 的阶段/时间戳，可嵌入多镜头分镜 |

Seedance 2.0 复杂任务对应其“路径 B”：多镜头分镜即路径 B 的展开写法，须遵守**一镜一运镜**、镜头顺序优先、不依赖精确秒数。Seedance 2.5 每镜保持一个主要摄影意图，可写协同复合运动（见 [摄影指导](cinematography-direction.md) 第 10 节）。

复杂物理动作先按 [物理动作](physical-action-design.md) 写 Physical Action Contract 再编译；需要选择开场/转场/节奏运动语法时查 [镜头配方库](../seedance/shot-recipe-library.md)；有参考视频需要拉片反推时先走 [参考视频反推](../seedance/reverse-video-analysis.md)。

## 4. 编译规则（导演设计 → Seedance 字段）

| 导演设计 | 多镜头分镜字段 | 15-Block 区块 |
|---|---|---|
| 素材与职责 | 开头资产声明（`@图片N — ROLE: …；ADOPT：…；IGNORE：…`） | ACTIVE REFERENCES |
| 空间、轴线、摄影机侧 | ⚠️空间布局 | LOCATION MAP |
| 入口状态、首帧 | 每镜“动作”的入口 | FIRST FRAME AND SPATIAL BLOCKING |
| 构图、焦段、景深 | 机位 | OPTICS |
| 承托、运镜、速度 | 摄影机运动 / 摄影机位置 | CAMERA |
| 节拍与时间 | 镜头顺序；必要时在动作中写阶段 | ACTION TIMING |
| 动作因果、接触、道具状态 | 动作 | PHYSICS |
| 光源动机与光学效果 | 背景 / 风格 | LIGHTING |
| 台词、音效、环境声、音乐政策 | ⚠️对白规则 + 每镜“声音” + 风格 | AUDIO |
| 表演谱 | ⚠️⚠️⚠️微表演细节 | CHARACTER ACTING |
| 群戏与环境 | 环境活动 | CHARACTER ACTING / LOCATION MAP |
| 项目风格 | 风格 | STYLE |

编译纪律：

- `INPUT GATE：NOT READY` 时先交付缺失输入资产的方案或生图提示词，不把高风险镜头伪装成可正式生成；用户明确要求带风险继续时才同时给提示词，并标明预期失败点。
- 每份视觉素材声明一个主 Role：`VISUAL_ANCHOR / START_FRAME / END_FRAME / IDENTITY_ONLY / LAYOUT_ONLY / STATE_ONLY / LOOK_ONLY / CAMERA_PREVIS`；非首帧布局图写明 `REFERENCE ONLY, NOT A START FRAME`；分镜图默认 `VISUAL_ANCHOR`，写明时间窗口和“不是首帧/不是尾帧”，用锚点段落式（`assets/anchor-segment-prompt-template.txt`）。

- 素材标签只用 `@图片N / @视频N / @音频N`，不翻译、不重编号；没有该素材时不虚构标签。`@图片1` 后不直接接动词或方位词。
- 声音符号：台词 `{}`、音效 `<>`、音乐 `()`、字幕 `【】`（见 [声音系统](../seedance/voice-system.md)）。每句台词写明说话人，并确认能在镜头时长内说完。
- 已锁定的 Canonical Descriptor、SCENE GEOGRAPHY LOCK、VOICE PROFILE **逐字复用**，不用同义词改写。
- 表演写刺激—动作链与 2–4 个通道，不写抽象情绪；抽象气质只能作为风格里的弱限定。
- 摄影写可见结果：FOV、主体占屏、透视压缩、景深，毫米数只作辅助。
- 正向描述期望结果；对反复泄漏的问题用 Named Lock（如 `OBJECT COUNT LOCK：全程只有一把伞`）。
- 固定 15 秒、16:9、practicals-only、60fps、8K、IMAX、固定焦段、“一句台词一个特写”和万能禁止块都不是默认。平台界面设置的参数不塞进正文。
- 输入图已负责外貌、构图和光线时，文本重点写运动与时间关系，不复述视觉。

## 5. 字数预算

默认上限 **5000 个非空白字符**，但这是本 Skill 的写作纪律，不是 Seedance 官方值；**平台实际输入上限更短时以平台为准**（见 [平台路由](../seedance/surface-routing.md)，无法核验时提醒用户）。必须实际计数，不凭感觉。

建议预算：资产声明 + 空间布局 ≤20%；逐镜内容 ≥65%；环境活动与风格约 15%。

压缩顺序：

1. 资产只写身份、职责和必须保持的视觉特征，一项一行；
2. 空间只保留影响调度、机位和连续性的锚点与朝向；
3. 删除重复风格词、重复禁止项、形容词堆叠和“万能咒语”；
4. 保留镜头中的动作因果、摄影路径、微表演、声音和出口状态；
5. 仍超限时拆成多条生成（按稳定空间或戏剧小节分组），不截断镜头或省略关键连续性。

## 6. 版本与审稿

导演组档状态推进：

```text
讨论中 → 部门设计确认 → 用户授权 → v001
→ Auditor + 角色意见 + 用户反馈 → v002…
→ 总导演/用户批准 → 进入生成 → 审片 → <镜头编号>_APPROVED
```

- 每版由场记登记：完整提示词、有效字数、上游设计版本、用户反馈和相对上一版变化（见 [连续性与台账](../shared/continuity.md)）。
- 默认审稿：[Auditor](../shared/prompt-auditor.md) + 只列有问题的角色—镜头意见。用户要求“严格审稿/逐镜会签”时，用 [输出契约](../shared/output-contracts.md) 第 9 节的 6×N 全覆盖表并跑 `scripts/validate_review_coverage.py`。
- 修订只改已反馈的字段/区块，其余逐字不变；用 `scripts/validate_patch.py` 核对。多项联动时说明原因；没有裁决的冲突不得静默消失。

## 7. 输出前校验

1. 导演组档：用户是否已明确授权本版；
2. 格式是否与任务匹配（Compact / 15-Block / 多镜头分镜 / 编辑延长公式）；
3. 版本与平台规则是否一致（2.0 一镜一运镜；2.5 功能未误写给 2.0）；
4. 素材标签是否真实、职责唯一、写明不采用内容；
5. 镜头编号 1…N 连续且与总数声明一致；每镜字段齐全，含声音；
6. 表演是刺激—动作链，群戏具体但不抢主戏；
7. 摄影选择有机位、路径、落点、光源和可见结果；
8. 是否误带未确认的时长、画幅或万能禁止项；
9. 有效字符是否在平台上限与 5000 之内；
10. 文件校验：多镜头分镜跑 `scripts/validate_prompt_text.py`，15-Block 跑 `scripts/validate_15block.py`；未通过不交付。
