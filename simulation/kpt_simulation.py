"""
Monte Carlo Simulation for Kitchen Prep Time (KPT) Prediction Improvement

This script simulates the impact of our 3-layer solution on FOR (Food Ready)
accuracy and rider wait times across 1000 restaurants over 30 days.

Author: Team ShadowFX
Hackathon: Zomathon 2026 - PS1
"""

import os
import sys
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fix Windows console encoding for Unicode/emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

NUM_RESTAURANTS = 1000
NUM_DAYS = 30

# Restaurant type distribution and properties
RESTAURANT_TYPES = {
    'small': {
        'proportion': 0.50,      # 50% of restaurants
        'orders_per_day_range': (10, 30),
        'base_prep_time': 12,    # minutes
    },
    'medium': {
        'proportion': 0.35,      # 35% of restaurants
        'orders_per_day_range': (30, 60),
        'base_prep_time': 18,    # minutes
    },
    'large': {
        'proportion': 0.15,      # 15% of restaurants
        'orders_per_day_range': (60, 100),
        'base_prep_time': 25,    # minutes
    }
}

# Baseline FOR accuracy (merchants mark on time only 60% of the time)
BASELINE_FOR_ACCURACY = 0.60

# When inaccurate, merchant delays marking by 3-10 minutes
DELAY_RANGE_INACCURATE = (3, 10)

# Intervention effects
LAYER1_ACCURACY_IMPROVEMENT = 0.82  # Layer 1 improves accuracy to 82%
LAYER2_BOTTOM_5_ACCURACY = 0.75     # Layer 2 improves bottom 5% to 75%
LAYER3_RUSH_ERROR_REDUCTION = 0.20  # 20% reduction in rush hour prediction error


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def assign_restaurant_types(num_restaurants: int) -> list:
    """
    Assign restaurant types based on defined proportions.
    
    Args:
        num_restaurants: Total number of restaurants to assign types to
        
    Returns:
        List of restaurant types ('small', 'medium', 'large')
    """
    types = []
    for r_type, props in RESTAURANT_TYPES.items():
        count = int(num_restaurants * props['proportion'])
        types.extend([r_type] * count)
    
    # Handle rounding differences
    while len(types) < num_restaurants:
        types.append('small')  # Default to small if needed
    
    random.shuffle(types)
    return types[:num_restaurants]


def get_orders_per_day(restaurant_type: str) -> int:
    """
    Get random number of orders per day based on restaurant type.
    
    Args:
        restaurant_type: 'small', 'medium', or 'large'
        
    Returns:
        Number of orders for that day
    """
    order_range = RESTAURANT_TYPES[restaurant_type]['orders_per_day_range']
    return random.randint(order_range[0], order_range[1])


def get_prep_time(restaurant_type: str, is_rush_hour: bool = False) -> float:
    """
    Get actual prep time with some variance and rush hour effects.
    
    Args:
        restaurant_type: 'small', 'medium', or 'large'
        is_rush_hour: Whether it's rush hour (adds 20% prep time)
        
    Returns:
        Prep time in minutes
    """
    base_time = RESTAURANT_TYPES[restaurant_type]['base_prep_time']
    # Add 20% variance to prep time
    variance = np.random.normal(0, base_time * 0.2)
    prep_time = base_time + variance
    
    if is_rush_hour:
        prep_time *= 1.2  # Rush hour adds 20% to prep time
    
    return max(5, prep_time)  # Minimum 5 minutes


def simulate_for_accuracy(is_accurate: bool, actual_prep_time: float) -> tuple:
    """
    Simulate FOR marking behavior and calculate rider wait time.
    
    Args:
        is_accurate: Whether merchant marks accurately
        actual_prep_time: Actual time food takes to prepare
        
    Returns:
        Tuple of (marked_prep_time, rider_wait_time)
    """
    if is_accurate:
        # Merchant marks correctly - no rider wait
        marked_prep_time = actual_prep_time
        rider_wait = 0
    else:
        # Merchant delays marking - rider has to wait
        delay = random.uniform(DELAY_RANGE_INACCURATE[0], DELAY_RANGE_INACCURATE[1])
        marked_prep_time = actual_prep_time + delay
        rider_wait = delay
    
    return marked_prep_time, rider_wait


def is_rush_hour() -> bool:
    """
    Determine if current order is during rush hour.
    Rush hours: 12-2 PM (lunch) and 7-9 PM (dinner)
    
    Returns:
        Boolean indicating if it's rush hour
    """
    # Simplified: 30% chance of being rush hour order
    return random.random() < 0.30


# =============================================================================
# MAIN SIMULATION FUNCTIONS
# =============================================================================

def run_baseline_simulation() -> pd.DataFrame:
    """
    Run the baseline simulation (before intervention).
    
    Simulates 30 days with 60% FOR accuracy across all restaurants.
    
    Returns:
        DataFrame with simulation results
    """
    results = []
    restaurant_types = assign_restaurant_types(NUM_RESTAURANTS)
    
    for day in range(1, NUM_DAYS + 1):
        for rest_id in range(NUM_RESTAURANTS):
            rest_type = restaurant_types[rest_id]
            num_orders = get_orders_per_day(rest_type)
            
            total_prep_time = 0
            total_rider_wait = 0
            accurate_count = 0
            
            for _ in range(num_orders):
                rush = is_rush_hour()
                actual_prep = get_prep_time(rest_type, rush)
                total_prep_time += actual_prep
                
                # Determine if this order is marked accurately
                is_accurate = random.random() < BASELINE_FOR_ACCURACY
                if is_accurate:
                    accurate_count += 1
                
                _, rider_wait = simulate_for_accuracy(is_accurate, actual_prep)
                total_rider_wait += rider_wait
            
            # Calculate daily metrics for this restaurant
            avg_prep_time = total_prep_time / num_orders
            for_accuracy = accurate_count / num_orders
            avg_rider_wait = total_rider_wait / num_orders
            
            results.append({
                'day': day,
                'restaurant_id': rest_id,
                'restaurant_type': rest_type,
                'order_count': num_orders,
                'avg_prep_time': round(avg_prep_time, 2),
                'FOR_accuracy': round(for_accuracy, 4),
                'avg_rider_wait': round(avg_rider_wait, 2),
                'intervention': 'before'
            })
    
    return pd.DataFrame(results)


def run_intervention_simulation(baseline_df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the simulation after implementing our 3-layer solution.
    
    Layer 1: Improves accuracy to 82% for all merchants
    Layer 2: Bottom 5% merchants improve to 75% (from ~30%)
    Layer 3: Rush hour prediction error reduces by 20%
    
    Args:
        baseline_df: DataFrame from baseline simulation to identify bottom performers
        
    Returns:
        DataFrame with post-intervention results
    """
    results = []
    
    # Identify bottom 5% merchants by accuracy from baseline
    merchant_avg_accuracy = baseline_df.groupby('restaurant_id')['FOR_accuracy'].mean()
    bottom_5_threshold = merchant_avg_accuracy.quantile(0.05)
    bottom_5_merchants = set(merchant_avg_accuracy[merchant_avg_accuracy <= bottom_5_threshold].index)
    
    # Get restaurant types from baseline
    restaurant_types = baseline_df.groupby('restaurant_id')['restaurant_type'].first().values
    
    for day in range(1, NUM_DAYS + 1):
        for rest_id in range(NUM_RESTAURANTS):
            rest_type = restaurant_types[rest_id]
            num_orders = get_orders_per_day(rest_type)
            
            total_prep_time = 0
            total_rider_wait = 0
            accurate_count = 0
            
            for _ in range(num_orders):
                rush = is_rush_hour()
                actual_prep = get_prep_time(rest_type, rush)
                total_prep_time += actual_prep
                
                # Determine accuracy based on intervention layers
                if rest_id in bottom_5_merchants:
                    # Layer 2: Bottom 5% get barcode verification
                    is_accurate = random.random() < LAYER2_BOTTOM_5_ACCURACY
                else:
                    # Layer 1: Everyone else gets rider location transparency
                    is_accurate = random.random() < LAYER1_ACCURACY_IMPROVEMENT
                
                if is_accurate:
                    accurate_count += 1
                
                _, rider_wait = simulate_for_accuracy(is_accurate, actual_prep)
                
                # Layer 3: Rush hour wait times reduced due to better prediction
                if rush:
                    rider_wait *= (1 - LAYER3_RUSH_ERROR_REDUCTION)
                
                total_rider_wait += rider_wait
            
            avg_prep_time = total_prep_time / num_orders
            for_accuracy = accurate_count / num_orders
            avg_rider_wait = total_rider_wait / num_orders
            
            results.append({
                'day': day,
                'restaurant_id': rest_id,
                'restaurant_type': rest_type,
                'order_count': num_orders,
                'avg_prep_time': round(avg_prep_time, 2),
                'FOR_accuracy': round(for_accuracy, 4),
                'avg_rider_wait': round(avg_rider_wait, 2),
                'intervention': 'after'
            })
    
    return pd.DataFrame(results)


def calculate_summary_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate summary metrics from simulation results.
    
    Args:
        df: DataFrame with simulation results
        
    Returns:
        Dictionary with summary metrics
    """
    total_orders = df['order_count'].sum()
    
    # Calculate weighted average rider wait
    weighted_wait = (df['avg_rider_wait'] * df['order_count']).sum() / total_orders
    
    # Calculate overall FOR accuracy
    weighted_accuracy = (df['FOR_accuracy'] * df['order_count']).sum() / total_orders
    
    # Estimate orders with 5+ min wait (assuming exponential distribution)
    # Using the average wait time to estimate probability of 5+ min wait
    orders_5min_plus = df.groupby('restaurant_type').apply(
        lambda x: (x['order_count'] * (1 - np.exp(-x['avg_rider_wait'].mean() / 5))).sum(),
        include_groups=False
    ).sum()
    
    return {
        'avg_rider_wait': round(weighted_wait, 2),
        'for_accuracy': round(weighted_accuracy * 100, 1),
        'orders_5min_plus_pct': round((orders_5min_plus / total_orders) * 100, 1)
    }


def print_summary_table(before_metrics: dict, after_metrics: dict):
    """
    Print a clean summary table comparing before vs after intervention.
    
    Args:
        before_metrics: Dictionary with baseline metrics
        after_metrics: Dictionary with post-intervention metrics
    """
    print("\n" + "=" * 70)
    print("🍕 KPT PREDICTION SIMULATION RESULTS")
    print("=" * 70)
    print(f"\n{'Metric':<35} {'Before':<15} {'After':<15} {'Change':<15}")
    print("-" * 70)
    
    # Rider Wait Time
    wait_change = after_metrics['avg_rider_wait'] - before_metrics['avg_rider_wait']
    wait_pct = (wait_change / before_metrics['avg_rider_wait']) * 100
    print(f"{'Avg Rider Wait Time (min)':<35} {before_metrics['avg_rider_wait']:<15.1f} "
          f"{after_metrics['avg_rider_wait']:<15.1f} {wait_pct:+.1f}%")
    
    # FOR Accuracy
    acc_change = after_metrics['for_accuracy'] - before_metrics['for_accuracy']
    print(f"{'FOR Accuracy (%)':<35} {before_metrics['for_accuracy']:<15.1f} "
          f"{after_metrics['for_accuracy']:<15.1f} {acc_change:+.1f}pp")
    
    # Orders with 5+ min wait
    orders_change = after_metrics['orders_5min_plus_pct'] - before_metrics['orders_5min_plus_pct']
    orders_pct = (orders_change / before_metrics['orders_5min_plus_pct']) * 100
    print(f"{'Orders with 5min+ Wait (%)':<35} {before_metrics['orders_5min_plus_pct']:<15.1f} "
          f"{after_metrics['orders_5min_plus_pct']:<15.1f} {orders_pct:+.1f}%")
    
    print("-" * 70)
    print("\n✅ Simulation completed successfully!")
    print("📊 Results saved to: simulation/results/simulation_output.csv")
    print("📈 Graphs saved to: simulation/results/simulation_graphs.png")
    print("=" * 70 + "\n")


def generate_graphs(before_df: pd.DataFrame, after_df: pd.DataFrame, output_path: str):
    """
    Generate visualization graphs comparing before and after intervention.
    
    Creates 4 subplots:
    1. Bar chart: Avg Rider Wait Time by restaurant type
    2. Line chart: Daily FOR Accuracy over 30 days
    3. Bar chart: % Orders with 5min+ wait
    4. Pie chart: Merchant distribution by type
    
    Args:
        before_df: DataFrame with baseline results
        after_df: DataFrame with post-intervention results
        output_path: Path to save the generated graph
    """
    # Set style and color palette
    plt.style.use('seaborn-v0_8-whitegrid')
    colors = {'before': '#FF6B35', 'after': '#004E89'}  # Orange and Blue
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('KPT Prediction Improvement - Simulation Results', fontsize=16, fontweight='bold')
    
    # -------------------------------------------------------------------------
    # Plot 1: Bar chart - Avg Rider Wait Time by Restaurant Type
    # -------------------------------------------------------------------------
    ax1 = axes[0, 0]
    
    wait_by_type_before = before_df.groupby('restaurant_type')['avg_rider_wait'].mean()
    wait_by_type_after = after_df.groupby('restaurant_type')['avg_rider_wait'].mean()
    
    x = np.arange(len(wait_by_type_before))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, wait_by_type_before.values, width, 
                    label='Before', color=colors['before'], alpha=0.8)
    bars2 = ax1.bar(x + width/2, wait_by_type_after.values, width, 
                    label='After', color=colors['after'], alpha=0.8)
    
    ax1.set_xlabel('Restaurant Type', fontweight='bold')
    ax1.set_ylabel('Avg Rider Wait Time (min)', fontweight='bold')
    ax1.set_title('Avg Rider Wait Time by Restaurant Type', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(['Large', 'Medium', 'Small'])
    ax1.legend()
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        height = bar.get_height()
        ax1.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
    
    # -------------------------------------------------------------------------
    # Plot 2: Line chart - Daily FOR Accuracy over 30 days
    # -------------------------------------------------------------------------
    ax2 = axes[0, 1]
    
    daily_acc_before = before_df.groupby('day')['FOR_accuracy'].mean() * 100
    daily_acc_after = after_df.groupby('day')['FOR_accuracy'].mean() * 100
    
    ax2.plot(daily_acc_before.index, daily_acc_before.values, 
             color=colors['before'], linewidth=2, marker='o', markersize=4, label='Before')
    ax2.plot(daily_acc_after.index, daily_acc_after.values, 
             color=colors['after'], linewidth=2, marker='s', markersize=4, label='After')
    
    ax2.set_xlabel('Day', fontweight='bold')
    ax2.set_ylabel('FOR Accuracy (%)', fontweight='bold')
    ax2.set_title('Daily FOR Accuracy Over 30 Days', fontweight='bold')
    ax2.legend()
    ax2.set_xlim(1, 30)
    ax2.set_ylim(50, 100)
    
    # -------------------------------------------------------------------------
    # Plot 3: Bar chart - % Orders with 5min+ wait
    # -------------------------------------------------------------------------
    ax3 = axes[1, 0]
    
    # Calculate percentage of orders with 5+ min wait
    def calc_5min_plus_pct(df):
        total_orders = df['order_count'].sum()
        orders_5min = (df['order_count'] * (1 - np.exp(-df['avg_rider_wait'] / 5))).sum()
        return (orders_5min / total_orders) * 100
    
    pct_before = calc_5min_plus_pct(before_df)
    pct_after = calc_5min_plus_pct(after_df)
    
    categories = ['Before Intervention', 'After Intervention']
    values = [pct_before, pct_after]
    bar_colors = [colors['before'], colors['after']]
    
    bars = ax3.bar(categories, values, color=bar_colors, alpha=0.8, width=0.5)
    ax3.set_ylabel('% of Orders with 5+ min Wait', fontweight='bold')
    ax3.set_title('Orders with 5+ Minute Rider Wait', fontweight='bold')
    ax3.set_ylim(0, 60)
    
    # Add value labels
    for bar, val in zip(bars, values):
        ax3.annotate(f'{val:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, val),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', 
                    fontsize=11, fontweight='bold')
    
    # -------------------------------------------------------------------------
    # Plot 4: Pie chart - Merchant distribution by type
    # -------------------------------------------------------------------------
    ax4 = axes[1, 1]
    
    type_counts = before_df.groupby('restaurant_id')['restaurant_type'].first().value_counts()
    
    pie_colors = ['#FF6B35', '#004E89', '#7EB5D6']  # Orange, Dark Blue, Light Blue
    explode = (0.05, 0.02, 0.02)
    
    wedges, texts, autotexts = ax4.pie(type_counts.values, labels=['Small (50%)', 'Medium (35%)', 'Large (15%)'],
                                        autopct='%1.0f%%', colors=pie_colors, explode=explode,
                                        shadow=True, startangle=90)
    
    ax4.set_title('Restaurant Distribution by Type', fontweight='bold')
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"📊 Graphs saved to: {output_path}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main function to run the complete Monte Carlo simulation.
    
    Runs baseline simulation, intervention simulation, calculates metrics,
    prints summary, and generates visualizations.
    """
    print("\n" + "=" * 70)
    print("🍕 KPT PREDICTION MONTE CARLO SIMULATION")
    print("=" * 70)
    print(f"\n📊 Simulating {NUM_RESTAURANTS} restaurants over {NUM_DAYS} days...")
    print(f"   - Small restaurants: {int(NUM_RESTAURANTS * 0.50)} (50%)")
    print(f"   - Medium restaurants: {int(NUM_RESTAURANTS * 0.35)} (35%)")
    print(f"   - Large restaurants: {int(NUM_RESTAURANTS * 0.15)} (15%)")
    print(f"\n⏳ Running baseline simulation (60% FOR accuracy)...")
    
    # Create results directory if it doesn't exist
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Run baseline simulation
    before_df = run_baseline_simulation()
    print(f"   ✓ Baseline simulation complete: {len(before_df)} data points")
    
    # Run intervention simulation
    print(f"\n⏳ Running intervention simulation (Layer 1, 2, 3 applied)...")
    after_df = run_intervention_simulation(before_df)
    print(f"   ✓ Intervention simulation complete: {len(after_df)} data points")
    
    # Combine results
    combined_df = pd.concat([before_df, after_df], ignore_index=True)
    
    # Save to CSV
    csv_path = os.path.join(results_dir, 'simulation_output.csv')
    combined_df.to_csv(csv_path, index=False)
    print(f"\n💾 Results saved to: {csv_path}")
    
    # Calculate and print summary metrics
    before_metrics = calculate_summary_metrics(before_df)
    after_metrics = calculate_summary_metrics(after_df)
    
    print_summary_table(before_metrics, after_metrics)
    
    # Generate graphs
    graphs_path = os.path.join(results_dir, 'simulation_graphs.png')
    generate_graphs(before_df, after_df, graphs_path)


if __name__ == "__main__":
    main()
