# 场景与镜头卡（Shot Card）

Prompt 之前先把镜头设计成可以执行的导演卡。复杂项目的镜头编号在 Shot Card、Prompt 文件、测试版本和剪辑备注中保持一致。

## MATERIAL

- Scene / Shot 编号；
- INT / EXT、地点资产、时间；
- 人物资产与状态版本；
- 道具 / 车辆；
- 动作概要；
- 台词原文；
- 时长；
- 复杂度。

## DIRECTION

- **GOAL**：观众在镜头结束时应理解或感受到什么。
- **TASK**：人物为了获得目标正在做什么，用一个行为动词：观察、逼问、掩饰、羞辱、逃避、说服……
- **DRAMATURGY**：从镜头开始到结束，关系、信息或状态发生了什么变化。
- Blocking：人物相对摄影机、场景锚点和其他人物的位置。
- Acting：脸和身体做什么。
- **WHAT THEY HIDE（人物隐藏什么）**：人物想隐藏、压住或不愿被别人看见的东西。
- Physical Action：复杂动作写力量来源、接触点、传力路径、主要阻力、承受对象反应和最终稳定状态，见 [物理动作](../director/physical-action-design.md)。
- 镜内生态：有次要人物、环境活动或群体反应需要设计时，把 [镜内生态](../director/in-frame-ecology.md) 的相关行动补入，检查它与主角行为、摄影路径及连续性出口的关系。

## CAMERA

景别、机位、焦距 / FOV、角度、一个主要摄影意图、前中后景。复杂全景因果不可读时，按 [物理动作与因果 Coverage](../director/physical-action-design.md) 选择最少的 Geography、Force Source、Load Path、Failure Point 或 Result / Reaction 镜头。

摄影决策不足或用户要求增强镜头时，按 [摄影指导](../director/cinematography-direction.md) 第 10 节补 DP 载荷；需要 Blender 执行时再输出 [摄影预演交接](../director/blender-camera-previs.md)。已确认轨迹沿用，只修改用户要求的部分。

## EDIT

- **EDIT**：切法、节奏、进入镜头的 hook、离开镜头的 hook；
- 上一镜结束状态；
- 下一镜需要接住的动作、视线、声音或空间方向；
- 因果 Coverage 的切镜顺序和每镜可观察终态（有时）。

## INPUT

- INPUT GATE：READY / NOT READY / NOT REQUIRED（见 [输入设计与预演](../seedance/input-design-and-previs.md)）；
- 每份素材的 Reference Role。

没有 GOAL、TASK 或 DRAMATURGY 的镜头，优先补导演设计，不急着加 Prompt 形容词。
