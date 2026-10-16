# HƯỚNG DẪN BIÊN DỊCH BÁO CÁO LATEX TRÊN OVERLEAF VÀ MÁY CÁ NHÂN

Dự án cung cấp hai phiên bản tài liệu LaTeX chuẩn khoa học bằng tiếng Việt trong thư mục `report/`:

1. **`nqueens_report_elsevier.tex`**: Phiên bản chuẩn mẫu bài báo khoa học của nhà xuất bản Elsevier (`\documentclass[a4paper,fleqn]{cas-sc}`) theo đúng yêu cầu của Bài tập lớn số 1.
2. **`nqueens_report_standard.tex`**: Phiên bản định dạng `article` chuẩn mực, tương thích 100% với mọi trình biên dịch LaTeX cục bộ và Overleaf mà không đòi hỏi file class mở rộng.

Cả hai phiên bản đều được đồng bộ 100% về cấu trúc học thuật, công thức toán học, Bảng 1, Bảng 2, Bảng 3, số liệu trung vị và các hình vẽ minh họa.

---

## 1. Các thông tin cần điền trước khi nộp bài

Trong file `.tex`, bạn chỉ cần cập nhật 3 vị trí:
1. **Tên tác giả**: Thay `Nguyễn Văn A` thành Họ và tên của bạn.
2. **Mã số sinh viên và Email**: Thay `24020000` và `24020000@vnu.edu.vn` bằng MSSV và email VNU thực tế của bạn.
3. **Mục Data Availability**: Thay đường dẫn GitHub `https://github.com/your-username/nqueens-sat-solver` thành link repository GitHub thực tế của bạn sau khi đẩy mã nguồn lên.

---

## 2. Hướng dẫn Biên dịch trên Overleaf

### Bước 1: Nén thư mục báo cáo
Nén toàn bộ các tệp sau trong thư mục `report/` thành tệp `report.zip`:
- `nqueens_report_elsevier.tex`
- `nqueens_report_standard.tex`
- `references.bib`
- Thư mục con `figures/` chứa:
  - `fig_clauses_scaling.pdf` (và `.png`)
  - `fig_solver_runtime.pdf` (và `.png`)
  - `fig_board_8queens.pdf` (và `.png`)

### Bước 2: Tải lên Overleaf
1. Truy cập [Overleaf.com](https://www.overleaf.com/) và đăng nhập.
2. Nhấn **New Project** $\rightarrow$ **Upload Project**.
3. Chọn tệp `report.zip` để tải lên.

### Bước 3: Cấu hình Trình biên dịch (Compiler)
1. Trên thanh công cụ Overleaf, nhấn vào biểu tượng **Menu** (góc trên cùng bên trái).
2. Tại mục **Compiler**:
   - Khuyên dùng: Chọn **XeLaTeX** (hỗ trợ font Unicode tiếng Việt hoàn hảo nhất trên mọi mẫu Elsevier).
   - Hoặc có thể chọn **pdfLaTeX** (đã cấu hình sẵn gói `[vietnamese,english]{babel}` và `[T5,T1]{fontenc}`).
3. Tại mục **Main document**:
   - Chọn `nqueens_report_elsevier.tex` (hoặc `nqueens_report_standard.tex`).
4. Nhấn **Recompile** để xuất file PDF hoàn chỉnh.

---

## 3. Biên dịch trên Máy tính Cá nhân (Offline qua Terminal)

Nếu máy tính đã cài đặt MiKTeX hoặc TeX Live:

```bash
# Biên dịch file Elsevier với XeLaTeX:
xelatex nqueens_report_elsevier.tex
bibtex nqueens_report_elsevier
xelatex nqueens_report_elsevier.tex
xelatex nqueens_report_elsevier.tex

# Hoặc biên dịch file Standard với pdfLaTeX:
pdflatex nqueens_report_standard.tex
bibtex nqueens_report_standard
pdflatex nqueens_report_standard.tex
pdflatex nqueens_report_standard.tex
```
