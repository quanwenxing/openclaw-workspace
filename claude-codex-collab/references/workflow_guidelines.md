# Claude-Codex Collaboration Guidelines

## Reviewing Strategy (Codex)
When acting as a reviewer, Codex should look for:
- Logical errors and edge cases.
- Performance bottlenecks.
- Security vulnerabilities (SQL injection, XSS, etc.).
- Maintainability and code style (following project conventions).

## Feedback Loop (Claude)
Claude should receive feedback in a constructive summary:
- "The following issues were identified by the reviewer: [List]"
- "Please address these and provide the final updated code."

## Exit Criteria
The loop ends when:
1. Codex explicitly says "LGTM" (Looks Good To Me).
2. Codex identifies no critical issues.
3. The max loop count (default 3) is reached.
