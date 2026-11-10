# Input and output contract

## Input

The root requires case_id, scope and evidence. Each evidence item has unique id, timestamp with UTC offset, source and observation. Optional proposed_actions require unique id, action, owner, impact (low/medium/high), rollback and a nonempty evidence_ids list referring to supplied evidence. Optional unknowns is a list of strings. Actions are always emitted as proposal_only and not_performed.

See [example.json](example.json) for a complete fictional input. All demo identities, indicators, events, products and reputation providers are synthetic. Documentation IPs and example domains are not threat intelligence.

Input must be a UTF-8 JSON object no larger than 2 MiB. Duplicate JSON keys, malformed required fields, ambiguous timestamps and conflicting identifiers are rejected. Timestamps require an explicit UTC offset. Small local snapshots are the intended workload; there is no streaming, database or production connector in this version.

## Output

`python3 agent.py INPUT.json` emits Markdown. Add `--format json` for structured output. The JSON envelope contains schema_version, agent, summary, findings, limitations and next_steps. The tool writes to standard output and does not modify the source input. Input errors return exit code 2; a valid assessment returns 0 even when findings are present.

JSON preserves evidence text. Markdown renders evidence as literal escaped text, so input cannot inject links, headings or HTML into the report. Every result preserves substantive limitations.

## Example interpretation

A chronological observation record and one evidence-linked response proposal; no containment action is executed.

Background: [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final). This project is an implementation example, not a compliance certification.
