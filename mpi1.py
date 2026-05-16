"""
mpi1.py - Parallel Word Counting
Strategy: broadcast query words + static (round-robin) file distribution.

Run: 
    mpirun --allow-run-as-root -np <P> python /app/mpi1.py
"""

import os
from collections import Counter
from mpi4py import MPI


# Helpers function to read files and count words

def load_query(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]


def count_words_in_file(filepath: str, query_set: set):

    freq = Counter()

    with open(filepath, "r", encoding="utf-8") as f:

        for line in f:

            for word in line.split():

                w = word.lower()

                if w in query_set:
                    freq[w] += 1

    return freq


# Main function

def main():

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()

    size = comm.Get_size()

    # Step 1 and 2 : Rank 0 reads and broadcasts query words

    if rank == 0:

        script_dir = os.path.dirname(os.path.abspath(__file__))

        dataset_dir = os.path.join(script_dir, "dataset")

        query_words = load_query(
            os.path.join(dataset_dir, "consulta.txt")
        )

        all_files = sorted(
            os.path.join(dataset_dir, f)
            for f in os.listdir(dataset_dir)
            if f.startswith("file_") and f.endswith(".txt")
        )

    else:

        query_words = None
        all_files = None
        dataset_dir = None  # Not used by workers

    # Step 2: broadcast

    query_words = comm.bcast(query_words, root=0)

    all_files = comm.bcast(all_files, root=0)

    query_set = set(query_words)

    # Step 3 and 4: Static distribution (round-robin)

    local_files = [
        f
        for i, f in enumerate(all_files)
        if i % size == rank
    ]

    # Step 5: Local counting

    # Synchronize all processes before timing
    comm.Barrier()

    # Global wall-clock timer
    t_wall_start = MPI.Wtime()

    # Local processing timer
    t_local_start = MPI.Wtime()

    local_freq = Counter()

    for fp in local_files:

        local_freq.update(
            count_words_in_file(fp, query_set)
        )

    t_local_end = MPI.Wtime()

    local_time = t_local_end - t_local_start

    print(
        f"[rank {rank:2d}] "
        f"files={len(local_files):5d}  "
        f"local_time={local_time:.6f}s",
        flush=True,
    )

    # Step 6: Gather partial results at rank 0

    all_local = comm.gather(local_freq, root=0)

    # Step 7: Merge and print top-10

    if rank == 0:

        global_freq = Counter()

        for c in all_local:
            global_freq.update(c)

        # Global execution time
        total_time = MPI.Wtime() - t_wall_start

        print(f"\n=== MPI v1 — {size} process(es) ===")

        print(f"Total files : {len(all_files)}")

        # IMPORTANT:
        # run_all.sh extracts this exact pattern
        print(f"EXECUTION_TIME={total_time:.6f}")

        print("\nTop 10 words:")

        for word, count in global_freq.most_common(10):
            print(f"  {word}: {count}")

        # Save full results for comparison with baseline

        out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dataset",
            "mpi1_results.csv"
        )

        with open(out_path, "w", encoding="utf-8") as fout:

            fout.write("palabra,conteo\n")

            for word in sorted(global_freq):
                fout.write(f"{word},{global_freq[word]}\n")

        print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()