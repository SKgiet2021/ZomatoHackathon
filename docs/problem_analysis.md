# Problem Analysis: Why Kitchen Prep Time Prediction Fails

> A deep dive into the root causes of inaccurate KPT predictions and their downstream effects.

---

## 🎯 The Core Problem

Zomato's Kitchen Prep Time (KPT) prediction model has a fundamental flaw: **the training data is corrupted by dishonest FOR (Food Ready) signals**.

When a merchant marks an order as "Food Ready," they're supposed to do it when the food is actually prepared. But in reality, many merchants wait until the rider arrives to press that button. This creates a systematic bias in the data that makes the model think food takes longer to prepare than it actually does.

---

## 🔍 Why FOR Signals Fail

### The Merchant Behavior Problem

Let's walk through a real-world scenario:

**12:15 PM** - Kitchen finishes cooking the order. Food is actually ready.

**12:15 PM - 12:25 PM** - The rider is still 10 minutes away. The merchant sees this in the app.

**12:25 PM** - Rider arrives at the restaurant. Merchant presses "Food Ready" button.

**What the model sees:** "This order took 25 minutes to prepare."

**What actually happened:** The order took 15 minutes to prepare, but the merchant waited 10 minutes to mark it ready.

### Why Do Merchants Do This?

1. **No Incentive to Be Accurate** - There's no penalty for late marking, and no reward for accuracy
2. **Rider Location Visibility** - Merchants can see when riders are far away, so they delay marking
3. **Perceived Efficiency** - Some merchants think marking late makes them look busier/more popular
4. **Habit** - It's just how they've always done it

### The Numbers

Our research shows that **only 60% of FOR signals are accurate**. That means 4 out of 10 orders have corrupted timestamps. When you're training an ML model on millions of orders, that's a massive amount of noise.

---

## 🌊 The Invisible Kitchen Rush Problem

Here's another issue: the model has no idea when a kitchen is actually busy.

### Current State

- The model sees: Order placed at 12:00, marked ready at 12:25
- The model thinks: "This restaurant takes 25 minutes on average"
- The reality: It's lunch rush, they had 15 orders in queue, and the actual prep time was 18 minutes

### Why This Matters

During peak hours (12-2 PM lunch, 7-9 PM dinner), kitchens are slammed. But the model doesn't know that. It just sees longer prep times and assumes that's normal for that restaurant.

**Example:**

| Time     | Orders in Queue | Actual Prep Time | Marked Prep Time                   |
| -------- | --------------- | ---------------- | ---------------------------------- |
| 11:30 AM | 2               | 12 min           | 15 min (rider arrived late)        |
| 12:30 PM | 15              | 18 min           | 28 min (rider arrived late + rush) |
| 2:30 PM  | 3               | 11 min           | 14 min (rider arrived late)        |

The model learns: "This restaurant takes ~19 minutes"

But the truth is: "This restaurant takes 12-18 minutes depending on rush, plus riders wait 3-10 minutes"

---

## ⛓️ The Downstream Impact Chain

The corrupted FOR signals create a cascade of problems:

### 1. Riders Wait Longer

```
Before: Rider arrives at 12:25, food actually ready at 12:15
        Rider waits 10 minutes doing nothing
After:  Rider arrives at 12:25, food marked ready at 12:15
        Rider picks up immediately
```

**Impact:** Riders complete fewer orders per hour, earn less, get frustrated.

### 2. Customers Get Wrong ETAs

```
Model predicts: "Your food will arrive in 45 minutes"
Reality: Food was ready 10 minutes ago, rider is waiting
Customer sees: "Why is my food taking so long when it's already prepared?"
```

**Impact:** Customer complaints, lower NPS, order cancellations.

### 3. Restaurants Lose Efficiency

```
Kitchen finishes order at 12:15
Food sits getting cold until 12:25
Customer receives cold food
Customer leaves bad review
```

**Impact:** Lower ratings, fewer orders, revenue loss.

### 4. The ML Model Gets Worse Over Time

```
Training Data: Corrupted timestamps
    ↓
Model Training: Learns wrong patterns
    ↓
Predictions: Overestimated prep times
    ↓
More riders arrive late
    ↓
More corrupted timestamps
    ↓
Model gets worse over time
```

**Impact:** A negative feedback loop that makes the problem worse.

---

## 📊 The Scale of the Problem

Let's put some numbers on this:

| Metric                  | Current State | Impact                              |
| ----------------------- | ------------- | ----------------------------------- |
| FOR Accuracy            | 60%           | 40% of training data is corrupted   |
| Avg Rider Wait          | 12.3 min      | ~3-4 minutes of unnecessary waiting |
| Orders with 5+ min wait | 42%           | Nearly half of all orders           |
| Daily Orders (India)    | ~3 million    | 1.2 million orders have wait issues |

---

## 💡 Why Previous Solutions Failed

### Why Not Just Ask Merchants to Be Honest?

- No enforcement mechanism
- No incentive for accuracy
- Competing priorities (merchants focus on food quality, not data accuracy)

### Why Not Use Rider Arrival Time?

- That's what we're currently doing, and it's wrong
- Rider arrival ≠ Food ready

### Why Not Use Kitchen Sensors?

- Too expensive for small restaurants (dhabas, street food)
- Requires hardware installation at scale
- Maintenance nightmare across 300,000+ merchants

---

## 🎯 The Solution: Incentivize Accuracy

Our approach is simple: **make it in the merchant's best interest to mark accurately.**

1. **Show rider location** - Merchants see real-time rider ETA
2. **Score accuracy** - Dashboard shows how accurate they've been
3. **Reward accuracy** - Priority routing, lower commission, badges
4. **Verify bottom performers** - Barcode verification for the worst 5%

This creates a positive feedback loop:

```
Accurate marking → Better model → Better predictions → Riders arrive on time
    ↑                                                        ↓
    ←←←←←←←←←←←←←←← Better customer experience ←←←←←←←←←←←←←←←
```

---

## 📝 Summary

The KPT prediction problem isn't a model problem—it's a **data problem**. The training data is corrupted because merchants have no incentive to mark "Food Ready" accurately. Our solution fixes this by:

1. Making rider location transparent (so merchants know when to mark)
2. Scoring and rewarding accuracy (so merchants want to mark correctly)
3. Verifying the worst performers (so the bottom 5% can't game the system)

By cleaning up the training data, the model naturally improves, creating better predictions, happier riders, and more satisfied customers.

---

_Next: See [Cost Analysis](cost_analysis.md) for the financial breakdown of our solution._
