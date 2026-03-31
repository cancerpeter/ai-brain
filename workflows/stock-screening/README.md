# Daily Stock Screening Workflow

This workflow produces a daily Markdown report for A-shares, Hong Kong stocks, and U.S. stocks using market-based indicators instead of financial statement analysis.

## Goal

Identify medium- to long-term candidates worth further research based on:

- Trend strength
- Momentum confirmation
- Relative strength versus benchmark
- Volume and liquidity
- Volatility and drawdown control

## Input Scope

- Use the previous trading day's market data as the main evaluation point.
- Use enough historical daily data to compute technical indicators reliably.
- Cover three universes separately: A-shares, Hong Kong stocks, and U.S. stocks.

## Core Indicators

1. Trend
   - `MA20`, `MA60`, `MA120`
   - Price above `MA60` and `MA120`
   - `MA20 > MA60` preferred
2. Momentum
   - `RSI14`
   - `MACD`
   - 20-day and 60-day price change
3. Relative Strength
   - A-shares versus CSI 300
   - Hong Kong stocks versus Hang Seng Index
   - U.S. stocks versus S&P 500
4. Volume and Liquidity
   - Volume ratio versus 5-day and 20-day averages
   - Turnover when available
   - Daily traded value
5. Risk
   - Daily amplitude
   - 20-day annualized volatility
   - 60-day max drawdown

## Screening Logic

1. Exclude names with poor liquidity or obviously broken trends.
2. Score each stock using the rubric in [`SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md).
3. Rank each market independently.
4. Select the best candidates that have both trend confirmation and acceptable risk.
5. Write short reasons and risks for each selected stock.

## Output

- Folder: `/Users/peter.chen/Documents/知识库搭建/reports/stock-screening`
- Filename: `YYYY-MM-DD-stock-screening.md`
- Format: use [`TEMPLATE.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md)

## Git Workflow

After the report is written:

1. Stage the report file.
2. Commit with message: `YYYY-MM-DD 股票筛选更新`
3. Push to the configured `origin` remote on `main`.

