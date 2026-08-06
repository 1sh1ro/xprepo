# Return-blind mechanism seed library

This library is an ideation input, not a signal catalog, formula repository, or performance leaderboard. A seed card identifies a plausible causal channel, source terms, and data requirements; it contains no historical return, IC, Sharpe, parameter winner, or investability claim.

## Reusable upstream sources

| Source | What is reused | Boundary |
| --- | --- | --- |
| OpenSourceAP CrossSection / SignalDoc | Fundamental mechanism labels and field vocabulary | The upstream project is GPL-2.0. Do not vendor its code, data, or generated formulas here; retain only independent mechanism summaries and a source link. |
| Microsoft Qlib Alpha158 | Price/volume operator vocabulary and construction families | Qlib is MIT-licensed, but these are still hypotheses. Use only operators and fields available point-in-time on the target venue; no source backtest ranking is imported. |
| SEC EDGAR / venue documentation | First-party filing and event-timing definitions | These are data-contract sources, not evidence that an effect transfers to tokenized stocks. |

The project registry always overrides this library. A card whose nearest family is rejected is blocked unless a written retest condition is met or the new card has a distinct causal mechanism, independent field source, or venue.

## Seed selection

1. Load the JSON and set `returns_visible: false`.
2. Remove cards whose required fields cannot pass point-in-time, identity, and coverage checks.
3. Screen surviving cards against the rejected registry before formula design.
4. Select one card using causal fit, data feasibility, novelty, execution plausibility, and falsifiability only.
5. Run the debate sandbox. The chair can reject a card; it cannot tune it with returns.

At most one seed card and one independent blank-slate mechanism may feed a campaign. The blank-slate option prevents the library from becoming a closed menu; it must meet the same registry and preregistration rules.

## Permitted and forbidden transformations

Permitted transformations change the causal observation while preserving the prediction: for example, an independently timestamped filing event, a different first-party field that measures the same stated channel, or a venue-specific transmission measure.

Forbidden transformations are sign flips, nearby lookbacks, thresholds, rank weights, formula concatenation, and any change selected because historical results improved. Those are formula search, not seed mining.

## Governance

Add a card only with: source ID and URL, source terms, a causal chain, observable prediction, required fields, availability constraints, a token-transfer argument, nearest rejected families, novelty requirement, data status, and forbidden mutations.

Run:

    python3 scripts/validate_seed_library.py assets/seed-library-v1.json

before committing a seed update. The validator rejects visible performance fields and formula/parameter keys by design.
