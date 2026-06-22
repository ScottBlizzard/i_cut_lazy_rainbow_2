# Table/Figure Data Alignment Audit

> 日期：2026-06-17  
> 用途：记录论文表格、图、JSON 输出之间的对应关系，防止手工抄数错误。

## Canonical Sources

| Paper item | Source JSON/script | Status |
|---|---|---|
| Synthetic smoke table | `outputs/phase1_synthetic_smoke.json`, `src/analyze_phase1.py` | local-only, not paper evidence |
| A40 5k synthetic smoke table | `outputs/phase1_synthetic_smoke_5k_a40.json`, `src/analyze_phase1.py` | server pipeline sanity, not paper evidence |
| A40 synthetic Lean wrapper sanity | `outputs/phase1_lean_synth_10_a40.json`, `src/analyze_phase1.py` | real Lean invocation sanity, not Mathlib evidence |
| A40 environment table | `outputs/log_phase1_env_a40_with_lean.txt`, `src/check_env.py` | infrastructure record |
| LeanDojo-v2 probe trace | `outputs/lean_dojo_v2_probe_summary.json`, `outputs/lean_dojo_v2_probe_goals.jsonl` | trace/generator sanity, not paper evidence |
| Current mathlib4 trace | `outputs/mathlib4_local_trace_v2_current_summary.json`, `outputs/log_mathlib4_local_trace_v2_current.txt` | running on A40 |
| Main fixed-budget table | pending real Lean run | pending |
| First-failure recovery table | pending real Lean run | pending |
| Premise budget curve | pending | pending |
| Time budget curve | pending | pending |
| Failure ablation table | pending | pending |
| Failure taxonomy gain | pending | pending |
| Local/miniCTX table | pending | pending |
| Reconstruction table | pending | pending |
| Proof-core attribution | pending | pending |

## 2026-06-18 Additions

| Paper item | Source JSON/script | Status |
|---|---|---|
| Mathlib trace-core fixed-budget table | `outputs/phase1_mathlib_trace_core_500_a40.json`, `src/analyze_phase1.py` | watcher pending after trace |
| Mathlib trace-core goals | `outputs/phase1_mathlib_v2_goals_500.jsonl`, `src/make_phase1_mathlib_goals_v2.py` | watcher pending after trace |
| Trace-core oracle backend | `src/trace_core_attempt.py` | code ready; evaluates proof-core recovery, not proof reconstruction |

## 2026-06-20 Canonical Feature-Aware Outputs

| Paper item | Source JSON/script | Status |
|---|---|---|
| Corrected 500-goal feature-aware trace-core table | `outputs/phase1_mathlib_trace_core_500_feature_ablation_a40.json`, `outputs/phase1_mathlib_trace_core_500_feature_ablation_a40.md` | current main Phase 1 trace-core evidence |
| Feature-augmented 500-goal set | `outputs/phase1_mathlib_v2_goals_500_features.jsonl`, `src/augment_phase1_features.py` | current canonical 500-goal feature file |
| Feature extraction implementation | `src/feature_extraction.py` | current method code |
| Static visible-feature baseline | `visible_feature_rerank` in `src/far_controller.py` | included in current table |
| Trace-core failure-label correction | `src/trace_core_attempt.py` | current backend; old all-timeout label is artifact |

Numbers that may be cited from the current 500-goal trace-core table:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `one_shot` | 58.0% | 0.0% | 28.9 |
| `topk_equal_budget` | 80.0% | 0.0% | 43.5 |
| `visible_feature_rerank` | 88.4% | 0.0% | 43.5 |
| `topk_expansion` | 91.6% | 80.0% | 46.2 |
| `rule_far_failure_type_only` | 91.6% | 80.0% | 46.2 |
| `rule_far_no_core_tags` | 97.0% | 92.9% | 44.4 |
| `rule_far_full` | 98.8% | 97.1% | 42.7 |

2k scale-up canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| Corrected 2k feature-aware trace-core table | `outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.json`, `outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.md` | current scale-up evidence |
| Feature-augmented 2k goal set | `outputs/phase1_mathlib_v2_goals_2000_features.jsonl`, `src/make_phase1_mathlib_goals_v2.py` | current canonical 2k feature file |

Numbers that may be cited from the 2k trace-core table:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `one_shot` | 58.0% | 0.0% | 28.4 |
| `topk_equal_budget` | 75.7% | 0.0% | 42.9 |
| `visible_feature_rerank` | 86.5% | 0.0% | 42.9 |
| `topk_expansion` | 91.5% | 79.9% | 46.9 |
| `rule_far_failure_type_only` | 91.5% | 79.9% | 46.9 |
| `rule_far_no_core_tags` | 95.7% | 89.7% | 45.1 |

Timeout stress canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| 2k timeout stress table | `outputs/phase2_timeout_stress_2000_a40.json`, `outputs/phase2_timeout_stress_2000_a40.md` | current timeout mechanism evidence |
| Timeout stress launcher | `src/launch_phase2_timeout_stress_a40.sh` | current implementation |
| Timeout-first trace-core prover | `src/provers/trace_core.py` | current stress backend |

Numbers that may be cited from timeout stress:

| Method | Success | FFR | Avg premises | Timeout rate |
|---|---:|---:|---:|---:|
| `one_shot` | 57.0% | 0.0% | 28.4 | 4.0% |
| `topk_equal_budget` | 43.8% | 0.0% | 42.9 | 56.2% |
| `visible_feature_rerank` | 43.8% | 0.0% | 42.9 | 56.2% |
| `topk_expansion` | 59.7% | 6.2% | 50.4 | 46.1% |
| `rule_far_no_core_tags` | 59.7% | 6.2% | 42.8 | 46.1% |
| `rule_far_no_core_timeout_shrink` | 69.3% | 28.6% | 42.7 | 23.5% |
| `rule_far_full` | 100.0% | 100.0% | 40.1 | 22.5% |
| `rule_far_full` | 98.3% | 96.0% | 42.9 |

Reconstruction bridge canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| 100-goal real Lean replay bridge | `outputs/phase1_reconstruction_bridge_replay_100.json`, `outputs/phase1_reconstruction_bridge_report_100.md` | current Phase 1 bridge evidence |
| Bridge goal sample manifest | `outputs/phase1_reconstruction_bridge_manifest_100.json` | records disagreement-heavy sampling |
| Bridge goal set | `outputs/phase1_reconstruction_bridge_goals_100.jsonl` | replay/evaluation input |
| Bridge scripts | `src/select_reconstruction_bridge_goals.py`, `src/mathlib_replay_tactics.py`, `src/analyze_reconstruction_bridge.py` | current implementation |

Numbers that may be cited from the reconstruction bridge:

| Method | Trace-core success | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|
| `one_shot` | 13.0% | 10.0% | 0.0% | 31.1 |
| `topk_equal_budget` | 22.0% | 16.0% | 0.0% | 52.9 |
| `visible_feature_rerank` | 38.0% | 33.0% | 0.0% | 52.9 |
| `topk_expansion` | 54.0% | 43.0% | 37.9% | 81.0 |
| `rule_far_failure_type_only` | 54.0% | 43.0% | 37.9% | 81.0 |
| `rule_far_no_core_tags` | 85.0% | 72.0% | 71.3% | 75.7 |
| `rule_far_full` | 92.0% | 79.0% | 79.3% | 67.6 |

Bridge caveat for captions:

- This is a disagreement-heavy diagnostic bridge, not a random verified benchmark table.
- Bridge verified success means trace-core recovery plus successful replay of the original traced tactic script in real Lean.

Feature-group ablation canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| 2k feature-group ablation | `outputs/phase2_feature_group_ablation_2000_a40.json`, `outputs/phase2_feature_group_ablation_2000_a40.md` | current Phase 2 feature evidence |
| In-process trace-core evaluator | `src/eval_phase1_trace_core.py`, `src/provers/trace_core.py` | current fast evaluator |
| Feature-group policies | `src/far_controller.py`, `src/feature_extraction.py` | current method/ablation implementation |

Numbers that may be cited from feature-group ablation:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `topk_expansion` | 91.5% | 79.9% | 46.9 |
| `visible_feature_name_rerank` | 85.3% | 0.0% | 42.9 |
| `visible_feature_statement_rerank` | 77.6% | 0.0% | 42.9 |
| `visible_feature_decl_rerank` | 78.3% | 0.0% | 42.9 |
| `visible_feature_rerank` | 86.5% | 0.0% | 42.9 |
| `rule_far_failure_type_only` | 91.5% | 79.9% | 46.9 |
| `rule_far_no_core_decl_features` | 92.6% | 82.4% | 46.2 |
| `rule_far_no_core_statement_features` | 92.8% | 82.9% | 46.4 |
| `rule_far_no_core_name_features` | 95.0% | 88.1% | 45.4 |
| `rule_far_no_core_name_statement_features` | 95.2% | 88.6% | 45.4 |
| `rule_far_no_core_tags` | 95.7% | 89.7% | 45.1 |

Global imported-core canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| 2k imported-core global retrieval stress | `outputs/phase3_global_retrieval_2000_a40.json`, `outputs/phase3_global_retrieval_2000_a40.md` | current Phase 3 external-validity stress |
| Imported-core goal set | `outputs/phase3_mathlib_global_imported_core_goals_2000.jsonl` | generated from LeanDojo-v2 traced Mathlib |
| Imported-core generator | `src/make_phase3_mathlib_global_goals.py` | current data construction |
| BM25/LeanSearch-style policies | `src/feature_extraction.py`, `src/far_controller.py` | current baseline implementation |
| Phase 3 launcher | `src/launch_phase3_global_retrieval_a40.sh` | current canonical run script |

Dataset facts that may be cited:

| Quantity | Value |
|---|---:|
| Goals | 2000 |
| Avg imported proof-core premises | 4.26 |
| Avg imported candidates | 188.6 |
| Avg same-file candidates | 50.9 |
| Avg total candidates | 239.5 |

Numbers that may be cited from global imported-core stress:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `one_shot` | 1.1% | 0.0% | 32.0 |
| `topk_equal_budget` | 1.6% | 0.0% | 56.0 |
| `visible_feature_rerank` | 2.4% | 0.0% | 56.0 |
| `same_file_prior_rerank` | 2.1% | 0.0% | 56.0 |
| `bm25_rerank` | 7.0% | 0.0% | 56.0 |
| `leansearch_iterative` | 11.9% | 8.3% | 91.9 |
| `bm25_expansion` | 11.9% | 8.3% | 92.2 |
| `rule_far_bm25` | 12.2% | 8.7% | 92.2 |
| `rule_far_no_core_tags` | 4.7% | 3.6% | 94.9 |
| `rule_far_full` | 55.7% | 55.2% | 86.6 |

Caption warning:

- Present this as an imported-core stress/diagnostic table.
- Do not present `rule_far_no_core_tags` as competitive in this setting.
- `rule_far_full` is an oracle upper bound, not a deployable method.
- The paper-safe conclusion is that imported-core retrieval requires a learned/global retriever before this setting can become a main positive benchmark.

Learned global retriever canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| 1500/500 learned imported-core heldout eval | `outputs/phase3_learned_retriever_eval_500_a40.json`, `outputs/phase3_learned_retriever_eval_500_a40.md` | current Phase 3B learned evidence |
| Learned scored heldout goals | `outputs/phase3_learned_eval_goals_500.jsonl` | heldout eval input |
| Learned retriever model summary | `outputs/phase3_learned_retriever_model_1500_500.json` | current model artifact |
| Learned retriever training script | `src/train_phase3_learned_retriever.py` | current implementation |
| Learned policies | `learned_rerank`, `learned_expansion`, `rule_far_learned` in `src/far_controller.py` | current policy implementation |
| Learned launcher | `src/launch_phase3_learned_retriever_a40.sh` | current canonical run script |

Retriever recall numbers that may be cited:

| Ranker | All-core@32 | All-core@56 | All-core@96 | Mean core recall@96 |
|---|---:|---:|---:|---:|
| `base_score` | 1.4% | 1.6% | 2.6% | 26.7% |
| `learned_score` | 50.4% | 64.2% | 84.0% | 96.3% |

Heldout learned numbers that may be cited:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `bm25_expansion` | 12.8% | 8.4% | 91.5 |
| `leansearch_iterative` | 12.2% | 7.8% | 91.4 |
| `rule_far_bm25` | 13.0% | 8.8% | 91.5 |
| `learned_rerank` | 64.2% | 0.0% | 56.0 |
| `learned_expansion` | 84.0% | 67.7% | 57.7 |
| `rule_far_learned` | 84.4% | 68.5% | 57.4 |
| `rule_far_full` | 55.6% | 55.0% | 86.6 |

Caption warning:

- This is a heldout 500-goal result, not the full 2k table.
- The learned retriever is trained on traced proof-core labels from the other 1500 imported-core goals.
- The current learned controller gain over learned expansion is small; do not present `rule_far_learned` as a large controller improvement yet.
- The safe conclusion is that learned global retrieval restores the imported-core setting and creates a stronger baseline for the next failure-aware controller.

Learned controller ablation canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| Heldout learned controller ablation | `outputs/phase3_learned_controller_ablation_500_a40.json`, `outputs/phase3_learned_controller_ablation_500_a40.md` | current Phase 3C controller evidence |
| Controller launcher | `src/launch_phase3_learned_controller_a40.sh` | current canonical run script |
| Learned+base fallback policy | `learned_base_fallback` in `src/far_controller.py` | current strong baseline |
| Failure-specific learned policy | `rule_far_learned_failure_specific` in `src/far_controller.py` | current hand-written controller |

Numbers that may be cited from controller ablation:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `learned_rerank` | 64.2% | 0.0% | 56.0 |
| `learned_expansion` | 84.0% | 67.7% | 57.7 |
| `rule_far_learned` | 84.4% | 68.5% | 57.4 |
| `learned_base_fallback` | 87.0% | 73.8% | 57.6 |
| `rule_far_learned_failure_specific` | 87.0% | 73.8% | 57.0 |
| `rule_far_full` | 55.6% | 55.0% | 86.6 |

Caption warning:

- `learned_base_fallback` is the current strong non-FAR baseline.
- `rule_far_learned_failure_specific` matches fallback but does not beat it in success rate.
- This table should motivate learned second-stage failure control, not claim that the hand-written controller is already complete.

Learned second-stage controller canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| Heldout second-stage controller eval | `outputs/phase3_second_stage_controller_eval_500_a40.json`, `outputs/phase3_second_stage_controller_eval_500_a40.md` | current Phase 3D main controller evidence |
| Second-stage scored heldout goals | `outputs/phase3_second_stage_eval_goals_500.jsonl` | heldout eval input |
| Second-stage controller model summary | `outputs/phase3_second_stage_controller_model_1500_500.json` | current model artifact |
| Second-stage trainer | `src/train_phase3_second_stage_controller.py` | current implementation |
| Second-stage policy | `rule_far_learned_second_stage` in `src/far_controller.py` | current policy implementation |
| Second-stage launcher | `src/launch_phase3_second_stage_controller_a40.sh` | current canonical run script |

Numbers that may be cited from second-stage controller eval:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `learned_rerank` | 64.2% | 0.0% | 56.0 |
| `learned_expansion` | 84.0% | 67.7% | 57.7 |
| `rule_far_learned` | 84.4% | 68.5% | 57.4 |
| `learned_base_fallback` | 87.0% | 73.8% | 57.6 |
| `rule_far_learned_failure_specific` | 87.0% | 73.8% | 57.0 |
| `rule_far_learned_second_stage` | 92.4% | 84.7% | 53.9 |
| `rule_far_full` | 55.6% | 55.0% | 86.6 |

Second-stage caption warning:

- This is a heldout 500-goal trace-core recovery result.
- The retriever and second-stage controller are both trained from traced proof-core labels on the 1500-goal training split.
- The strongest fair baseline is `learned_base_fallback`, not BM25 and not `learned_expansion` alone.
- The paper-safe controller claim is +5.4 success and +10.9 FFR over `learned_base_fallback`, with fewer average premises.
- Do not describe `rule_far_full` as an upper bound for learned imported-core methods; it is an old oracle-tag hand controller.

Split-stability fold0 canonical outputs:

| Paper item | Source JSON/script | Status |
|---|---|---|
| Fold0 second-stage eval | `outputs/phase3_second_stage_controller_eval_fold0_500_a40.json`, `outputs/phase3_second_stage_controller_eval_fold0_500_a40.md` | current Phase 3E split-stability evidence |
| Fold0 learned heldout goals | `outputs/phase3_learned_eval_fold0_goals_500.jsonl` | heldout eval input after learned scoring |
| Fold0 second-stage heldout goals | `outputs/phase3_second_stage_eval_fold0_goals_500.jsonl` | heldout eval input after second-stage scoring |
| Fold0 learned retriever model | `outputs/phase3_learned_retriever_model_fold0_1500_500.json` | model artifact |
| Fold0 second-stage model | `outputs/phase3_second_stage_controller_model_fold0_1500_500.json` | model artifact |
| Fold split generator | `src/make_phase3_fold_split.py` | current implementation |
| Fold stability launcher | `src/launch_phase3_split_stability_a40.sh` | current canonical run script |

Fold0 numbers that may be cited:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `learned_rerank` | 63.4% | 0.0% | 56.0 |
| `learned_expansion` | 79.0% | 57.7% | 58.4 |
| `rule_far_learned` | 79.4% | 58.5% | 58.4 |
| `learned_base_fallback` | 83.6% | 66.9% | 57.7 |
| `rule_far_learned_failure_specific` | 83.4% | 66.5% | 56.8 |
| `rule_far_learned_second_stage` | 91.6% | 83.1% | 54.3 |
| `rule_far_full` | 53.2% | 52.6% | 86.7 |

Fold0 caption warning:

- This is one alternate fold, not a full k-fold variance table.
- Fold0 is harder for the learned retriever than the original heldout split: `learned_expansion` is 79.0% vs 84.0%.
- Cite fold0 together with the original heldout result to support split stability.
- The strongest fold0 claim is +8.0 success and +16.2 FFR over `learned_base_fallback`, with fewer average premises.

Audit warning:

- Do not cite `outputs/phase1_mathlib_trace_core_500_ablation_a40.*` as the main less-oracle evidence; it used the older failure-label order that collapsed first failures into `timeout`.
- Do not cite `outputs/phase1_mathlib_trace_core_500_a40_artifact_initial_tag_leak.*`; it is a known tag-leak artifact.

## Audit Rules

1. 主文数字必须能追溯到 `outputs/*.json`。
2. Figure/table 生成脚本放在 `src/` 或 `analysis/`。
3. caption 必须说明 dataset、budget、baseline、CI 范围。
4. 若只有部分模型有 CI，只给这些模型加 bracket，并在 caption 说明。
5. 若某个 backend/protocol 没有 invalid/failure class，不计算 AUROC，改报 count。
