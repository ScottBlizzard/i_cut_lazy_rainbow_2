# 实验修正与异常分流计划

> 用途：当实验结果不好看或互相矛盾时，先在这里分流，再决定修 bug、扩大 insight、还是写 boundary。  
> 最后更新：2026-06-17

---

## 1. 总原则

不好看的结果不能直接丢，也不能直接包装成 insight。必须先判断：

| 类别 | 判定标准 | 处理 |
|---|---|---|
| Bug/artifact | 修 environment/parser/budget/backend 后消失 | 修正并重跑 |
| True insight | 多 seed/subset/backend 稳定，且理论能解释 | 补机制实验和理论 |
| Boundary condition | 特定 backend/dataset/budget 下稳定存在 | clean audit 后写成边界 |

---

## 2. 预期异常与修正路线

### A1. FAR 不提升 full Mathlib success

先检查：

- first-failure subset 是否提升。
- timeout subset 是否提升。
- local/miniCTX subset 是否提升。
- 同 solved rate 下 time/prover calls 是否降低。

如果只有 hard subset 提升：

- 不是降级。主线改成 failure traces matter most where one-shot retrieval fails。

### A2. Full failure message 不如 coarse failure type

可能 insight：

- Lean error text 噪音大。
- coarse taxonomy 是更稳定的 sufficient statistic。

补实验：

- message-only vs type-only vs structured trace。
- parser accuracy audit。

### A3. Top-k expansion 很强

先检查：

- 是否用了更多总 premise budget。
- 是否用了更多 wall-clock。
- 是否失败后扩到了 proof core。

补实验：

- fixed total premise budget。
- fixed total prover calls。
- proof-core precision 和 redundancy。

### A4. Reconstruction-aware rerank 降低 ATP success

可能 boundary：

- recon-friendly premises 与 ATP-friendly premises 有 trade-off。

补实验：

- ATP success、Lean reconstruction success、verified success 三列表。
- recon-failure subset 单独汇报。

### A5. Local boost 无效

检查：

- local premise pool 是否正确。
- local lemma 是否 accessible。
- benchmark 是否真的依赖 local lemmas。

如果 synthetic local suite 有效、真实 miniCTX 无效：

- 写成 local boost 需要 failure-triggered + context-quality 条件。

---

## 3. 结果可信度 checklist

每个主结果必须确认：

1. Lean/mathlib commit 记录。
2. Same theorem split across methods。
3. Same wall-clock budget。
4. Same prover call budget。
5. Same candidate premise pool，除非明确是 retriever comparison。
6. No test proof leakage。
7. JSON source 可回溯。
8. Table/figure 由脚本生成或有审计记录。

