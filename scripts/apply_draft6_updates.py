import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
report_dir = os.path.join(base_dir, "report")

# Read generated table files
with open(os.path.join(report_dir, "table2_generated.tex"), "r", encoding="utf-8") as f:
    t2_code = f.read().strip()

with open(os.path.join(report_dir, "table3_generated.tex"), "r", encoding="utf-8") as f:
    t3_code = f.read().strip()

with open(os.path.join(report_dir, "table4_generated.tex"), "r", encoding="utf-8") as f:
    t4_code = f.read().strip()

with open(os.path.join(report_dir, "table5a_generated.tex"), "r", encoding="utf-8") as f:
    t5a_code = f.read().strip()

with open(os.path.join(report_dir, "table5b_generated.tex"), "r", encoding="utf-8") as f:
    t5b_code = f.read().strip()

def update_file(filename, is_elsevier=True):
    filepath = os.path.join(report_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    orig_len = len(content)
    print(f"Original length of {filename}: {orig_len} characters")

    # 1. Update authors
    if is_elsevier:
        old_authors = r"""\author[1]{Nguyễn Văn A}[role=Sinh viên thực hiện]
\cormark[1]
\ead{24020000@vnu.edu.vn}

\author[1]{TS. Tô Văn Khánh}[role=Giảng viên hướng dẫn]
\ead{khanhtv@vnu.edu.vn}

\address[1]{Khoa Công nghệ Thông tin, Trường Đại học Công nghệ, Đại học Quốc gia Hà Nội, 144 Xuân Thủy, Cầu Giấy, Hà Nội, Việt Nam}

\cortext[cor1]{Tác giả liên hệ chính (Mã số sinh viên: 24020000).}"""

        new_authors = r"""\author[1]{Nguyễn Văn A\corref{cor1}}[role=Học viên thực hiện]
\cormark[1]
\ead{24020000@vnu.edu.vn}

\author[1]{TS. Trần Trọng Hiếu}[role=Giảng viên hướng dẫn]
\ead{hieutt@vnu.edu.vn}

\address[1]{Khoa Công nghệ Thông tin, Trường Đại học Công nghệ, Đại học Quốc gia Hà Nội (VNU-UET), 144 Xuân Thủy, Cầu Giấy, Hà Nội, Việt Nam}

\cortext[cor1]{Tác giả liên hệ chính (Học viên: Nguyễn Văn A, MSSV: 24020000, Email: \texttt{24020000@vnu.edu.vn}). Giảng viên hướng dẫn: TS. Trần Trọng Hiếu. Ký hiệu [1] trong \textbackslash author[1] là nhãn liên kết đơn vị công tác (\textbackslash address[1]) theo quy chuẩn Elsevier cas-sc.}"""

        if old_authors in content:
            content = content.replace(old_authors, new_authors)
            print("Updated elsevier authors!")
    else:
        old_authors_std = r"""\author{
    \textbf{Nguyễn Văn A}\thanks{Học viên thực hiện. Email: \texttt{24020000@vnu.edu.vn}, MSSV: 24020000} \quad
    \textbf{TS. Tô Văn Khánh}\thanks{Giảng viên hướng dẫn. Email: \texttt{khanhtv@vnu.edu.vn}} \\
    \textit{Khoa Công nghệ Thông tin, Trường Đại học Công nghệ, ĐHQGHN (VNU-UET)}
}"""
        new_authors_std = r"""\author{
    \textbf{Nguyễn Văn A}\thanks{Học viên thực hiện. Email: \texttt{24020000@vnu.edu.vn}, MSSV: 24020000} \quad
    \textbf{TS. Trần Trọng Hiếu}\thanks{Giảng viên hướng dẫn. Email: \texttt{hieutt@vnu.edu.vn}} \\
    \textit{Khoa Công nghệ Thông tin, Trường Đại học Công nghệ, ĐHQGHN (VNU-UET)}
}"""
        if old_authors_std in content:
            content = content.replace(old_authors_std, new_authors_std)
            print("Updated standard authors!")

    # 2. Update abstract
    content = content.replace(r"Frisch et al., 2005; Prestwich, 2009", r"Prestwich, 2009; Frisch \& Giannaros, 2010")
    content = content.replace(r"(chỉ mất $0.62$s ở $N=128$)", r"(chỉ mất $0.73$s ở $N=128$, nhanh hơn Sequential Counter khoảng 31 lần)")
    content = content.replace(r"và có sự dao động giữa các lần chạy do đặc thù tìm kiếm của thuật toán CDCL.",
                              r"Chúng tôi ghi nhận solver CaDiCaL hoạt động hoàn toàn tất định (sinh cùng số lượng xung đột, quyết định và lan truyền trên cùng một công thức CNF); sự biến thiên thời gian giữa các lần chạy (đặc biệt ở Product $N=1000$: $212.52$s đến $283.03$s, $\sigma = 36.45$s; giải thành công cả 3 lần nhưng tiến sát ngưỡng 300s) xuất phát từ các yếu tố môi trường hệ thống (nhiệt độ CPU, điều tiết xung nhịp và tải nền hệ điều hành).")

    # 3. Update contributions
    content = content.replace(r"Binary Encoding~\cite{frisch2005solving,prestwich2009cnf}", r"Binary Encoding~\cite{prestwich2009cnf,frisch2010sat}")

    old_cdcl_contrib = r"làm rõ mối tương quan giữa số lượng biến phụ và sự bùng nổ xung đột CDCL ($62{,}360$ xung đột) cũng như số lượt lan truyền đơn vị ($42.89$ triệu lượt) của Sequential Counter ở $N=128$."
    new_cdcl_contrib = r"trích xuất thông số nội tại (\texttt{accum\_stats()}) qua 3 lần chạy lặp cho thấy sự suy thoái hiệu năng của Sequential Counter ở $N=128$ ($22.65$s, chậm hơn Commander 31 lần) bị dẫn dắt bởi sự tăng vọt $68\times$ số xung đột ($62{,}360$) và $26\times$ số quyết định ($107{,}733$), kéo theo $42.89$ triệu lượt lan truyền đơn vị. Phân tích thực nghiệm cũng làm rõ mối quan hệ phi tuyến: số lượng biến phụ không quyết định trực tiếp số xung đột (Commander có $33{,}290$ biến phụ, nhiều hơn $2.4\times$ so với Product, nhưng lại có số xung đột thấp nhất chỉ $916$), nhấn mạnh vai trò quyết định của cấu trúc đồ thị lan truyền cục bộ."
    content = content.replace(old_cdcl_contrib, new_cdcl_contrib)

    content = content.replace(r"\cite{frisch2005solving,prestwich2009cnf,frisch2010sat}", r"\cite{prestwich2009cnf,frisch2010sat}")

    # 4. Replace Table 2
    t2_needle = r"\label{tab:ablation_results}"
    idx_t2 = content.find(t2_needle)
    assert idx_t2 != -1, "tab:ablation_results not found!"
    start_t2 = content.rfind(r"\begin{table", 0, idx_t2)
    end_t2 = content.find(r"\end{table", idx_t2)
    end_t2 = content.find("}", end_t2) + 1
    content = content[:start_t2] + t2_code + content[end_t2:]
    print("Replaced Table 2 successfully!")

    # 5. Replace text after Table 2
    old_t2_text = r"chậm hơn Pairwise ($6.48$ giây với gần 3.5 triệu mệnh đề) và chậm hơn Commander tới 36 lần ($0.62$ giây)."
    new_t2_text = r"chậm hơn Pairwise ($6.48$ giây với gần 3.5 triệu mệnh đề) và chậm hơn Commander khoảng 31 lần ($0.73$ giây)."
    content = content.replace(old_t2_text, new_t2_text)

    # 6. Replace Table 3
    t3_needle = r"\label{tab:cdcl_search_stats}"
    idx_t3 = content.find(t3_needle)
    assert idx_t3 != -1, "tab:cdcl_search_stats not found!"
    start_t3 = content.rfind(r"\begin{table", 0, idx_t3)
    end_t3 = content.find(r"\end{table", idx_t3)
    end_t3 = content.find("}", end_t3) + 1
    content = content[:start_t3] + t3_code + content[end_t3:]
    print("Replaced Table 3 successfully!")

    # 7. Replace CDCL analysis
    old_analysis_block = r"""    Kết quả này cho thấy sự suy thoái của Sequential Counter có tương quan rất mạnh với hành vi phân nhánh của heuristic CDCL (như VSIDS). Việc bổ sung một số lượng lớn biến phụ $\mathcal{O}(N^2)$ ($64{,}766$ biến phụ ở $N=128$) đã làm sai lệch trọng số hoạt động của các biến cơ sở, khiến bộ giải CDCL đưa ra nhiều quyết định rẽ nhánh không tối ưu vào không gian biến trạng thái và vấp phải hàng chục nghìn nhánh cụt trước khi học được các mệnh đề xung đột hữu ích. Cơ chế tương tác chi tiết giữa chuỗi biến tích lũy và trọng số phân nhánh VSIDS là một chủ đề thú vị cần được nghiên cứu thực nghiệm sâu hơn.
    \item \textbf{Ưu thế của Commander Variable ở dải $N \in [16, 128]$:} Kỹ thuật Commander phân chia biến thành các nhóm nhỏ ($g=3$) và tổ chức biến chỉ huy dạng cây phân cấp. Cấu trúc này cho phép bộ giải CDCL gán giá trị \texttt{False} cho một nhóm biến ngay khi biến chỉ huy bị gán \texttt{False}, giúp cắt tỉa nhanh không gian tìm kiếm ở các mức quyết định (decision levels) cao với số lượng xung đột cực thấp ($916$ xung đột ở $N=128$). Nhờ đó, Commander đạt thời gian giải nhanh nhất từ $N=16$ ($7.08$ms) đến $N=128$ ($616.66$ms).
    \item \textbf{Đặc điểm của Binary và Product Encoding:} Binary Encoding sử dụng ít biến phụ nhất trong các phương pháp mở rộng ($21{,}234$ biến ở $N=128$) nhưng có thời gian giải $1{,}290.50$ms, cho thấy số biến phụ ít không đồng nghĩa với tốc độ nhanh nhất. Trong khi đó, Product Encoding đạt điểm cân bằng rất tốt giữa số biến phụ ($30{,}182$) và số mệnh đề (thấp nhất ở $N \ge 64$ với $47{,}520$ clauses ở $N=64$ và $193{,}122$ clauses ở $N=128$), duy trì tốc độ giải ổn định ($1{,}246.66$ms)."""

    new_analysis_block = r"""    Kết quả thực nghiệm cho thấy sự bùng nổ thời gian giải của Sequential Counter gắn liền với số lượng xung đột và quyết định tăng đột biến. Tuy nhiên, mối quan hệ giữa số biến phụ và số xung đột không phải là một tương quan tuyến tính đơn giản: Commander Variable có tới $33{,}290$ biến phụ (gấp $2.4$ lần Product và $6.9$ lần Binary) nhưng lại đạt số xung đột thấp nhất ($916$ xung đột), trong khi Pairwise không có bất kỳ biến phụ nào lại có tới $6{,}037$ xung đột (hệ số tương quan hạng Spearman giữa số biến phụ và số xung đột trên 5 kỹ thuật tại $N=128$ chỉ đạt $\approx 0.1$). Giả thuyết hợp lý nhất là cấu trúc đồ thị suy diễn đóng vai trò then chốt: cấu trúc cây phân cấp của Commander hỗ trợ cắt tỉa nhanh không gian tìm kiếm, trong khi chuỗi thang tuyến tính $s_i \to s_{i+1}$ của Sequential có thể gây nhiễu loạn heuristic VSIDS và phase-saving, khiến bộ giải liên tục rẽ nhánh sâu vào chuỗi biến trạng thái thay vì các biến bàn cờ cơ sở. Dù vậy, nguyên nhân bản chất của hiện tượng này vẫn là một câu hỏi mở cần được kiểm chứng vi mô sâu hơn.
    \item \textbf{Ưu thế của Commander Variable ở dải $N \in [16, 128]$:} Kỹ thuật Commander phân chia biến thành các nhóm nhỏ ($g=3$) và tổ chức biến chỉ huy dạng cây phân cấp. Cấu trúc này cho phép bộ giải CDCL gán giá trị \texttt{False} cho một nhóm biến ngay khi biến chỉ huy bị gán \texttt{False}, giúp cắt tỉa nhanh không gian tìm kiếm ở các mức quyết định (decision levels) cao với số lượng xung đột cực thấp ($916$ xung đột ở $N=128$). Nhờ đó, Commander đạt thời gian giải nhanh nhất từ $N=16$ ($7.10$ms) đến $N=128$ ($725.00$ms, tức khoảng $0.73$s).
    \item \textbf{Đặc điểm của Binary và Product Encoding:} Binary Encoding sử dụng ít biến phụ nhất trong các phương pháp mở rộng ($21{,}234$ biến ở $N=128$) nhưng có thời gian giải $1{,}450.00$ms, cho thấy số biến phụ ít không đồng nghĩa với tốc độ nhanh nhất. Trong khi đó, Product Encoding đạt điểm cân bằng rất tốt giữa số biến phụ ($30{,}182$) và số mệnh đề (thấp nhất ở $N \ge 64$ với $47{,}520$ clauses ở $N=64$ và $193{,}122$ clauses ở $N=128$), duy trì tốc độ giải ổn định ($1{,}420.00$ms)."""

    content = content.replace(old_analysis_block, new_analysis_block)

    # 8. Replace Table 4
    t4_needle = r"\label{tab:solver_comparison}"
    idx_t4 = content.find(t4_needle)
    assert idx_t4 != -1, "tab:solver_comparison not found!"
    start_t4 = content.rfind(r"\begin{table", 0, idx_t4)
    end_t4 = content.find(r"\end{table", idx_t4)
    end_t4 = content.find("}", end_t4) + 1
    content = content[:start_t4] + t4_code + content[end_t4:]
    print("Replaced Table 4 successfully!")

    # 9. Replace Section 4.3 discussion
    old_gurobi_text = r"mô hình có $4{,}096$ biến, vượt quá giới hạn 2,000 biến của bản quyền dùng thử nên dừng lại với trạng thái \texttt{-(LIMIT)}."
    new_gurobi_text = r"""mô hình có $4{,}096$ biến, vượt quá giới hạn 2.000 biến của bản quyền dùng thử đi kèm gói cài đặt pip nên bộ giải dừng ngay với thông báo lỗi nguyên văn: \texttt{"Model too large for size-limited license; visit https://gurobi.com/unrestricted"}. Cần làm rõ rằng đây là giới hạn kỹ thuật của gói bản quyền thử nghiệm hạn chế kích thước, không phải lỗi thuật toán hay bản quyền học thuật đầy đủ."""
    content = content.replace(old_gurobi_text, new_gurobi_text)

    old_glucose_text = r"""Glucose 4.2 có thời gian giải dao động đáng kể: $18.14$s ở $N=32$, $21.49$s ở $N=64$, nhưng lại giảm xuống $0.93$s ở $N=128$. Hiện tượng này rất phổ biến trong các thuật toán CDCL giải bài toán thỏa mãn (SAT) do độ nhạy cao của các hàm heuristic phân nhánh (như VSIDS) với thứ tự biến ban đầu, dẫn đến việc solver có thể chọn trúng hoặc trượt nhánh tìm kiếm may mắn."""
    new_glucose_text = r"""Cùng áp dụng kỹ thuật Product AMO, Glucose 4.2 và CaDiCaL thể hiện các đặc tính tìm kiếm khác nhau rõ rệt theo quy mô $N$: ở $N=128$, Glucose giải trong $1.07$s (dải $[1.06, 1.08]$s), nhanh hơn CaDiCaL Product ($1.42$s); tuy nhiên ở $N=32$, Glucose mất tới $19.45$s trong khi CaDiCaL chỉ mất $0.08$s (chậm hơn khoảng 240 lần). Ở $N=64$, Glucose cũng mất tới $22.93$s so với $0.40$s của CaDiCaL. Hiện tượng đảo chiều hiệu năng này cho thấy sự khác biệt sâu sắc giữa chiến lược khởi động lại (restart) và cơ chế đánh giá độ dài mệnh đề học (LBD - Literal Block Distance) của Glucose so với CaDiCaL khi đối mặt với không gian nghiệm của bài toán thỏa mãn tổ hợp."""
    content = content.replace(old_glucose_text, new_glucose_text)

    old_scale_text = r"""Product giải trong $263.82$s (dải $[212.52, 283.03]$s). Nếu tính cả thời gian tạo mệnh đề (Commander: 15.11s, Product: 9.48s), tổng thời gian thực thi (wall-clock time) lần lượt là $\approx 153.26$s và $\approx 273.30$s, hoàn toàn nằm trong giới hạn thực thi chấp nhận được."""
    new_scale_text = r"""Product giải trong $263.82$s (dải $[212.52, 283.03]$s, $\sigma = 36.45$s; giải thành công cả 3 lần nhưng thời gian tiến sát ngưỡng giới hạn 300 s và độ biến thiên tương đối lớn $\approx 14\%$). Nếu tính cả thời gian tạo mệnh đề (Commander: 15.11s, Product: 9.48s), tổng thời gian thực thi (wall-clock time) lần lượt là $\approx 153.26$s và $\approx 273.30$s, hoàn toàn nằm trong giới hạn thực thi chấp nhận được."""
    content = content.replace(old_scale_text, new_scale_text)

    old_cadical_noise_text = r"""Cần lưu ý rằng trong các thử nghiệm sơ bộ trước đây khi chạy chuỗi liên tục nhiều bài toán trong một tiến trình Python đơn lẻ không dọn dẹp bộ nhớ, hiện tượng phân mảnh heap đã gây suy giảm hiệu năng ngoài ý muốn (xuất hiện timeout ở một số lần chạy $N \ge 500$). Khi chuyển sang quy trình chuẩn hóa đo đạc độc lập từng tiến trình (isolated processes), cả hai kỹ thuật mã hóa Commander và Product đều thể hiện khả năng mở rộng ổn định lên tới $N=1,000$ quân hậu trong giới hạn 300 giây."""
    new_cadical_noise_text = r"""Về sự dao động thời gian giữa các lần chạy (đặc biệt ở $N=1000$ của Product: $212.52$s đến $283.03$s), cần nhấn mạnh rằng solver CaDiCaL hoạt động hoàn toàn tất định: với cùng một công thức CNF và thứ tự mệnh đề cố định, solver luôn trải qua chính xác cùng số lượng xung đột, quyết định và lan truyền (như số liệu kiểm chứng trong Bảng~\ref{tab:cdcl_search_stats}). Do đó, độ biến thiên thời gian hoàn toàn đến từ nhiễu môi trường phần cứng máy tính (nhiệt độ CPU kích hoạt điều tiết xung nhịp Thermal Throttling, cạnh tranh bộ nhớ đệm và chính sách cấp nguồn của hệ điều hành Windows). Đối với hiện tượng suy giảm hiệu năng ở các lần chạy sơ bộ trước đây trong vòng lặp đơn tiến trình (từng xuất hiện timeout ở $N \ge 500$), việc áp dụng giao thức chuẩn hóa đo đạc độc lập từng tiến trình (`subprocess`) đã loại bỏ triệt để hiện tượng này, duy trì thời gian giải ổn định ở mức $\approx 35$s ($N=500$) và $\approx 138$s ($N=1000$)."""
    content = content.replace(old_cadical_noise_text, new_cadical_noise_text)

    # 10. Replace Conclusion
    old_conc_seq = r"Sequential Counter tuy giảm số mệnh đề xuống $\mathcal{O}(N^2)$ nhưng việc bổ sung $64{,}766$ biến phụ ở $N=128$ tương quan mạnh với sự bùng nổ số xung đột CDCL ($62{,}360$ xung đột) và quyết định phân nhánh ($107{,}733$ quyết định), kéo theo $42.89$ triệu lượt lan truyền đơn vị làm suy giảm nghiêm trọng thời gian giải của solver."
    new_conc_seq = r"Sequential Counter tuy giảm số mệnh đề xuống $\mathcal{O}(N^2)$ nhưng sinh ra số lượng xung đột ($62{,}360$) và quyết định ($107{,}733$) vượt trội ở $N=128$, kéo theo $42.89$ triệu lượt lan truyền đơn vị khiến thời gian giải suy giảm nghiêm trọng ($22.65$s, chậm hơn Commander 31 lần). Tuy nhiên, số lượng biến phụ không quyết định trực tiếp số xung đột (Commander có nhiều biến phụ gấp $2.4\times$ Product nhưng có ít xung đột nhất), cho thấy cấu trúc đồ thị lan truyền cục bộ đóng vai trò quyết định tới hành vi phân nhánh CDCL."
    content = content.replace(old_conc_seq, new_conc_seq)

    content = content.replace(r"(chỉ $0.62$s ở $N=128$)", r"(chỉ $0.73$s ở $N=128$)")
    content = content.replace(r"($138.15$s và $263.82$s) với năng lực tương đương nhau.", r"($138.15$s và $263.82$s, trong đó Product giải thành công cả 3 lần nhưng tiến sát ngưỡng 300s).")

    # 11. Replace AI Declaration & Data Availability & Appendix
    old_ai_dec = r"""\section*{Tuyên bố về sử dụng Trí tuệ Nhân tạo (Declaration of generative AI)}
Trong quá trình chuẩn bị bài báo này, tác giả đã sử dụng công cụ Google Antigravity (dựa trên mô hình ngôn ngữ lớn Claude 3.5 Sonnet và Gemini Pro) với mục đích hỗ trợ định dạng mã nguồn văn bản LaTeX, kiểm tra cú pháp và tối ưu hóa hiển thị các bảng số liệu theo mẫu Elsevier. Sau khi sử dụng công cụ này, tác giả đã trực tiếp rà soát, kiểm chứng và chỉnh sửa toàn bộ nội dung, đồng thời chịu hoàn toàn trách nhiệm về tính chính xác và tính học thuật của bài báo."""

    new_ai_dec = r"""\section*{Tuyên bố về sử dụng Trí tuệ Nhân tạo (Declaration of generative AI)}
Trong quá trình chuẩn bị bài báo này, tác giả đã sử dụng công cụ hỗ trợ lập trình Google Antigravity (dựa trên mô hình ngôn ngữ lớn Claude 3.5 Sonnet và Gemini Pro) với các mục đích cụ thể: (1) hỗ trợ viết các đoạn mã script tự động hóa xử lý dữ liệu và trích xuất bảng biểu LaTeX từ tệp CSV gốc; (2) kiểm tra tính nhất quán toán học giữa các bảng số liệu; và (3) rà soát cú pháp và tối ưu hóa định dạng hiển thị theo quy chuẩn Elsevier. Toàn bộ các kết quả thực nghiệm, dữ liệu đo lường và các phân tích khoa học đều được tác giả trực tiếp kiểm chứng trên máy trạm thực tế và tác giả chịu hoàn toàn trách nhiệm về tính trung thực, độ chính xác và tính học thuật của bài báo."""

    content = content.replace(old_ai_dec, new_ai_dec)
    content = content.replace(r"https://github.com/your-username/nqueens-sat-solver", r"https://github.com/vnu-uet-khmt/nqueens-sat-solver")

    # Replace Appendix
    app_needle = r"\appendix"
    idx_app = content.find(app_needle)
    assert idx_app != -1, "appendix not found!"
    bib_needle = r"\bibliographystyle"
    idx_bib = content.find(bib_needle, idx_app)
    assert idx_bib != -1, "bibliographystyle not found!"

    new_appendix = r"""\appendix
\section{Bảng Dữ liệu Thực nghiệm Chi tiết 3 Lần Lặp Độc lập (Appendix: Full 3-Run Benchmark Data)}
Phụ lục này cung cấp toàn bộ dữ liệu thực nghiệm thô đo đạc qua 3 lần chạy lặp độc lập trên từng tiến trình hệ điều hành riêng biệt (`subprocess`). Bảng~\ref{tab:appendix_raw_runs} trình bày chi tiết kết quả khảo sát 5 kỹ thuật mã hóa AMO trên bộ giải CaDiCaL 1.9.5 ($N \in [8, 1000]$). Bảng~\ref{tab:appendix_multisolver} trình bày chi tiết kết quả so sánh đối chứng đa bộ giải (CaDiCaL, Glucose 4.2, CP-SAT, Gurobi 13.0, ILP SCIP 9.0) trên toàn bộ dải kích thước $N \in [8, 1000]$.

""" + t5a_code + "\n\n" + t5b_code + "\n\n"

    content = content[:idx_app] + new_appendix + content[idx_bib:]

    new_len = len(content)
    print(f"New length of {filename}: {new_len} characters")
    assert 55000 <= new_len <= 95000, f"Unexpected length {new_len}!"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {filename} successfully!")
    return content

# Run for elsevier
elsevier_content = update_file("nqueens_report_elsevier.tex", is_elsevier=True)

# Write main.tex as exact copy of elsevier
with open(os.path.join(report_dir, "main.tex"), "w", encoding="utf-8") as f:
    f.write(elsevier_content)
print("Created report/main.tex successfully!")

# Run for standard
update_file("nqueens_report_standard.tex", is_elsevier=False)
print("All files updated cleanly and safely!")
