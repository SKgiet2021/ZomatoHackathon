# 🛵 Zomathon 2026: PS1 - Kitchen Prep Time (KPT) Prediction ⏱️

**Problem:** Zomato's Kitchen Prep Time prediction is inaccurate because merchants mark "Food Ready" when the rider arrives, not when the food is ACTUALLY ready. This corrupts training data, inflates rider wait times, and ruins the ETA experience.

## ✨ Our 3-Layer Solution

- **LAYER 1 (Rider Location Transparency):** Merchant app provides real-time rider location and ETA countdown. Merchants are scored on "Food Ready" accuracy. High accuracy unlocks priority routing and lower commissions!
- **LAYER 2 (Barcode Verification):** Targeted at the bottom 5% of merchants. They must pack the food, generate a QR code, snap a photo, and ONLY THEN can they mark "Food Ready".
- **LAYER 3 (Kitchen Load Visibility):** POS integration for large chains to track total orders. Kitchen Rush Slider (Green/Yellow/Red) for smaller merchants to signal peak load to the KPT model.

## � Expected Impact

| Metric                     | Before   | After   |
| :------------------------- | :------- | :------ |
| **Avg Rider Wait Time**    | 12.3 min | 8.1 min |
| **FOR Accuracy**           | 60%      | 87%     |
| **Orders with 5min+ Wait** | 42%      | 18%     |

## 🚀 How to Run the Simulation

We've built a Monte Carlo simulation to prove the impact of our solution across 1000 simulated restaurants over 30 days.

1.  **Install requirements:**
    ```bash
    pip install numpy pandas matplotlib seaborn
    ```
2.  **Run the script:**
    ```bash
    python simulation/kpt_simulation.py
    ```
    _This will generate a clean CSV dataset and graphs in the `simulation/results/` folder._

## �‍💻 Team: [Your Team Name]

- [Team Member 1 Name]
- [Team Member 2 Name]
- [Team Member 3 Name]

## 🛠️ Tech Stack

- **Simulation:** Python (Pandas, Numpy, Matplotlib, Seaborn)
- **System Architecture:** Proposed Microservices (Node.js, Python/FastAPI for ML, Redis for spatial tracking)
- **Mockups:** Figma

## 📎 Links

- [Proposal PDF Placeholder]
