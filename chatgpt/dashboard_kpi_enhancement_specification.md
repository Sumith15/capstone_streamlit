# KPI Enhancement Specification for the Five-Page Streamlit Business Intelligence Dashboard

## 1. Purpose

This document specifies additional KPIs that can be incorporated into a
five-page Streamlit dashboard built on Odoo sales data. It is written
for another AI assistant or developer who needs to understand:

-   What each KPI measures and why it matters.
-   How to calculate it.
-   Which source data is required.
-   Where it belongs in the dashboard.
-   Important business rules and interpretation caveats.

The dashboard should help business users understand performance,
identify emerging risks, and decide where to intervene. Prefer KPIs that
lead to an action rather than metrics that merely repeat information
already visible in charts.

**Important:** The formulas below are proposed definitions. Confirm them
against the organisation's accounting rules, Odoo workflow, available
columns, and agreed business definitions before implementation. Do not
fabricate values when required data is unavailable.

------------------------------------------------------------------------

## 2. Dashboard design principles

1.  **Avoid KPI duplication.** A metric should have one primary home. It
    can be referenced elsewhere only when the context is materially
    different.
2.  **Show the period and comparison basis.** Label whether a KPI is
    current-month, year-to-date, trailing 12 months, or selected date
    range.
3.  **Use consistent revenue definitions.** Decide whether revenue means
    ordered, confirmed, invoiced, or paid sales. Do not mix these
    definitions across pages.
4.  **Make calculations traceable.** Display a tooltip or information
    icon with the formula, period, and key assumptions.
5.  **Handle missing data honestly.** Show "Not available" or "Requires
    data" rather than a made-up value.
6.  **Separate actuals, estimates, and predictions.** Forecasts, churn
    scores, and recovery opportunities must be labelled as estimates.
7.  **Use meaningful comparisons.** Where possible, show change versus
    the previous equivalent period and a trend.
8.  **Keep the KPI row selective.** Five to eight prominent KPIs per
    page is generally enough. Put secondary metrics in expandable
    sections or supporting charts.

------------------------------------------------------------------------

# Page 1 --- Executive Revenue Overview

## Page purpose

Give executives a fast view of overall commercial performance: revenue,
order activity, customer activity, and the direction of the business.

## Existing KPIs

  -----------------------------------------------------------------------
  KPI                                 Meaning
  ----------------------------------- -----------------------------------
  Total Revenue                       Revenue generated in the selected
                                      period, using the agreed revenue
                                      definition.

  Revenue Growth %                    Percentage change in revenue versus
                                      the comparison period.

  Total Orders                        Number of qualifying sales orders
                                      in the selected period.

  Average Order Value (AOV)           Average revenue generated per
                                      qualifying order.

  Active Customers                    Distinct customers with qualifying
                                      sales activity in the selected
                                      period.
  -----------------------------------------------------------------------

## Recommended additional KPIs

### 1. Revenue per Active Customer

-   **Purpose:** Shows how much revenue the business generates, on
    average, from each active customer. Helps distinguish customer-base
    growth from deeper monetisation of existing customers.
-   **Formula:** `Total Revenue / Active Customers`
-   **Required data:** Revenue and distinct active customer count for
    the same period.
-   **Interpretation:** Increasing revenue per customer may indicate
    stronger customer value or larger purchases. A decline may indicate
    smaller orders or a change in customer mix.
-   **Caveat:** Use the same revenue basis and period for numerator and
    denominator. Do not divide by all registered customers if the KPI is
    intended to describe active customers.

### 2. Average Revenue per Day

-   **Purpose:** Normalises revenue for the length of the selected
    period and makes comparisons between periods of different lengths
    easier.
-   **Formula:** `Total Revenue / Number of days in selected period`
-   **Required data:** Dated revenue transactions or a daily revenue
    aggregate.
-   **Interpretation:** Useful for monitoring the current sales run
    rate.
-   **Caveat:** Calendar-day revenue and business-day revenue are
    different measures. Choose one and label it. Partial periods should
    be compared with equivalent partial periods.

### 3. Revenue Forecast --- Next Month

-   **Purpose:** Provides an estimate of next month's revenue to support
    planning and early intervention.
-   **Formula:** No single universal formula. Use a documented
    forecasting method, such as a seasonal baseline, moving average, or
    time-series model.
-   **Required data:** Preferably 18--24 months of consistent monthly
    revenue; more history is useful where seasonality exists.
-   **Interpretation:** Present forecast revenue alongside a prediction
    interval or confidence range where possible.
-   **Caveat:** Label this as a forecast, not actual revenue or a
    guaranteed target. Do not generate a forecast from a handful of
    observations. Explain the method and refresh date.

### 4. Order Fulfilment Rate (conditional)

-   **Purpose:** Connects sales performance to operational execution by
    showing the proportion of orders successfully fulfilled.
-   **Formula:**
    `Fully Fulfilled Eligible Orders / Total Eligible Orders * 100`
-   **Required data:** Order status, delivery status, ordered quantity,
    delivered quantity, and relevant dates.
-   **Interpretation:** A low or declining rate may indicate stock,
    logistics, or operational problems.
-   **Caveat:** Define whether partially fulfilled orders count as
    fulfilled. Exclude cancelled or draft orders consistently. This KPI
    cannot be calculated reliably from sales-order data alone if
    delivery information is absent.

## Page 1 implementation priority

1.  Revenue per Active Customer --- high value and usually
    straightforward.
2.  Average Revenue per Day --- straightforward when revenue dates are
    available.
3.  Revenue Forecast --- valuable but requires sufficient history and a
    defensible model.
4.  Order Fulfilment Rate --- include only if delivery data is
    available.

------------------------------------------------------------------------

# Page 2 --- Customer Intelligence

## Page purpose

Explain customer value, customer mix, repeat behaviour, retention, and
customer geography. The page should help the business understand who its
customers are and how customer relationships contribute to revenue.

## Existing KPIs

  -----------------------------------------------------------------------
  KPI                                 Meaning
  ----------------------------------- -----------------------------------
  Total Customers                     Distinct customers in the defined
                                      customer population.

  New Customers                       Customers whose first qualifying
                                      purchase occurred in the selected
                                      period.

  Repeat Customers                    Customers with more than one
                                      qualifying purchase, under the
                                      chosen definition.

  Customer Lifetime Value (CLV)       Estimated or historical value
                                      generated by a customer over a
                                      defined relationship horizon.

  Retention Rate                      Percentage of customers from a
                                      starting cohort who remain active
                                      in a later period.
  -----------------------------------------------------------------------

## Recommended additional KPIs

### 1. Customer Acquisition Rate

-   **Purpose:** Measures the rate at which the business adds new
    purchasing customers.
-   **Formula:**
    `New Customers in Period / Customers at Start of Period * 100`
-   **Required data:** Customer first-purchase date and the customer
    population at the start of the period.
-   **Interpretation:** A rising rate can indicate successful
    acquisition. Interpret it alongside acquisition cost and customer
    quality if those are available.
-   **Caveat:** Do not use all registered contacts as the denominator
    unless that is the intended business definition. A customer created
    in Odoo is not necessarily a customer who has purchased.

### 2. Customer Churn Rate

-   **Purpose:** Measures the proportion of previously active customers
    who become inactive under a defined churn rule.
-   **Formula:**
    `Customers Churned During Period / Active Customers at Start of Period * 100`
-   **Required data:** Customer transaction history, period boundaries,
    and a documented inactivity/churn rule.
-   **Interpretation:** A rising rate signals deterioration in customer
    retention.
-   **Caveat:** Churn is not simply "no order this month." For
    businesses with irregular purchase cycles, define a suitable
    inactivity window (for example, based on the normal purchase
    frequency). Avoid counting newly acquired customers in the starting
    population.

### 3. Dormant Customers

-   **Purpose:** Counts customers who have not purchased within a
    specified inactivity window, helping teams identify reactivation
    opportunities.
-   **Formula:**
    `Count of customers where Current Date - Last Qualifying Purchase Date > Dormancy Threshold`
-   **Required data:** Customer ID, last qualifying purchase date, and
    an agreed threshold.
-   **Interpretation:** A growing dormant population may indicate
    weakening engagement or an opportunity for win-back campaigns.
-   **Caveat:** Make the threshold configurable or justify it using
    historical purchase frequency. Display the threshold in the KPI
    label or tooltip.

### 4. Purchase Frequency

-   **Purpose:** Shows how often active customers place orders.
-   **Formula (period-based):**
    `Qualifying Orders / Distinct Purchasing Customers`
-   **Alternative:** Average number of days between consecutive
    qualifying purchases per customer.
-   **Required data:** Order ID, customer ID, and order date.
-   **Interpretation:** Higher frequency can indicate stronger
    engagement, but it varies substantially by product and customer
    type.
-   **Caveat:** State which definition is used. Exclude cancelled,
    draft, or duplicate orders according to the agreed sales rules.

## Page 2 implementation priority

1.  Dormant Customers --- highly actionable for customer-success and
    sales teams.
2.  Customer Churn Rate --- valuable once churn is formally defined.
3.  Purchase Frequency --- useful behavioural context.
4.  Customer Acquisition Rate --- useful when the starting customer
    population is available.

**Avoid duplication:** Retention Rate already exists on this page. Do
not add another generic retention KPI. Customer Churn Rate is
complementary only if it has a clear, consistent definition.

------------------------------------------------------------------------

# Page 3 --- Product Intelligence

## Page purpose

Show which products and categories generate revenue, how demand changes
over time, and which products may need commercial or operational
intervention.

## Existing KPIs

  -----------------------------------------------------------------------
  KPI                                 Meaning
  ----------------------------------- -----------------------------------
  Total Product Revenue               Revenue attributed to products in
                                      the selected period.

  Total Units Sold                    Total quantity sold, using the
                                      agreed unit-of-measure rules.

  Average Selling Price (ASP)         Revenue divided by units sold.

  Fast Moving Products                Products with high sales velocity
                                      under a defined ranking or
                                      threshold.

  Slow Moving Products                Products with low sales velocity
                                      under a defined ranking or
                                      threshold.
  -----------------------------------------------------------------------

## Recommended additional KPIs

### 1. Gross Profit Margin

-   **Purpose:** Distinguishes products that generate high revenue from
    products that generate high profit.
-   **Formula:**
    `(Net Revenue - Cost of Goods Sold) / Net Revenue * 100`
-   **Required data:** Net sales revenue, product cost or COGS, and
    consistent cost valuation.
-   **Interpretation:** A high-revenue product with a low margin may be
    less attractive than a lower-revenue product with a strong margin.
-   **Caveat:** Do not calculate this from sales price alone. Confirm
    whether discounts, returns, taxes, and inventory valuation are
    included. If cost data is unavailable, mark the KPI as unavailable.

### 2. Product Revenue Growth Rate

-   **Purpose:** Identifies products gaining or losing commercial
    momentum.
-   **Formula:**
    `(Current Period Product Revenue - Previous Period Product Revenue) / Previous Period Product Revenue * 100`
-   **Required data:** Product-level revenue for comparable current and
    previous periods.
-   **Interpretation:** Positive growth indicates revenue expansion;
    negative growth may signal declining demand.
-   **Caveat:** Handle zero or negative previous-period revenue
    explicitly. Do not display infinite growth. Use a minimum revenue or
    volume threshold to avoid overreacting to tiny product baselines.

### 3. Product Revenue Dependency

-   **Purpose:** Measures how much total product revenue depends on the
    best-selling products.
-   **Formula:**
    `Revenue from Top N Products / Total Product Revenue * 100`
-   **Required data:** Product-level revenue and total product revenue
    for the same period.
-   **Interpretation:** A high percentage indicates dependence on a
    small product portfolio. This may create exposure if demand or
    supply changes.
-   **Caveat:** Define N (for example, top 5 or top 10) and keep it
    consistent. This overlaps with Page 5's strategic concentration
    analysis; Page 3 should use it only as a product-performance
    diagnostic, while Page 5 should provide the executive-level
    dependency view.

### 4. Product Sell-through Rate (conditional)

-   **Purpose:** Measures how much available inventory is sold over a
    period, helping identify products that are not converting stock into
    sales.
-   **Formula:** `Units Sold / Units Available for Sale * 100`
-   **Required data:** Units sold and inventory availability for the
    same period, with consistent treatment of replenishment and returns.
-   **Interpretation:** Low sell-through may indicate overstocking or
    weak demand. Very high sell-through may indicate stockout risk.
-   **Caveat:** A reliable sell-through calculation needs inventory
    movement or stock availability data. Do not substitute units sold
    divided by current stock; that is a different metric.

## Page 3 implementation priority

1.  Product Revenue Growth Rate --- directly supports product
    intervention.
2.  Gross Profit Margin --- strategically important if cost data is
    reliable.
3.  Product Revenue Dependency --- useful, but avoid duplicating the
    Page 5 executive KPI.
4.  Product Sell-through Rate --- include only with inventory history.

------------------------------------------------------------------------

# Page 4 --- Churn & Risk Analytics

## Page purpose

Identify customers who may stop purchasing, quantify the revenue exposed
to churn, and prioritise accounts for intervention. This page should
translate risk signals into an action list.

## Existing KPIs

  -----------------------------------------------------------------------
  KPI                                 Meaning
  ----------------------------------- -----------------------------------
  High-Risk Customers                 Number of customers classified as
                                      high risk by a documented risk rule
                                      or model.

  Revenue At Risk                     Revenue associated with customers
                                      classified as at risk.

  Average Churn Score                 Average model-generated churn
                                      probability or risk score for the
                                      defined population.

  Churned Customers                   Customers meeting the agreed
                                      historical churn definition.

  Recoverable Revenue                 Estimated revenue that may be
                                      retained or recovered through
                                      intervention, if supported by a
                                      calibrated model.
  -----------------------------------------------------------------------

## Recommended additional KPIs

### 1. Revenue at Risk %

-   **Purpose:** Puts exposed revenue into context by showing the share
    of total revenue associated with at-risk customers.
-   **Formula:** `Revenue At Risk / Total Revenue * 100`
-   **Required data:** Revenue attributed to at-risk customers and total
    revenue over the same period.
-   **Interpretation:** A rising percentage indicates increasing
    concentration of revenue in customers showing risk signals.
-   **Caveat:** Clearly define whether "revenue at risk" uses
    trailing-period revenue, forward expected revenue, or another basis.
    Use the same period and revenue definition in numerator and
    denominator. Do not add the full lifetime revenue of a customer to a
    current-period denominator.

### 2. Revenue Lost to Churn

-   **Purpose:** Quantifies historical revenue associated with customers
    who have churned.
-   **Formula (one possible definition):** Sum of the customers'
    expected baseline revenue for a defined post-churn period, or a
    clearly labelled historical revenue measure for customers who
    churned.
-   **Required data:** Customer purchase history, churn date/rule, and a
    baseline or comparison period.
-   **Interpretation:** Shows the financial impact of churn that has
    already occurred.
-   **Caveat:** This is not automatically equal to the last order value
    or lifetime revenue. Define the counterfactual/baseline method. If
    no defensible baseline exists, report a simpler clearly labelled
    measure such as "prior-period revenue from customers now classified
    as churned."

### 3. At-Risk Customer Revenue Share by Risk Level

-   **Purpose:** Shows how exposed revenue is distributed across high-,
    medium-, and low-risk customer groups.
-   **Formula:**
    `Revenue At Risk for Risk Band / Total Revenue At Risk * 100`
-   **Required data:** Customer risk band and customer revenue on a
    consistent basis.
-   **Interpretation:** Helps prioritise high-risk accounts with
    meaningful financial exposure.
-   **Caveat:** Risk bands need documented thresholds. A risk score is
    not automatically a probability unless the model has been
    calibrated.

### 4. Average Days Since Last Purchase

-   **Purpose:** Shows how long customers have been inactive, providing
    an interpretable behavioural signal alongside a churn score.
-   **Formula:** `Average(Current Date - Last Qualifying Purchase Date)`
    across the selected customer population.
-   **Required data:** Last qualifying purchase date for each customer.
-   **Interpretation:** A rising value may indicate weakening customer
    activity.
-   **Caveat:** Segment by customer type or normal buying cycle. An
    overall average can be distorted by customers who naturally purchase
    infrequently.

## Page 4 implementation priority

1.  Revenue at Risk % --- strong executive context for the existing
    Revenue At Risk KPI.
2.  Average Days Since Last Purchase --- interpretable and useful for
    sales action.
3.  Revenue Lost to Churn --- useful once the baseline definition is
    defensible.
4.  Risk-level revenue share --- useful if it adds clarity beyond the
    existing risk distribution chart.

**Model integrity requirement:** If churn scores are produced by a
predictive model, document training data, prediction date, target
definition, validation metrics, and score calibration. If they are
rule-based, call them risk scores or risk indicators---not predicted
probabilities.

------------------------------------------------------------------------

# Page 5 --- Strategic Business Insights

## Page purpose

Provide leadership with a cross-business view of concentration,
portfolio health, financial exposure, and intervention opportunities.
This page should answer: "Where are we vulnerable, what is the impact,
and what should we do?"

## Existing KPIs

  -----------------------------------------------------------------------
  KPI                                 Meaning
  ----------------------------------- -----------------------------------
  Top Customer Contribution %         Share of revenue generated by the
                                      highest-contributing customer or
                                      defined top-customer group.

  Top Product Contribution %          Share of revenue generated by the
                                      highest-contributing product or
                                      defined top-product group.

  Revenue Dependency Score            Composite or concentration measure
                                      showing reliance on a limited set
                                      of revenue sources.

  Critical Alerts                     Count of actionable alerts meeting
                                      documented severity rules.

  AI Generated Insights               Number of generated insights, or
                                      preferably a concise insight
                                      summary. This is not a financial
                                      KPI.
  -----------------------------------------------------------------------

## Recommended additional KPIs

### 1. Customer Dependency Index (HHI)

-   **Purpose:** Quantifies customer revenue concentration across the
    entire customer base rather than looking only at the top customer.
-   **Formula:**
    `HHI = Sum of (each customer's revenue share percentage)^2`
-   **Required data:** Revenue by customer for the same period.
-   **Interpretation:** A higher HHI indicates greater dependence on
    fewer customers. Track its trend over time.
-   **Caveat:** State whether shares are expressed as percentages
    (0--100, HHI up to 10,000) or fractions (0--1, HHI up to 1). Do not
    mix scales. Industry-specific thresholds should not be assumed
    without context.

### 2. Product Portfolio Health

-   **Purpose:** Summarises the balance between products growing,
    stable, and declining.
-   **Formula (count-based):**
    `Number of products with positive growth / Number of eligible products * 100`
-   **Alternative:** Show the percentages of eligible products in
    growing, stable, and declining groups.
-   **Required data:** Product revenue across comparable periods and a
    minimum activity threshold.
-   **Interpretation:** A declining share of growing products can signal
    portfolio weakness even when total revenue is rising.
-   **Caveat:** Define growth bands and exclude products with
    insufficient sales history. A count-based score treats small and
    large products equally; consider a revenue-weighted view as a
    companion chart.

### 3. Revenue Growth Sustainability Score

-   **Purpose:** Distinguishes consistent growth from growth driven by a
    one-off spike or highly volatile periods.
-   **Suggested design:** A transparent 0--100 composite score based on:
    -   Percentage of months with positive revenue growth.
    -   Revenue growth volatility.
    -   Consistency of growth across the selected historical window.
-   **Possible illustrative formula:**
    `Score = 100 * (0.5 * Positive Month Ratio + 0.5 * Stability Score)`,
    where `Stability Score` is a documented normalised measure that
    decreases as monthly growth volatility increases.
-   **Required data:** A sufficiently long monthly revenue series,
    preferably 12--24 months or more.
-   **Interpretation:** Higher scores indicate more consistent growth
    under the chosen formula.
-   **Caveat:** This is a custom management indicator, not a standard
    accounting metric. Document and validate the formula. Do not display
    a score until the normalisation method and treatment of seasonality
    are defined.

### 4. Revenue Recovery Opportunity

-   **Purpose:** Estimates the revenue that could potentially be
    retained or recovered by acting on at-risk customers.
-   **Formula:**
    `Sum of (Customer Revenue Baseline * Calibrated Recovery Probability)`
    for eligible at-risk customers.
-   **Required data:** Customer revenue baseline, risk information,
    intervention outcomes, and a calibrated recovery probability or
    defensible scenario assumptions.
-   **Interpretation:** Helps prioritise retention campaigns by expected
    financial value.
-   **Caveat:** This is an expected opportunity, not guaranteed revenue.
    If recovery probabilities are unavailable, show scenario ranges
    (conservative/base/optimistic) and label them as assumptions. Do not
    present the existing customer revenue as automatically recoverable.

### 5. Revenue Exposure from Top Customers

-   **Purpose:** Makes customer concentration tangible by showing the
    revenue amount dependent on the top N customers.
-   **Formula:** `Sum of Revenue from Top N Customers`
-   **Required data:** Revenue by customer for a consistent period.
-   **Interpretation:** Useful for scenario analysis: what portion of
    revenue is exposed if one or more major accounts reduce purchases?
-   **Caveat:** This overlaps with Top Customer Contribution %. Include
    it only if leadership benefits from seeing the absolute currency
    exposure alongside the percentage.

## Page 5 implementation priority

1.  Customer Dependency Index (HHI) --- stronger concentration
    measurement than a top-customer percentage alone.
2.  Product Portfolio Health --- reveals broad product momentum.
3.  Revenue Growth Sustainability Score --- valuable if the formula is
    transparent and history is sufficient.
4.  Revenue Recovery Opportunity --- potentially powerful, but only with
    calibrated probabilities or clearly labelled scenarios.
5.  Revenue Exposure from Top Customers --- optional because of overlap
    with existing contribution metrics.

------------------------------------------------------------------------

# 3. Recommended KPI shortlist

The following is a practical shortlist that adds insight without
overcrowding the dashboard.

  -----------------------------------------------------------------------
  Page                    Recommended additions   Priority
  ----------------------- ----------------------- -----------------------
  Page 1 --- Executive    Revenue per Active      High / conditional
  Revenue                 Customer; Average       
                          Revenue per Day;        
                          Revenue Forecast; Order 
                          Fulfilment Rate         
                          (conditional)           

  Page 2 --- Customer     Dormant Customers;      High / medium
  Intelligence            Customer Churn Rate;    
                          Purchase Frequency;     
                          Customer Acquisition    
                          Rate                    

  Page 3 --- Product      Product Revenue Growth  High / conditional
  Intelligence            Rate; Gross Profit      
                          Margin; Product Revenue 
                          Dependency;             
                          Sell-through Rate       
                          (conditional)           

  Page 4 --- Churn & Risk Revenue at Risk %;      High / medium
                          Average Days Since Last 
                          Purchase; Revenue Lost  
                          to Churn; Risk-level    
                          Revenue Share           

  Page 5 --- Strategic    Customer Dependency     High / conditional
  Insights                Index (HHI); Product    
                          Portfolio Health;       
                          Revenue Growth          
                          Sustainability; Revenue 
                          Recovery Opportunity    
  -----------------------------------------------------------------------

**Best additions to prioritise first:** Revenue per Active Customer,
Dormant Customers, Product Revenue Growth Rate, Revenue at Risk %, and
Customer Dependency Index (HHI). These create a useful chain from
performance to customer/product signals to business exposure.

------------------------------------------------------------------------

# 4. Data requirements and implementation mapping

The dashboard is expected to consume curated Gold-layer data from an
Odoo data pipeline. The precise table and column names must be
discovered from the actual Snowflake schema; the names below are logical
entities, not claims about existing physical tables.

  ----------------------------------------------------------------------------
  Logical Gold dataset    Example fields required      KPIs supported
  ----------------------- ---------------------------- -----------------------
  Revenue summary         date/month, revenue,         Page 1 revenue, growth,
                          order_count,                 AOV, revenue/day,
                          active_customer_count        forecast

  Customer sales          customer_id,                 Page 1
  aggregate               first_order_date,            revenue/customer; Page
                          last_order_date,             2 acquisition,
                          order_count, revenue, period frequency, dormant
                                                       customers

  Customer cohort /       customer_id, cohort_period,  Page 2 retention and
  activity                activity_period,             churn
                          active_flag, churn_flag      

  Product sales aggregate product_id, category_id,     Page 3 growth, ASP,
                          period, revenue, quantity,   units, dependency
                          previous_period_revenue      

  Product cost / margin   product_id, period,          Page 3 gross profit
                          net_revenue, cogs,           margin
                          gross_profit                 

  Inventory movement /    product_id, date,            Page 3 sell-through
  availability            opening_stock, receipts,     
                          closing_stock, units_sold    

  Customer churn risk     customer_id, score,          Page 4 risk KPIs and
                          risk_band, scoring_date,     risk distribution
                          model_version                

  Customer revenue risk   customer_id,                 Page 4 revenue at risk
                          revenue_baseline,            and risk share
                          revenue_at_risk, risk_band,  
                          period                       

  Customer concentration  customer_id, revenue,        Page 5 HHI and customer
                          revenue_share, period        exposure

  Product concentration / product_id, revenue,         Page 5 product
  health                  growth_rate, status, period  portfolio health

  Forecast output         forecast_period,             Page 1 forecast
                          predicted_revenue,           
                          lower_bound, upper_bound,    
                          model_version                

  Recovery scenario /     customer_id,                 Page 5 recovery
  model output            baseline_revenue,            opportunity
                          recovery_probability,        
                          expected_recovery_revenue,   
                          scenario                     
  ----------------------------------------------------------------------------

## Data engineering considerations

-   Use stable customer and product business keys, and ensure dimension
    changes are handled consistently.
-   Deduplicate replayed source records before aggregating revenue or
    order counts.
-   Handle late-arriving updates and cancellations so historical metrics
    can be restated consistently.
-   Use the correct order lifecycle status. Draft, cancelled, quotation,
    confirmed, invoiced, and paid records must not be mixed
    accidentally.
-   Handle returns, credit notes, discounts, taxes, and currency
    conversion according to the agreed revenue definition.
-   Use a consistent calendar and timezone for period boundaries.
-   Preserve historical snapshots where needed for cohort, churn, and
    trend analysis.
-   Avoid double-counting order lines when joining orders, customers,
    products, deliveries, or invoices.
-   Record the data refresh timestamp and the reporting period on the
    dashboard.

------------------------------------------------------------------------

# 5. Metric governance: definitions that must be agreed

Before implementation, document these decisions in a data dictionary:

1.  **Revenue basis:** Ordered, confirmed, invoiced, or paid revenue?
2.  **Order eligibility:** Which order statuses count? How are cancelled
    and partially delivered orders treated?
3.  **Customer identity:** How are duplicate contacts, merged customers,
    and parent/child accounts handled?
4.  **Active customer:** What qualifies as an active customer, and over
    what period?
5.  **New customer:** Is "new" based on record creation date or first
    qualifying purchase date? Prefer first purchase for sales analytics.
6.  **Repeat customer:** Does repeat mean more than one order ever, or
    more than one order within a defined period?
7.  **Churn:** What inactivity period or business rule defines churn?
8.  **Dormancy:** Is the dormancy threshold the same as the churn
    threshold? It does not have to be.
9.  **Risk bands:** What score thresholds define high, medium, and low
    risk?
10. **Top N:** How many customers or products are included in
    concentration metrics?
11. **Comparison periods:** Previous month, previous year, rolling
    period, or like-for-like dates?
12. **Currency and units:** How are multiple currencies and product
    units of measure standardised?

------------------------------------------------------------------------

# 6. Guidance for another AI assistant or developer

When modifying the Streamlit dashboard using this specification:

-   First inspect the available Gold tables, schemas, sample records,
    and existing dashboard calculations.
-   Map each KPI to real columns and validate the formula before coding.
-   Reuse existing curated Gold aggregates where possible; do not
    recalculate complex business logic inconsistently in the UI.
-   Keep business transformations in the data layer and use Streamlit
    primarily for presentation and interaction.
-   Do not invent source columns, table names, model outputs,
    thresholds, or example values as if they were real.
-   If a KPI's required data is missing, mark it as unavailable and
    explain the missing dependency.
-   Use consistent formatting: percentages for rates, currency for
    revenue, counts for customers/orders, and days for inactivity.
-   Provide comparison context (for example, previous period change)
    only when the comparison is valid.
-   Add tooltips with definitions and calculation windows.
-   Clearly label forecast, risk, and recovery estimates.
-   Avoid adding every suggested KPI to the primary KPI row. Select the
    strongest metrics and use charts or expandable detail for the rest.
-   Preserve the dashboard's existing five-page structure and visual
    language unless there is a strong usability reason to change it.

## Final design principle

The dashboard should tell a connected business story:

**Page 1:** Are we performing well?\
**Page 2:** Are we building valuable customer relationships?\
**Page 3:** Is our product portfolio healthy?\
**Page 4:** What could go wrong, and how much revenue is exposed?\
**Page 5:** Where should leadership act first?

A strong KPI is not merely measurable. It is understandable, trusted,
connected to a business decision, and supported by data that can be
traced back to the source.
