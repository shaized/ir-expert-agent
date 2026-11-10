# IR Expert Agent

**Structure the response decision before taking action.**

A model-agnostic AI agent skill paired with a working Python evidence tool. The skill guides an assistant's analysis; the deterministic tool validates and organizes a local evidence snapshot. The included demo runs offline with no API key or dependencies.

[Agent instructions](SKILL.md) · [Example report](example-report.md) · [Input contract](INPUT.md) · [Portfolio](https://shaized.github.io/)

## Try it in one minute

Requires Python 3.11 or newer.

```sh
git clone https://github.com/shaized/ir-expert-agent.git
cd ir-expert-agent
python3 agent.py example.json
python3 agent.py example.json --format json
python3 -m unittest discover -v
```

**Expected result:** A chronological observation record and one evidence-linked response proposal; no containment action is executed.

## Use it as an AI agent

Open the repository in an assistant that can read local files and run Python, then give it this request:

> Read SKILL.md and follow its workflow. Build a response decision brief from example.json. Explain what the observations support, what remains unknown and the tradeoffs of the proposed action. Keep all actions as proposals.

SKILL.md is the agent entry point. INPUT.md defines the evidence contract. agent.py performs the domain-specific analysis; runtime.py handles bounded JSON input, validation and report rendering. The assistant can explain the results, investigate alternatives and identify missing evidence using the tools you authorize.

The Python command itself is **not an LLM runtime**. It makes no network calls and performs no operational actions. There is no bundled model, production connector, autonomous service or implied access to your environment.

## What the agent does

1. Establish incident scope, current impact, decision owner and the authority already granted for response work.
2. Preserve original evidence and collection metadata. Use agent.py to validate references and create a chronological decision brief; do not claim that the helper establishes chain of custody.
3. Distinguish observations, hypotheses, confirmed facts and unknowns. For proposed containment, document the exact target, likely impact, owner, rollback and supporting evidence.
4. Support human decisions on containment, eradication and recovery. State verification and closure criteria. A recommendation does not imply permission to execute it.

## Design

```text
Selected evidence → validated local tool → traceable report
                                             ↓
                         AI-assisted reasoning → analyst decision
```

The examples are original, vendor-neutral implementations. All bundled data is fictional. Results retain unknowns and evidence gaps rather than presenting missing data as reassurance. Read the input contract for exact matching, thresholds and limitations.

## Validate and extend

The test suite covers the example, meaningful boundary cases, invalid evidence references where applicable, timestamp handling, bounded input and safe Markdown output. GitHub Actions runs the same offline tests. To add a real integration, produce the documented input shape in a separately reviewed adapter; keep credentials and operational evidence outside this repository.

Background: [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final). This project is an implementation example, not a compliance certification.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Use synthetic fixtures in issues and pull requests. This is a focused reference implementation; validate it against your data and review workflow before operational use.

## License

[MIT](LICENSE) · Built by [Shai Zaidenberg](https://github.com/shaized)
