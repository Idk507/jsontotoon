# Plan: Create agent.md documentation for json2toon

A comprehensive agent.md file to guide AI agents in understanding and implementing the json2toon library. This document will bridge the README's user-facing content with detailed technical specifications, architecture decisions, and implementation guidance needed for code generation.

## Steps

1. **Structure the agent.md with project context** — Include project purpose, TOON format rationale, token efficiency goals, and target use cases for LLM integration
2. **Document the planned architecture** — Detail each module from the README's structure (`encoder.py`, `decoder.py`, `analyzer.py`, `prompt.py`, `metrics.py`, `cli.py`, `config.py`, `exceptions.py`) with responsibilities, inputs/outputs, and interdependencies
3. **Define TOON format specification** — Specify conversion rules for JSON primitives, arrays, objects, and nested structures with concrete examples
4. **Add implementation guidelines** — Include Python coding standards, type hints strategy, error handling patterns, testing approach, CLI framework recommendations, and development priorities
5. **Provide API design patterns** — Outline public interfaces, usage examples, integration workflows with LLM systems, and token counting methodology

## Further Considerations

1. **TOON format details** — The README mentions TOON but doesn't define it. Should agent.md include a full TOON specification, or assume it's defined elsewhere? Recommend including core conversion rules with examples.
2. **Testing strategy depth** — Should agent.md specify exact test cases for encoder/decoder accuracy, or just general testing principles? Recommend including key test scenarios (primitive arrays, nested objects, edge cases).
3. **CLI framework choice** — Which Python CLI framework to recommend: argparse (stdlib), click (popular), or typer (modern)? Recommend typer for modern type hints and auto-documentation.
