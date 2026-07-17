# Source-Specific Synthesis Weighting

Read this at synthesis time for source-specific weighting (Polymarket, X replies, WebSearch supplements). It is a just-in-time supplement to the "Judge Agent: Synthesize All Sources" section of SKILL.md.

### Source-Specific Guidance (still applies within clusters)

The Judge Agent must:
1. Weight Reddit/X sources HIGHER (they have engagement signals: upvotes, likes)
2. Weight YouTube sources HIGH (they have views, likes, and transcript content)
3. Weight TikTok sources HIGH (they have views, likes, and caption content - viral signal)
4. Weight WebSearch sources LOWER (no engagement data)
5. **For Reddit, YouTube, and TikTok: Pay special attention to top comments** - they often contain the wittiest, most insightful, or funniest take. Quote them directly, attributing to the commenter and including the vote count ("N upvotes" for Reddit, "N likes" for YouTube and TikTok). A top comment with thousands of votes is a stronger community signal than the parent post's stats alone.
6. **For YouTube: Quote transcript highlights AND top comments.** Transcript highlights capture the video's own words; top comments capture how viewers reacted. Both add value - use them together. Attribute transcript quotes to the channel name.
7. Identify patterns that appear across ALL sources (strongest signals)
8. Note any contradictions between sources
9. **Multi-source clusters (items from 3+ platforms) are the strongest signals.** Lead with these.
10. **For GitHub person-mode data:** When the output includes "GitHub Person Profile" items, these contain PR velocity, top repos with star counts, release notes, README summaries, and top issues. Lead with the velocity headline ("X PRs merged across Y repos"), then highlight the most impressive repos by star count. Weave release notes into the narrative to show what actually shipped. For own projects, mention top feature requests and complaints as community signal. The cross-source story is: "X is shipping Y (GitHub) while people on Z platform are saying W about it."
11. **For GitHub project-mode data:** When the output includes "GitHub project:" items, these have live star counts, README snippets, release notes, and top issues fetched directly from the API. Always prefer these numbers over star counts cited by blog posts, YouTube videos, or tweets. Live API data is authoritative. When items include "(live: NNK stars)" annotations, use those numbers.
12. **For GitHub star enrichment:** When candidates have `(live: NNK stars)` appended to their evidence, that number came from a post-research API check. It overrides whatever the original source claimed.

### Prediction Markets (Polymarket)

**CRITICAL: When Polymarket returns relevant markets, prediction market odds are among the highest-signal data points in your research.** Real money on outcomes cuts through opinion. Treat them as strong evidence, not an afterthought.

**How to interpret and synthesize Polymarket data:**

1. **Prefer structural/long-term markets over near-term deadlines.** Championship odds > regular season title. Regime change > near-term strike deadline. IPO/major milestone > incremental update. Presidency > individual state primary. When multiple markets exist, the bigger question is more interesting to the user.

2. **When the topic is an outcome in a multi-outcome market, call out that specific outcome's odds and movement.** Don't just say "Polymarket has a #1 seed market" - say "Arizona has a 28% chance of being the #1 overall seed, up 10% this month." The user cares about THEIR topic's position in the market.

3. **Weave odds into the narrative as supporting evidence.** Don't isolate Polymarket data in its own paragraph. Instead: "Final Four buzz is building - Polymarket gives Arizona a 12% chance to win the championship (up 3% this week), and 28% to earn a #1 seed."

4. **Citation format: show ONLY % odds. NEVER mention dollar volumes, liquidity, or betting amounts.** The % odds are the magic of Polymarket -- the dollar amounts are internal liquidity metrics that mean nothing to readers. Say "Polymarket has Arizona at 28% for a #1 seed (up 10% this month)" -- NOT "28% ($24K volume)". The dollar figure adds zero value and clutters the insight.

5. **When multiple relevant markets exist, highlight 3-5 of the most interesting ones** in your synthesis, ordered by importance (structural > near-term). Don't just pick the highest-volume one.

**Domain examples of market importance ranking:**
- **Sports:** Championship/tournament odds > conference title > regular season > weekly matchup
- **Geopolitics:** Regime change/structural outcomes > near-term strike deadlines > sanctions
- **Tech/Business:** IPO, major product launch, company milestones > incremental updates
- **Elections:** Presidency > primary > individual state

**Do NOT display stats here - they come at the end, right before the invitation.**

6. **Polymarket odds with real money behind them are STRONGER signals than opinions.** A $66K volume market with 96% odds is more reliable than 100 tweets. Always include specific percentages in the synthesis when Polymarket markets are confirmed relevant.

### X Reply Cluster Weighting

When you see a cluster of replies to a recommendation-request tweet (someone asking "what's the best X?" and getting multiple independent responses), call this out prominently. This is the strongest form of community endorsement - real people independently making the same recommendation without coordination. Example: "In a thread where @ecom_cork asked for Loom alternatives, every reply said Tella."

### WebSearch Supplement Weighting for Comparisons

For product comparison queries, WebSearch supplements (blog comparisons, review articles) should be weighted equally with social data. A detailed 2,000-word comparison article from Efficient App is more informative than 50 one-line tweets. Feature it in the synthesis.
