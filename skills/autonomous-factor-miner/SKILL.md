---
name: autonomous-factor-miner
description: Design and run mechanism-first autonomous alpha-factor research with a return-blind seed library, role-based pre-return debate, preregistration, point-in-time data checks, rejected-factor screening, isolated evaluation, cost and multiplicity gates, and forward-only tracking. Use when the user asks an agent to autonomously discover, mine, test, reject, shortlist, or monitor quantitative factors, especially for tokenized U.S. stocks, RWA assets, or a tokenized-stock-factor-research workspace.
---

# Autonomous Factor Miner

Build falsifiable mechanisms before formulas. Use seed cards and role-specialized debate to improve causal logic and novelty before returns are visible. Give the agent autonomy to propose and reject hypotheses, never to tune repeatedly against final-test results.

## Select the task mode

- `ideas`: Return mechanism contracts only. Do not edit research code or run tests.
- `campaign`: Discover mechanisms, preregister a bounded candidate family, implement it, and run the staged evaluation.
- `evaluate`: Evaluate an already frozen proposal. Do not revise its formula, direction, thresholds, costs, or holding period.
- `forward`: Append only post-freeze observations to an existing watchlist. Do not rerun discovery or retune.

Default an autonomous mining request to `campaign`. Keep all work research-only or paper-only. Never place orders, sign transactions, connect a live account, or label a result `live_ready` unless the user separately authorizes a live-trading workflow.

## Load only relevant resources

- Read [references/research-contract.md](references/research-contract.md) before creating or evaluating a campaign.
- Read [references/tokenized-stock-adapter.md](references/tokenized-stock-adapter.md) when working in a tokenized-stock project.
- Read [references/debate-sandbox.md](references/debate-sandbox.md) for `ideas` or `campaign` work before selecting a mechanism. The sandbox must not receive return, IC, Sharpe, or backtest-result data.
- Read [references/seed-library.md](references/seed-library.md) and load [assets/seed-library-v1.json](assets/seed-library-v1.json) for `ideas` or `campaign`. Select by causal fit, data feasibility, and novelty only.
- Copy [assets/factor-campaign-template.json](assets/factor-campaign-template.json) to create a campaign manifest.
- Run `scripts/validate_seed_library.py assets/seed-library-v1.json` before changing seed cards and `scripts/validate_campaign.py` before freezing and before any final test.

## Run the workflow

### 1. Resolve the research root and runtime

Resolve the actual repository root and inspect its current status before changing anything. Preserve unrelated user changes. Lock an explicit `Asia/Shanghai` date and record absolute data coverage timestamps.

Determine the available universe, venue, interval, source fields, event timestamps, availability timestamps, execution-price fields, costs, and rejected-factor registry. If a required field is unavailable, narrow the mechanism or mark it `blocked_data`; do not invent a proxy silently.

### 2. Screen prior failures first

Query the rejected-factor registry before implementing code. Treat renamed formulas, sign flips, nearby windows, and small threshold changes as the same failed family unless the registry's stated retest condition is satisfied.

Record one of `new_mechanism`, `allowed_retest` (with condition), `blocked_prior_failure`, or `blocked_data`. Stop a blocked family before backtesting.

### 3. Choose a return-blind seed

For each campaign, select at most one seed card plus at most one independent blank-slate mechanism. A seed card is a causal scaffold, not an approved formula.

Do not select or rank seeds using historical returns, IC, Sharpe, published backtest results, factor popularity, or a prior winner's parameterization. Do not turn a seed into a nearby window, sign, threshold, or weighting change of a rejected family. Record the source ID, source terms, data-feasibility result, nearest registry family, and why the causal channel is distinct.

### 4. Debate mechanisms before returns

Run a closed `debate_sandbox` after registry screening and before designing formulas. Give agents source documents, seed-card mechanisms, registry mechanism summaries, field dictionaries, and availability metadata, but never candidate return results.

Use at least an Explorer, point-in-time Data Auditor, and Novelty Librarian. Add a Quality/Value Critic and Growth/Information-Diffusion Critic for fundamental or disclosure-event ideas. The chair must select, reject, or narrow a causal hypothesis using stated evidence—not a majority vote.

Preserve a compact debate packet containing seed lineage, strongest objection, nearest prior family, data blockers, and selection reason. A structural duplicate must lead to a different causal mechanism, not a tuning change.

### 5. Generate mechanisms, not a formula grid

Generate 3–8 mechanism briefs from the seed's economic, behavioral, information-diffusion, or market-structure logic. For every brief state:

- causal chain and observable prediction;
- why the effect could transfer to this market;
- alternative explanations and falsification conditions;
- required point-in-time fields and availability contract;
- expected holding horizon and executable entry constraint.

Rank briefs before returns using data feasibility, novelty versus the registry, tokenization-specific relevance, execution plausibility, and falsifiability. Advance only one mechanism family per campaign unless the user asks for independent parallel campaigns.

### 6. Preregister a bounded family

Translate the selected mechanism into one core factor and at most four defensible variants. Each must preserve the same causal prediction and state a robustness reason. Do not enumerate dense window, threshold, direction, or transform grids.

Freeze factor IDs and expressions; direction; universe and identity rules; signal, availability, entry, and execution rules; holding/rebalance rules; baseline and stress costs; chronological train/validation/purge/final-test boundaries; acceptance/rejection gates; retry conditions; and forward-tracking policy.

Validate and lock the manifest:

    python3 scripts/validate_campaign.py path/to/campaign.json --write-lock
    python3 scripts/validate_campaign.py path/to/campaign.json --require-frozen

Do not run the final test unless the frozen validation succeeds.

### 7. Implement point-in-time features

Implement only the preregistered family. Add checks proving rolling calculations do not cross assets; warmups are per asset; `available_at <= signal_time`; entries follow the frozen delay; missing/stale inputs do not become zero; costs use actual turnover; and factor direction matches the manifest.

A broken data or execution contract is `data_invalid`, not a weak factor.

### 8. Evaluate without test leakage

Use train only for implementation diagnostics. Use validation to choose at most one frozen variant. Do not view the final test while changing code or selection rules.

After selecting the validation winner, verify the manifest hash and run the final test once. Never revise the same campaign from final-test feedback. A later campaign must use a substantively new mechanism, data source, venue, or satisfied retest condition. Keep a return-feedback firewall: validation cannot reopen seed selection or the debate sandbox.

### 9. Apply gates and preserve outcomes

Require coverage/future-join checks, suitable IC or event statistics, monotonicity, non-overlap where needed, fold consistency, baseline/stress cost, a same-time null, concentration, BH-FDR across tried candidates, correlation/incremental value, and long-only feasibility when shorts are unavailable.

Write rejected, redundant, and invalid families to the machine-readable registry with scope, exact rule, sample, reason codes, evidence, decision, and retest conditions. For survivors, start forward-only scoring at or after `frozen_at` and preserve old state on refresh failure.

Use only: `rejected`, `redundant`, `data_invalid`, `exploratory`, `paper_candidate`, and `prospective_watch`. Historical success alone cannot produce `validated` or `live_ready`.

### 10. Report the campaign

Lead with the decision, not the best-looking return. Report mechanism and causal prediction; source/seed lineage; data/identity/availability contract; registry result; preregistration hash and variant budget; train/validation/test separation; gross and cost evidence; multiplicity/correlation/concentration/feasibility; debate objections; status; limitations; and next allowed action.

Never publish a site, start recurring monitoring, or perform external writes unless the user explicitly requests that additional action.
