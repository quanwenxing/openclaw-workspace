---
name: claude-codex-collab
description: Orchestrates a multi-agent coding workflow using Claude Code (Builder) and Codex CLI (Reviewer). Use when you need to: (1) Build complex features with built-in quality assurance, (2) Get code implemented by Claude and immediately reviewed/refined by Codex, (3) Create iterative implementation-review loops to minimize bugs and vulnerabilities.
---

# Claude-Codex Collaboration Skill

This skill allows OpenClaw to act as a conductor, coordinating `claude` and `codex` CLIs to deliver high-quality code through an "Implement-Review-Refine" cycle.

## Core Roles

- **Claude Code (Builder)**: Responsible for writing implementation code, fixing bugs, and generating tests. Runs in non-interactive mode (`--print`).
- **Codex CLI (Reviewer)**: Responsible for code review, security audits, and optimization suggestions. Provides feedback on Claude's output.
- **OpenClaw (Orchestrator)**: Manages the loops, context transfer, and final decision-making.

## Workflow

1.  **Initialize**: Create a work directory for the task.
2.  **Implementation (Claude)**: Direct Claude to implement the request.
3.  **Review (Codex)**: Pass the implementation to Codex with the original context for a critical review.
4.  **Refine (Claude)**: Summarize Codex's feedback and direct Claude to apply fixes.
5.  **Iteration**: Repeat steps 3-4 (default max 3 loops) until Codex gives a "LGTM" or no critical issues are found.

## Usage

When the user asks for a feature or a fix using both agents, follow this pattern:

```bash
# Initialize the orchestration logic
python3 scripts/orchestrator.py "<detailed_task_description>"
```

### Options

- **Review Focus**: You can append focus areas to the task description, e.g., "Add a login feature. Focus on security and performance during review."
- **Max Loops**: Adjusted in `scripts/orchestrator.py` if a longer refinement session is needed.

## Resources

- `scripts/agent-wrapper.sh`: Low-level CLI wrapper for `claude` and `codex`.
- `scripts/orchestrator.py`: Python script managing the implementation-review loop.
- `references/workflow_guidelines.md`: detailed tips for high-quality collaboration.

## Constraints

- Ensure `claude` and `codex` are available in the system PATH.
- Use `work/YYYY/MMDD-HHMM_<slug>` for output to maintain workspace isolation rules.
- Always provide the final output (RESULT.md) after the collaboration finishes.
