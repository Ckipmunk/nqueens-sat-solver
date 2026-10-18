# HƯỚNG DẪN BIÊN DỊCH BÁO CÁO LATEX TRÊN OVERLEAF VÀ MÁY CÁ NHÂN

Dự án cung cấp báo cáo khoa học bằng tiếng Việt chuẩn Elsevier theo đúng yêu cầu Bài tập lớn số 1 môn Các vấn đề hiện đại trong KHMT:

- **Tác giả:** Phạm Khánh Duy (MSSV: `24021452`, Email: `24021452@vnu.edu.vn`)
- **Giảng viên hướng dẫn:** TS. Tô Văn Khánh (Email: `khanhtv@vnu.edu.vn`)
- **Tập tin chính:** `main.tex` / `nqueens_report_elsevier.tex` (sử dụng mẫu `cas-sc.cls` chính thức của Elsevier).

---

## 1. Hướng dẫn Biên dịch trên Overleaf

Dự án đã đóng gói sẵn tệp nén **`report.zip`** ngay tại thư mục gốc của dự án. Tệp nén này bao gồm đầy đủ:
- Bộ template chính thức: `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst`.
- Tập tin văn bản gốc: `main.tex` (đã đồng bộ 100% với `nqueens_report_elsevier.tex`).
- Tệp định dạng chuẩn mở rộng: `nqueens_report_standard.tex`.
- Tệp trích dẫn: `references.bib`.
- Thư mục hình ảnh độ phân giải cao: `figures/` (cả định dạng PDF vector và PNG).
- Các tệp bảng phụ trợ: `table2_generated.tex`, `table3_generated.tex`, `table4_generated.tex`, `table5a_generated.tex`, `table5b_generated.tex`.

### Các bước tải lên Overleaf:
1. Truy cập [Overleaf.com](https://www.overleaf.com/) và đăng nhập tài khoản.
2. Nhấn **New Project** $\rightarrow$ **Upload Project**.
3. Chọn tệp `report.zip` (ở thư mục gốc dự án) để tải lên. Overleaf sẽ tự động giải nén toàn bộ tệp vào thư mục gốc của project.
4. Cấu hình Compiler: Chọn **pdfLaTeX** hoặc **XeLaTeX**.
5. Nhấn **Recompile** (hoặc nhấn Recompile 2 lần nếu cần đồng bộ chỉ số nhãn và số trang "Page x of 19").

---

## 2. Biên dịch Ngoại tuyến trên Máy tính Cá nhân (Offline qua Terminal)

Nếu máy tính đã cài đặt MiKTeX hoặc TeX Live:

```bash
# Biên dịch file chính với XeLaTeX (chạy 2 lần để cập nhật số trang và tham chiếu):
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex

# Hoặc biên dịch với pdfLaTeX:
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
