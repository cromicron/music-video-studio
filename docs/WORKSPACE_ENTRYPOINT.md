# Workspace entrypoint for a published Cloud setup

If the environment starts in `/workspace` rather than the repository root, retain its existing global instructions and append this scoped entry to `/workspace/AGENTS.md` during the supported environment setup flow:

> For the Mercy in Minor music-video studio, use `/workspace/music-video-studio` as the project root. Before substantive work, read that repository's `AGENTS.md` and `PROJECT_MEMORY.md`, then run `python3 tools/studio.py --refresh` from that root. Follow its session guide, preserving local work and reconciling relevant saved branches. Current facts belong in the repository records, not in this workspace pointer.

This is a pointer, not another copy of project state. If the checkout path changes, update it in the prepared setup. Preserve global user instructions. Publishing/republishing the environment and a genuinely new unseeded task are separate from writing this file. See [the researched setup and test](CLOUD_CONTINUITY.md).
