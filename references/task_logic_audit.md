# Task Logic Audit: Cyberball Task (Williams & Jarvis, 2006)

## 1. Paradigm Intent

- Task: `cyberball`
- Primary construct: perceived social inclusion versus ostracism in a virtual ball-tossing interaction.
- Manipulated factors: block condition (`inclusion`, `exclusion`) controlling avatar toss policy toward participant.
- Dependent measures: tosses received by participant, tosses made by participant, response latency on participant turns.
- Key citations:
  - `W2048818633` (Williams & Jarvis, 2006, *Behavior Research Methods*)

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 2 (one inclusion block, one exclusion block).
- Tosses per block: fixed count from config (`trial_per_block`).
- Randomization/counterbalancing: block order follows configured conditions; avatar toss decisions are stochastic under inclusion and deterministic-after-threshold under exclusion.

### Trial State Machine (One Toss = One Trial)

1. `avatar_turn` (if current holder is avatar)
   - Onset trigger: `avatar_turn_onset`
   - Stimuli shown: three-player scene (participant bottom, two avatars top-left/top-right), ball at current holder, status line, wait prompt.
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after random avatar delay (`avatar_decision_delay` range).
   - Next state: `toss_animation`

2. `participant_decision` (if current holder is participant)
   - Onset trigger: `participant_turn_onset`
   - Stimuli shown: same three-player scene with participant decision prompt.
   - Valid keys: `[left_key, right_key]` (`f/j` by default).
   - Timeout behavior: if no key before `participant_timeout`, fallback target selected by policy (`no_response_policy`).
   - Next state: `toss_animation`

3. `toss_animation`
   - Onset trigger: `toss_start_to_participant` or `toss_start_to_left` or `toss_start_to_right`
   - Stimuli shown: ball motion from current holder to selected target, full scene remains visible.
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after `toss_animation_duration` plus optional `inter_toss_interval`.
   - End trigger: `toss_end`
   - Next state: next trial with updated holder.

## 3. Condition Semantics

- Condition ID: `inclusion`
  - Participant-facing meaning: participant remains included in passing interaction.
  - Concrete stimulus realization: participant appears as one of three nodes and repeatedly receives ball across the block.
  - Toss policy: avatars pass to participant with configured probability (`inclusion_receive_prob`, default ~0.33), otherwise to the other avatar.

- Condition ID: `exclusion`
  - Participant-facing meaning: participant is initially included, then ostracized.
  - Concrete stimulus realization: participant receives early tosses, then observes avatars passing only between each other.
  - Toss policy: participant receives first `exclusion_initial_receives` avatar-to-participant tosses, then avatars pass exclusively to each other.

## 4. Response and Scoring Rules

- Response mapping: `f` = toss to left avatar, `j` = toss to right avatar.
- Missing-response policy: no response within timeout triggers `participant_timeout`; target is selected via fallback policy and trial continues.
- Correctness logic: no correct/incorrect classification (social interaction paradigm, not speeded discrimination).
- Reward/penalty updates: no points/reward schedule; task tracks social exposure metrics instead.
- Running metrics:
  - per trial: holder before toss, holder after toss, participant turn flag, response key/timeout.
  - per block/task: participant received count, participant toss count, total toss count.

## 5. Stimulus Layout Plan

- Screen: game scene
  - Stimulus IDs shown together: `participant_node`, `left_node`, `right_node`, `participant_label`, `left_label`, `right_label`, `ball`, `status_line`, plus phase prompt.
  - Layout anchors (`pos`):
    - participant: bottom center (`0, -245`)
    - left avatar: upper-left (`-335, 180`)
    - right avatar: upper-right (`335, 180`)
    - status line: top center (`0, 300`)
    - prompt line: lower center (`0, -40` to `0, -45`)
  - Size/spacing:
    - player node radius: `58`
    - ball radius: `18`
    - labels and prompts sized for readability at `1280x720`.
  - Visual hierarchy:
    - current holder highlighted by yellow node border.
    - ball color distinct (yellow) from player nodes.
  - Readability checks: all labels and prompts are spatially separated from nodes and from each other.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `avatar_turn_onset` | 20 | avatar decision phase starts |
| `participant_turn_onset` | 30 | participant decision phase starts |
| `participant_choice_left` | 31 | participant chose left avatar |
| `participant_choice_right` | 32 | participant chose right avatar |
| `participant_timeout` | 33 | participant did not respond in time |
| `toss_start_to_participant` | 40 | toss animation starts toward participant |
| `toss_start_to_left` | 41 | toss animation starts toward left avatar |
| `toss_start_to_right` | 42 | toss animation starts toward right avatar |
| `toss_end` | 43 | toss animation finished |

## 7. Inference Log

- Decision: model each toss event as one trial for PsyFlow/TAPS logging.
- Why inference was required: the original Cyberball paradigm is continuous; TAPS requires auditable trial records.
- Citation-supported rationale: continuous three-player tossing is preserved while each toss transition is treated as a unit event.

- Decision: use deterministic ostracism after an initial receive threshold in `exclusion`.
- Why inference was required: papers describe manipulation conceptually (initial inclusion then exclusion), not one canonical numeric schedule.
- Citation-supported rationale: thresholded switch operationalizes the cited inclusion-then-ostracism manipulation while remaining configurable.
