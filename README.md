# Cyberball Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Cyberball Task |
| Version | v0.1.1-dev |
| URL / Repository | https://github.com/TaskBeacon/T000034-cyberball |
| Short Description | Three-player virtual ball-toss paradigm for social inclusion and ostracism. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | English |
| Voice Name | en-US-AriaNeural (voice disabled by default) |

## 1. Task Overview

This task implements Cyberball as a three-player virtual ball game based on Williams & Jarvis (2006), with one participant and two avatars. Experimental manipulation is block-level social context:

- `inclusion`: avatars continue to involve the participant in toss circulation.
- `exclusion`: participant is initially included, then avatars toss only to each other.

Each toss event is logged as one auditable trial to satisfy PsyFlow/TAPS trial-level runtime contracts.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Block setup | Select current condition (`inclusion` or `exclusion`) and reset controller state. |
| 2. Toss loop | Run `trial_per_block` toss events using shared ball-holder state. |
| 3. Block summary | Show block feedback with participant receive/turn counts. |
| 4. Completion | Show final summary and save trial log CSV. |

### Trial-Level Flow

| Step | Description |
|---|---|
| `avatar_turn` | If an avatar holds the ball, show waiting scene for randomized delay and choose next holder by condition policy. |
| `participant_decision` | If participant holds the ball, capture `f/j` decision with timeout fallback policy. |
| `toss_animation` | Animate ball transfer to target holder and log toss outcome fields. |

### Controller Logic

| Component | Description |
|---|---|
| Toss policy | Inclusion uses probabilistic avatar-to-participant passing; exclusion switches to avatar-only passing after initial receives. |
| Block state | Tracks toss count and participant receives per block and globally. |
| Timeout fallback | On missed participant decision, target is selected by configured fallback policy. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `avatar_turn` | Avatar holds ball and decision latency is simulated. |
| `participant_decision` | Participant response window (`f/j`) when ball is at participant node. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `black` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Stimulus Group | Description |
|---|---|
| `participant_node`, `left_node`, `right_node` | Three-player scene nodes (participant bottom, avatars top-left/top-right). |
| `participant_label`, `left_label`, `right_label` | Player identity labels anchored to each node. |
| `ball` | Shared ball rendered and moved between holder nodes. |
| `avatar_wait_prompt`, `participant_prompt`, `status_line` | Phase prompt and block-condition status overlays. |
| `instruction_text`, `block_break`, `good_bye` | Entry, transition, and exit screens. |

### d. Timing

| Stage | Duration |
|---|---|
| avatar decision delay | uniform range from `avatar_decision_delay` |
| participant decision | `participant_timeout` |
| toss animation | `toss_animation_duration` |
| post-toss gap | `inter_toss_interval` |

## 4. Methods (for academic publication)

Participants engaged in a virtual three-player ball-toss task designed to manipulate perceived social inclusion versus ostracism. One block implemented inclusion dynamics and one block implemented exclusion dynamics. During participant-held ball states, participants selected toss targets via key responses (`f/j`), while avatar-held states followed condition-specific toss policies.

The implementation records one trial per toss event with explicit holder transitions, decision outcomes, timeout handling, and trigger-aligned phase context. This trialization preserves the continuous interaction character of Cyberball while enabling auditable event-level behavioral analysis.
