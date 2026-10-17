import sys
import os
sys.path.insert(0, os.path.abspath('src'))
import statistics
from sat_solver import NQueensSATSolver
import csv

methods = ['pairwise', 'sequential', 'commander', 'binary', 'product']
sizes = [32, 64, 128]
results = []

print("Running 3-run CDCL search stats measurement...")
for N in sizes:
    for amo in methods:
        runs = []
        for r in range(3):
            solver = NQueensSATSolver(n=N, amo_method=amo)
            _, stats = solver.solve("cadical195")
            st = stats.get('accum_stats', {})
            runs.append({
                'run': r + 1,
                'solve_time': stats['solving_time'],
                'conflicts': st.get('conflicts', 0),
                'decisions': st.get('decisions', 0),
                'propagations': st.get('propagations', 0),
                'vars': stats['num_vars'],
                'clauses': stats['num_clauses']
            })
        
        times = [x['solve_time'] for x in runs]
        confs = [x['conflicts'] for x in runs]
        decs = [x['decisions'] for x in runs]
        props = [x['propagations'] for x in runs]
        
        results.append({
            'N': N,
            'AMO': amo,
            'vars': runs[0]['vars'],
            'clauses': runs[0]['clauses'],
            'med_time': statistics.median(times),
            'med_conflicts': int(statistics.median(confs)),
            'med_decisions': int(statistics.median(decs)),
            'med_props': int(statistics.median(props)),
            'all_runs': runs
        })
        print(f"N={N:3d} | {amo:11s} | Solve: {statistics.median(times):.4f}s | Conf: {int(statistics.median(confs)):6d} | Dec: {int(statistics.median(decs)):6d} | Prop: {int(statistics.median(props)):9d}")

# Save detailed CSV
with open('data/cdcl_search_stats_3runs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['N', 'AMO', 'vars', 'clauses', 'median_time_s', 'median_conflicts', 'median_decisions', 'median_propagations',
                     'run1_time', 'run1_conf', 'run1_dec', 'run1_prop',
                     'run2_time', 'run2_conf', 'run2_dec', 'run2_prop',
                     'run3_time', 'run3_conf', 'run3_dec', 'run3_prop'])
    for r in results:
        runs = r['all_runs']
        writer.writerow([
            r['N'], r['AMO'], r['vars'], r['clauses'],
            f"{r['med_time']:.4f}", r['med_conflicts'], r['med_decisions'], r['med_props'],
            f"{runs[0]['solve_time']:.4f}", runs[0]['conflicts'], runs[0]['decisions'], runs[0]['propagations'],
            f"{runs[1]['solve_time']:.4f}", runs[1]['conflicts'], runs[1]['decisions'], runs[1]['propagations'],
            f"{runs[2]['solve_time']:.4f}", runs[2]['conflicts'], runs[2]['decisions'], runs[2]['propagations'],
        ])

print("Finished successfully! Saved to data/cdcl_search_stats_3runs.csv")
