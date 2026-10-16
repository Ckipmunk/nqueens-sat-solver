"""
Module: plot_results.py
Mục đích: Vẽ các đồ thị khoa học chuẩn Elsevier từ dữ liệu unified_benchmark.json:
1. fig_clauses_scaling.pdf/.png: Đồ thị số lượng mệnh đề của 5 phương pháp AMO (log-log)
2. fig_solver_runtime.pdf/.png: Đồ thị thời gian giải giữa các solver (log-log, có đánh dấu timeout và limit)
3. fig_board_8queens.pdf/.png: Bàn cờ minh họa nghiệm 8-Queens
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def generate_plots():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    figs_dir = os.path.join(base_dir, "report", "figures")
    os.makedirs(figs_dir, exist_ok=True)

    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        'figure.titlesize': 14
    })

    unified_file = os.path.join(data_dir, "unified_benchmark.json")
    if not os.path.exists(unified_file):
        print(f"Không tìm thấy {unified_file}")
        return

    with open(unified_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Đồ thị Clauses Scaling
    fig, ax = plt.subplots(figsize=(6.8, 4.3), dpi=300)
    markers = {'pairwise': 'o', 'sequential': 's', 'commander': '^', 'binary': 'd', 'product': 'v'}
    colors = {'pairwise': '#d62728', 'sequential': '#1f77b4', 'commander': '#2ca02c', 'binary': '#9467bd', 'product': '#ff7f0e'}
    labels = {
        'pairwise': 'Pairwise (Direct) - O(N³)',
        'sequential': 'Sequential Counter - O(N²)',
        'commander': 'Commander Variable - O(N²)',
        'binary': 'Binary (Bitwise) - O(N² log N)',
        'product': 'Product (2D Grid) - O(N²)'
    }

    ablation_dict = data["amo_ablation"]
    for m in ['pairwise', 'sequential', 'commander', 'binary', 'product']:
        n_vals = []
        clauses = []
        for n_str in ['8', '16', '32', '64', '128']:
            if m in ablation_dict[n_str] and ablation_dict[n_str][m].get("num_clauses"):
                n_vals.append(int(n_str))
                clauses.append(ablation_dict[n_str][m]["num_clauses"])
        ax.plot(n_vals, clauses, marker=markers[m], color=colors[m], label=labels[m], linewidth=1.8, markersize=6)

    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.set_xlabel('Kích thước bàn cờ N')
    ax.set_ylabel('Tổng số mệnh đề CNF (Clauses)')
    ax.set_title('Quy mô mệnh đề CNF của 5 kỹ thuật mã hóa AMO')
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(figs_dir, "fig_clauses_scaling.png"), dpi=300)
    plt.savefig(os.path.join(figs_dir, "fig_clauses_scaling.pdf"))
    plt.close()
    print("Đã tạo biểu đồ: fig_clauses_scaling.png / pdf")

    # 2. Đồ thị Solver Runtime
    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=300)
    solv_markers = {
        "SAT CaDiCaL (Commander)": '^',
        "SAT CaDiCaL (Product)": 'v',
        "SAT CaDiCaL (Sequential)": 's',
        "SAT Glucose 4.2 (Product)": 'o',
        "CP-SAT (OR-Tools, 1w)": 'D',
        "Gurobi 13.0 (1t)": '*',
        "ILP SCIP 9.0": 'x'
    }
    solv_colors = {
        "SAT CaDiCaL (Commander)": '#2ca02c',
        "SAT CaDiCaL (Product)": '#ff7f0e',
        "SAT CaDiCaL (Sequential)": '#1f77b4',
        "SAT Glucose 4.2 (Product)": '#17becf',
        "CP-SAT (OR-Tools, 1w)": '#9467bd',
        "Gurobi 13.0 (1t)": '#8c564b',
        "ILP SCIP 9.0": '#d62728'
    }

    comp_dict = data["solver_comparison"]
    all_solvers = [
        "SAT CaDiCaL (Commander)",
        "SAT CaDiCaL (Product)",
        "SAT CaDiCaL (Sequential)",
        "SAT Glucose 4.2 (Product)",
        "CP-SAT (OR-Tools, 1w)",
        "Gurobi 13.0 (1t)",
        "ILP SCIP 9.0"
    ]

    for s_name in all_solvers:
        n_vals = []
        times = []
        for n_str in ['8', '16', '32', '64', '128', '256', '500', '1000']:
            s_data = comp_dict[n_str].get(s_name, {})
            t = s_data.get("time_s")
            if t is not None:
                n_vals.append(int(n_str))
                times.append(t)
        if n_vals:
            ax.plot(n_vals, times, marker=solv_markers[s_name], color=solv_colors[s_name],
                    label=s_name, linewidth=1.8, markersize=6.5)

    # Vẽ đường Time Limit 300s
    ax.axhline(y=300.0, color='gray', linestyle=':', linewidth=1.5, label='Time limit (300s)')
    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.set_xlabel('Kích thước bàn cờ N')
    ax.set_ylabel('Thời gian giải trung vị (giây - log scale)')
    ax.set_title('So sánh thời gian giải: SAT vs CP-SAT vs Gurobi vs SCIP')
    ax.grid(True, which="both", ls="--", alpha=0.5)
    # Đặt vị trí legend góc dưới bên phải để tránh đè lên đường dữ liệu ở góc trên
    ax.legend(loc='lower right', frameon=True, framealpha=0.9)
    plt.tight_layout()
    plt.savefig(os.path.join(figs_dir, "fig_solver_runtime.png"), dpi=300)
    plt.savefig(os.path.join(figs_dir, "fig_solver_runtime.pdf"))
    plt.close()
    print("Đã tạo biểu đồ: fig_solver_runtime.png / pdf")

    # 3. Bàn cờ 8-Queens
    fig, ax = plt.subplots(figsize=(4.5, 4.5), dpi=300)
    sol_8 = [6, 4, 2, 0, 5, 7, 1, 3]
    board = np.zeros((8, 8))
    for r in range(8):
        for c in range(8):
            board[r, c] = 0.8 if (r + c) % 2 == 1 else 0.2

    ax.imshow(board, cmap='copper', origin='upper')
    for r, c in enumerate(sol_8):
        ax.text(c, r, u'♛', fontsize=26, ha='center', va='center', color='gold', weight='bold')

    ax.set_xticks(range(8))
    ax.set_yticks(range(8))
    ax.set_xticklabels([chr(ord('a') + i) for i in range(8)])
    ax.set_yticklabels(range(1, 9))
    ax.set_title('Nghiệm minh họa N-Queens (N=8)')
    plt.tight_layout()
    plt.savefig(os.path.join(figs_dir, "fig_board_8queens.png"), dpi=300)
    plt.savefig(os.path.join(figs_dir, "fig_board_8queens.pdf"))
    plt.close()
    print("Đã tạo bàn cờ: fig_board_8queens.png / pdf")

if __name__ == "__main__":
    generate_plots()
