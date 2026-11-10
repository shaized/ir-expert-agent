"""Build an evidence-linked incident response decision brief."""

from runtime import choice, cli, instant, report, rows, strings, text, unique, utc


def analyze(data):
    case_id = text(data.get("case_id"), "case_id")
    scope = text(data.get("scope"), "scope")
    evidence = rows(data.get("evidence"), "evidence")
    unique(evidence)
    evidence_ids = {item["id"] for item in evidence}
    timeline = []
    for item in evidence:
        timestamp = instant(item.get("timestamp"), "evidence.timestamp")
        timeline.append(
            {
                "id": item["id"],
                "timestamp": utc(timestamp),
                "source": text(item.get("source"), "evidence.source"),
                "observation": text(item.get("observation"), "evidence.observation"),
                "type": "reported_observation",
            }
        )
    timeline.sort(
        key=lambda item: (instant(item["timestamp"], "timestamp"), item["id"])
    )
    actions = rows(data.get("proposed_actions", []), "proposed_actions")
    unique(actions)
    proposals = []
    for action in actions:
        refs = strings(action.get("evidence_ids"), "action.evidence_ids")
        if not refs or not set(refs).issubset(evidence_ids):
            raise ValueError("every action needs known, nonempty evidence_ids")
        proposals.append(
            {
                "id": action["id"],
                "type": "proposal_only",
                "action": text(action.get("action"), "action.action"),
                "owner": text(action.get("owner"), "action.owner"),
                "impact": choice(
                    action.get("impact"), ["low", "medium", "high"], "action.impact"
                ),
                "rollback": text(action.get("rollback"), "action.rollback"),
                "evidence_ids": refs,
                "execution": "not_performed",
            }
        )
    gaps = strings(data.get("unknowns", []), "unknowns")
    return report(
        "IR Expert Agent",
        {
            "case_id": case_id,
            "scope": scope,
            "observations": len(timeline),
            "proposals": len(proposals),
            "unknowns": len(gaps),
            "disposition": "analyst_review_required",
        },
        timeline + proposals,
        gaps
        + [
            "Observations are supplied by the caller and have not been independently corroborated.",
            "The brief does not determine breach status, regulatory duties, incident closure or authorization to act.",
            "Evidence references are validated for existence, not for authenticity or chain of custody.",
        ],
        [
            "Validate the scope and preserve source evidence with collection metadata.",
            "Separate confirmed facts, hypotheses and unknowns in the incident record.",
            "Have the incident owner approve specific response actions through the established process.",
            "Define recovery verification and closure criteria before declaring the incident resolved.",
        ],
    )


if __name__ == "__main__":
    cli(analyze, __doc__)
