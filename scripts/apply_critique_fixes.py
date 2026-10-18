import os

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
    old_abs_list = [
        r"Ở quy mô cực đại $N \ge 256$, Commander và Product mở rộng thành công lên tới $N=500$ ($32.11$s và $32.26$s) và $N=1000$ ($100.92$s và $200.36$s).",
        r"Ở quy mô cực đại $N \ge 256$, Commander mở rộng thành công ổn định 3/3 lần lên tới $N=500$ ($32.11$s) và $N=1000$ ($100.92$s); Product đạt 3/3 lần thành công ở $N=500$ ($32.26$s) và đạt tỷ lệ thành công 2/3 lần ở $N=1000$ ($200.36$s; 1 lần chạm giới hạn thời gian 300.0s)."
    ]
    new_abs = (
        r"Ở quy mô cực đại $N \ge 256$, Commander mở rộng thành công ổn định 3/3 lần lên tới $N=500$ ($32.11$s) và $N=1000$ ($100.92$s); Product đạt 3/3 lần thành công ở $N=500$ ($32.26$s) và đạt tỷ lệ thành công 2/3 lần ở $N=1000$ (trung vị $200.36$s; 1 lần chạm giới hạn thời gian 300.0s với nguyên nhân chưa xác định chắc chắn)."
    )
    for old_s in old_abs_list:
        content = content.replace(old_s, new_abs)

    # 2. Contributions N=1000 Product phrasing (Draft 10: remove "do chi phí lan truyền...")
    old_contrib_list = [
        r"Kết quả thực nghiệm cho thấy cả Commander Variable và Product Encoding cho phép CaDiCaL 1.9.5 giải quyết thành công bàn cờ kích thước cực lớn $N = 500$ ($32.11$s và $32.26$s) và $N = 1000$ ($1{,}000{,}000$ ô cờ; $100.92$s và $200.36$s), trong khi CP-SAT và SCIP đều dừng do hết thời gian (timeout) ở $N \ge 256$",
        r"Kết quả thực nghiệm cho thấy CaDiCaL 1.9.5 kết hợp Commander Variable giải quyết thành công 3/3 lần bàn cờ kích thước cực lớn $N = 500$ ($32.11$s) và $N = 1000$ ($1{,}000{,}000$ ô cờ; $100.92$s); kết hợp Product Encoding đạt 3/3 lần thành công ở $N = 500$ ($32.26$s) và đạt tỷ lệ giải thành công 2/3 lần ở $N = 1000$ ($200.36$s; 1 lần chạm trần thời gian 300.0s do chi phí lan truyền trên gần 12 triệu mệnh đề), trong khi CP-SAT và SCIP đều dừng do hết thời gian (timeout) ở $N \ge 256$",
        r"Kết quả thực nghiệm cho thấy CaDiCaL 1.9.5 kết hợp Commander Variable giải quyết thành công 3/3 lần bàn cờ kích thước cực lớn $N = 500$ ($32.11$s) và $N = 1000$ ($1{,}000{,}000$ ô cờ; $100.92$s); kết hợp Product Encoding đạt 3/3 lần thành công ở $N = 500$ ($32.26$s) và đạt tỷ lệ giải thành công 2/3 lần ở $N = 1000$ (trung vị $200.36$s; 1 lần chạm trần thời gian 300.0s với nguyên nhân chưa được xác định chắc chắn), trong khi CP-SAT và SCIP đều dừng do hết thời gian (timeout) ở $N \ge 256$"
    ]
    new_contrib = (
        r"Kết quả thực nghiệm cho thấy CaDiCaL 1.9.5 kết hợp Commander Variable giải quyết thành công 3/3 lần bàn cờ kích thước cực lớn $N = 500$ ($32.11$s) và $N = 1000$ ($1{,}000{,}000$ ô cờ; $100.92$s); kết hợp Product Encoding đạt 3/3 lần thành công ở $N = 500$ ($32.26$s) và đạt tỷ lệ giải thành công 2/3 lần ở $N = 1000$ (trung vị $200.36$s; 1 lần chạm trần thời gian 300.0s với nguyên nhân chưa được xác định chắc chắn), trong khi CP-SAT và SCIP đều dừng do hết thời gian (timeout) ở $N \ge 256$"
    )
    for old_s in old_contrib_list:
        content = content.replace(old_s, new_contrib)

    # 3. Key Takeaways Box N=1000 Product phrasing
    old_box_list = [
        r"\textbf{Khả năng mở rộng quy mô cực đại ($N \ge 256$):} SAT Solving (CaDiCaL kết hợp Commander Variable và Product Encoding) là hướng tiếp cận duy nhất giải quyết thành công bàn cờ kích thước $N=500$ ($32.11$s) và $N=1000$ ($100.92$s với một triệu ô cờ).",
        r"\textbf{Khả năng mở rộng quy mô cực đại ($N \ge 256$):} SAT Solving (CaDiCaL) là hướng tiếp cận duy nhất giải quyết được bàn cờ kích thước $N=500$ ($32.11$s với Commander và $32.26$s với Product) và $N=1000$ (Commander giải thành công 3/3 lần với $100.92$s; Product giải thành công 2/3 lần với $200.36$s; 1 lần chạm trần 300.0s)."
    ]
    new_box = (
        r"\textbf{Khả năng mở rộng quy mô cực đại ($N \ge 256$):} SAT Solving (CaDiCaL) là hướng tiếp cận duy nhất giải quyết được bàn cờ kích thước $N=500$ ($32.11$s với Commander và $32.26$s với Product) và $N=1000$ (Commander giải thành công 3/3 lần với $100.92$s; Product giải thành công 2/3 lần với trung vị $200.36$s; 1 lần chạm trần 300.0s với nguyên nhân chưa xác định chắc chắn)."
    )
    for old_s in old_box_list:
        content = content.replace(old_s, new_box)

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

    # 5. Section 4.2: Neutral academic tone
    old_tone_42 = (
        r"Điều này bác bỏ giả thiết trước đây cho rằng mỗi bước xung đột của Sequential Counter đòi hỏi khối lượng suy diễn đơn vị đột biến trên danh sách theo dõi mệnh đề (\textit{watchlist})."
    )
    new_tone_42 = (
        r"Số liệu thực nghiệm cho thấy tỷ lệ này không có sự đột biến so với các phương pháp khác, do đó không ủng hộ giả thuyết cho rằng mỗi bước xung đột của Sequential Counter đòi hỏi khối lượng suy diễn đơn vị đột biến trên danh sách theo dõi mệnh đề (\textit{watchlist})."
    )
    content = content.replace(old_tone_42, new_tone_42)

    # 6. Section 4.2: CDCL conflicts explanation (Draft 10: remove watchlist "chứng minh", "ngang hàng")
    old_target_conf = (
        r"Điều này chứng minh rằng ở quy mô siêu lớn ($N \ge 500$), chi phí duyệt danh sách theo dõi mệnh đề (watchlist) cho các lượt lan truyền đơn vị lũy kế cũng đóng vai trò trọng yếu ngang hàng với số lần học xung đột CDCL."
    )
    new_target_conf = (
        r"Quan sát này cho thấy ở quy mô cực đại, số lượng xung đột CDCL đơn thuần không còn đủ để giải thích toàn bộ thời gian thực thi của solver; các yếu tố khác như cấu trúc phân nhánh cây, chiều sâu quay lui và cơ chế quản lý bộ nhớ đệm mệnh đề học cũng đóng vai trò đáng kể."
    )
    content = content.replace(old_target_conf, new_target_conf)

    # 7. Section 4.2 & 4.3: Session variations (Draft 10: "có thể do", reference CSV files in repo, tone down relative speedup)
    old_session_var_list = [
        r"Đối với sự biến thiên thời gian giải tuyệt đối (wall-clock time) giữa các phiên đo khác nhau (ví dụ: Commander ở $N=128$ dao động trong khoảng $0.43\text{s} - 0.76\text{s}$ giữa các phiên đo độc lập phụ thuộc vào trạng thái nhiệt và tải nền của hệ điều hành), các phân tích so sánh tương đối luôn duy trì tính nhất quán cao: tỷ lệ tăng tốc của Commander so với Sequential Counter ở $N=128$ luôn duy trì ổn định từ 31 đến 55 lần trên mọi phiên đo, khẳng định ưu thế cấu trúc vượt trội của cây phân cấp. Ở quy mô cực đại $N=1000$ (khi Product có 1 lần chạm trần 300s và 2 lần giải thành công $\approx 200$s), các yếu tố tải bộ nhớ đệm L3, phân mảnh bộ nhớ và cơ chế điều phối tiến trình nền của hệ điều hành được nhìn nhận dưới dạng các giả thuyết thực nghiệm giải thích độ nhạy của solver. Đặc biệt, để kiểm chứng sâu hơn độ nhạy của Product tại $N=1000$, chúng tôi đã tiến hành thêm một phiên đo độc lập thứ hai có ghi vết tài nguyên phần cứng liên tục qua \texttt{psutil}. Kết quả tái xác nhận tỷ lệ giải thành công đúng 2/3 lần ($235.00$s và $231.65$s, RAM đỉnh $\approx 3{,}833$ MB) với các chỉ số CDCL đồng nhất tuyệt đối ($13{,}397$ xung đột, $1{,}657{,}256$ quyết định và $102.7$ triệu lượt lan truyền); trong khi lượt chạy còn lại chạm trần 300s khi xung nhịp CPU bị điều tiết nhiệt xuống dải 1.98--2.50 GHz (so với xung nhịp cơ sở 3.60 GHz).",
        r"Đối với sự biến thiên thời gian giải tuyệt đối (wall-clock time) giữa các phiên đo khác nhau (ví dụ: Commander ở $N=128$ dao động trong khoảng $0.43\text{s} - 0.76\text{s}$ giữa các phiên đo độc lập, có thể xuất phát từ các yếu tố phần cứng và hệ điều hành như điều tiết xung nhịp hoặc tải nền hệ thống), các phân tích so sánh tương đối luôn duy trì tính nhất quán cao: tỷ lệ tăng tốc của Commander so với Sequential Counter ở $N=128$ luôn duy trì ổn định từ 31 đến 55 lần trên mọi phiên đo, khẳng định ưu thế cấu trúc vượt trội của cây phân cấp."
    ]
    new_session_var = (
        r"Đối với sự biến thiên thời gian giải tuyệt đối (wall-clock time) giữa các phiên đo khác nhau (ví dụ: Commander ở $N=128$ dao động trong khoảng $0.43\text{s} - 0.76\text{s}$ giữa các phiên đo độc lập, có thể xuất phát từ các yếu tố phần cứng và hệ điều hành như điều tiết xung nhịp hoặc tải nền hệ thống), các phân tích so sánh tương đối luôn duy trì tính nhất quán cao: Commander ở $N=128$ luôn nhanh hơn ít nhất 31 lần so với Sequential Counter (dao động từ 31 đến 55 lần giữa các phiên đo khác nhau), thể hiện ưu thế nhất quán của cấu trúc cây phân cấp. Toàn bộ dữ liệu của các phiên đo trước đây được lưu trữ đầy đủ trong thư mục \path{data/} của kho mã nguồn (bao gồm \path{data/ablation_amo.csv} và \path{data/product_1000_multitrial.json}) để phục vụ đối chiếu độc lập. Ở quy mô cực đại $N=1000$ (khi Product có 1 lần chạm trần 300s và 2 lần giải thành công $\approx 200$s), các yếu tố tải bộ nhớ đệm L3, phân mảnh bộ nhớ và cơ chế điều phối tiến trình nền của hệ điều hành được nhìn nhận dưới dạng các giả thuyết thực nghiệm giải thích độ nhạy của solver. Đặc biệt, để kiểm chứng sâu hơn độ nhạy của Product tại $N=1000$, chúng tôi đã tiến hành thêm một phiên đo độc lập thứ hai có ghi vết tài nguyên phần cứng liên tục qua \texttt{psutil}. Kết quả tái xác nhận tỷ lệ giải thành công đúng 2/3 lần ($235.00$s và $231.65$s, RAM đỉnh $\approx 3{,}833$ MB) với các chỉ số CDCL đồng nhất ($13{,}397$ xung đột, $1{,}657{,}256$ quyết định và $102.7$ triệu lượt lan truyền); trong khi lượt chạy còn lại chạm trần 300s khi xung nhịp CPU bị điều tiết nhiệt xuống dải 1.98--2.50 GHz (so với xung nhịp cơ sở 3.60 GHz)."
    )
    for old_s in old_session_var_list:
        content = content.replace(old_s, new_session_var)

    # 8. Section 4.3: Neutral tone for Gurobi license limit
    old_gurobi_43 = (
        r"Cần làm rõ rằng đây là giới hạn kỹ thuật của gói license hạn chế kích thước đi kèm gói pip, không phải lỗi thuật toán hay license học thuật đầy đủ."
    )
    new_gurobi_43 = (
        r"Cần lưu ý rằng việc dừng lại của Gurobi ở $N \ge 64$ xuất phát từ giới hạn kỹ thuật của gói license hạn chế kích thước (size-limited license) đi kèm bản phân phối pip công khai (tối đa 2.000 biến), thay vì phản ánh giới hạn năng lực giải thuật của phiên bản Gurobi thương mại đầy đủ."
    )
    content = content.replace(old_gurobi_43, new_gurobi_43)

    # 9. Section 5: Conclusion N=1000 Product phrasing and remove "tuyệt đối"
    old_conc_prod_list = [
        r"\item \textbf{Năng lực mở rộng của Commander và Product:} Commander Variable và Product Encoding là hai kỹ thuật mã hóa có năng lực mở rộng tốt nhất. Commander Variable giúp solver CaDiCaL đạt tốc độ giải nhanh nhất trên dải $N \in [16, 128]$ (chỉ $0.76$s ở $N=128$), đồng thời duy trì độ ổn định tuyệt đối lên tới $N=500$ ($32.11$s, 3/3 lần) và $N=1000$ ($100.92$s, 3/3 lần thành công trên bàn cờ 1 triệu ô). Product Encoding đạt tốc độ tương đương ở $N=500$ ($32.26$s, 3/3 lần) và đạt tỷ lệ giải thành công 2/3 lần tại $N=1000$ (trung vị $200.36$s; 1 lần chạm giới hạn thời gian 300s do chi phí lan truyền trên 11.95 triệu mệnh đề).",
        r"\item \textbf{Năng lực mở rộng của Commander và Product:} Commander Variable và Product Encoding là hai kỹ thuật mã hóa có năng lực mở rộng tốt nhất. Commander Variable giúp solver CaDiCaL đạt tốc độ giải nhanh nhất trên dải $N \in [16, 128]$ (chỉ $0.76$s ở $N=128$), đồng thời duy trì độ ổn định tuyệt đối lên tới $N=500$ ($32.11$s, 3/3 lần) và $N=1000$ ($100.92$s, 3/3 lần thành công trên bàn cờ 1 triệu ô). Product Encoding đạt tốc độ tương đương ở $N=500$ ($32.26$s, 3/3 lần) và đạt tỷ lệ giải thành công 2/3 lần tại $N=1000$ (trung vị $200.36$s; 1 lần chạm giới hạn thời gian 300s với nguyên nhân chưa được xác định chắc chắn).",
        r"\item \textbf{Năng lực mở rộng của Commander và Product:} Commander Variable và Product Encoding là hai kỹ thuật mã hóa có năng lực mở rộng tốt nhất. Commander Variable giúp solver CaDiCaL đạt tốc độ giải nhanh nhất trên dải $N \in [16, 128]$ (chỉ $0.76$s ở $N=128$), đồng thời duy trì độ ổn định cao lên tới $N=500$ ($32.11$s, 3/3 lần) và $N=1000$ ($100.92$s, 3/3 lần thành công trên bàn cờ 1 triệu ô). Product Encoding đạt tốc độ tương đương ở $N=500$ ($32.26$s, 3/3 lần) và đạt tỷ lệ giải thành công 2/3 lần tại $N=1000$ (trung vị $200.36$s; 1 lần chạm giới hạn thời gian 300s với nguyên nhân chưa được xác định chắc chắn)."
    ]
    new_conc_prod = (
        r"\item \textbf{Năng lực mở rộng của Commander và Product:} Commander Variable và Product Encoding là hai kỹ thuật mã hóa có năng lực mở rộng tốt nhất. Commander Variable giúp solver CaDiCaL đạt tốc độ giải nhanh nhất trên dải $N \in [16, 128]$ (chỉ $0.76$s ở $N=128$), đồng thời duy trì độ ổn định cao lên tới $N=500$ ($32.11$s, 3/3 lần) và $N=1000$ ($100.92$s, 3/3 lần thành công trên bàn cờ 1 triệu ô, độ lệch chuẩn $\sigma \approx 3.17$s). Product Encoding đạt tốc độ tương đương ở $N=500$ ($32.26$s, 3/3 lần) và đạt tỷ lệ giải thành công 2/3 lần tại $N=1000$ (trung vị $200.36$s; 1 lần chạm giới hạn thời gian 300s với nguyên nhân chưa được xác định chắc chắn)."
    )
    for old_s in old_conc_prod_list:
        content = content.replace(old_s, new_conc_prod)

    # 10. Data Availability: Author's public GitHub repo + list of data files
    old_data_avail_list = [
        r"Toàn bộ mã nguồn cài đặt 5 kỹ thuật mã hóa AMO, các bộ giải SAT (PySAT), CP-SAT, Gurobi, SCIP và dữ liệu thực nghiệm được cung cấp đầy đủ trong gói dự án đính kèm và lưu trữ công khai trên GitHub repository:",
        r"Toàn bộ mã nguồn cài đặt 5 kỹ thuật mã hóa AMO, các bộ giải SAT (PySAT), CP-SAT, Gurobi, SCIP và toàn bộ dữ liệu thực nghiệm thô được công bố công khai tại kho lưu trữ GitHub chính thức của nhóm nghiên cứu:"
    ]
    new_data_avail = (
        r"Toàn bộ mã nguồn cài đặt 5 kỹ thuật mã hóa AMO, các bộ giải SAT (PySAT), CP-SAT, Gurobi, SCIP và toàn bộ dữ liệu thực nghiệm thô được công bố công khai tại kho lưu trữ GitHub chính thức của tác giả:"
    )
    for old_s in old_data_avail_list:
        content = content.replace(old_s, new_data_avail)

    old_data_items_list = [
        (
            r"\begin{itemize}" "\n"
            r"    \item \textbf{Mã nguồn thực nghiệm:} \path{scripts/isolated_run_worker.py}, \path{scripts/run_isolated_master_benchmark.py}, \path{scripts/run_multisolver_benchmark.py}." "\n"
            r"    \item \textbf{Tự động sinh bảng biểu:} \path{scripts/generate_all_tables_from_master.py}, \path{scripts/sync_data_files.py}." "\n"
            r"    \item \textbf{Dữ liệu thực nghiệm gốc:} \path{data/master_cadical_runs.csv}, \path{data/master_multisolver_runs.csv}, \path{data/benchmark_execution.log}." "\n"
            r"    \item \textbf{Kho lưu trữ GitHub:} \url{https://github.com/vnu-uet-khmt/nqueens-sat-solver}" "\n"
            r"\end{itemize}"
        ),
        (
            r"\begin{itemize}" "\n"
            r"    \item \textbf{Mã nguồn thực nghiệm:} \path{scripts/isolated_run_worker.py}, \path{scripts/run_isolated_master_benchmark.py}, \path{scripts/run_multisolver_benchmark.py}." "\n"
            r"    \item \textbf{Tự động sinh bảng biểu:} \path{scripts/generate_all_tables_from_master.py}, \path{scripts/sync_data_files.py}." "\n"
            r"    \item \textbf{Dữ liệu thực nghiệm gốc:} \path{data/master_cadical_runs.csv}, \path{data/master_multisolver_runs.csv}, \path{data/benchmark_execution.log}." "\n"
            r"    \item \textbf{Kho lưu trữ GitHub:} \url{https://github.com/Ckipmunk/nqueens-sat-solver}" "\n"
            r"\end{itemize}"
        )
    ]
    new_data_items = (
        r"\begin{itemize}" "\n"
        r"    \item \textbf{Mã nguồn thực nghiệm:} \path{scripts/isolated_run_worker.py}, \path{scripts/run_isolated_master_benchmark.py}, \path{scripts/run_multisolver_benchmark.py}." "\n"
        r"    \item \textbf{Tự động sinh bảng biểu:} \path{scripts/generate_all_tables_from_master.py}, \path{scripts/sync_data_files.py}." "\n"
        r"    \item \textbf{Dữ liệu thực nghiệm thô:} \path{data/master_cadical_runs.csv}, \path{data/master_multisolver_runs.csv}, \path{data/ablation_amo.csv}, \path{data/product_1000_multitrial.json}, \path{data/benchmark_execution.log}." "\n"
        r"    \item \textbf{Kho lưu trữ GitHub công khai:} \url{https://github.com/Ckipmunk/nqueens-sat-solver}" "\n"
        r"\end{itemize}"
    )
    for old_items in old_data_items_list:
        content = content.replace(old_items, new_data_items)

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
            print(f"Applied Draft 10 critique fixes to {fname}")

if __name__ == "__main__":
    main()
