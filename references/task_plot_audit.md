# Task Plot Audit

- generated_at: 2026-03-18T15:10:20+08:00
- mode: existing
- task_path: E:\xhmhc\TaskBeacon\T000034-cyberball
- workflow: manual redesign on top of inferred baseline

## 1. Inputs and provenance

- E:\xhmhc\TaskBeacon\T000034-cyberball\README.md
- E:\xhmhc\TaskBeacon\T000034-cyberball\config\config.yaml
- E:\xhmhc\TaskBeacon\T000034-cyberball\src\run_trial.py
- E:\xhmhc\TaskBeacon\skills\task-plot\scripts\task_plot_renderer.py

## 2. Runtime logic alignment (source -> plot)

- Core toss loop is aligned to `run_trial.py`: `avatar_turn` or `participant_turn` -> `toss_animation` -> optional `inter_toss`.
- Inclusion row is represented as a participant-involved cycle.
- Exclusion row is represented as early (participant still involved) and late (avatar-only passing) phases.
- Timing labels are aligned to config values:
- `avatar_decision_delay`: `800-1200 ms`
- `participant_timeout`: `2500 ms`
- `toss_animation_duration`: `450 ms`

## 3. Visual design decisions (manual)

- Replaced text-heavy screens with scene snapshots using `render_items`:
- three player nodes (`A`, `B`, `You`)
- highlighted holder/target ring
- yellow ball marker
- short prompt text per stage
- Kept two condition rows and four screens per row for readability.
- Reduced slope/overlap and enabled fixed width canvas for stable spacing.
- Circle fidelity fix applied in renderer to avoid ellipse distortion in non-square axes.

## 4. Renderer contract usage

- Spec root key: `task_plot_spec`
- Spec version: `0.2`
- Figure output uses `auto_width: false` to keep configured width (`width_in`) instead of auto-compaction.
- Shape rendering now supports multiple shapes per screen and circle/ring/dot with aspect compensation.

## 5. Render parameters (effective)

- output_file: `task_flow.png`
- dpi: `320`
- width_in: `14.0`
- auto_width: `false`
- screens_per_timeline: `4`
- screen_overlap_ratio: `0.06`
- screen_slope_deg: `12.0`
- screen_aspect_ratio: `1.50`

## 6. Output files and checksums

- E:\xhmhc\TaskBeacon\T000034-cyberball\references\task_plot_spec.yaml: sha256=fc1244e617438b295913bdb55fd34ffe5bf4fa36062ce0bc84848aa897f66cec
- E:\xhmhc\TaskBeacon\T000034-cyberball\references\task_plot_spec.json: sha256=4d462f20bf674a1dc8d0bb29cac6985cc7299486d0abc68e12d0f331e2dbfbcf
- E:\xhmhc\TaskBeacon\T000034-cyberball\task_flow.png: sha256=623bdb8d5174cdf83ae1fd712aefd982ba0a3ca4215f2c072224bb602ce4c9e8

## 7. Remaining uncertainty

- The plot uses representative snapshots rather than frame-accurate animation trajectories.
- Exclusion split is shown as early/late conceptual phases; exact switching threshold remains controlled by controller runtime policy.
