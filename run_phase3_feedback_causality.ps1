$ErrorActionPreference = "Stop"

$policies = @(
  "learned_base_fallback",
  "rule_far_learned_second_stage",
  "rule_far_learned_second_stage_fixed_imported",
  "rule_far_learned_second_stage_fixed_bridge",
  "rule_far_learned_second_stage_fixed_type",
  "rule_far_learned_second_stage_cyclic",
  "rule_far_learned_second_stage_shuffled"
)

$splits = @(
  @{ Name = "original"; Goals = "outputs\phase3_second_stage_eval_goals_500.jsonl"; Out = "outputs\phase3_feedback_causality_original_500.json" },
  @{ Name = "fold0"; Goals = "outputs\phase3_second_stage_eval_fold0_goals_500.jsonl"; Out = "outputs\phase3_feedback_causality_fold0_500.json" },
  @{ Name = "fold1"; Goals = "outputs\phase3_second_stage_eval_fold1_goals_500.jsonl"; Out = "outputs\phase3_feedback_causality_fold1_500.json" },
  @{ Name = "fold2"; Goals = "outputs\phase3_second_stage_eval_fold2_goals_500.jsonl"; Out = "outputs\phase3_feedback_causality_fold2_500.json" }
)

foreach ($split in $splits) {
  Write-Host "Running Gate 0 feedback-causality split: $($split["Name"])"
  python src\eval_phase1_trace_core.py `
    --goals $($split["Goals"]) `
    --out $($split["Out"]) `
    --first-k 32 `
    --retry-k 32 `
    --max-attempts 3 `
    --timeout-s 30 `
    --policies $policies
}

$outs = $splits | ForEach-Object { $_["Out"] }
python src\summarize_phase3_feedback_causality.py `
  --inputs $outs `
  --out outputs\phase3_feedback_causality_gate0.md
