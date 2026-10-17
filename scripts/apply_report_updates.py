import os
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
report_dir = os.path.join(base_dir, "report")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    tex_path = os.path.join(report_dir, "nqueens_report_elsevier.tex")
    content = read_file(tex_path)

    # 1. Preamble hypersetup
    old_hyp = r"\hypersetup{pdfauthor={Phạm Khánh Duy}, pdftitle={Nghiên cứu các Kỹ thuật Mã hóa SAT cho Bài toán N-Queens}}}"
    new_hyp = r"\hypersetup{pdfauthor={Pham Khanh Duy, To Van Khanh}, pdftitle={Nghien cuu cac Ky thuat Ma hoa SAT cho Bai toan N-Queens}, colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}"
    if old_hyp in content:
        content = content.replace(old_hyp, new_hyp)
    else:
        print("Warning: old_hyp not matched exactly, checking regex...")
        content = re.sub(r'\\hypersetup\{pdfauthor=\{[^}]+\},\s*pdftitle=\{[^}]+\}\}+', new_hyp, content)

    # 2. Section 1 RAM text: 4 GB -> 7.7 GB
    old_ram_text = r"tiêu tốn đỉnh điểm khoảng 4 GB RAM ($4{,}073.8$ MB, $\approx 3.98$ GiB)"
    new_ram_text = r"tiêu tốn đỉnh điểm khoảng 7.7 GB RAM ($7{,}679.4$ MB, $\approx 7.50$ GiB)"
    if old_ram_text in content:
        content = content.replace(old_ram_text, new_ram_text)
    else:
        print("Warning: old_ram_text not found")

    # 3. Duplicate paragraph in Section 4.2
    dup_pattern = r"(Bảng~\\ref\{tab:ablation_results\} và Hình~\\ref\{fig:clauses_scaling\} thống kê số biến logic.*?\(thời gian mã hóa trung vị \$14\.74\$s, thời gian giải trung vị \$83\.46\$s, dải \[\$81\.03, 88\.80\]\$s, tiêu tốn \$7\{,\}679\.4\$ MB RAM đỉnh\)\.\s*\n\s*\n)(Bảng~\\ref\{tab:ablation_results\} và Hình~\\ref\{fig:clauses_scaling\} thống kê số biến logic.*?\(thời gian mã hóa \$15\.77\$s, thời gian giải trung vị \$89\.94\$s, dải \[\$82\.19, 94\.50\]\$s\)\.)"
    if re.search(dup_pattern, content):
        content = re.sub(dup_pattern, r"\1", content)
        print("Removed duplicate paragraph in Section 4.2 successfully!")
    else:
        print("Warning: duplicate pattern not matched by regex, checking plain substring...")
        old_dup = r"Bảng~\ref{tab:ablation_results} và Hình~\ref{fig:clauses_scaling} thống kê số biến logic, số mệnh đề CNF, thời gian tạo mô hình (Encoding Time) và thời gian giải (Solving Time) bằng CaDiCaL 1.9.5 trên dải kích thước $N \in [8, 128]$. Ngoài ra, tại $N = 256$, phương pháp Pairwise vẫn sinh thành công mô hình với 65,536 biến và 27,831,552 mệnh đề (thời gian mã hóa $15.77$s, thời gian giải trung vị $89.94$s, dải $[82.19, 94.50]$s)."
        if old_dup in content:
            content = content.replace(old_dup + "\n\n", "")
            print("Removed duplicate paragraph via plain string!")

    # 4. Replace Table 2
    t2_gen = read_file(os.path.join(report_dir, "table2_generated.tex"))
    t2_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{So sánh thực nghiệm toàn diện giữa 5 kỹ thuật mã hóa AMO.*?\\label\{tab:ablation_results\}.*?\\end\{table\*\}"
    content = re.sub(t2_regex, lambda m: t2_gen, content, flags=re.DOTALL)

    # 5. Replace Table 3
    t3_gen = read_file(os.path.join(report_dir, "table3_generated.tex"))
    t3_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{Thống kê định lượng động cơ tìm kiếm CDCL của CaDiCaL 1.9.5.*?\\label\{tab:cdcl_search_stats\}.*?\\end\{table\*\}"
    content = re.sub(t3_regex, lambda m: t3_gen, content, flags=re.DOTALL)

    # 6. Replace Table 4
    t4_gen = read_file(os.path.join(report_dir, "table4_generated.tex"))
    t4_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{So sánh thời gian giải trung vị \(giây\) giữa các bộ giải SAT.*?\\label\{tab:solver_comparison\}.*?\\end\{table\*\}"
    content = re.sub(t4_regex, lambda m: t4_gen, content, flags=re.DOTALL)

    # 7. Update Section 4.3 discussion numbers to match Table 4 / Table 5b
    content = content.replace(r"($0.0002$s ở $N=8$ và $0.0254$s ở $N=32$)", r"($0.0002$s ở $N=8$ và $0.0272$s ở $N=32$)")
    content = content.replace(r"tăng vọt từ $0.0182$s ($N=16$) lên $3.0327$s ($N=32$)", r"tăng vọt từ $0.0190$s ($N=16$) lên $3.1150$s ($N=32$)")
    content = content.replace(r"($N=128$ giải trong $2.80$s)", r"($N=128$ giải trong $3.46$s)")
    content = content.replace(r"nhanh gấp khoảng $3.0$ lần CP-SAT với $0.5643$s", r"nhanh gấp khoảng $3.2$ lần CP-SAT với $0.5912$s")
    content = content.replace(r"tuy nhiên ở $N=32$, Glucose mất tới $19.45$s", r"tuy nhiên ở $N=32$, Glucose mất tới $20.71$s")
    content = content.replace(r"chậm hơn khoảng $227$ lần: $19.4494 / 0.0857 \approx 227$", r"chậm hơn khoảng $242$ lần: $20.7088 / 0.0857 \approx 242$")
    content = content.replace(r"Ở $N=64$, Glucose cũng mất tới $22.93$s", r"Ở $N=64$, Glucose cũng mất tới $36.56$s")
    content = content.replace(r"chậm hơn khoảng 54 lần", r"chậm hơn khoảng 87 lần: $36.5604 / 0.4211 \approx 87$")

    # 8. Data availability script path line-breaking
    content = content.replace(r"\texttt{scripts/run_isolated_master_benchmark.py}", r"\texttt{scripts/\allowbreak run\_isolated\_\allowbreak master\_benchmark.py}")

    # 9. Replace Table 5a
    t5a_gen = read_file(os.path.join(report_dir, "table5a_generated.tex"))
    t5a_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{Dữ liệu thực nghiệm chi tiết 3 lần chạy độc lập.*?\\label\{tab:appendix_raw_runs\}.*?\\end\{table\*\}"
    content = re.sub(t5a_regex, lambda m: t5a_gen, content, flags=re.DOTALL)

    # 10. Replace Table 5b
    t5b_gen = read_file(os.path.join(report_dir, "table5b_generated.tex"))
    t5b_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{Dữ liệu thực nghiệm chi tiết 3 lần chạy lặp độc lập so sánh đa bộ giải.*?\\label\{tab:appendix_multisolver\}.*?\\end\{table\*\}"
    content = re.sub(t5b_regex, lambda m: t5b_gen, content, flags=re.DOTALL)

    # Write out nqueens_report_elsevier.tex
    write_file(tex_path, content)
    print("Updated report/nqueens_report_elsevier.tex successfully!")

    # Write out main.tex (identical copy for Overleaf root compilation)
    main_path = os.path.join(report_dir, "main.tex")
    write_file(main_path, content)
    print("Updated report/main.tex successfully!")

    # For standard article, update tables and metadata
    std_path = os.path.join(report_dir, "nqueens_report_standard.tex")
    if os.path.exists(std_path):
        std_content = read_file(std_path)
        std_content = re.sub(t2_regex, lambda m: t2_gen, std_content, flags=re.DOTALL)
        std_content = re.sub(t3_regex, lambda m: t3_gen, std_content, flags=re.DOTALL)
        std_content = re.sub(t4_regex, lambda m: t4_gen, std_content, flags=re.DOTALL)
        std_content = re.sub(t5a_regex, lambda m: t5a_gen, std_content, flags=re.DOTALL)
        std_content = re.sub(t5b_regex, lambda m: t5b_gen, std_content, flags=re.DOTALL)
        if old_ram_text in std_content:
            std_content = std_content.replace(old_ram_text, new_ram_text)
        if old_dup in std_content:
            std_content = std_content.replace(old_dup + "\n\n", "")
        std_content = std_content.replace(r"($0.0002$s ở $N=8$ và $0.0254$s ở $N=32$)", r"($0.0002$s ở $N=8$ và $0.0272$s ở $N=32$)")
        std_content = std_content.replace(r"tăng vọt từ $0.0182$s ($N=16$) lên $3.0327$s ($N=32$)", r"tăng vọt từ $0.0190$s ($N=16$) lên $3.1150$s ($N=32$)")
        std_content = std_content.replace(r"($N=128$ giải trong $2.80$s)", r"($N=128$ giải trong $3.46$s)")
        std_content = std_content.replace(r"nhanh gấp khoảng $3.0$ lần CP-SAT với $0.5643$s", r"nhanh gấp khoảng $3.2$ lần CP-SAT với $0.5912$s")
        std_content = std_content.replace(r"tuy nhiên ở $N=32$, Glucose mất tới $19.45$s", r"tuy nhiên ở $N=32$, Glucose mất tới $20.71$s")
        std_content = std_content.replace(r"chậm hơn khoảng $227$ lần: $19.4494 / 0.0857 \approx 227$", r"chậm hơn khoảng $242$ lần: $20.7088 / 0.0857 \approx 242$")
        std_content = std_content.replace(r"Ở $N=64$, Glucose cũng mất tới $22.93$s", r"Ở $N=64$, Glucose cũng mất tới $36.56$s")
        std_content = std_content.replace(r"chậm hơn khoảng 54 lần", r"chậm hơn khoảng 87 lần: $36.5604 / 0.4211 \approx 87$")
        std_content = std_content.replace(r"\texttt{scripts/run_isolated_master_benchmark.py}", r"\texttt{scripts/\allowbreak run\_isolated\_\allowbreak master\_benchmark.py}")
        write_file(std_path, std_content)
        print("Updated report/nqueens_report_standard.tex successfully!")

if __name__ == "__main__":
    main()
