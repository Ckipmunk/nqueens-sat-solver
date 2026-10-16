"""
Module: ilp_solver.py
Mục đích: Mô hình hóa và giải bài toán N-Queens bằng Quy hoạch tuyến tính nguyên (ILP / MIP)
sử dụng Gurobi Optimizer (gurobipy) hoặc Google OR-Tools Linear Solver (SCIP / CBC).
"""

import time
from typing import List, Tuple, Optional, Dict

class NQueensILPSolver:
    def __init__(self, n: int):
        self.n = n
        self.solving_time = 0.0

    def solve_gurobi(self, time_limit: float = 60.0, num_threads: int = 1) -> Tuple[Optional[List[int]], Dict]:
        """
        Giải bài toán N-Queens bằng Gurobi Optimizer (gurobipy).
        """
        stats = {
            "n": self.n,
            "method": "Gurobi Optimizer 13.0",
            "num_vars": self.n * self.n,
            "solving_time": 0.0,
            "status": "UNKNOWN"
        }

        try:
            import gurobipy as gp
            from gurobipy import GRB

            env = gp.Env(empty=True)
            env.setParam("OutputFlag", 0)
            env.setParam("Threads", num_threads)
            env.setParam("TimeLimit", time_limit)
            env.start()

            model = gp.Model("NQueens_Gurobi", env=env)
            n = self.n

            # Biến x_{r, c} in {0, 1}
            x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

            # 1. Hàng: sum_c x_{r, c} = 1
            for r in range(n):
                model.addConstr(gp.quicksum(x[r, c] for c in range(n)) == 1, name=f"row_{r}")

            # 2. Cột: sum_r x_{r, c} = 1
            for c in range(n):
                model.addConstr(gp.quicksum(x[r, c] for r in range(n)) == 1, name=f"col_{c}")

            # 3. Đường chéo chính: r - c = k
            for k in range(-(n - 2), n - 1):
                diag = [x[r, c] for r in range(n) for c in range(n) if r - c == k]
                if len(diag) > 1:
                    model.addConstr(gp.quicksum(diag) <= 1, name=f"diag1_{k}")

            # 4. Đường chéo phụ: r + c = k
            for k in range(1, 2 * n - 2):
                anti_diag = [x[r, c] for r in range(n) for c in range(n) if r + c == k]
                if len(anti_diag) > 1:
                    model.addConstr(gp.quicksum(anti_diag) <= 1, name=f"diag2_{k}")

            model.setObjective(0, GRB.MINIMIZE)

            start_t = time.perf_counter()
            model.optimize()
            solve_t = time.perf_counter() - start_t
            stats["solving_time"] = solve_t

            if model.Status in (GRB.OPTIMAL, GRB.SUBOPTIMAL) and model.SolCount > 0:
                stats["status"] = "FEASIBLE"
                queens = [-1] * n
                for r in range(n):
                    for c in range(n):
                        if x[r, c].X > 0.5:
                            queens[r] = c
                            break
                return queens, stats
            elif model.Status == GRB.TIME_LIMIT:
                stats["status"] = "TIMEOUT"
                return None, stats
            elif model.Status == GRB.INFEASIBLE:
                stats["status"] = "INFEASIBLE"
                return None, stats
            else:
                stats["status"] = "TIMEOUT"
                return None, stats

        except Exception as e:
            stats["status"] = "ERROR"
            stats["error"] = str(e)
            return None, stats

    def solve_scip(self, time_limit: float = 60.0) -> Tuple[Optional[List[int]], Dict]:
        """
        Giải bài toán N-Queens bằng SCIP MIP thông qua Google OR-Tools.
        """
        stats = {
            "n": self.n,
            "method": "ILP (SCIP 9.0)",
            "num_vars": self.n * self.n,
            "solving_time": 0.0,
            "status": "UNKNOWN"
        }

        try:
            from ortools.linear_solver import pywraplp
            solver = pywraplp.Solver.CreateSolver("SCIP")
            if not solver:
                solver = pywraplp.Solver.CreateSolver("CBC")
            if not solver:
                stats["status"] = "SOLVER_NOT_FOUND"
                return None, stats

            solver.SetTimeLimit(int(time_limit * 1000))
            n = self.n

            x = {}
            for r in range(n):
                for c in range(n):
                    x[r, c] = solver.BoolVar(f"x_{r}_{c}")

            for r in range(n):
                solver.Add(solver.Sum([x[r, c] for c in range(n)]) == 1)

            for c in range(n):
                solver.Add(solver.Sum([x[r, c] for r in range(n)]) == 1)

            for k in range(-(n - 2), n - 1):
                diag = [x[r, c] for r in range(n) for c in range(n) if r - c == k]
                if len(diag) > 1:
                    solver.Add(solver.Sum(diag) <= 1)

            for k in range(1, 2 * n - 2):
                anti_diag = [x[r, c] for r in range(n) for c in range(n) if r + c == k]
                if len(anti_diag) > 1:
                    solver.Add(solver.Sum(anti_diag) <= 1)

            solver.Minimize(0)

            start_t = time.perf_counter()
            status = solver.Solve()
            solve_t = time.perf_counter() - start_t
            stats["solving_time"] = solve_t

            if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
                stats["status"] = "FEASIBLE"
                queens = [-1] * n
                for r in range(n):
                    for c in range(n):
                        if x[r, c].solution_value() > 0.5:
                            queens[r] = c
                            break
                return queens, stats
            elif status == pywraplp.Solver.INFEASIBLE:
                stats["status"] = "INFEASIBLE"
                return None, stats
            else:
                stats["status"] = "TIMEOUT"
                return None, stats

        except ImportError:
            stats["status"] = "NO_ORTOOLS"
            return None, stats

    def solve(self, solver_type: str = "Gurobi", time_limit: float = 60.0) -> Tuple[Optional[List[int]], Dict]:
        if solver_type.lower() == "gurobi":
            sol, stats = self.solve_gurobi(time_limit=time_limit)
            if stats["status"] not in ("ERROR", "UNKNOWN"):
                return sol, stats
            # Fallback sang SCIP nếu Gurobi gặp lỗi
            return self.solve_scip(time_limit=time_limit)
        else:
            return self.solve_scip(time_limit=time_limit)
