from __future__ import annotations

import asyncio
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import Any
from uuid import uuid4

@dataclass(frozen=True)
class CapabilitySpec:
    iri: str
    title: str
    consequence: str
    binding: str

CAPABILITY_SPECS=(
    CapabilitySpec("urn:claudecodegym:capability:inspect-version","inspect-version","READ","inspect-version"),
    CapabilitySpec("urn:claudecodegym:capability:inspect-help","inspect-help","READ","inspect-help"),
    CapabilitySpec("urn:claudecodegym:capability:inspect-corpus","inspect-corpus","READ","inspect-corpus"),
    CapabilitySpec("urn:claudecodegym:capability:execute-headless-case","execute-headless-case","DO","execute-headless-case"),
    CapabilitySpec("urn:claudecodegym:capability:verify-case","verify-case","READ","verify-case"),
)

def gymact_capabilities() -> tuple[Any,...]:
    """Project local specs into GymAct models only when GymAct is actually installed."""
    try:
        from gymact.models import Capability, Consequence
    except ImportError as exc:
        raise RuntimeError("GYMACT_RUNTIME_UNAVAILABLE") from exc
    return tuple(Capability(iri=s.iri,title=s.title,consequence=Consequence(s.consequence),binding=s.binding) for s in CAPABILITY_SPECS)

class ClaudeCodeEnvironment:
    requires_authority=True
    def __init__(self, *, workspace: Path, claude_binary: str="claude", timeout_s: float=120.0) -> None:
        self.environment_id=f"urn:claudecodegym:environment:{uuid4().hex}"
        self.workspace=workspace.resolve()
        self.claude_binary=claude_binary
        self.timeout_s=timeout_s
        self._last: dict[str,Any]|None=None
        self._closed=False
    def _open(self):
        if self._closed: raise RuntimeError("environment is torn down")
    def capabilities(self): self._open(); return gymact_capabilities()
    async def _run(self,*args:str)->dict[str,Any]:
        self._open()
        exe=shutil.which(self.claude_binary)
        if exe is None: raise RuntimeError("CLAUDE_CODE_BINARY_UNAVAILABLE")
        proc=await asyncio.create_subprocess_exec(exe,*args,cwd=self.workspace,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        try:
            out,err=await asyncio.wait_for(proc.communicate(),timeout=self.timeout_s)
        except TimeoutError:
            proc.kill(); await proc.wait(); raise RuntimeError("CLAUDE_CODE_TIMEOUT")
        result={"argv":[self.claude_binary,*args],"exit_code":proc.returncode,"stdout":out.decode(errors="replace"),"stderr":err.decode(errors="replace")}
        self._last=deepcopy(result); return result
    async def observe(self)->dict[str,Any]: self._open(); return {"workspace":str(self.workspace),"claude_available":shutil.which(self.claude_binary) is not None,"last":deepcopy(self._last)}
    async def actuate(self, capability: Any, payload: dict[str,Any])->dict[str,Any]:
        binding=capability.binding
        if binding=="inspect-version": return await self._run("--version")
        if binding=="inspect-help": return await self._run("--help")
        if binding=="inspect-corpus":
            from .catalog import Catalog
            c=Catalog(); result={"documents":len(c.documents()),"tools":len(c.tools()),"observed_at":c.observed_at,"index_sha256":c.index_sha256}; self._last=deepcopy(result); return result
        if binding=="execute-headless-case":
            prompt=payload.get("prompt")
            if not isinstance(prompt,str) or not prompt.strip(): raise ValueError("payload.prompt must be a non-empty string")
            args=["-p",prompt,"--output-format","json"]
            model=payload.get("model")
            if model is not None:
                if not isinstance(model,str) or not model: raise ValueError("payload.model must be a string")
                args.extend(["--model",model])
            return await self._run(*args)
        if binding=="verify-case":
            expected_exit=payload.get("exit_code",0); observed=deepcopy(self._last)
            return {"passed":bool(observed and observed.get("exit_code")==expected_exit),"observed":observed}
        raise ValueError(f"unsupported provider binding: {binding}")
    async def verify(self, expected:dict[str,Any]):
        observed=await self.observe(); return all(observed.get(k)==v for k,v in expected.items()), observed
    async def checkpoint(self): self._open(); return {"last":deepcopy(self._last)}
    async def restore(self, checkpoint): self._open(); self._last=deepcopy(checkpoint.get("last"))
    async def teardown(self): self._closed=True

class ClaudeCodeProvider:
    name="claudecode"
    materialization_requires_authority=False
    async def materialize(self, *, scenario:str|None, config:dict[str,Any])->ClaudeCodeEnvironment:
        del scenario
        workspace=Path(config.get("workspace","."))
        if not workspace.exists() or not workspace.is_dir(): raise ValueError("config.workspace must be an existing directory")
        timeout=float(config.get("timeout_s",120.0))
        if timeout<=0 or timeout>600: raise ValueError("config.timeout_s must be > 0 and <= 600")
        return ClaudeCodeEnvironment(workspace=workspace,claude_binary=str(config.get("claude_binary","claude")),timeout_s=timeout)
