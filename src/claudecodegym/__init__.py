"""ClaudeCodeGym: source-backed GymAct scenarios for Claude Code."""

from .catalog import Catalog, DocSource, ToolFact
from .provider import ClaudeCodeEnvironment, ClaudeCodeProvider
from .scenarios import Scenario, ScenarioFactory

__all__ = ["Catalog", "DocSource", "ToolFact", "ClaudeCodeEnvironment", "ClaudeCodeProvider", "Scenario", "ScenarioFactory"]
__version__ = "26.8.12"
