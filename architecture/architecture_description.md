# 🏗️ System Architecture

Our solution introduces lightweight microservices that bridge the gap between real-world kitchen states and the AI prediction engine.

## 📱 Components

### 1. Merchant App

- **Telemetry Subscriber:** Receives low-latency rider GPS coordinates via WebSocket for the Layer 1 countdown.
- **Rush State Broadcaster:** A simple module that pushes the state of the "Kitchen Rush Slider" (Green/Yellow/Red) to the backend.
- **QR Generator Engine:** Only active for bottom 5% merchants. Packages order details into a barcode format.

### 2. Rider App

- **Validation Module:** Prompts the rider post-delivery: "Was the food _actually_ ready when marked?". This acts as the final ground-truth check for the Merchant Accuracy Score.

### 3. Backend Services

- **Accuracy Score Engine (ASE):** The core rules engine. It compares Rider Arrival GPS timestamps, Merchant FOR timestamps, and Rider Departure timestamps. If `(Rider Arrival - FOR Timestamp) > Threshold` repeatedly, it flags the merchant.
- **Barcode Verification Service:** An image-processing API that validates photos of the packed order with the corresponding temporal QR code before unlocking the FOR button.
- **KPT Model (Enhanced):** The existing Machine Learning KPT model, now retrained to accept "Kitchen Rush State" (0, 1, 2) and "Merchant Accuracy Tier" as highly weighted features.

## 📊 ASCII Diagram

```text
[ Rider App ] ---(GPS Stream)---> [ Zomato Core API ]
      |                                   |
      `--(Post-Delivery Validation)--> [ Accuracy Score Engine ] <--- (FOR Flags)
                                          |           |
                                          |           v
                                          |     [ Merchant DB ] (Tier: 0-100)
                                          |           |
[ Merchant App ] <---(Rider ETA/GPS)------'           |
      |                                               |
      +---(Marks FOR)---------------------------------'
      |
      +---(Kitchen Rush Slider)-----------------> [ Enhanced KPT ML Model ]
      |                                               ^
      +---(Layer 2: Barcode Photo Upload)             |
          |                                           |
          v                                           |
    [ Barcode Verification Service ] --(Valid)--------'
```
