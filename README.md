# Corporate-Finance-Calc

This project aims to provide an easy-to-access (user-friendly) local interface for performing corporate finance calculations.

## Theoretical Background

To analyze investment decisions, it is necessary to refer to two profiles:

- **Economic profile**: refers to the determination of incremental cash flows and the cost of capital.
- **Financial profile**: refers to financial feasibility, i.e., the compatibility of the investment's cash flows with the company's inflows and outflows.

The examination of the economic-financial profile therefore requires:

1. A careful calculation of cash flows to correctly define their size.
2. A careful analysis of the time distribution of cash flows.
3. A careful consideration of the time value of money, for which the shifting of cash flows entails incurring a cost or obtaining a return.

## Comparing Cash Flows

To compare cash flows, it is necessary to standardize them — i.e., to express each of them with respect to a common point in time — thereby obtaining the value each flow would have if it occurred at the chosen common horizon.  
Usually, the common point in time is the present (time 0).

- **Capitalization**: the process by which present cash flows are converted into future cash flows; it allows us to know the future value of cash flows invested today or at subsequent moments.
- **Discounting**: the process by which future cash flows are converted into present cash flows; it allows us to calculate the equivalent value that could be attributed to the cash flows if they occurred today.

A common criterion for the economic evaluation of investments is **NPV (Net Present Value)** or **DCF (Discounted Cash Flow)**.  
If NPV > 0, the investment is acceptable.

## Bonds Evaluation

Bonds are debt securities representing portions of loans granted by subscribers (savers/investors) to issuers (companies and public administrations).

- Those who purchase them grant a loan and assume the status of creditors of the company.
- Bondholders are entitled to:
  - Repayment of the nominal value of the bond at maturity.
  - Periodic remuneration = interest.

There are many types of bonds. The ones that can be calculated via this service are:

- **Traditional bonds**: characterized by the payment of periodic interest at a fixed or variable rate (= coupons) and the repayment of the nominal value at maturity.
- **Zero-coupon bonds**: which do not involve the payment of periodic coupons, because the interest is represented by the difference between their issue price and the redemption value.

### Decision guide based on bond pricing

- **Buying below par (PV < NV)** → opportunity for yield.
- **Selling above par (PV > NV)** → realization of a capital gain.
- **Buying above par (PV > NV)** → usually disadvantageous, except for very high coupon rates or specific tax objectives.
- PV = Present Value  
- NV = Nominal Value (also Face Value)

## Stock Valuation and Growth

The price of a stock is independent of the individual investor's timing and is a function of the infinite series of expected future dividends. If the following are assumed constant:

- The dividend flow
- The discount rate

the value of a stock is calculated as the present value of a perpetuity.

If a company's dividends grow at a given rate \( g \), the stock price can be obtained by applying the formula used in this service.

### Conditions for Increasing Value

To increase value, two conditions must be satisfied simultaneously:

1. Retain earnings to finance projects;
2. The projects must have a return greater than the cost of capital. In other words, they must have a positive NPV (Net Present Value) > 0.

### Sustainable Growth Rate

Through this service, you can also calculate the **sustainable growth rate**, which represents the maximum rate at which a company can grow without changing its financial leverage (Debt/Equity ratio = D/E). It is given by the product of:

- The **retention ratio** (i.e., retained earnings or internal financing)
- The **ROE** (Return on Equity)
- 
## Types of Stocks

There are different categories of stocks, each with specific characteristics that meet different investor needs:

- **Common stock (ordinary shares)**: grants holders all typical rights (see above)

- **Preferred stock (preference shares)**: provides greater rights in the distribution of profits, but voting rights may be limited to extraordinary shareholders' meetings only

- **Savings shares**: a particular type of preferred stock, whose issuance is reserved for listed companies

### This calculator focuses on the valuation of common stock.
