# Production 15-Block 正式镜头结构

用于高风险、多人、连续动作、对白、复杂空间或需要多轮返修的正式生产镜头。简单镜头继续用 Compact Prompt，不强制 15 Block。

## Production 15-Block

这是 15 个核心区块；对白、物理、连续性、实验和返修字段属于按风险追加的可选扩展，不把所有镜头都强制膨胀成同样长度。

1. **SCENE CONTEXT** — 戏剧背景、镜头目的、人物、时长。
2. **ACTIVE REFERENCES** — 本镜实际加载的素材、唯一职责和 Reference Role；生产约定可让 `@标签` 只在这里出现一次，后文用人物/场景语义名指代。
3. **LOCATION MAP** — Scene Geography Lock、锚点、轴线、方向。
4. **FIRST FRAME AND SPATIAL BLOCKING** — 第一帧已有人物和道具就位；动作将起或已经开始，不用空首帧浪费模型建立空间。
5. **FORMAT MODE** — 先声明 `DELIVERY INTENT: FINAL SHOT / MATERIAL SEQUENCE`，再写时长、画幅、单镜/多镜、实时/变速、字幕/BGM政策；平台参数由界面或 API 设置。
6. **OPTICS** — 景别、焦距 / FOV、主体占屏、景深、透视结果。
7. **CAMERA** — 机位、主运动、起点、路径、终点、是否切镜；复杂因果若使用 Insert Coverage，保持受力方向和时间进程连续。
8. **ACTION TIMING** — 阶段或时间预算；按动作相位写每段主要变化与可见终态，不机械塞入全部相位。
9. **PHYSICS** — 力量来源、质量与材料、接触点、传力路径、主要阻力、承受对象反作用、可见次生后果和最终稳定状态；详见 [物理动作与因果 Coverage](../director/physical-action-design.md)。
10. **LIGHTING** — 真实光源、方向、软硬、色温、阴影和曝光关系。
11. **AUDIO** — 说话人、VOICE PROFILE、台词、环境声、动作音效、音乐政策。
12. **CHARACTER ACTING** — TASK、WHAT THEY HIDE（人物隐藏什么）、行为、eye-life、手和呼吸。
13. **STYLE** — 世界观、年代、材质、色彩和影像质感。
14. **QUALITY** — 只保留真正保护可读性、材质与稳定性的质量要求。
15. **POSITIVE CONSTRAINTS** — 用“正确结果”写物理与动作；对反复泄漏、年代、人数、道具数量、声音归属等使用 Named Lock。

## 区块标题写法

每个区块标题独占一行开头，使用上面的英文名，后接中文冒号或换行，例如 `LOCATION MAP：` 或 `【LOCATION MAP】`。15 块按顺序全部保留；某块确实不适用时写“无”或“同上一镜”，不要删除区块——这样 Auditor 能逐块检查，Workbench 能逐块 PATCH。

保存后运行 `python3 scripts/validate_15block.py <prompt.txt>`；返修后运行 `python3 scripts/validate_patch.py <旧版> <新版> --patch "LOCATION MAP,ACTION TIMING"`。

## 约束写法

背景行动需要控制时按 [镜内生态](../director/in-frame-ecology.md) 的组装规则进入现有位置、时序、表演与声音区块；只带入本镜相关内容，不另加整张群演表。

动作优先正向描述，例如“腹部先接触地面并俯卧停止”，而不是让模型反复思考错误姿态。对于反复出现的错误对象，可以明确写 Named Lock，例如：`OBJECT COUNT LOCK：全程只有一把伞。`

“没有 Negative Block”不是硬规则；目标是减少无效否定，同时保留真正必要的禁止项。

## 摄影预演的接入

有 [摄影指导](../director/cinematography-direction.md) 或 [Blender 预演](../director/blender-camera-previs.md) 时不增加第16块：职责放 ACTIVE REFERENCES；起始构图放 FIRST FRAME；取景与焦点放 OPTICS；已设计的路径和朝向放 CAMERA；触发与停止放 ACTION TIMING；世界光源放 LIGHTING。精确坐标/关键帧表留在 Blender 交接，不作为生成模型的接口参数。
