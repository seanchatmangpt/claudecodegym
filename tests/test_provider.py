import asyncio
from pathlib import Path
import pytest
from claudecodegym.provider import ClaudeCodeProvider, CapabilitySpec

def test_provider_materializes_bounded_workspace(tmp_path: Path):
    env=asyncio.run(ClaudeCodeProvider().materialize(scenario=None,config={"workspace":str(tmp_path),"timeout_s":1})); assert env.requires_authority is True; assert env.workspace==tmp_path.resolve()

def test_missing_claude_binary_is_typed_failure(tmp_path: Path):
    env=asyncio.run(ClaudeCodeProvider().materialize(scenario=None,config={"workspace":str(tmp_path),"claude_binary":"__definitely_absent_claude__"})); cap=CapabilitySpec("x","x","READ","inspect-version")
    with pytest.raises(RuntimeError,match="CLAUDE_CODE_BINARY_UNAVAILABLE"): asyncio.run(env.actuate(cap,{}))

def test_invalid_headless_prompt_refused_before_process(tmp_path: Path):
    env=asyncio.run(ClaudeCodeProvider().materialize(scenario=None,config={"workspace":str(tmp_path)})); cap=CapabilitySpec("x","x","DO","execute-headless-case")
    with pytest.raises(ValueError,match="payload.prompt"): asyncio.run(env.actuate(cap,{"prompt":""}))
