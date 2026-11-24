# Claude Code + Unusual Whales options scanner
**Source:** Austin (AlgoX Trading) · https://www.instagram.com/reel/DYk6vQFjoBT/ · 2026-05-20

**What it actually shows:** Claude Code (shown on Windows) with the Unusual Whales MCP. A prompt scans the market for live options contracts and scores them out of 100 on unusual flow, volume, volume/OI, put/call skew, GEX, momentum and theta burn, then returns a top-10 table. He claims an SMCI call alert made +120% and his "small account" went from $500 to $3,800 in a week. The reel ends by pushing his paid Discord.

**Named things to verify:**
- The MCP is real: `unusual-whales/unusual-whales-official-mcp`. Unusual Whales is a paid market-data service.
- The scanner idea is plausible: Claude can call that data and rank it.
- The returns are cherry-picked and unverifiable, and the reel is an ad for a trading Discord.

**Engagement bait?** Yes. It's a funnel to a paid trading community.

**Verdict:** SKIP. Short-dated options on "unusual flow" are very high risk, and a scoring table doesn't make an edge. The technical bit (an MCP feeding live data into Claude) is a real, reusable pattern, already covered by how you use MCPs. Not investment advice.
