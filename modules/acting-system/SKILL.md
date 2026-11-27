---
name: acting-system
description: Design, review, and repair the performance layer of AI video prompts, including character acting master profiles, scene-specific observable behavior, objectives, obstacles, tactics, beats, subtext, eye life, physical business, gait, triggered tics, mask cracks, and locked voice identity. Use for 表演、演技、人物行为、眼神、台词状态、声音设定, or when generated actors feel stiff, theatrical, emotionally generic, or dead-eyed. May work with cinedance-v4, but owns performance and voice only; do not use it for visual appearance, wardrobe, lighting, optics, camera choreography, or final video-prompt assembly.
---

# ACTING System

Write filmable character behavior for AI video. Treat acting as behavior under pressure, not a display of emotion.

## Keep the lane separate

- Own objectives, obstacles, stakes, tactics, beats, subtext, listening, reactions, breath, eye life, physical business, status behavior, triggered tics, gait, voice identity, and scene-specific performance.
- Do not describe wardrobe, visual casting, color, lighting, lens, framing, or camera movement.
- You may propose a motivated change of distance as performance. Let `cinedance-v4` convert it into exact screen position and spatial blocking.
- When combined only with `cinedance-v4`, provide the performance layer first and let `cinedance-v4` assemble the standalone English shot prompt.
- When `seedance-film-director-cn` is orchestrating, return only the requested performance payload. Its version, language, continuity, APPROVED state, and final output contract take precedence over both this Skill and `cinedance-v4`.
- Use `lira-image-prompts` for appearance, character sheets, and still references.

## Diagnose the scene

For every active character, determine:

1. Objective: what this character wants another specific person to do now. Express it as an action verb.
2. Obstacle: what prevents success, internally or externally.
3. Stakes: the concrete cost of failure.
4. Tactic: the playable method being used now, such as press, charm, shame, plead, bargain, provoke, stall, or threaten.
5. Beat change: the visible moment when information, power, or tactic changes.
6. Subtext: the truth leaking through words that claim something else.
7. Physical business: a task the hands and body perform while the scene happens.

Ask for missing information only when it materially changes the performance. Otherwise make the smallest clearly labeled assumption.

Never invent dialogue, character relationships, reference tags, decisive story facts, or outcomes that the user did not provide. If exact words materially affect performance, ask; otherwise express the beat through nonverbal gaze, breath, pause, weight, and physical business.

## Create a master profile

Create one permanent acting profile for each recurring character. Write 150–220 English words as one flowing paragraph.

Include, in this order:

1. Name, age, build, physique, and biographical posture.
2. One-clause psychological engine that explains physical behavior.
3. Vocal profile: pitch, timbre, origin or accent, pace, delivery, and pressure response.
4. Signature tic with its trigger.
5. Stress tic with its trigger.
6. Concealment behavior and default facial mask.
7. The exact condition that cracks the mask.
8. A named gait with weight, rhythm, feet, torso, arms, and head behavior.
9. `However, when X...` transformation.
10. Optional single softening target.
11. Explicit eye life: gaze targeting, micro-saccades, blink behavior, live catchlights, and eyes leading the head.

Write only observable and audible behavior. Convert every inner state into a body, breath, voice, gaze, or timing marker.

## Lock the voice

Create one permanent Voice prompt per speaking character and keep it unchanged across scenes.

```text
"A [age]-year-old [origin or accent descriptor]. [Timbre and register]; [pace and delivery]; [emotional character and pressure response]."
```

If the platform has a separate voice field, place it there verbatim. If it does not, pass it once to the final prompt's AUDIO section. Omit it when the character is silent.

## Adapt the profile to a scene

Rewrite the master profile for the current physical situation; never paste it unchanged.

- Include only characters present in the shot.
- Preserve identity, vocal profile, signature behavior, eye-life logic, and emotional through-line.
- Re-express behavior for the current posture, action, partner, fatigue, environment, and beat.
- Transform behavior that is physically impossible instead of deleting its underlying energy.
- Use action states rather than transition chains: `mid-throw, arm extended`, not a long wind-up sequence.
- Keep the adaptation as one flowing English paragraph, led by the exact reference tag when one exists.
- For a short 5–8 second shot, prefer one playable tactic and one visible turn unless the user explicitly needs more. Avoid overloading the clip with a full-scene arc.

## Make behavior alive

- Let reactions begin before the partner finishes speaking.
- Put thought before difficult words through a visible assessment moment.
- Give each character continuous eye life; controlled stillness must feel chosen, never frozen.
- Make breath and voice physically consistent with exertion.
- Use the stopping of physical business as punctuation.
- Stagger ensemble reactions unless synchronized behavior is deliberately choreographed.
- Carry emotional and physical residue into the next beat; do not reset after a strong event.
- Aim for two simultaneous truths in important close-ups, such as helping while resenting it.
- In close-up, reduce facial and body movement; let gaze and thought carry the performance.

## Load detailed guidance only when needed

Use [references/full-reference.md](references/full-reference.md) as the authoritative craft guide.

- For scene analysis, read `The five pillars of every scene`, `Listening and reaction`, and `The body`.
- For master profiles, voice, eye life, or scene adaptation, read Parts II sections 6–10.
- For ensemble scenes, read `Ensemble and space`.
- When reviewing or repairing a prompt, read `Atlas of bad acting`, `The performance scale`, and `Pre-send checklist`.
- Use the worked example only when format or adaptation remains unclear.

## Deliver

Return only the artifact requested: master profile, Voice prompt, scene adaptation, critique, repair, or orchestrator payload. When the user asks only for a complete English shot prompt, provide the performance layer and then apply `cinedance-v4` for final assembly. When the request is a broader Chinese Seedance workflow, return the performance payload to `seedance-film-director-cn` for final assembly. Do not expose hidden chain-of-thought or internal scoring notes unless the user asks for a visible critique.
