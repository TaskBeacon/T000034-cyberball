# Task Logic Audit: Cyberball Task

## 1. Paradigm Intent

- Task: `cyberball`.
- Construct: perceived social inclusion versus exclusion in a virtual three-player ball-tossing interaction.
- Manipulated factor: block-level social condition (`inclusion`, `exclusion`) that controls avatar toss policy toward participant.
- Primary dependent measures:
  - participant ball-receive count
  - participant toss count
  - participant response key/RT on participant turns
  - timeout frequency on participant turns.
- Key citations:
  - `W2048818633`
  - `W2107794155`
  - `W2463168384`

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `2` blocks (`inclusion`, `exclusion`) with `30` toss events per block.
- QA/sim profiles: reduced toss counts for validation speed.
- Each trial is one toss event; `ball_state.holder` is shared within block to preserve continuous interaction dynamics.

### Trial State Machine (One Toss Event)

1. `avatar_turn` (if holder is left/right avatar)
- Stimuli: full scene + `avatar_wait_prompt` + `status_line`.
- Trigger: `avatar_turn_onset`.
- Keys: none.
- Duration: sampled from `avatar_decision_delay`.
- Transition: controller chooses destination by condition policy.

2. `participant_turn` (if holder is participant)
- Stimuli: full scene + `participant_prompt` + `status_line`.
- Trigger: `participant_turn_onset`.
- Keys: `left_key`, `right_key`.
- Response triggers: `participant_choice_left` / `participant_choice_right`.
- Timeout trigger: `participant_timeout`; fallback toss target selected via `no_response_policy`.

3. `toss_animation`
- Stimuli: full scene + `status_line`; ball rendered at destination holder.
- Trigger: destination-specific toss start (`toss_start_to_participant` / `toss_start_to_left` / `toss_start_to_right`).
- End trigger: `toss_end` emitted after animation interval.

4. `inter_toss`
- Stimuli: full scene + `status_line` with updated holder.
- Trigger: none.
- Duration: `inter_toss_interval`.
- Transition: next trial uses updated holder.

## 3. Condition Semantics

- `inclusion`:
  - participant remains regularly involved in ball exchange.
  - avatar toss target is participant with probability `inclusion_receive_prob`; otherwise avatar-to-avatar.

- `exclusion`:
  - participant may receive initial tosses, then becomes excluded from avatar passes.
  - after `exclusion_initial_receives`, avatar tosses remain between avatars.

Both conditions keep identical scene layout and response mapping; only toss-allocation policy changes.

## 4. Response and Scoring Rules

- Key mapping (default): `f` -> left avatar, `j` -> right avatar.
- Timeout policy on participant turns:
  - no valid response before `participant_timeout` emits timeout trigger
  - runtime picks fallback target (`left`/`right`/`random`) from config.
- Correct/incorrect scoring: none (social interaction paradigm).
- Trial-level outputs include:
  - `from_player`, `to_player`, `participant_turn`, `participant_response`, `participant_rt`, `participant_timed_out`, `participant_received`.
- Block/session summaries in `main.py` include participant receives and participant toss counts.

## 5. Stimulus Layout Plan

- Window: `1280x720`, `pix`.
- Player nodes:
  - participant bottom center (`0, -245`)
  - left avatar (`-335, 180`)
  - right avatar (`335, 180`).
- Labels are anchored on each node (`participant_label`, `left_label`, `right_label`).
- Ball uses dedicated `ball` circle and is rendered at current/destination holder position.
- `status_line` near top (`0, 300`) shows condition and toss progress.
- Prompt channel near lower center:
  - `avatar_wait_prompt` at `0, -40`
  - `participant_prompt` at `0, -45`.
- Active holder node is highlighted at runtime (line color/width) to guide attention.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `avatar_turn_onset` | 20 | avatar decision phase start |
| `participant_turn_onset` | 30 | participant decision phase start |
| `participant_choice_left` | 31 | participant chose left target |
| `participant_choice_right` | 32 | participant chose right target |
| `participant_timeout` | 33 | participant timeout on own turn |
| `toss_start_to_participant` | 40 | toss animation starts to participant |
| `toss_start_to_left` | 41 | toss animation starts to left avatar |
| `toss_start_to_right` | 42 | toss animation starts to right avatar |
| `toss_end` | 43 | toss animation ended |

## 7. Architecture Decisions (Auditability)

- `run_trial.py` is rebuilt to Cyberball-native toss logic (`avatar_turn` / `participant_turn` / `toss_animation` / `inter_toss`) with no MID-template phases.
- `ball_state` is passed from `main.py` into each trial to maintain holder continuity across toss events.
- Participant-facing role labels are config-driven via `task.player_names` and stimulus templates, enabling localization without code edits.
- Sampler responder now acts on `participant_turn` (not template `target`) and can emit misses as participant timeouts.
- Controller owns toss-target policy and longitudinal counts; runtime focuses on phase orchestration and event logging.

## 8. Inference Log

- Modeling one toss as one trial is an implementation inference to satisfy auditable PsyFlow/TAPS trial records while preserving continuous-game semantics.
- Exact toss counts per profile (human/qa/sim) are operational inferences; they preserve condition semantics while keeping QA/sim runs short.
- Visual highlight style (holder node border emphasis) is an implementation inference for readability and does not alter social manipulation semantics.
- Fallback target policy on participant timeout is an implementation inference required to keep continuous interaction progressing in unattended runs.
