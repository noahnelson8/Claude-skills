# 12 "hedge fund-level" trading strategy prompts (carousel)
**Source:** Stics AI · https://www.instagram.com/p/DZFkEp0DsfH/ · 2026-06-02

**What it actually shows:** 12 prompt templates: strategy generation, backtesting, risk-reward, market regime detection, multi-factor strategy, optimization, portfolio construction, trade setups, Monte Carlo simulation, drawdown analysis, macro strategy and "alpha detection".

**Named things to verify:** The catch is serious. "Backtest this strategy using 5–10 years of historical data" only works if Claude actually has the price data and runs code on it. Asked cold, it will write a plausible-looking table of Sharpe ratios and win rates that it made up. "Generate 3 high-probability trades based on current data" has the same problem. Tuning a strategy to past data (#6) is also the classic way to fool yourself (overfitting).

**Engagement bait?** Follow-bait only; the prompts are fully visible.

**Verdict:** SKIP. Not a skill, and risky as written. If you ever want to learn backtesting for coursework, the honest version is having Claude write Python that loads real data (e.g. from yfinance) and computes the metrics, so every number is reproducible. Not investment advice.
