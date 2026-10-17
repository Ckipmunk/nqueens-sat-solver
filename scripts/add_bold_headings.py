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

def enhance_bold_headings(content):
    # 1. Preamble font formatting for section titles to be sharp bold
    font_styling = (
        "\n% Cấu hình các cấp đề mục tiêu đề in đậm rõ nét (Bold Heading Typography)\n"
        r"\makeatletter" "\n"
        r"\def\sectionfont{\rmfamily\fontsize{12pt}{14pt}\bfseries\boldmath}" "\n"
        r"\def\ssectionfont{\rmfamily\fontsize{11pt}{13pt}\bfseries\boldmath}" "\n"
        r"\def\sssectionfont{\rmfamily\fontsize{10.5pt}{12pt}\bfseries\boldmath\upshape}" "\n"
        r"\makeatother" "\n"
    )
    if r"\def\sssectionfont" not in content:
        if r"\setlist[enumerate]{leftmargin=1.8em, itemsep=0.25em, topsep=0.3em}" in content:
            content = content.replace(
                r"\setlist[enumerate]{leftmargin=1.8em, itemsep=0.25em, topsep=0.3em}",
                r"\setlist[enumerate]{leftmargin=1.8em, itemsep=0.25em, topsep=0.3em}" + font_styling
            )

    # 2. Section 1 bold paragraph headings
    s1_target = (
        r"\section{Giới thiệu (Introduction)}" "\n"
        r"Bài toán $N$-Queens (xếp $N$ quân hậu) được nhà nghiên cứu Max Bezzel"
    )
    s1_repl = (
        r"\section{Giới thiệu (Introduction)}" "\n\n"
        r"\noindent\textbf{1. Bối cảnh lịch sử và Định nghĩa bài toán:}\\" "\n"
        r"Bài toán $N$-Queens (xếp $N$ quân hậu) được nhà nghiên cứu Max Bezzel"
    )
    if r"\noindent\textbf{1. Bối cảnh lịch sử và Định nghĩa bài toán:}" not in content:
        content = content.replace(s1_target, s1_repl)

    s1_target2 = (
        "\n\n"
        r"Mặc dù có cấu trúc phát biểu trực quan và đơn giản, $N$-Queens là bài toán chuẩn mực"
    )
    s1_repl2 = (
        "\n\n"
        r"\noindent\textbf{2. Ý nghĩa lý thuyết và Ứng dụng thực tiễn:}\\" "\n"
        r"Mặc dù có cấu trúc phát biểu trực quan và đơn giản, $N$-Queens là bài toán chuẩn mực"
    )
    if r"\noindent\textbf{2. Ý nghĩa lý thuyết và Ứng dụng thực tiễn:}" not in content:
        content = content.replace(s1_target2, s1_repl2)

    s1_target3 = (
        "\n\n"
        r"Để giải quyết bài toán $N$-Queens, cộng đồng khoa học đã phát triển nhiều hướng tiếp cận khác nhau:"
    )
    s1_repl3 = (
        "\n\n"
        r"\noindent\textbf{3. Các hướng tiếp cận giải quyết bài toán:}\\" "\n"
        r"Để giải quyết bài toán $N$-Queens, cộng đồng khoa học đã phát triển nhiều hướng tiếp cận khác nhau:"
    )
    if r"\noindent\textbf{3. Các hướng tiếp cận giải quyết bài toán:}" not in content:
        content = content.replace(s1_target3, s1_repl3)

    s1_target4 = (
        r"\end{enumerate}" "\n\n"
        r"Trọng tâm của tiếp cận SAT nằm ở việc chuyển đổi các ràng buộc số lượng"
    )
    s1_repl4 = (
        r"\end{enumerate}" "\n\n"
        r"\noindent\textbf{4. Thách thức bùng nổ mệnh đề trong tiếp cận SAT:}\\" "\n"
        r"Trọng tâm của tiếp cận SAT nằm ở việc chuyển đổi các ràng buộc số lượng"
    )
    if r"\noindent\textbf{4. Thách thức bùng nổ mệnh đề trong tiếp cận SAT:}" not in content:
        content = content.replace(s1_target4, s1_repl4)

    s1_target5 = (
        r"\textbf{Đóng góp chính của bài báo:}"
    )
    s1_repl5 = (
        r"\noindent\textbf{5. Đóng góp khoa học cốt lõi của bài báo:}"
    )
    if r"\noindent\textbf{5. Đóng góp khoa học cốt lõi của bài báo:}" not in content:
        content = content.replace(s1_target5, s1_repl5)

    s1_target6 = (
        r"\end{itemize}" "\n\n"
        r"Cấu trúc các phần tiếp theo của bài báo:"
    )
    s1_repl6 = (
        r"\end{itemize}" "\n\n"
        r"\noindent\textbf{6. Cấu trúc tổ chức của bài báo:}\\" "\n"
        r"Cấu trúc các phần tiếp theo của bài báo:"
    )
    if r"\noindent\textbf{6. Cấu trúc tổ chức của bài báo:}" not in content:
        content = content.replace(s1_target6, s1_repl6)

    # 3. Section 2 bold paragraph headings
    # 2.2 Related Work
    s2_rw_target = (
        r"\subsection{Các nghiên cứu liên quan (Related Work)}" "\n"
        r"Nghiên cứu về $N$-Queens đã trải qua hơn 170 năm"
    )
    s2_rw_repl = (
        r"\subsection{Các nghiên cứu liên quan (Related Work)}" "\n\n"
        r"\noindent\textbf{Tiến trình nghiên cứu và Kết quả giải tích:}\\" "\n"
        r"Nghiên cứu về $N$-Queens đã trải qua hơn 170 năm"
    )
    if r"\noindent\textbf{Tiến trình nghiên cứu và Kết quả giải tích:}" not in content:
        content = content.replace(s2_rw_target, s2_rw_repl)

    s2_rw_target2 = (
        "\n\n"
        r"Tuy nhiên, các thuật toán heuristic và công thức giải tích chỉ giải quyết"
    )
    s2_rw_repl2 = (
        "\n\n"
        r"\noindent\textbf{Giới hạn của Heuristic và Nhu cầu về Bộ giải chính xác:}\\" "\n"
        r"Tuy nhiên, các thuật toán heuristic và công thức giải tích chỉ giải quyết"
    )
    if r"\noindent\textbf{Giới hạn của Heuristic và Nhu cầu về Bộ giải chính xác:}" not in content:
        content = content.replace(s2_rw_target2, s2_rw_repl2)

    s2_rw_target3 = (
        "\n\n"
        r"Trong lĩnh vực SAT Solving, việc mã hóa các ràng buộc số lượng"
    )
    s2_rw_repl3 = (
        "\n\n"
        r"\noindent\textbf{Các nghiên cứu nền tảng về kỹ thuật mã hóa AMO trong SAT:}\\" "\n"
        r"Trong lĩnh vực SAT Solving, việc mã hóa các ràng buộc số lượng"
    )
    if r"\noindent\textbf{Các nghiên cứu nền tảng về kỹ thuật mã hóa AMO trong SAT:}" not in content:
        content = content.replace(s2_rw_target3, s2_rw_repl3)

    # 2.3 ILP
    s2_ilp_target = (
        r"\subsection{Mô hình Quy hoạch Tuyến tính Nguyên (ILP Formulation)}" "\n"
        r"Trong mô hình ILP 0-1, ta định nghĩa biến nhị phân"
    )
    s2_ilp_repl = (
        r"\subsection{Mô hình Quy hoạch Tuyến tính Nguyên (ILP Formulation)}" "\n\n"
        r"\noindent\textbf{Không gian biến quyết định nhị phân:}\\" "\n"
        r"Trong mô hình ILP 0-1, ta định nghĩa biến nhị phân"
    )
    if r"\noindent\textbf{Không gian biến quyết định nhị phân:}" not in content:
        content = content.replace(s2_ilp_target, s2_ilp_repl)

    s2_ilp_target2 = (
        "\n\n"
        r"Mô hình ILP được thiết lập như sau:" "\n"
        r"\begin{align}"
    )
    s2_ilp_repl2 = (
        "\n\n"
        r"\noindent\textbf{Hệ phương trình và bất phương trình ràng buộc ILP:}\\" "\n"
        r"Mô hình ILP được thiết lập như sau:" "\n"
        r"\begin{align}"
    )
    if r"\noindent\textbf{Hệ phương trình và bất phương trình ràng buộc ILP:}" not in content:
        content = content.replace(s2_ilp_target2, s2_ilp_repl2)

    s2_ilp_target3 = (
        r"\end{align}" "\n"
        r"Phương trình \eqref{eq:ilp-row} và \eqref{eq:ilp-col} đảm bảo"
    )
    s2_ilp_repl3 = (
        r"\end{align}" "\n"
        r"\noindent\textbf{Ý nghĩa ràng buộc và Thách thức nới lỏng tuyến tính (LP Relaxation):}\\" "\n"
        r"Phương trình \eqref{eq:ilp-row} và \eqref{eq:ilp-col} đảm bảo"
    )
    if r"\noindent\textbf{Ý nghĩa ràng buộc và Thách thức nới lỏng tuyến tính (LP Relaxation):}" not in content:
        content = content.replace(s2_ilp_target3, s2_ilp_repl3)

    # 2.4 CP
    s2_cp_target = (
        r"\subsection{Mô hình Lập trình Ràng buộc (CP Formulation)}" "\n"
        r"Tiếp cận Lập trình Ràng buộc (CP) biểu diễn bài toán"
    )
    s2_cp_repl = (
        r"\subsection{Mô hình Lập trình Ràng buộc (CP Formulation)}" "\n\n"
        r"\noindent\textbf{Biểu diễn biến chỉ số và miền giá trị nguyên:}\\" "\n"
        r"Tiếp cận Lập trình Ràng buộc (CP) biểu diễn bài toán"
    )
    if r"\noindent\textbf{Biểu diễn biến chỉ số và miền giá trị nguyên:}" not in content:
        content = content.replace(s2_cp_target, s2_cp_repl)

    s2_cp_target2 = (
        "\n\n"
        r"Mô hình CP tương ứng:" "\n"
        r"\begin{align}"
    )
    s2_cp_repl2 = (
        "\n\n"
        r"\noindent\textbf{Hệ ràng buộc toàn cục AllDifferent:}\\" "\n"
        r"Mô hình CP tương ứng:" "\n"
        r"\begin{align}"
    )
    if r"\noindent\textbf{Hệ ràng buộc toàn cục AllDifferent:}" not in content:
        content = content.replace(s2_cp_target2, s2_cp_repl2)

    s2_cp_target3 = (
        r"\end{align}" "\n"
        r"Toán tử toàn cục \texttt{AllDifferent} cho phép bộ giải"
    )
    s2_cp_repl3 = (
        r"\end{align}" "\n"
        r"\noindent\textbf{Cơ chế suy diễn và Hạn chế cấu hình đơn luồng:}\\" "\n"
        r"Toán tử toàn cục \texttt{AllDifferent} cho phép bộ giải"
    )
    if r"\noindent\textbf{Cơ chế suy diễn và Hạn chế cấu hình đơn luồng:}" not in content:
        content = content.replace(s2_cp_target3, s2_cp_repl3)

    # 4. Section 3 bold headings
    s3_1_target = (
        r"\subsection{Không gian biến logic và Phân rã Ràng buộc}" "\n"
        r"Ta khai báo $N^2$ biến logic cơ sở"
    )
    s3_1_repl = (
        r"\subsection{Không gian biến logic và Phân rã Ràng buộc}" "\n\n"
        r"\noindent\textbf{Định nghĩa không gian biến mệnh đề cơ sở:}\\" "\n"
        r"Ta khai báo $N^2$ biến logic cơ sở"
    )
    if r"\noindent\textbf{Định nghĩa không gian biến mệnh đề cơ sở:}" not in content:
        content = content.replace(s3_1_target, s3_1_repl)

    s3_1_target2 = (
        "\n\n"
        r"Nguyên lý phân rã ràng buộc \textit{Exactly-One} (EO)"
    )
    s3_1_repl2 = (
        "\n\n"
        r"\noindent\textbf{Nguyên lý phân rã ràng buộc Đúng-Một (Exactly-One):}\\" "\n"
        r"Nguyên lý phân rã ràng buộc \textit{Exactly-One} (EO)"
    )
    if r"\noindent\textbf{Nguyên lý phân rã ràng buộc Đúng-Một (Exactly-One):}" not in content:
        content = content.replace(s3_1_target2, s3_1_repl2)

    s3_1_target3 = (
        r"\end{itemize}" "\n\n"
        r"Các đường chéo (chính và phụ) có độ dài $\ge 2$"
    )
    s3_1_repl3 = (
        r"\end{itemize}" "\n\n"
        r"\noindent\textbf{Quy tắc ràng buộc trên các đường chéo:}\\" "\n"
        r"Các đường chéo (chính và phụ) có độ dài $\ge 2$"
    )
    if r"\noindent\textbf{Quy tắc ràng buộc trên các đường chéo:}" not in content:
        content = content.replace(s3_1_target3, s3_1_repl3)

    # 3.2 AMO subsubsections
    # 3.2.1 Pairwise
    s3_pw_target = (
        r"\subsubsection{1. Pairwise Encoding (Mã hóa Cặp trực tiếp)}" "\n"
        r"Cấm trực tiếp mọi cặp biến"
    )
    s3_pw_repl = (
        r"\subsubsection{1. Pairwise Encoding (Mã hóa Cặp trực tiếp)}" "\n"
        r"\textbf{Nguyên lý mã hóa:}\\" "\n"
        r"Cấm trực tiếp mọi cặp biến"
    )
    if r"\textbf{Nguyên lý mã hóa:}\\" "\n" r"Cấm trực tiếp mọi cặp biến" not in content:
        content = content.replace(s3_pw_target, s3_pw_repl)

    s3_pw_target2 = (
        r"\end{equation}" "\n"
        r"Số mệnh đề cho 1 nhóm là $\binom{k}{2} = \mathcal{O}(k^2)$."
    )
    s3_pw_repl2 = (
        r"\end{equation}" "\n"
        r"\textbf{Độ phức tạp và Triển khai:}\\" "\n"
        r"Số mệnh đề cho 1 nhóm là $\binom{k}{2} = \mathcal{O}(k^2)$."
    )
    if r"\textbf{Độ phức tạp và Triển khai:}\\" "\n" r"Số mệnh đề cho 1 nhóm là $\binom{k}{2}" not in content:
        content = content.replace(s3_pw_target2, s3_pw_repl2)

    # 3.2.2 Sequential
    s3_seq_target = (
        r"\subsubsection{2. Sequential Counter Encoding (Bộ đếm Tuần tự Sinz, 2005)}" "\n"
        r"Sử dụng $k-1$ biến phụ"
    )
    s3_seq_repl = (
        r"\subsubsection{2. Sequential Counter Encoding (Bộ đếm Tuần tự Sinz, 2005)}" "\n"
        r"\textbf{Nguyên lý mã hóa:}\\" "\n"
        r"Sử dụng $k-1$ biến phụ"
    )
    if r"\textbf{Nguyên lý mã hóa:}\\" "\n" r"Sử dụng $k-1$ biến phụ" not in content:
        content = content.replace(s3_seq_target, s3_seq_repl)

    s3_seq_target2 = (
        r"\end{align}" "\n"
        r"Số biến phụ là $k - 1 = \mathcal{O}(k)$."
    )
    s3_seq_repl2 = (
        r"\end{align}" "\n"
        r"\textbf{Độ phức tạp và Triển khai:}\\" "\n"
        r"Số biến phụ là $k - 1 = \mathcal{O}(k)$."
    )
    if r"\textbf{Độ phức tạp và Triển khai:}\\" "\n" r"Số biến phụ là $k - 1 = \mathcal{O}(k)$." not in content:
        content = content.replace(s3_seq_target2, s3_seq_repl2)

    # 3.2.3 Commander
    s3_cmd_target = (
        r"\subsubsection{3. Commander Variable Encoding (Klieber \& Kwon, 2007)}" "\n"
        r"\textit{(Tự cài đặt độc lập - Thư viện PySAT CardEnc chuẩn không tích hợp sẵn phương pháp này)}.\\" "\n"
        r"Chia $k$ biến thành các nhóm nhỏ"
    )
    s3_cmd_repl = (
        r"\subsubsection{3. Commander Variable Encoding (Klieber \& Kwon, 2007)}" "\n"
        r"\textit{(Tự cài đặt độc lập - Thư viện PySAT CardEnc chuẩn không tích hợp sẵn phương pháp này)}.\\" "\n"
        r"\textbf{Nguyên lý mã hóa:}\\" "\n"
        r"Chia $k$ biến thành các nhóm nhỏ"
    )
    if r"\textbf{Nguyên lý mã hóa:}\\" "\n" r"Chia $k$ biến thành các nhóm nhỏ" not in content:
        content = content.replace(s3_cmd_target, s3_cmd_repl)

    s3_cmd_target2 = (
        r"\end{enumerate}" "\n"
        r"Số biến phụ $\mathcal{O}(k)$, số mệnh đề $\mathcal{O}(k)$."
    )
    s3_cmd_repl2 = (
        r"\end{enumerate}" "\n"
        r"\textbf{Độ phức tạp:}\\" "\n"
        r"Số biến phụ $\mathcal{O}(k)$, số mệnh đề $\mathcal{O}(k)$."
    )
    if r"\textbf{Độ phức tạp:}\\" "\n" r"Số biến phụ $\mathcal{O}(k)$, số mệnh đề $\mathcal{O}(k)$." not in content:
        content = content.replace(s3_cmd_target2, s3_cmd_repl2)

    # 3.2.4 Binary
    s3_bin_target = (
        r"\subsubsection{4. Binary / Bitwise Encoding (Prestwich, 2009; Frisch \& Giannaros, 2010)}" "\n"
        r"Sử dụng $m = \lceil \log_2 k \rceil$ biến phụ nhị phân"
    )
    s3_bin_repl = (
        r"\subsubsection{4. Binary / Bitwise Encoding (Prestwich, 2009; Frisch \& Giannaros, 2010)}" "\n"
        r"\textbf{Nguyên lý mã hóa:}\\" "\n"
        r"Sử dụng $m = \lceil \log_2 k \rceil$ biến phụ nhị phân"
    )
    if r"\textbf{Nguyên lý mã hóa:}\\" "\n" r"Sử dụng $m = \lceil \log_2 k \rceil$" not in content:
        content = content.replace(s3_bin_target, s3_bin_repl)

    s3_bin_target2 = (
        r"với $\ell(b_j, 1) = b_j$ và $\ell(b_j, 0) = \neg b_j$. Số biến phụ $\lceil \log_2 k \rceil = \mathcal{O}(\log k)$, số mệnh đề $\mathcal{O}(k \log k)$."
    )
    s3_bin_repl2 = (
        r"với $\ell(b_j, 1) = b_j$ và $\ell(b_j, 0) = \neg b_j$." "\n\n"
        r"\textbf{Độ phức tạp và Triển khai:}\\" "\n"
        r"Số biến phụ $\lceil \log_2 k \rceil = \mathcal{O}(\log k)$, số mệnh đề $\mathcal{O}(k \log k)$."
    )
    if r"\textbf{Độ phức tạp và Triển khai:}\\" "\n" r"Số biến phụ $\lceil \log_2 k \rceil = \mathcal{O}(\log k)$" not in content:
        content = content.replace(s3_bin_target2, s3_bin_repl2)

    # 3.2.5 Product
    s3_prd_target = (
        r"\subsubsection{5. Product Encoding (Chen, 2010)}" "\n"
        r"\textit{(Tự cài đặt độc lập - Thư viện PySAT CardEnc chuẩn không tích hợp sẵn phương pháp này)}.\\" "\n"
        r"Ánh xạ biến vào lưới"
    )
    s3_prd_repl = (
        r"\subsubsection{5. Product Encoding (Chen, 2010)}" "\n"
        r"\textit{(Tự cài đặt độc lập - Thư viện PySAT CardEnc chuẩn không tích hợp sẵn phương pháp này)}.\\" "\n"
        r"\textbf{Nguyên lý mã hóa:}\\" "\n"
        r"Ánh xạ biến vào lưới"
    )
    if r"\textbf{Nguyên lý mã hóa:}\\" "\n" r"Ánh xạ biến vào lưới" not in content:
        content = content.replace(s3_prd_target, s3_prd_repl)

    s3_prd_target2 = (
        r"\end{align}" "\n"
        r"Số biến phụ $p + q = \mathcal{O}(\sqrt{k})$, số mệnh đề $\mathcal{O}(k)$."
    )
    s3_prd_repl2 = (
        r"\end{align}" "\n"
        r"\textbf{Độ phức tạp:}\\" "\n"
        r"Số biến phụ $p + q = \mathcal{O}(\sqrt{k})$, số mệnh đề $\mathcal{O}(k)$."
    )
    if r"\textbf{Độ phức tạp:}\\" "\n" r"Số biến phụ $p + q = \mathcal{O}(\sqrt{k})$" not in content:
        content = content.replace(s3_prd_target2, s3_prd_repl2)

    # 3.3 Symmetry breaking
    s3_3_target = (
        r"\subsection{Kỹ thuật Phá vỡ Đối xứng (Symmetry Breaking)}" "\n"
        r"Nhóm đối xứng của bài toán $N$-Queens"
    )
    s3_3_repl = (
        r"\subsection{Kỹ thuật Phá vỡ Đối xứng (Symmetry Breaking)}" "\n\n"
        r"\noindent\textbf{Cấu trúc nhóm đối xứng của bàn cờ ($D_4$):}\\" "\n"
        r"Nhóm đối xứng của bài toán $N$-Queens"
    )
    if r"\noindent\textbf{Cấu trúc nhóm đối xứng của bàn cờ ($D_4$):}" not in content:
        content = content.replace(s3_3_target, s3_3_repl)

    s3_3_target2 = (
        r"\end{proof}" "\n\n"
        r"\textit{Ghi chú thực nghiệm:} Phá vỡ đối xứng"
    )
    s3_3_repl2 = (
        r"\end{proof}" "\n\n"
        r"\noindent\textbf{Ghi chú thực nghiệm về việc loại trừ đối xứng trong đánh giá:}\\" "\n"
        r"\textit{Ghi chú thực nghiệm:} Phá vỡ đối xứng"
    )
    if r"\noindent\textbf{Ghi chú thực nghiệm về việc loại trừ đối xứng trong đánh giá:}" not in content:
        content = content.replace(s3_3_target2, s3_3_repl2)

    # 3.4 Correctness proof
    s3_4_target = (
        r"\begin{proof}" "\n"
        r"$(\implies)$ Giả sử công thức $\mathcal{F}_{\text{NQueens}}$ có một phép gán"
    )
    s3_4_repl = (
        r"\begin{proof}" "\n"
        r"\noindent\textbf{1. Chứng minh chiều thuận ($\implies$ - Tính đúng đắn / Soundness):}\\" "\n"
        r"Giả sử công thức $\mathcal{F}_{\text{NQueens}}$ có một phép gán"
    )
    if r"\noindent\textbf{1. Chứng minh chiều thuận" not in content:
        content = content.replace(s3_4_target, s3_4_repl)

    s3_4_target2 = (
        r"$(\impliedby)$ Ngược lại, giả sử tồn tại nghiệm hợp lệ"
    )
    s3_4_repl2 = (
        r"\noindent\textbf{2. Chứng minh chiều nghịch ($\impliedby$ - Tính đầy đủ / Completeness):}\\" "\n"
        r"Ngược lại, giả sử tồn tại nghiệm hợp lệ"
    )
    if r"\noindent\textbf{2. Chứng minh chiều nghịch" not in content:
        content = content.replace(s3_4_target2, s3_4_repl2)

    # 5. Section 4.1 hardware and software environment
    s4_1_target = (
        r"Toàn bộ các thí nghiệm được triển khai và đo lường trên máy trạm có cấu hình:" "\n"
        r"\begin{itemize}" "\n"
        r"    \item \textbf{Bộ vi xử lý (CPU):}"
    )
    s4_1_repl = (
        r"Toàn bộ các thí nghiệm được triển khai và đo lường trên máy trạm có cấu hình:" "\n"
        r"\begin{itemize}" "\n"
        r"    \item \textbf{Cấu hình vi xử lý (CPU):}"
    )
    content = content.replace(s4_1_target, s4_1_repl)

    # In 4.1 sublist items
    content = content.replace(
        r"\item Để loại trừ triệt để ảnh hưởng của phân mảnh bộ nhớ",
        r"\item \textbf{Cách ly tiến trình (\texttt{subprocess}):} Để loại trừ triệt để ảnh hưởng của phân mảnh bộ nhớ"
    )
    content = content.replace(
        r"\item Toàn bộ số liệu trong Bảng 2 và Bảng 4",
        r"\item \textbf{Tính nhất quán dữ liệu:} Toàn bộ số liệu trong Bảng 2 và Bảng 4"
    )

    # Section 4.2 findings bolded
    content = content.replace(
        r"\item \textbf{Mối quan hệ phi tuyến giữa số lượng mệnh đề và thời gian giải:}",
        r"\item \textbf{Phát hiện 1 (Mối quan hệ phi tuyến giữa số mệnh đề và thời gian giải):}"
    )
    content = content.replace(
        r"\item \textbf{Phân tích động lực tìm kiếm CDCL (CDCL Search Dynamics):}",
        r"\item \textbf{Phát hiện 2 (Phân tích vi mô động lực tìm kiếm CDCL - CDCL Search Dynamics):}"
    )
    content = content.replace(
        r"\item \textbf{Ưu thế của Commander Variable ở dải $N \in [16, 128]$:}",
        r"\item \textbf{Phát hiện 3 (Ưu thế vượt trội của Commander Variable ở dải $N \in [16, 128]$):}"
    )
    content = content.replace(
        r"\item \textbf{Đặc điểm của Binary và Product Encoding:}",
        r"\item \textbf{Phát hiện 4 (Đặc tính cân bằng của Binary và Product Encoding):}"
    )
    content = content.replace(
        r"\item \textbf{Thời gian mã hóa và Bộ nhớ ở quy mô lớn:}",
        r"\item \textbf{Phát hiện 5 (Chi phí thời gian mã hóa và Bộ nhớ ở quy mô cực đại $N \ge 256$):}"
    )

    # Section 4.3 solver comparison findings bolded
    content = content.replace(
        r"\item \textbf{Hiệu năng của Gurobi và ILP:}",
        r"\item \textbf{Khía cạnh 1 (Hiệu năng của Gurobi 13.0 và SCIP - Trường phái ILP):}"
    )
    content = content.replace(
        r"\item \textbf{Hiệu năng của Google OR-Tools CP-SAT và Hạn chế cấu hình:}",
        r"\item \textbf{Khía cạnh 2 (Hiệu năng của Google OR-Tools CP-SAT - Trường phái CP):}"
    )
    content = content.replace(
        r"\item \textbf{So sánh hai chiều giữa Glucose 4.2 và CaDiCaL:}",
        r"\item \textbf{Khía cạnh 3 (So sánh đối đầu giữa Glucose 4.2 và CaDiCaL 1.9.5):}"
    )
    content = content.replace(
        r"\item \textbf{Khả năng mở rộng của SAT CaDiCaL và Bản chất độ biến động thời gian ở quy mô cực đại ($N \ge 256$):}",
        r"\item \textbf{Khía cạnh 4 (Khả năng mở rộng của SAT CaDiCaL và Bản chất độ biến động thời gian ở quy mô cực đại $N \ge 256$):}"
    )

    # 6. Section 5 structured subsections
    s5_target = (
        r"\section{Kết luận và Thảo luận (Conclusion \& Discussion)}" "\n"
        r"Bài báo đã nghiên cứu, cài đặt và đánh giá toàn diện phương pháp giải chính xác"
    )
    s5_repl = (
        r"\section{Kết luận và Thảo luận (Conclusion \& Discussion)}" "\n\n"
        r"\subsection{Kết luận tổng kết (Summary of Findings)}" "\n"
        r"Bài báo đã nghiên cứu, cài đặt và đánh giá toàn diện phương pháp giải chính xác"
    )
    if r"\subsection{Kết luận tổng kết (Summary of Findings)}" not in content:
        content = content.replace(s5_target, s5_repl)

    s5_lim_target = (
        r"\textbf{Thảo luận về Hạn chế (Limitations):}\\" "\n"
        r"Cần nhấn mạnh rằng bài toán $N$-Queens"
    )
    s5_lim_repl = (
        r"\subsection{Hạn chế của nghiên cứu (Limitations)}" "\n"
        r"Cần nhấn mạnh rằng bài toán $N$-Queens"
    )
    if r"\subsection{Hạn chế của nghiên cứu (Limitations)}" not in content:
        content = content.replace(s5_lim_target, s5_lim_repl)

    s5_fut_target = (
        r"\textbf{Hướng phát triển tương lai:}\\" "\n"
        r"Mở rộng mô hình SAT cho các biến thể"
    )
    s5_fut_repl = (
        r"\subsection{Hướng phát triển trong tương lai (Future Research Directions)}" "\n"
        r"Mở rộng mô hình SAT cho các biến thể"
    )
    if r"\subsection{Hướng phát triển trong tương lai (Future Research Directions)}" not in content:
        content = content.replace(s5_fut_target, s5_fut_repl)

    # Section 5 bullet points bolded lead-ins
    content = content.replace(
        r"\item Mã hóa Pairwise bùng nổ đa thức bậc ba",
        r"\item \textbf{Bùng nổ bộ nhớ của Pairwise:} Mã hóa Pairwise bùng nổ đa thức bậc ba"
    )
    content = content.replace(
        r"\item Sequential Counter tuy giảm số mệnh đề xuống",
        r"\item \textbf{Suy thoái tìm kiếm của Sequential Counter:} Sequential Counter tuy giảm số mệnh đề xuống"
    )
    content = content.replace(
        r"\item Commander Variable và Product Encoding là hai kỹ thuật",
        r"\item \textbf{Năng lực mở rộng của Commander và Product:} Commander Variable và Product Encoding là hai kỹ thuật"
    )
    content = content.replace(
        r"\item So sánh đối chứng thực nghiệm cho thấy SAT Solving",
        r"\item \textbf{Vị thế vượt trội của SAT Solving trước ILP và CP:} So sánh đối chứng thực nghiệm cho thấy SAT Solving"
    )

    return content

def main():
    for fname in ["nqueens_report_elsevier.tex", "main.tex", "nqueens_report_standard.tex"]:
        path = os.path.join(report_dir, fname)
        if os.path.exists(path):
            content = read_file(path)
            new_content = enhance_bold_headings(content)
            write_file(path, new_content)
            print(f"Updated bold headings in {fname}")

if __name__ == "__main__":
    main()
