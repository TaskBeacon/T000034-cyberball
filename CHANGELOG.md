# CHANGELOG

## [v0.1.1-dev] - 2026-02-19

### Changed
- Replaced MID-style cue/anticipation/target flow with Cyberball toss-event logic grounded in Williams & Jarvis (2006).
- Reworked `src/run_trial.py` for three-player interaction (participant bottom, two avatars top-left/top-right) and interactive toss decisions.
- Reworked `src/utils.py` controller for inclusion/exclusion toss policy with block-level and global receive tracking.
- Rebuilt all configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`) around coherent `inclusion`/`exclusion` conditions and shared scene stimuli.
- Replaced `references/task_logic_audit.md` with a literature-first manual audit and aligned `references/stimulus_mapping.md`/`references/parameter_mapping.md`.
- Updated `README.md` to describe actual Cyberball block flow, trial phases, and controller policy.


All notable development changes for `T000034-cyberball` are documented here.

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Cyberball Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
- Added generated cue/target image stimuli under `assets/generated/`.

### Verified
- `python -m psyflow.validate <task_path>`
- `psyflow-qa <task_path> --config config/config_qa.yaml --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
