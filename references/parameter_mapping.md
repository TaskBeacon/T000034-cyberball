# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task.conditions | `task.conditions` | `['inclusion','exclusion']` | W2048818633 | Cyberball manipulation centers on socially inclusive versus ostracizing interaction blocks. | inferred | One condition token per block in current runtime design. |
| task.blocks_trials | `task.total_blocks`, `task.trial_per_block` | Human `2 x 30`; QA `1 x 8`; scripted sim `2 x 6`; sampler sim `2 x 10` | W2048818633 | Repeated toss events are needed within each social condition to induce social context. | inferred | QA/sim profiles shorten blocks for gate speed. |
| task.key_mapping | `task.left_key`, `task.right_key`, `task.key_list` | left=`f`, right=`j`, continue=`space` | W2107794155 | Participant turn requires binary target choice to left/right co-player. | inferred | Mapping remains config-defined for localization and device portability. |
| task.localization.player_names | `task.player_names` | participant=`You`, left=`Player A`, right=`Player B` | W2048818633 | Roles are stable and should be configurable for language localization. | inferred | Runtime consumes config labels for prompts and logs. |
| task.no_response_policy | `task.no_response_policy` | human/sim=`random`, qa=`left` | W2107794155 | Timeout handling must preserve trial progression during participant turns. | inferred | QA uses deterministic fallback for reproducible checks. |
| timing.avatar_delay | `timing.avatar_decision_delay` | Human `[0.8,1.2]`; QA/sim `[0.05,0.08]` | W2048818633 | Avatar decision delays preserve interactive pacing between tosses. | inferred | Sampled each avatar turn via controller RNG. |
| timing.participant_timeout | `timing.participant_timeout` | Human `2.5s`; QA/sim `0.45s` | W2107794155 | Bounded response windows support omission/event coding. | inferred | Timeout emits `participant_timeout` trigger. |
| timing.toss_animation | `timing.toss_animation_duration` | Human `0.45s`; QA/sim `0.05-0.06s` | W2048818633 | Ball-transfer epoch must be visible as an explicit toss event. | inferred | Toss onset trigger depends on destination player. |
| timing.inter_toss_interval | `timing.inter_toss_interval` | Human `0.25s`; QA/sim `0.02s` | W2048818633 | Brief pause separates consecutive toss events. | inferred | Implemented as `inter_toss` phase. |
| controller.inclusion_prob | `controller.inclusion_receive_prob` | `0.33` | W2048818633 | Inclusion blocks should maintain recurring participant receipt. | inferred | Used when avatar chooses toss target in inclusion. |
| controller.exclusion_schedule | `controller.exclusion_initial_receives` | `2` | W2463168384 | Exclusion paradigms commonly include brief initial inclusion before ostracism. | inferred | After threshold, avatar tosses stay between avatars. |
| trigger.turns | `triggers.map.avatar_turn_onset`, `triggers.map.participant_turn_onset` | `20`, `30` | W2107794155 | Turn-phase boundaries should be separately event-coded. | inferred | Mapped to `avatar_turn` and `participant_turn` phases. |
| trigger.participant_choice | `triggers.map.participant_choice_left`, `triggers.map.participant_choice_right`, `triggers.map.participant_timeout` | `31`, `32`, `33` | W2107794155 | Participant left/right choices and omissions are distinct behavioral events. | inferred | Emitted by `capture_response(...)` on participant turns. |
| trigger.toss | `triggers.map.toss_start_to_participant`, `triggers.map.toss_start_to_left`, `triggers.map.toss_start_to_right`, `triggers.map.toss_end` | `40`, `41`, `42`, `43` | W2048818633 | Toss trajectory endpoints and toss completion need explicit event markers. | inferred | Toss start code selected from destination player ID. |
