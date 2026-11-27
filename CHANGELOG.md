# Changelog

## v1.6 — 2026-11-09 · 分镜图默认当视觉锚点，不当首尾帧（用户实测“视觉参考比首尾帧好很多”）

- 新 Reference Role `VISUAL_ANCHOR`：分镜图放在片段内部某个时间窗口，用运镜“抵达”，前有引入段、后有过程/出口段；提示词写明“不是首帧/不是尾帧”。
- 排法（项目经验）：锚点前后各留约 1.5 秒；两锚点之间约 3 秒以上物理过程，禁止直接变形；12 秒 ≤2 个、15 秒 ≤3 个锚点；每个锚点段写抵达方式、文字复述、在锚点上的戏、离开理由；单独写【结束状态】给下一片段接口。
- `START_FRAME` / `END_FRAME` 收窄到：接上一片段实际采用素材的最后一帧、向前/向后延长、精确复现 packshot 或 APPROVED 画面、静止落版、用户明确要求。
- 新增第四种格式“锚点段落式”：`assets/anchor-segment-prompt-template.txt`、用户样例 `assets/anchor-example-12s.txt`、校验 `scripts/validate_anchor_prompt.py`（时间段连续、锚点不贴 0 秒和结尾、“不是首帧/尾帧”声明、--production 查每段焦段与 T 档、表演段、声音档案）。
- 同步：关键帧分镜白模（重写首节）、输入设计与预演、多模态素材、Seedance 2.5、提示词导演、Auditor 第 7 条、连续性、输出契约、SKILL.md。
- v1.5.0 备份：`~/.agents/skill-backups/seedance-directing-team-cn_v1.5.0_20261109.tar.gz`。

## v1.5 — 2026-11-04 · 接入外部参考库 cinematic-director（DirectorSKILL）

- 参考库装在 `~/.agents/skill-libs/cinematic-director/`（不在 skill 扫描目录，不会自动触发）；SKILL.md 专业模块后新增“外部参考库”路由表和禁用清单。
- 只取：导演风格参数（喂给 DP 关）、产品/logo 特写方法、片型总命题四行、片长换算镜头数方法。
- 禁用：F11 模糊字修法、片型手册的运镜/光线/节奏行、它的提示词模板与 Seedance 适配、它的“少问少产出”默认规则、连续性手册与 QC 格式。
- 审片与返修第 6 节新增三类症状：道具遮挡后消失/换样、速度不对、手部畸形（提炼自其 F19/F13/F10）。
- v1.4.0 备份：`~/.agents/skill-backups/seedance-directing-team-cn_v1.4.0_20261104.tar.gz`。

## v1.4 — 2026-11-03 · 正式项目必过关卡（用户反馈“摄影指导、表演指导经常没跑”）

- SKILL.md 新增“正式项目必过关卡”：有人物表演或说话的正式项目，写提示词前必须先出摄影设计（调用用户 DP Skill `commercial-dp-planning`）和人物表演档案/声音档案（表演指导 + `acting-system`）；不随档位跳过；交付时列出实际读过的文件。
- 专业模块改为“在 Claude Code 中直接读取 `~/.codex/skills/<模块>/` 执行”，删去“Claude Code 中不可用”的豁免。
- 导演层路由表的摄影行接入 `commercial-dp-planning`。
- `validate_prompt_text.py` 新增 `--production`：检查每个有戏人物的“⚠️<人物>表演（本组）”段、说话人的“<人物>声音”档案、每个机位的焦段与 T 档/光圈；不加此参数时输出标注 “format only”。
- 多镜头模板加入表演段、声音档案和机位器材字段。
- `--production` 也把每张上传的人物设定板（IDENTITY_ONLY …设定板）算作有戏人物；人物名允许别名（如“周琳夜间”对“周琳”）。


## 2026-11-03 · 器材写入提示词（用户偏好）

- camera-and-lens-system 第 9 节加用户偏好：器材名、实有焦段和 T 档写进提示词，可见结果保留。

## 2026-11-02 · 人物设定板模板

- 新增 references/seedance/character-sheet-template.md：用户定的 16:9 五格写实棚拍人物设定板提示词（逐字模板 + 两个槽位 + 不能站立人物的姿态变体 + Codex 出图要点 + 验收 8 条）。
- asset-production-system 和 SKILL.md 路由表加入链接。

## v1.3 — 2026-10-12

合并全局版 seedance-film-director-cn v2.3.0（2026-09-20，此前合并用的是项目内 8 月旧版）。

新增 7 个参考文件：
- `seedance/input-design-and-previs.md`：Input Design Gate、Layout / Shot State Plate、Reference Role（START_FRAME / END_FRAME / IDENTITY_ONLY / LAYOUT_ONLY / STATE_ONLY / LOOK_ONLY / CAMERA_PREVIS）。
- `seedance/reverse-video-analysis.md`：参考视频反推与差异诊断（证据层）。
- `seedance/shot-recipe-library.md`：video-shotcraft 镜头配方适配。
- `director/physical-action-design.md`：Physical Action Contract、动作相位母式、因果 Coverage。
- `director/in-frame-ecology.md`：镜内生态与群演调度（作为镜内执行导演的详细方法）。
- `director/blender-camera-previs.md`：Blender 摄影预演交接与验收。
- `shared/generation-experiments-and-selects.md`：FINAL SHOT / MATERIAL SEQUENCE、控制变量实验、候选评分、Selects Manifest。

规则变更（以 v2.3.0 为准）：
- **APPROVED**：只有“锁定这个版本 / 标记为 APPROVED / 后续沿用这一版”才锁定；“通过/可以了”只是候选接受。新增 `SELECT_APPROVED`。
- **运镜**：每镜一个主要摄影意图，2.5 可用协同复合运动；2.0 仍从严一镜一运镜。
- **版本默认**：未指定版本时简单任务按 2.5 并标注待确认，正式任务先确认。
- **表演**：微事件不再“每 1–2 秒”机械排程；新增表演任务主线、活人感与身体联动、微表情时间轴、说话者/听者双轨、台词时间预算（3–4 字/秒）。
- **镜内生态**：从“每个可见角色都有任务和错峰反应”改为按可辨认程度分配精度、反应有因、允许有意静止与有因同步（导演组、导演语法、K20、通过标准同步修正）。
- **返修**：“单变量”细化为“一个因果变量 + 必要依赖的修改包”。

合并进已有文件：摄影指导新增第 10 节（观看关系、运动触发表、DP 载荷）；Auditor 重写为 BLOCKER/WARNING/NOTE 三级、28 项五组；输出契约新增 L0–L3 与 13–17 节；连续性新增累积状态、物理/输入/可剪性维度、Selects；15-Block、提示词架构（声音与光影基线、压缩阶梯）、多模态（Reference Role）、长视频（环境事件时间线）、平台路由（事实记录）、Shot Card、生产模式、审片返修、模板库（TPL 18/19）同步更新。多镜头模板素材行改为 ROLE 格式。

SKILL.md 新增“专业模块”路由（lira-image-prompts / acting-system / cinedance-v4，仅在 Codex 中可用时调用）。新增 `scripts/check_skill.py`。

## v1.2 — 2026-10-12

场景与道具资产恢复生成画内文字（出图模型 image 2.5 文字能力已足够，O 类）。

- 新增 `references/seedance/in-world-text.md`：画内/画外文字分流、A/B/C 分级、TEXT SPEC 文字清单、生图写法、状态与连续性、进入 Seedance 的保持写法、逐字验收、权利边界。
- 改写“标牌文字一律前期合成/后期”的旧规则（safety-and-rights、seedance-20、seedance-25）：画内虚构文字直接生成，后期只负责字幕和兜底。
- 资产生产、世界观圣经（新增文字体系字段）、多模态控制维度、输出契约（资产设计含 TEXT SPEC，审片含文字核对）、连续性矩阵、Auditor 第 23 条、症状速查、生成检查门、多镜头模板同步更新。

## v1.1 — 2026-10-12

并入《电影摄影机与镜头系统 Skill v2》为摄影指导的器材选型参考 `references/director/camera-and-lens-system.md`。

- 默认组合改为“设计讨论起点”，不自动写入提示词。
- 新增“落到 AI 生图与 Seedance”：器材→可见结果翻译表；器材名仅作弱风格提示且标为待验证；帧率/快门改写为运动质感。
- 器材信息整体标为 O 类（valid_as_of 2026-10-12）；项目化示例（三国、武将）改为通用类型。
- 去掉与 optics-fov 重复的焦距原理；SKILL.md、摄影指导、光学与 FOV、输出契约、Auditor（第 22 条）、导演组加入链接。

## v1 — 2026-10-11

合并 seedance-film-director-cn V2 与 leos-six-department-directing-team-skill-v1。

- 三档工作模式：轻量（直接出提示词）/ 标准（Shot Card + Auditor）/ 导演组（六角色会诊 + 生成门）。
- 提示词格式统一为 Compact / Production 15-Block / 多镜头分镜三选一。
- Leos 模板改用 `@图片N` 标签，每镜新增“声音：”行，使用 Seedance 声音符号。
- 5000 字上限改为“平台上限与 5000 取较小值”。
- 审稿默认 Auditor + 有问题的角色意见；6×N 全覆盖改为“严格审稿”可选项，脚本新增 `--roles`。
- 合并去重：scene-geography + spatial-and-assets → spatial-and-geography；continuity-and-review + continuity-and-learning → continuity；troubleshooting + review-and-repair → review-and-repair；两份 output-contracts 合并；acting-system 并入 performance-direction。
- 修正：seedance-20 音乐符号全角 `（）` → 统一以 voice-system 为准；“WHAT HE HIDES” → “WHAT THEY HIDE（人物隐藏什么）”；校验脚本占比阈值与文档统一为 20% / 65%。
- 新增脚本：validate_15block.py、validate_patch.py。
- Auditor 增加版本/平台、标签和 7 项导演层检查；摄影指导增加“落到 Seedance”（2.0 一镜一运镜）。
- 删除 Leos 内部会议来源索引 M01–M13（无法核验），保留 K01–K26 知识卡。
