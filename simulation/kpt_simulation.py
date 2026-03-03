"""
Zomathon 2026: PS1 - Kitchen Prep Time (KPT) Prediction
Monte Carlo simulation to prove the impact of the Kitchen Prep Time intervention.
"""

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_simulation_data():
    """Generates the before/after data for KPT intervention."""
    
    num_restaurants = 1000
    days = 30
    
    # 1. Setup Restaurant Profiles
    restaurant_types = ['small', 'medium', 'large']
    
    # 50% small, 35% medium, 15% large
    type_allocation = np.random.choice(
        restaurant_types, 
        num_restaurants, 
        p=[0.50, 0.35, 0.15]
    )
    
    restaurants = []
    for i, r_type in enumerate(type_allocation):
        if r_type == 'small':
            base_prep = 12
            daily_orders_range = (10, 30)
            baseline_accuracy = 0.60
        elif r_type == 'medium':
            base_prep = 18
            daily_orders_range = (30, 65)
            baseline_accuracy = 0.60
        else: # large
            base_prep = 25
            daily_orders_range = (65, 100)
            baseline_accuracy = 0.60
            
        restaurants.append({
            'restaurant_id': f'R_{i+1:04d}',
            'restaurant_type': r_type,
            'base_prep_time': base_prep,
            'daily_orders_range': daily_orders_range,
            'baseline_accuracy': baseline_accuracy
        })
        
    # Determine the bottom 5% offenders for Layer 2. Let's flag them early.
    # We assign them a terribly low initial accuracy
    bottom_5_percent_count = int(num_restaurants * 0.05)
    bottom_offenders = random.sample(restaurants, bottom_5_percent_count)
    for r in bottom_offenders:
        r['baseline_accuracy'] = 0.30 # Bottom 5% have 30% accuracy initially
        
    records = []
    
    print("Running simulation (Before vs After)...")
    
    for day in range(1, days + 1):
        for r in restaurants:
            order_count = np.random.randint(r['daily_orders_range'][0], r['daily_orders_range'][1])
            
            # --- BEFORE INTERVENTION SIMULATION ---
            # Determine how many orders had accurate FOR times
            accurate_orders_before = int(order_count * r['baseline_accuracy'])
            inaccurate_orders_before = order_count - accurate_orders_before
            
            # Wait time calculation (Before)
            # Accurate FOR -> little to no wait (average 2 mins for rider transit buffering)
            wait_accurate_before = np.random.normal(2.0, 1.0, accurate_orders_before)
            wait_accurate_before = np.clip(wait_accurate_before, 0, None)
            
            # Inaccurate FOR -> delay of 3 to 10 minutes artificially added
            added_delay_before = np.random.uniform(3, 10, inaccurate_orders_before)
            wait_inaccurate_before = np.random.normal(2.0, 1.0, inaccurate_orders_before) + added_delay_before
            
            all_waits_before = np.concatenate([wait_accurate_before, wait_inaccurate_before])
            avg_wait_before = np.mean(all_waits_before)
            orders_over_5_before = np.sum(all_waits_before >= 5.0)
            
            records.append({
                'day': day,
                'restaurant_id': r['restaurant_id'],
                'restaurant_type': r['restaurant_type'],
                'order_count': order_count,
                'avg_prep_time': r['base_prep_time'],
                'FOR_accuracy': r['baseline_accuracy'] * 100, # convert to percentage
                'avg_rider_wait': avg_wait_before,
                'orders_over_5min': orders_over_5_before,
                'intervention': 'Before'
            })
            
            # --- AFTER INTERVENTION SIMULATION ---
            # Layer 1 effect: normal merchants boost to 82%
            # Layer 2 effect: bottom 5% offenders boost to 75%
            # Layer 3 effect: rush hour variance drops, standardizing KPT error (simulated as minor wait reduction)
            
            if r in bottom_offenders:
                new_accuracy = 0.75 # Layer 2 kicks in
            else:
                new_accuracy = 0.82 # Layer 1 kicks in
                
            accurate_orders_after = int(order_count * new_accuracy)
            inaccurate_orders_after = order_count - accurate_orders_after
            
            wait_accurate_after = np.random.normal(1.5, 0.5, accurate_orders_after) # Layer 3 helps reduce buffer slightly
            wait_accurate_after = np.clip(wait_accurate_after, 0, None)
            
            # The remaining inaccurates might have shorter malicious delays due to fear of the Accuracy Score
            added_delay_after = np.random.uniform(2, 6, inaccurate_orders_after)
            wait_inaccurate_after = np.random.normal(1.5, 0.5, inaccurate_orders_after) + added_delay_after
            
            all_waits_after = np.concatenate([wait_accurate_after, wait_inaccurate_after])
            avg_wait_after = np.mean(all_waits_after)
            orders_over_5_after = np.sum(all_waits_after >= 5.0)
            
            records.append({
                'day': day,
                'restaurant_id': r['restaurant_id'],
                'restaurant_type': r['restaurant_type'],
                'order_count': order_count,
                'avg_prep_time': r['base_prep_time'],
                'FOR_accuracy': new_accuracy * 100,
                'avg_rider_wait': avg_wait_after,
                'orders_over_5min': orders_over_5_after,
                'intervention': 'After'
            })
            
    df = pd.DataFrame(records)
    return df

def generate_reports_and_graphs(df):
    """Processes DataFrame to output console summary, CSV, and graphs."""
    
    # 1. Prepare Directory
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # 2. Save CSV
    csv_path = os.path.join(results_dir, 'simulation_output.csv')
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
    
    # 3. Terminal Summary Table
    print("\n" + "="*50)
    print("📈 ZOMATHON PS1: IMPACT SUMMARY 📈")
    print("="*50)
    
    before_df = df[df['intervention'] == 'Before']
    after_df = df[df['intervention'] == 'After']
    
    total_orders = before_df['order_count'].sum() # Same for after
    
    # Metrics
    avg_wait_b = before_df['avg_rider_wait'].mean()
    avg_wait_a = after_df['avg_rider_wait'].mean()
    
    acc_b = before_df['FOR_accuracy'].mean()
    acc_a = after_df['FOR_accuracy'].mean()
    
    percent_over_5_b = (before_df['orders_over_5min'].sum() / total_orders) * 100
    percent_over_5_a = (after_df['orders_over_5min'].sum() / total_orders) * 100
    
    print(f"{'Metric':<25} | {'Before':<10} | {'After':<10}")
    print("-" * 50)
    print(f"{'Avg Rider Wait Time':<25} | {avg_wait_b:.2f} min | {avg_wait_a:.2f} min")
    print(f"{'FOR Accuracy':<25} | {acc_b:.1f}%     | {acc_a:.1f}%")
    print(f"{'Orders w/ 5min+ Wait':<25} | {percent_over_5_b:.1f}%     | {percent_over_5_a:.1f}%")
    print("="*50 + "\n")

    # 4. Generate Graphs
    sns.set_theme(style="whitegrid")
    # Professional color scheme: blues and oranges
    palette = {"Before": "#4A90E2", "After": "#F39C12"}
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Kitchen Prep Time (KPT) Intervention Results: 30-Day Simulation', fontsize=18, fontweight='bold', y=0.98)
    
    # Subplot 1: Avg Rider Wait Time Before vs After (by restaurant type)
    sns.barplot(
        data=df, 
        x='restaurant_type', 
        y='avg_rider_wait', 
        hue='intervention',
        ax=axes[0, 0],
        palette=palette,
        order=['small', 'medium', 'large']
    )
    axes[0, 0].set_title('Avg Rider Wait Time by Merchant Type', fontsize=14)
    axes[0, 0].set_ylabel('Wait Time (Minutes)')
    axes[0, 0].set_xlabel('Merchant Type')
    
    # Subplot 2: Line chart: Daily FOR Accuracy over 30 days
    daily_acc = df.groupby(['day', 'intervention'])['FOR_accuracy'].mean().reset_index()
    sns.lineplot(
        data=daily_acc,
        x='day',
        y='FOR_accuracy',
        hue='intervention',
        ax=axes[0, 1],
        palette=palette,
        linewidth=2.5,
        marker='o'
    )
    axes[0, 1].set_title('Average Daily FOR Accuracy (%)', fontsize=14)
    axes[0, 1].set_ylabel('Accuracy Score (%)')
    axes[0, 1].set_xlabel('Day')
    axes[0, 1].set_ylim(40, 100)
    
    # Subplot 3: Bar chart: % Orders with 5min+ wait Before vs After
    # Group by intervention and sum
    over_5_totals = {"Before": percent_over_5_b, "After": percent_over_5_a}
    bars = axes[1, 0].bar(over_5_totals.keys(), over_5_totals.values(), color=["#4A90E2", "#F39C12"], width=0.5)
    axes[1, 0].set_title('% Orders with 5M+ Wait (Total)', fontsize=14)
    axes[1, 0].set_ylabel('% of All Orders')
    
    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Subplot 4: Pie chart: Merchant distribution by type
    r_counts = df[df['day'] == 1]['restaurant_type'].value_counts()
    axes[1, 1].pie(
        r_counts.values, 
        labels=r_counts.index.str.capitalize(), 
        autopct='%1.1f%%', 
        colors=['#3498DB', '#9B59B6', '#E74C3C'],
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    axes[1, 1].set_title('Merchant Distribution in Simulation', fontsize=14)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    graph_path = os.path.join(results_dir, 'simulation_graphs.png')
    plt.savefig(graph_path, dpi=300)
    print(f"Graphs saved to {graph_path}")

if __name__ == "__main__":
    simulation_df = generate_simulation_data()
    generate_reports_and_graphs(simulation_df)
    print("\nSimulation complete. Hackathon materials are ready! 🚀")
