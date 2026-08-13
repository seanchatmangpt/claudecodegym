# Architecture

ClaudeCodeGym separates four evidence layers:

1. **Observed public surface** — `official_docs.lock.json` pins the complete official Claude Code documentation index observed on 2026-08-12. `tools.json` records the built-in tool names and default permission-prompt facts observed in the official tools reference.
2. **Admitted GymAct ABox** — `ggen/claudecode-gymact-pack/ontology.ttl` contains only executable provider operations as `sosa:Procedure` facts. No custom TBox is introduced.
3. **Manufacture** — the consumer-local ggen pack projects that ABox into Rust operation, MCP, reference, and proof surfaces. Generated outputs belong under `generated/` and are never editing surfaces.
4. **Execution/standing** — `ClaudeCodeProvider` materializes a bounded workspace. READ inspection and DO headless execution remain distinct. A real GymAct runtime supplies authority, receipts, OCEL, and replay; this repo does not counterfeit those claims.

## Scenario calculus

`ScenarioFactory` manufactures deterministic cases from `ToolFact × permission mode × failure disposition`, pruning impossible denial cases. This is a bounded test topology, not a claim that every tool exists on every Claude Code surface or plan. Surface/plan availability stays source evidence until observed by an execution adapter.

## Freshness

Run `claudecodegym-research --observed-at <explicit ISO timestamp>` to re-fetch the official index and regenerate its lock. A changed SHA is drift, not automatic admission: review the diff, update tool facts/ontology only when the source supports it, then rerun tests and ggen.
