#!/usr/bin/env python3
import math, time, statistics, argparse, csv, sys

def option2_loops(n: int) -> int:
    # Mirrors the assignment’s Option 2:
    # int j = 2; while (j < n) {
    #   k = 2; while (k < n) { Sum += ...; k = k * sqrt(k); }
    #   j += j/2;
    # }
    j = 2.0
    s = 0
    while j < n:
        k = 2.0
        while k < n:
            s += 1  # unit work to simulate Sum += a[k]*b[k]
            k = k * math.sqrt(k)  # k <- k^(3/2)
        j += j / 2.0              # j <- 1.5*j
    return s

def time_run(n: int, trials: int = 3) -> float:
    times_ms = []
    for _ in range(trials):
        t0 = time.perf_counter()
        option2_loops(n)
        t1 = time.perf_counter()
        times_ms.append((t1 - t0) * 1000.0)
    return statistics.median(times_ms)

def main():
    ap = argparse.ArgumentParser(description="Measure Option 2 loops runtime.")
    ap.add_argument("--min-exp", type=int, default=2, help="start at n=10^min_exp (default 2)")
    ap.add_argument("--max-exp", type=int, default=6, help="end at n=10^max_exp (default 6)")
    ap.add_argument("--trials", type=int, default=3, help="median of this many trials (default 3)")
    ap.add_argument("--csv", type=str, default="option2_timings.csv", help="output CSV")
    args = ap.parse_args()

    ns = [10**e for e in range(args.min_exp, args.max_exp + 1)]
    rows = []
    print("n,experimental_time_ms")
    for n in ns:
        ms = time_run(n, trials=args.trials)
        rows.append((n, ms))
        print(f"{n},{ms:.6f}")

    with open(args.csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "experimental_time_ms"])
        for n, ms in rows:
            w.writerow([n, f"{ms:.6f}"])

if __name__ == "__main__":
    sys.exit(main())
