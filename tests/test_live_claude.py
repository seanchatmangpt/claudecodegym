import asyncio, shutil
from pathlib import Path
import pytest
from claudecodegym.provider import ClaudeCodeProvider, CapabilitySpec

@pytest.mark.skipif(shutil.which("claude") is None, reason="real Claude Code binary not installed in validation environment")
def test_real_claude_version_executes(tmp_path: Path):
    env=asyncio.run(ClaudeCodeProvider().materialize(scenario=None,config={"workspace":str(tmp_path),"timeout_s":30})); cap=CapabilitySpec("x","x","READ","inspect-version"); out=asyncio.run(env.actuate(cap,{})); assert out["exit_code"]==0; assert out["stdout"].strip()
