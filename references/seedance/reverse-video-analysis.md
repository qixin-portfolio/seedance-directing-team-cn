# 参考视频反推分析

这是 Seedance 导演 Skill 的只读证据层：把参考视频或生成失败片中的可观察事实，转译成可执行、可审计的镜头约束。它不接管用户意图、资产职责、版本/平台路由、复杂度路由、连续性、输出契约或最终 Prompt 组装。

## 第一性原理与优先级

先解决“观众在这个镜头里应理解或感受到什么”，再解决“模型需要哪些约束才能稳定呈现”。优先级固定为：

1. 安全与权利边界；
2. 用户明确目标与参考片实际意图；
3. Seedance 版本、平台能力和当前生产阶段；
4. 现有权威模块与输出契约：`Scene Card`、`Physical Action Contract`、`Voice System`、`Continuity`、`Prompt Auditor`、`Workbench`；
5. 本文件提供的观察、差异归因和候选约束。

发生冲突时，低层资料库让位于高层规则。本模块只提供证据和建议，不改变上面的优先级。

## 使用边界

- 分析用户实际提供且当前环境可读取的本地或远程授权素材、帧序列、分镜、描述或生成结果；无法读取时明确标注“未核验”，不假装看过。
- 先记录观察事实，再写推断。不可观察的细节只能作为带不确定性的假设，不能伪装成参考片事实。
- “产品/卖点/CTA”只在商业或产品导向参考中使用；剧情、纪录、企业形象、氛围和纯动作参考，改用事件目标、冲突、信息变化、情绪变化或镜头功能。
- “静音、环境声、延迟对白、空镜和氛围段”只有在偏离参考片意图或用户目标时才算失败；不能把电商规则套到非电商镜头。
- 不调用 GitHub、Lark/飞书、社区上传、遥测或任何外部写入脚本；不把私有路径、未授权原始媒体或可识别信息写入可复用规则。

## 证据采集顺序

### 1. 开场理解目标

检查 0.0-3.0 秒观众实际获得的第一轮信息：主体、事件、冲突、产品卖点、情绪或空间关系，按当前参考片意图选择其中适用项。记录第一句对白、第一组动作声、环境声或有意静默的起点；不预设必须说话或必须出现产品。

### 2. 镜头角色与主体层级

锁定谁拍谁、机位是第一人称/同事手持/固定/自拍/过肩、景别、运动路径、可见主体数量、遮挡和前中后景层级。主体显著性必须服从真实拍摄关系，不能用假 POV、额外人物或英雄式产品构图改写参考片的视角。

### 3. 事件链与镜头功能

按时间顺序写成可拍摄的因果链：起始状态或目标 → 触发 → 操作/关系变化 → 反馈或信息变化 → 可观察终态。每个 beat 标注其功能：建立空间、推进事件、揭示信息、证明卖点、制造情绪、建立信任、结果或 CTA；不要因“氛围”二字删除参考片中承担叙事或情绪功能的停留。

### 4. 工具、材料与物理

复杂动作直接复用 [Physical Action Contract](../director/physical-action-design.md)，不得另起一套简化物理标准。至少核对：力量来源与方向、质量/速度/材料、接触点、传力路径、主要阻力、承受对象反作用、可见次生后果和最终稳定状态。复杂副任务会抢主体或引发错误几何时，优先简化动作或拆最少的因果 Coverage。

### 5. 声音与动作同步

按参考片实际声音政策检查：对白说话人和口型、环境声床、动作音、音乐、字幕和有意静默。只有存在可核验的音画漂移时，才修复静音开场、延迟对白、噪声门死寂、动作无声或声音先于接触；声音约束最终交给 [Voice System](voice-system.md) 和 Prompt Auditor。

## 差异诊断

先做 Reference vs Generated 的时间对齐，再只归因于有证据的漂移：

| 观察到的漂移 | 优先检查的 Prompt 原因 | 修复方向 |
|---|---|---|
| 开场让观众晚于参考片理解主体、事件或情绪 | 没有定义该镜头的开场理解目标 | 重写适用的第一拍、信息出现顺序或动作起点；不强加产品钩子 |
| 主体变 prop、手持或假 POV | 主体显著性覆盖了镜头角色 | 先锁拍摄关系和主体数量，再写自然可见的主体功能 |
| 工具、材料、阶段或状态跳变 | 动作链只写结果，缺少状态与连续性锁 | 复用 Physical Action Contract，补阶段顺序、接触几何和材料状态 |
| 局部效果无来源或承受对象不反应 | 缺少完整受力链或稳定终态 | 补力量来源 → 接触 → 传力 → 阻力/反作用 → 回弹/衰减/稳定 |
| 画面比参考片更像广告或过度干净 | 没有捕捉参考片的拍摄纹理和世界细节 | 补原生手机/纪录/商业摄影等真实证据，不默认反广告 |
| 音画信息或节奏不一致 | 声音政策、台词时间或动作同步没有锁定 | 复用 Voice System，按参考片决定对白、环境声、动作音、音乐或静默 |
| 情绪、关系或空间变化被压平 | 把镜头当成产品展示或动作清单 | 回到 Shot Card 的 GOAL、TASK、DRAMATURGY 和 EDIT hook |

## 吸收分级

学习卡是内部迭代记录，不是每次对用户的强制输出。只有用户要求优化 Skill、要求复盘沉淀，或同类失败已重复出现时才生成：

```yaml
case_id: short-name
evidence: reference/generated/frame/audio evidence
drift: observable difference
likely_prompt_cause: missing or conflicting constraint
prompt_fix: smallest useful change
change_level: prompt-only | candidate skill rule | reference-template update | eval case | tooling
reusable_rule: portable rule, only when supported by repeated evidence
risk_of_overfit: low | medium | high
privacy_note: omit unauthorized/private paths, raw media, or unnecessary identifiable details
```

只有同时满足“可复用、可观察、可执行、精简、非私有、不冲突”才考虑进入本地 reference；否则保留为本镜头 Prompt 修复或 eval case。候选规则先交给 Prompt Auditor，再由总导演模块组装。

## 输出与返修

- 用户只要直接提示词：遵守 [输出契约](../shared/output-contracts.md)，交付完整可粘贴 Prompt；本模块的诊断只做必要摘要。
- 用户要求失败返修：内部采用 Workbench 的“只 patch 失败区块、其余逐字不变”；对外需要可直接生成时，同时给出组装后的完整 Prompt 或明确用户应替换的区块。
- 只有高风险、多人、复杂物理、对白、高连续性或多轮返修才升级 Production 15-Block；简单镜头继续使用 Compact Prompt。
- 参考反推不改变首帧/首尾帧、Input Gate、Scene Geography、VOICE PROFILE、APPROVED 锁定或用户已确认的素材职责。

## 交付格式

按任务选择，不强制全部出现：

```text
【参考证据】
与当前镜头目标有关的事实、未核验项和假设。

【差异诊断】
Reference vs Generated 的时间对齐差异，以及最可能的 Prompt 原因。

【新版 Seedance Prompt】
遵守当前输出契约；需要返修时只改变失败区块，最终按需提供完整 Prompt。

【学习卡】
仅在用户要求沉淀或满足重复失败门槛时输出。
```
