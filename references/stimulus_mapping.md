# Stimulus Mapping

Task: `Cyberball Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `inclusion` | `participant_node`, `left_node`, `right_node`, `participant_label`, `left_label`, `right_label`, `ball`, `status_line`, `avatar_wait_prompt`, `participant_prompt` | `W2048818633` | Three-player virtual ball-toss game with participant included in circulation. | `psychopy_builtin` | Avatar toss policy includes participant with configurable probability. |
| `exclusion` | `participant_node`, `left_node`, `right_node`, `participant_label`, `left_label`, `right_label`, `ball`, `status_line`, `avatar_wait_prompt`, `participant_prompt` | `W2048818633` | Three-player game with social exclusion manipulation after initial inclusion. | `psychopy_builtin` | Avatar toss policy transitions to avatar-only passing after configured initial receives. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye` | `W2048818633` | Shared task envelope screens for instructions, block transitions, and termination. | `psychopy_builtin` | Content is condition-agnostic and used across modes. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
