# Prompt Workbench（返修工作台）

Workbench 的目标是保存已经工作的东西。每个正式镜头把最终 Prompt 当作一个可版本化文件，而不是每次重新生成一整篇文字。

## PATCH 原则

收到失败镜头后：

1. 先用审片规则定位问题来源；
2. 找到最可能负责该问题的 Prompt 区块；
3. **只修改失败区块**；
4. **保持其余区块逐字不变**；
5. 记录测试编号、变更句、原因和 verdict；
6. 保存新旧两版文件后运行 `python3 scripts/validate_patch.py <旧版> <新版> --patch "<区块,…>"`，确认未声明的区块逐字未动。多镜头分镜的区块名为 `前置`、`镜头N`、`环境活动`、`风格`。

示例：

```text
03-03_T05
失败：快递员车头方向错误
PATCH：LOCATION MAP + FIRST FRAME AND SPATIAL BLOCKING
保持：ACTIVE REFERENCES / OPTICS / CAMERA / LIGHTING / AUDIO / ACTING / STYLE 全部不变
```

## Prompt 版本日志

每镜维护 `Prompt 版本日志`（正式项目同时写入 [三本账](continuity.md#5-三本账)）：

```text
03-03_T01 — 初版 — FAIL：身份稳定，车头错误
03-03_T02 — PATCH LOCATION MAP — FAIL：方向正确，动作过快
03-03_T03 — PATCH ACTION TIMING — PASS
03-03_APPROVED — 正式基准
```

## 什么时候停止改句子

同一结构性失败连续重复时，不继续堆形容词。依次考虑：

- 换编辑模式；
- 重建人物 / 场景 / 道具资产；
- 降低同镜头动作密度；
- 拆镜；
- 改机位；
- **升级镜头设计**，让复杂动作从首帧就处在关键状态。

如果只是采样随机性，保留 Prompt 有限重抽；如果同一错误持续出现，改结构而不是改文风。
