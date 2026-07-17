---
title: last30days skill-contract incident log (the forensics behind the output contract + LAWs 1-10)
date: 2026-07-17
category: docs/solutions/architecture
module: skills/last30days/SKILL.md
problem_type: design_decision
component: skill_contract
tags:
  - skill-contract
  - output-contract
  - context-engineering
  - incident-log
---

# last30days skill-contract incident log

These are the forensic incidents that motivated the `/last30days` output contract and LAWs 1-10. They have been relocated here, out of the runtime `skills/last30days/SKILL.md`, to cut context bloat: the contract had grown to ~37.7K tokens loaded on every invocation, and the model repeatedly failed to reach rules near the bottom of the file — the documented "I never reached line 1224" failure mode. The imperative rules stay in SKILL.md; the dated post-mortems that justify them live here for maintainers.

Each section below preserves the original narrative wording as it appeared inline in SKILL.md next to the LAW or Step it motivated.

## STEP 0 stale-clone self-check — the marketplaces/ stale-clone runs

Three 2026-04-22 test runs (Linear, Coinbase) loaded SKILL.md from `marketplaces/`, ran `--help` from the same stale path, did not see the `--competitors` flag that existed in the cache, and fell back to a manual comparison plan. Result: 2 of 3 windows never invoked the feature they were asked to test.

## SKILL CONTRACT — Named failure mode (2026-04-18 public v3.0.6 0/8 regression)

On 8 consecutive public invocations, Opus 4.7 treated `/last30days` as a generic research keyword and improvised. Every single run violated LAW 2 (invented titles like "The headline", "Kanye West: the last 30 days"), LAW 4 (section headers like "Why he is everywhere this month", "1. gstack dominates", "The 'Homecoming' peak"), or both. One run (Matt Van Horn) skipped Step 0.5 / Step 0.55 entirely and ran the engine bare with zero resolution flags. Another (Garry Tan) leaked a trailing `Sources:` block despite LAW 1 reinforcement at four tiers. Two runs (Peter Steinberger, Kanye vs Kim) landed on a stale `~/.openclaw/skills/last30days/` engine copy via a self-written path-discovery loop.

## SKILL CONTRACT — How v3.0.7 fixes it (the three structural anchors)

**How v3.0.7 fixes it:** three structural anchors.
1. **The MANDATORY first-line badge** (`🌐 last30days v{VERSION} · synced {YYYY-MM-DD}`) at the top of every response is the LAW 2 / LAW 4 enforcement anchor. See "BADGE (MANDATORY, FIRST LINE OF OUTPUT)" in the synthesis section.
2. **The SKILL_DIR substitution** in the engine Bash calls uses the directory of the SKILL.md the model just Read — no resolver list, no precedence walk. Whichever install the harness loaded SKILL.md from is the install whose engine runs. Aligns spec-with-code and works for any harness without enumerating its install path.
3. **This preface** tells you plainly: do NOT improvise. Follow SKILL.md top to bottom.

The 10/10 beta validation from 2026-04-18 and the 0/8 public v3.0.6 regression from the same day had THE SAME MODEL and SIMILAR SKILL.md CONTENT; the delta is the three anchors this release restores.

## OUTPUT CONTRACT — why the LAWs were hoisted to the top (v3.0.8)

These anchors used to live at line 1094 of this file. Three independent Opus 4.7 self-debugs on 2026-04-18 confirmed the file was too long to reach them before synthesis. Moved here in v3.0.8.

## BADGE MANDATORY — direct cause of the v3.0.6 section-header regression

The 2026-04-18 public v3.0.6 0/8 regression produced outputs with section headers like "The headline", "Why he is everywhere", "1. gstack dominates", "The 'Homecoming' peak". Direct cause: this anchor was absent.

## VOICE CONTRACT LAW — Peter Steinberger disaster #2 (stripped bold)

Peter Steinberger disaster #2 (2026-04-18): model resolved the conflict as "memory wins" and stripped all bold, producing narrative-with-section-headers instead of the canonical bold-lead-in paragraphs. Correct resolution: skill template wins inside skill output.

## LAW 1 — Peter Steinberger disaster #3 (verbatim WebSearch Sources reminder)

Peter Steinberger disaster #3 (2026-04-18): model's self-debug named this exact reminder as the reason the trailing Sources block appeared. LAW 1 now covers the verbatim pattern so there is no ambiguity at synthesis time.

## LAW 1 — post-synthesis self-check (the fourth tier)

Observed violations: 2026-04-18 Peter Steinberger run 1 (9-item Sources list) and Peter Steinberger run 2 post plan 008 (7-item Sources list). Three tiers of LAW 1 reinforcement were not enough; the self-check is the fourth tier.

## LAW 4 — Observed violation (2026-04-18, Peter Steinberger disaster #2)

**Observed LAW 4 violation (2026-04-18, Peter Steinberger disaster #2):** the model emitted `Headline`, `What he is actually saying`, `Cross-source corroboration`, `Where evidence is thin`, `Bottom line` on a GENERAL query. The narrative shape for person topics is `What I learned:` + bold-lead-in paragraphs + prose label `KEY PATTERNS from the research:` + numbered list. No blog-post subheadings.

## LAW 6 — Observed violation (2026-04-19, Hermes Agent Use Cases disaster)

**Observed LAW 6 violation (2026-04-19, Hermes Agent Use Cases disaster):** two consecutive `/last30days Hermes Agent (Actual) Use Cases` runs returned the raw `## Ranked Evidence Clusters` block verbatim as user output, with 8 cluster entries carrying `(score N, M items, sources: ...)` tuples and `- Uncertainty: single-source` lines. Root cause: the prior canonical-boundary text said "Pass through the lines ABOVE this boundary verbatim," which the model scoped broadly to include the scratchpad. The current boundary text and this LAW 6 scope pass-through to the PASS-THROUGH FOOTER block only. A third run on the same topic framed as "Hermes Workflows" produced the correct `What I learned:` prose synthesis, which is the shape every run must produce.

## LAW 7 — Observed violation (2026-04-19, Hermes Agent Use Cases Run 1)

**Observed LAW 7 violation (2026-04-19, Hermes Agent Use Cases Run 1):** the model called the engine bare with no `--plan`, no pre-flight handle resolution. The engine emitted a stderr warning ("No --plan and no LLM provider configured. Using deterministic fallback...") which the model read as a capability constraint ("I don't have a key, I can't do LLM stuff") instead of as what it actually was: a reminder that the reasoning model skipped its own planning step. The misread came from the word "provider" - the engine uses "provider" to mean "the key for the engine's INTERNAL planner," but the model parsed it as "I need a provider to plan at all." You do not. You ARE the provider. Run 2 of the same topic (2026-04-19, framed as "best workflows") with the same model and same cache generated the plan itself via `--plan` and produced clean results - the delta was this step.

## LAW 8 — Observed need (2026-04-20 inline-links saga, "I never reached line 1224")

**Observed LAW 8 need (2026-04-20 inline-links saga):** the citation rule existed in SKILL.md but was placed in the CITATION PRIORITY block around line 1224 - below the chunked-read window. Four consecutive test runs (Matt Van Horn, Peter Steinberger, Best Headphones, OpenClaw vs Hermes) confirmed the rule was deployed (diff IN SYNC, grep found the text) but was skipped on every synthesis because the model read lines 1-1000 and stopped. The model's own self-diagnosis, repeated verbatim four times: "I never reached line 1224." LAW 8 hoists the rule into the same guaranteed-loaded band as LAWs 1-7 so it enters context on every run. Same pattern that solved v3.0.6 (invented titles), disaster #2 (stripped bold), disaster #3 (trailing Sources), and the Hermes 2026-04-19 evidence-dump disaster.

## LAW 9 — Observed need (2026-06-17)

**Observed LAW 9 need (2026-06-17):** five consecutive runs (Kanye, Steinberger, Kevin Rose, Lan Xuezhao, Matt-vs-Trevin) shipped news-shaped reports that missed every funny comment, fabricated one citation URL, and leaked tooling meta-commentary - because the comment-weaving rule lived at line ~1189/1245, below the chunked-read window, and `## Best Takes` was empty (no in-subprocess fun scorer). The fix is two-part: the engine now always surfaces `## Top Community Comments` regardless of fun scoring, and this LAW hoists the weave-the-comments gate into the guaranteed-loaded band. Same hoist that fixed LAW 8.

## HOW TO INVOKE — Step 0.45 skip (2026-04-18 Birthday gift disaster)

Skipping Step 0.45 on a keyword-trap topic is the named failure mode of the 2026-04-18 "Birthday gift for 42 year old man" disaster: the engine ran on the literal phrase and returned 5 minutes of r/todayilearned / r/japannews / r/LivestreamFail noise because no human posts "I bought a 42 year old man a gift" on Reddit.

## HOW TO INVOKE — person-topic one-flag skip (Peter Steinberger disaster #2)

A person-topic command with ONLY `--x-handle` is the Peter Steinberger disaster #2 failure mode (2026-04-18): the model read the X-handle subsection literally, stopped there, and skipped the rest of the checklist. Result: weak Reddit targeting, no GitHub person-mode scoping, no related-voices enrichment, and a thin corpus. The fix is to read the Step 0.5 Pre-Flight Checklist FIRST and resolve every applicable flag before running the engine.

## Step 0.45 Class 1 — the Birthday gift run's actual output

The 2026-04-18 "Birthday gift for 42 year old man" run returned r/todayilearned, r/japannews crime posts, r/LivestreamFail drama - none about gifts.

## Step 0.5 Pre-Flight Checklist — stop-after-first-flag (Peter Steinberger disaster #2)

Reading only the "X handle" subsection and stopping there is the named failure mode of the Peter Steinberger disaster #2 (2026-04-18). The model admitted on debug: "I treated the 'X handle resolution' section as the full contract for pre-flight resolution and didn't --help the script to see what else existed."

## Step 0.5b — X handle without GitHub handle (Peter Steinberger failure mode)

Resolving the X handle but NOT the GitHub handle is the documented Peter Steinberger failure mode (2026-04-18).

## Step 0.55 Section 2a — category-peer miss (2026-04-22 GPT Image 2 failure)

Missing them is the 2026-04-22 `GPT Image 2` failure mode: the model resolved `r/OpenAI, r/ChatGPT, r/singularity, r/ChatGPTpromptengineering` (all OpenAI-brand) and missed `r/StableDiffusion, r/midjourney, r/dalle2, r/aiArt` where prompting techniques are actually shared. The user had to manually prompt "check image generation reddits too" to get a usable run.

The absence of the `(+ {category_id} peers)` annotation on a product-in-a-known-category topic is a Step 0.55 regression — the named 2026-04-22 failure mode.

## Step 0.75 disambiguation — collision-prone name (2026-06-17 Kevin Rose failure)

A bare collision-prone name as a subquery is the named 2026-06-17 failure mode — "Kevin Rose" returned 55 items with ~0 about the actual founder until every subquery was anchored to "Digg founder".
