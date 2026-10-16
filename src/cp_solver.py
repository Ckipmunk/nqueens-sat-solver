"""
Module: cp_solver.py
Mục đích: Mô hình hóa và giải bài toán N-Queens bằng Lập trình ràng buộc (Constraint Programming)
sử dụng Google OR-Tools CP-SAT (hỗ trợ ràng buộc AllDifferent tối ưu).
"""

import time
from typing import List, Tuple, Optional, Dict

class NQueensCPSolver:
    def __init__(self, n: int):
        self.n = n
        self.solving_time = 0.0

    def solve(self, time_limit: float = 60.0, num_workers: int = 1) -> Tuple[Optional[List[int]], Dict]:
        """
        Giải bài toán N-Queens bằng OR-Tools CP-SAT.
        Biến: q_i là vị trí cột của quân hậu tại hàng i (0 <= q_i < n).
        Ràng buộc:
        1. AllDifferent(q_0, ..., q_{n-1}) : Không cùng cột
        2. AllDifferent(q_i + i)           : Không cùng đường chéo phụ
        3. AllDifferent(q_i - i)           : Không cùng đường chéo chính
        """
        stats = {
            "n": self.n,
            "method": f"CP-SAT (OR-Tools, {num_workers} worker)",
            "solving_time": 0.0,
            "status": "UNKNOWN",
            "num_vars": self.n,
            "num_constraints": 3
        }

        try:
            from ortools.sat.python import cp_model
            model = cp_model.CpModel()

            # Khai báo biến q_i in [0, n - 1]
            queens = [model.NewIntVar(0, self.n - 1, f"q_{i}") for i in range(self.n)]

            # 1. Ràng buộc các cột khác nhau
            model.AddAllDifferent(queens)

            # 2. Ràng buộc các đường chéo chính khác nhau: q_i - i
            diag1 = [queens[i] - i for i in range(self.n)]
            model.AddAllDifferent(diag1)

            # 3. Ràng buộc các đường chéo phụ khác nhau: q_i + i
            diag2 = [queens[i] + i for i in range(self.n)]
            model.AddAllDifferent(diag2)

            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = time_limit
            solver.parameters.num_search_workers = num_workers

            start_t = time.perf_counter()
            status = solver.Solve(model)
            solve_t = time.perf_counter() - start_t

            stats["solving_time"] = solve_t

            if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                stats["status"] = "FEASIBLE"
                sol = [solver.Value(queens[i]) for i in range(self.n)]
                return sol, stats
            elif status == cp_model.INFEASIBLE:
                stats["status"] = "INFEASIBLE"
                return None, stats
            else:
                stats["status"] = "TIMEOUT"
                return None, stats

        except ImportError:
            stats["status"] = "NO_ORTOOLS"
            stats["error"] = "Thư viện ortools chưa được cài đặt."
            return None, stats
