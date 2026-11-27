# Seedance 导演组 · 中文影视一体化

合并自两个 Skill：

- `seedance-film-director-cn` v2.3.0（Seedance 执行层：版本/平台路由、输入设计与 Reference Role、素材职责、编辑延长、关键帧白模、15-Block、Auditor、Workbench、实验与 Selects、APPROVED；以及物理动作、镜内生态、摄影指导、Blender 预演、参考视频反推、镜头配方）
- `leos-six-department-directing-team-skill-v1`（导演层：六角色导演组、表演谱、群戏、摄影设计、三本账、知识卡）。原仓库 https://github.com/MasterLeos/leos-six-department-directing-team-skill-v1 未附许可证，本合并版仅供个人项目使用，不对外分发。

- 《电影摄影机与镜头系统 Skill v2》（器材选型：摄影机底色、镜头性格、焦距/光圈、画幅兼容、组合预设），并入为 `references/director/camera-and-lens-system.md`。

原 Skill 均保持原样未改动。

## 结构

```text
SKILL.md                  入口：档位选择 + 两层路由 + 原则
references/seedance/      执行层（来自 Seedance V2）
references/director/      导演层（来自 Leos，已改为输出 Seedance 语法）+ 摄影机与镜头选型
references/shared/        两边合并去重：空间地理、连续性、审片返修、Auditor、Workbench、输出契约、知识
assets/                   多镜头分镜模板（@图片N + 每镜声音行）、三本账 CSV、项目风格档案
scripts/                  校验脚本（Python 3.9+，仅标准库）
```

## 校验

```bash
python3 scripts/validate_prompt_text.py prompt.txt --max-chars 5000   # 多镜头分镜
python3 scripts/validate_15block.py prompt.txt                         # 15-Block 单镜
python3 scripts/validate_patch.py v001.txt v002.txt --patch "CAMERA"   # Workbench 只改声明区块
python3 scripts/validate_review_coverage.py review.md --shots 4        # 严格审稿 6×N 覆盖
python3 scripts/check_skill.py                                         # Skill 自身一致性
```
