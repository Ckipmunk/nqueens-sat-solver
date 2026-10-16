"""
Module: sat_solver.py
Mục đích: Xây dựng mô hình SAT hoàn chỉnh cho bài toán N-Queens và giải thông qua PySAT
(hoặc xuất file DIMACS CNF phục vụ các bộ giải độc lập như CaDiCaL, Kissat, Glucose).
"""

import time
from typing import List, Dict, Tuple, Optional
from amo_encodings import VarManager, encode_alo, encode_amo, encode_exactly_one

class NQueensSATSolver:
    def __init__(self, n: int, amo_method: str = "sequential", symmetry_breaking: bool = False):
        """
        Khởi tạo mô hình N-Queens bằng SAT.
        :param n: Kích thước bàn cờ N x N
        :param amo_method: Kỹ thuật mã hóa AMO ('pairwise', 'sequential', 'commander', 'binary', 'product')
        :param symmetry_breaking: Có áp dụng kỹ thuật phá vỡ đối xứng hay không
        """
        self.n = n
        self.amo_method = amo_method
        self.symmetry_breaking = symmetry_breaking
        
        # Quản lý biến logic:
        # Biến cơ sở X_{i,j} tương ứng với ô (i, j) có hậu hay không (0 <= i, j < n).
        # Chỉ số từ 1 đến n*n.
        self.var_mgr = VarManager(start_id=n * n + 1)
        self.clauses: List[List[int]] = []
        self.encoding_time = 0.0
        self.solving_time = 0.0
        
        self._build_model()

    def var_id(self, r: int, c: int) -> int:
        """Chuyển tọa độ (r, c) thành mã biến logic (1-indexed)."""
        return r * self.n + c + 1

    def coord_from_id(self, var: int) -> Tuple[int, int]:
        """Chuyển mã biến cơ sở thành tọa độ (r, c)."""
        idx = var - 1
        return idx // self.n, idx % self.n

    def _build_model(self):
        """Xây dựng toàn bộ tập mệnh đề CNF cho bài toán N-Queens."""
        start_t = time.perf_counter()
        n = self.n
        clauses = []

        # 1. Ràng buộc hàng: Mỗi hàng có ĐÚNG 1 quân hậu (Exactly-One = ALO + AMO)
        for r in range(n):
            row_vars = [self.var_id(r, c) for c in range(n)]
            clauses.extend(encode_exactly_one(row_vars, self.amo_method, self.var_mgr))

        # 2. Ràng buộc cột: Mỗi cột có ĐÚNG 1 quân hậu (Exactly-One = ALO + AMO)
        for c in range(n):
            col_vars = [self.var_id(r, c) for r in range(n)]
            clauses.extend(encode_exactly_one(col_vars, self.amo_method, self.var_mgr))

        # 3. Ràng buộc đường chéo chính (xuôi): r - c = k
        # k chạy từ -(n-2) đến (n-2) (bỏ qua các đường chéo chỉ có 1 ô)
        for k in range(-(n - 2), n - 1):
            diag_vars = []
            for r in range(n):
                c = r - k
                if 0 <= c < n:
                    diag_vars.append(self.var_id(r, c))
            if len(diag_vars) > 1:
                clauses.extend(encode_amo(diag_vars, self.amo_method, self.var_mgr))

        # 4. Ràng buộc đường chéo phụ (ngược): r + c = k
        # k chạy từ 1 đến 2n - 3 (bỏ qua k=0 và k=2n-2 có độ dài 1 ô)
        for k in range(1, 2 * n - 2):
            anti_diag_vars = []
            for r in range(n):
                c = k - r
                if 0 <= c < n:
                    anti_diag_vars.append(self.var_id(r, c))
            if len(anti_diag_vars) > 1:
                clauses.extend(encode_amo(anti_diag_vars, self.amo_method, self.var_mgr))

        # 5. Phá vỡ đối xứng (Symmetry Breaking - tùy chọn):
        # Bàn cờ N-Queens có đối xứng phản xạ gương qua trục giữa cột.
        # Ta có thể giới hạn quân hậu ở hàng 0 chỉ nằm ở nửa bên trái bàn cờ: c < ceil(n / 2)
        if self.symmetry_breaking and n > 1:
            mid = (n + 1) // 2
            for c in range(mid, n):
                clauses.append([-self.var_id(0, c)])

        self.clauses = clauses
        self.encoding_time = time.perf_counter() - start_t

    @property
    def num_vars(self) -> int:
        """Tổng số biến (bao gồm biến cơ sở và biến phụ tạo thêm)."""
        return self.var_mgr.next_var - 1

    @property
    def num_clauses(self) -> int:
        """Tổng số mệnh đề CNF."""
        return len(self.clauses)

    def export_dimacs(self, filepath: str):
        """Xuất mô hình ra định dạng DIMACS CNF chuẩn."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"c N-Queens SAT Model (N={self.n}, AMO={self.amo_method})\n")
            f.write(f"p cnf {self.num_vars} {self.num_clauses}\n")
            for clause in self.clauses:
                f.write(" ".join(map(str, clause)) + " 0\n")

    def solve(self, solver_name: str = "cadical195") -> Tuple[Optional[List[int]], Dict]:
        """
        Giải bài toán bằng solver được chỉ định qua PySAT.
        :param solver_name: Tên solver trong PySAT ('cadical195', 'glucose4', 'kissat', 'lingeling', v.v.)
        :return: (nghiệm dưới dạng vị trí cột của từng hàng, dict thông tin thống kê)
        """
        stats = {
            "n": self.n,
            "amo_method": self.amo_method,
            "num_vars": self.num_vars,
            "num_clauses": self.num_clauses,
            "encoding_time": self.encoding_time,
            "solving_time": 0.0,
            "total_time": 0.0,
            "status": "UNKNOWN",
            "solver": solver_name
        }

        try:
            from pysat.solvers import Solver
            t_start = time.perf_counter()
            with Solver(name=solver_name, bootstrap_with=self.clauses) as solver:
                sat_res = solver.solve()
                solve_t = time.perf_counter() - t_start
                self.solving_time = solve_t
                stats["solving_time"] = solve_t
                stats["total_time"] = self.encoding_time + solve_t

                if sat_res:
                    model = solver.get_model()
                    stats["status"] = "SAT"
                    queen_positions = self._extract_solution(model)
                    return queen_positions, stats
                else:
                    stats["status"] = "UNSAT"
                    return None, stats

        except ImportError:
            stats["status"] = "NO_PYSAT"
            stats["error"] = "Thư viện python-sat (PySAT) chưa được cài đặt."
            return None, stats

    def _extract_solution(self, model: List[int]) -> List[int]:
        """Trích xuất vị trí cột của từng quân hậu từ mô hình nghiệm True/False."""
        sol_set = set(v for v in model if v > 0 and v <= self.n * self.n)
        queens = [-1] * self.n
        for r in range(self.n):
            for c in range(self.n):
                if self.var_id(r, c) in sol_set:
                    queens[r] = c
                    break
        return queens


def verify_nqueens_solution(queens: List[int]) -> bool:
    """
    Hàm kiểm tra độc lập tính hợp lệ của nghiệm N-Queens:
    - Mỗi hàng có đúng 1 quân hậu
    - Không có 2 quân hậu nào cùng cột
    - Không có 2 quân hậu nào cùng đường chéo
    """
    n = len(queens)
    if any(q < 0 or q >= n for q in queens):
        return False
    if len(set(queens)) != n:
        return False
    for i in range(n):
        for j in range(i + 1, n):
            if abs(queens[i] - queens[j]) == abs(i - j):
                return False
    return True
