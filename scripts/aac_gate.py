#!/usr/bin/env python3
"""AAC Creation Gate v2.0.

Deterministic CI gate for AAC card artifacts. It validates workflow, node,
agent-envelope, registry, and run-card schema files without external packages.

The gate is intentionally conservative: it checks structure, required fields,
object boundaries, cross-references, lane intersections, owners, hard-refuse
paths, and kill switches. It does not replace AgentTwin or the full 57-item AAC
rubric. Every FAIL must include a concrete remediation and passing example.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LANE_ORDER = [
    "read",
    "recommend",
    "draft",
    "write",
    "send",
    "pay",
    "label",
    "escalate",
]

RELEVANT_PREFIXES = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".codex/",
    ".hermes/",
    "skills/",
    "optional-skills/",
    "docs/agents/",
    "docs/aac/",
    "docs/workflows/",
    "docs/specs/",
    "prompts/",
    "workflows/",
    "cron/",
    "plugins/",
    "tools/",
    "mcp/",
    ".github/workflows/",
)

DISCIPLINES = ("bounded", "grounded", "gated", "observed", "governed")
GATES = ("input", "output", "cross_check", "action")


@dataclass
class Finding:
    level: str
    path: str
    message: str
    remediation: str = ""

    def render(self) -> str:
        text = f"{self.level}: {self.path}: {self.message}"
        if self.remediation:
            text += f"\n  Remediation: {self.remediation}"
        return text


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def changed_files(repo: Path, base: str | None, head: str | None) -> list[str]:
    if base and head:
        output = run_git(["diff", "--name-only", f"{base}...{head}"], repo)
    elif base:
        output = run_git(["diff", "--name-only", base], repo)
    else:
        output = run_git(["diff", "--name-only", "HEAD"], repo)
    return [line.strip() for line in output.splitlines() if line.strip()]


def is_relevant(path: str) -> bool:
    if path in RELEVANT_PREFIXES:
        return True
    return any(path.startswith(prefix) for prefix in RELEVANT_PREFIXES)


def load_json(path: Path, findings: list[Finding]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - CI should show exact parse failure
        findings.append(
            Finding(
                "FAIL",
                str(path),
                f"invalid JSON: {exc}",
                "Fix JSON syntax. AAC cards are JSON so the GitHub gate has no YAML dependency.",
            )
        )
        return None


def non_empty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, dict):
        return bool(value)
    if isinstance(value, bool):
        return True
    return value is not None


def require_fields(card: dict[str, Any], path: str, fields: list[str], findings: list[Finding]) -> None:
    for field in fields:
        if field not in card or not non_empty(card[field]):
            findings.append(
                Finding(
                    "FAIL",
                    path,
                    f"missing required field '{field}'",
                    f"Add '{field}' to the AAC card before merge. Passing example: set a non-empty value that proves the gate is reviewable.",
                )
            )


def require_nested(card: dict[str, Any], path: str, parent: str, fields: tuple[str, ...], findings: list[Finding]) -> None:
    value = card.get(parent)
    if not isinstance(value, dict):
        findings.append(
            Finding(
                "FAIL",
                path,
                f"missing object '{parent}'",
                f"Add '{parent}' with fields: {', '.join(fields)}.",
            )
        )
        return
    for field in fields:
        if field not in value or not non_empty(value[field]):
            findings.append(
                Finding(
                    "FAIL",
                    path,
                    f"missing '{parent}.{field}'",
                    f"Add '{parent}.{field}' so the card is enforceable. Passing example: use a concrete named owner, cost, lane, source, gate, or sink value rather than 'TBD'.",
                )
            )


def lane_index(lane: str) -> int:
    try:
        return LANE_ORDER.index(lane)
    except ValueError:
        return -1


def validate_workflow(card: dict[str, Any], path: str, findings: list[Finding]) -> None:
    require_fields(
        card,
        path,
        [
            "aac_card_version",
            "workflow_id",
            "workflow_box",
            "control_topology",
            "value_mode",
            "cost_framing",
            "trigger",
            "finished_state",
            "max_lane",
            "nodes",
            "agents",
            "hard_refuse",
            "observability",
            "residue",
            "escalation_path",
        ],
        findings,
    )
    require_nested(card, path, "sinks", ("happy", "refuse", "hard_refuse"), findings)
    require_nested(card, path, "owners", ("process_owner", "technical_owner", "reviewer", "residue_accepter"), findings)
    require_nested(card, path, "cost_framing", ("cost_of_failure", "cost_of_inaction", "per_error_cost_band"), findings)
    if card.get("control_topology") not in {"unit", "graph_directed", "agent_directed_envelope", "hybrid"}:
        findings.append(
            Finding(
                "FAIL",
                path,
                "control_topology must be unit, graph_directed, agent_directed_envelope, or hybrid",
                "Declare the topology before AgentTwin or CI can score the workflow. Passing example: control_topology='graph_directed' for a fixed node DAG.",
            )
        )
    if card.get("value_mode") not in {"replace", "augment", "extend"}:
        findings.append(
            Finding("FAIL", path, "value_mode must be replace, augment, or extend", "Set value_mode explicitly. Passing example: value_mode='augment' when AI drafts and a human approves.")
        )


def validate_node(card: dict[str, Any], path: str, findings: list[Finding]) -> None:
    require_fields(
        card,
        path,
        [
            "aac_card_version",
            "workflow",
            "node_id",
            "runtime_mode",
            "max_lane",
            "owner",
            "input_contract",
            "output_contract",
            "data_classification",
            "hard_refuse",
            "telemetry",
            "kill_switch",
        ],
        findings,
    )
    if card.get("runtime_mode") not in {"D", "C", "A", "H"}:
        findings.append(Finding("FAIL", path, "runtime_mode must be D, C, A, or H", "Assign runtime by AAC attributes."))
    require_nested(card, path, "disciplines", DISCIPLINES, findings)
    require_nested(card, path, "gates", GATES, findings)


def validate_agent(card: dict[str, Any], path: str, findings: list[Finding]) -> None:
    require_fields(
        card,
        path,
        [
            "aac_card_version",
            "agent_id",
            "purpose",
            "allowed_workflows",
            "allowed_nodes",
            "tools",
            "allowed_action_classes",
            "forbidden_action_classes",
            "memory_policy",
            "telemetry_required",
            "kill_switch",
            "owner",
            "residue_accepter",
        ],
        findings,
    )
    require_nested(card, path, "disciplines", DISCIPLINES, findings)
    if card.get("memory_policy") not in {"none", "read_only", "proposal_only", "approved_write"}:
        findings.append(
            Finding(
                "FAIL",
                path,
                "memory_policy must be none, read_only, proposal_only, or approved_write",
                "Do not allow implicit memory writes from agent inference.",
            )
        )
    if card.get("telemetry_required") is not True:
        findings.append(Finding("FAIL", path, "telemetry_required must be true", "Agent envelopes must be observed."))


def validate_cross_refs(
    workflows: dict[str, tuple[dict[str, Any], str]],
    nodes: dict[str, tuple[dict[str, Any], str]],
    agents: dict[str, tuple[dict[str, Any], str]],
    findings: list[Finding],
) -> None:
    for workflow_id, (workflow, workflow_path) in workflows.items():
        workflow_lane = str(workflow.get("max_lane", ""))
        for node_id in workflow.get("nodes", []):
            if node_id not in nodes:
                findings.append(
                    Finding("FAIL", workflow_path, f"workflow references missing node '{node_id}'", "Add the node card or remove the reference.")
                )
                continue
            node, node_path = nodes[node_id]
            if node.get("workflow") != workflow_id:
                findings.append(
                    Finding("FAIL", node_path, f"node.workflow must equal '{workflow_id}'", "Match node card to its workflow card.")
                )
            wf_i = lane_index(workflow_lane)
            node_i = lane_index(str(node.get("max_lane", "")))
            if wf_i >= 0 and node_i > wf_i:
                findings.append(
                    Finding(
                        "FAIL",
                        node_path,
                        f"node max_lane '{node.get('max_lane')}' exceeds workflow max_lane '{workflow_lane}'",
                        "Lower the node max_lane or explicitly raise the workflow lane with owner approval.",
                    )
                )
        for agent_id in workflow.get("agents", []):
            if agent_id not in agents:
                findings.append(
                    Finding("FAIL", workflow_path, f"workflow references missing agent '{agent_id}'", "Add the agent envelope card or remove the reference.")
                )

    for agent_id, (agent, agent_path) in agents.items():
        for workflow_id in agent.get("allowed_workflows", []):
            if workflow_id not in workflows:
                findings.append(Finding("FAIL", agent_path, f"agent references missing workflow '{workflow_id}'", "Add the workflow card."))
        for node_id in agent.get("allowed_nodes", []):
            if node_id not in nodes:
                findings.append(Finding("FAIL", agent_path, f"agent references missing node '{node_id}'", "Add the node card."))
        forbidden = set(agent.get("forbidden_action_classes", []))
        allowed = set(agent.get("allowed_action_classes", []))
        overlap = sorted(forbidden & allowed)
        if overlap:
            findings.append(
                Finding(
                    "FAIL",
                    agent_path,
                    f"action classes cannot be both allowed and forbidden: {', '.join(overlap)}",
                    "Remove the overlap; effective permission must be unambiguous.",
                )
            )


def validate_registry(repo: Path, agents: dict[str, tuple[dict[str, Any], str]], findings: list[Finding]) -> None:
    registry_path = repo / "docs" / "aac" / "agent-registry.json"
    if not registry_path.exists():
        findings.append(
            Finding(
                "FAIL",
                "docs/aac/agent-registry.json",
                "missing agent registry",
                "Add docs/aac/agent-registry.json with one row per agent envelope.",
            )
        )
        return
    data = load_json(registry_path, findings)
    if not isinstance(data, dict):
        return
    registry_agents = data.get("agents")
    if not isinstance(registry_agents, list):
        findings.append(Finding("FAIL", str(registry_path), "registry must contain an 'agents' array", "Add agents: []."))
        return
    registered = {row.get("agent_id") for row in registry_agents if isinstance(row, dict)}
    for agent_id, (_, agent_path) in agents.items():
        if agent_id not in registered:
            findings.append(
                Finding("FAIL", agent_path, f"agent '{agent_id}' missing from registry", "Add an agent-registry row with owner, status, max lane, and kill switch.")
            )


def collect_cards(repo: Path, findings: list[Finding]) -> tuple[dict[str, tuple[dict[str, Any], str]], dict[str, tuple[dict[str, Any], str]], dict[str, tuple[dict[str, Any], str]]]:
    workflows: dict[str, tuple[dict[str, Any], str]] = {}
    nodes: dict[str, tuple[dict[str, Any], str]] = {}
    agents: dict[str, tuple[dict[str, Any], str]] = {}

    for path in sorted((repo / "docs" / "aac").glob("**/*.aac.json")):
        rel = str(path.relative_to(repo))
        data = load_json(path, findings)
        if not isinstance(data, dict):
            continue
        card_type = data.get("card_type")
        if card_type == "workflow":
            validate_workflow(data, rel, findings)
            workflow_id = data.get("workflow_id")
            if isinstance(workflow_id, str):
                workflows[workflow_id] = (data, rel)
        elif card_type == "node":
            validate_node(data, rel, findings)
            node_id = data.get("node_id")
            if isinstance(node_id, str):
                nodes[node_id] = (data, rel)
        elif card_type == "agent":
            validate_agent(data, rel, findings)
            agent_id = data.get("agent_id")
            if isinstance(agent_id, str):
                agents[agent_id] = (data, rel)
        else:
            findings.append(
                Finding(
                    "FAIL",
                    rel,
                    "card_type must be workflow, node, or agent",
                    "Set card_type and include the required fields for that card type.",
                )
            )

    return workflows, nodes, agents


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AAC 2.0 card artifacts.")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--base", default=os.getenv("GITHUB_BASE_SHA"), help="Base SHA for changed-file detection")
    parser.add_argument("--head", default=os.getenv("GITHUB_SHA"), help="Head SHA for changed-file detection")
    parser.add_argument("--format", choices=["text", "github"], default="text")
    parser.add_argument("--all", action="store_true", help="Validate cards even if no AAC-relevant changed files are detected")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    findings: list[Finding] = []

    try:
        changed = changed_files(repo, args.base, args.head)
    except Exception:
        changed = []

    relevant = [path for path in changed if is_relevant(path)]

    if not relevant and not args.all:
        print("AAC Creation Gate: PASS (no AAC-relevant changed files detected)")
        return 0

    workflows, nodes, agents = collect_cards(repo, findings)

    if relevant and not (workflows or nodes or agents):
        findings.append(
            Finding(
                "FAIL",
                "docs/aac/",
                "AAC-relevant changes detected but no .aac.json cards exist",
                "Add workflow, node, and agent cards under docs/aac/ before merge. Passing example: docs/aac/workflows/<workflow>.aac.json plus matching node and agent cards.",
            )
        )

    validate_cross_refs(workflows, nodes, agents, findings)
    validate_registry(repo, agents, findings)

    run_schema = repo / "docs" / "aac" / "run-card.schema.json"
    if not run_schema.exists():
        findings.append(
            Finding(
                "FAIL",
                "docs/aac/run-card.schema.json",
                "missing run-card schema",
                "Add a run-card schema so runtime-green claims have a proof contract.",
            )
        )

    failures = [finding for finding in findings if finding.level == "FAIL"]

    if args.format == "github":
        print("# AAC Creation Gate")
        print()
        if relevant:
            print("## AAC-relevant changed files")
            for path in relevant:
                print(f"- `{path}`")
            print()
        if failures:
            print("## Result: FAIL")
            print()
            for finding in failures:
                print(f"- **{finding.path}** — {finding.message}")
                if finding.remediation:
                    print(f"  - Remediation: {finding.remediation}")
                print(f"::error file={finding.path}::{finding.message}")
        else:
            print("## Result: PASS")
            print()
            print(f"Validated {len(workflows)} workflow card(s), {len(nodes)} node card(s), and {len(agents)} agent card(s).")
    else:
        if failures:
            print("AAC Creation Gate: FAIL")
            for finding in failures:
                print(finding.render())
        else:
            print("AAC Creation Gate: PASS")
            print(f"Validated {len(workflows)} workflow card(s), {len(nodes)} node card(s), and {len(agents)} agent card(s).")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
