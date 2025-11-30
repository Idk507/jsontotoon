# json2toon

Convert JSON structures into **TOON** (Token-Oriented Object Notation) and generate **LLM-friendly prompts**.

`json2toon` helps you:

- Compress verbose JSON into a more token-efficient TOON format
- Keep data structure explicit and tabular where possible
- Wrap TOON data in ready-to-send prompts for LLMs
- Optionally parse TOON back into JSON

> ⚠️ Note: This project is **experimental** while the TOON ecosystem is still evolving.

---

## Features

- ✅ JSON → TOON conversion
- ✅ Optional TOON → JSON decoding (subset at first, extensible later)
- ✅ Smart analysis (primitive arrays, uniform object arrays, nested structures)
- ✅ Prompt helpers for LLM calls (code fences, instructions)
- ✅ Token cost comparison between JSON & TOON
- ✅ CLI tools:
  - `json2toon`
  - `toon2json`
  - `json2toon-report`

---

## Installation

```bash
pip install json2toon


json2toon/
├─ pyproject.toml
├─ README.md
├─ LICENSE
├─ src/
│  └─ json2toon/
│     ├─ __init__.py
│     ├─ config.py
│     ├─ core.py
│     ├─ encoder.py
│     ├─ decoder.py
│     ├─ analyzer.py
│     ├─ prompt.py
│     ├─ metrics.py
│     ├─ cli.py
│     └─ exceptions.py
└─ tests/
   ├─ __init__.py
   ├─ test_encoder.py
   ├─ test_decoder.py
   ├─ test_prompt.py
   └─ test_metrics.py
