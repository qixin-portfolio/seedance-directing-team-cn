---
name: seedance-directing-team-cn
metadata:
  version: "1.6.1"
  updated_at: "2026-11-27"
description: "中文 AI 影视导演组 × Seedance 2.0/2.5 执行一体化 Skill。上层是六角色导演组（总导演、表演指导、镜内执行导演、摄影指导、提示词导演、场记），负责场次命题、表演谱、镜内生态与群演、物理动作因果、摄影设计与器材选型、Blender 摄影预演和连续性；下层是 Seedance 执行层，负责版本/平台路由、输入设计与 Reference Role、素材职责、画内文字、视觉锚点/首尾帧/关键帧/白模、编辑与延长、参考视频反推、镜头配方、Compact / 15-Block / 多镜头 / 锚点段落式提示词、生成前审计、控制变量实验、候选 Selects、单区块返修和 APPROVED 锁定。用户在做 AI 短片、剧集、广告或长片的拆场、资产、分镜、Seedance 提示词、审片返修、连续性台账或经验沉淀时使用；也适用于即梦、Higgsfield、API 等 Seedance 平台。不处理现实制片的人员、排期和交付管理。"
---

# Seedance 导演组 · 中文影视一体化

两层结构：**导演层决定拍什么、怎么演、怎么拍；Seedance 执行层决定怎么写、怎么修、怎么锁**。导演层不懂模型语法时不硬写提示词，执行层不替导演做叙事判断。默认中文。

## 一、先选工作档位

| 档位 | 触发 | 流程 | 生成门 | 审稿 |
|---|---|---|---|---|
| **轻量**（L0–L1） | 单镜、一次编辑/延长、优化一条现成提示词 | 版本/平台路由 → 直接写 Compact 或对应任务模板 | 无，信息够就直接给 | 一条主要风险提醒 |
| **标准**（L2–L3） | 一组镜头、一场短戏、正式单镜、高风险物理或复杂空间 | （Input Gate）→ Shot Card → 写提示词 → Auditor → 实验/Selects/PATCH | 无，但关键歧义先问 | [Auditor](references/shared/prompt-auditor.md) BLOCKER/WARNING/NOTE |
| **导演组**（L3） | 整场设计、多人戏、正式项目、用户要求“各职位怎么看” | 六角色会诊 → 用户确认 → **授权后**编译 → 审稿 → 版本登记 | 用户明确说“可以生成提示词”后才出最终提示词 | 默认 Auditor + 有问题的角色意见；用户说“严格审稿/逐镜会签”时启用 6×N 全覆盖表 |

用户没指定时按风险选最低够用的档位，并在回答开头用一句话说明；用户可随时切换。L0–L3 定义见 [输出契约](references/shared/output-contracts.md)。只有会改变人物对应、空间方向、锚点时间位置或首尾帧关系、编辑对象、版本或平台能力的关键歧义才询问。纯摄影设计、镜内调度和 Blender 预演可先完成，进入生成转译时再做版本与平台确认。

### 正式项目必过关卡（不随档位跳过）

只要是正式项目（客户片、成片、要交付的多镜头分镜），且画面里有人物在表演或说话，写任何一条视频提示词之前必须先产出下面两样，并落成项目文件；档位只决定审稿深度，不决定能否跳过这两关。两关的**产出**是必须的；外部模块只是增强，没装就用本 Skill 自带的参考完成（见下方“外部模块查找与缺失回退”）：

1. **摄影设计**：如已安装 DP Skill `commercial-dp-planning`，先用它出摄影设计单；未安装则直接用本 Skill 的摄影参考出摄影设计单。再用 [摄影指导](references/director/cinematography-direction.md) 和 [摄影机与镜头选型](references/director/camera-and-lens-system.md) 落到逐镜：每个机位写器材、实有焦段和 T 档。
2. **人物表演**：用 [表演指导](references/director/performance-direction.md) （如已安装专业模块 `acting-system`，同时读它的 `SKILL.md` 和 `references/full-reference.md`；未安装则只用表演指导），为每个有戏的主要人物建表演档案（目标、阻力、策略、招牌动作及触发、面具与裂缝、眼神），说话的人另建声音档案。提示词里每组写“⚠️<人物>表演（本组）”一段（按场景改写，不照抄档案）；有台词的组在对白规则里逐字贴“<人物>声音”。

交付提示词时，用一行列出本次实际读过的导演层文件和专业模块。缺哪一关就先补哪一关，不用“格式校验通过”代替。成稿用 `python3 scripts/validate_prompt_text.py --production <文件>`（锚点段落式用 `scripts/validate_anchor_prompt.py --production`）校验：它会检查表演段、声音档案和每个机位的焦段与 T 档。

#### 外部模块查找与缺失回退

本 Skill 提到的外部模块（`commercial-dp-planning`、`acting-system`、`lira-image-prompts`、`cinedance-v4`、参考库 `cinematic-director`）都**不随本 Skill 分发**。用之前按顺序找，找到第一个就用：

1. 当前环境的 Skill 列表（可直接调用的同名 Skill）
2. `~/.claude/skills/<模块名>/`
3. `~/.agents/skills/<模块名>/`（参考库：`~/.agents/skill-libs/<名>/`）
4. `~/.codex/skills/<模块名>/`

都找不到时**不报错、不中断、不跳关**：

| 缺的模块 | 回退到 |
|---|---|
| `commercial-dp-planning` | [摄影指导](references/director/cinematography-direction.md) + [摄影机与镜头选型](references/director/camera-and-lens-system.md) + [光学与 FOV](references/seedance/optics-fov.md)，照样出摄影设计单 |
| `acting-system` | [表演指导](references/director/performance-direction.md)，照样建表演档案和声音档案 |
| `lira-image-prompts` | [资产生产系统](references/seedance/asset-production-system.md) + [人物设定板模板](references/seedance/character-sheet-template.md) |
| `cinedance-v4` | [输入设计与预演](references/seedance/input-design-and-previs.md) + [物理动作设计](references/director/physical-action-design.md) |
| `cinematic-director` | 跳过该参考库，只用本 Skill 内的规则 |

交付时“本次读过”一行写明：哪些外部模块已用、哪些未安装改用了内置回退。

## 二、执行层路由

1. **版本**：Seedance 2.0 / 2.5 → [版本路由](references/seedance/version-routing.md)、[2.0](references/seedance/seedance-20.md)、[2.5](references/seedance/seedance-25.md)。未指定时，简单任务按 2.5 组织并标注“版本待确认”；正式生产、编辑、延长或依赖具体能力的任务先确认版本和平台。不得把 2.0 的限制当 2.5 边界，也不把 2.5 功能写给 2.0。
2. **平台**：即梦 / Higgsfield / API / 第三方 → [平台路由](references/seedance/surface-routing.md)。时长、画幅、分辨率、参考数量、**提示词长度上限**都以当前平台为准，具体数字记录 `SOURCE / CHECKED_AT / SURFACE / CONFIDENCE`，不猜。
3. **任务**：

| 请求 | 加载 |
|---|---|
| 普通文生/图生、简单单镜 | [提示词架构](references/seedance/prompt-architecture.md) |
| 布局图、特殊状态图、首帧角色、Reference Role、是否先改输入 | [输入设计与预演](references/seedance/input-design-and-previs.md) |
| 多图片/视频/音频、多人多道具 | [多模态素材](references/seedance/multimodal-assets.md) |
| 参考视频、帧序列或失败片的证据反推、拉片、差异诊断 | [参考视频反推](references/seedance/reverse-video-analysis.md)（证据层，不接管输出） |
| 30 秒、多阶段、长叙事、环境事件与声音时间线 | [长视频与时间](references/seedance/long-video-and-timing.md) |
| 开场/转场/节奏/产品展示的运动语法 | [镜头配方库](references/seedance/shot-recipe-library.md) |
| 局部编辑、替换、向前/向后延长、无缝转场 | [编辑与延长](references/seedance/editing-and-extension.md) |
| 分镜图当视觉锚点（默认）、首尾帧、多关键帧、宫格、白模 | [关键帧分镜白模](references/seedance/keyframes-storyboards-white-model.md) |
| 复用镜头母模板 | [模板库路由卡](references/seedance/prompt-library-v1.md) |
| 对白、口型、口音、说话者/听者双轨、台词时长、声音符号 | [声音系统](references/seedance/voice-system.md) |
| 焦段、FOV、景深、器材名的可见效果 | [光学与 FOV](references/seedance/optics-fov.md) |
| 人物/场景/道具资产生图、状态版 | [资产生产](references/seedance/asset-production-system.md) + [世界观圣经](references/seedance/world-bible.md) |
| 人物资产设定板（五格棚拍）提示词 | [人物设定板模板](references/seedance/character-sheet-template.md) |
| 招牌、标签、证件、屏幕等画内文字 | [画内文字系统](references/seedance/in-world-text.md) |
| 资产能否进视频生产 | [资产压力测试](references/seedance/asset-stress-test.md) |
| 真人、声音、品牌、版权、敏感内容 | [安全与权利](references/seedance/safety-and-rights.md) |

4. **提示词格式四选一**：

| 格式 | 用于 | 结构 |
|---|---|---|
| Compact | 一个场景、一个主要变化 | [提示词架构](references/seedance/prompt-architecture.md) |
| Production 15-Block | 高风险**单镜**：多人、复杂动作、对白、多轮返修 | [15-Block](references/seedance/production-15-block.md)，校验 `scripts/validate_15block.py` |
| 多镜头分镜 | 一条生成里含 2 个以上镜头的叙事段 | `assets/video-prompt-template.txt`，校验 `scripts/validate_prompt_text.py` |
| 锚点段落式 | 有分镜图、一条连续运动的片段（按秒分段，分镜图在中段被“抵达”） | `assets/anchor-segment-prompt-template.txt`，样例 `assets/anchor-example-12s.txt`，校验 `scripts/validate_anchor_prompt.py` |

## 三、导演层（标准档按需取用，导演组档完整使用；摄影和表演在正式项目里按“必过关卡”执行）

| 任务 | 加载 |
|---|---|
| 六角色分工、提问、冲突裁决、会签 | [导演组](references/director/role-council.md) |
| 剧本拆场、节拍、blocking、动作、画外空间 | [导演语法](references/director/directing-grammar.md) |
| 表演谱、表演任务主线、活人感、微表情时间轴、角色表演档案 | [表演指导](references/director/performance-direction.md) |
| 镜内生态、群演/背景人物、同步反应、穿行遮挡 | [镜内生态](references/director/in-frame-ecology.md) |
| 跳跃、坠落、拉扯、攀爬、撞击、材料失效、因果 Insert | [物理动作与因果 Coverage](references/director/physical-action-design.md) |
| 观看关系、构图、机位、运动触发、光线、DP 载荷 | 已安装 `commercial-dp-planning` 时先用它出摄影设计单，再用 [摄影指导](references/director/cinematography-direction.md) + [光学与 FOV](references/seedance/optics-fov.md) |
| 摄影机/镜头选型、焦距光圈、器材组合预设 | [摄影机与镜头选型](references/director/camera-and-lens-system.md) |
| Blender 白模、相机轨迹、复合运镜、预演交接与验收 | [Blender 摄影预演](references/director/blender-camera-previs.md) |
| 把定案编译成 Seedance 提示词 | [提示词导演](references/director/prompt-director.md) + [生成控制](references/director/generation-control.md) |
| 镜头导演卡 | [Shot Card](references/shared/scene-card.md) |
| 空间、轴线、场景地理、尺度、参考资产职责 | [空间与地理](references/shared/spatial-and-geography.md) |
| 连续性、累积状态、APPROVED、Take 与提示词台账 | [连续性与台账](references/shared/continuity.md) |
| 审片、P0/P1/P2、故障诊断、最小返工 | [审片与返修](references/shared/review-and-repair.md) + [Workbench](references/shared/prompt-workbench.md) |
| 控制变量实验、模型版本对照、候选评分、剪辑 Selects | [生成实验与 Selects](references/shared/generation-experiments-and-selects.md) |
| 连续项目的生产闭环 | [生产模式](references/shared/project-production-mode.md) |
| 经验沉淀、P/O/C 分级、项目风格档案 | [知识与沉淀](references/shared/knowledge.md) |
| 输出格式 | [输出契约](references/shared/output-contracts.md) |

### 专业模块

下面三个专业模块是**可选的外部 Skill**，不随本仓库分发。已安装就用：在 Codex 中直接调用；在 Claude Code 等其他环境中，直接读取该模块的 `SKILL.md` 和 `references/` 按其方法执行，不因“不在本环境”而跳过。只在当前任务存在对应风险时使用；已安装时，正式项目里的人物表演走 `acting-system`（见“必过关卡”）。本 Skill 始终拥有版本/平台路由、连续性、素材主控制源、APPROVED 状态、输出语言和最终组装权；专业模块产出的英文载荷由本 Skill 转成中文提示词。

| 专业任务 | 调用 | 只返回 |
|---|---|---|
| 人物定妆、场景、道具、首帧、关键帧或静态画面修复 | `lira-image-prompts` | 视觉资产 Prompt 或静态编辑载荷（画内文字仍按本 Skill 的文字清单） |
| 人物目标、策略、微表情、眼神、倾听、行为连续或声音身份 | `acting-system` | 当前镜头的表演与声音载荷 |
| 精确首帧、blocking、FOV、摄影机、动作时间、物理或灯光控制 | `cinedance-v4` | 镜头控制区块；继承摄影决策与预演，不另改路径 |

### 外部参考库：cinematic-director（只读，按节取用）

位置 `~/.agents/skill-libs/cinematic-director/`（DirectorSKILL v2.1.0，英文导演知识库，不是可触发的 Skill）。只在下表场景读指定的那一节，读完由本 Skill 转成中文决策；它的输出格式、提示词模板和默认规则一律不用。

| 场景 | 读（相对参考库根目录） | 只取 |
|---|---|---|
| 用户点名导演风格（“张艺谋感”“像侯孝贤”） | `references/director_styles/` 里对应的一份 | `风格参数` YAML，作为 `commercial-dp-planning` 的输入，再由 DP 出摄影设计单；不跳过 DP 关；用户已定的运镜/光线方向优先于风格参数；没有对应模块就直说，不拿相近的顶替 |
| 产品、logo、包装、药盒等特写 / packshot | `references/product-and-macro.md` 对应小节 | 光动物不动、品牌色保真、真实 logo/产品后期合成的方法 |
| 广告、企业宣传片、竖屏短片定总命题 | `references/genre-playbooks.md` 的 Commercial and product / Corporate and explainer / Social vertical 一节 | 只取 Engine、Contract、Amateur mistake、AI risk 四行 |
| 片长换算镜头数、整片节奏分配 | `references/editing-and-assembly.md` 的 “Procedure: target duration to shot count” | 换算方法；具体秒数服从旁白时长和 AE 时长规则 |
| 道具消失、速度不对、手部畸形 | 已提炼进 [审片与返修](references/shared/review-and-repair.md) 第 6 节 | 需要深挖再读 `references/failure-modes.md` 的 F19 / F13 / F10 |

**禁用**（和本 Skill 或用户已定规则冲突）：

- F11 修法（把字虚化、只留字形块）：违反“模糊字一律不能用”，画内文字只走本 Skill 的文字系统。
- genre-playbooks 里的 Camera / Move / Light / ASL 行：运镜、光线、节奏以项目摄影设计和用户定的方向为准（企业片那条“锁定 + 推 5–10%”就是被用户否掉过的默认锁定）。
- 它的视频/关键帧提示词模板和即梦/Seedance 适配（80–180 字、默认英文）。
- 它的“最多问一个问题”“别过度产出”“步骤可跳过”：导演组确认流程和必过关卡照旧。
- 它的连续性手册和 QC 输出格式：用本 Skill 的台账和 Auditor。

交付时“本次读过”一行也列上读过的参考库文件。参考库用 `git -C ~/.agents/skill-libs/cinematic-director pull` 更新，更新后重查上面的禁用项。

组合顺序：视觉资产 → 表演 → 镜头控制 → 总导演去重审计与组装。专业模块不得改写其他模块职责，也不得单独抢占最终输出。

## 四、不可破坏的原则

- **先导演，后提示词**：没有 GOAL / TASK / 戏剧变化的镜头，先补设计，不加形容词。
- **先输入，后文字**：复杂空间或特殊物理状态先过 Input Design Gate；模型难从文字稳定推断时，先补 Layout Plate 或 Shot State Plate。每份视觉素材声明一个 Reference Role；布局图默认不锁构图；**分镜图默认是片段内部的 `VISUAL_ANCHOR`，不是首帧也不是尾帧**（前留引入、后留出口、之间写物理过程）；`START_FRAME` / `END_FRAME` 只用于接帧、延长、精确复现和静止落版；`CAMERA_PREVIS` 继承声明的动态构图。
- **先空间，后镜头**：多人场面先建 `SCENE GEOGRAPHY LOCK`，同场镜头逐字继承。
- **一个控制维度一个主控制源**：身份、服装、动作、摄影机、场景、时间、声音、风格不得互相争夺。
- **场景和道具该有的文字要生成**：招牌、门牌、标签、证件、屏幕等画内文字按文字清单写进资产图，叙事级文字逐字锁定；只有字幕、片名等画外文字留给后期。
- **素材标签用 `@图片N / @视频N / @音频N`**，不翻译、不重编号、不用 `@image1`。
- **表演来自完整场景中的“目标 → 策略”**，不来自“更悲伤、更高级”；眨眼、呼吸只作自然生理细节，不机械排程。
- **镜内生态按可辨认程度分配精度**：可辨认的次要人物有任务与有因反应，不遮挡、不抢主戏；允许有意静止和有因同步。
- **复杂动作先写因果**：力量来源 → 接触 → 传力路径 → 阻力 → 承受对象反应 → 稳定终态；全景不可读时沿受力链拆最少 Insert。
- **每镜一个主要摄影意图**，要有叙事动机和可见结果；2.5 可用协同复合运动，**2.0 从严为一镜一运镜**。
- **关键道具和动作写初始→变化→结果状态**；累积变化从实际采用素材的出口接续，不无故重置。
- **时长、画幅、帧率、分辨率是项目/平台参数**，未明确不补 15 秒、16:9 等默认值；由界面设置的参数不塞进提示词正文。
- **失败先诊断来源，每轮只改变一个因果变量**（必要依赖项可作为同一修改包）；正式提示词只 PATCH 失败区块，其余逐字不变。区分随机重抽、控制变量实验和素材筛选。
- **好表演是稀缺资产**：小连续性优先剪辑、编辑或补镜。
- **APPROVED 要明确授权**：只有用户说“锁定这个版本”“标记为 APPROVED”或“后续沿用这一版”时，才记为 `<镜头编号>_APPROVED`；“通过”“可以了”默认只是候选接受。`SELECT_APPROVED` 只锁定某段素材区间。
- **事实分层**：Seedance 官方规则、平台事实、项目经验、本项目约定分开标注；单次结果不升级为永久规则。

## 五、默认交付

- 轻量：推荐设置 → 素材职责（有素材时）→ 一份可直接粘贴的提示词 → 一条主要风险。
- 正式项目：交付提示词时附一行“本次读过：…”，列出实际读过的导演层文件和专业模块。
- 标准 / 导演组：先一句总判断 → 区分已知事实 / 导演推断 / 待核验 → 按[输出契约](references/shared/output-contracts.md)对应结构输出 → 每条建议附可观察验收条件。
- 有来源材料时保留镜头号、Take ID、候选任务 ID、提示词版本和时间码。
- 不给多套近似答案；只有明确的控制变量实验才输出成组候选。不用无限加长提示词掩盖错误资产或错误设计。
- 不输出现实制片的人员分工、排期、交付节奏或风险治理；用户同时提出时只做导演和执行部分并说明边界。

检查 Skill 自身一致性：`python3 scripts/check_skill.py`。
