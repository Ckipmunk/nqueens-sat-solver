import os
import sys
import time
import json
import psutil
import hashlib

# Ensure src in sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, "src"))

from sat_solver import NQueensSATSolver
from pysat.solvers import Solver

def compute_cnf_hash(clauses):
    # Sort clauses to get canonical hash
    # For very large formula (> 1M clauses), sample deterministic subset for speed
    if len(clauses) > 500000:
        sample = clauses[::max(1, len(clauses) // 100000)]
        sorted_c = [sorted(c) for c in sample]
        sorted_c.sort()
        s = f"SAMPLE_{len(clauses)}_{sorted_c}".encode('utf-8')
    else:
        sorted_c = [sorted(c) for c in clauses]
        sorted_c.sort()
        s = str(sorted_c).encode('utf-8')
    return hashlib.sha256(s).hexdigest()[:8]

def run_worker(n, method, run_id, timeout=300):
    p = psutil.Process(os.getpid())
    res = {
        "n": n,
        "method": method,
        "run_id": run_id,
        "status": "UNKNOWN",
        "num_vars": 0,
        "num_clauses": 0,
        "cnf_hash": "",
        "encoding_time": 0.0,
        "solving_time": 0.0,
        "peak_ram_mb": 0.0,
        "conflicts": 0,
        "decisions": 0,
        "propagations": 0,
        "restarts": 0
    }

    try:
        # 1. Encoding
        t0 = time.perf_counter()
        model = NQueensSATSolver(n, amo_method=method)
        t_enc = time.perf_counter() - t0
        
        res["encoding_time"] = t_enc
        res["num_vars"] = model.num_vars
        res["num_clauses"] = model.num_clauses
        res["cnf_hash"] = compute_cnf_hash(model.clauses)

        # 2. Solving
        t1 = time.perf_counter()
        slv = Solver(name='cadical195', bootstrap_with=model.clauses)
        is_sat = slv.solve()
        t_solv = time.perf_counter() - t1

        stats = slv.accum_stats()
        slv.delete()

        res["solving_time"] = t_solv
        res["status"] = "SAT" if is_sat else "UNSAT"
        res["conflicts"] = stats.get("conflicts", 0)
        res["decisions"] = stats.get("decisions", 0)
        res["propagations"] = stats.get("propagations", 0)
        res["restarts"] = stats.get("restarts", 0)

    except MemoryError:
        res["status"] = "OOM"
    except Exception as e:
        res["status"] = f"ERROR: {str(e)}"
    finally:
        # Measure true isolated peak working set of this process
        res["peak_ram_mb"] = p.memory_info().peak_wset / (1024 * 1024)

    print(json.dumps(res))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({"error": "Usage: isolated_run_worker.py <n> <method> <run_id> [timeout]"}))
        sys.exit(1)

    n_val = int(sys.argv[1])
    method_val = sys.argv[2]
    run_id_val = int(sys.argv[3])
    timeout_val = int(sys.argv[4]) if len(sys.argv) > 4 else 300

    run_worker(n_val, method_val, run_id_val, timeout_val)
