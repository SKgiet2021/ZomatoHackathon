# 🔍 Problem Analysis: The "Food Ready" Dilemma

## 🧐 Why FOR Signals Fail (The Merchant Behavior Problem)

The fundamental flaw in the current Kitchen Prep Time (KPT) model isn't the algorithm; it's the data. Currently, the "Food Ready" (FOR) signal is highly unreliable.
Why? Because merchants often use it as a tool to summon riders rather than an honest status update.

**Example:**
At 12:15 PM, a merchant finishes cooking order #401. The food is packed and ready. However, the merchant knows that if they mark "Food Ready" now, the food might get cold before the rider arrives. Alternatively, they might mark it _early_ to ensure the rider is waiting outside when the cooking stops. The result? The FOR timestamp is tied to _rider proximity_, not _kitchen completion_.

## 🌪️ The Invisible Kitchen Rush Problem

A secondary issue is the "Invisible Rush". Zomato knows about Zomato orders, but the merchant's kitchen is serving Swiggy, dine-in, and direct takeaway simultaneously. When the KPT model predicts 18 minutes, it does so blindly, unaware that the kitchen is currently slammed with 40 offline orders.

## 🔗 The Downstream Impact Chain

1.  **The ML Model:** Learns from corrupt FOR timestamps, making future KPT predictions inherently flawed.
2.  **The Riders:** Arrive "on time" according to the app, but end up waiting 15+ minutes at the restaurant. This leads to frustration, lost earning potential, and "Rider Wait Time" penalties.
3.  **The Restaurants:** Angry riders crowd their dispatch area. Cold food leads to bad ratings.
4.  **The Customers:** Recieve wildly inaccurate ETAs. The app says "Rider waiting at restaurant" for 20 minutes, destroying trust and increasing order cancellations.
