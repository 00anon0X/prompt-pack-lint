# prompt-pack-lint

Lint AI prompt packs before publishing or sharing them.

It catches common issues in prompt libraries and agent instruction files:

- unresolved placeholders like `{{API_KEY}}`
- secret-like values such as API keys or passwords
- TODO/FIXME markers
- autonomous-agent prompts that lack a safety/guardrail section

## Install

```bash
pipx install git+https://github.com/00anon0X/prompt-pack-lint.git
```

## Usage

```bash
prompt-pack-lint prompts/
prompt-pack-lint system-prompt.md
```

Exit code is `1` when findings are present, making it usable in CI.

## Development

```bash
python -m pytest -q
python -m prompt_pack_lint.cli README.md
```

## License

MIT
