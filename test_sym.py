import sys
sys.path.insert(0, './src')
from sat_solver import NQueensSATSolver

for n in [16, 32, 64]:
    t_no = NQueensSATSolver(n, "commander", False).solve("cadical195")[1]["solving_time"] * 1000.0
    t_sym = NQueensSATSolver(n, "commander", True).solve("cadical195")[1]["solving_time"] * 1000.0
    print(f"N={n:2d} | No-Sym: {t_no:6.2f}ms | With-Sym: {t_sym:6.2f}ms")
