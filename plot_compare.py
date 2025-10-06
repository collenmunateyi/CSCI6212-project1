#!/usr/bin/env python3
import math, argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def theory(n: int) -> float:
    ln = math.log(n)
    return ln * math.log(ln)

def main():
    ap = argparse.ArgumentParser(description="Compare experimental vs theoretical for Option 2.")
    ap.add_argument("--csv", type=str, default="option2_timings.csv", help="input CSV from run_option2_timings.py")
    ap.add_argument("--out", type=str, default="comparison_plot.png", help="output plot filename")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    if set(df.columns) != {"n", "experimental_time_ms"}:
        # accept alternative header capitalization too
        df.columns = [c.strip().lower() for c in df.columns]
        df.rename(columns={"experimental time (ms)": "experimental_time_ms"}, inplace=True)

    df["theory_raw"] = df["n"].apply(lambda x: theory(int(x)))

    f = df["theory_raw"].to_numpy(dtype=float)
    t = df["experimental_time_ms"].to_numpy(dtype=float)
    c = float((f @ t) / (f @ f))   # least-squares: minimize || c f - t ||_2

    df["scaled_theory_ms"] = c * f

    print("Fitted scale constant c =", c)
    print(df.to_string(index=False, formatters={
        "experimental_time_ms": lambda x: f"{x:.6f}",
        "theory_raw": lambda x: f"{x:.4f}",
        "scaled_theory_ms": lambda x: f"{x:.6f}",
    }))

    plt.figure(figsize=(7,5), dpi=150)
    plt.plot(df["n"], df["experimental_time_ms"], marker="o", label="Experimental (ms)")
    plt.plot(df["n"], df["scaled_theory_ms"], marker="s", label="Scaled Theory (ms)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n (log scale)")
    plt.ylabel("Time / Scaled Units (log scale)")
    plt.title("Experimental vs Scaled Theoretical (log–log)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.out)
    print("Saved plot to", args.out)

if __name__ == "__main__":
    main()
