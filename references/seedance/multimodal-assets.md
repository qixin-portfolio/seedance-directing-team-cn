# 多模态素材职责

## 唯一主控制源

先建立控制维度表。每个维度只能有一个**唯一主控制源**：

| 维度 | 常见主控制源 |
|---|---|
| 人物身份与服装 | PRODUCTION_APPROVED 人物资产 / Canonical Descriptor + 图片 |
| 片段内部关键构图 | 分镜图（`VISUAL_ANCHOR`，按时间窗口） |
| 首帧/尾帧状态（只限接帧、延长、精确复现） | 首帧或尾帧图片 |
| 动作与人物调度 | 参考视频或白模 |
| 摄影机路径与节奏 | 参考视频或文字镜头计划 |
| 场景空间 | 场景 Plate、视频或锁定 Scene Map，选一个主源 |
| 声音与音色 | 授权音频或固定 VOICE PROFILE |
| 时间与事件顺序 | 阶段、时间戳或分镜顺序 |
| 材质与视觉风格 | World Bible、风格图片或文字美术设定 |
| 画内文字（招牌、标签、屏幕） | 含该文字的场景/道具资产图或首帧图；提示词只写“保持不变” |

如果两份素材争夺同一维度，先指定胜出者；没有职责的素材删除。

## Reference Role

正式镜头先为每份视觉输入指定一个主 Role：`VISUAL_ANCHOR`（分镜图默认）、`START_FRAME`、`END_FRAME`、`IDENTITY_ONLY`、`LAYOUT_ONLY`、`STATE_ONLY`、`LOOK_ONLY` 或摄影预演视频的 `CAMERA_PREVIS`。详细边界和 Input Gate 见 [输入设计与预演](input-design-and-previs.md)。

- `CAMERA_PREVIS` 显式继承声明的动态构图与路径，见 [摄影预演](../director/blender-camera-previs.md)；普通图像参考中，`VISUAL_ANCHOR` 在声明的时间窗口继承构图（不是首尾帧）；只有 `START_FRAME` 继承开场构图；`END_FRAME` 定义明确终态。
- `LAYOUT_ONLY`、`STATE_ONLY` 和 `LOOK_ONLY` 默认都是 Reference Only，不得自动成为首帧。
- 每份素材同时写 `ROLE / ADOPT / IGNORE / FRAMING POLICY`。

## 素材职责写法

逐份说明**采用**什么，以及容易误带时**不采用**什么：

```text
@图片1 — ROLE: IDENTITY_ONLY；ADOPT：<人物A>的五官、发型和服装；IGNORE：背景和原始姿势；FRAMING POLICY：不继承构图。
@图片2 — ROLE: LAYOUT_ONLY；ADOPT：空间布局和运动方向；IGNORE：图中人物、材质和文字；FRAMING POLICY：REFERENCE ONLY, NOT A START FRAME。
@图片3 — ROLE: LOOK_ONLY；ADOPT：场景材质、光线和调色；IGNORE：人物和原始 framing。
@视频1只用于<人物A>的动作节奏和摄影机路径，不采用视频中的人物身份、服装、场景、文字、Logo和声音。
@音频1用于<人物A>的授权音色和指定台词，不控制画面节奏。
```

不要写“@图片1到@图片4分别定义四个人”。应逐一命名并绑定。

## Canonical Descriptor 与标签

项目资产已锁定时，`@char / @loc / @prop` 是项目管理标识，真正的身份稳定同时依赖 Canonical Descriptor 和参考图片。不要把无语义 Asset ID 当成模型能自动理解的完整身份。

在 Production 15-Block 中，可把 `@图片N / @视频N / @音频N` 集中放在 ACTIVE REFERENCES，后续区块使用人物、场景、道具语义名，减少重复标签和版本混乱。这是本项目生产约定，不是官方语法要求。

## 多视角与多人

- 同一人物的不同视角用独立图片，并声明“共同定义同一个人物，成片始终只有一个”。
- 参考人物较多时，为每个人设置不同脸、发型、服装、体型、空间锚点、动作和声音。
- 多人交互先写谁可以接触谁、谁不得越过轴线、谁持有什么道具。
- 群体镜头不要要求所有远景面孔达到近景肖像细节；前中景身份稳定优先。

## 按镜头选择素材

多素材不是全部同时出现。只加载当前镜头实际需要的角色、道具、场景、动作和声音参考。场景结束时写人物位置、道具归属和下一镜需继承的状态。

## 标签纪律

- 完整保留 `@图片N / @视频N / @音频N` 的编号和拼写。
- 不把标签翻译、重编号或替换成无语义 Asset ID。
- `@图片1` 后不要直接接动词或方位词；写“@图片1中的人物A”或先定义 `<人物A>`。
