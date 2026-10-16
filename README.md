# BÀI TẬP LỚN SỐ 1: N-QUEENS SOLVER BẰNG SAT SOLVING VÀ SO SÁNH VỚI ILP, CP

**Môn học:** Các vấn đề hiện đại trong Khoa học Máy tính  
**Học kỳ:** HK I, Năm học 2026 – 2027  
**Đề tài:** 2. N-Queens Solver (SAT Encoding for Logic Puzzles, N-Queens)  
**Mẫu báo cáo:** Chuẩn bài báo Elsevier (`\documentclass[a4paper,fleqn]{cas-sc}`) theo hướng dẫn file mẫu đính kèm.

---

## 📌 Giới thiệu dự án

Dự án này thực hiện việc nghiên cứu, cài đặt và đánh giá thực nghiệm toàn diện bài toán $N$-Queens giải bằng công nghệ **SAT Solving** (thông qua thư viện **PySAT**) và so sánh đối chứng với các phương pháp giải chính xác khác:
- **Constraint Programming (CP):** Google OR-Tools CP-SAT (toán tử toàn cục `AllDifferent`).
- **Integer Linear Programming (ILP):** Gurobi Optimizer 13.0 và SCIP 9.0 (0-1 MIP Model).

### Các đóng góp chính của dự án:
1. **Triển khai 5 kỹ thuật mã hóa ràng buộc At-Most-One (AMO):**
   - **Pairwise (Direct):** $\mathcal{O}(k^2)$ mệnh đề, 0 biến phụ (gọi qua PySAT CardEnc hoặc tự cài đặt).
   - **Sequential Counter (Sinz, 2005):** $\mathcal{O}(k)$ mệnh đề, $\mathcal{O}(k)$ biến phụ (gọi qua PySAT CardEnc hoặc tự cài đặt).
   - **Commander Variable (Klieber & Kwon, 2007):** $\mathcal{O}(k)$ mệnh đề, cấu trúc phân cấp (tự cài đặt độc lập theo bài báo gốc).
   - **Binary (Bitwise, Frisch et al., 2005):** $\mathcal{O}(k \log k)$ mệnh đề, $\mathcal{O}(\log k)$ biến phụ (gọi qua PySAT CardEnc hoặc tự cài đặt).
   - **Product Encoding (Chen, 2010):** $\mathcal{O}(k)$ mệnh đề, $\mathcal{O}(\sqrt{k})$ biến phụ (tự cài đặt độc lập theo bài báo gốc).
2. **Quy trình đo đạc thực nghiệm chuẩn khoa học:**
   - Chạy lặp lại 3 lần lấy giá trị trung vị (median) để loại trừ sai số ngẫu nhiên.
   - Thống nhất cùng một giới hạn thời gian (Time Limit = 300.0s) cho tất cả các solver.
   - Chạy đơn luồng (1 worker / 1 thread) để đảm bảo so sánh công bằng với SAT solver chạy 1 luồng.
3. **Thực nghiệm quy mô lớn:** Đánh giá trên các kích thước bàn cờ từ nhỏ ($N=8$) đến cực lớn ($N=1000$).
4. **Báo cáo khoa học bằng LaTeX tiếng Việt:** Viết theo mẫu chuẩn Elsevier `cas-sc` với đầy đủ Related Work, chứng minh tính đúng đắn (Proposition & Proofs), phân tích chuyên sâu về kiến trúc CDCL, và các mục khai báo chuẩn mực (CRediT, Competing Interest, Generative AI).

---

## 📂 Cấu trúc thư mục dự án

```
nqueens_sat_project/
├── src/
│   ├── amo_encodings.py      # Cài đặt 5 kỹ thuật mã hóa AMO: Pairwise, SeqCounter, Commander, Binary, Product
│   ├── sat_solver.py         # Bộ giải SAT N-Queens với PySAT (CaDiCaL 1.9.5, Glucose 4.2)
│   ├── cp_solver.py          # Bộ giải Constraint Programming bằng Google OR-Tools CP-SAT (1 worker)
│   ├── ilp_solver.py         # Bộ giải ILP 0-1 bằng Gurobi Optimizer 13.0 và SCIP 9.0 (1 thread)
│   ├── benchmark.py          # Kịch bản thực nghiệm đo lường trung vị tự động từ N=8 đến N=1000
│   └── plot_results.py       # Tự động vẽ các biểu đồ khoa học và hình minh họa bàn cờ
├── data/
│   ├── ablation_amo.json     # Dữ liệu đo đạc 5 kỹ thuật mã hóa AMO (JSON)
│   ├── ablation_amo.csv      # Bảng dữ liệu 5 kỹ thuật mã hóa AMO (CSV)
│   ├── solver_comparison.json# Dữ liệu so sánh thời gian giải giữa SAT, CP-SAT, Gurobi, SCIP (JSON)
│   └── solver_comparison.csv # Bảng dữ liệu so sánh thời gian giải (CSV)
├── report/
│   ├── nqueens_report_elsevier.tex # Báo cáo khoa học LaTeX theo chuẩn Elsevier cas-sc (Tiếng Việt)
│   ├── nqueens_report_standard.tex # Báo cáo khoa học LaTeX bản chuẩn article (dễ biên dịch mọi nơi)
│   ├── references.bib        # Danh mục tài liệu tham khảo học thuật BibTeX
│   ├── README_OVERLEAF.md    # Hướng dẫn chi tiết biên dịch trên Overleaf
│   └── figures/              # Chứa các biểu đồ xuất ra cho báo cáo
│       ├── fig_clauses_scaling.pdf (.png)
│       ├── fig_solver_runtime.pdf (.png)
│       └── fig_board_8queens.pdf (.png)
└── README.md                 # Tài liệu hướng dẫn sử dụng dự án
```

---

## 🚀 Hướng dẫn cài đặt và Chạy thử nghiệm

### 1. Cài đặt môi trường Python
Yêu cầu Python phiên bản $\ge 3.8$. Cài đặt các thư viện:
```bash
pip install python-sat ortools gurobipy matplotlib
```

### 2. Kiểm tra nhanh các thuật toán mã hóa và bộ giải:
```bash
python -c "
import sys; sys.path.insert(0, './src')
from sat_solver import NQueensSATSolver, verify_nqueens_solution
solver = NQueensSATSolver(8, amo_method='commander')
sol, stats = solver.solve('cadical195')
print('Nghiệm tìm được:', sol)
print('Xác minh hợp lệ:', verify_nqueens_solution(sol))
print('Thời gian giải:', stats['solving_time'], 's')
"
```

### 3. Chạy thực nghiệm đo đạc toàn diện (trung vị 3 lần lặp, Time limit 300s):
```bash
python ./src/benchmark.py
```
Lệnh này sẽ:
- Thực hiện khảo sát triệt tiêu (Ablation study) trên 5 kỹ thuật AMO với $N \in [8, 16, 32, 64, 128]$.
- Thực hiện so sánh đối đầu giữa SAT CaDiCaL, SAT Glucose, Google OR-Tools CP-SAT, Gurobi Optimizer và SCIP MIP với $N \in [8, 16, 32, 64, 128, 256, 500, 1000]$.
- Tự động xuất kết quả đo đạc ra cả file JSON và CSV trong thư mục `data/`.

### 4. Vẽ lại các đồ thị và hình ảnh báo cáo:
```bash
python ./src/plot_results.py
```
Biểu đồ sẽ được tự động lưu vào thư mục `report/figures/`.

---

## 📄 Hướng dẫn biên dịch Báo cáo LaTeX

Vui lòng xem hướng dẫn chi tiết tại [report/README_OVERLEAF.md](report/README_OVERLEAF.md).
- Nén toàn bộ thư mục `report/` thành file zip và upload lên Overleaf.
- Trên Overleaf, chọn file `nqueens_report_elsevier.tex` (hoặc `nqueens_report_standard.tex`) và bấm **Recompile** để xuất file PDF hoàn chỉnh.

---

## 🌐 Hướng dẫn Đẩy dự án lên GitHub

Theo yêu cầu của đề bài:
> *"Sinh viên chỉ rõ link Github (or others) về Repository lưu mã nguồn và kết quả thực nghiệm của bài toán trong Báo cáo BTL số 1 (để phần Data Availability)."*

Các bước đẩy mã nguồn lên GitHub:
```bash
# Khởi tạo git repository
git init
git add .
git commit -m "feat: N-Queens SAT Solver with 5 AMO encodings, CP/ILP/Gurobi benchmarks, and LaTeX report"

# Liên kết với remote repository của bạn trên GitHub
git branch -M main
git remote add origin https://github.com/<your-username>/nqueens-sat-solver.git
git push -u origin main
```
Sau đó, hãy cập nhật đường link GitHub thực tế của bạn vào mục **Data Availability** trong file báo cáo LaTeX trước khi nộp.
