"""
mpi2.py - Parallel Word Counting

Strategy:
Dynamic task dispatching (manager/worker) where rank 0 also
processes files to improve CPU utilization and reduce idle time.

Run:
    mpirun --allow-run-as-root -np <P> python /app/mpi2.py
"""

import os
from collections import Counter
from mpi4py import MPI


# MPI message tags
TAG_TASK = 1      # Send a file path to process
TAG_RESULT = 2    # Send partial word counts
TAG_FINAL = 3     # Send final statistics



# Helper functions


def load_query(path: str):

    # Read all query words from consulta.txt
    # Each line contains one word

    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]


def count_words_in_file(filepath: str, query_set: set):

    # Count occurrences of query words inside one file

    freq = Counter()

    with open(filepath, "r", encoding="utf-8") as f:

        for line in f:

            for word in line.split():

                w = word.lower()

                if w in query_set:
                    freq[w] += 1

    return freq



# Worker process (rank > 0)


def worker(comm, query_words):

    rank = comm.Get_rank()

    query_set = set(query_words)

    local_freq = Counter()

    n_files = 0

    # Synchronize all processes before timing
    comm.Barrier()

    t_local_start = MPI.Wtime()

    while True:

        # Wait for a task from the manager
        fp = comm.recv(source=0, tag=TAG_TASK)

        # None means there is no more work
        if fp is None:
            break

        # Process assigned file
        partial_freq = count_words_in_file(fp, query_set)

        local_freq.update(partial_freq)

        n_files += 1

        # Send partial result back to rank 0
        comm.send(
            partial_freq,
            dest=0,
            tag=TAG_RESULT
        )

    t_local_end = MPI.Wtime()

    local_time = t_local_end - t_local_start

    # Print local statistics
    print(
        f"[rank {rank:2d}] "
        f"files={n_files:5d}  "
        f"local_time={local_time:.6f}s",
        flush=True,
    )

    # Send final statistics to manager
    comm.send(
        (local_time, n_files),
        dest=0,
        tag=TAG_FINAL
    )



# Manager + worker process (rank 0)


def manager_worker(comm, all_files, query_words):

    size = comm.Get_size()

    query_set = set(query_words)

    # Queue with all remaining files
    file_queue = list(all_files)

    global_freq = Counter()

    # Store statistics per process
    files_per_rank = Counter()

    time_per_rank = {}


    # Special case: only 1 process


    if size == 1:

        comm.Barrier()

        t0 = MPI.Wtime()

        for fp in file_queue:

            global_freq.update(
                count_words_in_file(fp, query_set)
            )

        total_time = MPI.Wtime() - t0

        print("\n=== MPI v2 Optimized — 1 process ===")

        print(f"EXECUTION_TIME={total_time:.6f}")

        print("\nTop 10 words:")

        for word, count in global_freq.most_common(10):
            print(f"  {word}: {count}")

        return


    # Initial distribution


    # Send one file to each worker at the beginning

    comm.Barrier()

    t_wall_start = MPI.Wtime()

    for w in range(1, size):

        if file_queue:

            fp = file_queue.pop(0)

            comm.send(fp, dest=w, tag=TAG_TASK)

        else:

            # If there are not enough files
            comm.send(None, dest=w, tag=TAG_TASK)


    # Rank 0 also processes files


    # This improves resource utilization because
    # the manager is not idle anymore

    t_local_start = MPI.Wtime()

    local_files_rank0 = 0

    while file_queue:

        # Rank 0 processes one file
        fp = file_queue.pop(0)

        partial_freq = count_words_in_file(fp, query_set)

        global_freq.update(partial_freq)

        local_files_rank0 += 1

        # Check if some worker already finished
        # without blocking execution

        while comm.Iprobe(source=MPI.ANY_SOURCE, tag=TAG_RESULT):

            status = MPI.Status()

            recv_freq = comm.recv(
                source=MPI.ANY_SOURCE,
                tag=TAG_RESULT,
                status=status
            )

            src = status.Get_source()

            global_freq.update(recv_freq)

            # Assign a new file immediately
            if file_queue:

                next_fp = file_queue.pop(0)

                comm.send(
                    next_fp,
                    dest=src,
                    tag=TAG_TASK
                )

            else:

                # No more files available
                comm.send(
                    None,
                    dest=src,
                    tag=TAG_TASK
                )


    # Receive remaining worker messages


    active_workers = size - 1

    while active_workers > 0:

        status = MPI.Status()

        result = comm.recv(
            source=MPI.ANY_SOURCE,
            tag=MPI.ANY_TAG,
            status=status
        )

        src = status.Get_source()

        tag = status.Get_tag()

        if tag == TAG_RESULT:

            global_freq.update(result)

            # Worker has finished its last task
            comm.send(
                None,
                dest=src,
                tag=TAG_TASK
            )

        elif tag == TAG_FINAL:

            local_time, n_files = result

            files_per_rank[src] = n_files

            time_per_rank[src] = local_time

            active_workers -= 1

    t_local_end = MPI.Wtime()

    rank0_local_time = t_local_end - t_local_start

    files_per_rank[0] = local_files_rank0

    time_per_rank[0] = rank0_local_time

    total_time = MPI.Wtime() - t_wall_start


    # Print final summary


    print(
        f"\n=== MPI v2 Optimized — {size} process(es) ==="
    )

    print(f"Total files : {len(all_files)}")

    for r in sorted(files_per_rank):

        print(
            f"  [rank {r:2d}] "
            f"files={files_per_rank[r]:5d}  "
            f"local_time={time_per_rank[r]:.6f}s"
        )

    # Compute imbalance ratio
    max_time = max(time_per_rank.values())

    min_time = min(time_per_rank.values())

    if min_time > 0:

        imbalance_ratio = max_time / min_time

        print(
            f"\nLoad imbalance ratio: "
            f"{imbalance_ratio:.4f}"
        )

    # This exact format is required by run_all.sh
    print(f"\nEXECUTION_TIME={total_time:.6f}")

    # Show top 10 most frequent words
    print("\nTop 10 words:")

    for word, count in global_freq.most_common(10):

        print(f"  {word}: {count}")

    # Save full output to CSV
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "dataset",
        "mpi2_results.csv"
    )

    with open(out_path, "w", encoding="utf-8") as fout:

        fout.write("palabra,conteo\n")

        for word in sorted(global_freq):

            fout.write(f"{word},{global_freq[word]}\n")

    print(f"\nFull results saved to: {out_path}")



# Main


def main():

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()

    # Rank 0 prepares dataset information
    if rank == 0:

        script_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        dataset_dir = os.path.join(
            script_dir,
            "dataset"
        )

        # Load query words
        query_words = load_query(
            os.path.join(dataset_dir, "consulta.txt")
        )

        # Get all text files from dataset
        all_files = sorted(
            os.path.join(dataset_dir, f)
            for f in os.listdir(dataset_dir)
            if f.startswith("file_")
            and f.endswith(".txt")
        )

    else:

        query_words = None

        all_files = None

    # Broadcast data to all processes
    query_words = comm.bcast(query_words, root=0)

    all_files = comm.bcast(all_files, root=0)

    # Run manager or worker logic
    if rank == 0:

        manager_worker(
            comm,
            all_files,
            query_words
        )

    else:

        worker(
            comm,
            query_words
        )


if __name__ == "__main__":
    main()