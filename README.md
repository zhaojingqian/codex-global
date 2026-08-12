# Portable Codex globals

This private repository versions the portable part of `CODEX_HOME` so the same
global guidance and reusable workflows can be used on multiple machines.

## Tracked scope

- `AGENTS.md`: personal guidance applied globally by Codex.
- `agents/*.toml`: personal sub-agent role configuration.
- `skills/`: personal and explicitly installed skills.
- `.gitignore`, this README, and `bootstrap.sh`: repository safety and setup.

The repository intentionally excludes Codex-managed `.system` skills and all
other `CODEX_HOME` state, including authentication, authorities, configuration,
memories, sessions, automations, plugins, caches, logs, attachments, databases,
and generated artifacts. Keep the GitHub repository private; privacy is not a
substitute for checking diffs before every commit.

## Use on another machine

Install and start Codex once so its home directory exists. Then clone this
repository to a temporary directory and run the bootstrap script:

```bash
codex_sync_clone="$(mktemp -d)/codex-global"
git clone https://github.com/zhaojingqian/codex-global.git "$codex_sync_clone"
bash "$codex_sync_clone/bootstrap.sh"
```

The bootstrap checks every tracked path first. If a target file already exists
with different bytes, it prints the conflict and exits before creating Git
metadata or copying files. Matching files are retained and missing files are
copied. It never deletes or overwrites Codex state.

Restart Codex after the first bootstrap or after pulling changes so a new task
loads the updated global guidance and skill inventory.

## Routine updates

Review the portable diff from the Codex home directory:

```bash
git -C "${CODEX_HOME:-$HOME/.codex}" status --short
git -C "${CODEX_HOME:-$HOME/.codex}" diff
```

Stage only the exact guidance, role, or skill paths you intentionally changed;
then commit and push `main`. Do not use force-add to bypass `.gitignore`, and do
not run `git clean` in `CODEX_HOME` because ignored paths are live Codex state.

Skills installed or upgraded by a package manager appear as ordinary Git diffs.
Review those diffs before committing them. Codex-managed `.system` skills and
plugin-cache skills remain owned by Codex/plugin installation on each machine.
