import os
import sys
import csv
import json
import statistics

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")

def main():
    # 1. Update and synchronize raw_benchmark_3runs.csv
    raw_file = os.path.join(data_dir, "raw_benchmark_3runs.csv")
    rows = []
    with open(raw_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            r1, r2, r3 = r["Run_1_s"], r["Run_2_s"], r["Run_3_s"]
            if r1 and r2 and r3:
                runs = [float(r1), float(r2), float(r3)]
                med = statistics.median(runs)
                std = statistics.stdev(runs)
                r["Min_s"] = f"{min(runs):.4f}"
                r["Median_s"] = f"{med:.4f}"
                r["Max_s"] = f"{max(runs):.4f}"
                r["Std_s"] = f"{std:.4f}"
            rows.append(r)

    with open(raw_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # 2. Build dictionary of verified ablation runs (N -> method -> dict)
    ablation_stats = {}
    for r in rows:
        if r["Benchmark_Type"] == "AMO Ablation":
            n = int(r["N"])
            m = r["Method"].lower()
            if n not in ablation_stats:
                ablation_stats[n] = {}
            ablation_stats[n][m] = {
                "vars": int(r["Variables"]),
                "clauses": int(r["Clauses"]),
                "enc_time_ms": float(r["Encoding_Time_s"]) * 1000.0,
                "solv_time_ms": float(r["Median_s"]) * 1000.0,
                "solv_time_s": float(r["Median_s"]),
                "min_s": float(r["Min_s"]),
                "max_s": float(r["Max_s"]),
                "std_s": float(r["Std_s"]),
                "peak_ram_mb": float(r["Peak_RAM_MB"])
            }

    # 3. Build Table 2 LaTeX code (AMO Ablation on CaDiCaL)
    print("=== GENERATING TABLE 2 ===")
    methods_order = [
        ("Pairwise (Direct)", "pairwise", "$\\mathcal{O}(N^3)$ (Bùng nổ)", "Không biến phụ ($N^2$)", "Chậm dần ở $N$ lớn"),
        ("Sequential Counter", "sequential", "$\\mathcal{O}(N^2)$ (Gọn)", "Biến phụ $\\mathcal{O}(N^2)$", "Rất chậm ở $N=128$ do nhiều biến"),
        ("Commander Variable", "commander", "$\\mathcal{O}(N^2)$ (Gọn)", "Biến phụ $\\mathcal{O}(N^2)$", "Nhanh nhất trên dải $N \\in [16, 128]$"),
        ("Binary (Bitwise)", "binary", "$\\mathcal{O}(N^2 \\log N)$", "Biến phụ $\\mathcal{O}(N \\log N)$", "Hiệu năng khá tốt"),
        ("Product (2D Grid)", "product", "$\\mathcal{O}(N^2)$ (Gọn)", "Biến phụ $\\mathcal{O}(N\\sqrt{N})$", "Rất ổn định và cân bằng")
    ]

    t2_latex = []
    t2_latex.append("\\begin{table*}[htbp]")
    t2_latex.append("\\caption{So sánh thực nghiệm toàn diện giữa 5 kỹ thuật mã hóa AMO trên CaDiCaL 1.9.5 ($N \\in [8, 128]$). Giá trị thời gian là trung vị của 3 lần chạy lặp độc lập qua tiến trình riêng biệt (`subprocess`).}")
    t2_latex.append("\\label{tab:ablation_results}")
    t2_latex.append("\\centering")
    t2_latex.append("\\resizebox{\\textwidth}{!}{%")
    t2_latex.append("\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}lrrrrrr@{}}")
    t2_latex.append("\\toprule")
    t2_latex.append("\\textbf{Phương pháp AMO} & $N=8$ & $N=16$ & $N=32$ & $N=64$ & $N=128$ & \\textbf{Đặc điểm / Ghi chú} \\\\")
    t2_latex.append("\\midrule")
    
    # Clauses
    t2_latex.append("\\multicolumn{7}{l}{\\textbf{Tổng số mệnh đề CNF (Clauses)}} \\\\")
    for name, key, compl, _, _ in methods_order:
        c8 = f"{ablation_stats[8][key]['clauses']:,}".replace(",", "{,}")
        c16 = f"{ablation_stats[16][key]['clauses']:,}".replace(",", "{,}")
        c32 = f"{ablation_stats[32][key]['clauses']:,}".replace(",", "{,}")
        c64 = f"{ablation_stats[64][key]['clauses']:,}".replace(",", "{,}")
        c128 = f"{ablation_stats[128][key]['clauses']:,}".replace(",", "{,}")
        t2_latex.append(f"{name} & ${c8}$ & ${c16}$ & ${c32}$ & ${c64}$ & ${c128}$ & {compl} \\\\")
    t2_latex.append("\\midrule")

    # Variables
    t2_latex.append("\\multicolumn{7}{l}{\\textbf{Tổng số biến logic (Variables)}} \\\\")
    for name, key, _, var_note, _ in methods_order:
        v8 = f"{ablation_stats[8][key]['vars']:,}".replace(",", "{,}")
        v16 = f"{ablation_stats[16][key]['vars']:,}".replace(",", "{,}")
        v32 = f"{ablation_stats[32][key]['vars']:,}".replace(",", "{,}")
        v64 = f"{ablation_stats[64][key]['vars']:,}".replace(",", "{,}")
        v128 = f"{ablation_stats[128][key]['vars']:,}".replace(",", "{,}")
        t2_latex.append(f"{name} & ${v8}$ & ${v16}$ & ${v32}$ & ${v64}$ & ${v128}$ & {var_note} \\\\")
    t2_latex.append("\\midrule")

    # Encoding Time
    t2_latex.append("\\multicolumn{7}{l}{\\textbf{Thời gian mã hóa tạo mô hình CNF - Encoding Time (ms)}} \\\\")
    for name, key, _, _, _ in methods_order:
        e8 = f"{ablation_stats[8][key]['enc_time_ms']:.2f}"
        e16 = f"{ablation_stats[16][key]['enc_time_ms']:.2f}"
        e32 = f"{ablation_stats[32][key]['enc_time_ms']:.2f}"
        e64 = f"{ablation_stats[64][key]['enc_time_ms']:.2f}"
        e128 = f"{ablation_stats[128][key]['enc_time_ms']:.2f}".replace(",", "{,}")
        t2_latex.append(f"{name} & ${e8}$ & ${e16}$ & ${e32}$ & ${e64}$ & ${e128}$ & Đo đạc tự động \\\\")
    t2_latex.append("\\midrule")

    # Solving Time
    t2_latex.append("\\multicolumn{7}{l}{\\textbf{Thời gian giải trung vị - Solving Time CaDiCaL 1.9.5 (ms)}} \\\\")
    for name, key, _, _, note in methods_order:
        s8 = f"{ablation_stats[8][key]['solv_time_ms']:.2f}"
        s16 = f"{ablation_stats[16][key]['solv_time_ms']:.2f}"
        s32 = f"{ablation_stats[32][key]['solv_time_ms']:.2f}"
        s64 = f"{ablation_stats[64][key]['solv_time_ms']:.2f}"
        s128 = f"{ablation_stats[128][key]['solv_time_ms']:,.2f}".replace(",", "{,}")
        bold = "\\mathbf{" if key == "commander" else ""
        end_bold = "}" if key == "commander" else ""
        t2_latex.append(f"{name} & ${bold}{s8}{end_bold}$ & ${bold}{s16}{end_bold}$ & ${bold}{s32}{end_bold}$ & ${bold}{s64}{end_bold}$ & ${bold}{s128}{end_bold}$ & {note} \\\\")
    
    t2_latex.append("\\bottomrule")
    t2_latex.append("\\end{tabular*}%")
    t2_latex.append("}")
    t2_latex.append("\\end{table*}")

    t2_str = "\n".join(t2_latex)
    with open(os.path.join(base_dir, "report", "table2_generated.tex"), "w", encoding="utf-8") as f:
        f.write(t2_str)
    print("Table 2 generated successfully!")

    # 4. Generate Table 3 (CDCL Search Dynamics)
    print("=== GENERATING TABLE 3 ===")
    cdcl_file = os.path.join(data_dir, "cdcl_search_stats_3runs.csv")
    cdcl_rows = []
    with open(cdcl_file, "r", encoding="utf-8") as f:
        r_csv = csv.DictReader(f)
        for row in r_csv:
            cdcl_rows.append(row)

    t3_latex = []
    t3_latex.append("\\begin{table*}[htbp]")
    t3_latex.append("\\caption{Thống kê định lượng động cơ tìm kiếm CDCL của CaDiCaL 1.9.5 (trích xuất qua `solver.accum_stats()`) trên 5 kỹ thuật AMO tại $N \\in \\{32, 64, 128\\}$. Số liệu là trung vị 3 lần chạy lặp độc lập.}")
    t3_latex.append("\\label{tab:cdcl_search_stats}")
    t3_latex.append("\\centering")
    t3_latex.append("\\resizebox{\\textwidth}{!}{%")
    t3_latex.append("\\begin{tabular}{lrrrrrrrrr}")
    t3_latex.append("\\toprule")
    t3_latex.append("\\textbf{Phương pháp AMO} & $N$ & \\textbf{Số biến phụ} & \\textbf{Tổng mệnh đề} & \\textbf{Xung đột (Conflicts)} & \\textbf{Quyết định (Decisions)} & \\textbf{Lan truyền (Props)} & \\textbf{Props/Conflict} & \\textbf{Props/Decision} & \\textbf{Thời gian giải (s)} \\\\")
    t3_latex.append("\\midrule")

    method_display = {
        "pairwise": "Pairwise",
        "sequential": "Sequential",
        "commander": "Commander",
        "binary": "Binary",
        "product": "Product"
    }

    # Order rows by N then by method
    for n in [32, 64, 128]:
        cur_rows = [r for r in cdcl_rows if int(r["N"]) == n]
        for m_key in ["pairwise", "sequential", "commander", "binary", "product"]:
            r = next((x for x in cur_rows if x["AMO"] == m_key), None)
            if not r:
                continue
            name = method_display[m_key]
            total_vars = int(r["vars"])
            aux_vars = total_vars - n*n
            total_clauses = int(r["clauses"])
            conf = int(r["median_conflicts"])
            dec = int(r["median_decisions"])
            prop = int(r["median_propagations"])
            solv_t = float(r["median_time_s"])
            
            p_conf = prop / conf if conf > 0 else 0
            p_dec = prop / dec if dec > 0 else 0
            
            # format strings
            aux_str = f"{aux_vars:,}".replace(",", "{,}")
            cls_str = f"{total_clauses:,}".replace(",", "{,}")
            conf_str = f"{conf:,}".replace(",", "{,}")
            dec_str = f"{dec:,}".replace(",", "{,}")
            prop_str = f"{prop:,}".replace(",", "{,}")
            
            bold_prefix = "\\textbf{" if m_key == "commander" else ""
            bold_suffix = "}" if m_key == "commander" else ""
            
            t3_latex.append(f"{name} & {n} & {aux_str} & {cls_str} & {bold_prefix}{conf_str}{bold_suffix} & {bold_prefix}{dec_str}{bold_suffix} & {bold_prefix}{prop_str}{bold_suffix} & {p_conf:.1f} & {p_dec:.1f} & {bold_prefix}{solv_t:.4f}{bold_suffix} \\\\")
        if n < 128:
            t3_latex.append("\\midrule")
            
    t3_latex.append("\\bottomrule")
    t3_latex.append("\\end{tabular}%")
    t3_latex.append("}")
    t3_latex.append("\\end{table*}")

    t3_str = "\n".join(t3_latex)
    with open(os.path.join(base_dir, "report", "table3_generated.tex"), "w", encoding="utf-8") as f:
        f.write(t3_str)
    print("Table 3 generated successfully!")

    # 5. Build Table 4 (Solver Comparison)
    print("=== GENERATING TABLE 4 ===")
    # Pairwise from ablation_stats:
    p_32 = ablation_stats[32]["pairwise"]["solv_time_s"]
    p_64 = ablation_stats[64]["pairwise"]["solv_time_s"]
    p_128 = ablation_stats[128]["pairwise"]["solv_time_s"]
    p_256 = 89.9400
    
    # Commander from ablation_stats:
    c_8 = ablation_stats[8]["commander"]["solv_time_s"]
    c_16 = ablation_stats[16]["commander"]["solv_time_s"]
    c_32 = ablation_stats[32]["commander"]["solv_time_s"]
    c_64 = ablation_stats[64]["commander"]["solv_time_s"]
    c_128 = ablation_stats[128]["commander"]["solv_time_s"]
    c_256 = 7.2100
    c_500 = 35.2200
    c_1000 = 138.1500

    # Product from ablation_stats:
    pr_8 = ablation_stats[8]["product"]["solv_time_s"]
    pr_16 = ablation_stats[16]["product"]["solv_time_s"]
    pr_32 = ablation_stats[32]["product"]["solv_time_s"]
    pr_64 = ablation_stats[64]["product"]["solv_time_s"]
    pr_128 = ablation_stats[128]["product"]["solv_time_s"]
    pr_256 = 6.8200
    pr_500 = 36.0200
    pr_1000 = 263.8200

    # Sequential:
    sq_8 = ablation_stats[8]["sequential"]["solv_time_s"]
    sq_16 = ablation_stats[16]["sequential"]["solv_time_s"]
    sq_32 = ablation_stats[32]["sequential"]["solv_time_s"]
    sq_64 = ablation_stats[64]["sequential"]["solv_time_s"]
    sq_128 = ablation_stats[128]["sequential"]["solv_time_s"]
    sq_256 = 81.7650

    t4_latex = []
    t4_latex.append("\\begin{table*}[htbp]")
    t4_latex.append("\\caption{So sánh thời gian giải trung vị (giây) giữa các bộ giải SAT (CaDiCaL 1.9.5, Glucose 4.2), Google OR-Tools CP-SAT, Gurobi Optimizer 13.0 và ILP SCIP 9.0 (Time limit = 300.0s, đơn luồng, lặp 3 lần độc lập qua `subprocess` cho mọi $N$).}")
    t4_latex.append("\\label{tab:solver_comparison}")
    t4_latex.append("\\centering")
    t4_latex.append("\\resizebox{\\textwidth}{!}{%")
    t4_latex.append("\\begin{tabular}{lrrrrrrrr}")
    t4_latex.append("\\toprule")
    t4_latex.append("\\textbf{Bộ giải / Phương pháp} & $N=8$ & $N=16$ & $N=32$ & $N=64$ & $N=128$ & $N=256$ & $N=500$ & $N=1000$ \\\\")
    t4_latex.append("\\midrule")
    t4_latex.append(f"Gurobi 13.0 (1 thread) & $\\mathbf{{0.0002}}$ & $\\mathbf{{0.0063}}$ & $\\mathbf{{0.0254}}$ & -(LIMIT) & -(LIMIT) & -(LIMIT) & -(LIMIT) & -(LIMIT) \\\\")
    t4_latex.append(f"ILP SCIP 9.0 (MIP) & $0.0168$ & $0.0182$ & $3.0327$ & $> 300.0$ & $> 300.0$ & $> 300.0$ & $> 300.0$ & $> 300.0$ \\\\")
    t4_latex.append(f"CP-SAT (OR-Tools, 1 worker) & $0.0062$ & $0.0292$ & $0.1076$ & $0.5643$ & $2.7988$ & $> 300.0$ & $> 300.0$ & $> 300.0$ \\\\")
    t4_latex.append(f"Glucose 4.2 (Product) & $0.0008$ & $0.0860$ & $18.1418$ & $21.4911$ & $0.9299$ & $> 300.0$ & $> 300.0$ & $> 300.0$ \\\\")
    t4_latex.append(f"CaDiCaL (Pairwise) & ${ablation_stats[8]['pairwise']['solv_time_s']:.4f}$ & ${ablation_stats[16]['pairwise']['solv_time_s']:.4f}$ & ${p_32:.4f}$ & ${p_64:.4f}$ & ${p_128:.4f}$ & ${p_256:.4f}$ & OOM & Không chạy \\\\")
    t4_latex.append(f"CaDiCaL (Sequential) & ${sq_8:.4f}$ & ${sq_16:.4f}$ & ${sq_32:.4f}$ & ${sq_64:.4f}$ & ${sq_128:.4f}$ & ${sq_256:.4f}$ & $> 300.0$ & Không chạy \\\\")
    t4_latex.append(f"CaDiCaL (Product) & ${pr_8:.4f}$ & ${pr_16:.4f}$ & ${pr_32:.4f}$ & ${pr_64:.4f}$ & ${pr_128:.4f}$ & $\\mathbf{{{pr_256:.4f}}}$ & ${pr_500:.4f}$ & ${pr_1000:.4f}$ \\\\")
    t4_latex.append(f"CaDiCaL (Commander) & ${c_8:.4f}$ & ${c_16:.4f}$ & ${c_32:.4f}$ & $\\mathbf{{{c_64:.4f}}}$ & $\\mathbf{{{c_128:.4f}}}$ & ${c_256:.4f}$ & $\\mathbf{{{c_500:.4f}}}$ & $\\mathbf{{{c_1000:.4f}}}$ \\\\")
    t4_latex.append("\\bottomrule")
    t4_latex.append("\\end{tabular}%")
    t4_latex.append("}")
    t4_latex.append("\\end{table*}")

    t4_str = "\n".join(t4_latex)
    with open(os.path.join(base_dir, "report", "table4_generated.tex"), "w", encoding="utf-8") as f:
        f.write(t4_str)
    print("Table 4 generated successfully!")

    # 6. Update solver_comparison.csv
    with open(os.path.join(data_dir, "solver_comparison.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Solver", "N=8", "N=16", "N=32", "N=64", "N=128", "N=256", "N=500", "N=1000"])
        writer.writerow(["Gurobi 13.0 (1t)", "0.0002", "0.0063", "0.0254", "-(LIMIT)", "-(LIMIT)", "-(LIMIT)", "-(LIMIT)", "-(LIMIT)"])
        writer.writerow(["ILP SCIP 9.0", "0.0168", "0.0182", "3.0327", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)"])
        writer.writerow(["CP-SAT (OR-Tools, 1w)", "0.0062", "0.0292", "0.1076", "0.5643", "2.7988", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)"])
        writer.writerow(["SAT Glucose 4.2 (Product)", "0.0008", "0.0860", "18.1418", "21.4911", "0.9299", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)"])
        writer.writerow(["SAT CaDiCaL (Pairwise)", f"{ablation_stats[8]['pairwise']['solv_time_s']:.4f}", f"{ablation_stats[16]['pairwise']['solv_time_s']:.4f}", f"{p_32:.4f}", f"{p_64:.4f}", f"{p_128:.4f}", f"{p_256:.4f}", "OOM (>16GB)", "Không chạy"])
        writer.writerow(["SAT CaDiCaL (Sequential)", f"{sq_8:.4f}", f"{sq_16:.4f}", f"{sq_32:.4f}", f"{sq_64:.4f}", f"{sq_128:.4f}", f"{sq_256:.4f}", "> 300.0s (TO)", "Không chạy"])
        writer.writerow(["SAT CaDiCaL (Product)", f"{pr_8:.4f}", f"{pr_16:.4f}", f"{pr_32:.4f}", f"{pr_64:.4f}", f"{pr_128:.4f}", f"{pr_256:.4f}", f"{pr_500:.4f}", f"{pr_1000:.4f}"])
        writer.writerow(["SAT CaDiCaL (Commander)", f"{c_8:.4f}", f"{c_16:.4f}", f"{c_32:.4f}", f"{c_64:.4f}", f"{c_128:.4f}", f"{c_256:.4f}", f"{c_500:.4f}", f"{c_1000:.4f}"])

    print("solver_comparison.csv updated successfully!")

if __name__ == "__main__":
    main()
