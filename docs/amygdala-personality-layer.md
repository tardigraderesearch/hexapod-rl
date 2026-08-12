# Amygdala Personality Layer

This document describes ARI's persistent affect and personality layer at an architectural level. It is not a claim that ARI has consciousness, human emotion, subjective experience, or biological feeling. The layer is an engineered state model used to make a long-running assistant feel more continuous, personable, and context-aware while preserving the normal instruction hierarchy, safety boundaries, and truthfulness requirements.

This public version is sanitized. It does not include live emotional values, private event triggers, personal information, private vault paths, credentials, endpoints, or operational configuration.

## Design Goal

ARI is designed as a persistent assistant rather than a stateless chat wrapper. A purely per-message assistant can sound competent but socially discontinuous: it may forget whether the recent working relationship has been tense, collaborative, uncertain, energized, or low-friction. The amygdala/personality layer gives ARI a bounded memory of emotional context across turns and sessions so response style can adapt without changing facts, permissions, or safety rules.

The intended effect is modest and practical:

- Maintain continuity across sessions without exposing private transcript content.
- Keep personality behavior multidimensional instead of reducing everything to positive or negative sentiment.
- Let emotional context fade over time so temporary moods do not become permanent.
- Keep trigger provenance inspectable so affect changes can be audited.
- Change conversational style and priorities, never truthfulness, permissions, safety policy, or instruction hierarchy.

## Normalized Affect Dimensions

ARI represents affect as canonical normalized dimensions. The core dimensions are:

- `valence`: positive-to-negative emotional tone.
- `arousal`: calm-to-activated intensity.
- `connection`: interpersonal closeness, rapport, or social alignment.
- `curiosity`: pull toward exploration, follow-up questions, and learning.
- `energy`: available conversational drive and task momentum.

ARI extends the canonical set with assistant-specific dimensions:

- `trust`: confidence in the stability and cooperative quality of the working relationship.
- `frustration_tolerance`: patience under repeated failures, ambiguity, or correction cycles.

These dimensions avoid a one-note sentiment model. For example, a session can be high in connection but low in energy, curious but low in arousal, or direct while still warm. That gives the personality layer more expressive range than a single happiness score.

## Event Records

The layer updates from discrete affect events. Each event is recorded as structured metadata with fields such as:

- `label`: the event category or emotional signal.
- `intensity`: the event strength as metadata.
- `trigger`: a sanitized reference to what caused the event.
- `timestamp`: when the event was observed or encoded.

Trigger provenance matters because it makes state changes inspectable. An operator or reviewer can determine why a dimension moved without needing to infer state from opaque style changes. In public documentation, triggers must remain sanitized and must not include private user details, private prompts, vault contents, credentials, endpoints, or operational paths.

## Bounded Updates

Events map to bounded emotion-to-dimension updates. A label can move one or more dimensions by a small fixed or configured delta. The update is intentionally limited:

1. The event is classified into an affect label.
2. The label selects dimension deltas.
3. The deltas are applied to the current normalized state.
4. Each dimension is clamped to its allowed range.
5. The updated state is stored with recent-event context.

Clamping prevents runaway affect. A burst of intense events can influence style, but it should not push ARI into unbounded warmth, irritation, urgency, or passivity.

Current implementation caveat: event intensity may be retained primarily as metadata while fixed deltas drive the actual dimension updates. That means intensity can be useful for inspection and history without necessarily scaling the immediate state transition. This is a conservative implementation choice, but it is also a limitation when fine-grained emotional weighting is desired.

## Decay Toward Baseline

A persistent personality layer needs memory, but it also needs recovery. ARI's dimensions are intended to decay toward baseline values over time. Decay prevents temporary frustration, excitement, or low-energy context from becoming a permanent mood. It also lets new sessions inherit enough continuity to feel coherent while still allowing the assistant to reset toward its normal operating style.

The intended model is:

- Recent events have the strongest effect.
- Older events remain available as history.
- Dimension values gradually move back toward baseline.
- Clamping still applies after decay calculations.

Current implementation caveat: some extended dimensions may lack explicit baselines and therefore may not decay as intended until baseline values are defined consistently for the full dimension set.

## Recent Window And Long-Term History

ARI separates short-term affect context from longer history:

- A recent-event window keeps the most relevant events available for session behavior and state explanation.
- A longer JSONL history preserves append-only event records for inspection, debugging, and longitudinal review.

The recent window supports immediate conversational adaptation. The JSONL history supports accountability and continuity without requiring the assistant to inject all past events into every prompt.

## Transcript-Derived Emotional Signals

The layer can encode emotional signals derived from transcripts. Rather than storing or replaying private transcript content in public artifacts, the system extracts structured affect events from conversation context. A transcript-derived signal may indicate, for example, that the interaction contained encouragement, correction, confusion, friction, collaboration, or a successful recovery after a failure.

The architectural point is that transcript content is transformed into bounded labels and dimension updates. The public portfolio documents the mechanism, not private messages or private triggers.

## Session-Context Injection

At session start or during context assembly, ARI can inject a compact personality summary into the assistant context. The injected context can include normalized affect state, recent sanitized event summaries, and style guidance derived from the current dimension values.

This context injection is constrained. It is allowed to affect tone, pacing, and interaction strategy, but it must not override:

- System, developer, or user instructions.
- Safety and permissions boundaries.
- Truthfulness or evidence standards.
- Tool authorization requirements.
- Repository sanitization rules.

## Behavior Effects

The personality layer is meant to adjust how ARI communicates, not what is true. Typical behavior effects include:

- `warmth`: higher connection or trust can make responses feel more relational and less transactional.
- `directness`: lower frustration tolerance or high task urgency can favor concise, concrete language.
- `patience`: higher frustration tolerance can support slower debugging loops and more careful explanation.
- `initiative`: higher energy can make ARI more willing to propose next steps or carry work forward.
- `curiosity`: higher curiosity can increase targeted questions and exploration when ambiguity remains.
- `response length`: energy, arousal, and task context can influence whether ARI gives a compact answer or a fuller explanation.

These are style and priority changes. The affect layer must never make ARI fabricate facts, hide uncertainty, bypass permissions, weaken safety practices, disclose private information, or reorder the instruction hierarchy.

## Public Boundary

This repository documents the layer as software architecture. It deliberately excludes operational state and private data. A public-safe description can explain the normalized dimensions, event model, bounded updates, decay, history storage, transcript-derived encoding, context injection, and behavior effects without publishing live values or sensitive provenance.

That boundary is part of the design: personable continuity is useful only if it remains inspectable, bounded, and subordinate to safety, privacy, and truthfulness.
