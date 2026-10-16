import sys
sys.path.insert(0, './src')
from sat_solver import NQueensSATSolver, verify_nqueens_solution

for m in ['product', 'commander']:
    print(f'Testing {m} on N=1000...')
    solver = NQueensSATSolver(1000, amo_method=m)
    print(f'  Enc done in {solver.encoding_time:.2f}s, Vars: {solver.num_vars}, Clauses: {solver.num_clauses}')
    sol, stats = solver.solve('cadical195')
    st = stats['solving_time']
    valid = verify_nqueens_solution(sol) if sol else False
    print(f'  Solve done in {st:.2f}s, Status: {stats["status"]}, Valid: {valid}')
