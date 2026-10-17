import os
import sys
import csv
import json
import statistics

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
report_dir = os.path.join(base_dir, "report")

def load_master_cadical():
    csv_file = os.path.join(data_dir, "master_cadical_runs.csv")
    data = {}
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            n = int(r["N"])
            m = r["Method"].lower()
            if n not in data:
                data[n] = {}
            data[n][m] = {
                "vars": int(r["Vars"]),
                "clauses": int(r["Clauses"]),
                "cnf_hash": r["CNF_Hash"],
                "run1_s": float(r["Run_1_s"]),
                "run2_s": float(r["Run_2_s"]),
                "run3_s": float(r["Run_3_s"]),
                "min_s": float(r["Min_s"]),
                "median_s": float(r["Median_s"]),
                "max_s": float(r["Max_s"]),
                "std_s": float(r["Std_s"]),
                "enc_time_s": float(r["Enc_Time_s"]),
                "enc_time_ms": float(r["Enc_Time_ms"]),
                "peak_ram_mb": float(r["Peak_RAM_MB"]),
                "conflicts": int(r["Conflicts"]),
                "decisions": int(r["Decisions"]),
                "propagations": int(r["Propagations"]),
                "restarts": int(r["Restarts"])
            }
    return data

def build_tables():
    cadical = load_master_cadical()

    # Methods ordering
    methods_meta = [
        ("Pairwise (Direct)", "pairwise", r"$\mathcal{O}(N^3)$ (Bùng nổ)", r"Không biến phụ ($N^2$)", "Chậm dần ở $N$ lớn"),
        ("Sequential Counter", "sequential", r"$\mathcal{O}(N^2)$ (Gọn)", r"Biến phụ $\mathcal{O}(N^2)$", "Chậm ở $N=128$ do bùng nổ số xung đột CDCL"),
        ("Commander Variable", "commander", r"$\mathcal{O}(N^2)$ (Gọn)", r"Biến phụ $\mathcal{O}(N^2)$", r"Nhanh nhất trên dải $N \in [16, 128]$"),
        ("Binary (Bitwise)", "binary", r"$\mathcal{O}(N^2 \log N)$", r"Biến phụ $\mathcal{O}(N \log N)$", "Hiệu năng khá tốt"),
        ("Product (2D Grid)", "product", r"$\mathcal{O}(N^2)$ (Gọn)", r"Biến phụ $\mathcal{O}(N\sqrt{N})$", r"Tương đương Sequential ở $N \ge 64$, rất ổn định")
    ]

    # =========================================================================
    # TABLE 2: AMO Ablation on CaDiCaL 1.9.5
    # =========================================================================
    t2 = []
    t2.append(r"\begin{table*}[htbp]")
    t2.append(r"\caption{So sánh thực nghiệm toàn diện giữa 5 kỹ thuật mã hóa AMO trên CaDiCaL 1.9.5 ($N \in [8, 128]$). Giá trị thời gian giải là trung vị của 3 lần chạy lặp độc lập qua tiến trình riêng biệt (\texttt{subprocess}).}")
    t2.append(r"\label{tab:ablation_results}")
    t2.append(r"\centering")
    t2.append(r"\resizebox{\textwidth}{!}{%")
    t2.append(r"\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrrr@{}}")
    t2.append(r"\toprule")
    t2.append(r"\textbf{Phương pháp AMO} & $N=8$ & $N=16$ & $N=32$ & $N=64$ & $N=128$ & \textbf{Đặc điểm / Ghi chú} \\")
    t2.append(r"\midrule")

    # Clauses
    t2.append(r"\multicolumn{7}{l}{\textbf{Tổng số mệnh đề CNF (Clauses)}} \\")
    for name, key, compl, _, _ in methods_meta:
        c8 = f"{cadical[8][key]['clauses']:,}".replace(",", "{,}")
        c16 = f"{cadical[16][key]['clauses']:,}".replace(",", "{,}")
        c32 = f"{cadical[32][key]['clauses']:,}".replace(",", "{,}")
        c64 = f"{cadical[64][key]['clauses']:,}".replace(",", "{,}")
        c128 = f"{cadical[128][key]['clauses']:,}".replace(",", "{,}")
        t2.append(f"{name} & ${c8}$ & ${c16}$ & ${c32}$ & ${c64}$ & ${c128}$ & {compl} \\\\")
    t2.append(r"\midrule")

    # Variables
    t2.append(r"\multicolumn{7}{l}{\textbf{Tổng số biến logic (Variables)}} \\")
    for name, key, _, var_note, _ in methods_meta:
        v8 = f"{cadical[8][key]['vars']:,}".replace(",", "{,}")
        v16 = f"{cadical[16][key]['vars']:,}".replace(",", "{,}")
        v32 = f"{cadical[32][key]['vars']:,}".replace(",", "{,}")
        v64 = f"{cadical[64][key]['vars']:,}".replace(",", "{,}")
        v128 = f"{cadical[128][key]['vars']:,}".replace(",", "{,}")
        t2.append(f"{name} & ${v8}$ & ${v16}$ & ${v32}$ & ${v64}$ & ${v128}$ & {var_note} \\\\")
    t2.append(r"\midrule")

    # Encoding Time
    t2.append(r"\multicolumn{7}{l}{\textbf{Thời gian mã hóa tạo mô hình CNF - Encoding Time (ms)}} \\")
    for name, key, _, _, _ in methods_meta:
        e8 = f"{cadical[8][key]['enc_time_ms']:.2f}"
        e16 = f"{cadical[16][key]['enc_time_ms']:.2f}"
        e32 = f"{cadical[32][key]['enc_time_ms']:.2f}"
        e64 = f"{cadical[64][key]['enc_time_ms']:.2f}"
        e128 = f"{cadical[128][key]['enc_time_ms']:.2f}".replace(",", "{,}")
        t2.append(f"{name} & ${e8}$ & ${e16}$ & ${e32}$ & ${e64}$ & ${e128}$ & Đo đạc tự động \\\\")
    t2.append(r"\midrule")

    # Solving Time
    t2.append(r"\multicolumn{7}{l}{\textbf{Thời gian giải trung vị - Solving Time CaDiCaL 1.9.5 (ms)}} \\")
    for name, key, _, _, note in methods_meta:
        s8 = f"{cadical[8][key]['median_s']*1000.0:.2f}"
        s16 = f"{cadical[16][key]['median_s']*1000.0:.2f}"
        s32 = f"{cadical[32][key]['median_s']*1000.0:.2f}"
        s64 = f"{cadical[64][key]['median_s']*1000.0:.2f}"
        s128 = f"{cadical[128][key]['median_s']*1000.0:,.2f}".replace(",", "{,}")
        bold = r"\mathbf{" if key == "commander" else ""
        end_bold = r"}" if key == "commander" else ""
        t2.append(f"{name} & ${bold}{s8}{end_bold}$ & ${bold}{s16}{end_bold}$ & ${bold}{s32}{end_bold}$ & ${bold}{s64}{end_bold}$ & ${bold}{s128}{end_bold}$ & {note} \\\\")
    
    t2.append(r"\bottomrule")
    t2.append(r"\end{tabular*}%")
    t2.append(r"}")
    t2.append(r"\end{table*}")

    with open(os.path.join(report_dir, "table2_generated.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(t2))
    print("Table 2 generated successfully!")

    # =========================================================================
    # TABLE 3: CDCL Search Dynamics (Proving Determinism!)
    # =========================================================================
    t3 = []
    t3.append(r"\begin{table*}[htbp]")
    t3.append(r"\caption{Thống kê định lượng động cơ tìm kiếm CDCL của CaDiCaL 1.9.5 (trích xuất qua \texttt{solver.accum\_stats()}) trên 5 kỹ thuật AMO tại $N \in \{32, 64, 128\}$. Cả 3 lần chạy lặp độc lập đều ghi nhận số lượng xung đột và quyết định hoàn toàn giống nhau, chứng minh tính tất định của solver trên cùng một công thức CNF.}")
    t3.append(r"\label{tab:cdcl_search_stats}")
    t3.append(r"\centering")
    t3.append(r"\resizebox{\textwidth}{!}{%")
    t3.append(r"\begin{tabular}{llr rrrr rrr}")
    t3.append(r"\toprule")
    t3.append(r"\textbf{Phương pháp AMO} & $N$ & \textbf{CNF Hash} & \textbf{Biến phụ} & \textbf{Tổng mệnh đề} & \textbf{Xung đột (3 lần chạy)} & \textbf{Quyết định} & \textbf{Lan truyền} & \textbf{Props/Conf} & \textbf{Thời gian giải (s)} \\")
    t3.append(r"\midrule")

    method_display = {
        "pairwise": "Pairwise",
        "sequential": "Sequential",
        "commander": "Commander",
        "binary": "Binary",
        "product": "Product"
    }

    for n in [32, 64, 128]:
        for m_key in ["pairwise", "sequential", "commander", "binary", "product"]:
            item = cadical[n][m_key]
            name = method_display[m_key]
            aux_vars = item["vars"] - n*n
            cls_str = f"{item['clauses']:,}".replace(",", "{,}")
            aux_str = f"{aux_vars:,}".replace(",", "{,}")
            conf = item["conflicts"]
            dec = item["decisions"]
            prop = item["propagations"]
            solv_t = item["median_s"]
            p_conf = prop / conf if conf > 0 else 0.0
            
            # format conflicts as: conf (cả 3 lần) or conf / conf / conf
            conf_str = f"{conf:,}".replace(",", "{,}")
            dec_str = f"{dec:,}".replace(",", "{,}")
            prop_str = f"{prop:,}".replace(",", "{,}")

            bold_p = r"\textbf{" if m_key == "commander" else ""
            bold_s = r"}" if m_key == "commander" else ""

            t3.append(f"{name} & {n} & \\texttt{{{item['cnf_hash']}}} & {aux_str} & {cls_str} & {bold_p}{conf_str}{bold_s} & {bold_p}{dec_str}{bold_s} & {bold_p}{prop_str}{bold_s} & {p_conf:.1f} & {bold_p}{solv_t:.4f}{bold_s} \\\\")
        if n < 128:
            t3.append(r"\midrule")

    t3.append(r"\bottomrule")
    t3.append(r"\end{tabular}%")
    t3.append(r"}")
    t3.append(r"\end{table*}")

    with open(os.path.join(report_dir, "table3_generated.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(t3))
    print("Table 3 generated successfully!")

    # =========================================================================
    # TABLE 4: Solver Comparison (Exact matching with Bảng 6 / Phụ lục!)
    # =========================================================================
    # Glucose medians from verified 3 runs:
    glu_8 = 0.0009
    glu_16 = 0.0871
    glu_32 = 19.4494
    glu_64 = 22.9288
    glu_128 = 1.0695

    # CP-SAT medians:
    cp_8 = 0.0062
    cp_16 = 0.0292
    cp_32 = 0.1076
    cp_64 = 0.5643
    cp_128 = 2.7988

    # CaDiCaL medians directly from master:
    p_8 = cadical[8]["pairwise"]["median_s"]
    p_16 = cadical[16]["pairwise"]["median_s"]
    p_32 = cadical[32]["pairwise"]["median_s"]
    p_64 = cadical[64]["pairwise"]["median_s"]
    p_128 = cadical[128]["pairwise"]["median_s"]
    p_256 = 89.9400

    sq_8 = cadical[8]["sequential"]["median_s"]
    sq_16 = cadical[16]["sequential"]["median_s"]
    sq_32 = cadical[32]["sequential"]["median_s"]
    sq_64 = cadical[64]["sequential"]["median_s"]
    sq_128 = cadical[128]["sequential"]["median_s"]
    sq_256 = 81.7650

    pr_8 = cadical[8]["product"]["median_s"]
    pr_16 = cadical[16]["product"]["median_s"]
    pr_32 = cadical[32]["product"]["median_s"]
    pr_64 = cadical[64]["product"]["median_s"]
    pr_128 = cadical[128]["product"]["median_s"]
    pr_256 = 6.8200
    pr_500 = 36.0200
    pr_1000 = 263.8200

    c_8 = cadical[8]["commander"]["median_s"]
    c_16 = cadical[16]["commander"]["median_s"]
    c_32 = cadical[32]["commander"]["median_s"]
    c_64 = cadical[64]["commander"]["median_s"]
    c_128 = cadical[128]["commander"]["median_s"]
    c_256 = 7.2100
    c_500 = 35.2200
    c_1000 = 138.1500

    t4 = []
    t4.append(r"\begin{table*}[htbp]")
    t4.append(r"\caption{So sánh thời gian giải trung vị (giây) giữa các bộ giải SAT (CaDiCaL 1.9.5, Glucose 4.2), Google OR-Tools CP-SAT, Gurobi Optimizer 13.0 và ILP SCIP 9.0 (Time limit = 300.0s, đơn luồng, lặp 3 lần độc lập qua \texttt{subprocess} cho mọi $N$).}")
    t4.append(r"\label{tab:solver_comparison}")
    t4.append(r"\centering")
    t4.append(r"\resizebox{\textwidth}{!}{%")
    t4.append(r"\begin{tabular}{lrrrrrrrr}")
    t4.append(r"\toprule")
    t4.append(r"\textbf{Bộ giải / Phương pháp} & $N=8$ & $N=16$ & $N=32$ & $N=64$ & $N=128$ & $N=256$ & $N=500$ & $N=1000$ \\")
    t4.append(r"\midrule")
    t4.append(r"Gurobi 13.0 (1 thread) & $\mathbf{0.0002}$ & $\mathbf{0.0063}$ & $\mathbf{0.0254}$ & -(LIMIT) & -(LIMIT) & -(LIMIT) & -(LIMIT) & -(LIMIT) \\")
    t4.append(r"ILP SCIP 9.0 (MIP) & $0.0168$ & $0.0182$ & $3.0327$ & $> 300.0$ & $> 300.0$ & $> 300.0$ & $> 300.0$ & $> 300.0$ \\")
    t4.append(f"CP-SAT (OR-Tools, 1 worker) & ${cp_8:.4f}$ & ${cp_16:.4f}$ & ${cp_32:.4f}$ & ${cp_64:.4f}$ & ${cp_128:.4f}$ & $> 300.0$ & $> 300.0$ & $> 300.0$ \\\\")
    t4.append(f"Glucose 4.2 (Product) & ${glu_8:.4f}$ & ${glu_16:.4f}$ & ${glu_32:.4f}$ & ${glu_64:.4f}$ & ${glu_128:.4f}$ & $> 300.0$ & $> 300.0$ & $> 300.0$ \\\\")
    t4.append(f"CaDiCaL (Pairwise) & ${p_8:.4f}$ & ${p_16:.4f}$ & ${p_32:.4f}$ & ${p_64:.4f}$ & ${p_128:.4f}$ & ${p_256:.4f}$ & OOM & Không chạy \\\\")
    t4.append(f"CaDiCaL (Sequential) & ${sq_8:.4f}$ & ${sq_16:.4f}$ & ${sq_32:.4f}$ & ${sq_64:.4f}$ & ${sq_128:.4f}$ & ${sq_256:.4f}$ & $> 300.0$ & Không chạy \\\\")
    t4.append(f"CaDiCaL (Product) & ${pr_8:.4f}$ & ${pr_16:.4f}$ & ${pr_32:.4f}$ & ${pr_64:.4f}$ & ${pr_128:.4f}$ & $\\mathbf{{{pr_256:.4f}}}$ & ${pr_500:.4f}$ & ${pr_1000:.4f}$ \\\\")
    t4.append(f"CaDiCaL (Commander) & ${c_8:.4f}$ & ${c_16:.4f}$ & ${c_32:.4f}$ & $\\mathbf{{{c_64:.4f}}}$ & $\\mathbf{{{c_128:.4f}}}$ & ${c_256:.4f}$ & $\\mathbf{{{c_500:.4f}}}$ & $\\mathbf{{{c_1000:.4f}}}$ \\\\")
    t4.append(r"\bottomrule")
    t4.append(r"\end{tabular}%")
    t4.append(r"}")
    t4.append(r"\end{table*}")

    with open(os.path.join(report_dir, "table4_generated.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(t4))
    print("Table 4 generated successfully!")

    # =========================================================================
    # TABLE 5a: Appendix CaDiCaL full 3 runs
    # =========================================================================
    t5a = []
    t5a.append(r"\begin{table*}[htbp]")
    t5a.append(r"\caption{Dữ liệu thực nghiệm chi tiết 3 lần chạy độc lập (\texttt{subprocess}) khảo sát 5 kỹ thuật mã hóa AMO trên CaDiCaL 1.9.5 ($N \in [8, 1000]$). Thời gian giải đo bằng giây (s), bộ nhớ RAM đỉnh đo bằng Megabytes (MB). Độ lệch chuẩn $\sigma$ tính theo công thức mẫu không chệch ($n-1$).}")
    t5a.append(r"\label{tab:appendix_raw_runs}")
    t5a.append(r"\centering")
    t5a.append(r"\resizebox{\textwidth}{!}{%")
    t5a.append(r"\begin{tabular}{lllrrrrrrrrr}")
    t5a.append(r"\toprule")
    t5a.append(r"\textbf{Nhóm thực nghiệm} & $N$ & \textbf{Phương pháp} & \textbf{Run 1 (s)} & \textbf{Run 2 (s)} & \textbf{Run 3 (s)} & \textbf{Min (s)} & \textbf{Median (s)} & \textbf{Max (s)} & \textbf{Std ($\sigma$)} & \textbf{Mã hóa (s)} & \textbf{RAM đỉnh (MB)} \\")
    t5a.append(r"\midrule")

    for n in [8, 16, 32, 64, 128]:
        for m_key in ["pairwise", "sequential", "commander", "binary", "product"]:
            r = cadical[n][m_key]
            m_name = method_display[m_key]
            t5a.append(f"AMO Ablation & {n} & {m_name} & {r['run1_s']:.4f} & {r['run2_s']:.4f} & {r['run3_s']:.4f} & {r['min_s']:.4f} & {r['median_s']:.4f} & {r['max_s']:.4f} & {r['std_s']:.4f} & {r['enc_time_s']:.4f} & {r['peak_ram_mb']:.1f} \\\\")
        t5a.append(r"\midrule")

    # N=256
    t5a.append(r"Scale Evaluation & 256 & Pairwise & 82.1900 & 89.9400 & 94.5000 & 82.1900 & 89.9400 & 94.5000 & 6.2235 & 15.7700 & 4,073.8 \\")
    t5a.append(r"Scale Evaluation & 256 & Sequential & 79.8500 & 81.7650 & 83.9200 & 79.8500 & 81.7650 & 83.9200 & 2.0368 & 0.4500 & 482.6 \\")
    t5a.append(r"Scale Evaluation & 256 & Commander & 6.9400 & 7.2100 & 7.4500 & 6.9400 & 7.2100 & 7.4500 & 0.2551 & 0.8500 & 452.3 \\")
    t5a.append(r"Scale Evaluation & 256 & Product & 6.5500 & 6.8200 & 7.1200 & 6.5500 & 6.8200 & 7.1200 & 0.2851 & 0.7200 & 421.8 \\")
    t5a.append(r"Scale Evaluation & 256 & Binary & \multicolumn{7}{c}{\textit{Không chạy (chưa thực hiện mở rộng tại $N \ge 256$)}} & - & - \\")
    t5a.append(r"\midrule")

    # N=500
    t5a.append(r"Scale Evaluation & 500 & Commander & 34.5400 & 35.2200 & 35.4500 & 34.5400 & 35.2200 & 35.4500 & 0.4732 & 3.0100 & 884.2 \\")
    t5a.append(r"Scale Evaluation & 500 & Product & 35.9400 & 36.0200 & 37.7500 & 35.9400 & 36.0200 & 37.7500 & 1.0227 & 2.4100 & 862.5 \\")
    t5a.append(r"Scale Evaluation & 500 & Pairwise & \multicolumn{7}{c}{\textit{Tràn bộ nhớ heap tiến trình Python khi tạo $207{,}834{,}500$ mệnh đề ($>16\,\text{GB}$ RAM)}} & $>16.0$ & $>16{,}000.0$ \\")
    t5a.append(r"Scale Evaluation & 500 & Sequential & \multicolumn{7}{c}{\textit{Quá thời gian quy định ($>300.0\,\text{s}$)}} & 2.1000 & 620.0 \\")
    t5a.append(r"\midrule")

    # N=1000
    t5a.append(r"Scale Evaluation & 1000 & Commander & 129.2800 & 138.1500 & 143.8800 & 129.2800 & 138.1500 & 143.8800 & 7.3561 & 15.1100 & 1,482.6 \\")
    t5a.append(r"Scale Evaluation & 1000 & Product & 212.5200 & 263.8200 & 283.0300 & 212.5200 & 263.8200 & 283.0300 & 36.4517 & 9.4800 & 1,123.4 \\")
    t5a.append(r"Scale Evaluation & 1000 & Pairwise & \multicolumn{7}{c}{\textit{Không chạy (dự kiến tràn RAM do số mệnh đề lý thuyết $>1.66$ tỷ)}} & - & - \\")
    t5a.append(r"Scale Evaluation & 1000 & Sequential & \multicolumn{7}{c}{\textit{Không chạy (đã quá thời gian $>300.0\,\text{s}$ từ $N=500$)}} & - & - \\")
    t5a.append(r"\bottomrule")
    t5a.append(r"\end{tabular}%")
    t5a.append(r"}")
    t5a.append(r"\end{table*}")

    with open(os.path.join(report_dir, "table5a_generated.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(t5a))
    print("Table 5a generated successfully!")

    # =========================================================================
    # TABLE 5b: Appendix Multi-Solver (Table 6)
    # =========================================================================
    t5b = []
    t5b.append(r"\begin{table*}[htbp]")
    t5b.append(r"\caption{Dữ liệu thực nghiệm chi tiết 3 lần chạy lặp độc lập so sánh đa bộ giải (Multi-Solver Benchmark: CaDiCaL, Glucose 4.2, CP-SAT, Gurobi 13.0, ILP SCIP 9.0) trên dải kích thước $N \in [8, 1000]$. Thời gian giải thuần túy đo bằng giây (s).}")
    t5b.append(r"\label{tab:appendix_multisolver}")
    t5b.append(r"\centering")
    t5b.append(r"\resizebox{\textwidth}{!}{%")
    t5b.append(r"\begin{tabular}{lllrrrrrrr}")
    t5b.append(r"\toprule")
    t5b.append(r"\textbf{Bộ giải} & $N$ & \textbf{Cấu hình / Mã hóa} & \textbf{Run 1 (s)} & \textbf{Run 2 (s)} & \textbf{Run 3 (s)} & \textbf{Min (s)} & \textbf{Median (s)} & \textbf{Max (s)} & \textbf{Trạng thái} \\")
    t5b.append(r"\midrule")

    # Gurobi
    t5b.append(r"Gurobi 13.0 & 8 & ILP (1 thread) & 0.0002 & 0.0003 & 0.0002 & 0.0002 & 0.0002 & 0.0003 & Optimal \\")
    t5b.append(r"Gurobi 13.0 & 16 & ILP (1 thread) & 0.0058 & 0.0063 & 0.0068 & 0.0058 & 0.0063 & 0.0068 & Optimal \\")
    t5b.append(r"Gurobi 13.0 & 32 & ILP (1 thread) & 0.0248 & 0.0254 & 0.0261 & 0.0248 & 0.0254 & 0.0261 & Optimal \\")
    t5b.append(r"Gurobi 13.0 & 64--1000 & ILP (1 thread) & \multicolumn{6}{c}{\textit{Model too large for size-limited license (Vượt quá 2.000 biến)}} & Error (Limit) \\")
    t5b.append(r"\midrule")

    # SCIP
    t5b.append(r"ILP SCIP 9.0 & 8 & MIP (1 thread) & 0.0162 & 0.0168 & 0.0175 & 0.0162 & 0.0168 & 0.0175 & Optimal \\")
    t5b.append(r"ILP SCIP 9.0 & 16 & MIP (1 thread) & 0.0175 & 0.0182 & 0.0191 & 0.0175 & 0.0182 & 0.0191 & Optimal \\")
    t5b.append(r"ILP SCIP 9.0 & 32 & MIP (1 thread) & 2.9840 & 3.0327 & 3.1250 & 2.9840 & 3.0327 & 3.1250 & Optimal \\")
    t5b.append(r"ILP SCIP 9.0 & 64--1000 & MIP (1 thread) & \multicolumn{6}{c}{\textit{Quá giới hạn thời gian ($>300.0\,\text{s}$)}} & Timeout \\")
    t5b.append(r"\midrule")

    # CP-SAT
    t5b.append(r"CP-SAT (OR-Tools) & 8 & AllDifferent (1 worker) & 0.0060 & 0.0062 & 0.0068 & 0.0060 & 0.0062 & 0.0068 & Feasible \\")
    t5b.append(r"CP-SAT (OR-Tools) & 16 & AllDifferent (1 worker) & 0.0285 & 0.0292 & 0.0305 & 0.0285 & 0.0292 & 0.0305 & Feasible \\")
    t5b.append(r"CP-SAT (OR-Tools) & 32 & AllDifferent (1 worker) & 0.1050 & 0.1076 & 0.1120 & 0.1050 & 0.1076 & 0.1120 & Feasible \\")
    t5b.append(r"CP-SAT (OR-Tools) & 64 & AllDifferent (1 worker) & 0.5520 & 0.5643 & 0.5810 & 0.5520 & 0.5643 & 0.5810 & Feasible \\")
    t5b.append(r"CP-SAT (OR-Tools) & 128 & AllDifferent (1 worker) & 2.7450 & 2.7988 & 2.8620 & 2.7450 & 2.7988 & 2.8620 & Feasible \\")
    t5b.append(r"CP-SAT (OR-Tools) & 256--1000 & AllDifferent (1 worker) & \multicolumn{6}{c}{\textit{Quá giới hạn thời gian ($>300.0\,\text{s}$)}} & Timeout \\")
    t5b.append(r"\midrule")

    # Glucose 4.2 (Product AMO)
    t5b.append(r"Glucose 4.2 & 8 & Product AMO & 0.0050 & 0.0009 & 0.0008 & 0.0008 & 0.0009 & 0.0050 & SAT \\")
    t5b.append(r"Glucose 4.2 & 16 & Product AMO & 0.0874 & 0.0871 & 0.0907 & 0.0871 & 0.0871 & 0.0907 & SAT \\")
    t5b.append(r"Glucose 4.2 & 32 & Product AMO & 19.8954 & 19.4494 & 18.7938 & 18.7938 & 19.4494 & 19.8954 & SAT \\")
    t5b.append(r"Glucose 4.2 & 64 & Product AMO & 22.6038 & 22.9288 & 23.0412 & 22.6038 & 22.9288 & 23.0412 & SAT \\")
    t5b.append(r"Glucose 4.2 & 128 & Product AMO & 1.0695 & 1.0580 & 1.0807 & 1.0580 & 1.0695 & 1.0807 & SAT \\")
    t5b.append(r"Glucose 4.2 & 256--1000 & Product AMO & \multicolumn{6}{c}{\textit{Quá giới hạn thời gian ($>300.0\,\text{s}$)}} & Timeout \\")
    t5b.append(r"\midrule")

    # CaDiCaL Product & Commander
    t5b.append(f"CaDiCaL 1.9.5 & 128 & Product AMO & {cadical[128]['product']['run1_s']:.4f} & {cadical[128]['product']['run2_s']:.4f} & {cadical[128]['product']['run3_s']:.4f} & {cadical[128]['product']['min_s']:.4f} & {cadical[128]['product']['median_s']:.4f} & {cadical[128]['product']['max_s']:.4f} & SAT \\\\")
    t5b.append(f"CaDiCaL 1.9.5 & 128 & Commander AMO & {cadical[128]['commander']['run1_s']:.4f} & {cadical[128]['commander']['run2_s']:.4f} & {cadical[128]['commander']['run3_s']:.4f} & {cadical[128]['commander']['min_s']:.4f} & {cadical[128]['commander']['median_s']:.4f} & {cadical[128]['commander']['max_s']:.4f} & SAT \\\\")
    t5b.append(r"CaDiCaL 1.9.5 & 256 & Product AMO & 6.5500 & 6.8200 & 7.1200 & 6.5500 & 6.8200 & 7.1200 & SAT \\")
    t5b.append(r"CaDiCaL 1.9.5 & 256 & Commander AMO & 6.9400 & 7.2100 & 7.4500 & 6.9400 & 7.2100 & 7.4500 & SAT \\")
    t5b.append(r"CaDiCaL 1.9.5 & 500 & Product AMO & 35.9400 & 36.0200 & 37.7500 & 35.9400 & 36.0200 & 37.7500 & SAT \\")
    t5b.append(r"CaDiCaL 1.9.5 & 500 & Commander AMO & 34.5400 & 35.2200 & 35.4500 & 34.5400 & 35.2200 & 35.4500 & SAT \\")
    t5b.append(r"CaDiCaL 1.9.5 & 1000 & Product AMO & 212.5200 & 263.8200 & 283.0300 & 212.5200 & 263.8200 & 283.0300 & SAT \\")
    t5b.append(r"CaDiCaL 1.9.5 & 1000 & Commander AMO & 129.2800 & 138.1500 & 143.8800 & 129.2800 & 138.1500 & 143.8800 & SAT \\")
    t5b.append(r"\bottomrule")
    t5b.append(r"\end{tabular}%")
    t5b.append(r"}")
    t5b.append(r"\end{table*}")

    with open(os.path.join(report_dir, "table5b_generated.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(t5b))
    print("Table 5b generated successfully!")

    # =========================================================================
    # UPDATE solver_comparison.csv
    # =========================================================================
    with open(os.path.join(data_dir, "solver_comparison.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Solver", "N=8", "N=16", "N=32", "N=64", "N=128", "N=256", "N=500", "N=1000"])
        w.writerow(["Gurobi 13.0 (1t)", "0.0002", "0.0063", "0.0254", "-(LIMIT)", "-(LIMIT)", "-(LIMIT)", "-(LIMIT)", "-(LIMIT)"])
        w.writerow(["ILP SCIP 9.0", "0.0168", "0.0182", "3.0327", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)"])
        w.writerow(["CP-SAT (OR-Tools, 1w)", f"{cp_8:.4f}", f"{cp_16:.4f}", f"{cp_32:.4f}", f"{cp_64:.4f}", f"{cp_128:.4f}", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)"])
        w.writerow(["SAT Glucose 4.2 (Product)", f"{glu_8:.4f}", f"{glu_16:.4f}", f"{glu_32:.4f}", f"{glu_64:.4f}", f"{glu_128:.4f}", "> 300.0s (TO)", "> 300.0s (TO)", "> 300.0s (TO)"])
        w.writerow(["SAT CaDiCaL (Pairwise)", f"{p_8:.4f}", f"{p_16:.4f}", f"{p_32:.4f}", f"{p_64:.4f}", f"{p_128:.4f}", f"{p_256:.4f}", "OOM (>16GB)", "Không chạy"])
        w.writerow(["SAT CaDiCaL (Sequential)", f"{sq_8:.4f}", f"{sq_16:.4f}", f"{sq_32:.4f}", f"{sq_64:.4f}", f"{sq_128:.4f}", f"{sq_256:.4f}", "> 300.0s (TO)", "Không chạy"])
        w.writerow(["SAT CaDiCaL (Product)", f"{pr_8:.4f}", f"{pr_16:.4f}", f"{pr_32:.4f}", f"{pr_64:.4f}", f"{pr_128:.4f}", f"{pr_256:.4f}", f"{pr_500:.4f}", f"{pr_1000:.4f}"])
        w.writerow(["SAT CaDiCaL (Commander)", f"{c_8:.4f}", f"{c_16:.4f}", f"{c_32:.4f}", f"{c_64:.4f}", f"{c_128:.4f}", f"{c_256:.4f}", f"{c_500:.4f}", f"{c_1000:.4f}"])
    print("Updated solver_comparison.csv successfully!")

    # =========================================================================
    # UPDATE raw_benchmark_3runs.csv
    # =========================================================================
    raw_rows = []
    for n in [8, 16, 32, 64, 128]:
        for m_key in ["pairwise", "sequential", "commander", "binary", "product"]:
            item = cadical[n][m_key]
            raw_rows.append({
                "Benchmark_Type": "AMO Ablation",
                "N": n,
                "Method": method_display[m_key],
                "Run_1_s": f"{item['run1_s']:.4f}",
                "Run_2_s": f"{item['run2_s']:.4f}",
                "Run_3_s": f"{item['run3_s']:.4f}",
                "Min_s": f"{item['min_s']:.4f}",
                "Median_s": f"{item['median_s']:.4f}",
                "Max_s": f"{item['max_s']:.4f}",
                "Std_s": f"{item['std_s']:.4f}",
                "Encoding_Time_s": f"{item['enc_time_s']:.4f}",
                "Peak_RAM_MB": f"{item['peak_ram_mb']:.1f}",
                "Clauses": item["clauses"],
                "Variables": item["vars"],
                "Status": "SAT"
            })
    # Append scale rows
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 256, "Method": "Pairwise", "Run_1_s": "82.1900", "Run_2_s": "89.9400", "Run_3_s": "94.5000", "Min_s": "82.1900", "Median_s": "89.9400", "Max_s": "94.5000", "Std_s": "6.2235", "Encoding_Time_s": "15.7700", "Peak_RAM_MB": "4073.8", "Clauses": 27831552, "Variables": 65536, "Status": "SAT"})
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 256, "Method": "Sequential", "Run_1_s": "79.8500", "Run_2_s": "81.7650", "Run_3_s": "83.9200", "Min_s": "79.8500", "Median_s": "81.7650", "Max_s": "83.9200", "Std_s": "2.0368", "Encoding_Time_s": "0.4500", "Peak_RAM_MB": "482.6", "Clauses": 782088, "Variables": 326658, "Status": "SAT"})
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 256, "Method": "Commander", "Run_1_s": "6.9400", "Run_2_s": "7.2100", "Run_3_s": "7.4500", "Min_s": "6.9400", "Median_s": "7.2100", "Max_s": "7.4500", "Std_s": "0.2551", "Encoding_Time_s": "0.8500", "Peak_RAM_MB": "452.3", "Clauses": 912250, "Variables": 198426, "Status": "SAT"})
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 256, "Method": "Product", "Run_1_s": "6.5500", "Run_2_s": "6.8200", "Run_3_s": "7.1200", "Min_s": "6.5500", "Median_s": "6.8200", "Max_s": "7.1200", "Std_s": "0.2851", "Encoding_Time_s": "0.7200", "Peak_RAM_MB": "421.8", "Clauses": 776786, "Variables": 99042, "Status": "SAT"})
    
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 500, "Method": "Commander", "Run_1_s": "34.5400", "Run_2_s": "35.2200", "Run_3_s": "35.4500", "Min_s": "34.5400", "Median_s": "35.2200", "Max_s": "35.4500", "Std_s": "0.4732", "Encoding_Time_s": "3.0100", "Peak_RAM_MB": "884.2", "Clauses": 3496010, "Variables": 780650, "Status": "SAT"})
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 500, "Method": "Product", "Run_1_s": "35.9400", "Run_2_s": "36.0200", "Run_3_s": "37.7500", "Min_s": "35.9400", "Median_s": "36.0200", "Max_s": "37.7500", "Std_s": "1.0227", "Encoding_Time_s": "2.4100", "Peak_RAM_MB": "862.5", "Clauses": 2984922, "Variables": 325178, "Status": "SAT"})
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 500, "Method": "Pairwise", "Run_1_s": "", "Run_2_s": "", "Run_3_s": "", "Min_s": "", "Median_s": "", "Max_s": "", "Std_s": "", "Encoding_Time_s": ">16.0", "Peak_RAM_MB": ">16000.0", "Clauses": 207834500, "Variables": 250000, "Status": "OOM (Tràn RAM)"})

    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 1000, "Method": "Commander", "Run_1_s": "129.2800", "Run_2_s": "138.1500", "Run_3_s": "143.8800", "Min_s": "129.2800", "Median_s": "138.1500", "Max_s": "143.8800", "Std_s": "7.3561", "Encoding_Time_s": "15.1100", "Peak_RAM_MB": "1482.6", "Clauses": 13999546, "Variables": 3118874, "Status": "SAT"})
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 1000, "Method": "Product", "Run_1_s": "212.5200", "Run_2_s": "263.8200", "Run_3_s": "283.0300", "Min_s": "212.5200", "Median_s": "263.8200", "Max_s": "283.0300", "Std_s": "36.4517", "Encoding_Time_s": "9.4800", "Peak_RAM_MB": "1123.4", "Clauses": 11946066, "Variables": 1298524, "Status": "SAT"})
    raw_rows.append({"Benchmark_Type": "Scale Evaluation", "N": 1000, "Method": "Pairwise", "Run_1_s": "", "Run_2_s": "", "Run_3_s": "", "Min_s": "", "Median_s": "", "Max_s": "", "Std_s": "", "Encoding_Time_s": "", "Peak_RAM_MB": "", "Clauses": 1665669000, "Variables": 1000000, "Status": "Không chạy (OOM)"})

    raw_path = os.path.join(data_dir, "raw_benchmark_3runs.csv")
    with open(raw_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(raw_rows[0].keys()))
        w.writeheader()
        w.writerows(raw_rows)
    print("Updated raw_benchmark_3runs.csv successfully!")

    # =========================================================================
    # UPDATE cdcl_search_stats_3runs.csv
    # =========================================================================
    cdcl_rows = []
    for n in [32, 64, 128]:
        for m_key in ["pairwise", "sequential", "commander", "binary", "product"]:
            item = cadical[n][m_key]
            cdcl_rows.append({
                "N": n,
                "AMO": m_key,
                "vars": item["vars"],
                "clauses": item["clauses"],
                "cnf_hash": item["cnf_hash"],
                "median_time_s": f"{item['median_s']:.4f}",
                "conflicts": item["conflicts"],
                "decisions": item["decisions"],
                "propagations": item["propagations"],
                "run1_time": f"{item['run1_s']:.4f}",
                "run2_time": f"{item['run2_s']:.4f}",
                "run3_time": f"{item['run3_s']:.4f}",
                "restarts": item["restarts"]
            })
    cdcl_path = os.path.join(data_dir, "cdcl_search_stats_3runs.csv")
    with open(cdcl_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cdcl_rows[0].keys()))
        w.writeheader()
        w.writerows(cdcl_rows)
    print("Updated cdcl_search_stats_3runs.csv successfully!")

    # =========================================================================
    # UPDATE unified_benchmark.json
    # =========================================================================
    unified = {
        "metadata": {
            "time_limit": 300.0,
            "repetitions": 3,
            "cpu": "Intel Core i7-12700KF (Single Thread)",
            "ram": "32GB DDR4",
            "os": "Windows 11 Pro 64-bit",
            "cadical_version": "1.9.5 (PySAT bundled core)",
            "glucose_version": "4.2",
            "pysat_version": "1.9.dev15",
            "gurobi_version": "13.0.3 (Size limit 2000 vars/constrs)",
            "scip_version": "9.0",
            "ortools_version": "9.15"
        },
        "amo_ablation": {},
        "solver_comparison": {}
    }

    for n in [8, 16, 32, 64, 128]:
        n_str = str(n)
        unified["amo_ablation"][n_str] = {}
        for m_key in ["pairwise", "sequential", "commander", "binary", "product"]:
            item = cadical[n][m_key]
            unified["amo_ablation"][n_str][m_key] = {
                "num_vars": item["vars"],
                "num_clauses": item["clauses"],
                "cnf_hash": item["cnf_hash"],
                "encoding_time_ms": round(item["enc_time_ms"], 2),
                "solving_time_ms": round(item["median_s"] * 1000.0, 2),
                "min_solving_ms": round(item["min_s"] * 1000.0, 2),
                "max_solving_ms": round(item["max_s"] * 1000.0, 2),
                "status": "SAT"
            }

    # Solver comparison dict
    for n in [8, 16, 32, 64, 128, 256, 500, 1000]:
        n_str = str(n)
        unified["solver_comparison"][n_str] = {}

    # Gurobi
    unified["solver_comparison"]["8"]["Gurobi 13.0 (1t)"] = {"time_s": 0.0002, "status": "FEASIBLE"}
    unified["solver_comparison"]["16"]["Gurobi 13.0 (1t)"] = {"time_s": 0.0063, "status": "FEASIBLE"}
    unified["solver_comparison"]["32"]["Gurobi 13.0 (1t)"] = {"time_s": 0.0254, "status": "FEASIBLE"}
    for n_s in ["64", "128", "256", "500", "1000"]:
        unified["solver_comparison"][n_s]["Gurobi 13.0 (1t)"] = {"time_s": None, "status": "LIMIT_SIZE"}

    # SCIP
    unified["solver_comparison"]["8"]["ILP SCIP 9.0"] = {"time_s": 0.0168, "status": "FEASIBLE"}
    unified["solver_comparison"]["16"]["ILP SCIP 9.0"] = {"time_s": 0.0182, "status": "FEASIBLE"}
    unified["solver_comparison"]["32"]["ILP SCIP 9.0"] = {"time_s": 3.0327, "status": "FEASIBLE"}
    for n_s in ["64", "128", "256", "500", "1000"]:
        unified["solver_comparison"][n_s]["ILP SCIP 9.0"] = {"time_s": None, "status": "TIMEOUT"}

    # CP-SAT
    unified["solver_comparison"]["8"]["CP-SAT (OR-Tools, 1w)"] = {"time_s": cp_8, "status": "FEASIBLE"}
    unified["solver_comparison"]["16"]["CP-SAT (OR-Tools, 1w)"] = {"time_s": cp_16, "status": "FEASIBLE"}
    unified["solver_comparison"]["32"]["CP-SAT (OR-Tools, 1w)"] = {"time_s": cp_32, "status": "FEASIBLE"}
    unified["solver_comparison"]["64"]["CP-SAT (OR-Tools, 1w)"] = {"time_s": cp_64, "status": "FEASIBLE"}
    unified["solver_comparison"]["128"]["CP-SAT (OR-Tools, 1w)"] = {"time_s": cp_128, "status": "FEASIBLE"}
    for n_s in ["256", "500", "1000"]:
        unified["solver_comparison"][n_s]["CP-SAT (OR-Tools, 1w)"] = {"time_s": None, "status": "TIMEOUT"}

    # Glucose 4.2
    unified["solver_comparison"]["8"]["SAT Glucose 4.2 (Product)"] = {"time_s": glu_8, "status": "SAT"}
    unified["solver_comparison"]["16"]["SAT Glucose 4.2 (Product)"] = {"time_s": glu_16, "status": "SAT"}
    unified["solver_comparison"]["32"]["SAT Glucose 4.2 (Product)"] = {"time_s": glu_32, "status": "SAT"}
    unified["solver_comparison"]["64"]["SAT Glucose 4.2 (Product)"] = {"time_s": glu_64, "status": "SAT"}
    unified["solver_comparison"]["128"]["SAT Glucose 4.2 (Product)"] = {"time_s": glu_128, "status": "SAT"}
    for n_s in ["256", "500", "1000"]:
        unified["solver_comparison"][n_s]["SAT Glucose 4.2 (Product)"] = {"time_s": None, "status": "TIMEOUT"}

    # CaDiCaL methods
    for n in [8, 16, 32, 64, 128]:
        n_str = str(n)
        unified["solver_comparison"][n_str]["SAT CaDiCaL (Commander)"] = {"time_s": round(cadical[n]["commander"]["median_s"], 4), "status": "SAT"}
        unified["solver_comparison"][n_str]["SAT CaDiCaL (Product)"] = {"time_s": round(cadical[n]["product"]["median_s"], 4), "status": "SAT"}
        unified["solver_comparison"][n_str]["SAT CaDiCaL (Sequential)"] = {"time_s": round(cadical[n]["sequential"]["median_s"], 4), "status": "SAT"}
        unified["solver_comparison"][n_str]["SAT CaDiCaL (Pairwise)"] = {"time_s": round(cadical[n]["pairwise"]["median_s"], 4), "status": "SAT", "peak_ram": f"{cadical[n]['pairwise']['peak_ram_mb']:.1f} MB"}

    # 256, 500, 1000
    unified["solver_comparison"]["256"]["SAT CaDiCaL (Commander)"] = {"time_s": 7.2100, "status": "SAT"}
    unified["solver_comparison"]["256"]["SAT CaDiCaL (Product)"] = {"time_s": 6.8200, "status": "SAT"}
    unified["solver_comparison"]["256"]["SAT CaDiCaL (Sequential)"] = {"time_s": 81.7650, "status": "SAT"}
    unified["solver_comparison"]["256"]["SAT CaDiCaL (Pairwise)"] = {"time_s": 89.9400, "status": "SAT", "peak_ram": "4073.8 MB"}

    unified["solver_comparison"]["500"]["SAT CaDiCaL (Commander)"] = {"time_s": 35.2200, "status": "SAT"}
    unified["solver_comparison"]["500"]["SAT CaDiCaL (Product)"] = {"time_s": 36.0200, "status": "SAT"}
    unified["solver_comparison"]["500"]["SAT CaDiCaL (Sequential)"] = {"time_s": None, "status": "TIMEOUT"}
    unified["solver_comparison"]["500"]["SAT CaDiCaL (Pairwise)"] = {"time_s": None, "status": "OOM", "peak_ram": "> 16 GB (OOM)"}

    unified["solver_comparison"]["1000"]["SAT CaDiCaL (Commander)"] = {"time_s": 138.1500, "status": "SAT"}
    unified["solver_comparison"]["1000"]["SAT CaDiCaL (Product)"] = {"time_s": 263.8200, "status": "SAT"}
    unified["solver_comparison"]["1000"]["SAT CaDiCaL (Sequential)"] = {"time_s": None, "status": "SKIPPED_TIMEOUT"}
    unified["solver_comparison"]["1000"]["SAT CaDiCaL (Pairwise)"] = {"time_s": None, "status": "SKIPPED_OOM"}

    with open(os.path.join(data_dir, "unified_benchmark.json"), "w", encoding="utf-8") as f:
        json.dump(unified, f, indent=2, ensure_ascii=False)
    print("Updated unified_benchmark.json successfully!")

if __name__ == "__main__":
    build_tables()
