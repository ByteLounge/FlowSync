"""Enhanced visualization utilities for FlowSync."""

import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Tuple
from core.models import SimulationOutput

def create_performance_charts(base: SimulationOutput, opt: SimulationOutput) -> Tuple[Any, Any]:
    """Creates professional-grade comparison charts.

    Returns:
        Tuple[plt.Figure, plt.Figure]: (Line charts fig, Bar charts fig)
    """
    # Set global aesthetic style
    plt.rcParams.update({
        'font.size': 10,
        'axes.edgecolor': '#DDDDDD',
        'axes.labelcolor': '#444444',
        'xtick.color': '#666666',
        'ytick.color': '#666666',
        'grid.color': '#EEEEEE',
        'grid.linestyle': '--'
    })

    # --- FIGURE 1: Line Charts (Dynamics over Time) ---
    fig_line, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Calculate Total System Queues
    base_total_q = np.sum([np.array(f.queue_over_time) for f in base.data.values()], axis=0)
    opt_total_q = np.sum([np.array(f.queue_over_time) for f in opt.data.values()], axis=0)

    # Plot Total System Queue
    ax1.plot(base.time_axis, base_total_q, color='#E53935', label='Baseline (Total)', linewidth=2.5, alpha=0.8)
    ax1.plot(opt.time_axis, opt_total_q, color='#1B5E20', label='FlowSync (Total)', linewidth=3)
    ax1.fill_between(base.time_axis, opt_total_q, base_total_q, color='#E8F5E9', alpha=0.3, label='Congestion Saved')

    ax1.set_title("Total System Congestion", pad=20, weight='bold', size=14)
    ax1.set_xlabel("Time (minutes)")
    ax1.set_ylabel("Users in Queue")
    ax1.legend(frameon=False)
    ax1.grid(True)

    # Plot Average Wait Time Comparison
    base_avg_w = np.mean([np.array(f.wait_times) for f in base.data.values()], axis=0)
    opt_avg_w = np.mean([np.array(f.wait_times) for f in opt.data.values()], axis=0)

    ax2.plot(base.time_axis, base_avg_w, color='#D81B60', label='Baseline Avg', linewidth=2.5, linestyle='--')
    ax2.plot(opt.time_axis, opt_avg_w, color='#2E7D32', label='FlowSync Avg', linewidth=3)
    
    ax2.set_title("System Wait-Time Trends", pad=20, weight='bold', size=14)
    ax2.set_xlabel("Time (minutes)")
    ax2.set_ylabel("Wait Time (minutes)")
    ax2.legend(frameon=False)
    ax2.grid(True)

    # --- FIGURE 2: Bar Charts (Executive Summary) ---
    fig_bar, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 5))

    # Avg Wait Bar Chart
    labels = ['Baseline', 'FlowSync']
    waits = [base.avg_wait, opt.avg_wait]
    colors = ['#EF5350', '#66BB6A']
    
    bars1 = ax3.bar(labels, waits, color=colors, width=0.6)
    ax3.set_title("Average Wait Time (lower is better)", pad=15, weight='bold')
    ax3.set_ylabel("Minutes")
    ax3.bar_label(bars1, fmt='%.1f min', padding=3)

    # Max Queue Bar Chart
    queues = [base.max_queue, opt.max_queue]
    bars2 = ax4.bar(labels, queues, color=colors, width=0.6)
    ax4.set_title("Maximum Queue Size (lower is better)", pad=15, weight='bold')
    ax4.set_ylabel("User Count")
    ax4.bar_label(bars2, fmt='%d users', padding=3)

    for ax in [ax1, ax2, ax3, ax4]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    return fig_line, fig_bar
