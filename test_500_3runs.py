import sys, time
sys.path.insert(0, './src')
from sat_solver import NQueensSATSolver

print("=== Measuring Commander at N=500 (3 runs) ===", flush=True)
for r in range(3):
    t0 = time.perf_counter()
    s = NQueensSATSolver(500, amo_method='commander')
    enc = time.perf_counter() - t0
    sol, stats = s.solve('cadical195')
    print(f"Commander N=500 Run {r+1}: enc={enc:.2f}s, solve={stats['solving_time']:.2f}s, status={stats['status']}", flush=True)

print("\n=== Measuring Product at N=500 (3 runs) ===", flush=True)
for r in range(3):
    t0 = time.perf_counter()
    s = NQueensSATSolver(500, amo_method='product')
    enc = time.perf_counter() - t0
    sol, stats = s.solve('cadical195')
    print(f"Product N=500 Run {r+1}: enc={enc:.2f}s, solve={stats['solving_time']:.2f}s, status={stats['status']}", flush=True)
