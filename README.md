# Cyberball Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Cyberball Task |
| Version | v0.1.1-dev |
| URL / Repository | https://github.com/TaskBeacon/T000034-cyberball |
| Short Description | Social inclusion and exclusion manipulation in virtual ball-tossing. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This task implements a Cyberball-style social interaction paradigm with three conditions: `include`, `exclude`, and `observe`. Each trial presents a social-context cue, a response window for ball-pass or observation response, and immediate feedback.

The implementation is structured for PsyFlow `human`, `qa`, and `sim` modes with explicit trigger events and trial-level logs suitable for behavior and synchronized acquisition.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Block initialization | `BlockUnit` prepares the condition sequence for each block. |
| 2. Trial execution | `run_trial(...)` runs cue, anticipation, target, and feedback stages. |
| 3. Block summary | Block-level response metrics and score are displayed. |
| 4. Task completion | Final cumulative score is displayed and saved. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Cue | Condition-specific social context cue (`include`/`exclude`/`observe`). |
| Anticipation | Brief fixation interval before response window. |
| Target | Participant chooses pass target or performs observation response. |
| Pre-feedback fixation | Short transition fixation stage. |
| Feedback | Response-confirmation feedback is shown. |

### Controller Logic

| Component | Description |
|---|---|
| Adaptive timing | Target duration is adjusted toward configured accuracy target. |
| Condition tracking | Hit/miss history is tracked by condition. |
| Scoring | Trial outcomes update the cumulative score. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `cue` | Social context cue stage. |
| `anticipation` | Pre-target waiting stage. |
| `target` | Active response window. |

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
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Stimulus Group | Description |
|---|---|
| `include_cue`, `exclude_cue`, `observe_cue` | Condition-specific social context cues. |
| `include_target`, `exclude_target`, `observe_target` | Response-window stimuli for pass/observe actions. |
| `*_hit_feedback`, `*_miss_feedback` | Condition-specific feedback screens. |
| `fixation`, `block_break`, `good_bye` | Shared fixation and summary screens. |

### d. Timing

| Stage | Duration |
|---|---|
| cue | 0.5 s |
| anticipation | 1.0 s |
| prefeedback | 0.4 s |
| feedback | 0.8 s |
| target | adaptive (`controller.min_duration` to `controller.max_duration`) |

## 4. Methods (for academic publication)

Participants completed a virtual ball-tossing paradigm manipulating perceived social inclusion and exclusion. Trial-level conditions (`include`, `exclude`, `observe`) were presented in blocks, and participant responses were recorded during a fixed target-response window.

The implementation used explicit stage-separated events (cue, anticipation, target, feedback) with trigger emission at key transitions. Condition-wise outcome tracking and adaptive response-window control were used to maintain task engagement and measurement stability.

All trials were logged with condition label, response status, and score delta for downstream behavioral and computational analyses.
