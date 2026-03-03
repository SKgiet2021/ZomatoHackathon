# 🎨 UI Mockups Description

Below are the descriptions of the high-fidelity mockups designed for this solution.

## 1. Merchant App - Rider Location Card (Layer 1)

- **Layout:** Pinned to the top of the Active Orders screen.
- **Key Elements:** A mini-map showing the rider's live icon moving towards the restaurant pin. A large, bold countdown timer: "Rider arriving in 4 mins".
- **Colors:** Zomato Red for the timer, transitioning to urgent Orange when ETA < 2 mins.
- **User Sees:** Immediate visual feedback that the rider is approaching, incentivizing them to finish packing rather than preemptively marking FOR.

## 2. Merchant App - Accuracy Score Dashboard

- **Layout:** A dedicated tab in the Merchant Performance section.
- **Key Elements:** A massive circular gauge showing the score (e.g., 88/100). Below it, a progress bar showing rewards unlocked (e.g., "Tier 1: Priority Dispatch Unlocked!"). A list of "Recent Flagged Orders" showing where they misreported times.
- **Colors:** Green for scores 80+, Yellow for 50-79, Red for <50.
- **User Sees:** Gamified accountability. They clearly see how their behavior directly impacts their platform search ranking and commissions.

## 3. Barcode Verification Screen (Layer 2)

- **Layout:** A modal that intercepts the "Mark Food Ready" action for low-tier merchants.
- **Key Elements:** A camera viewfinder taking up 70% of the screen. An overlay box indicating where to align the receipt/QR code. A shutter button labeled "Scan & Mark Ready".
- **Colors:** Dark, focused UI with bright green targeting brackets.
- **User Sees:** A strict checkpoint. They cannot bypass the system without physically proving the order is packed.

## 4. Rider App - Post Delivery Validation

- **Layout:** A quick swipe-up card appearing immediately after marking an order "Delivered".
- **Key Elements:** A single question: "Was the food ready upon your arrival at the restaurant?". Two large buttons: 👍 Yes / 👎 No (I had to wait).
- **Colors:** Neutral white card, standard green/red buttons.
- **User Sees:** A 1-second task that empowers the rider to report the truth.

## 5. Kitchen Rush Slider (Layer 3)

- **Layout:** A persistent toggle switch at the top navigation bar of the Merchant tablet.
- **Key Elements:** A smooth, 3-stage slider: [🟢 Normal] - [🟡 Busy] - [🔴 Slammed].
- **Colors:** Green (0-10 offline orders), Yellow (11-25 offline orders), Red (25+ offline orders).
- **User Sees:** A simple, frictionless way to tell Zomato's algorithm that their kitchen is currently overwhelmed, protecting them from unrealistic KPT expectations.
