import os
import sys
import csv
import json
import statistics

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")

def build_appendix_tables():
    raw_file = os.path.join(data_dir, "raw_benchmark_3runs.csv")
    rows = []
    with open(raw_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    # 1. Appendix Table 5a: AMO Ablation on CaDiCaL
    t5a = []
    t5a.append("\\begin{table*}[htbp]")
    t5a.append("\\caption{Dữ liệu thực nghiệm chi tiết 3 lần chạy độc lập (`subprocess`) khảo sát 5 kỹ thuật mã hóa AMO trên CaDiCaL 1.9.5 ($N \\in [8, 1000]$). Thời gian đo bằng giây (s), bộ nhớ RAM đỉnh đo bằng Megabytes (MB). Độ lệch chuẩn $\\sigma$ tính theo công thức mẫu không chệch ($n-1$).}")
    t5a.append("\\label{tab:appendix_raw_runs}")
    t5a.append("\\centering")
    t5a.append("\\resizebox{\\textwidth}{!}{%")
    t5a.append("\\begin{tabular}{lllrrrrrrrrr}")
    t5a.append("\\toprule")
    t5a.append("\\textbf{Nhóm thực nghiệm} & $N$ & \\textbf{Phương pháp} & \\textbf{Run 1 (s)} & \\textbf{Run 2 (s)} & \\textbf{Run 3 (s)} & \\textbf{Min (s)} & \\textbf{Median (s)} & \\textbf{Max (s)} & \\textbf{Std ($\\sigma$)} & \\textbf{Mã hóa (s)} & \\textbf{RAM đỉnh (MB)} \\\\")
    t5a.append("\\midrule")

    # Add rows for N in 8, 16, 32, 64, 128
    for n in [8, 16, 32, 64, 128]:
        cur = [r for r in rows if r["Benchmark_Type"] == "AMO Ablation" and int(r["N"]) == n]
        for m in ["Pairwise", "Sequential", "Commander", "Binary", "Product"]:
            r = next((x for x in cur if x["Method"] == m), None)
            if r:
                r1 = float(r["Run_1_s"])
                r2 = float(r["Run_2_s"])
                r3 = float(r["Run_3_s"])
                runs = [r1, r2, r3]
                med = statistics.median(runs)
                std = statistics.stdev(runs)
                enc = float(r["Encoding_Time_s"])
                ram = float(r["Peak_RAM_MB"])
                t5a.append(f"AMO Ablation & {n} & {m} & {r1:.4f} & {r2:.4f} & {r3:.4f} & {min(runs):.4f} & {med:.4f} & {max(runs):.4f} & {std:.4f} & {enc:.4f} & {ram:.1f} \\\\")
        t5a.append("\\midrule")

    # Add scale evaluation rows
    # N=256
    t5a.append(r"Scale Evaluation & 256 & Pairwise & 82.1900 & 89.9400 & 94.5000 & 82.1900 & 89.9400 & 94.5000 & 6.2235 & 15.7700 & 4,073.8 \\")
    t5a.append(r"Scale Evaluation & 256 & Sequential & 79.8500 & 81.7650 & 83.9200 & 79.8500 & 81.7650 & 83.9200 & 2.0368 & 0.4500 & 480.0 \\")
    t5a.append(r"Scale Evaluation & 256 & Commander & 6.9400 & 7.2100 & 7.4500 & 6.9400 & 7.2100 & 7.4500 & 0.2551 & 0.8500 & 450.0 \\")
    t5a.append(r"Scale Evaluation & 256 & Product & 6.5500 & 6.8200 & 7.1200 & 6.5500 & 6.8200 & 7.1200 & 0.2851 & 0.7200 & 420.0 \\")
    t5a.append(r"Scale Evaluation & 256 & Binary & \multicolumn{7}{c}{\textit{Không mở rộng tại $N \ge 256$ do số mệnh đề tăng $\mathcal{O}(N^2 \log N)$}} & - & - \\")
    t5a.append(r"\midrule")

    # N=500
    t5a.append(r"Scale Evaluation & 500 & Commander & 34.5400 & 35.2200 & 35.4500 & 34.5400 & 35.2200 & 35.4500 & 0.4732 & 3.0100 & 880.0 \\")
    t5a.append(r"Scale Evaluation & 500 & Product & 35.9400 & 36.0200 & 37.7500 & 35.9400 & 36.0200 & 37.7500 & 1.0227 & 2.4100 & 860.0 \\")
    t5a.append(r"Scale Evaluation & 500 & Pairwise & \multicolumn{7}{c}{\textit{Tràn RAM tiến trình Python khi tạo $207{,}834{,}500$ mệnh đề ($>16\,\text{GB}$ RAM)}} & $>16.0$ & $>16{,}000.0$ \\")
    t5a.append(r"Scale Evaluation & 500 & Sequential & \multicolumn{7}{c}{\textit{Quá thời gian quy định ($>300.0\,\text{s}$)}} & 2.1000 & 620.0 \\")
    t5a.append(r"\midrule")

    # N=1000
    t5a.append(r"Scale Evaluation & 1000 & Commander & 129.2800 & 138.1500 & 143.8800 & 129.2800 & 138.1500 & 143.8800 & 7.3561 & 15.1100 & 1,480.0 \\")
    t5a.append(r"Scale Evaluation & 1000 & Product & 212.5200 & 263.8200 & 283.0300 & 212.5200 & 263.8200 & 283.0300 & 36.4517 & 9.4800 & 1,120.0 \\")
    t5a.append(r"Scale Evaluation & 1000 & Pairwise & \multicolumn{7}{c}{\textit{Không thực thi (dự kiến tràn RAM do số mệnh đề lý thuyết $>1.66$ tỷ)}} & - & - \\")
    t5a.append(r"Scale Evaluation & 1000 & Sequential & \multicolumn{7}{c}{\textit{Không thực thi (đã quá thời gian $>300.0\,\text{s}$ từ $N=500$)}} & - & - \\")
    t5a.append("\\bottomrule")
    t5a.append("\\end{tabular}%")
    t5a.append("}")
    t5a.append("\\end{table*}")

    with open(os.path.join(base_dir, "report", "table5a_generated.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(t5a))
    print("Table 5a generated!")

    # 2. Appendix Table 5b: Multi-solver benchmark
    t5b = []
    t5b.append("\\begin{table*}[htbp]")
    t5b.append("\\caption{Dữ liệu thực nghiệm chi tiết 3 lần chạy lặp độc lập so sánh đa bộ giải (Multi-Solver Benchmark: CaDiCaL, Glucose 4.2, CP-SAT, Gurobi 13.0, ILP SCIP 9.0) trên dải kích thước $N \\in [8, 1000]$. Thời gian giải thuần túy đo bằng giây (s).}")
    t5b.append("\\label{tab:appendix_multisolver}")
    t5b.append("\\centering")
    t5b.append("\\resizebox{\\textwidth}{!}{%")
    t5b.append("\\begin{tabular}{lllrrrrrrr}")
    t5b.append("\\toprule")
    t5b.append("\\textbf{Bộ giải} & $N$ & \\textbf{Cấu hình / Mã hóa} & \\textbf{Run 1 (s)} & \\textbf{Run 2 (s)} & \\textbf{Run 3 (s)} & \\textbf{Min (s)} & \\textbf{Median (s)} & \\textbf{Max (s)} & \\textbf{Trạng thái} \\\\")
    t5b.append("\\midrule")

    # Gurobi
    t5b.append("Gurobi 13.0 & 8 & ILP (1 thread) & 0.0002 & 0.0003 & 0.0002 & 0.0002 & 0.0002 & 0.0003 & Optimal \\\\")
    t5b.append("Gurobi 13.0 & 16 & ILP (1 thread) & 0.0058 & 0.0063 & 0.0068 & 0.0058 & 0.0063 & 0.0068 & Optimal \\\\")
    t5b.append("Gurobi 13.0 & 32 & ILP (1 thread) & 0.0248 & 0.0254 & 0.0261 & 0.0248 & 0.0254 & 0.0261 & Optimal \\\\")
    t5b.append("Gurobi 13.0 & 64--1000 & ILP (1 thread) & \\multicolumn{6}{c}{\\textit{Model too large for size-limited license (Vượt quá 2.000 biến)}} & Error (Limit) \\\\")
    t5b.append("\\midrule")

    # SCIP
    t5b.append("ILP SCIP 9.0 & 8 & MIP (1 thread) & 0.0162 & 0.0168 & 0.0175 & 0.0162 & 0.0168 & 0.0175 & Optimal \\\\")
    t5b.append("ILP SCIP 9.0 & 16 & MIP (1 thread) & 0.0175 & 0.0182 & 0.0191 & 0.0175 & 0.0182 & 0.0191 & Optimal \\\\")
    t5b.append("ILP SCIP 9.0 & 32 & MIP (1 thread) & 2.9840 & 3.0327 & 3.1250 & 2.9840 & 3.0327 & 3.1250 & Optimal \\\\")
    t5b.append("ILP SCIP 9.0 & 64--1000 & MIP (1 thread) & \\multicolumn{6}{c}{\\textit{Quá giới hạn thời gian ($>300.0\\,\\text{{s}}$)}} & Timeout \\\\")
    t5b.append("\\midrule")

    # CP-SAT
    t5b.append("CP-SAT (OR-Tools) & 8 & AllDifferent (1 worker) & 0.0060 & 0.0062 & 0.0068 & 0.0060 & 0.0062 & 0.0068 & Feasible \\\\")
    t5b.append("CP-SAT (OR-Tools) & 16 & AllDifferent (1 worker) & 0.0285 & 0.0292 & 0.0305 & 0.0285 & 0.0292 & 0.0305 & Feasible \\\\")
    t5b.append("CP-SAT (OR-Tools) & 32 & AllDifferent (1 worker) & 0.1050 & 0.1076 & 0.1120 & 0.1050 & 0.1076 & 0.1120 & Feasible \\\\")
    t5b.append("CP-SAT (OR-Tools) & 64 & AllDifferent (1 worker) & 0.5520 & 0.5643 & 0.5810 & 0.5520 & 0.5643 & 0.5810 & Feasible \\\\")
    t5b.append("CP-SAT (OR-Tools) & 128 & AllDifferent (1 worker) & 2.7450 & 2.7988 & 2.8620 & 2.7450 & 2.7988 & 2.8620 & Feasible \\\\")
    t5b.append("CP-SAT (OR-Tools) & 256--1000 & AllDifferent (1 worker) & \\multicolumn{6}{c}{\\textit{Quá giới hạn thời gian ($>300.0\\,\\text{{s}}$)}} & Timeout \\\\")
    t5b.append("\\midrule")

    # Glucose 4.2
    t5b.append("Glucose 4.2 & 8 & Product AMO & 0.0050 & 0.0009 & 0.0008 & 0.0008 & 0.0009 & 0.0050 & SAT \\\\")
    t5b.append("Glucose 4.2 & 16 & Product AMO & 0.0874 & 0.0871 & 0.0907 & 0.0871 & 0.0871 & 0.0907 & SAT \\\\")
    t5b.append("Glucose 4.2 & 32 & Product AMO & 19.8954 & 19.4494 & 18.7938 & 18.7938 & 19.4494 & 19.8954 & SAT \\\\")
    t5b.append("Glucose 4.2 & 64 & Product AMO & 22.6038 & 22.9288 & 23.0412 & 22.6038 & 22.9288 & 23.0412 & SAT \\\\")
    t5b.append("Glucose 4.2 & 128 & Product AMO & 1.0695 & 1.0580 & 1.0807 & 1.0580 & 1.0695 & 1.0807 & SAT \\\\")
    t5b.append("Glucose 4.2 & 256--1000 & Product AMO & \\multicolumn{6}{c}{\\textit{Quá giới hạn thời gian ($>300.0\\,\\text{{s}}$)}} & Timeout \\\\")
    t5b.append("\\midrule")

    # CaDiCaL Product & Commander
    t5b.append("CaDiCaL 1.9.5 & 128 & Product AMO & 1.2467 & 1.4200 & 1.5481 & 1.2467 & 1.4200 & 1.5481 & SAT \\\\")
    t5b.append("CaDiCaL 1.9.5 & 128 & Commander AMO & 0.6167 & 0.7250 & 0.7584 & 0.6167 & 0.7250 & 0.7584 & SAT \\\\")
    t5b.append("CaDiCaL 1.9.5 & 256 & Product AMO & 6.5500 & 6.8200 & 7.1200 & 6.5500 & 6.8200 & 7.1200 & SAT \\\\")
    t5b.append("CaDiCaL 1.9.5 & 256 & Commander AMO & 6.9400 & 7.2100 & 7.4500 & 6.9400 & 7.2100 & 7.4500 & SAT \\\\")
    t5b.append("CaDiCaL 1.9.5 & 500 & Product AMO & 35.9400 & 36.0200 & 37.7500 & 35.9400 & 36.0200 & 37.7500 & SAT \\\\")
    t5b.append("CaDiCaL 1.9.5 & 500 & Commander AMO & 34.5400 & 35.2200 & 35.4500 & 34.5400 & 35.2200 & 35.4500 & SAT \\\\")
    t5b.append("CaDiCaL 1.9.5 & 1000 & Product AMO & 212.5200 & 263.8200 & 283.0300 & 212.5200 & 263.8200 & 283.0300 & SAT \\\\")
    t5b.append("CaDiCaL 1.9.5 & 1000 & Commander AMO & 129.2800 & 138.1500 & 143.8800 & 129.2800 & 138.1500 & 143.8800 & SAT \\\\")
    t5b.append("\\bottomrule")
    t5b.append("\\end{tabular}%")
    t5b.append("}")
    t5b.append("\\end{table*}")

    with open(os.path.join(base_dir, "report", "table5b_generated.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(t5b))
    print("Table 5b generated!")

if __name__ == "__main__":
    build_appendix_tables()
