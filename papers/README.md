# Related Paper Package

> 这个目录用于保存 FAR-Hammer 相关论文 PDF 和阅读笔记。不要复制 `ICLR_1` 的 mechanistic interpretability 论文包；本项目需要 Lean/formal reasoning 专属资料包。

## 必读论文

| # | Paper | Venue/status | Link | Role |
|---|---|---|---|---|
| 01 | Premise Selection for a Lean Hammer | ICLR 2026 Oral | https://arxiv.org/abs/2506.07477 | Direct baseline: LeanHammer/LeanPremise |
| 02 | LeanSearch v2: Global Premise Retrieval for Lean 4 Theorem Proving | arXiv 2026 | https://arxiv.org/abs/2605.13137 | Most dangerous retrieval competitor |
| 03 | LeanDojo: Theorem Proving with Retrieval-Augmented Language Models | NeurIPS 2023 Datasets and Benchmarks Oral | https://arxiv.org/abs/2306.15626 | Infrastructure and ReProver baseline |
| 04 | Learning to Repair Lean Proofs from Compiler Feedback / APRIL | ICLR 2026 VerifAI / arXiv | https://arxiv.org/abs/2602.02990 | Proof repair boundary |
| 05 | APOLLO: Automated LLM and Lean Collaboration for Advanced Formal Reasoning | NeurIPS 2025 Poster | https://openreview.net/forum?id=fxDCgOruk0 | Compiler-guided proof repair boundary |
| 06 | OProver: A Unified Framework for Agentic Formal Theorem Proving | arXiv 2026 | https://arxiv.org/abs/2605.17283 | Agentic whole-proof prover boundary |
| 07 | Process-Verified Reinforcement Learning for Theorem Proving via Lean | ICLR 2026 Poster | https://openreview.net/forum?id=P00k4DFaXF | Lean feedback as training signal |
| 08 | LeanProgress: Guiding Search for Neural Theorem Proving via Proof Progress Prediction | TMLR 2025 | https://arxiv.org/abs/2502.17925 | Complementary search guidance |
| 09 | miniCTX: Neural Theorem Proving with Long Contexts | arXiv 2024 | https://arxiv.org/abs/2408.03350 | Local/unseen context benchmark |
| 10 | DeepSeek-Prover-V2 | arXiv 2025 | https://arxiv.org/abs/2504.21801 | Big prover baseline context, not direct target |

## 已下载 PDF

- `01_Premise_Selection_for_a_Lean_Hammer_Zhu_et_al_2025.pdf`
- `02_LeanSearch_v2_Global_Premise_Retrieval_2026.pdf`
- `03_LeanDojo_ReProver_Yang_et_al_2023.pdf`
- `04_APRIL_Learning_to_Repair_Lean_Proofs_2026.pdf`
- `05_APOLLO_Ospanov_et_al_2025.pdf`
- `06_OProver_Agentic_Formal_Theorem_Proving_2026.pdf`
- `07_Process_Verified_RL_Lean_ICLR2026.pdf`
- `08_LeanProgress_Proof_Progress_Prediction_2025.pdf`
- `09_miniCTX_Long_Contexts_2024.pdf`
- `10_DeepSeek_Prover_V2_2025.pdf`

## 读法

每篇论文读完后补一个同名 `.md` 笔记，至少包含：

1. 已有贡献。
2. 它会如何攻击 FAR-Hammer。
3. 我们必须正面对比的 baseline。
4. 我们的差异化一句话。
5. 可复用的 dataset/code/metric。
