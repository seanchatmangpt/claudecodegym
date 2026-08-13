from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
import json

BASE_URL = "https://code.claude.com/docs/"

@dataclass(frozen=True)
class DocSource:
    path: str
    url: str

@dataclass(frozen=True)
class ToolFact:
    name: str
    consequence: str
    permission_required_default: bool

class Catalog:
    """Immutable projection of the checked-in official-source lock and tool facts."""
    def __init__(self) -> None:
        data = files("claudecodegym.data")
        self._docs_raw = json.loads(data.joinpath("official_docs.lock.json").read_text())
        self._tools_raw = json.loads(data.joinpath("tools.json").read_text())

    @property
    def observed_at(self) -> str:
        return self._docs_raw["observed_at"]

    @property
    def index_sha256(self) -> str:
        return self._docs_raw["index_sha256"]

    def documents(self) -> tuple[DocSource, ...]:
        return tuple(DocSource(path=p, url=BASE_URL+p) for p in self._docs_raw["document_paths"])

    def tools(self) -> tuple[ToolFact, ...]:
        return tuple(ToolFact(**x) for x in self._tools_raw["tools"])

    def source_for_path(self, suffix: str) -> DocSource | None:
        return next((d for d in self.documents() if d.url.endswith(suffix)), None)
