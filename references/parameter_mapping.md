# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.conditions` | `['inclusion', 'exclusion']` | `W2048818633` | `high` | Core manipulation in Cyberball is social inclusion versus ostracism. |
| `task.total_blocks` | `2` | `W2048818633` | `inferred` | Two-block structure operationalizes inclusion and exclusion contrasts. |
| `task.trial_per_block` | `30` | `W2048818633` | `inferred` | Fixed toss count per block for reproducible TAPS trial logging. |
| `task.left_key` | `f` | `W2048818633` | `inferred` | Left/right avatar target mapping for participant toss decisions. |
| `task.right_key` | `j` | `W2048818633` | `inferred` | Left/right avatar target mapping for participant toss decisions. |
| `timing.avatar_decision_delay` | `[0.8, 1.2]` | `W2048818633` | `inferred` | Provides naturalistic pacing during avatar turns. |
| `timing.participant_timeout` | `2.5` | `W2048818633` | `inferred` | Bounded participant decision window for consistent trial progression. |
| `timing.toss_animation_duration` | `0.45` | `W2048818633` | `inferred` | Supports visible ball-transfer event between player nodes. |
| `controller.inclusion_receive_prob` | `0.33` | `W2048818633` | `inferred` | Matches inclusion expectation in a three-player toss network. |
| `controller.exclusion_initial_receives` | `2` | `W2048818633` | `inferred` | Implements initial inclusion before ostracism in exclusion blocks. |
| `triggers.map.avatar_turn_onset` | `20` | `W2048818633` | `inferred` | Marks avatar decision phase onset. |
| `triggers.map.participant_turn_onset` | `30` | `W2048818633` | `inferred` | Marks participant decision phase onset. |
| `triggers.map.toss_start_to_participant` | `40` | `W2048818633` | `inferred` | Marks toss animation start toward participant node. |
| `triggers.map.toss_start_to_left` | `41` | `W2048818633` | `inferred` | Marks toss animation start toward left avatar node. |
| `triggers.map.toss_start_to_right` | `42` | `W2048818633` | `inferred` | Marks toss animation start toward right avatar node. |
