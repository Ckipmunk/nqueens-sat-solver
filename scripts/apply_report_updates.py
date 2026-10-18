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
    # 1. Preamble visual improvements
    preamble_target = r"\usepackage{listings}"
    preamble_repl = (
        r"\usepackage{listings}" "\n"
        r"\usepackage{enumitem}" "\n"
        r"\usepackage[most]{tcolorbox}" "\n\n"
        r"% ==========================================================================" "\n"
        r"% BẢNG MÀU VÀ ĐỊNH DẠNG HỌC THUẬT NÂNG CAO (ACADEMIC STYLING)" "\n"
        r"% ==========================================================================" "\n"
        r"\definecolor{primaryblue}{RGB}{16, 78, 139}       % Xanh navy chuẩn học thuật" "\n"
        r"\definecolor{accentteal}{RGB}{0, 115, 115}         % Xanh ngọc điểm nhấn" "\n"
        r"\definecolor{tableheader}{RGB}{232, 238, 246}      % Nền tiêu đề bảng" "\n"
        r"\definecolor{subheadbg}{RGB}{238, 242, 248}        % Nền phân nhóm trong bảng" "\n"
        r"\definecolor{tablerowalt}{RGB}{249, 250, 253}      % Nền dòng so le nhẹ nhàng" "\n"
        r"\definecolor{boxbg}{RGB}{247, 249, 253}            % Nền hộp ghi chú" "\n"
        r"\definecolor{boxborder}{RGB}{185, 205, 230}        % Viền hộp ghi chú" "\n\n"
        r"% Cải thiện độ thoáng và độ dễ đọc cho văn bản tiếng Việt" "\n"
        r"\linespread{1.07}" "\n"
        r"\setlength{\parskip}{0.35em plus 0.1em minus 0.1em}" "\n"
        r"\setlength{\parindent}{1.2em}" "\n"
        r"\setlist[itemize]{leftmargin=1.8em, itemsep=0.25em, topsep=0.3em}" "\n"
        r"\setlist[enumerate]{leftmargin=1.8em, itemsep=0.25em, topsep=0.3em}"
    )
    if "primaryblue" not in content:
        content = content.replace(preamble_target, preamble_repl)

    # 2. Suppress empty orcid
    if r"\let\printorcid\relax" not in content:
        content = content.replace(r"\begin{document}", r"\let\printorcid\relax" "\n" r"\begin{document}")

    # 3. Clean Author metadata (no cor1 in name)
    content = content.replace(
        r"\author[1]{Phạm Khánh Duy\corref{cor1}}[role=Học viên thực hiện]",
        r"\author[1]{Phạm Khánh Duy}[role=Học viên thực hiện]"
    )

    # 4. Definition 1 inside styled tcolorbox
    def1_target = (
        r"\subsection{Phát biểu bài toán N-Queens}" "\n"
        r"Cho bàn cờ vuông kích thước $N \times N$, tập tọa độ các ô cờ là $\mathcal{H}_N = \{(r, c) \mid 0 \le r, c < N\}$, trong đó $r$ là chỉ số hàng và $c$ là chỉ số cột. Bài toán yêu cầu đặt $N$ quân hậu vào tập vị trí $\mathcal{Q} \subset \mathcal{H}_N$ thỏa mãn:" "\n"
        r"\begin{align}" "\n"
        r"    &|\mathcal{Q}| = N, \\" "\n"
        r"    &\forall (r_1, c_1), (r_2, c_2) \in \mathcal{Q}, \; (r_1, c_1) \neq (r_2, c_2) \implies \nonumber\\" "\n"
        r"    &\quad r_1 \neq r_2 \quad \land \quad c_1 \neq c_2 \quad \land \quad |r_1 - r_2| \neq |c_1 - c_2|." "\n"
        r"\end{align}"
    )
    def1_styled = (
        r"\subsection{Phát biểu bài toán N-Queens}" "\n"
        r"\begin{tcolorbox}[" "\n"
        r"    colback=boxbg, colframe=boxborder, arc=2mm, boxrule=0.75pt," "\n"
        r"    left=10pt, right=10pt, top=7pt, bottom=7pt," "\n"
        r"    title=\textbf{\color{primaryblue}Định nghĩa 1 (Bài toán $N$-Queens tiêu chuẩn)}," "\n"
        r"    coltitle=primaryblue" "\n"
        r"]" "\n"
        r"Cho bàn cờ vuông kích thước $N \times N$, tập tọa độ các ô cờ là $\mathcal{H}_N = \{(r, c) \mid 0 \le r, c < N\}$, trong đó $r$ là chỉ số hàng và $c$ là chỉ số cột. Bài toán yêu cầu đặt $N$ quân hậu vào tập vị trí $\mathcal{Q} \subset \mathcal{H}_N$ thỏa mãn:" "\n"
        r"\begin{align}" "\n"
        r"    &|\mathcal{Q}| = N, \\" "\n"
        r"    &\forall (r_1, c_1), (r_2, c_2) \in \mathcal{Q}, \; (r_1, c_1) \neq (r_2, c_2) \implies \nonumber\\" "\n"
        r"    &\quad r_1 \neq r_2 \quad \land \quad c_1 \neq c_2 \quad \land \quad |r_1 - r_2| \neq |c_1 - c_2|." "\n"
        r"\end{align}" "\n"
        r"\end{tcolorbox}"
    )
    if "Định nghĩa 1 (Bài toán $N$-Queens tiêu chuẩn)" not in content:
        content = content.replace(def1_target, def1_styled)

    # 5. Table 1 styling: arraystretch & colors
    t1_regex = r"\\begin\{table\*\}\[htbp\]\s*\\caption\{So sánh lý thuyết độ phức tạp của 5 kỹ thuật mã hóa AMO.*?\\label\{tab:amo_complexity\}.*?\\end\{table\*\}"
    t1_styled = (
        r"\begin{table*}[htbp]" "\n"
        r"\caption{So sánh lý thuyết độ phức tạp của 5 kỹ thuật mã hóa AMO cho một nhóm $k$ biến và toàn bàn cờ $N \times N$.}" "\n"
        r"\label{tab:amo_complexity}" "\n"
        r"\centering" "\n"
        r"\renewcommand{\arraystretch}{1.22}" "\n"
        r"\resizebox{\textwidth}{!}{%" "\n"
        r"\begin{tabular}{lllc p{6.5cm}}" "\n"
        r"\toprule" "\n"
        r"\rowcolor{tableheader}" "\n"
        r"\textbf{Kỹ thuật mã hóa} & \textbf{Biến phụ (nhóm $k$)} & \textbf{Mệnh đề (nhóm $k$)} & \textbf{Mệnh đề toàn bàn cờ} & \textbf{Đặc điểm triển khai} \\" "\n"
        r"\midrule" "\n"
        r"Pairwise (Direct) & $0$ & $\mathcal{O}(k^2)$ & $\mathcal{O}(N^3)$ (Bùng nổ) & Sẵn có trong PySAT CardEnc; tốn RAM lớn ở $N \ge 256$ \\" "\n"
        r"\rowcolor{tablerowalt} Sequential Counter & $\mathcal{O}(k)$ & $\mathcal{O}(k)$ & $\mathcal{O}(N^2)$ (Gọn) & Sẵn có trong PySAT CardEnc; chuỗi suy diễn dài \\" "\n"
        r"Commander Variable & $\mathcal{O}(k)$ & $\mathcal{O}(k)$ & $\mathcal{O}(N^2)$ (Gọn) & Tự cài đặt theo Klieber \& Kwon~\cite{klieber2007efficient}; cấu trúc cây $g=3$ \\" "\n"
        r"\rowcolor{tablerowalt} Binary (Bitwise) & $\mathcal{O}(\log k)$ & $\mathcal{O}(k \log k)$ & $\mathcal{O}(N^2 \log N)$ & Sẵn có trong PySAT CardEnc; ít biến phụ nhất \\" "\n"
        r"Product (2D Grid) & $\mathcal{O}(\sqrt{k})$ & $\mathcal{O}(k)$ & $\mathcal{O}(N^2)$ (Gọn) & Tự cài đặt theo Chen~\cite{chen2010product}; lưới $p \times q$ tối ưu \\" "\n"
        r"\bottomrule" "\n"
        r"\end{tabular}%" "\n"
        r"}" "\n"
        r"\end{table*}"
    )
    content = re.sub(t1_regex, lambda m: t1_styled, content, flags=re.DOTALL)

    # 6. Executive Key Takeaways Box at start of Section 4
    sec4_target = (
        r"\section{Kết quả Thực nghiệm và Thảo luận (Computational Experiments)}" "\n\n"
        r"\subsection{Thiết lập Môi trường Thực nghiệm}"
    )
    sec4_styled = (
        r"\section{Kết quả Thực nghiệm và Thảo luận (Computational Experiments)}" "\n\n"
        r"\begin{tcolorbox}[" "\n"
        r"    colback=boxbg, colframe=boxborder, arc=2mm, boxrule=0.85pt," "\n"
        r"    left=12pt, right=12pt, top=8pt, bottom=8pt," "\n"
        r"    title=\textbf{\color{primaryblue}Tóm tắt các Phát hiện Thực nghiệm Cốt lõi (Key Experimental Takeaways)}," "\n"
        r"    coltitle=primaryblue" "\n"
        r"]" "\n"
        r"\begin{itemize}[leftmargin=1.5em, itemsep=0.25em, topsep=0.2em]" "\n"
        r"    \item \textbf{Khả năng mở rộng quy mô cực đại ($N \ge 256$):} SAT Solving (CaDiCaL kết hợp Commander Variable và Product Encoding) là hướng tiếp cận duy nhất giải quyết thành công bàn cờ kích thước $N=500$ ($32.11$s) và $N=1000$ ($100.92$s với một triệu ô cờ). Trong khi đó, các bộ giải CP-SAT và ILP SCIP đều chạm ngưỡng giới hạn thời gian ($>300.0$s) từ $N=256$." "\n"
        r"    \item \textbf{Hiệu năng ở quy mô nhỏ ($N \le 32$):} Gurobi 13.0 dẫn đầu về tốc độ ở $N=8$ ($0.0002$s) và $N=32$ ($0.0272$s) nhờ các thuật toán cắt mặt phẳng tiên tiến; CaDiCaL Commander đạt thời gian giải tốt nhất ở $N=16$ ($0.0077$s). Từ $N \ge 64$, Gurobi dừng do hạn mức license gói pip (tối đa 2.000 biến)." "\n"
        r"    \item \textbf{Cơ chế suy thoái của Sequential Counter ở $N=128$:} Mặc dù số mệnh đề rất gọn ($\mathcal{O}(N^2)$), thời gian giải tăng vọt lên $24.85$s (chậm hơn Commander 33 lần) do bùng nổ $68\times$ số xung đột CDCL ($62{,}360$ so với $916$), kéo theo $42.89$ triệu lượt lan truyền đơn vị trên cây suy diễn." "\n"
        r"    \item \textbf{Hạn chế bộ nhớ của Pairwise Encoding:} Do số mệnh đề tăng theo bậc ba $\mathcal{O}(N^3)$, Pairwise tiêu tốn đỉnh điểm $7{,}679.4$ MB RAM ở $N=256$ ($27.8$ triệu mệnh đề) và cạn kiệt bộ nhớ (\texttt{MemoryError}) ở $N=500$ khi khởi tạo $207.8$ triệu đối tượng mệnh đề trong danh sách liên tục của Python." "\n"
        r"\end{itemize}" "\n"
        r"\end{tcolorbox}" "\n\n"
        r"\subsection{Thiết lập Môi trường Thực nghiệm}"
    )
    if "Tóm tắt các Phát hiện Thực nghiệm Cốt lõi" not in content:
        content = content.replace(sec4_target, sec4_styled)

    # 7. Replace Tables 2, 3, 4, 5a, 5b with newly generated visual versions
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

    try:
        from add_bold_headings import enhance_bold_headings
        content = enhance_bold_headings(content)
    except Exception as e:
        print(f"Warning: could not run enhance_bold_headings: {e}")

    try:
        from apply_critique_fixes import apply_fixes
        content = apply_fixes(content)
    except Exception as e:
        print(f"Warning: could not run apply_fixes: {e}")

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
