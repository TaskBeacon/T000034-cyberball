# Source Excerpt (Cyberball Task)

## Input Files
- README: E:\xhmhc\TaskBeacon\T000034-cyberball\README.md
- Config: E:\xhmhc\TaskBeacon\T000034-cyberball\config\config.yaml
- run_trial: E:\xhmhc\TaskBeacon\T000034-cyberball\src\run_trial.py

## Runtime Excerpt (phase order)

```python
if participant_turn:
    participant_phase = StimUnit(..., unit_label="participant_turn")
    set_trial_context(participant_phase, phase="participant_turn", ...)
    participant_phase.capture_response(keys=[left_key, right_key], duration=participant_timeout, ...)
else:
    avatar_phase = StimUnit(..., unit_label="avatar_turn")
    set_trial_context(avatar_phase, phase="avatar_turn", ...)
    avatar_phase.show(duration=avatar_delay, ...)

toss_phase = StimUnit(..., unit_label="toss_animation")
set_trial_context(toss_phase, phase="toss_animation", ...)
toss_phase.show(duration=toss_duration, ...)

if inter_toss_interval > 0:
    inter_toss = StimUnit(..., unit_label="inter_toss")
    set_trial_context(inter_toss, phase="inter_toss", ...)
    inter_toss.show(duration=inter_toss_interval)
```

## Config Excerpt (timing and keys)

```yaml
timing:
  avatar_decision_delay: [0.8, 1.2]
  toss_animation_duration: 0.45
  participant_timeout: 2.5
  inter_toss_interval: 0.25
task:
  left_key: f
  right_key: j
```

## Plot Mapping Note

- Final spec keeps two timeline rows (`inclusion`, `exclusion`) with four representative screens each.
- Screen visuals are manual `render_items` snapshots (nodes + ball + prompt), aligned to the runtime phases above.
- Exclusion row explicitly includes early participant-involved stages and late avatar-only stages for readability.
