# fundingArbitrageML

Funding rate arbitrage is a market-neutral strategy that aims to capture the funding rate payments paid by perpetual futures traders. This repository provides the code and framework to automate this process, estimate profitability (after fees), and predict future funding rates using machine learning.

---

## Strategy Overview

Funding rate arbitrage can be performed both long and short, but to get started, we consider the following approach:

- **Buy the token on spot.**
- **Short the same amount in perpetual futures.**

This creates a **risk-neutral position**—your portfolio value does not change with the underlying price movement. You collect the funding rate paid by one side of the market (e.g., shorts), while your spot and futures positions offset each other in terms of price risk.

---

## Fees

- **Futures Fee:** 0.045%  
- **Spot Fee:** 0.1%  
- **Total Round-Trip Fee:** 0.29% (enter + exit on both spot and futures)

**Profitability Example:**  
If the funding rate is +29% annualized (shorts get paid 29%):

1. **Daily equivalent:**  
   29% / 365 ≈ 0.079% per day

2. **Breakeven Days:**  
   - Required to recover 0.29% in fees:
   - 0.29 / 29 ≈ 0.01 years → 3.65 days

So, you would need to hold the trade for at least 3.65 days at a constant 29% annualized funding rate to break even on fees.

---

## Machine Learning Approach

The machine learning part of this project is focused on predicting funding rates to make data-driven trading decisions.

- **Model Output Example:**  
  - “The average funding rate for _x_ days into the future will be _y%_.”
  - “We are _z%_ confident.”

This enables us to open arbitrage positions only if the model predicts that the funding payments will exceed our total fees over the holding period.

**Bonus:**  
We also aim to rank tokens by their likelihood to have high positive funding rates in the future. By identifying these tokens, we can apply our predictive ML model more efficiently, targeting only the most profitable opportunities.

---

## Challenges

- **Liquidation Risk:**  
  Using leverage on the futures position reduces capital needs but increases liquidation risk. To manage this:
  - If close to liquidation, close the futures leg at a loss, take profit from the spot, and use it to rebalance the short. This helps avoid liquidation but increases fees (estimated at 0.145% on moved assets).

- **Slippage & Execution Delay:**  
  Fast-moving markets can cause slippage and execution lag, possibly resulting in an uneven spot/futures position and reduced profits.

---

## Getting Started

_Coming soon: Instructions on environment setup, exchange API configuration, and running the model._

---

## License

MIT
