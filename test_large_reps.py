import sys, os, time, gc, psutil
sys.path.insert(0, './src')
from sat_solver import NQueensSATSolver, verify_nqueens_solution

def get_process_memory_mb():
    p = psutil.Process()
    return p.memory_info().rss / (1024 * 1024)

print(f"Initial Memory: {get_process_memory_mb():.1f} MB")

# 1. Test Pairwise at N=256
print("\n=== Testing Pairwise at N=256 ===")
t0 = time.perf_counter()
solver_pw_256 = NQueensSATSolver(256, amo_method='pairwise')
enc_t_256 = time.perf_counter() - t0
mem_enc_256 = get_process_memory_mb()
print(f"N=256 Pairwise: vars={solver_pw_256.num_vars}, clauses={solver_pw_256.num_clauses}, enc_time={enc_t_256:.2f}s, Peak RAM={mem_enc_256:.1f}MB")

t_solve_0 = time.perf_counter()
sol_pw_256, stats_pw_256 = solver_pw_256.solve('cadical195')
solve_t_256 = time.perf_counter() - t_solve_0
print(f"N=256 Pairwise solved: status={stats_pw_256['status']}, solve_time={solve_t_256:.2f}s, valid={verify_nqueens_solution(sol_pw_256) if sol_pw_256 else False}")

del solver_pw_256, sol_pw_256
gc.collect()

# 2. Test Pairwise at N=500 (Check memory limit)
print("\n=== Testing Pairwise at N=500 ===")
t0 = time.perf_counter()
try:
    solver_pw_500 = NQueensSATSolver(500, amo_method='pairwise')
    enc_t_500 = time.perf_counter() - t0
    mem_enc_500 = get_process_memory_mb()
    print(f"N=500 Pairwise: vars={solver_pw_500.num_vars}, clauses={solver_pw_500.num_clauses}, enc_time={enc_t_500:.2f}s, Peak RAM={mem_enc_500:.1f}MB")
except MemoryError as e:
    print(f"N=500 Pairwise OOM during encoding: {e}")
except Exception as e:
    print(f"N=500 Pairwise Exception during encoding: {e}")

# 3. Test CDCL accum_stats for all 5 encodings at N=64 and N=128
print("\n=== Testing CDCL accum_stats for N=64, 128 ===")
for n in [64, 128]:
    for amo in ['pairwise', 'sequential', 'commander', 'binary', 'product']:
        s = NQueensSATSolver(n, amo_method=amo)
        sol, stats = s.solve('cadical195')
        acc = stats.get('accum_stats', {})
        print(f"N={n:3d} | {amo:10s} | vars={stats['num_vars']:6d} | clauses={stats['num_clauses']:8d} | solve={stats['solving_time']:7.4f}s | conflicts={acc.get('conflicts',0):5d} | decisions={acc.get('decisions',0):6d} | propagations={acc.get('propagations',0):8d}")
        del s
        gc.collect()
