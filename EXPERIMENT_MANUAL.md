# 实验手册 (Experiment Manual)

> 用途：防止上下文丢失时快速恢复实验环境。每次新对话开始时先读本文件。  
> 最后更新：2026-06-17  
> 当前状态：4090 维修中，短期主实验服务器切到 A40；A40 已确认 Python/Git/Lean/Lake，可运行 Phase 1 synthetic mock 和 real Lean wrapper sanity。

---

## 一、服务器信息

### 1. 4090 服务器（8x RTX 4090, 24GB/卡）

> 当前状态：维修中，短期不作为实验依赖。

| 项目 | 值 |
|---|---|
| SSH 命令 | `ssh ccj@10.10.217.244` |
| 认证方式 | 免密（已配置密钥） |
| 内网要求 | 必须连接学校/实验室内网 |
| 项目路径 | `/home/ccj/workspace_1/iclr_2/` |
| 代码路径 | `/home/ccj/workspace_1/iclr_2/src/` |
| 输出路径 | `/home/ccj/workspace_1/iclr_2/outputs/` |
| 推荐 Python 环境 | `conda activate iclr2`（若未创建则 Phase 0 创建） |
| Lean 环境 | 暂停确认，等维修结束后复查 |
| 主要用途 | 恢复后用于 parallel prover calls、retriever/reranker grid、failure parser ablation |

标准启动：

```bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate iclr2
cd /home/ccj/workspace_1/iclr_2/src
CUDA_VISIBLE_DEVICES=0 python <script>.py > ../outputs/log_<name>.txt 2>&1 &
```

GPU 检查：

```bash
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader
```

### 2. A40 服务器（2x NVIDIA A40, 46GB/卡）

| 项目 | 值 |
|---|---|
| SSH 命令 | `ssh -p 10008 root@10.91.11.250` |
| 认证方式 | 免密（已配置密钥） |
| 内网要求 | 必须连接学校/实验室内网 |
| 项目路径 | `/workspace/thymic_project/paper/iclr_2/` |
| 代码路径 | `/workspace/thymic_project/paper/iclr_2/src/` |
| 输出路径 | `/workspace/thymic_project/paper/iclr_2/outputs/` |
| 推荐 Python 环境 | `conda activate /workspace/thymic_project/paper/iclr2/.conda` |
| Lean 环境 | `source /root/.elan/env`；Lean 4.31.0 / Lake 5.0.0 |
| HuggingFace | 若不能访问，设置 `export HF_ENDPOINT=https://hf-mirror.com` |
| 主要用途 | 当前主实验服务器；大 embedding/reranker、LeanSearch candidate generation、memory-heavy runs、Phase 1 sanity |

标准启动：

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda
source /root/.elan/env
export HF_ENDPOINT=https://hf-mirror.com
cd /workspace/thymic_project/paper/iclr_2/src
CUDA_VISIBLE_DEVICES=0 python <script>.py > ../outputs/log_<name>.txt 2>&1 &
```

A40 当前环境记录：

| 项目 | 状态 |
|---|---|
| Python | 3.10.20 |
| Git | 2.53.0 |
| Lean | 4.31.0 |
| Lake | 5.0.0 |
| `torch` | 2.6.0+cu124 |
| `transformers` | 5.2.0 |
| `sentence_transformers` | 5.6.0 |
| `sklearn` | 1.7.2 |
| `faiss` | 1.14.3 |
| `lean_dojo` | 4.20.0 |
| LeanDojo-v2 env | `/workspace/thymic_project/paper/iclr2_py311`, Python 3.11.15 |

对应输出：`outputs/log_phase1_env_a40_with_lean.txt`。

---

## 二、本地环境

| 项目 | 值 |
|---|---|
| 本地根目录 | `D:\ICLR_2` |
| 代码路径 | `D:\ICLR_2\src\` |
| 输出路径 | `D:\ICLR_2\outputs\` |
| 论文目录 | `D:\ICLR_2\iclr2027\` |
| 相关论文 | `D:\ICLR_2\papers\` |
| 主蓝图 | `D:\ICLR_2\idea_guide_failure_aware_lean_premise_iclr2027_zh.md` |
| 实验报告 | `D:\ICLR_2\experiment_report.md` |

本地同步代码：

```powershell
.\push.ps1
.\push.ps1 -Server A40
```

服务器结果拉回本地：

```powershell
.\pull_outputs.ps1
.\pull_outputs.ps1 -Server A40
```

单文件上传：

```powershell
scp D:\ICLR_2\src\<file>.py ccj@10.10.217.244:/home/ccj/workspace_1/iclr_2/src/
```

A40 单文件上传：

```powershell
scp -P 10008 D:\ICLR_2\src\<file>.py root@10.91.11.250:/workspace/thymic_project/paper/iclr_2/src/
```

下载结果：

```powershell
scp ccj@10.10.217.244:/home/ccj/workspace_1/iclr_2/outputs/<file> D:\ICLR_2\outputs\
scp -P 10008 root@10.91.11.250:/workspace/thymic_project/paper/iclr_2/outputs/<file> D:\ICLR_2\outputs\
```

---

## 三、Phase 0 环境检查清单

在服务器上确认：

```bash
which python
python --version
which lake || true
which lean || true
lean --version || true
lake --version || true
```

Python 包：

```bash
python - <<'PY'
import sys
print(sys.version)
for p in ["torch", "transformers", "sentence_transformers", "faiss", "sklearn"]:
    try:
        m = __import__(p)
        print(p, getattr(m, "__version__", "ok"))
    except Exception as e:
        print(p, "MISSING", e)
PY
```

Lean 基础环境和 LeanDojo Python 包在 A40 已确认；Mathlib traced repo / LeanHammer 仍待接入。原 LeanDojo 4.20.0 对 Lean 4.31 trace 失败，LeanDojo-v2 需要 Python 3.11，因此单独使用 `iclr2_py311` 测试。

LeanDojo-v2 trace-only 环境说明：

- 全量 `lean-dojo-v2` 依赖会拉 deepspeed/torch/training stack，安装很慢。
- 当前 `iclr2_py311` 使用 `lean-dojo-v2 --no-deps`、trace 所需轻依赖、以及 deepspeed/pytorch-lightning minimal stubs，只用于 repo trace / theorem extraction。
- tiny Lean 4.31 probe 已通过：`outputs/lean_dojo_v2_probe_summary.json`、`outputs/lean_dojo_v2_probe_goals.jsonl`。
- 当前 mathlib4 HEAD trace 后台任务：
  - PID: `46621`
  - commit: `014c1563dc2c952488b6acfd3fac97ee588f0c6d`
  - route: GitHub codeload archive -> local `git init` repo -> LeanDojo-v2 trace
  - log: `/workspace/thymic_project/paper/iclr_2/outputs/log_mathlib4_local_trace_v2_current.txt`
  - summary: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib4_local_trace_v2_current_summary.json`

监控命令：

```bash
ps -p 46621 -o pid,etime,pcpu,pmem,rss,cmd
ps -eo pid,ppid,etime,pcpu,pmem,rss,cmd | grep -E 'trace_mathlib_v2|git clone|lake|lean ' | grep -v grep
tail -n 80 /workspace/thymic_project/paper/iclr_2/outputs/log_mathlib4_local_trace_v2_current.txt
```

trace 完成后生成真实 goals：

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2_py311
cd /workspace/thymic_project/paper/iclr_2/src
TRACE_ROOT="$(python -c 'import json; from pathlib import Path; print(json.loads(Path("../outputs/mathlib4_local_trace_v2_current_summary.json").read_text())["traced_root"])')"
python make_phase1_mathlib_goals_v2.py --trace-root "$TRACE_ROOT" --out ../outputs/phase1_mathlib_v2_goals_500.jsonl --n-goals 500 --max-candidates 256
```

已完成 A40 检查命令：

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda
source /root/.elan/env
cd /workspace/thymic_project/paper/iclr_2/src
python check_env.py > ../outputs/log_phase1_env_a40_with_lean.txt 2>&1
```

---

## 四、代码架构计划

| 文件/目录 | 功能 |
|---|---|
| `src/config.py` | 路径、budget、backend、dataset 配置 |
| `src/schema.py` | JSON schema/dataclass |
| `src/data_io.py` | JSON/JSONL load-write helpers |
| `src/retrievers/` | retriever interfaces and mock retriever |
| `src/provers/` | mock prover and external command prover |
| `src/failure_parser.py` | failure taxonomy parser |
| `src/far_controller.py` | one-shot/top-k/random/history/Rule-FAR policies |
| `src/synthetic_data.py` | local synthetic goals for smoke tests |
| `src/eval_phase1.py` | local synthetic fixed-budget evaluation |
| `src/eval_phase1_real.py` | real-goal evaluation via external Lean prover command |
| `src/analyze_phase1.py` | JSON to markdown summary |
| `src/check_env.py` | local/server environment check |

### Phase 1 本地 smoke test

```powershell
cd D:\ICLR_2\src
python check_env.py
python eval_phase1.py --n-goals 100 --seed 1 --out ..\outputs\phase1_synthetic_smoke.json
python analyze_phase1.py --input ..\outputs\phase1_synthetic_smoke.json --out ..\outputs\phase1_synthetic_smoke.md
python -m compileall .
```

### Real Lean backend contract

`src/eval_phase1_real.py` 不直接依赖某个 Lean 库。它调用一个外部命令：

```bash
python eval_phase1_real.py \
  --goals ../outputs/phase1_goals.jsonl \
  --prover-command "python lean_attempt.py" \
  --out ../outputs/phase1_real.json
```

`lean_attempt.py` 必须支持：

```bash
python lean_attempt.py --request request.json --response response.json
```

Request JSON 包含：

```json
{
  "goal": {"goal_id": "...", "goal_state": "...", "candidates": []},
  "premises": [],
  "timeout_s": 10.0
}
```

Response JSON 必须匹配 `ProverResult`：

```json
{
  "success": false,
  "verified": false,
  "failure": {
    "failure_type": "timeout",
    "backend": "lean",
    "message": "...",
    "reconstruction_status": "not_attempted",
    "unsolved_goals": [],
    "raw": {}
  },
  "used_premises": [],
  "proof_core_recovered": [],
  "time_s": 10.0,
  "backend_status": "timeout",
  "reconstruction_status": "not_attempted"
}
```

## 2026-06-18 A40 Mathlib Trace Recovery Notes

Current active run:

- Trace PID: `490924`
- Watcher PID: `491421`
- Trace log: `/workspace/thymic_project/paper/iclr_2/outputs/log_mathlib4_local_trace_v2_current.txt`
- Watcher log: `/workspace/thymic_project/paper/iclr_2/outputs/log_mathlib_trace_core_watcher.txt`
- Local mathlib commit used by LeanDojo: `64a930d1015bab6c2bf24f885c7d3403c160cc28`
- Original mathlib commit recorded in repo: `014c1563dc2c952488b6acfd3fac97ee588f0c6d`

Important recovery fixes:

- Remote LeanDojo-v2 AST parser has a local compatibility patch for Lean 4.31 declaration nodes.
- Mathlib dependencies are mirrored under `/workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors`.
- The active mathlib `lake-manifest.json` uses `file://` dependency URLs, avoiding GitHub clone during LeanDojo temp builds.

Monitor command:

```bash
ssh -p 10008 root@10.91.11.250 "ps -eo pid,ppid,stat,etime,cmd | grep -E 'trace_mathlib_v2|lake build|ExtractData|watch_mathlib_trace_core' | grep -v grep; tail -n 80 /workspace/thymic_project/paper/iclr_2/outputs/log_mathlib4_local_trace_v2_current.txt; tail -n 40 /workspace/thymic_project/paper/iclr_2/outputs/log_mathlib_trace_core_watcher.txt"
```

If the mathlib local dependency manifest must be regenerated:

```bash
ssh -p 10008 root@10.91.11.250
cd /workspace/thymic_project/paper/iclr_2
bash src/prepare_mathlib_local_deps_a40.sh
```

If the trace must be restarted:

```bash
ssh -p 10008 root@10.91.11.250
cd /workspace/thymic_project/paper/iclr_2/src
FORCE_ARCHIVE=1 setsid bash launch_mathlib_local_trace_a40_v2.sh 014c1563dc2c952488b6acfd3fac97ee588f0c6d > ../outputs/nohup_mathlib4_local_trace_v2_current.txt 2>&1 < /dev/null &
echo $! > ../outputs/pid_mathlib4_local_trace_v2_current.txt
```

Then start the watcher with the trace PID:

```bash
cd /workspace/thymic_project/paper/iclr_2
TRACE_PID="$(cat outputs/pid_mathlib4_local_trace_v2_current.txt)"
setsid bash src/watch_mathlib_trace_core_a40.sh "$TRACE_PID" > outputs/log_mathlib_trace_core_watcher_outer.txt 2>&1 < /dev/null &
echo $! > outputs/pid_mathlib_trace_core_watcher.txt
```

---

## 五、常见问题排查

| 问题 | 原因 | 解决 |
|---|---|---|
| `python: command not found` | conda 未激活 | source conda.sh 后 activate |
| `lean: command not found` | Lean/elan 未装或 PATH 错 | Phase 0 安装/修 PATH |
| Mathlib build 很慢 | 第一次 lake build | 使用缓存；记录 commit |
| prover timeout 大量出现 | premise set/noise 或 backend 配置 | 对比 tiny subset sanity |
| random retry 异常强 | budget 不公平或 retry candidate 泄漏 | 审计 wall-clock/calls |
| LeanSearch API 失败 | 网络/API 限制 | 服务器离线 corpus 或本地 cache |
| PowerShell 引号问题 | 内嵌命令复杂 | 写脚本上传执行 |

## 2026-06-18 A40 Trace-Core Runbook

Current automatic watcher:

```bash
ps -p 205137 -o pid,etime,cmd
tail -n 80 /workspace/thymic_project/paper/iclr_2/outputs/log_mathlib_trace_core_after_trace.txt
```

Manual fallback after trace completion:

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2_py311
cd /workspace/thymic_project/paper/iclr_2/src
TRACE_ROOT="$(python -c 'import json; from pathlib import Path; print(json.loads(Path("../outputs/mathlib4_local_trace_v2_current_summary.json").read_text())["traced_root"])')"
python make_phase1_mathlib_goals_v2.py --trace-root "$TRACE_ROOT" --out ../outputs/phase1_mathlib_v2_goals_500.jsonl --n-goals 500 --max-candidates 256
bash launch_phase1_mathlib_trace_core_a40.sh ../outputs/phase1_mathlib_v2_goals_500.jsonl ../outputs/phase1_mathlib_trace_core_500_a40.json ../outputs/phase1_mathlib_trace_core_500_a40.md
```

Interpretation:

- `phase1_mathlib_trace_core_500_a40.*` is trace-grounded proof-core recovery evidence.
- It is not yet full Lean proof reconstruction evidence.
- Use it to validate the failure-aware premise-selection hypothesis before wiring a Mathlib-aware long-lived prover.
