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

def apply_fixes(content):
    # 1. Abstract N=1000 Product phrasing
    old_abs = (
        r"Ở quy mô cực đại $N \ge 256$, Commander và Product mở rộng thành công lên tới $N=500$ ($32.11$s và $32.26$s) và $N=1000$ ($100.92$s và $200.36$s)."
    )
    new_abs = (
        r"Ở quy mô cực đại $N \ge 256$, Commander mở rộng thành công ổn định 3/3 lần lên tới $N=500$ ($32.11$s) và $N=1000$ ($100.92$s); Product đạt 3/3 lần thành công ở $N=500$ ($32.26$s) và đạt tỷ lệ thành công 2/3 lần ở $N=1000$ ($200.36$s; 1 lần chạm giới hạn thời gian 300.0s)."
    )
    content = content.replace(old_abs, new_abs)

    # 2. Contributions N=1000 Product phrasing
    old_contrib = (
        r"Kết quả thực nghiệm cho thấy cả Commander Variable và Product Encoding cho phép CaDiCaL 1.9.5 giải quyết thành công bàn cờ kích thước cực lớn $N = 500$ ($32.11$s và $32.26$s) và $N = 1000$ ($1{,}000{,}000$ ô cờ; $100.92$s và $200.36$s), trong khi CP-SAT và SCIP đều dừng do hết thời gian (timeout) ở $N \ge 256$"
    )
    new_contrib = (
        r"Kết quả thực nghiệm cho thấy CaDiCaL 1.9.5 kết hợp Commander Variable giải quyết thành công 3/3 lần bàn cờ kích thước cực lớn $N = 500$ ($32.11$s) và $N = 1000$ ($1{,}000{,}000$ ô cờ; $100.92$s); kết hợp Product Encoding đạt 3/3 lần thành công ở $N = 500$ ($32.26$s) và đạt tỷ lệ giải thành công 2/3 lần ở $N = 1000$ ($200.36$s; 1 lần chạm trần thời gian 300.0s do chi phí lan truyền trên gần 12 triệu mệnh đề), trong khi CP-SAT và SCIP đều dừng do hết thời gian (timeout) ở $N \ge 256$"
    )
    content = content.replace(old_contrib, new_contrib)

    # 3. Key Takeaways Box N=1000 Product phrasing
    old_box = (
        r"\textbf{Khả năng mở rộng quy mô cực đại ($N \ge 256$):} SAT Solving (CaDiCaL kết hợp Commander Variable và Product Encoding) là hướng tiếp cận duy nhất giải quyết thành công bàn cờ kích thước $N=500$ ($32.11$s) và $N=1000$ ($100.92$s với một triệu ô cờ)."
    )
    new_box = (
        r"\textbf{Khả năng mở rộng quy mô cực đại ($N \ge 256$):} SAT Solving (CaDiCaL) là hướng tiếp cận duy nhất giải quyết được bàn cờ kích thước $N=500$ ($32.11$s với Commander và $32.26$s với Product) và $N=1000$ (Commander giải thành công 3/3 lần với $100.92$s; Product giải thành công 2/3 lần với $200.36$s; 1 lần chạm trần 300.0s)."
    )
    content = content.replace(old_box, new_box)

    # 4. Section 4.1: Unify Gurobi error message and add CaDiCaL version note
    old_gurobi_41 = r"thông báo kích thước vượt hạn mức bản quyền (\texttt{SIZE LIMIT EXCEEDED})"
    new_gurobi_41 = r'thông báo kích thước mô hình vượt hạn mức bản quyền đi kèm: \texttt{"Model too large for size-limited license; visit https://gurobi.com/unrestricted"}'
    content = content.replace(old_gurobi_41, new_gurobi_41)

    cadical_note = (
        r"          \item \textbf{Lưu ý về phiên bản CaDiCaL:} Mặc dù tài liệu hệ thống công bố mới nhất mô tả phiên bản CaDiCaL 2.0~\cite{biere2024cadical}, bản phát hành được tích hợp tĩnh và biên dịch sẵn trong bản phân phối PySAT 1.9.dev15 sử dụng trong nghiên cứu này là CaDiCaL 1.9.5 (thông qua giao tiếp C++ PySAT C-API)." "\n"
    )
    if "Lưu ý về phiên bản CaDiCaL" not in content:
        content = content.replace(
            r"          \item \textbf{Lưu ý về hạn mức bản quyền thương mại (License Limits):}",
            cadical_note + r"          \item \textbf{Lưu ý về hạn mức bản quyền thương mại (License Limits):}"
        )

    # 5. Section 4.2: Neutral academic tone (replace "Điều này bác bỏ giả thiết trước đây...")
    old_tone_42 = (
        r"Điều này bác bỏ giả thiết trước đây cho rằng mỗi bước xung đột của Sequential Counter đòi hỏi khối lượng suy diễn đơn vị đột biến trên danh sách theo dõi mệnh đề (\textit{watchlist})."
    )
    new_tone_42 = (
        r"Số liệu thực nghiệm cho thấy tỷ lệ này không có sự đột biến so với các phương pháp khác, do đó không ủng hộ giả thuyết cho rằng mỗi bước xung đột của Sequential Counter đòi hỏi khối lượng suy diễn đơn vị đột biến trên danh sách theo dõi mệnh đề (\textit{watchlist})."
    )
    content = content.replace(old_tone_42, new_tone_42)

    # 6. Section 4.2: Replace "tuyệt đối" and scope "thời gian giải gắn liền với số xung đột"
    old_abs_42 = (
        r"Đáng chú ý, khi mở rộng đo đạc CDCL vi mô lên các kích thước lớn ($N \ge 256$), solver CaDiCaL tiếp tục duy trì tính nhất quán tuyệt đối về số xung đột và quyết định trên cùng công thức CNF qua cả 3 lần chạy độc lập: ở $N=256$, Commander luôn có đúng $5{,}132$ xung đột, Product có $6{,}607$ xung đột, Pairwise có $6{,}174$ xung đột, trong khi Sequential lên tới $120{,}089$ xung đột; ở $N=500$, Commander có $5{,}096$ xung đột còn Product có $7{,}798$ xung đột; ở $N=1000$, Commander có $943$ xung đột còn Product có $13{,}397$ xung đột."
    )
    new_abs_42 = (
        r"Đáng chú ý, khi mở rộng đo đạc CDCL vi mô lên các kích thước lớn ($N \ge 256$), solver CaDiCaL tiếp tục duy trì tính nhất quán cao về số xung đột và quyết định trên cùng công thức CNF qua các lần giải thành công (3/3 lần trên hầu hết cấu hình và 2/2 lần giải thành công đối với Product tại $N=1000$): ở $N=256$, Commander luôn có đúng $5{,}132$ xung đột, Product có $6{,}607$ xung đột, Pairwise có $6{,}174$ xung đột, trong khi Sequential lên tới $120{,}089$ xung đột; ở $N=500$, Commander có $5{,}096$ xung đột còn Product có $7{,}798$ xung đột; ở $N=1000$, Commander có $943$ xung đột còn Product có $13{,}397$ xung đột (kiểm chứng trên các lần chạy hoàn thành)."
    )
    content = content.replace(old_abs_42, new_abs_42)

    old_conf_rel = (
        r"Kết quả thực nghiệm cho thấy sự bùng nổ thời gian giải của Sequential Counter gắn liền với số lượng xung đột và quyết định tăng đột biến. Tuy nhiên, mối quan hệ giữa số biến phụ và số xung đột không phải là một tương quan tuyến tính đơn giản: Commander Variable có tới $33{,}290$ biến phụ (gấp $2.4$ lần Product và $6.9$ lần Binary) nhưng lại đạt số xung đột thấp nhất ($916$ xung đột), trong khi Pairwise không có bất kỳ biến phụ nào lại có tới $6{,}037$ xung đột (hệ số tương quan hạng Spearman giữa số biến phụ và số xung đột trên 5 kỹ thuật tại $N=128$ chỉ đạt $\approx 0.1$)."
    )
    new_conf_rel = (
        r"Kết quả thực nghiệm ở dải kích thước $N \le 256$ cho thấy sự suy thoái thời gian giải của Sequential Counter gắn liền chặt chẽ với sự bùng nổ số lượng xung đột và quyết định phân nhánh. Tuy nhiên, mối quan hệ giữa số biến phụ và số xung đột không phải là tương quan tuyến tính đơn giản: Commander Variable có tới $33{,}290$ biến phụ (gấp $2.4$ lần Product và $6.9$ lần Binary) nhưng lại đạt số xung đột thấp nhất ($916$ xung đột), trong khi Pairwise không có biến phụ nào lại có tới $6{,}037$ xung đột (hệ số Spearman $\approx 0.1$). Đặc biệt, khi mở rộng lên quy mô cực đại $N=1000$, mối quan hệ này thể hiện thêm tính đa chiều: Commander dù chỉ có $943$ xung đột nhưng đòi hỏi tới $368{,}056$ quyết định và gần $199$ triệu lượt lan truyền đơn vị trên không gian gần 14 triệu mệnh đề, mất $100.92$s; trong khi Product có $13{,}397$ xung đột và $1.66$ triệu quyết định, mất $\approx 200$s. Điều này chứng minh rằng ở quy mô siêu lớn ($N \ge 500$), chi phí duyệt danh sách theo dõi mệnh đề (watchlist) cho các lượt lan truyền đơn vị lũy kế cũng đóng vai trò trọng yếu ngang hàng với số lần học xung đột CDCL."
    )
    content = content.replace(old_conf_rel, new_conf_rel)

    # 7. Section 4.2 & 4.3: Discuss variation across measurement sessions
    old_session_var = (
        r"Về bản chất tìm kiếm, thực nghiệm quan sát thấy solver CaDiCaL vận hành mang tính tất định: trên cùng một công thức CNF và thứ tự mệnh đề cố định, solver luôn ghi nhận chính xác cùng số lượng xung đột và quyết định giữa các lần chạy độc lập (như kiểm chứng trong Bảng~\ref{tab:cdcl_search_stats}). Đối với sự dao động thời gian giữa các lần chạy ở quy mô lớn (đặc biệt ở $N=1000$ khi Product có lần chạm trần 300s), các yếu tố như nhiệt độ CPU kích hoạt điều tiết xung nhịp (Thermal Throttling), cạnh tranh bộ nhớ đệm L3 và cơ chế điều phối tiến trình nền của hệ điều hành Windows được nhìn nhận dưới dạng các giả thuyết thực nghiệm cần được kiểm chứng vi mô sâu hơn."
    )
    new_session_var = (
        r"Về bản chất tìm kiếm, thực nghiệm quan sát thấy solver CaDiCaL vận hành mang tính tất định: trên cùng một công thức CNF và thứ tự mệnh đề cố định, solver luôn ghi nhận chính xác cùng số lượng xung đột và quyết định giữa các lần chạy độc lập (như kiểm chứng trong Bảng~\ref{tab:cdcl_search_stats}). Đối với sự biến thiên thời gian giải tuyệt đối (wall-clock time) giữa các phiên đo khác nhau (ví dụ: Commander ở $N=128$ dao động trong khoảng $0.43\text{s} - 0.76\text{s}$ giữa các phiên đo độc lập phụ thuộc vào trạng thái nhiệt và tải nền của hệ điều hành), các phân tích so sánh tương đối luôn duy trì tính nhất quán cao: tỷ lệ tăng tốc của Commander so với Sequential Counter ở $N=128$ luôn duy trì ổn định từ 31 đến 55 lần trên mọi phiên đo, khẳng định ưu thế cấu trúc vượt trội của cây phân cấp. Ở quy mô cực đại $N=1000$ (khi Product có 1 lần chạm trần 300s và 2 lần giải thành công $\approx 200$s), các yếu tố tải bộ nhớ đệm L3, phân mảnh bộ nhớ và cơ chế điều phối tiến trình nền của hệ điều hành được nhìn nhận dưới dạng các giả thuyết thực nghiệm giải thích độ nhạy của solver. Đặc biệt, để kiểm chứng sâu hơn độ nhạy của Product tại $N=1000$, chúng tôi đã tiến hành thêm một phiên đo độc lập thứ hai có ghi vết tài nguyên phần cứng liên tục qua \texttt{psutil}. Kết quả tái xác nhận tỷ lệ giải thành công đúng 2/3 lần ($235.00$s và $231.65$s, RAM đỉnh $\approx 3{,}833$ MB) với các chỉ số CDCL đồng nhất tuyệt đối ($13{,}397$ xung đột, $1{,}657{,}256$ quyết định và $102.7$ triệu lượt lan truyền); trong khi lượt chạy còn lại chạm trần 300s khi xung nhịp CPU bị điều tiết nhiệt xuống dải 1.98--2.50 GHz (so với xung nhịp cơ sở 3.60 GHz)."
    )
    content = content.replace(old_session_var, new_session_var)

    # 8. Section 4.3: Neutral tone for Gurobi license limit
    old_gurobi_43 = (
        r"Cần làm rõ rằng đây là giới hạn kỹ thuật của gói license hạn chế kích thước đi kèm gói pip, không phải lỗi thuật toán hay license học thuật đầy đủ."
    )
    new_gurobi_43 = (
        r"Cần lưu ý rằng việc dừng lại của Gurobi ở $N \ge 64$ xuất phát từ giới hạn kỹ thuật của gói license hạn chế kích thước (size-limited license) đi kèm bản phân phối pip công khai (tối đa 2.000 biến), thay vì phản ánh giới hạn năng lực giải thuật của phiên bản Gurobi thương mại đầy đủ."
    )
    content = content.replace(old_gurobi_43, new_gurobi_43)

    # 9. Section 5: Conclusion N=1000 Product phrasing
    old_conc_prod = (
        r"\item \textbf{Năng lực mở rộng của Commander và Product:} Commander Variable và Product Encoding là hai kỹ thuật mã hóa có năng lực mở rộng tốt nhất. Commander Variable giúp solver CaDiCaL đạt tốc độ giải nhanh nhất trên dải $N \in [16, 128]$ (chỉ $0.76$s ở $N=128$). Ở quy mô cực đại $N \ge 256$, cả Commander Variable và Product Encoding đều mở rộng thành công lên tới $N=500$ ($32.11$s và $32.26$s) và $N = 1000$ ($100.92$s và $200.36$s, trong đó Product giải thành công 2/3 lần trong giới hạn 300s)."
    )
    new_conc_prod = (
        r"\item \textbf{Năng lực mở rộng của Commander và Product:} Commander Variable và Product Encoding là hai kỹ thuật mã hóa có năng lực mở rộng tốt nhất. Commander Variable giúp solver CaDiCaL đạt tốc độ giải nhanh nhất trên dải $N \in [16, 128]$ (chỉ $0.76$s ở $N=128$), đồng thời duy trì độ ổn định tuyệt đối lên tới $N=500$ ($32.11$s, 3/3 lần) và $N=1000$ ($100.92$s, 3/3 lần thành công trên bàn cờ 1 triệu ô). Product Encoding đạt tốc độ tương đương ở $N=500$ ($32.26$s, 3/3 lần) và đạt tỷ lệ giải thành công 2/3 lần tại $N=1000$ (trung vị $200.36$s; 1 lần chạm giới hạn thời gian 300s do chi phí lan truyền trên 11.95 triệu mệnh đề)."
    )
    content = content.replace(old_conc_prod, new_conc_prod)

    # 10. Data Availability: Remove "gói dự án đính kèm" and update GitHub repository URL
    old_data_avail = (
        r"Toàn bộ mã nguồn cài đặt 5 kỹ thuật mã hóa AMO, các bộ giải SAT (PySAT), CP-SAT, Gurobi, SCIP và dữ liệu thực nghiệm được cung cấp đầy đủ trong gói dự án đính kèm và lưu trữ công khai trên GitHub repository:"
    )
    new_data_avail = (
        r"Toàn bộ mã nguồn cài đặt 5 kỹ thuật mã hóa AMO, các bộ giải SAT (PySAT), CP-SAT, Gurobi, SCIP và toàn bộ dữ liệu thực nghiệm thô được công bố công khai tại kho lưu trữ GitHub chính thức của nhóm nghiên cứu:"
    )
    content = content.replace(old_data_avail, new_data_avail)

    content = content.replace(
        r"\url{https://github.com/vnu-uet-khmt/nqueens-sat-solver}",
        r"\url{https://github.com/Ckipmunk/nqueens-sat-solver}"
    )

    return content

def main():
    for fname in ["nqueens_report_elsevier.tex", "main.tex", "nqueens_report_standard.tex"]:
        path = os.path.join(report_dir, fname)
        if os.path.exists(path):
            content = read_file(path)
            updated = apply_fixes(content)
            write_file(path, updated)
            print(f"Applied critique fixes to {fname}")

if __name__ == "__main__":
    main()
