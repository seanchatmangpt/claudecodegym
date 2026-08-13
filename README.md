# ClaudeCodeGym

A source-backed GymAct gym for systematically exercising Claude Code without collapsing documentation, tool availability, execution, and verified consequence into one claim.

## Current admitted corpus

- 187 official Claude Code documentation pages discovered from Anthropic's live `llms.txt` index on 2026-08-12.
- 44 built-in tool names from Anthropic's official tools reference, conservatively classified into GymAct `READ`/`DO` consequences.
- Deterministic scenario manufacture across tool, permission-mode, and failure dimensions (>500 cases; exact count is tested).
- Consumer-local GymAct ggen bridge pack derived from GymAct's canonical `consumer-bridge-pack-template`.
- Exact GymAct source boundary: `5a40c8f402aeb14699e216e17b2ef7aae9f0bc8f`; profile shape copy is SHA-256 locked.

## What is executable

`ClaudeCodeProvider` can inspect the installed Claude Code version/help, inspect the locked research corpus, execute a bounded headless `claude -p ... --output-format json` case, and verify the last process exit status. The environment is authority-requiring because headless cases can change a workspace or reach external services.

The ggen ABox claims **only those implemented operations**. The larger 187-page/44-tool corpus is research input for scenario manufacture, not an assertion that every capability is available in the current environment.

## Verify

```bash
python -m pytest
# with ggen installed:
ggen sync run
```

A real Claude Code binary enables `tests/test_live_claude.py`. A real GymAct installation is required to project `CapabilitySpec` values into `gymact.models.Capability` and to earn receipt/OCEL standing. Tests that do not have those collaborators never claim ALIVE for them.

## Sources

The source lock stores every official documentation path plus the observed index digest rather than mirroring Anthropic documentation text. Refresh with:

```bash
claudecodegym-research --observed-at 2026-08-12T23:27:00-07:00
```

See `docs/architecture.md` for the observation → admission → manufacture → execution → receipt boundary.
