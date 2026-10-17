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

def update_content(content):
    # 1. Preamble: hypersetup and printorcid suppression
    old_hyp = r"\hypersetup{pdfauthor={Pham Khanh Duy, To Van Khanh}, pdftitle={Nghien cuu cac Ky thuat Ma hoa SAT cho Bai toan N-Queens}, colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}"
    new_hyp = (
        r"\hypersetup{pdfauthor={Pham Khanh Duy, To Van Khanh}, pdftitle={Nghien cuu cac Ky thuat Ma hoa SAT cho Bai toan N-Queens}, colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}" "\n"
        r"\let\printorcid\relax"
    )
    if r"\let\printorcid\relax" not in content:
        if old_hyp in content:
            content = content.replace(old_hyp, new_hyp)
        else:
            content = content.replace(r"\begin{document}", r"\let\printorcid\relax" "\n" r"\begin{document}")

    # 2. Author: remove \corref{cor1} from inside \author[1]{...}
    content = content.replace(
        r"\author[1]{Phạm Khánh Duy\corref{cor1}}[role=Học viên thực hiện]",
        r"\author[1]{Phạm Khánh Duy}[role=Học viên thực hiện]"
    )

    # 3. Section 1 RAM text: 7.7 GB
    content = content.replace(
        r"tiêu tốn đỉnh điểm khoảng 4 GB RAM ($4{,}073.8$ MB, $\approx 3.98$ GiB)",
        r"tiêu tốn đỉnh điểm khoảng 7.7 GB RAM ($7{,}679.4$ MB, $\approx 7.50$ GiB)"
    )

    # 4. Section 1: "lặp đúng 3 lần cho mọi N in [8, 1000]" -> nói chính xác
    content = content.replace(
        r"lặp lại đúng 3 lần cho mọi kích thước $N \in [8, 1000]$ trong từng tiến trình con độc lập",
        r"lặp lại đúng 3 lần cho mọi kích thước $N$ được khảo sát của từng kỹ thuật (lên tới $N=1000$ đối với Commander và Product) trong từng tiến trình con độc lập"
    )

    # 5. Section 4.1: Gurobi license wording
    content = content.replace(
        r"phiên bản học thuật dùng thử đi kèm thư viện Python có giới hạn 2,000 biến",
        r"license đi kèm gói pip có giới hạn 2,000 biến"
    )

    # 6. Section 4.3 discussion numbers & Gurobi N=16
    content = content.replace(r"($0.0002$s ở $N=8$ và $0.0254$s ở $N=32$)", r"($0.0002$s ở $N=8$ và $0.0272$s ở $N=32$)")
    content = content.replace(r"tăng vọt từ $0.0182$s ($N=16$) lên $3.0327$s ($N=32$)", r"tăng vọt từ $0.0190$s ($N=16$) lên $3.1150$s ($N=32$)")
    content = content.replace(r"($N=128$ giải trong $2.80$s)", r"($N=128$ giải trong $3.46$s)")
    content = content.replace(r"nhanh gấp khoảng $3.0$ lần CP-SAT với $0.5643$s", r"nhanh gấp khoảng $3.2$ lần CP-SAT với $0.5912$s")
    content = content.replace(r"tuy nhiên ở $N=32$, Glucose mất tới $19.45$s", r"tuy nhiên ở $N=32$, Glucose mất tới $20.71$s")
    content = content.replace(r"chậm hơn khoảng $227$ lần: $19.4494 / 0.0857 \approx 227$", r"chậm hơn khoảng $242$ lần: $20.7088 / 0.0857 \approx 242$")
    content = content.replace(r"Ở $N=64$, Glucose cũng mất tới $22.93$s", r"Ở $N=64$, Glucose cũng mất tới $36.56$s")
    content = content.replace(r"chậm hơn khoảng 54 lần", r"chậm hơn khoảng 87 lần: $36.5604 / 0.4211 \approx 87$")

    # 7. Section 4.3 text: "thực nghiệm khẳng định... tất định" -> "quan sát thấy"
    content = content.replace(
        r"Về bản chất tìm kiếm, thực nghiệm khẳng định solver CaDiCaL vận hành mang tính tất định:",
        r"Về bản chất tìm kiếm, thực nghiệm quan sát thấy solver CaDiCaL vận hành mang tính tất định:"
    )

    # 8. Conclusion: Gurobi N=16 correction
    content = content.replace(
        r"Gurobi thể hiện tốc độ nhanh nhất ở quy mô nhỏ $N \le 32$ nhưng dừng ở $N \ge 64$ do giới hạn kích thước license đi kèm gói pip (2.000 biến).",
        r"Gurobi thể hiện tốc độ nhanh nhất ở $N = 8$ và $N = 32$ (trong khi CaDiCaL Commander nhanh nhất ở $N = 16$), nhưng dừng ở $N \ge 64$ do giới hạn kích thước license đi kèm gói pip (2.000 biến)."
    )

    # 9. Data Availability: Clean itemize formatting to eliminate margin overflow completely
    old_data_avail_pattern = r"\\section\*\{Tính khả dụng của dữ liệu và mã nguồn \(Data Availability\)\}.*?\\url\{https://github\.com/vnu-uet-khmt/nqueens-sat-solver\}\s*\\end\{center\}"
    new_data_avail = (
        r"\section*{Tính khả dụng của dữ liệu và mã nguồn (Data Availability)}" "\n"
        r"Toàn bộ mã nguồn cài đặt 5 kỹ thuật mã hóa AMO, các bộ giải SAT (PySAT), CP-SAT, Gurobi, SCIP và dữ liệu thực nghiệm được cung cấp đầy đủ trong gói dự án đính kèm và lưu trữ công khai trên GitHub repository:" "\n"
        r"\begin{itemize}" "\n"
        r"    \item \textbf{Mã nguồn thực nghiệm:} \path{scripts/isolated_run_worker.py}, \path{scripts/run_isolated_master_benchmark.py}, \path{scripts/run_multisolver_benchmark.py}." "\n"
        r"    \item \textbf{Tự động sinh bảng biểu:} \path{scripts/generate_all_tables_from_master.py}, \path{scripts/sync_data_files.py}." "\n"
        r"    \item \textbf{Dữ liệu thực nghiệm gốc:} \path{data/master_cadical_runs.csv}, \path{data/master_multisolver_runs.csv}, \path{data/benchmark_execution.log}." "\n"
        r"    \item \textbf{Kho lưu trữ GitHub:} \url{https://github.com/vnu-uet-khmt/nqueens-sat-solver}" "\n"
        r"\end{itemize}"
    )
    content = re.sub(old_data_avail_pattern, lambda m: new_data_avail, content, flags=re.DOTALL)

    # 10. Replace Tables
    t2_gen = read_file(os.path.join(report_dir, "table2_generated.tex"))
    t2_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{So sánh thực nghiệm toàn diện giữa 5 kỹ thuật mã hóa AMO.*?\\label\{tab:ablation_results\}.*?\\end\{table\*\}"
    content = re.sub(t2_regex, lambda m: t2_gen, content, flags=re.DOTALL)

    t3_gen = read_file(os.path.join(report_dir, "table3_generated.tex"))
    t3_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{Thống kê định lượng động cơ tìm kiếm CDCL của CaDiCaL 1.9.5.*?\\label\{tab:cdcl_search_stats\}.*?\\end\{table\*\}"
    content = re.sub(t3_regex, lambda m: t3_gen, content, flags=re.DOTALL)

    t4_gen = read_file(os.path.join(report_dir, "table4_generated.tex"))
    t4_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{So sánh thời gian giải trung vị \(giây\) giữa các bộ giải SAT.*?\\label\{tab:solver_comparison\}.*?\\end\{table\*\}"
    content = re.sub(t4_regex, lambda m: t4_gen, content, flags=re.DOTALL)

    t5a_gen = read_file(os.path.join(report_dir, "table5a_generated.tex"))
    t5a_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{Dữ liệu thực nghiệm chi tiết 3 lần chạy độc lập.*?\\label\{tab:appendix_raw_runs\}.*?\\end\{table\*\}"
    content = re.sub(t5a_regex, lambda m: t5a_gen, content, flags=re.DOTALL)

    t5b_gen = read_file(os.path.join(report_dir, "table5b_generated.tex"))
    t5b_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{Dữ liệu thực nghiệm chi tiết 3 lần chạy lặp độc lập so sánh đa bộ giải.*?\\label\{tab:appendix_multisolver\}.*?\\end\{table\*\}"
    content = re.sub(t5b_regex, lambda m: t5b_gen, content, flags=re.DOTALL)

    return content

def main():
    tex_path = os.path.join(report_dir, "nqueens_report_elsevier.tex")
    content = read_file(tex_path)
    updated = update_content(content)
    write_file(tex_path, updated)
    print("Updated report/nqueens_report_elsevier.tex successfully!")

    main_path = os.path.join(report_dir, "main.tex")
    write_file(main_path, updated)
    print("Updated report/main.tex successfully!")

    std_path = os.path.join(report_dir, "nqueens_report_standard.tex")
    if os.path.exists(std_path):
        std_content = read_file(std_path)
        std_updated = update_content(std_content)
        write_file(std_path, std_updated)
        print("Updated report/nqueens_report_standard.tex successfully!")

if __name__ == "__main__":
    main()
