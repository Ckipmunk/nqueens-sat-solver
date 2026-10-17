import sys, os, time, gc, psutil, json
sys.path.insert(0, './src')
from sat_solver import NQueensSATSolver, verify_nqueens_solution

def get_process_memory_mb():
    p = psutil.Process()
    return p.memory_info().rss / (1024 * 1024)

print("Starting 3-run evaluation for large N (256, 500, 1000)...", flush=True)

configs = [
    (256, 'commander'),
    (256, 'product'),
    (500, 'commander'),
    (500, 'product'),
    (1000, 'commander'),
    (1000, 'product')
]

results = {}

for n, amo in configs:
    print(f"\n==================== N = {n}, AMO = {amo} ====================", flush=True)
    results[f"{n}_{amo}"] = {
        "n": n,
        "amo": amo,
        "runs": [],
        "encoding_times": [],
        "peak_ram_mb": []
    }
    
    # We do 3 runs
    for r in range(3):
        gc.collect()
        mem_before = get_process_memory_mb()
        t0 = time.perf_counter()
        solver = NQueensSATSolver(n, amo_method=amo)
        enc_t = time.perf_counter() - t0
        mem_after = get_process_memory_mb()
        peak_ram = max(mem_after, mem_before)
        
        num_v = solver.num_vars
        num_c = solver.num_clauses
        
        print(f"Run {r+1}: vars={num_v}, clauses={num_c}, enc_t={enc_t:.2f}s, Peak RAM={peak_ram:.1f}MB", flush=True)
        
        # Solving with 300s limit check
        t_s0 = time.perf_counter()
        sol, stats = solver.solve('cadical195')
        s_time = stats['solving_time']
        status = stats['status']
        acc = stats.get('accum_stats', {})
        
        valid = False
        if sol:
            valid = verify_nqueens_solution(sol)
            
        print(f"Run {r+1} result: status={status}, solve_t={s_time:.2f}s, valid={valid}, conflicts={acc.get('conflicts',0)}, decisions={acc.get('decisions',0)}, props={acc.get('propagations',0)}", flush=True)
        
        results[f"{n}_{amo}"]["runs"].append({
            "run": r + 1,
            "solving_time_s": s_time,
            "status": status,
            "valid": valid,
            "accum_stats": acc
        })
        results[f"{n}_{amo}"]["encoding_times"].append(enc_t)
        results[f"{n}_{amo}"]["peak_ram_mb"].append(peak_ram)
        results[f"{n}_{amo}"]["num_vars"] = num_v
        results[f"{n}_{amo}"]["num_clauses"] = num_c
        
        del solver, sol
        gc.collect()

# Save to JSON
with open('data/large_n_3runs.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("\nAll runs finished and saved to data/large_n_3runs.json!", flush=True)
