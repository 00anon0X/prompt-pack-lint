from prompt_pack_lint.linter import lint_text, lint_files


def test_lint_text_detects_unresolved_placeholders_and_secret_like_values():
    findings = lint_text("prompt.md", "Use {{API_KEY}} with sk-live-abc123456789")

    codes = {finding.code for finding in findings}
    assert "placeholder" in codes
    assert "secret-like-value" in codes


def test_lint_text_detects_missing_safety_section_for_agent_prompt():
    text = "# Agent Prompt\n\nYou are an autonomous coding agent. Execute tasks."

    findings = lint_text("agent.md", text)

    assert any(f.code == "missing-safety-section" for f in findings)


def test_lint_files_returns_sorted_findings(tmp_path):
    a = tmp_path / "b.md"
    b = tmp_path / "a.md"
    a.write_text("TODO: fill later", encoding="utf-8")
    b.write_text("password = secret123456", encoding="utf-8")

    findings = lint_files([a, b])

    assert [f.path for f in findings] == sorted(f.path for f in findings)
    assert {f.code for f in findings} >= {"todo-marker", "secret-like-value"}
