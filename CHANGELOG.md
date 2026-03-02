# CHANGELOG

## [v0.1.3-dev] - 2026-03-02

### Changed
- Rebuilt `src/run_trial.py` from template leftovers to a Cyberball-native toss-event state machine (`avatar_turn -> participant_turn -> toss_animation -> inter_toss`).
- Wired shared `ball_state` holder continuity across block trials and aligned trial outputs with QA requirements (`from_player`, `to_player`, `participant_turn`, `participant_response`, `participant_received`).
- Updated `responders/task_sampler.py` to act on `participant_turn` semantics instead of template `target` phase behavior.
- Added config-first localization labels in `task.player_names` across all mode configs and consumed them at runtime.
- Replaced all reference artifacts with current contract-compliant schemas (`references.yaml`, `references.md`, `parameter_mapping.md`, `stimulus_mapping.md`, `task_logic_audit.md` with sections `## 1` to `## 8`).

### Fixed
- Added missing required `task.seed_mode` to all config profiles and aligned scripted-sim event log naming to contract expectations.

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
