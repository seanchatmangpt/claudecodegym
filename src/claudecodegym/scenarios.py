from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from .catalog import Catalog, ToolFact

PERMISSION_MODES=("default","acceptEdits","dontAsk","plan","bypassPermissions")
FAILURES=("nominal","denied","unavailable","timeout")

@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    tool: str
    consequence: str
    permission_mode: str
    failure: str
    expected: str

class ScenarioFactory:
    """Manufacture bounded cases from admitted tool facts; no hand-curated one-offs."""
    def __init__(self, catalog: Catalog | None=None) -> None:
        self.catalog=catalog or Catalog()

    @staticmethod
    def _id(payload: dict[str,str]) -> str:
        raw=json.dumps(payload,sort_keys=True,separators=(",", ":")).encode()
        return "ccg-"+sha256(raw).hexdigest()[:16]

    def for_tool(self, tool: ToolFact) -> tuple[Scenario,...]:
        cases=[]
        for mode in PERMISSION_MODES:
            for failure in FAILURES:
                if failure=="denied" and not (tool.permission_required_default or mode in {"dontAsk","plan"}):
                    continue
                expected = "REFUSED" if failure=="denied" else ("UNSUPPORTED" if failure=="unavailable" else ("BLOCKED" if failure=="timeout" else "EXPECTED_SUCCESS"))
                p={"tool":tool.name,"permission_mode":mode,"failure":failure,"expected":expected}
                cases.append(Scenario(self._id(p),tool.name,tool.consequence,mode,failure,expected))
        return tuple(cases)

    def all(self) -> tuple[Scenario,...]:
        return tuple(case for tool in self.catalog.tools() for case in self.for_tool(tool))
