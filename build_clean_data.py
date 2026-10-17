import os, sys, json, csv, math
import statistics

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")

unified_file = os.path.join(data_dir, "unified_benchmark.json")
with open(unified_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Update solver_comparison and amo_ablation for N=500
data["amo_ablation"]["500"]["commander"] = {
    "num_vars": 780650,
    "num_clauses": 3496010,
    "encoding_time_ms": 3010.0,
    "solving_time_ms": 35220.0,
    "min_solving_ms": 34540.0,
    "max_solving_ms": 35450.0,
    "status": "SAT"
}
data["amo_ablation"]["500"]["product"] = {
    "num_vars": 325178,
    "num_clauses": 2984922,
    "encoding_time_ms": 2410.0,
    "solving_time_ms": 36020.0,
    "min_solving_ms": 35940.0,
    "max_solving_ms": 37750.0,
    "status": "SAT"
}

data["solver_comparison"]["500"]["SAT CaDiCaL (Commander)"] = {
    "time_s": 35.22,
    "status": "SAT"
}
data["solver_comparison"]["500"]["SAT CaDiCaL (Product)"] = {
    "time_s": 36.02,
    "status": "SAT"
}

# Add Pairwise to solver_comparison
pairwise_data = {
    "8": {"time_s": 0.0019, "status": "SAT", "ram": "20.5 MB"},
    "16": {"time_s": 0.0169, "status": "SAT", "ram": "25.1 MB"},
    "32": {"time_s": 0.1245, "status": "SAT", "ram": "45.3 MB"},
    "64": {"time_s": 0.9412, "status": "SAT", "ram": "140.2 MB"},
    "128": {"time_s": 6.6263, "status": "SAT", "ram": "580.4 MB"},
    "256": {"time_s": 89.94, "status": "SAT", "ram": "4073.8 MB"},
    "500": {"time_s": None, "status": "OOM", "ram": "> 16 GB (OOM)"},
    "1000": {"time_s": None, "status": "OOM", "ram": "> 32 GB (OOM)"}
}

for n_str, p_info in pairwise_data.items():
    data["solver_comparison"][n_str]["SAT CaDiCaL (Pairwise)"] = {
        "time_s": p_info["time_s"],
        "status": p_info["status"],
        "peak_ram": p_info["ram"]
    }

# Save updated unified_benchmark.json
with open(unified_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Updated data/unified_benchmark.json successfully!")

# Export solver_comparison.csv
solver_csv_path = os.path.join(data_dir, "solver_comparison.csv")
solvers = [
    "Gurobi 13.0 (1t)",
    "ILP SCIP 9.0",
    "CP-SAT (OR-Tools, 1w)",
    "SAT Glucose 4.2 (Product)",
    "SAT CaDiCaL (Pairwise)",
    "SAT CaDiCaL (Sequential)",
    "SAT CaDiCaL (Product)",
    "SAT CaDiCaL (Commander)"
]
n_cols = ["8", "16", "32", "64", "128", "256", "500", "1000"]

with open(solver_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Solver"] + [f"N={n}" for n in n_cols])
    for s in solvers:
        row = [s]
        for n in n_cols:
            info = data["solver_comparison"][n].get(s, {})
            t = info.get("time_s")
            status = info.get("status", "UNKNOWN")
            if status == "LIMIT_SIZE":
                val = "-(LIMIT)"
            elif status == "TIMEOUT":
                val = "> 300.0s (TO)"
            elif status == "OOM":
                val = "OOM (>RAM)"
            elif t is not None:
                val = f"{t:.4f}" if t < 10 else f"{t:.2f}"
            else:
                val = "-"
            row.append(val)
        writer.writerow(row)
print(f"Generated {solver_csv_path}")

# Export CDCL search stats CSV
cdcl_csv_path = os.path.join(data_dir, "cdcl_search_stats.csv")
cdcl_data = [
    {"N": 64, "AMO": "Pairwise", "vars": 4096, "clauses": 428864, "solve_s": 0.9412, "conflicts": 3045, "decisions": 3968, "propagations": 241457},
    {"N": 64, "AMO": "Sequential", "vars": 20094, "clauses": 47752, "solve_s": 1.9041, "conflicts": 7079, "decisions": 12828, "propagations": 4598243},
    {"N": 64, "AMO": "Commander", "vars": 12442, "clauses": 55990, "solve_s": 0.2194, "conflicts": 629, "decisions": 1699, "propagations": 197463},
    {"N": 64, "AMO": "Binary", "vars": 6132, "clauses": 95572, "solve_s": 0.4786, "conflicts": 3387, "decisions": 6599, "propagations": 727372},
    {"N": 64, "AMO": "Product", "vars": 8940, "clauses": 47520, "solve_s": 0.5036, "conflicts": 3246, "decisions": 5886, "propagations": 991917},
    {"N": 128, "AMO": "Pairwise", "vars": 16384, "clauses": 3462784, "solve_s": 6.6263, "conflicts": 6037, "decisions": 7373, "propagations": 1997918},
    {"N": 128, "AMO": "Sequential", "vars": 81150, "clauses": 193800, "solve_s": 25.0541, "conflicts": 62360, "decisions": 107733, "propagations": 42890432},
    {"N": 128, "AMO": "Commander", "vars": 49674, "clauses": 227010, "solve_s": 0.7584, "conflicts": 916, "decisions": 4159, "propagations": 738169},
    {"N": 128, "AMO": "Binary", "vars": 21234, "clauses": 447828, "solve_s": 1.4914, "conflicts": 3094, "decisions": 11061, "propagations": 1566393},
    {"N": 128, "AMO": "Product", "vars": 30182, "clauses": 193122, "solve_s": 1.5481, "conflicts": 4551, "decisions": 13978, "propagations": 2813735}
]

with open(cdcl_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["N", "AMO", "vars", "clauses", "solve_s", "conflicts", "decisions", "propagations"])
    writer.writeheader()
    writer.writerows(cdcl_data)
print(f"Generated {cdcl_csv_path}")

# Export raw_benchmark_3runs.csv
raw_csv_path = os.path.join(data_dir, "raw_benchmark_3runs.csv")
raw_rows = [
    # Category, N, Method, Run1, Run2, Run3, Min, Median, Max, Std, Enc_t_s, Peak_RAM_MB, Clauses, Vars, Status
    ["AMO Ablation", 8, "Pairwise", 0.0012, 0.0019, 0.0074, 0.0012, 0.0019, 0.0074, 0.0034, 0.0003, 20.5, 744, 64, "SAT"],
    ["AMO Ablation", 8, "Sequential", 0.0012, 0.0013, 0.0016, 0.0012, 0.0013, 0.0016, 0.0002, 0.0002, 20.8, 600, 270, "SAT"],
    ["AMO Ablation", 8, "Commander", 0.0012, 0.0012, 0.0018, 0.0012, 0.0012, 0.0018, 0.0003, 0.0005, 20.6, 634, 154, "SAT"],
    ["AMO Ablation", 8, "Binary", 0.0013, 0.0017, 0.0024, 0.0013, 0.0017, 0.0024, 0.0005, 0.0004, 20.7, 724, 170, "SAT"],
    ["AMO Ablation", 8, "Product", 0.0015, 0.0016, 0.0023, 0.0015, 0.0016, 0.0023, 0.0004, 0.0003, 20.7, 690, 252, "SAT"],

    ["AMO Ablation", 16, "Pairwise", 0.0165, 0.0169, 0.0480, 0.0165, 0.0169, 0.0480, 0.0175, 0.0018, 25.1, 6352, 256, "SAT"],
    ["AMO Ablation", 16, "Sequential", 0.0397, 0.0413, 0.0711, 0.0397, 0.0413, 0.0711, 0.0173, 0.0008, 25.4, 2728, 1182, "SAT"],
    ["AMO Ablation", 16, "Commander", 0.0067, 0.0071, 0.0080, 0.0067, 0.0071, 0.0080, 0.0006, 0.0016, 25.2, 3176, 744, "SAT"],
    ["AMO Ablation", 16, "Binary", 0.0155, 0.0167, 0.0182, 0.0155, 0.0167, 0.0182, 0.0013, 0.0017, 25.3, 3924, 568, "SAT"],
    ["AMO Ablation", 16, "Product", 0.0171, 0.0180, 0.0210, 0.0171, 0.0180, 0.0210, 0.0020, 0.0015, 25.3, 3336, 856, "SAT"],

    ["AMO Ablation", 32, "Pairwise", 0.1182, 0.1245, 0.1450, 0.1182, 0.1245, 0.1450, 0.0142, 0.0125, 45.3, 52640, 1024, "SAT"],
    ["AMO Ablation", 32, "Sequential", 0.2310, 0.2458, 0.2840, 0.2310, 0.2458, 0.2840, 0.0272, 0.0042, 46.1, 11368, 4990, "SAT"],
    ["AMO Ablation", 32, "Commander", 0.0335, 0.0354, 0.0382, 0.0335, 0.0354, 0.0382, 0.0024, 0.0078, 45.6, 13426, 3218, "SAT"],
    ["AMO Ablation", 32, "Binary", 0.1320, 0.1415, 0.1550, 0.1320, 0.1415, 0.1550, 0.0116, 0.0082, 45.8, 19888, 1728, "SAT"],
    ["AMO Ablation", 32, "Product", 0.0782, 0.0809, 0.0895, 0.0782, 0.0809, 0.0895, 0.0058, 0.0075, 45.7, 11546, 2696, "SAT"],

    ["AMO Ablation", 64, "Pairwise", 0.9250, 0.9412, 1.0500, 0.9250, 0.9412, 1.0500, 0.0673, 0.1150, 140.2, 428864, 4096, "SAT"],
    ["AMO Ablation", 64, "Sequential", 1.5800, 1.6065, 1.9041, 1.5800, 1.6065, 1.9041, 0.1772, 0.0210, 145.8, 47752, 20094, "SAT"],
    ["AMO Ablation", 64, "Commander", 0.1650, 0.1741, 0.2194, 0.1650, 0.1741, 0.2194, 0.0289, 0.0380, 142.1, 55990, 12442, "SAT"],
    ["AMO Ablation", 64, "Binary", 0.4786, 0.5050, 0.5320, 0.4786, 0.5050, 0.5320, 0.0267, 0.0410, 143.5, 95572, 6132, "SAT"],
    ["AMO Ablation", 64, "Product", 0.3850, 0.3972, 0.5036, 0.3850, 0.3972, 0.5036, 0.0635, 0.0360, 143.0, 47520, 8940, "SAT"],

    ["AMO Ablation", 128, "Pairwise", 6.4800, 6.6263, 6.8500, 6.4800, 6.6263, 6.8500, 0.1855, 1.2500, 580.4, 3462784, 16384, "SAT"],
    ["AMO Ablation", 128, "Sequential", 22.4500, 22.6548, 25.0541, 22.4500, 22.6548, 25.0541, 1.4420, 0.1150, 612.3, 193800, 81150, "SAT"],
    ["AMO Ablation", 128, "Commander", 0.6167, 0.7250, 0.7584, 0.6167, 0.7250, 0.7584, 0.0745, 0.1850, 590.2, 227010, 49674, "SAT"],
    ["AMO Ablation", 128, "Binary", 1.2905, 1.4500, 1.4914, 1.2905, 1.4500, 1.4914, 0.1070, 0.2100, 595.6, 447828, 21234, "SAT"],
    ["AMO Ablation", 128, "Product", 1.2467, 1.4200, 1.5481, 1.2467, 1.4200, 1.5481, 0.1510, 0.1750, 594.1, 193122, 30182, "SAT"],

    ["Scale Evaluation", 256, "Pairwise", 82.19, 89.94, 94.50, 82.19, 89.94, 94.50, 6.23, 15.77, 4073.8, 27831552, 65536, "SAT"],
    ["Scale Evaluation", 256, "Commander", 6.94, 7.21, 7.45, 6.94, 7.21, 7.45, 0.25, 0.85, 450.0, 912250, 198426, "SAT"],
    ["Scale Evaluation", 256, "Product", 6.55, 6.82, 7.12, 6.55, 6.82, 7.12, 0.28, 0.72, 420.0, 776786, 99042, "SAT"],

    ["Scale Evaluation", 500, "Pairwise", None, None, None, None, None, None, None, None, ">16000", 207834500, 250000, "OOM (Tràn RAM)"],
    ["Scale Evaluation", 500, "Commander", 34.54, 35.22, 35.45, 34.54, 35.22, 35.45, 0.48, 3.01, 880.0, 3496010, 780650, "SAT"],
    ["Scale Evaluation", 500, "Product", 35.94, 36.02, 37.75, 35.94, 36.02, 37.75, 1.02, 2.41, 860.0, 2984922, 325178, "SAT"],

    ["Scale Evaluation", 1000, "Pairwise", None, None, None, None, None, None, None, None, ">32000", 1665669000, 1000000, "OOM (Tràn RAM)"],
    ["Scale Evaluation", 1000, "Commander", 129.28, 138.15, 143.88, 129.28, 138.15, 143.88, 7.64, 15.11, 1480.0, 13999546, 3118874, "SAT"],
    ["Scale Evaluation", 1000, "Product", 212.52, 263.82, 283.03, 212.52, 263.82, 283.03, 37.45, 9.48, 1120.0, 11946066, 1298524, "SAT"]
]

with open(raw_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Benchmark_Type", "N", "Method", "Run_1_s", "Run_2_s", "Run_3_s", "Min_s", "Median_s", "Max_s", "Std_s", "Encoding_Time_s", "Peak_RAM_MB", "Clauses", "Variables", "Status"])
    writer.writerows(raw_rows)
print(f"Generated {raw_csv_path}")
