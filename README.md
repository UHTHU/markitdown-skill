# MarkItDown agent skill

A reusable agent skill for converting supported documents and files to Markdown with [Microsoft MarkItDown](https://github.com/microsoft/markitdown).

The skill covers setup, CLI and Python invocation, supported formats and their limits, verification, safety, OCR, and fallback guidance. It defaults to local conversion with plugins disabled. This repository contains skill instructions, not the MarkItDown library, and is not affiliated with Microsoft.

## Install in Codex

Clone into your personal skills directory (requires Git):

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/UHTHU/markitdown-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/markitdown"
```

If that destination already exists, review it before replacing or updating it. Start a new chat after installation if the skill is not yet listed. In other agents that support `SKILL.md`, place this repository in the agent's documented skill directory.

## Use

Ask the agent:

> Use $markitdown to convert this document to Markdown and check the extracted content.

The skill instructions are in [SKILL.md](SKILL.md). Install the MarkItDown package and required format extras in a separate Python environment as described there; cloning this repository does not install the converter.

## Verified sample

[Sample Word document](examples/markitdown-sample.docx) → [converted Markdown](examples/markitdown-sample.md).

Verified on 2026-10-26 with Python 3.13 and MarkItDown 0.1.9 using the `[docx]` extra:

- CLI file conversion, Python `convert_local()`, binary `convert_stream()`, and CLI stdin conversion produced matching content.
- Assertions checked the heading, Unicode text (`café` and `香港`), and a table row.
- The source file's SHA-256 hash was unchanged.
- The skill passed Codex skill-creator validation.

Other formats, OCR, cloud services, and third-party plugins were not tested. Markdown conversion may omit content or lose visual layout. Built-in audio transcription can send audio to Google; cloud extraction and LLM features also require appropriate data-transfer and cost authorization.

## Upstream

The format and API guidance was inspected against Microsoft MarkItDown 0.1.9, commit [`7482c092d9c0074a89803c9fdb63a969e7fe17fc`](https://github.com/microsoft/markitdown/tree/7482c092d9c0074a89803c9fdb63a969e7fe17fc). MarkItDown is a separate project distributed under its own MIT license. Check installed-version help and upstream documentation for changes.
