# Make-AI-Agents — Workspace Rules

## Purpose
This repo is a **build workspace** for AI agents and Gemini Gems. Agents and Gems are built here, then moved to their own dedicated repos when ready. This is not a deployable package.

## What this repo is NOT
- Not a Python package — no `__init__.py`, `setup.py`, `pyproject.toml`, or `requirements.txt` at root
- Not a monorepo — no shared imports between agent folders
- Not a deployment target — nothing here ships directly

## Structure
- `make_agent.md` / `make_agent.json` — agent definition template
- `make_agent_qc.md` / `make_agent_qc.json` — agent QC template
- `make_gems/` — Gem definition templates, QC tools, and compiled `.txt` instruction files
  - `gem_instructions/` — compiled copy-paste instructions for each Gem
- `update_agents/` — agent definitions built in this workspace
- `canvas_course_expert/` — example of a complex agent (already moved to its own repo)
- `qc_reports/`, `source_docs/` — supporting materials

## Rules
- **No `__init__.py` or init files anywhere** — agents are standalone, not importable modules
- **No root-level `requirements.txt`** — each agent carries its own dependencies when moved
- **No packaging or CI/CD config** — this is a drafting space, not a pipeline
- When an agent is complete, it moves to its own repo. The folder here can stay as a reference or be deleted.
- Gems compile to a `.txt` file in `make_gems/gem_instructions/` and a `.json` in `make_gems/`
