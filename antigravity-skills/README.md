# 🦾 Custom Antigravity Agent Skills

This directory contains packaged, modular agent automation skills. Each folder inside this directory represents a reusable capability that can be loaded by agentic runtime executors.

---

## 📂 Skill Directory Structure

Skills must conform to the standard layout below:

```
antigravity-skills/
└── <skill-name>/
    ├── SKILL.md                 # Main instructions with YAML frontmatter (Required)
    ├── scripts/                 # Executable scripts or helpers (Optional)
    ├── examples/                # Example code or output formats (Optional)
    └── references/              # Detailed papers, schemas, or raw documents (Optional)
```

---

## 📝 Writing `SKILL.md`

Every `SKILL.md` file must contain a YAML frontmatter header detailing its metadata. This header is parsed by agent tools to match and load relevant instructions:

```markdown
---
name: your-skill-lowercase-slug
description: >-
  A clear, 1-2 sentence description explaining when an agent should trigger
  and execute this skill (e.g. "Use this skill when processing regulatory
  tax rates for VAT validation...").
---

# Your Skill Title

Detailed markdown instructions describing the step-by-step workflow, tool requirements,
rules, and error-handling steps. Keep the main body under 500 lines. Use 'references/'
for longer documentation.
```

---

## 🚦 Guidelines for Agent Skill Utilization

1. **Auto-Discovery:** Skills placed in this directory are loaded automatically by agent workspaces.
2. **Explicit Verification:** Before executing a skill's scripts, the agent must check that local prerequisites (like Python virtualenv packages) are synchronized.
3. **No Overwriting without Consent:** Active agents must not rewrite or delete shared skills without explicit user consent.
