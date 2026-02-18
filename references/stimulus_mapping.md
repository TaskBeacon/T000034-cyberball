# Stimulus Mapping

Task: `Cyberball Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `include` | `include_cue`, `include_target` | `W2107794155` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for INCLUDE; target token for condition-specific response context. |
| `exclude` | `exclude_cue`, `exclude_target` | `W2107794155` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for EXCLUDE; target token for condition-specific response context. |
| `observe` | `observe_cue`, `observe_target` | `W2107794155` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for OBSERVE; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
