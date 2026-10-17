import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
report_dir = os.path.join(base_dir, "report")

# Load table files
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

def update_elsevier():
    filepath = os.path.join(report_dir, "nqueens_report_elsevier.tex")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Preamble & Hyperref metadata
    hyp = r"\usepackage{hyperref}" + "\n" + r"\hypersetup{pdfauthor={Phạm Khánh Duy}, pdftitle={Nghiên cứu các Kỹ thuật Mã hóa SAT cho Bài toán N-Queens}}"
    if r"\hypersetup{" in content:
        p_hyp = content.find(r"\hypersetup{")
        p_hyp_end = content.find("}", content.find("pdftitle={", p_hyp)) + 1
        content = content[:p_hyp] + r"\hypersetup{pdfauthor={Phạm Khánh Duy}, pdftitle={Nghiên cứu các Kỹ thuật Mã hóa SAT cho Bài toán N-Queens}}" + content[p_hyp_end:]
    else:
        content = content.replace(r"\usepackage{hyperref}", hyp)

    # 2. Authors and Footnote
    old_author_block = content[content.find(r"\author[1]{"):content.find(r"\begin{abstract}")]
    new_author_block = r"""\author[1]{Phạm Khánh Duy\corref{cor1}}[role=Học viên thực hiện]
\cormark[1]
\ead{24021452@vnu.edu.vn}

\author[1]{TS. Tô Văn Khánh}[role=Giảng viên hướng dẫn]
\ead{khanhtv@vnu.edu.vn}

\address[1]{Khoa Công nghệ Thông tin, Trường Đại học Công nghệ, Đại học Quốc gia Hà Nội (VNU-UET), 144 Xuân Thủy, Cầu Giấy, Hà Nội, Việt Nam}

\cortext[cor1]{Tác giả liên hệ chính: Phạm Khánh Duy (Học viên thực hiện, MSSV: 24021452, Email: \texttt{24021452@vnu.edu.vn}). Giảng viên hướng dẫn: TS. Tô Văn Khánh (Email: \texttt{khanhtv@vnu.edu.vn}).}

"""
    content = content.replace(old_author_block, new_author_block)

    # 3. Abstract
    p_abs_start = content.find(r"\begin{abstract}")
    p_abs_end = content.find(r"\end{abstract}") + len(r"\end{abstract}")
    new_abs_block = r"""\begin{abstract}
Bài toán $N$-Queens là bài toán kinh điển trong khoa học máy tính và tối ưu tổ hợp rời rạc, yêu cầu sắp xếp $N$ quân hậu trên bàn cờ $N \times N$ không tấn công lẫn nhau. Khi kích thước $N$ gia tăng, không gian tìm kiếm bùng nổ theo giai thừa $\mathcal{O}(N!)$, tạo ra thách thức lớn cho các bộ giải chính xác. Bài báo này nghiên cứu tiếp cận giải chính xác $N$-Queens bằng SAT Solving qua thư viện PySAT. Trọng tâm nghiên cứu là phân tích lý thuyết và đánh giá thực nghiệm 5 kỹ thuật mã hóa At-Most-One (AMO): Pairwise, Sequential Counter, Commander Variable, Binary (Prestwich, 2009; Frisch \& Giannaros, 2010) và Product Encoding. Kết quả đo đạc chuẩn hóa qua các tiến trình độc lập (\texttt{subprocess}) cho thấy Pairwise bùng nổ $\mathcal{O}(N^3)$ mệnh đề, tiêu tốn khoảng 7.7 GB RAM đỉnh tại $N=256$ ($7{,}679.4$ MB) và dừng do ngoại lệ \texttt{MemoryError} khi khởi tạo $207.8$ triệu mệnh đề tại $N=500$. Ngược lại, Sequential, Product và Commander duy trì bậc $\mathcal{O}(N^2)$ mệnh đề. Về hiệu năng giải bằng CaDiCaL 1.9.5, Commander Variable đạt tốc độ nhanh nhất trên dải $N \in [16, 128]$ (chỉ mất $0.76$s ở $N=128$, nhanh hơn Sequential khoảng 33 lần). Ở quy mô cực đại $N \ge 256$, Commander và Product mở rộng thành công lên tới $N=500$ ($32.11$s và $32.26$s) và $N=1000$ ($100.92$s và $200.36$s). Thực nghiệm 3 lần chạy lặp độc lập quan sát thấy tính tất định của CaDiCaL với số lượng xung đột và quyết định đồng nhất $100\%$ trên cùng công thức CNF; sự biến thiên thời gian giải ở quy mô lớn được phân tích dưới các giả thuyết về điều tiết xung nhịp phần cứng và quản lý bộ nhớ đệm hệ điều hành. So sánh đối chứng đơn luồng (Time Limit 300.0s) với CP-SAT (Google OR-Tools), Gurobi 13.0 và SCIP 9.0 cho thấy SAT Solving vượt trội về tính mở rộng ở $N \ge 256$, trong khi Gurobi dừng ở $N \ge 64$ do giới hạn kích thước license đi kèm gói pip (tối đa 2.000 biến).
\end{abstract}"""
    content = content[:p_abs_start] + new_abs_block + content[p_abs_end:]

    # 4. Contributions (Section 1)
    p_c_start = content.find(r"\textbf{Đóng góp chính của bài báo:}")
    p_c_end = content.find(r"Cấu trúc các phần tiếp theo")
    new_contrib = r"""\textbf{Đóng góp chính của bài báo:}
\begin{itemize}
    \item Nghiên cứu, cài đặt và phân tích so sánh lý thuyết lẫn thực nghiệm 5 kỹ thuật mã hóa AMO: Pairwise, Sequential Counter~\cite{sinz2005towards}, Commander Variable~\cite{klieber2007efficient}, Binary Encoding~\cite{prestwich2009cnf,frisch2010sat} và Product Encoding~\cite{chen2010product}. Phân định rõ giữa các hàm PySAT CardEnc có sẵn và các thuật toán tự cài đặt độc lập.
    \item Triển khai hoàn chỉnh bộ giải $N$-Queens Solver trên nền tảng PySAT~\cite{ignatiev2018pysat}, tích hợp solver CaDiCaL 1.9.5 và Glucose 4.2.
    \item Thiết lập giao thức đo lường chuẩn hóa: lặp lại đúng 3 lần cho mọi kích thước $N \in [8, 1000]$ trong từng tiến trình con độc lập (\texttt{subprocess}) cách ly bộ nhớ hoàn toàn, đo RAM đỉnh thực tế cho từng lần chạy qua \texttt{psutil}, áp dụng cùng Time Limit 300.0 giây, chạy đơn luồng (1 worker / 1 thread) cho tất cả các solver.
    \item Thu thập dữ liệu thực nghiệm vi mô giải thích động lực tìm kiếm CDCL (\textit{search dynamics}): trích xuất thông số nội tại (\texttt{accum\_stats()}) và tính mã băm SHA-256 của từng công thức CNF qua 3 lần chạy lặp. Kết quả thực nghiệm 3 lần chạy lặp độc lập quan sát thấy tính tất định của CaDiCaL trên cùng một CNF với số lượng xung đột và quyết định hoàn toàn đồng nhất ($3/3$ lần trùng khớp), đồng thời chỉ ra sự suy thoái hiệu năng của Sequential Counter ở $N=128$ ($24.85$s, chậm hơn Commander 33 lần) bị dẫn dắt bởi sự tăng vọt $68\times$ số xung đột ($62{,}360$ so với $916$) và $26\times$ số quyết định ($107{,}733$ so với $4{,}159$), kéo theo $42.89$ triệu lượt lan truyền đơn vị. Phân tích thực nghiệm cũng làm rõ mối quan hệ phi tuyến: số lượng biến phụ không quyết định trực tiếp số xung đột (Commander có $33{,}290$ biến phụ, nhiều hơn $2.4\times$ so với Product, nhưng lại có số xung đột thấp nhất chỉ $916$).
    \item So sánh đối chứng toàn diện giữa SAT Solving với Google OR-Tools CP-SAT, Gurobi Optimizer 13.0 và SCIP 9.0 (ILP MIP) trên dải kích thước bàn cờ từ $N = 8$ đến $N = 1000$.
    \item Kết quả thực nghiệm cho thấy cả Commander Variable và Product Encoding cho phép CaDiCaL 1.9.5 giải quyết thành công bàn cờ kích thước cực lớn $N = 500$ ($32.11$s và $32.26$s) và $N = 1000$ ($1{,}000{,}000$ ô cờ; $100.92$s và $200.36$s), trong khi CP-SAT và SCIP đều dừng do hết thời gian (timeout) ở $N \ge 256$, còn Gurobi dừng ở $N \ge 64$ do giới hạn kích thước license đi kèm gói pip (2.000 biến).
\end{itemize}

"""
    content = content[:p_c_start] + new_contrib + content[p_c_end:]

    # 5. Intro Pairwise N=256 text
    old_p256 = content[content.find(r"phương pháp Pairwise vẫn sinh thành công"):content.find(r"Bảng~\ref{tab:ablation_results}")]
    new_p256 = r"""phương pháp Pairwise vẫn sinh thành công mô hình với 65,536 biến và 27,831,552 mệnh đề (thời gian mã hóa trung vị $14.74$s, thời gian giải trung vị $83.46$s, dải $[81.03, 88.80]$s, tiêu tốn $7{,}679.4$ MB RAM đỉnh).

"""
    content = content[:content.find(r"phương pháp Pairwise vẫn sinh thành công")] + new_p256 + content[content.find(r"Bảng~\ref{tab:ablation_results}"):]

    # 6. Replace Table 2
    idx_t2 = content.find(r"\label{tab:ablation_results}")
    start_t2 = content.rfind(r"\begin{table", 0, idx_t2)
    end_t2 = content.find(r"\end{table", idx_t2)
    end_t2 = content.find("}", end_t2) + 1
    content = content[:start_t2] + t2_code + content[end_t2:]

    # 7. Text after Table 2
    p_t2_post_start = content.find(r"\textbf{Nhận xét và phân tích chuyên sâu về Bảng~\ref{tab:ablation_results}:}")
    p_t2_post_end = content.find(r"\label{tab:cdcl_search_stats}")
    p_t2_post_end = content.rfind(r"\begin{table", 0, p_t2_post_end)
    new_t2_post = r"""\textbf{Nhận xét và phân tích chuyên sâu về Bảng~\ref{tab:ablation_results}:}
\begin{enumerate}
    \item \textbf{Mối quan hệ phi tuyến giữa số lượng mệnh đề và thời gian giải:} Kết quả thực nghiệm cho thấy \textit{số lượng mệnh đề ít hơn không đồng nghĩa với thời gian giải nhanh hơn}. Ở $N=128$, Sequential Counter có số lượng mệnh đề rất thấp ($193{,}800$ clauses), nhưng thời gian giải của CaDiCaL lại lên tới $24.85$ giây, chậm hơn Pairwise ($6.30$ giây với gần 3.5 triệu mệnh đề) và chậm hơn Commander khoảng 33 lần ($0.76$ giây).
    \item \textbf{Phân tích động lực tìm kiếm CDCL (CDCL Search Dynamics):} 
    Để làm sáng tỏ cơ chế nội tại vì sao Sequential Counter có số lượng mệnh đề rất thấp nhưng thời gian giải lại tăng vọt ở $N=128$, chúng tôi đã trích xuất đầy đủ các thông số thống kê vi mô của solver CaDiCaL (\texttt{accum\_stats()}) qua 3 lần chạy độc lập cho cả 5 kỹ thuật mã hóa tại $N \in \{32, 64, 128\}$, được trình bày trong Bảng~\ref{tab:cdcl_search_stats}.

"""
    content = content[:p_t2_post_start] + new_t2_post + content[p_t2_post_end:]

    # 8. Replace Table 3
    idx_t3 = content.find(r"\label{tab:cdcl_search_stats}")
    start_t3 = content.rfind(r"\begin{table", 0, idx_t3)
    end_t3 = content.find(r"\end{table", idx_t3)
    end_t3 = content.find("}", end_t3) + 1
    content = content[:start_t3] + t3_code + content[end_t3:]

    # 9. Text after Table 3
    p_cdcl_start = content.find(r"Dữ liệu đo đạc định lượng cung cấp góc nhìn sâu sắc")
    p_cdcl_end = content.find(r"\subsection{Thực nghiệm 2: So sánh Hiệu năng")
    new_cdcl_post = r"""Dữ liệu đo đạc định lượng cung cấp góc nhìn sâu sắc về tương tác giữa cấu trúc mã hóa và động cơ suy diễn CDCL:
    \begin{itemize}
        \item \textbf{Tỷ lệ lan truyền trên mỗi xung đột ($\text{Props} / \text{Conflict}$):} Tại $N=128$, tỷ lệ này của Sequential Counter đạt $687.8$, trên thực tế thấp hơn so với Commander Variable ($805.9$) và xấp xỉ Product ($618.3$). Điều này bác bỏ giả thiết trước đây cho rằng mỗi bước xung đột của Sequential Counter đòi hỏi khối lượng suy diễn đơn vị đột biến trên danh sách theo dõi mệnh đề (\textit{watchlist}).
        \item \textbf{Tỷ lệ lan truyền trên mỗi quyết định ($\text{Props} / \text{Decision}$):} Sequential Counter đạt $398.1$, cao gấp khoảng $2.2$ lần Commander ($177.5$) và Product ($201.3$). Hệ số $2.2$ lần này phù hợp với giả thuyết về chi phí lan truyền gán giá trị đơn vị dọc theo chuỗi biến tích lũy dạng thang $s_i \to s_{i+1}$.
        \item \textbf{Nguyên nhân thực sự của sự bùng nổ thời gian giải:} Tổng số lượt lan truyền đơn vị của Sequential Counter tăng vọt gấp $58$ lần so với Commander ($42.89 \times 10^6$ so với $738 \times 10^3$) chủ yếu do \textbf{số lượng xung đột tăng gấp $68$ lần ($62{,}360$ so với $916$)} và \textbf{số lượng quyết định phân nhánh tăng gấp $26$ lần ($107{,}733$ so với $4{,}159$)}.
    \end{itemize}
    Kết quả thực nghiệm cho thấy sự bùng nổ thời gian giải của Sequential Counter gắn liền với số lượng xung đột và quyết định tăng đột biến. Tuy nhiên, mối quan hệ giữa số biến phụ và số xung đột không phải là một tương quan tuyến tính đơn giản: Commander Variable có tới $33{,}290$ biến phụ (gấp $2.4$ lần Product và $6.9$ lần Binary) nhưng lại đạt số xung đột thấp nhất ($916$ xung đột), trong khi Pairwise không có bất kỳ biến phụ nào lại có tới $6{,}037$ xung đột (hệ số tương quan hạng Spearman giữa số biến phụ và số xung đột trên 5 kỹ thuật tại $N=128$ chỉ đạt $\approx 0.1$). Đáng chú ý, khi mở rộng đo đạc CDCL vi mô lên các kích thước lớn ($N \ge 256$), solver CaDiCaL tiếp tục duy trì tính nhất quán tuyệt đối về số xung đột và quyết định trên cùng công thức CNF qua cả 3 lần chạy độc lập: ở $N=256$, Commander luôn có đúng $5{,}132$ xung đột, Product có $6{,}607$ xung đột, Pairwise có $6{,}174$ xung đột, trong khi Sequential lên tới $120{,}089$ xung đột; ở $N=500$, Commander có $5{,}096$ xung đột còn Product có $7{,}798$ xung đột; ở $N=1000$, Commander có $943$ xung đột còn Product có $13{,}397$ xung đột. Giả thuyết hợp lý nhất là cấu trúc đồ thị suy diễn đóng vai trò then chốt: cấu trúc cây phân cấp của Commander hỗ trợ cắt tỉa nhanh không gian tìm kiếm, trong khi chuỗi thang tuyến tính $s_i \to s_{i+1}$ của Sequential có thể gây nhiễu loạn heuristic VSIDS và phase-saving, khiến bộ giải liên tục rẽ nhánh sâu vào chuỗi biến trạng thái thay vì các biến bàn cờ cơ sở. Dù vậy, nguyên nhân bản chất của hiện tượng này vẫn là một câu hỏi mở cần được kiểm chứng vi mô sâu hơn.
    \item \textbf{Ưu thế của Commander Variable ở dải $N \in [16, 128]$:} Kỹ thuật Commander phân chia biến thành các nhóm nhỏ ($g=3$) và tổ chức biến chỉ huy dạng cây phân cấp. Cấu trúc này cho phép bộ giải CDCL gán giá trị \texttt{False} cho một nhóm biến ngay khi biến chỉ huy bị gán \texttt{False}, giúp cắt tỉa nhanh không gian tìm kiếm ở các mức quyết định cao với số lượng xung đột cực thấp ($916$ xung đột ở $N=128$). Nhờ đó, Commander đạt thời gian giải nhanh nhất từ $N=16$ ($7.70$ms) đến $N=128$ ($756.90$ms, tức khoảng $0.76$s).
    \item \textbf{Đặc điểm của Binary và Product Encoding:} Binary Encoding sử dụng ít biến phụ nhất trong các phương pháp mở rộng ($21{,}234$ biến ở $N=128$) và có thời gian giải $1{,}415.10$ms, tương đương Product Encoding ($1{,}486.30$ms). Trong khi đó, Product Encoding đạt điểm cân bằng rất tốt giữa số biến phụ ($30{,}182$) và số mệnh đề ($193{,}122$ clauses ở $N=128$, tương đương Sequential với $193{,}800$ clauses), duy trì tốc độ giải ổn định.
    \item \textbf{Thời gian mã hóa và Bộ nhớ ở quy mô lớn:} Với $N \in [8, 128]$, thời gian sinh CNF của các phương pháp đều dưới 2 giây. Tuy nhiên ở các kích thước lớn, chi phí sinh mệnh đề bằng Python tăng đáng kể: ở $N=500$, Commander cần 2.83s mã hóa và $1{,}389.9$ MB RAM đỉnh, Product cần 1.79s và $983.1$ MB RAM; ở $N=1000$, Commander cần 11.38s mã hóa (13.99 triệu mệnh đề, $4{,}410.8$ MB RAM), Product cần 7.57s (11.95 triệu mệnh đề, $3{,}832.5$ MB RAM). Đặc biệt, Pairwise ở $N=256$ đòi hỏi 14.74s mã hóa cho 27.83 triệu mệnh đề và tiêu tốn đỉnh điểm $7{,}679.4$ MB RAM ($\approx 7.50$ GiB), và đến $N=500$ ($207{,}834{,}500$ mệnh đề, xấp xỉ 207.8 triệu) thì dừng do ngoại lệ \texttt{MemoryError} khi tiến trình Python cố gắng khởi tạo cấu trúc danh sách (\texttt{list}) vượt quá không gian bộ nhớ heap khả dụng liên tục của runtime 64-bit trên hệ thống Windows.
\end{enumerate}

"""
    content = content[:p_cdcl_start] + new_cdcl_post + content[p_cdcl_end:]

    # 10. Replace Table 4
    idx_t4 = content.find(r"\label{tab:solver_comparison}")
    start_t4 = content.rfind(r"\begin{table", 0, idx_t4)
    end_t4 = content.find(r"\end{table", idx_t4)
    end_t4 = content.find("}", end_t4) + 1
    content = content[:start_t4] + t4_code + content[end_t4:]

    # 11. Discussion Section 4.3
    p_sec43_start = content.find(r"\textbf{Thảo luận chuyên sâu về hiệu năng so sánh:}")
    p_sec43_end = content.find(r"\section{Kết luận và Thảo luận")
    new_sec43 = r"""\textbf{Thảo luận chuyên sâu về hiệu năng so sánh:}
\begin{enumerate}
    \item \textbf{Hiệu năng của Gurobi và ILP:} Ở các kích thước nhỏ ($N \le 32$), Gurobi 13.0 thể hiện tốc độ ấn tượng ($0.0002$s ở $N=8$ và $0.0254$s ở $N=32$) nhờ các thuật toán tiền xử lý (Presolve) và cắt mặt phẳng (cutting planes) tiên tiến. Tuy nhiên, ở $N \ge 64$, mô hình có $4{,}096$ biến, vượt quá giới hạn 2.000 biến của license dùng thử đi kèm gói cài đặt pip nên bộ giải dừng ngay với thông báo lỗi nguyên văn: \texttt{"Model too large for size-limited license; visit https://gurobi.com/unrestricted"}. Cần làm rõ rằng đây là giới hạn kỹ thuật của gói license hạn chế kích thước đi kèm gói pip, không phải lỗi thuật toán hay license học thuật đầy đủ. Đối với SCIP (bộ giải không giới hạn kích thước), thời gian giải tăng vọt từ $0.0182$s ($N=16$) lên $3.0327$s ($N=32$) và chạm trần $300.0$s ở $N \ge 64$. Điều này phù hợp với lý thuyết tối ưu tổ hợp: mô hình ILP nới lỏng tuyến tính của $N$-Queens cho nghiệm phân số đồng nhất $x_{r,c} = 1/N$, khiến cận dưới trùng nhau tại mọi nút và triệt tiêu sức mạnh cắt tỉa của cây nhánh-cận.
    \item \textbf{Hiệu năng của Google OR-Tools CP-SAT và Hạn chế cấu hình:} CP-SAT đơn luồng (\texttt{num\_workers = 1}, chiến lược tìm kiếm mặc định) hoạt động rất hiệu quả ở dải $N \in [8, 128]$ ($N=128$ giải trong $2.80$s) nhờ các thuật toán lọc miền giá trị dựa trên toán tử \texttt{AllDifferent}. Tuy nhiên, ở $N \ge 256$, bộ giải không thể tìm thấy nghiệm trong giới hạn 300 giây và trả về trạng thái \texttt{UNKNOWN/TIMEOUT}. Cấu hình đơn luồng là bắt buộc nhằm đảm bảo tính so sánh công bằng đối đầu với SAT CaDiCaL (vốn là giải thuật đơn luồng tuần tự); tuy nhiên, cấu hình này cũng hạn chế tiềm năng thực tế của CP-SAT khi không khai thác danh mục thuật toán song song đa luồng (portfolio search) và các bộ sinh nghiệm láng giềng lớn (LNS - Large Neighborhood Search).
    \item \textbf{So sánh hai chiều giữa Glucose 4.2 và CaDiCaL:} Cùng áp dụng kỹ thuật Product AMO, Glucose 4.2 và CaDiCaL thể hiện các đặc tính tìm kiếm khác nhau rõ rệt theo quy mô $N$: ở $N=128$, Glucose giải trong $1.07$s (dải $[1.06, 1.08]$s), nhanh hơn CaDiCaL Product ($1.49$s); tuy nhiên ở $N=32$, Glucose mất tới $19.45$s trong khi CaDiCaL chỉ mất $0.0857$s (chậm hơn khoảng $227$ lần: $19.4494 / 0.0857 \approx 227$). Ở $N=64$, Glucose cũng mất tới $22.93$s so với $0.4211$s của CaDiCaL (chậm hơn khoảng 54 lần). Sự khác biệt hiệu năng này có thể liên quan đến giả thuyết về chiến lược quản lý độ dài mệnh đề học (LBD - Literal Block Distance) và tần suất khởi động lại (restart) giữa hai bộ giải khi cấu trúc đồ thị lan truyền thay đổi theo quy mô $N$.
    \item \textbf{Khả năng mở rộng của SAT CaDiCaL và Bản chất độ biến động thời gian ở quy mô cực đại ($N \ge 256$):} 
    CaDiCaL 1.9.5 với mã hóa Commander và Product thể hiện khả năng mở rộng quy mô vượt trội so với các phương pháp đối chứng:
    \begin{itemize}
        \item Ở $N=64$, CaDiCaL Commander giải trong $0.1870$s (nhanh gấp khoảng $3.0$ lần CP-SAT với $0.5643$s).
        \item Ở $N=256$, Product giải trong $7.99$s (dải $[7.67, 8.05]$s) và Commander giải trong $8.46$s (dải $[8.12, 8.58]$s). Mô hình Pairwise vẫn giải được ở $N=256$ trong $83.46$s nhưng tiêu tốn đỉnh điểm $7{,}679.4$ MB RAM ($\approx 7.50$ GiB).
        \item Ở $N=500$, khi được đo lường trong từng tiến trình độc lập, cả Commander và Product đều giải quyết thành công bàn cờ với thời gian tương đương nhau: Commander đạt trung vị $32.11$s (dải $[31.94, 32.64]$s, $\sigma = 0.37$s), Product đạt trung vị $32.26$s (dải $[31.75, 32.32]$s, $\sigma = 0.31$s). Pairwise ở kích thước này dừng do ngoại lệ \texttt{MemoryError} khi tiến trình Python cố gắng khởi tạo $207{,}834{,}500$ đối tượng mệnh đề trong danh sách liên tục.
        \item Ở kích thước cực đại $N=1000$ ($1{,}000{,}000$ ô cờ), Commander giải thành công cả 3 lần với trung vị $100.92$s (dải $[99.29, 105.40]$s, $\sigma = 3.17$s, RAM đỉnh $4{,}410.8$ MB). Product giải thành công 2 trong 3 lần chạy với thời gian $\approx 199.47$s và $200.36$s (1 lần chạm giới hạn thời gian $300.0$s), RAM đỉnh $3{,}832.5$ MB. Nếu tính cả thời gian tạo mệnh đề (Commander: 11.38s, Product: 7.57s), tổng thời gian thực thi (wall-clock time) lần lượt là $\approx 112.30$s và $\approx 207.93$s.
    \end{itemize}
    Về bản chất tìm kiếm, thực nghiệm khẳng định solver CaDiCaL vận hành mang tính tất định: trên cùng một công thức CNF và thứ tự mệnh đề cố định, solver luôn ghi nhận chính xác cùng số lượng xung đột và quyết định giữa các lần chạy độc lập (như kiểm chứng trong Bảng~\ref{tab:cdcl_search_stats}). Đối với sự dao động thời gian giữa các lần chạy ở quy mô lớn (đặc biệt ở $N=1000$ khi Product có lần chạm trần 300s), các yếu tố như nhiệt độ CPU kích hoạt điều tiết xung nhịp (Thermal Throttling), cạnh tranh bộ nhớ đệm L3 và cơ chế điều phối tiến trình nền của hệ điều hành Windows được nhìn nhận dưới dạng các giả thuyết thực nghiệm cần được kiểm chứng vi mô sâu hơn.
\end{enumerate}

---

"""
    content = content[:p_sec43_start] + new_sec43 + content[p_sec43_end:]

    # 12. Conclusion
    p_conc_start = content.find(r"\section{Kết luận và Thảo luận (Conclusion \& Discussion)}")
    p_conc_end = content.find(r"\textbf{Thảo luận về Hạn chế (Limitations):}")
    new_conc_block = r"""\section{Kết luận và Thảo luận (Conclusion \& Discussion)}
Bài báo đã nghiên cứu, cài đặt và đánh giá toàn diện phương pháp giải chính xác bài toán $N$-Queens bằng SAT Solving trên thư viện PySAT. Thông qua việc phân tích lý thuyết và thực nghiệm 5 kỹ thuật mã hóa AMO, bài báo rút ra các kết luận quan trọng:
\begin{itemize}
    \item Mã hóa Pairwise bùng nổ đa thức bậc ba $\mathcal{O}(N^3)$ mệnh đề trên toàn bàn cờ. Thực nghiệm đo đạc ghi nhận Pairwise tiêu tốn $7{,}679.4$ MB RAM đỉnh tại $N=256$ ($\approx 7.50$ GiB cho $27{,}831{,}552$ mệnh đề, giải trong $83.46$s) và dừng do ngoại lệ \texttt{MemoryError} tại $N=500$ khi khởi tạo $207{,}834{,}500$ mệnh đề trong danh sách đối tượng Python.
    \item Sequential Counter tuy giảm số mệnh đề xuống $\mathcal{O}(N^2)$ nhưng sinh ra số lượng xung đột ($62{,}360$) và quyết định ($107{,}733$) vượt trội ở $N=128$, kéo theo $42.89$ triệu lượt lan truyền đơn vị khiến thời gian giải suy giảm nghiêm trọng ($24.85$s, chậm hơn Commander khoảng 33 lần). Tuy nhiên, số lượng biến phụ không quyết định trực tiếp số xung đột (Commander có nhiều biến phụ gấp $2.4\times$ Product nhưng có ít xung đột nhất), cho thấy cấu trúc đồ thị lan truyền cục bộ đóng vai trò quyết định tới hành vi phân nhánh CDCL.
    \item Commander Variable và Product Encoding là hai kỹ thuật mã hóa có năng lực mở rộng tốt nhất. Commander Variable giúp solver CaDiCaL đạt tốc độ giải nhanh nhất trên dải $N \in [16, 128]$ (chỉ $0.76$s ở $N=128$). Ở quy mô cực đại $N \ge 256$, cả Commander Variable và Product Encoding đều mở rộng thành công lên tới $N=500$ ($32.11$s và $32.26$s) và $N = 1000$ ($100.92$s và $200.36$s, trong đó Product giải thành công 2/3 lần trong giới hạn 300s). Product Encoding đạt quy mô mệnh đề tương đương Sequential ở $N \ge 64$ ($47{,}520$ clauses ở $N=64$ và $193{,}122$ clauses ở $N=128$), trong khi Sequential Counter có ít mệnh đề hơn ở $N \le 32$.
    \item So sánh đối chứng thực nghiệm cho thấy SAT Solving (đặc biệt là CaDiCaL 1.9.5) vượt trội rõ rệt so với SCIP và CP-SAT về khả năng mở rộng ở các kích thước $N \ge 256$. Gurobi thể hiện tốc độ nhanh nhất ở quy mô nhỏ $N \le 32$ nhưng dừng ở $N \ge 64$ do giới hạn kích thước license đi kèm gói pip (2.000 biến).
\end{itemize}

"""
    content = content[:p_conc_start] + new_conc_block + content[p_conc_end:]

    # 13. CRediT
    p_cr_start = content.find(r"\section*{Đóng góp của tác giả")
    p_cr_end = content.find(r"\section*{Tuyên bố về quyền lợi")
    new_credit = r"""\section*{Đóng góp của tác giả (CRediT authorship contribution statement)}
\textbf{Phạm Khánh Duy:} Ý tưởng nghiên cứu (Conceptualization), Phương pháp luận (Methodology), Xây dựng phần mềm và lập trình thực nghiệm (Software, Validation), Phân tích kết quả thực nghiệm (Formal analysis), Viết bản thảo bài báo khoa học và hiệu đính (Writing - original draft, Writing - review \& editing).

\textbf{TS. Tô Văn Khánh:} Định hướng nghiên cứu (Supervision), Góp ý ý tưởng và phản biện học thuật (Conceptualization, Writing - review \& editing).

"""
    content = content[:p_cr_start] + new_credit + content[p_cr_end:]

    # 14. Data availability and Appendix
    p_end_start = content.find(r"\section*{Tuyên bố về sử dụng Trí tuệ Nhân tạo")
    p_end_end = content.find(r"\bibliographystyle")
    new_end = r"""\section*{Tuyên bố về sử dụng Trí tuệ Nhân tạo (Declaration of generative AI)}
Trong quá trình chuẩn bị bài báo này, tác giả đã sử dụng công cụ hỗ trợ lập trình Google Antigravity (dựa trên mô hình ngôn ngữ lớn Claude 3.5 Sonnet và Gemini Pro) với các mục đích cụ thể: (1) hỗ trợ viết các đoạn mã script tự động hóa đo đạc thực nghiệm độc lập và trích xuất bảng biểu LaTeX từ tệp CSV gốc; (2) kiểm tra tính nhất quán toán học giữa các bảng số liệu; và (3) rà soát cú pháp và tối ưu hóa định dạng hiển thị theo quy chuẩn Elsevier. Toàn bộ các kết quả thực nghiệm, dữ liệu đo lường và các phân tích khoa học đều được tác giả trực tiếp kiểm chứng trên máy trạm thực tế và tác giả chịu hoàn toàn trách nhiệm về tính trung thực, độ chính xác và tính học thuật của bài báo.

\section*{Tính khả dụng của dữ liệu và mã nguồn (Data Availability)}
Toàn bộ mã nguồn cài đặt 5 kỹ thuật mã hóa AMO, các bộ giải SAT (PySAT), CP-SAT, Gurobi, SCIP, các script chạy thực nghiệm tự động đo lường độc lập (\texttt{scripts/isolated\_run\_worker.py}, \texttt{scripts/run\_isolated\_master\_benchmark.py}), script tự động sinh bảng biểu LaTeX (\texttt{scripts/generate\_all\_tables\_from\_master.py}), tệp dữ liệu thô chi tiết cả 3 lần chạy (\texttt{data/master\_cadical\_runs.csv}) và nhật ký thực thi đầy đủ (\texttt{data/benchmark\_execution.log}) được cung cấp đầy đủ trong gói dự án đính kèm và lưu trữ công khai trên GitHub repository tại địa chỉ:
\begin{center}
\url{https://github.com/vnu-uet-khmt/nqueens-sat-solver}
\end{center}

\appendix
\section{Bảng Dữ liệu Thực nghiệm Chi tiết 3 Lần Lặp Độc lập (Appendix: Full 3-Run Benchmark Data)}
Phụ lục này cung cấp toàn bộ dữ liệu thực nghiệm thô đo đạc qua 3 lần chạy lặp độc lập trên từng tiến trình hệ điều hành riêng biệt (\texttt{subprocess}). Bảng~\ref{tab:appendix_raw_runs} trình bày chi tiết kết quả khảo sát 5 kỹ thuật mã hóa AMO trên bộ giải CaDiCaL 1.9.5 ($N \in [8, 1000]$). Bảng~\ref{tab:appendix_multisolver} trình bày chi tiết kết quả so sánh đối chứng đa bộ giải (CaDiCaL, Glucose 4.2, CP-SAT, Gurobi 13.0, ILP SCIP 9.0) trên toàn bộ dải kích thước $N \in [8, 1000]$.

""" + t5a_code + "\n\n" + t5b_code + "\n\n"
    content = content[:p_end_start] + new_end + content[p_end_end:]

    # Backticks
    content = content.replace(r"`subprocess`", r"\texttt{subprocess}")
    content = content.replace(r"‘subprocess‘", r"\texttt{subprocess}")
    content = content.replace(r"`accum_stats()`", r"\texttt{accum\_stats()}")

    new_len = len(content)
    print(f"Updated nqueens_report_elsevier.tex: {new_len} characters")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    # Also update main.tex
    main_path = os.path.join(report_dir, "main.tex")
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated nqueens_report_elsevier.tex and main.tex successfully!")

def update_standard():
    filepath = os.path.join(report_dir, "nqueens_report_standard.tex")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Hypersetup
    if r"\hypersetup{" in content:
        p_hyp = content.find(r"\hypersetup{")
        p_hyp_end = content.find("}", content.find("pdftitle={", p_hyp)) + 1
        content = content[:p_hyp] + r"""\hypersetup{
    colorlinks=true,
    linkcolor=blue!80!black,
    citecolor=red!70!black,
    urlcolor=blue!70!black,
    pdfauthor={Phạm Khánh Duy},
    pdftitle={Nghiên cứu các Kỹ thuật Mã hóa SAT cho Bài toán N-Queens}
}""" + content[p_hyp_end:]

    # Authors
    old_authors_std = content[content.find(r"\author{"):content.find(r"\date{")]
    new_authors_std = r"""\author{
    \textbf{Phạm Khánh Duy}$^{1}$ \quad \textbf{TS. Tô Văn Khánh}$^{1,*}$ \\[0.5em]
    $^{1}$Khoa Công nghệ Thông tin, Trường Đại học Công nghệ, ĐHQGHN, Hà Nội, Việt Nam \\
    \texttt{\{24021452, khanhtv\}@vnu.edu.vn}
}

"""
    content = content.replace(old_authors_std, new_authors_std)

    # Abstract
    p_abs_start = content.find(r"\begin{abstract}")
    p_abs_end = content.find(r"\end{abstract}") + len(r"\end{abstract}")
    new_abs_block = r"""\begin{abstract}
Bài toán $N$-Queens là bài toán kinh điển trong khoa học máy tính và tối ưu tổ hợp rời rạc, yêu cầu sắp xếp $N$ quân hậu trên bàn cờ $N \times N$ không tấn công lẫn nhau. Khi kích thước $N$ gia tăng, không gian tìm kiếm bùng nổ theo giai thừa $\mathcal{O}(N!)$, tạo ra thách thức lớn cho các bộ giải chính xác. Bài báo này nghiên cứu tiếp cận giải chính xác $N$-Queens bằng SAT Solving qua thư viện PySAT. Trọng tâm nghiên cứu là phân tích lý thuyết và đánh giá thực nghiệm 5 kỹ thuật mã hóa At-Most-One (AMO): Pairwise, Sequential Counter, Commander Variable, Binary (Prestwich, 2009; Frisch \& Giannaros, 2010) và Product Encoding. Kết quả đo đạc chuẩn hóa qua các tiến trình độc lập (\texttt{subprocess}) cho thấy Pairwise bùng nổ $\mathcal{O}(N^3)$ mệnh đề, tiêu tốn khoảng 7.7 GB RAM đỉnh tại $N=256$ ($7{,}679.4$ MB) và dừng do ngoại lệ \texttt{MemoryError} khi khởi tạo $207.8$ triệu mệnh đề tại $N=500$. Ngược lại, Sequential, Product và Commander duy trì bậc $\mathcal{O}(N^2)$ mệnh đề. Về hiệu năng giải bằng CaDiCaL 1.9.5, Commander Variable đạt tốc độ nhanh nhất trên dải $N \in [16, 128]$ (chỉ mất $0.76$s ở $N=128$, nhanh hơn Sequential khoảng 33 lần). Ở quy mô cực đại $N \ge 256$, Commander và Product mở rộng thành công lên tới $N=500$ ($32.11$s và $32.26$s) và $N=1000$ ($100.92$s và $200.36$s). Thực nghiệm 3 lần chạy lặp độc lập quan sát thấy tính tất định của CaDiCaL với số lượng xung đột và quyết định đồng nhất $100\%$ trên cùng công thức CNF; sự biến thiên thời gian giải ở quy mô lớn được phân tích dưới các giả thuyết về điều tiết xung nhịp phần cứng và quản lý bộ nhớ đệm hệ điều hành. So sánh đối chứng đơn luồng (Time Limit 300.0s) với CP-SAT (Google OR-Tools), Gurobi 13.0 và SCIP 9.0 cho thấy SAT Solving vượt trội về tính mở rộng ở $N \ge 256$, trong khi Gurobi dừng ở $N \ge 64$ do giới hạn kích thước license đi kèm gói pip (tối đa 2.000 biến).
\end{abstract}"""
    content = content[:p_abs_start] + new_abs_block + content[p_abs_end:]

    # Contributions
    p_c_start = content.find(r"\textbf{Đóng góp chính của bài báo:}")
    p_c_end = content.find(r"\section{Cơ sở lý thuyết và Mô hình hóa")
    new_contrib = r"""\textbf{Đóng góp chính của bài báo:}
\begin{itemize}
    \item Nghiên cứu, cài đặt và phân tích so sánh lý thuyết lẫn thực nghiệm 5 kỹ thuật mã hóa AMO: Pairwise, Sequential Counter~\cite{sinz2005towards}, Commander Variable~\cite{klieber2007efficient}, Binary Encoding~\cite{prestwich2009cnf,frisch2010sat} và Product Encoding~\cite{chen2010product}. Phân định rõ giữa các hàm PySAT CardEnc có sẵn và các thuật toán tự cài đặt độc lập.
    \item Triển khai hoàn chỉnh bộ giải $N$-Queens Solver trên nền tảng PySAT~\cite{ignatiev2018pysat}, tích hợp solver CaDiCaL 1.9.5 và Glucose 4.2.
    \item Thiết lập giao thức đo lường chuẩn hóa: lặp lại đúng 3 lần cho mọi kích thước $N \in [8, 1000]$ trong từng tiến trình con độc lập (\texttt{subprocess}) cách ly bộ nhớ hoàn toàn, đo RAM đỉnh thực tế cho từng lần chạy qua \texttt{psutil}, áp dụng cùng Time Limit 300.0 giây, chạy đơn luồng (1 worker / 1 thread) cho tất cả các solver.
    \item Thu thập dữ liệu thực nghiệm vi mô giải thích động lực tìm kiếm CDCL (\textit{search dynamics}): trích xuất thông số nội tại (\texttt{accum\_stats()}) và tính mã băm SHA-256 của từng công thức CNF qua 3 lần chạy lặp. Kết quả thực nghiệm 3 lần chạy lặp độc lập quan sát thấy tính tất định của CaDiCaL trên cùng một CNF với số lượng xung đột và quyết định hoàn toàn đồng nhất ($3/3$ lần trùng khớp), đồng thời chỉ ra sự suy thoái hiệu năng của Sequential Counter ở $N=128$ ($24.85$s, chậm hơn Commander 33 lần) bị dẫn dắt bởi sự tăng vọt $68\times$ số xung đột ($62{,}360$ so với $916$) và $26\times$ số quyết định ($107{,}733$ so với $4{,}159$), kéo theo $42.89$ triệu lượt lan truyền đơn vị. Phân tích thực nghiệm cũng làm rõ mối quan hệ phi tuyến: số lượng biến phụ không quyết định trực tiếp số xung đột (Commander có $33{,}290$ biến phụ, nhiều hơn $2.4\times$ so với Product, nhưng lại có số xung đột thấp nhất chỉ $916$).
    \item So sánh đối chứng toàn diện giữa SAT Solving với Google OR-Tools CP-SAT, Gurobi Optimizer 13.0 và SCIP 9.0 (ILP MIP) trên dải kích thước bàn cờ từ $N = 8$ đến $N = 1000$.
    \item Kết quả thực nghiệm cho thấy cả Commander Variable và Product Encoding cho phép CaDiCaL 1.9.5 giải quyết thành công bàn cờ kích thước cực lớn $N = 500$ ($32.11$s và $32.26$s) và $N = 1000$ ($1{,}000{,}000$ ô cờ; $100.92$s và $200.36$s), trong khi CP-SAT và SCIP đều dừng do hết thời gian (timeout) ở $N \ge 256$, còn Gurobi dừng ở $N \ge 64$ do giới hạn kích thước license đi kèm gói pip (2.000 biến).
\end{itemize}

---

"""
    content = content[:p_c_start] + new_contrib + content[p_c_end:]

    # Replace Table 2
    idx_t2 = content.find(r"\label{tab:ablation_results}")
    start_t2 = content.rfind(r"\begin{table", 0, idx_t2)
    end_t2 = content.find(r"\end{table", idx_t2)
    end_t2 = content.find("}", end_t2) + 1
    content = content[:start_t2] + t2_code + content[end_t2:]

    # Text after Table 2
    p_t2_post_start = content.find(r"\textbf{Nhận xét và phân tích chuyên sâu về Bảng~\ref{tab:ablation_results}:}")
    p_t2_post_end = content.find(r"\label{tab:cdcl_search_stats}")
    p_t2_post_end = content.rfind(r"\begin{table", 0, p_t2_post_end)
    new_t2_post = r"""\textbf{Nhận xét và phân tích chuyên sâu về Bảng~\ref{tab:ablation_results}:}
\begin{enumerate}
    \item \textbf{Mối quan hệ phi tuyến giữa số lượng mệnh đề và thời gian giải:} Kết quả thực nghiệm cho thấy \textit{số lượng mệnh đề ít hơn không đồng nghĩa với thời gian giải nhanh hơn}. Ở $N=128$, Sequential Counter có số lượng mệnh đề rất thấp ($193{,}800$ clauses), nhưng thời gian giải của CaDiCaL lại lên tới $24.85$ giây, chậm hơn Pairwise ($6.30$ giây với gần 3.5 triệu mệnh đề) và chậm hơn Commander khoảng 33 lần ($0.76$ giây).
    \item \textbf{Phân tích động lực tìm kiếm CDCL (CDCL Search Dynamics):} 
    Để làm sáng tỏ cơ chế nội tại vì sao Sequential Counter có số lượng mệnh đề rất thấp nhưng thời gian giải lại tăng vọt ở $N=128$, chúng tôi đã trích xuất đầy đủ các thông số thống kê vi mô của solver CaDiCaL (\texttt{accum\_stats()}) qua 3 lần chạy độc lập cho cả 5 kỹ thuật mã hóa tại $N \in \{32, 64, 128\}$, được trình bày trong Bảng~\ref{tab:cdcl_search_stats}.

"""
    content = content[:p_t2_post_start] + new_t2_post + content[p_t2_post_end:]

    # Replace Table 3
    idx_t3 = content.find(r"\label{tab:cdcl_search_stats}")
    start_t3 = content.rfind(r"\begin{table", 0, idx_t3)
    end_t3 = content.find(r"\end{table", idx_t3)
    end_t3 = content.find("}", end_t3) + 1
    content = content[:start_t3] + t3_code + content[end_t3:]

    # Text after Table 3
    p_cdcl_start = content.find(r"Dữ liệu đo đạc định lượng cung cấp góc nhìn sâu sắc")
    p_cdcl_end = content.find(r"\subsection{Thực nghiệm 2: So sánh Hiệu năng")
    new_cdcl_post = r"""Dữ liệu đo đạc định lượng cung cấp góc nhìn sâu sắc về tương tác giữa cấu trúc mã hóa và động cơ suy diễn CDCL:
    \begin{itemize}
        \item \textbf{Tỷ lệ lan truyền trên mỗi xung đột ($\text{Props} / \text{Conflict}$):} Tại $N=128$, tỷ lệ này của Sequential Counter đạt $687.8$, trên thực tế thấp hơn so với Commander Variable ($805.9$) và xấp xỉ Product ($618.3$). Điều này bác bỏ giả thiết trước đây cho rằng mỗi bước xung đột của Sequential Counter đòi hỏi khối lượng suy diễn đơn vị đột biến trên danh sách theo dõi mệnh đề (\textit{watchlist}).
        \item \textbf{Tỷ lệ lan truyền trên mỗi quyết định ($\text{Props} / \text{Decision}$):} Sequential Counter đạt $398.1$, cao gấp khoảng $2.2$ lần Commander ($177.5$) và Product ($201.3$). Hệ số $2.2$ lần này phù hợp với giả thuyết về chi phí lan truyền gán giá trị đơn vị dọc theo chuỗi biến tích lũy dạng thang $s_i \to s_{i+1}$.
        \item \textbf{Nguyên nhân thực sự của sự bùng nổ thời gian giải:} Tổng số lượt lan truyền đơn vị của Sequential Counter tăng vọt gấp $58$ lần so với Commander ($42.89 \times 10^6$ so với $738 \times 10^3$) chủ yếu do \textbf{số lượng xung đột tăng gấp $68$ lần ($62{,}360$ so với $916$)} và \textbf{số lượng quyết định phân nhánh tăng gấp $26$ lần ($107{,}733$ so với $4{,}159$)}.
    \end{itemize}
    Kết quả thực nghiệm cho thấy sự bùng nổ thời gian giải của Sequential Counter gắn liền với số lượng xung đột và quyết định tăng đột biến. Tuy nhiên, mối quan hệ giữa số biến phụ và số xung đột không phải là một tương quan tuyến tính đơn giản: Commander Variable có tới $33{,}290$ biến phụ (gấp $2.4$ lần Product và $6.9$ lần Binary) nhưng lại đạt số xung đột thấp nhất ($916$ xung đột), trong khi Pairwise không có bất kỳ biến phụ nào lại có tới $6{,}037$ xung đột (hệ số tương quan hạng Spearman giữa số biến phụ và số xung đột trên 5 kỹ thuật tại $N=128$ chỉ đạt $\approx 0.1$). Đáng chú ý, khi mở rộng đo đạc CDCL vi mô lên các kích thước lớn ($N \ge 256$), solver CaDiCaL tiếp tục duy trì tính nhất quán tuyệt đối về số xung đột và quyết định trên cùng công thức CNF qua cả 3 lần chạy độc lập: ở $N=256$, Commander luôn có đúng $5{,}132$ xung đột, Product có $6{,}607$ xung đột, Pairwise có $6{,}174$ xung đột, trong khi Sequential lên tới $120{,}089$ xung đột; ở $N=500$, Commander có $5{,}096$ xung đột còn Product có $7{,}798$ xung đột; ở $N=1000$, Commander có $943$ xung đột còn Product có $13{,}397$ xung đột. Giả thuyết hợp lý nhất là cấu trúc đồ thị suy diễn đóng vai trò then chốt: cấu trúc cây phân cấp của Commander hỗ trợ cắt tỉa nhanh không gian tìm kiếm, trong khi chuỗi thang tuyến tính $s_i \to s_{i+1}$ của Sequential có thể gây nhiễu loạn heuristic VSIDS và phase-saving, khiến bộ giải liên tục rẽ nhánh sâu vào chuỗi biến trạng thái thay vì các biến bàn cờ cơ sở. Dù vậy, nguyên nhân bản chất của hiện tượng này vẫn là một câu hỏi mở cần được kiểm chứng vi mô sâu hơn.
    \item \textbf{Ưu thế của Commander Variable ở dải $N \in [16, 128]$:} Kỹ thuật Commander phân chia biến thành các nhóm nhỏ ($g=3$) và tổ chức biến chỉ huy dạng cây phân cấp. Cấu trúc này cho phép bộ giải CDCL gán giá trị \texttt{False} cho một nhóm biến ngay khi biến chỉ huy bị gán \texttt{False}, giúp cắt tỉa nhanh không gian tìm kiếm ở các mức quyết định cao với số lượng xung đột cực thấp ($916$ xung đột ở $N=128$). Nhờ đó, Commander đạt thời gian giải nhanh nhất từ $N=16$ ($7.70$ms) đến $N=128$ ($756.90$ms, tức khoảng $0.76$s).
    \item \textbf{Đặc điểm của Binary và Product Encoding:} Binary Encoding sử dụng ít biến phụ nhất trong các phương pháp mở rộng ($21{,}234$ biến ở $N=128$) và có thời gian giải $1{,}415.10$ms, tương đương Product Encoding ($1{,}486.30$ms). Trong khi đó, Product Encoding đạt điểm cân bằng rất tốt giữa số biến phụ ($30{,}182$) và số mệnh đề ($193{,}122$ clauses ở $N=128$, tương đương Sequential với $193{,}800$ clauses), duy trì tốc độ giải ổn định.
    \item \textbf{Thời gian mã hóa và Bộ nhớ ở quy mô lớn:} Với $N \in [8, 128]$, thời gian sinh CNF của các phương pháp đều dưới 2 giây. Tuy nhiên ở các kích thước lớn, chi phí sinh mệnh đề bằng Python tăng đáng kể: ở $N=500$, Commander cần 2.83s mã hóa và $1{,}389.9$ MB RAM đỉnh, Product cần 1.79s và $983.1$ MB RAM; ở $N=1000$, Commander cần 11.38s mã hóa (13.99 triệu mệnh đề, $4{,}410.8$ MB RAM), Product cần 7.57s (11.95 triệu mệnh đề, $3{,}832.5$ MB RAM). Đặc biệt, Pairwise ở $N=256$ đòi hỏi 14.74s mã hóa cho 27.83 triệu mệnh đề và tiêu tốn đỉnh điểm $7{,}679.4$ MB RAM ($\approx 7.50$ GiB), và đến $N=500$ ($207{,}834{,}500$ mệnh đề, xấp xỉ 207.8 triệu) thì dừng do ngoại lệ \texttt{MemoryError} khi tiến trình Python cố gắng khởi tạo cấu trúc danh sách (\texttt{list}) vượt quá không gian bộ nhớ heap khả dụng liên tục của runtime 64-bit trên hệ thống Windows.
\end{enumerate}

"""
    content = content[:p_cdcl_start] + new_cdcl_post + content[p_cdcl_end:]

    # Replace Table 4
    idx_t4 = content.find(r"\label{tab:solver_comparison}")
    start_t4 = content.rfind(r"\begin{table", 0, idx_t4)
    end_t4 = content.find(r"\end{table", idx_t4)
    end_t4 = content.find("}", end_t4) + 1
    content = content[:start_t4] + t4_code + content[end_t4:]

    # Discussion Section 4.3
    p_sec43_start = content.find(r"\textbf{Thảo luận chuyên sâu về hiệu năng so sánh:}")
    p_sec43_end = content.find(r"\section{Kết luận và Thảo luận")
    new_sec43 = r"""\textbf{Thảo luận chuyên sâu về hiệu năng so sánh:}
\begin{enumerate}
    \item \textbf{Hiệu năng của Gurobi và ILP:} Ở các kích thước nhỏ ($N \le 32$), Gurobi 13.0 thể hiện tốc độ ấn tượng ($0.0002$s ở $N=8$ và $0.0254$s ở $N=32$) nhờ các thuật toán tiền xử lý (Presolve) và cắt mặt phẳng (cutting planes) tiên tiến. Tuy nhiên, ở $N \ge 64$, mô hình có $4{,}096$ biến, vượt quá giới hạn 2.000 biến của license dùng thử đi kèm gói cài đặt pip nên bộ giải dừng ngay với thông báo lỗi nguyên văn: \texttt{"Model too large for size-limited license; visit https://gurobi.com/unrestricted"}. Cần làm rõ rằng đây là giới hạn kỹ thuật của gói license hạn chế kích thước đi kèm gói pip, không phải lỗi thuật toán hay license học thuật đầy đủ. Đối với SCIP (bộ giải không giới hạn kích thước), thời gian giải tăng vọt từ $0.0182$s ($N=16$) lên $3.0327$s ($N=32$) và chạm trần $300.0$s ở $N \ge 64$. Điều này phù hợp với lý thuyết tối ưu tổ hợp: mô hình ILP nới lỏng tuyến tính của $N$-Queens cho nghiệm phân số đồng nhất $x_{r,c} = 1/N$, khiến cận dưới trùng nhau tại mọi nút và triệt tiêu sức mạnh cắt tỉa của cây nhánh-cận.
    \item \textbf{Hiệu năng của Google OR-Tools CP-SAT và Hạn chế cấu hình:} CP-SAT đơn luồng (\texttt{num\_workers = 1}, chiến lược tìm kiếm mặc định) hoạt động rất hiệu quả ở dải $N \in [8, 128]$ ($N=128$ giải trong $2.80$s) nhờ các thuật toán lọc miền giá trị dựa trên toán tử \texttt{AllDifferent}. Tuy nhiên, ở $N \ge 256$, bộ giải không thể tìm thấy nghiệm trong giới hạn 300 giây và trả về trạng thái \texttt{UNKNOWN/TIMEOUT}. Cấu hình đơn luồng là bắt buộc nhằm đảm bảo tính so sánh công bằng đối đầu với SAT CaDiCaL (vốn là giải thuật đơn luồng tuần tự); tuy nhiên, cấu hình này cũng hạn chế tiềm năng thực tế của CP-SAT khi không khai thác danh mục thuật toán song song đa luồng (portfolio search) và các bộ sinh nghiệm láng giềng lớn (LNS - Large Neighborhood Search).
    \item \textbf{So sánh hai chiều giữa Glucose 4.2 và CaDiCaL:} Cùng áp dụng kỹ thuật Product AMO, Glucose 4.2 và CaDiCaL thể hiện các đặc tính tìm kiếm khác nhau rõ rệt theo quy mô $N$: ở $N=128$, Glucose giải trong $1.07$s (dải $[1.06, 1.08]$s), nhanh hơn CaDiCaL Product ($1.49$s); tuy nhiên ở $N=32$, Glucose mất tới $19.45$s trong khi CaDiCaL chỉ mất $0.0857$s (chậm hơn khoảng $227$ lần: $19.4494 / 0.0857 \approx 227$). Ở $N=64$, Glucose cũng mất tới $22.93$s so với $0.4211$s của CaDiCaL (chậm hơn khoảng 54 lần). Sự khác biệt hiệu năng này có thể liên quan đến giả thuyết về chiến lược quản lý độ dài mệnh đề học (LBD - Literal Block Distance) và tần suất khởi động lại (restart) giữa hai bộ giải khi cấu trúc đồ thị lan truyền thay đổi theo quy mô $N$.
    \item \textbf{Khả năng mở rộng của SAT CaDiCaL và Bản chất độ biến động thời gian ở quy mô cực đại ($N \ge 256$):} 
    CaDiCaL 1.9.5 với mã hóa Commander và Product thể hiện khả năng mở rộng quy mô vượt trội so với các phương pháp đối chứng:
    \begin{itemize}
        \item Ở $N=64$, CaDiCaL Commander giải trong $0.1870$s (nhanh gấp khoảng $3.0$ lần CP-SAT với $0.5643$s).
        \item Ở $N=256$, Product giải trong $7.99$s (dải $[7.67, 8.05]$s) và Commander giải trong $8.46$s (dải $[8.12, 8.58]$s). Mô hình Pairwise vẫn giải được ở $N=256$ trong $83.46$s nhưng tiêu tốn đỉnh điểm $7{,}679.4$ MB RAM ($\approx 7.50$ GiB).
        \item Ở $N=500$, khi được đo lường trong từng tiến trình độc lập, cả Commander và Product đều giải quyết thành công bàn cờ với thời gian tương đương nhau: Commander đạt trung vị $32.11$s (dải $[31.94, 32.64]$s, $\sigma = 0.37$s), Product đạt trung vị $32.26$s (dải $[31.75, 32.32]$s, $\sigma = 0.31$s). Pairwise ở kích thước này dừng do ngoại lệ \texttt{MemoryError} khi tiến trình Python cố gắng khởi tạo $207{,}834{,}500$ đối tượng mệnh đề trong danh sách liên tục.
        \item Ở kích thước cực đại $N=1000$ ($1{,}000{,}000$ ô cờ), Commander giải thành công cả 3 lần với trung vị $100.92$s (dải $[99.29, 105.40]$s, $\sigma = 3.17$s, RAM đỉnh $4{,}410.8$ MB). Product giải thành công 2 trong 3 lần chạy với thời gian $\approx 199.47$s và $200.36$s (1 lần chạm giới hạn thời gian $300.0$s), RAM đỉnh $3{,}832.5$ MB. Nếu tính cả thời gian tạo mệnh đề (Commander: 11.38s, Product: 7.57s), tổng thời gian thực thi (wall-clock time) lần lượt là $\approx 112.30$s và $\approx 207.93$s.
    \end{itemize}
    Về bản chất tìm kiếm, thực nghiệm khẳng định solver CaDiCaL vận hành mang tính tất định: trên cùng một công thức CNF và thứ tự mệnh đề cố định, solver luôn ghi nhận chính xác cùng số lượng xung đột và quyết định giữa các lần chạy độc lập (như kiểm chứng trong Bảng~\ref{tab:cdcl_search_stats}). Đối với sự dao động thời gian giữa các lần chạy ở quy mô lớn (đặc biệt ở $N=1000$ khi Product có lần chạm trần 300s), các yếu tố như nhiệt độ CPU kích hoạt điều tiết xung nhịp (Thermal Throttling), cạnh tranh bộ nhớ đệm L3 và cơ chế điều phối tiến trình nền của hệ điều hành Windows được nhìn nhận dưới dạng các giả thuyết thực nghiệm cần được kiểm chứng vi mô sâu hơn.
\end{enumerate}

---

"""
    content = content[:p_sec43_start] + new_sec43 + content[p_sec43_end:]

    # Conclusion
    p_conc_start = content.find(r"\section{Kết luận và Thảo luận (Conclusion \& Discussion)}")
    p_conc_end = content.find(r"\textbf{Thảo luận về Hạn chế (Limitations):}")
    new_conc_block = r"""\section{Kết luận và Thảo luận (Conclusion \& Discussion)}
Bài báo đã nghiên cứu, cài đặt và đánh giá toàn diện phương pháp giải chính xác bài toán $N$-Queens bằng SAT Solving trên thư viện PySAT. Thông qua việc phân tích lý thuyết và thực nghiệm 5 kỹ thuật mã hóa AMO, bài báo rút ra các kết luận quan trọng:
\begin{itemize}
    \item Mã hóa Pairwise bùng nổ đa thức bậc ba $\mathcal{O}(N^3)$ mệnh đề trên toàn bàn cờ. Thực nghiệm đo đạc ghi nhận Pairwise tiêu tốn $7{,}679.4$ MB RAM đỉnh tại $N=256$ ($\approx 7.50$ GiB cho $27{,}831{,}552$ mệnh đề, giải trong $83.46$s) và dừng do ngoại lệ \texttt{MemoryError} tại $N=500$ khi khởi tạo $207{,}834{,}500$ mệnh đề trong danh sách đối tượng Python.
    \item Sequential Counter tuy giảm số mệnh đề xuống $\mathcal{O}(N^2)$ nhưng sinh ra số lượng xung đột ($62{,}360$) và quyết định ($107{,}733$) vượt trội ở $N=128$, kéo theo $42.89$ triệu lượt lan truyền đơn vị khiến thời gian giải suy giảm nghiêm trọng ($24.85$s, chậm hơn Commander khoảng 33 lần). Tuy nhiên, số lượng biến phụ không quyết định trực tiếp số xung đột (Commander có nhiều biến phụ gấp $2.4\times$ Product nhưng có ít xung đột nhất), cho thấy cấu trúc đồ thị lan truyền cục bộ đóng vai trò quyết định tới hành vi phân nhánh CDCL.
    \item Commander Variable và Product Encoding là hai kỹ thuật mã hóa có năng lực mở rộng tốt nhất. Commander Variable giúp solver CaDiCaL đạt tốc độ giải nhanh nhất trên dải $N \in [16, 128]$ (chỉ $0.76$s ở $N=128$). Ở quy mô cực đại $N \ge 256$, cả Commander Variable và Product Encoding đều mở rộng thành công lên tới $N=500$ ($32.11$s và $32.26$s) và $N = 1000$ ($100.92$s và $200.36$s, trong đó Product giải thành công 2/3 lần trong giới hạn 300s). Product Encoding đạt quy mô mệnh đề tương đương Sequential ở $N \ge 64$ ($47{,}520$ clauses ở $N=64$ và $193{,}122$ clauses ở $N=128$), trong khi Sequential Counter có ít mệnh đề hơn ở $N \le 32$.
    \item So sánh đối chứng thực nghiệm cho thấy SAT Solving (đặc biệt là CaDiCaL 1.9.5) vượt trội rõ rệt so với SCIP và CP-SAT về khả năng mở rộng ở các kích thước $N \ge 256$. Gurobi thể hiện tốc độ nhanh nhất ở quy mô nhỏ $N \le 32$ nhưng dừng ở $N \ge 64$ do giới hạn kích thước license đi kèm gói pip (2.000 biến).
\end{itemize}

"""
    content = content[:p_conc_start] + new_conc_block + content[p_conc_end:]

    # CRediT
    p_cr_start = content.find(r"\section*{Đóng góp của tác giả")
    p_cr_end = content.find(r"\section*{Tuyên bố về quyền lợi")
    new_credit = r"""\section*{Đóng góp của tác giả (CRediT authorship contribution statement)}
\textbf{Phạm Khánh Duy:} Ý tưởng nghiên cứu (Conceptualization), Phương pháp luận (Methodology), Xây dựng phần mềm và lập trình thực nghiệm (Software, Validation), Phân tích kết quả thực nghiệm (Formal analysis), Viết bản thảo bài báo khoa học và hiệu đính (Writing - original draft, Writing - review \& editing).

\textbf{TS. Tô Văn Khánh:} Định hướng nghiên cứu (Supervision), Góp ý ý tưởng và phản biện học thuật (Conceptualization, Writing - review \& editing).

"""
    content = content[:p_cr_start] + new_credit + content[p_cr_end:]

    # Ending
    p_end_start = content.find(r"\section*{Tuyên bố về sử dụng Trí tuệ Nhân tạo")
    p_end_end = content.find(r"\bibliographystyle")
    new_end = r"""\section*{Tuyên bố về sử dụng Trí tuệ Nhân tạo (Declaration of generative AI)}
Trong quá trình chuẩn bị bài báo này, tác giả đã sử dụng công cụ hỗ trợ lập trình Google Antigravity (dựa trên mô hình ngôn ngữ lớn Claude 3.5 Sonnet và Gemini Pro) với các mục đích cụ thể: (1) hỗ trợ viết các đoạn mã script tự động hóa đo đạc thực nghiệm độc lập và trích xuất bảng biểu LaTeX từ tệp CSV gốc; (2) kiểm tra tính nhất quán toán học giữa các bảng số liệu; và (3) rà soát cú pháp và tối ưu hóa định dạng hiển thị theo quy chuẩn Elsevier. Toàn bộ các kết quả thực nghiệm, dữ liệu đo lường và các phân tích khoa học đều được tác giả trực tiếp kiểm chứng trên máy trạm thực tế và tác giả chịu hoàn toàn trách nhiệm về tính trung thực, độ chính xác và tính học thuật của bài báo.

\section*{Tính khả dụng của dữ liệu và mã nguồn (Data Availability)}
Toàn bộ mã nguồn cài đặt 5 kỹ thuật mã hóa AMO, các bộ giải SAT (PySAT), CP-SAT, Gurobi, SCIP, các script chạy thực nghiệm tự động đo lường độc lập (\texttt{scripts/isolated\_run\_worker.py}, \texttt{scripts/run\_isolated\_master\_benchmark.py}), script tự động sinh bảng biểu LaTeX (\texttt{scripts/generate\_all\_tables\_from\_master.py}), tệp dữ liệu thô chi tiết cả 3 lần chạy (\texttt{data/master\_cadical\_runs.csv}) và nhật ký thực thi đầy đủ (\texttt{data/benchmark\_execution.log}) được cung cấp đầy đủ trong gói dự án đính kèm và lưu trữ công khai trên GitHub repository tại địa chỉ:
\begin{center}
\url{https://github.com/vnu-uet-khmt/nqueens-sat-solver}
\end{center}

\appendix
\section{Bảng Dữ liệu Thực nghiệm Chi tiết 3 Lần Lặp Độc lập (Appendix: Full 3-Run Benchmark Data)}
Phụ lục này cung cấp toàn bộ dữ liệu thực nghiệm thô đo đạc qua 3 lần chạy lặp độc lập trên từng tiến trình hệ điều hành riêng biệt (\texttt{subprocess}). Bảng~\ref{tab:appendix_raw_runs} trình bày chi tiết kết quả khảo sát 5 kỹ thuật mã hóa AMO trên bộ giải CaDiCaL 1.9.5 ($N \in [8, 1000]$). Bảng~\ref{tab:appendix_multisolver} trình bày chi tiết kết quả so sánh đối chứng đa bộ giải (CaDiCaL, Glucose 4.2, CP-SAT, Gurobi 13.0, ILP SCIP 9.0) trên toàn bộ dải kích thước $N \in [8, 1000]$.

""" + t5a_code + "\n\n" + t5b_code + "\n\n"
    content = content[:p_end_start] + new_end + content[p_end_end:]

    # Backticks
    content = content.replace(r"`subprocess`", r"\texttt{subprocess}")
    content = content.replace(r"‘subprocess‘", r"\texttt{subprocess}")
    content = content.replace(r"`accum_stats()`", r"\texttt{accum\_stats()}")

    new_len = len(content)
    print(f"Updated nqueens_report_standard.tex: {new_len} characters")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated nqueens_report_standard.tex successfully!")

if __name__ == "__main__":
    update_elsevier()
    update_standard()
    print("ALL TEX FILES UPDATED TO DRAFT 9 SUCCESSFULLY!")
