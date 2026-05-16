<h1 align="center">
Parallel Word Counting with MPI
</h1>

---

# Team Information

- Course: Computer Structure 2
- Project: Parallel Word Counting in a Text Corpus with MPI
- Group: 10
- Univeristy: Universidad del Norte

## Team Members

- Oscar Gil Vergara
- Jean Marthe Moises
- Alberto Niebles Rincon
- Valentina Schotborgh Barrios

---

# Problem Description

The objetive of this laboratory is to design, implement, and experimentally evaluate parallel solutions for a text-processing problem using MPI. Our dataset consists of:
- A file named `consulta.txt` containing query words.
- Multiple text files named `file_XXXX.txt` that form a text corpus.

The goal is to count how many times each query word appears in the corpus and report the top 10 most frequent words.

The project was divided into three stages:
1. Sequential baseline implementation.
2. MPI version 1 using static workload distribution.
3. MPI version 2 using dynamic workload distribution to reduce load imbalance.

---

# Environment and Execution Instructions

## Environment
- Execution Environment: Docker container
- Programming Language and version: Python 3.13.7
- Parallel Library: MPI with mpi4py

## Docker Image

```bash
augustosalazar/slim-mpi:2
```
# Available CPU Cores
To determine the computational resources available for the experiments, the following command was executed inside the Docker container:
```bash
docker run --rm augustosalazar/slim-mpi:2 nproc
```
This command reports the number of processing units (CPU cores) visible to the container environment.
The command produced the following output:

```text
12
```
Therefore, the execution environment had access to 12 CPU cores during the experiments. This information is important because the degree of parallelism that can be efficiently exploited by MPI implementations depends directly on the number of available processing units.

# Execution Instructions
The following commands were used to execute the different stages of the project inside the Docker container environment.

---

## Generate Dataset

The dataset generator creates:

- the query file `consulta.txt`,
- the text corpus composed of multiple `file_XXXX.txt` files.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 python /app/generator.py
```

---

## Run Sequential Baseline

The sequential implementation processes all files without parallelism and is used as the reference execution time for computing speedup and efficiency.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 python /app/baseline_secuencial.py
```

---

## Run MPI Version 1

MPI Version 1 uses static workload distribution based on a round-robin strategy.

The number of MPI processes is specified with the `-np` parameter.

Example:

```bash
mpirun --allow-run-as-root --oversubscribe -np <number_of_processes> python mpi1.py
```

---

## Run MPI Version 2

MPI Version 2 uses a dynamic manager-worker scheduling strategy to reduce load imbalance.

The number of MPI processes is specified with the `-np` parameter.

Example:

```bash
mpirun --allow-run-as-root --oversubscribe -np <number_of_processes> python mpi2.py
```

---
## Run Complete Experimental Pipeline

The provided `run_all.sh` script was used to automate the complete experimental workflow required in the laboratory instructions. The script automatically performs the following tasks:

1. Generates the dataset using `generator.py`,
2. Executes the sequential baseline implementation,
3. Executes MPI Version 1,
4. Executes MPI Version 2,
5. Repeats the experiments multiple times,
6. Stores execution logs for each run,
7. Generates a CSV summary file with the collected execution times. :contentReference[oaicite:1]{index=1}

The experiments were executed with the following numbers of processes:

```text
p ∈ {1, 2, 4, 8}
```

For each configuration:

```text
3 runs were performed
```

The complete workflow is executed with:

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 sh /app/run_all.sh
```
# Experimental Plan

## Sequential Baseline

The sequential implementation processes all files one by one without parallelism.

Its purpose is to:

- validate correctness,
- provide the reference execution time,
- compute speedup and efficiency.

The baseline implementation reads every file in the dataset and counts the occurrences of each query word.

---

## MPI Version 1

MPI Version 1 uses:

- broadcast communication,
- static round-robin workload distribution,
- local counting per process,
- gather operations to merge partial results.

### Workflow

1. Rank 0 reads `consulta.txt`.
2. Rank 0 broadcasts the query words.
3. Rank 0 obtains the list of files.
4. Files are distributed statically using round-robin.
5. Each process counts words locally.
6. Partial results are gathered in rank 0.
7. Rank 0 builds the final result.

The implementation also reports:

- local processing time,
- number of assigned files per process.

---

## MPI Version 2

MPI Version 2 was designed to reduce load imbalance.

Instead of static distribution, it uses a dynamic manager-worker strategy.

### Workflow

1. Rank 0 acts as a manager.
2. Workers request tasks dynamically.
3. Files are assigned on demand.
4. Workers process files and send partial results.
5. Rank 0 merges the results.

This strategy attempts to keep all processes busy and reduce idle time.

The implementation also computes a load imbalance ratio.

---

## Test Procedure

The experiments were executed with:

```text
p ∈ {1, 2, 4, 8}
```

For each configuration:

- 3 executions were performed,
- execution times were recorded,
- average execution times were computed.

The following metrics were calculated.

## Speedup

```text
Sp = Tseq / Tp
```

## Efficiency

```text
Ep = Sp / p
```

where:

- `Tseq` is the sequential execution time,
- `Tp` is the average parallel execution time.

---
# Experimental Plan Execution

# Sequential Baseline Timing

The sequential baseline implementation was executed using a single process (`p = 1`) because it does not use MPI or any form of parallelism. In this implementation, all files are processed one after another by a single execution flow. No workload distribution or parallel execution occurs.
The execution time obtained for the sequential reference implementation was:

| Program | p | Avg Time (s) |
|---|---|---|
| baseline | 1 | 19.458910 |

This value was later used as the reference baseline for computing speedup and efficiency in the MPI implementations. The sequential version establishes the minimum reference point that allows evaluating whether parallel execution actually improves performance.

---

# MPI Version 1 Timing Results

MPI Version 1 uses a static workload distribution strategy based on round-robin assignment.

In this approach:

- rank 0 obtains the list of files,
- the files are distributed before execution starts,
- each process receives approximately the same number of files,
- each process works independently on its assigned subset.

The following table summarizes the average execution times obtained for different numbers of MPI processes:

| Program | p | Avg Time (s) | Speedup | Efficiency |
|---|---|---|---|---|
| mpi1 | 1 | 16.680622 | 1.1666 | 1.1666 |
| mpi1 | 2 | 8.120918 | 2.3961 | 1.1981 |
| mpi1 | 4 | 6.392979 | 3.0438 | 0.7609 |
| mpi1 | 8 | 4.043902 | 4.8119 | 0.6015 |

The results show a clear reduction in execution time as the number of processes increases. This happens because the workload is divided among multiple processes, allowing several files to be processed simultaneously instead of sequentially.

For example:

- using 2 processes reduced the execution time from approximately 19.46 seconds to 8.12 seconds,
- using 8 processes reduced the execution time to approximately 4.04 seconds.

This demonstrates that parallel execution significantly improved performance compared to the sequential baseline. The best execution time was obtained with:

```text
p = 8
```

which achieved approximately:

```text
4.04 seconds
```

However, the speedup was not perfectly linear. As the number of processes increases, the execution time continues improving, but the gains become progressively smaller because of:

- communication overhead,
- synchronization costs,
- file I/O operations,
- workload imbalance between processes.

---

# Load Imbalance Evidence

MPI Version 1 uses a static round-robin distribution strategy, meaning that all files are assigned before execution begins. Although this guarantees that every process receives approximately the same number of files, it does not guarantee that every process receives the same amount of computational work.

Some files may contain:
- larger text content,
- more words,
- more query word matches,
- higher processing cost.

As a result, some processes may finish their assigned work earlier than others. The following execution log obtained with 8 processes illustrates this behavior:

```text
[rank 0] files=375 local_time=3.618352s
[rank 1] files=375 local_time=3.707049s
[rank 6] files=375 local_time=3.817110s
[rank 3] files=375 local_time=3.852881s
[rank 4] files=375 local_time=3.934744s
[rank 5] files=375 local_time=4.023601s
[rank 7] files=375 local_time=4.076794s
[rank 2] files=375 local_time=4.156282s
```

Even though all processes received exactly 375 files, their execution times were different.

For example:

```text
rank 0 -> 3.61s
rank 2 -> 4.15s
```

This means that some processes completed their work earlier and then had to wait until the slowest process finished. In parallel computing, this situation is known as load imbalance.

When load imbalance occurs:
- some processes remain without useful work,
- computing resources are underutilized,
- the total execution time becomes limited by the slowest process.

Therefore, even if several processes finish early, the entire program cannot terminate until all processes complete their assigned tasks. This negatively affects scalability and overall efficiency.

---

# MPI Version 2 Timing Results

MPI Version 2 was implemented to reduce the load imbalance observed in MPI Version 1 while also improving CPU utilization. Unlike the static round-robin strategy used previously, MPI Version 2 uses a dynamic manager-worker scheduling approach. However, in this implementation, rank 0 is not only responsible for coordinating the workload distribution. Rank 0 also actively processes files while simultaneously managing worker communication. This design decision was introduced to avoid wasting computational resources. If rank 0 acted only as a manager, one CPU core would remain dedicated exclusively to communication and synchronization tasks, reducing overall resource utilization.

Instead, MPI Version 2 allows rank 0 to:

- process files locally,
- receive partial results from workers,
- dynamically assign new files,
- merge global word frequencies,
- monitor workload distribution.

The implementation therefore combines:

- dynamic task scheduling,
- asynchronous communication,
- manager-worker coordination,
- concurrent computation on rank 0.

The following table summarizes the average execution times obtained for different numbers of MPI processes:

| Program | p | Avg Time (s) | Speedup | Efficiency |
|---|---|---|---|---|
| mpi2 | 1 | 17.048232 | 1.1414 | 1.1414 |
| mpi2 | 2 | 15.114866 | 1.2874 | 0.6437 |
| mpi2 | 4 | 11.470611 | 1.6964 | 0.4241 |
| mpi2 | 8 | 8.904470 | 2.1853 | 0.2732 |

The results show that execution time still improved compared to the sequential baseline as the number of processes increased. However, MPI Version 2 performed worse than MPI Version 1. This occurred because the dynamic scheduling strategy introduced additional communication overhead.

Workers continuously interacted with rank 0 to:

- request new tasks,
- send partial results,
- receive new file assignments.

At the same time, rank 0 was also processing files locally. Although this strategy improved workload balancing and CPU utilization, it also increased:

- synchronization costs,
- message traffic,
- communication frequency,
- manager coordination overhead.

As the number of processes increased, the amount of communication also increased, reducing the overall scalability of the implementation.

---

# Load Balance Improvement

MPI Version 2 was specifically designed to correct the imbalance problem observed in MPI Version 1. Instead of assigning all files statically before execution starts, the implementation uses dynamic task dispatching.

The workflow operates as follows:

1. Rank 0 initially distributes one file to each worker process.
2. Worker processes start processing their assigned files.
3. Whenever a worker finishes processing a file, it sends its partial result back to rank 0.
4. Rank 0 immediately assigns a new file if work is still available.
5. This process continues dynamically until the file queue becomes empty.

An important optimization implemented in this version is that rank 0 also processes files while coordinating the workload distribution. This prevents the manager process from remaining inactive during execution. Additionally, MPI Version 2 uses non-blocking probing (`MPI.Iprobe`) to detect completed worker tasks without stopping rank 0 computation. This allows communication and computation to overlap, improving overall CPU utilization.

The following execution log obtained with 8 processes demonstrates the improved workload balance:

```text
[rank 0] files=867 local_time=8.615235s
[rank 1] files=305 local_time=8.591272s
[rank 2] files=306 local_time=8.587484s
[rank 3] files=307 local_time=8.581639s
[rank 4] files=301 local_time=8.581649s
[rank 5] files=311 local_time=8.581673s
[rank 6] files=295 local_time=8.587285s
[rank 7] files=308 local_time=8.615032s
```

Unlike MPI Version 1, the local execution times are now almost identical across all processes. This means that processes finished their workloads at nearly the same time, significantly reducing waiting periods caused by imbalance.

The implementation reported:

```text
Load imbalance ratio: 1.0039
```

A value extremely close to 1 indicates that the workload distribution was nearly perfectly balanced. This demonstrates that the dynamic scheduling strategy successfully corrected the imbalance problem observed in the static distribution approach. However, despite improving workload balance, MPI Version 2 still produced worse total execution times than MPI Version 1. The reason is that the communication overhead introduced by the dynamic manager-worker strategy outweighed the performance gains obtained from improved balancing.

# Top 10 Most Frequent Words

The following top 10 most frequent query words were obtained:

```text
a: 785774
para: 392156
sus: 228913
otros: 105530
ante: 99832
unos: 88794
otra: 83901
vosotros: 61617
mios: 58420
tuya: 56635
```

The same top 10 words were obtained across all implementations. This validates the correctness of both MPI implementations with respect to the sequential baseline.

---
# Analysis

## Did the first MPI implementation improve execution time compared to the sequential baseline?

The first MPI implementation produced a significant improvement compared to the sequential baseline. The sequential version required approximately 19.46 seconds to process the complete dataset, while MPI Version 1 reduced the execution time to approximately 4.04 seconds when using 8 processes.

This improvement occurred because the workload was divided among multiple processes, allowing several files to be processed simultaneously instead of sequentially. As the number of processes increased, more portions of the dataset could be analyzed in parallel, which reduced the total execution time considerably.

The results demonstrate that parallelism was effective for this problem and that MPI Version 1 successfully exploited the available computational resources.

---

## Was the observed speedup linear?

Although the execution time improved consistently as the number of processes increased, the speedup was not perfectly linear.

Ideally, doubling the number of processes would reduce the execution time by half. However, real parallel systems rarely behave this way because parallel execution introduces additional overhead that does not exist in sequential execution.

For example, MPI Version 1 achieved the following speedups:

- 2 processes → speedup of 2.3961
- 4 processes → speedup of 3.0438
- 8 processes → speedup of 4.8119

The improvement becomes progressively smaller as more processes are added. This behavior is expected in parallel computing because part of the execution time is spent on communication, synchronization, workload coordination, and file I/O operations instead of useful computation.

Additionally, some processes may finish earlier than others and remain waiting until the slowest process completes its workload. This effect also limits scalability.Therefore, even though the implementation scaled well, the obtained speedup was sublinear rather than perfectly linear.

---

## Is there evidence of load imbalance? How was it observed?

MPI Version 1 clearly showed evidence of load imbalance. The implementation used a static round-robin distribution strategy in which each process received the same number of files before execution started. However, assigning the same number of files does not necessarily mean that all processes receive the same amount of work. Some files may contain more words, larger text sections, or more occurrences of the query terms, which increases the processing time required for those files.

This effect became visible in the execution logs. For example:

```text
rank 0 -> 3.61s
rank 2 -> 4.15s
```

Even though both processes received exactly 375 files, their local execution times were different. This means that some processes completed their work earlier and then had to wait until the slowest process finished. During this waiting period, computational resources remain underutilized because certain CPU cores are no longer performing useful work.

In parallel computing, this situation is called load imbalance, and it negatively affects scalability because the total execution time is always limited by the slowest process.

---

## Did the second implementation reduce load imbalance?

MPI Version 2 significantly reduced the imbalance observed in MPI Version 1. Instead of assigning all files statically at the beginning of execution, MPI Version 2 used a dynamic manager-worker strategy. In this approach, workers requested new tasks whenever they finished processing their current file. This allowed faster processes to continue receiving work instead of remaining inactive while other processes were still busy.

An important improvement in this implementation is that rank 0 was not used exclusively as a manager. Rank 0 also processed files locally while simultaneously coordinating workload distribution and receiving partial results from the workers. This improved CPU utilization and avoided wasting one processing unit only on communication tasks.

The effectiveness of the balancing strategy can be observed in the execution logs:

```text
[rank 0] local_time=8.615235s
[rank 1] local_time=8.591272s
[rank 2] local_time=8.587484s
...
```

The execution times became almost identical across all processes.

Additionally, the implementation reported a load imbalance ratio of:

```text
1.0039
```

A value extremely close to 1 indicates that the workload distribution was nearly perfectly balanced. Therefore, MPI Version 2 successfully corrected the imbalance problem observed in the static distribution strategy.

---

## Did the improved distribution strategy produce a real performance improvement?

Although MPI Version 2 greatly improved workload balance, it did not achieve better total execution times than MPI Version 1. MPI Version 1 achieved approximately 4.04 seconds using 8 processes, while MPI Version 2 required approximately 8.90 seconds under the same configuration.

The main reason is that dynamic scheduling introduced significantly more communication overhead. Workers continuously exchanged messages with rank 0 to request new files and send partial results. At the same time, rank 0 was also coordinating the global execution and merging results. This increased the amount of synchronization and communication occurring during execution. As a consequence, the overhead introduced by dynamic scheduling became larger than the performance gains obtained from improved balancing.

In other words, MPI Version 2 distributed the workload more fairly, but the additional coordination costs reduced the overall performance of the implementation. This result illustrates an important concept in parallel computing: improving load balance does not always guarantee better execution time if the balancing strategy itself introduces excessive overhead.

---

## What limitations affected the experiment?

Several factors affected the performance and scalability of the experiments. First, MPI communication overhead became increasingly important as the number of processes increased. Processes constantly exchanged messages, synchronized execution states, and coordinated workload distribution, all of which added additional execution cost. Second, file I/O operations also limited performance. Every process repeatedly accessed files from disk, and file reading operations are generally much slower than memory operations.

Another important limitation was workload heterogeneity. Some files contained more computational work than others, which affected the static distribution strategy and produced imbalance in MPI Version 1. Docker containerization also introduced a small amount of execution overhead compared to running directly on the host operating system.

Finally, in MPI Version 2, the manager-worker strategy generated a high communication frequency between processes. Although this improved workload balance, the additional coordination cost negatively affected total execution time.

Overall, the experiment demonstrates that parallel performance depends not only on increasing the number of processes, but also on designing efficient workload distribution and minimizing communication overhead.

---
# Conclusions

The experimental results demonstrated that both MPI implementations successfully improved execution time compared to the sequential baseline. The sequential implementation required approximately 19.46 seconds to process the complete dataset, while MPI Version 1 reduced the execution time to approximately 4.04 seconds when using 8 processes. This confirms that parallel execution was effective for the proposed workload and that distributing the corpus among multiple processes significantly improved performance.

The experiments also showed that increasing the number of processes generally reduced execution time. However, the observed speedup was not perfectly linear. As more processes were added, communication overhead, synchronization costs, and file I/O operations became increasingly important and limited scalability. One of the most important problems observed in MPI Version 1 was load imbalance. Although the workload was distributed statically and each process received the same number of files, the local execution times were different because some files required more processing work than others. As a consequence, some processes finished earlier while others continued processing, reducing the overall efficiency of the parallel execution.

MPI Version 2 was specifically designed to correct this imbalance problem through a dynamic manager-worker strategy. In this implementation, workers dynamically requested new tasks whenever they completed their current workload, which allowed the work distribution to become much more balanced. Additionally, rank 0 was able to process files while simultaneously coordinating task assignment and result collection, improving CPU utilization.

The execution logs and the measured load imbalance ratio demonstrated that MPI Version 2 achieved an almost perfectly balanced workload distribution. The imbalance ratio of approximately 1.0039 indicates that all processes finished at nearly the same time. However, despite improving workload balance, MPI Version 2 did not achieve better overall performance than MPI Version 1. The additional communication and synchronization overhead introduced by the dynamic scheduling strategy outweighed the benefits obtained from the improved balance. As a result, MPI Version 2 required approximately 8.90 seconds using 8 processes, which was considerably slower than the 4.04 seconds obtained with MPI Version 1.

Based on the experimental evidence, the static workload distribution used in MPI Version 1 was more efficient for this particular problem and dataset, even though it produced some imbalance. On the other hand, MPI Version 2 demonstrated that achieving better load balance does not necessarily guarantee better performance if the balancing strategy introduces excessive communication overhead.

Overall, the experiments illustrate one of the main challenges in parallel computing: obtaining a good tradeoff between workload balance and communication cost in order to maximize scalability and performance.
