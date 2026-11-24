# 3 OPSEC tools
**Source:** Carter Perez · https://www.instagram.com/reel/DbavfO-xZoF/ · 2026-07-30

**What it actually shows** (tool names come from the screen; the reel doesn't say them):
1. **DeFlock** maps (deflock.me), a crowdsourced map of Flock license-plate cameras with routing that avoids them.
2. **Quad9 DNS** (9.9.9.9), which blocks known malicious domains and keeps DNS lookups away from your ISP.
3. **neko**, a self-hosted throwaway browser that runs in Docker and streams to you over WebRTC.

**Named things to verify:**
- `FoggedLens/deflock` is real (~1k stars), and so is `m1k1o/neko` (Apache-2.0, ~23k stars). Quad9 is a well-known nonprofit DNS service.
- Overclaims: changing your DNS stops the ISP from reading *DNS lookups*, but it can still see which sites you connect to by IP and hostname, unless you also use a VPN. neko needs a server running Docker.

**Engagement bait?** Yes ("Comment OPSEC"), but the tools are visible on screen.

**Verdict:** TOOL, not a skill. Quad9 is a free five-minute setting worth doing. DeFlock is a personal-privacy choice. neko only matters if you run a home server.
