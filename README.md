# 🍕 Zomathon-PS1-KPT: Kitchen Prep Time Prediction Solution

> **Zomathon 2026** | Problem Statement: PS1 - Kitchen Prep Time (KPT) Prediction
> Team: **ShadowFX**

---

## 🎯 The Problem in One Line

Zomato's Kitchen Prep Time predictions are inaccurate because merchants mark "Food Ready" when the rider arrives—not when the food is actually ready—corrupting training data and causing wrong ETAs, longer wait times, and more cancellations.

---

## 💡 Our 3-Layer Solution

### Layer 1: Rider Location Transparency (Main Solution)

- Merchant app shows **real-time rider location** + ETA countdown
- Merchants get an **Accuracy Score (0-100)** on their dashboard
- High accuracy unlocks **rewards**: priority routing, lower commission, leaderboard badges

### Layer 2: Barcode Verification (Bottom 5% Merchants Only)

- Kitchen packs food → generates QR code → takes photo → uploads
- "Mark Food Ready" button **only unlocks after photo upload**
- Thermal printers for large chains, app QR for medium, Layer 1 only for dhabas

### Layer 3: Kitchen Load Visibility

- POS integration for top 500 chains (anonymous order count)
- **Kitchen Rush Slider** (Green/Yellow/Red) for all other merchants
- KPT model uses this as extra feature for rush hour prediction

---

## 📊 Expected Impact

| Metric                    | Before   | After   | Improvement |
| ------------------------- | -------- | ------- | ----------- |
| Avg Rider Wait Time       | 12.3 min | 8.1 min | ⬇️ 34%      |
| FOR (Food Ready) Accuracy | 60%      | 87%     | ⬆️ 45%      |
| Orders with 5min+ Wait    | 42%      | 18%     | ⬇️ 57%      |

---

## 🚀 How to Run the Simulation

```bash
# Clone the repo
git clone https://github.com/[your-username]/Zomathon-PS1-KPT.git
cd Zomathon-PS1-KPT

# Install dependencies
pip install numpy pandas matplotlib seaborn

# Run the Monte Carlo simulation
python simulation/kpt_simulation.py
```

The simulation will:

1. Print a summary table in the terminal
2. Generate `simulation/results/simulation_output.csv`
3. Generate `simulation/results/simulation_graphs.png` with 4 visualizations

---

## 👥 Team ShadowFX

| Name             | Role                |
| ---------------- | ------------------- |
| Swadhin Kumar    | Team Lead & Backend |
| Suraj Ku. Behera | Frontend & ML       |

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Mobile**: React Native (Merchant & Rider Apps)
- **ML/AI**: scikit-learn, XGBoost for KPT model
- **Real-time**: WebSockets for GPS tracking
- **Database**: PostgreSQL + Redis
- **Cloud**: AWS/GCP

---

## 📄 Documentation

- [Problem Analysis](docs/problem_analysis.md) - Deep dive into why FOR signals fail
- [Cost Analysis](docs/cost_analysis.md) - Breakdown of implementation costs
- [Architecture](architecture/architecture_description.md) - System design overview
- [Mockups](mockups/mockups_description.md) - UI/UX descriptions

---

## 📎 Links

- [Proposal PDF](link-to-proposal-pdf) ← Add your proposal document link here
- [Demo Video](link-to-demo) ← Add demo video link here

---

## 📁 Project Structure

```
Zomathon-PS1-KPT/
├── README.md
├── simulation/
│   ├── kpt_simulation.py
│   └── results/
│       ├── simulation_output.csv
│       └── simulation_graphs.png
├── mockups/
│   └── mockups_description.md
├── architecture/
│   └── architecture_description.md
└── docs/
    ├── problem_analysis.md
    └── cost_analysis.md
```

---

_Built with ❤️ for Zomathon 2026_
