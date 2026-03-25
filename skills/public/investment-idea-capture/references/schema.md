# investment-idea-capture schema v1

## idea record (`memory/investment_ideas.jsonl`)

```json
{
  "idea_id": "idea-20260301-004",
  "captured_at": "2026-03-01T19:40:00+09:00",
  "source_type": "user_thesis",
  "source_title": "string",
  "source_url": null,
  "hypothesis": "string",
  "markets": ["string"],
  "time_horizon": "短期〜中期",
  "candidate_strategies": ["string"],
  "unknowns": ["string"],
  "constraints": ["string"],
  "quant_assessment": {
    "feasibility": 0,
    "data_availability": 0,
    "testability": 0,
    "evidence_strength": 0,
    "crowding_risk": 0,
    "overall": 0
  },
  "status": "inbox",
  "next_actions": ["string"]
}
```

## review record (`memory/investment_reviews.jsonl`)

```json
{
  "reviewed_at": "2026-03-15T09:00:00+09:00",
  "idea_id": "idea-20260301-004",
  "decision": "keep",
  "reason": "string",
  "reopen_condition": null,
  "score_before": 58,
  "score_after": 63,
  "notes": "string"
}
```
