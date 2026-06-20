Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Cyberball Task
Construct: social inclusion / ostracism / social exclusion
Rows/conditions:
- Inclusion: avatars continue to include the participant in toss circulation.
- Exclusion early: participant may receive initial tosses.
- Exclusion ostracism: avatars toss only to each other after the initial receives.

Timeline phases:
- Inclusion: Avatar turn (800-1200 ms; no response; avatar holds ball) -> Participant decision (2500 ms; press F=Player A / J=Player B; if participant holds ball) -> Toss animation (450 ms; no response; ball transfer) -> Post-toss gap (250 ms; no response)
- Exclusion early: Avatar turn (800-1200 ms; no response; initial avatar toss may go to participant) -> Participant decision (2500 ms; press F=Player A / J=Player B; if participant holds ball) -> Toss animation (450 ms; no response; ball transfer) -> Post-toss gap (250 ms; no response)
- Exclusion ostracism: Avatar turn (800-1200 ms; no response; avatars pass to each other) -> Participant decision (2500 ms; usually skipped; no participant hold) -> Toss animation (450 ms; no response; avatar-to-avatar transfer) -> Post-toss gap (250 ms; no response)

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per social context stage.
- Each row contains 4 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows participant-visible screen content only.
- Use simple circles for You, Player A, Player B, and the ball; do not draw people.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place condition labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 18-20% of the image.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, feedback, rewards, or timings.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- Preserve these exact terms where used: Inclusion, Exclusion early, Exclusion ostracism, You, Player A, Player B, F=Player A, J=Player B, 800-1200 ms, 2500 ms, 450 ms, 250 ms.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.
