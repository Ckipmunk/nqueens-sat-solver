import os
import sys
import csv
import json
import statistics

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")

def sync():
    master_csv = os.path.join(data_dir, "master_cadical_runs.csv")
    with open(master_csv, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    # 1. Sync raw_benchmark_3runs.csv
    by_key = {}
    for r in reader:
        key = (r["experiment"], int(r["n"]), r["method"])
        if key not in by_key:
            by_key[key] = []
        by_key[key].append(r)

    raw_3runs_path = os.path.join(data_dir, "raw_benchmark_3runs.csv")
    with open(raw_3runs_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Experiment", "N", "Method", "Run_1", "Run_2", "Run_3", "Min", "Median", "Max", "Std", "Encoding_Time_s", "Peak_RAM_MB"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for (exp, n, m), runs in by_key.items():
            solv_times = [float(r["solving_time_s"]) for r in runs]
            enc_times = [float(r["encoding_time_s"]) for r in runs]
            rams = [float(r["peak_ram_mb"]) for r in runs]

            writer.writerow({
                "Experiment": exp,
                "N": n,
                "Method": m.capitalize(),
                "Run_1": f"{solv_times[0]:.4f}",
                "Run_2": f"{solv_times[1]:.4f}" if len(solv_times) > 1 else f"{solv_times[0]:.4f}",
                "Run_3": f"{solv_times[2]:.4f}" if len(solv_times) > 2 else f"{solv_times[-1]:.4f}",
                "Min": f"{min(solv_times):.4f}",
                "Median": f"{statistics.median(solv_times):.4f}",
                "Max": f"{max(solv_times):.4f}",
                "Std": f"{statistics.stdev(solv_times):.4f}" if len(solv_times) > 1 else "0.0000",
                "Encoding_Time_s": f"{statistics.median(enc_times):.4f}",
                "Peak_RAM_MB": f"{statistics.median(rams):.1f}"
            })

    # 2. Sync cdcl_search_stats_3runs.csv
    cdcl_path = os.path.join(data_dir, "cdcl_search_stats_3runs.csv")
    with open(cdcl_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Method", "N", "CNF_Hash", "Aux_Vars", "Clauses", "Conflicts", "Decisions", "Propagations", "Props_Per_Conflict", "Props_Per_Decision", "Solving_Time_s"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for n in [32, 64, 128]:
            for m in ["pairwise", "sequential", "commander", "binary", "product"]:
                key = ("AMO Ablation", n, m)
                if key in by_key:
                    runs = by_key[key]
                    solv_times = [float(r["solving_time_s"]) for r in runs]
                    r0 = runs[0]
                    v = int(r0["num_vars"]) - n*n
                    c = int(r0["num_clauses"])
                    conf = int(r0["conflicts"])
                    dec = int(r0["decisions"])
                    prop = int(r0["propagations"])
                    p_c = prop / max(1, conf)
                    p_d = prop / max(1, dec)
                    writer.writerow({
                        "Method": m.capitalize(),
                        "N": n,
                        "CNF_Hash": r0["cnf_hash"],
                        "Aux_Vars": v,
                        "Clauses": c,
                        "Conflicts": conf,
                        "Decisions": dec,
                        "Propagations": prop,
                        "Props_Per_Conflict": f"{p_c:.1f}",
                        "Props_Per_Decision": f"{p_d:.1f}",
                        "Solving_Time_s": f"{statistics.median(solv_times):.4f}"
                    })

        for n in [256, 500, 1000]:
            for m in ["commander", "product", "sequential", "pairwise"]:
                key = ("Scale Evaluation", n, m)
                if key in by_key:
                    runs = by_key[key]
                    solved_runs = [r for r in runs if float(r["solving_time_s"]) < 300.0]
                    r0 = solved_runs[0] if solved_runs else runs[0]
                    solv_times = [float(r["solving_time_s"]) for r in runs]
                    v = int(r0["num_vars"]) - n*n
                    c = int(r0["num_clauses"])
                    conf = int(r0["conflicts"])
                    dec = int(r0["decisions"])
                    prop = int(r0["propagations"])
                    p_c = prop / max(1, conf)
                    p_d = prop / max(1, dec)
                    writer.writerow({
                        "Method": m.capitalize(),
                        "N": n,
                        "CNF_Hash": r0["cnf_hash"],
                        "Aux_Vars": v,
                        "Clauses": c,
                        "Conflicts": conf,
                        "Decisions": dec,
                        "Propagations": prop,
                        "Props_Per_Conflict": f"{p_c:.1f}",
                        "Props_Per_Decision": f"{p_d:.1f}",
                        "Solving_Time_s": f"{statistics.median(solv_times):.4f}"
                    })

    # Load multisolver runs
    ms_csv = os.path.join(data_dir, "master_multisolver_runs.csv")
    ms_runs_by_key = {}
    if os.path.exists(ms_csv):
        with open(ms_csv, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                k = (r["solver"], int(r["n"]))
                if k not in ms_runs_by_key:
                    ms_runs_by_key[k] = []
                ms_runs_by_key[k].append(float(r["time_s"]))

    # 3. Sync unified_benchmark.json
    unified = {"amo_ablation": {}, "solver_comparison": {}}
    for n in [8, 16, 32, 64, 128]:
        unified["amo_ablation"][str(n)] = {}
        for m in ["pairwise", "sequential", "commander", "binary", "product"]:
            key = ("AMO Ablation", n, m)
            if key in by_key:
                runs = by_key[key]
                solv_times = [float(r["solving_time_s"]) for r in runs]
                enc_times = [float(r["encoding_time_s"]) for r in runs]
                r0 = runs[0]
                unified["amo_ablation"][str(n)][m] = {
                    "num_vars": int(r0["num_vars"]),
                    "num_clauses": int(r0["num_clauses"]),
                    "encoding_time_s": statistics.median(enc_times),
                    "solving_time_s": statistics.median(solv_times),
                    "cnf_hash": r0["cnf_hash"]
                }

    solvers = ["SAT CaDiCaL (Commander)", "SAT CaDiCaL (Product)", "SAT CaDiCaL (Pairwise)", "SAT CaDiCaL (Sequential)", "SAT Glucose 4.2 (Product)", "CP-SAT (OR-Tools, 1w)", "Gurobi 13.0 (1t)", "ILP SCIP 9.0"]
    n_list = [8, 16, 32, 64, 128, 256, 500, 1000]

    for n in n_list:
        n_str = str(n)
        unified["solver_comparison"][n_str] = {}
        for s in solvers:
            if "CaDiCaL" in s:
                m = s.split("(")[1].split(")")[0].lower()
                k1 = ("AMO Ablation", n, m)
                k2 = ("Scale Evaluation", n, m)
                t_val = None
                if k1 in by_key:
                    t_val = statistics.median([float(r["solving_time_s"]) for r in by_key[k1]])
                elif k2 in by_key:
                    runs = by_key[k2]
                    med = statistics.median([float(r["solving_time_s"]) for r in runs])
                    if med < 300.0:
                        t_val = med
                unified["solver_comparison"][n_str][s] = {"time_s": t_val}
            elif "Glucose" in s:
                times = ms_runs_by_key.get(("Glucose 4.2", n), [])
                unified["solver_comparison"][n_str][s] = {"time_s": statistics.median(times) if times else None}
            elif "CP-SAT" in s:
                times = ms_runs_by_key.get(("CP-SAT (OR-Tools)", n), [])
                unified["solver_comparison"][n_str][s] = {"time_s": statistics.median(times) if times else None}
            elif "Gurobi" in s:
                times = ms_runs_by_key.get(("Gurobi 13.0", n), [])
                unified["solver_comparison"][n_str][s] = {"time_s": statistics.median(times) if times else None}
            elif "SCIP" in s:
                times = ms_runs_by_key.get(("ILP SCIP 9.0", n), [])
                unified["solver_comparison"][n_str][s] = {"time_s": statistics.median(times) if times else None}

    with open(os.path.join(data_dir, "unified_benchmark.json"), "w", encoding="utf-8") as f:
        json.dump(unified, f, indent=2, ensure_ascii=False)

    print("SYNCHRONIZED ALL DATA FILES SUCCESSFULLY!")

if __name__ == "__main__":
    sync()
