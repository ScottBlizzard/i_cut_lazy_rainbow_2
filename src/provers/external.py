"""External prover command wrapper.

Contract for server-side Lean integration:

The command is invoked as:

    <command> --request request.json --response response.json

Request JSON:

{
  "goal": {... Goal ...},
  "premises": [{... Premise ...}],
  "timeout_s": 10.0
}

Response JSON must match `ProverResult` fields from schema.py. This isolates
the experiment loop from Lean/LeanDojo/LeanHammer implementation details.
"""

from __future__ import annotations

import json
import shlex
import subprocess
import tempfile
from pathlib import Path

from schema import Goal, Premise, ProverResult, prover_result_from_dict, to_jsonable


class ExternalCommandProver:
    name = "external_command"

    def __init__(self, command: str, *, cwd: Path | None = None) -> None:
        self.command = command
        self.cwd = cwd

    def prove(self, goal: Goal, premises: list[Premise], *, timeout_s: float) -> ProverResult:
        with tempfile.TemporaryDirectory() as td:
            req = Path(td) / "request.json"
            resp = Path(td) / "response.json"
            req.write_text(
                json.dumps(
                    {
                        "goal": to_jsonable(goal),
                        "premises": to_jsonable(premises),
                        "timeout_s": timeout_s,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            cmd = shlex.split(self.command) + ["--request", str(req), "--response", str(resp)]
            subprocess.run(cmd, cwd=self.cwd, check=True, timeout=timeout_s + 30)
            data = json.loads(resp.read_text(encoding="utf-8"))
            return prover_result_from_dict(data)
