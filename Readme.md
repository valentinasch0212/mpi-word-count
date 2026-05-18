# Parallel Word Counting in a Text Corpus with MPI

## 1. Team Information

- **Course:** Computer Structure II
- **Project:** Parallel Word Counting in a Text Corpus with MPI
- **Group:** 10
- **University:** Universidad del Norte

### Team Members

- Oscar Gil Vergara
- Jean Marthe Moises
- Alberto Niebles Rincon
- Valentina Schotborgh Barrios

---

# 2. Problem Description

The objective of this laboratory was to design, implement, and experimentally evaluate parallel solutions for a text-processing problem using MPI.

The dataset consists of:

- A file named `consulta.txt` containing query words.
- Multiple text files named `file_XXXX.txt` that form the text corpus.

The goal is to count how many times each query word appears in the corpus and report the top 10 most frequent words.

The laboratory was divided into three stages:

1. Use the provided sequential implementation as a baseline.
2. Build a first MPI implementation using static workload distribution.
3. Build a second MPI implementation focused on reducing load imbalance.

---

# 3. Environment and Execution Instructions

# Environment

- Execution Environment: Docker container
- Programming Language: Python 3.13.7
- Parallel Library: MPI with mpi4py
- Docker Image:

```bash
augustosalazar/slim-mpi:2
```

## Available CPU Cores

To determine the computational resources available during the experiments, the following command was executed:

```bash
docker run --rm augustosalazar/slim-mpi:2 nproc
```

The output obtained was:

```text
12
```

<p align="center">
  <img width="1000" height="90" alt="Captura de pantalla 2026-05-17 191941" src="https://github.com/user-attachments/assets/6095d3e2-98d5-49bf-a851-2482c185b3ba" />

</p>

The execution environment therefore had access to 12 CPU cores. The number of available CPU cores is important because it directly affects the amount of parallelism that MPI implementations can exploit during execution.

---

# Execution Instructions

## Docker Image

Pull the MPI Docker image:

```bash
docker pull augustosalazar/slim-mpi:2
```

---

## Generate Dataset

The dataset generator creates the query file `consulta.txt` and the corpus files used during the experiments.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 \
python /app/generator.py
```

---

## Run Sequential Baseline

The sequential implementation processes all files without parallelism and is used as the reference implementation for computing speedup and efficiency.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 \
python /app/baseline_secuencial.py
```

---

## Run MPI Version 1

MPI Version 1 uses static workload distribution based on a round-robin strategy.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 \
mpiexec --allow-run-as-root --oversubscribe -n <number_of_processes> \
python /app/mpi1.py
```

Example with 4 processes:

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 \
mpiexec --allow-run-as-root --oversubscribe -n 4 \
python /app/mpi1.py
```

---

## Run MPI Version 2

MPI Version 2 uses a dynamic manager-worker scheduling strategy.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 \
mpiexec --allow-run-as-root --oversubscribe -n <number_of_processes> \
python /app/mpi2.py
```

Example with 4 processes:

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 \
mpiexec --allow-run-as-root --oversubscribe -n 4 \
python /app/mpi2.py
```

---

## Run Complete Experimental Pipeline

The complete experimental procedure was automated using the provided `run_all.sh` script.

This script:

1. Generates the dataset.
2. Executes the sequential baseline.
3. Executes MPI Version 1.
4. Executes MPI Version 2.
5. Repeats the experiments multiple times.
6. Stores execution logs.
7. Generates a CSV summary file with the execution times.

The experiments were executed using:

```text
p ∈ {1, 2, 4, 8}
```

For each configuration, 3 runs were performed.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 \
sh /app/run_all.sh
```

---

# 4. Experimental Plan

## a. Sequential Baseline

The sequential baseline implementation processes the entire dataset using a single execution flow without any form of parallelism. Its main purpose is to provide a reference execution time and verify correctness before introducing MPI-based parallel implementations. The program first reads the query words stored in `consulta.txt`, then iterates through every `file_XXXX.txt` document contained in the dataset directory. For each file, the implementation reads all lines sequentially, splits them into tokens, converts words to lowercase when case sensitivity is disabled, and counts the occurrences of the query words using a global `Counter` structure. 

In addition to generating the final word frequencies, the sequential implementation also records useful statistics such as the number of processed files, the total number of tokens read and the top 10 most frequent query words found in the corpus. The results are stored in a CSV file (`baseline_results.csv`) so that they can later be compared with the outputs produced by the MPI implementations in order to validate correctness. Since the sequential version does not use communication, synchronization or workload distribution, its execution time serves as the baseline reference for computing speedup and efficiency in the parallel experiments. 

---

## b. MPI Version 1

MPI Version 1 uses:

- Broadcast communication.
- Static round-robin workload distribution.
- Local counting per process.
- Gather operations to merge partial results.

### Workflow

1. Rank 0 reads `consulta.txt`.
2. Rank 0 broadcasts the query words.
3. Rank 0 obtains the list of files.
4. Files are distributed statically among the processes.
5. Each process counts words locally.
6. Partial results are gathered in rank 0.
7. Rank 0 builds the final result.

This implementation reports the number of assigned files and the local execution time for each process.

---

## c. The Test Procedure

The experiments were executed using:

```text
p ∈ {1, 2, 4, 8}
```

For each configuration:

- 3 runs were performed.
- Execution times were recorded.
- Local execution times were collected.
- Average execution times were computed.

The following metrics were calculated.

### Speedup

```text
Sp = Tseq / Tp
```

### Efficiency

```text
Ep = Sp / p
```

where:

- `Tseq` is the sequential execution time.

- `Tp` is the average execution time using `p` MPI processes.

---

# 5. Experimental Plan Execution

The following section presents the experimental results obtained from the sequential and MPI implementations.

### Experimental execution records

The following CSV summary contains the execution times collected during the experiments.


<p align="center">
  <img width="400" height="400" alt="CSVNUEVO" src="https://github.com/user-attachments/assets/24b071b0-5cce-48be-9b53-4bc2d694f1ca" />

</p>


The CSV file stores the execution times collected for every implementation, process configuration, and experimental run. These records were later used to compute the average execution times, speedup, efficiency, and load imbalance ratios presented in this report.

## a. Sequential Baseline Timing

The sequential baseline implementation was executed using a single process because it does not use MPI. The execution time obtained for the sequential reference implementation was approximately:

| Program | p | Avg Time (s) |
|---|---|---|
| baseline | 1 | 20.930117 |

This value was later used as the reference baseline for computing speedup and efficiency.

<p align="center">
  <img width="700" height="546" alt="image" src="https://github.com/user-attachments/assets/5679d317-eae7-4b14-bf2c-26bd4e715b1b" />

</p>

The execution also produced the global top 10 most frequent words used as the correctness reference for both MPI implementations.


---
## b. MPI Version 1 Timing Results

### MPI Version 1 — Single Process Execution (p = 1)

Before evaluating scalability with multiple processes, MPI Version 1 was also executed using a single MPI process (` p = 1 `). This experiment allowed us to compare the MPI implementation against the sequential baseline while keeping the MPI communication structure active. The following execution logs show the three experimental runs performed for `p = 1`.

<p align="center">
  <img width="1000" height="900" alt="mpi1_p1" src="https://github.com/user-attachments/assets/2cf1fc04-e741-456d-9663-229c4a000b62" />

</p>

The execution times obtained were:

```text
26.297202 s
28.925550 s
17.477195 s
```

The average execution time computed for MPI Version 1 with `p = 1` was:

```text
24.233316 s
```

The load imbalance ratio obtained for `p = 1` was:

```text
1.0000
```
Since only one MPI process was used, there was no workload distribution among multiple processes and therefore no imbalance between processes.

---
MPI Version 1 was experimentally evaluated using the static round-robin distribution strategy.

| Program | p | Avg Time (s) | Speedup | Efficiency | Avg Load Imbalance Ratio |
|---|---|---|---|---|---|
| mpi1 | 1 | 24.233316 | 0.8637 | 0.8637 | 1.0000 |
| mpi1 | 2 | 8.785993 | 2.3822 | 1.1911 | 1.0202 |
| mpi1 | 4 | 6.356382 | 3.2929 | 0.8232 | 1.0203 |
| mpi1 | 8 | 4.142994 | 5.0515 | 0.6314 | 1.0633 |

The results show a significant reduction in execution time as the number of processes increases.

For example:

- Using 2 processes reduced execution time from approximately 24.23 seconds to 8.79 seconds.

- Using 8 processes reduced execution time to approximately 4.14 seconds.

The best execution time was achieved with:

```text
p = 8
```

Obtaining approximately:

```text
4.14 seconds
```
Although execution time improved considerably, the speedup was not perfectly linear. As the number of processes increased, communication overhead, synchronization costs, and workload imbalance increasingly affected scalability.

---

## c. Load Imbalance Evidence

MPI Version 1 uses static workload distribution, meaning that all files are assigned before execution starts. Even though each process receives approximately the same number of files, this does not guarantee that every process receives the same amount of work. Some files may contain more words, larger text sections, more query matches and higher processing cost. The following execution log obtained with 8 processes illustrates this behavior:

<p align="center">
  <img width="700" height="546" alt="image" src="https://github.com/user-attachments/assets/c0de637a-39c3-467e-80b0-b2ab6773ae66" />

</p>

Even though all processes received the same number of files, their execution times were different. This means that some processes completed their workload earlier and then had to wait until the slowest process finished.

The measured load imbalance ratio for MPI Version 1 was computed as:

```text
Load imbalance ratio = Tmax / Tavg
```

where:

```text
Tmax = Execution time of the slowest process.
Tavg = Average execution time across all MPI processes.
```
This metric measures how much slower the slowest MPI process was compared to the average execution time of all processes. A load imbalance ratio equal to 1 indicates a perfectly balanced workload distribution where all MPI processes required approximately the same execution time. Values larger than 1 indicate that some processes required more time than others, causing certain processes to remain idle while waiting for the slowest one to finish. In static workload distribution strategies this situation commonly appears because different files may contain different computational costs even when the number of assigned files per process is the same.



### MPI Version 1 — Load Imbalance Ratio Calculations

#### p = 2

```text
Run 1 = 8.154630 / 7.939695 = 1.0271
Run 2 = 10.230085 / 10.067642 = 1.0161
Run 3 = 7.967568 / 7.831939 = 1.0173

Average = (1.0271 + 1.0161 + 1.0173) / 3
Average = 1.0202
```

#### p = 4

```text
Run 1 = 6.311770 / 6.201925 = 1.0177
Run 2 = 6.477633 / 6.321632 = 1.0247
Run 3 = 6.277652 / 6.163469 = 1.0185

Average = (1.0177 + 1.0247 + 1.0185) / 3
Average = 1.0203
```

#### p = 8

```text
Run 1 = 4.079945 / 3.826403 = 1.0663
Run 2 = 4.087323 / 3.845451 = 1.0629
Run 3 = 4.259556 / 4.016059 = 1.0606

Average = (1.0663 + 1.0629 + 1.0606) / 3
Average = 1.0633
```

The obtained results clearly show evidence of load imbalance in MPI Version 1. Although each MPI process received the same number of files, the execution times were not identical because some files required more computational work than others. As the number of processes increased, the imbalance ratio also increased, especially for `p = 8`, where the average imbalance ratio reached approximately `1.0633`. This indicates that some processes finished earlier and remained idle while waiting for the slowest process to complete execution.

## d. Implementation of MPI Version 2 Correcting the Imbalance with its Timing Results

MPI Version 2 was specifically designed to reduce the imbalance observed in MPI Version 1. Instead of assigning all files statically before execution starts, workers dynamically request new tasks whenever they finish processing their current workload. Additionally, rank 0 also processes files while coordinating workload distribution and collecting partial results. This prevents one processing unit from remaining dedicated exclusively to management tasks.

MPI Version 2 also uses non-blocking probing (MPI.Iprobe) to detect completed worker tasks without stopping rank 0 computation. This allows communication and computation to overlap during execution.

### MPI Version 2 — Single Process Execution (p = 1)
MPI Version 2 was also executed using a single MPI process (p = 1) in order to analyze the overhead introduced by the dynamic scheduling strategy even when no real parallelism is available. The following execution logs show the three runs performed during the experiment:

<p align="center">
  <img width="1000" height="952" alt="mpi2_p1" src="https://github.com/user-attachments/assets/74f172e8-6088-4b20-a914-fc7877081e08" />

</p>

The execution times obtained were:
```text
22.856472 s
18.782545 s
18.062209 s
```

The average execution time computed for MPI Version 2 with p = 1 was:

```text
19.900409 s
```

The load imbalance ratio obtained for `p = 1` was:

```text
1.0000
```
Since only one MPI process was used, there was no workload distribution among multiple processes and therefore no imbalance between processes.

---

### MPI Version 2 Timing Results

| Program | p | Avg Time (s) | Speedup | Efficiency | Avg Load Imbalance Ratio |
|---|---|---|---|---|---|
| mpi2 | 1 | 19.900409 | 1.0517 | 1.0517 | 1.0000 |
| mpi2 | 2 | 14.850799 | 1.4094 | 0.7047 | 1.0000 |
| mpi2 | 4 | 12.051509 | 1.7367 | 0.4342 | 1.0005 |
| mpi2 | 8 | 9.760644 | 2.1440 | 0.2680 | 1.0027 |

The results show that MPI Version 2 achieved a much more balanced workload distribution compared to MPI Version 1. The dynamic manager-worker scheduling strategy allowed processes that finished their work earlier to immediately receive new files to process, reducing idle time and preventing some processes from remaining inactive while waiting for the slowest process to finish. The average load imbalance ratio values were computed from the three experimental runs for each process configuration. The following table summarizes the average load imbalance ratios computed from the three experimental runs for each process configuration.

However, although MPI Version 2 significantly improved workload balance, it did not achieve better execution times than MPI Version 1. The dynamic scheduling strategy introduced additional communication and synchronization overhead because workers continuously interacted with the manager process during execution. As a result, the implementation achieved better balance but required more total execution time.


### Load Imbalance Ratio Calculations

#### p = 2

```text
Run 1 = 1.0000
Run 2 = 1.0000
Run 3 = 1.0000

Average = (1.0000 + 1.0000 + 1.0000) / 3
Average = 1.0000
```

#### p = 4

```text
Run 1 = 1.0012
Run 2 = 1.0002
Run 3 = 1.0002

Average = (1.0012 + 1.0002 + 1.0002) / 3
Average = 1.0005
```

#### p = 8

```text
Run 1 = 1.0031
Run 2 = 1.0023
Run 3 = 1.0028

Average = (1.0031 + 1.0023 + 1.0028) / 3
Average = 1.0027
```

Compared to MPI Version 1:

```text
MPI1 average imbalance ratio (p = 8) = 1.0633
MPI2 average imbalance ratio (p = 8) ≈ 1.0027
```
MPI Version 2 improved workload balance, but its execution time was worse than MPI Version 1. This occurred because the dynamic scheduling strategy introduced additional communication overhead. Workers continuously exchanged messages with rank 0 to request new tasks and send partial results, increasing synchronization and coordination costs. As the number of processes increased, the communication overhead also increased, limiting scalability.

---

### Load Balance Improvement

The following execution log obtained with 8 processes demonstrates the improved workload balance:
<p align="center">
  <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/2dfbb089-3370-433b-937b-f0c94a7dc1d6" />

</p>

The implementation reported:

```text
Load imbalance ratio: 1.0028
```
A value extremely close to 1 indicates that the workload distribution was nearly perfectly balanced. On the other hand, the MPI Version 1 had the following execution log with the same process configuration: 

<p align="center">
  <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/1020a1e0-9220-45ce-888b-d9c632f2d191" />

</p>

Reporting:

```text
Load imbalance ratio: 1.0606
```

Compared to MPI Version 1, the imbalance ratio decreased from:

1.0606 → 1.0028

This demonstrates that the dynamic scheduling strategy successfully distributed the workload more evenly across all processes. Even though MPI Version 2 achieved much better workload balance, the communication overhead introduced by the manager-worker strategy outweighed the benefits obtained from improved balancing.

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
The same top 10 words were obtained across all implementations, validating the correctness of both MPI solutions.

---

# 6. Analysis

## a. Did the first MPI implementation improve execution time compared to the sequential baseline?

MPI Version 1 produced a significant improvement compared to the sequential baseline. The sequential implementation required approximately 20.93 seconds to process the dataset, while MPI Version 1 reduced execution time to approximately 4.14 seconds when using 8 processes.

This improvement occurred because the workload was distributed among multiple processes, allowing several files to be processed simultaneously instead of sequentially.


---

## b. Was the observed speedup linear?

Although execution time improved consistently as the number of processes increased, the speedup was not perfectly linear. Ideally, doubling the number of processes would reduce execution time by half. However, real parallel systems rarely behave this way because communication, synchronization, workload coordination, and file I/O operations introduce additional overhead.

For example, MPI Version 1 achieved:

```text
2 processes → speedup of 2.3822

4 processes → speedup of 3.2929

8 processes → speedup of 5.0515
```

The improvement became progressively smaller as more processes were added. Some efficiency values slightly above 1 may be explained by execution variability, cache effects, operating system scheduling, and measurement noise during short execution intervals.

---

## c. Is there evidence of load imbalance? How was it observed?

MPI Version 1 clearly showed evidence of load imbalance. Even though each process received the same number of files, the local execution times were different:

```text
rank 0 -> 3.517087s
rank 2 -> 4.079945s
```

The average load imbalance ratio for MPI Version 1 using 8 processes was:

```text
1.0633
```

This value confirms that the workload distribution was not perfectly balanced. As a consequence, some processes completed their workload earlier and remained waiting until the slowest process finished. This situation reduced computational resource utilization and negatively affected scalability.

## d. Did the second implementation reduce load imbalance?

MPI Version 2 significantly reduced the imbalance observed in MPI Version 1. Workers dynamically requested new tasks whenever they finished processing their current workload, allowing faster processes to continue receiving work instead of remaining inactive. Additionally, rank 0 also processed files locally while coordinating workload distribution and collecting partial results.

The effectiveness of the balancing strategy can be observed in the execution logs:

```text
[rank 0] local_time=9.414753s
[rank 1] local_time=9.414713s
[rank 2] local_time=9.376230s
```

The execution times became almost identical across all processes. The implementation also reported average load imbalance ratios very close to 1:

```text
p = 2 -> 1.0000
p = 4 -> 1.0005
p = 8 -> 1.0027
```

These values indicate that the workload distribution was nearly perfectly balanced.

Compared to MPI Version 1:

```text
MPI1 average imbalance ratio (p = 8) ≈ 1.0633
MPI2 average imbalance ratio (p = 8) ≈ 1.0027
```

This demonstrates that MPI Version 2 successfully reduced the imbalance problem.

---

## e. Did the improved distribution strategy produce a real performance improvement?

Although MPI Version 2 greatly improved workload balance, it did not achieve better execution times than MPI Version 1. MPI Version 1 achieved approximately 4.14 seconds using 8 processes, while MPI Version 2 required approximately 9.76 seconds under the same configuration.

The main reason is that dynamic scheduling introduced significantly more communication overhead. Workers continuously exchanged messages with rank 0 to request new files and send partial results, increasing synchronization and coordination costs. As a consequence, the overhead introduced by dynamic scheduling became larger than the performance gains obtained from improved balancing.

This demonstrates that improving workload balance does not necessarily guarantee better overall performance if the balancing strategy introduces excessive communication overhead.

---

## f. What limitations affected your experiment?

Several factors affected the performance and scalability of the experiments. MPI communication overhead became increasingly important as the number of processes increased. Processes constantly exchanged messages and synchronized execution states, increasing execution cost. File I/O operations also limited performance because all processes repeatedly accessed files from disk.

Another important limitation was workload heterogeneity. Some files required more computational work than others, producing imbalance in MPI Version 1.

Finally, in MPI Version 2, the manager-worker strategy generated a high communication frequency between processes. Although this improved workload balance, the additional coordination cost negatively affected total execution time.

Overall, the experiment demonstrates that parallel performance depends not only on increasing the number of processes, but also on designing efficient workload distribution strategies while minimizing communication overhead.

---

# 7. Conclusions

The experimental results demonstrated that both MPI implementations improved execution time compared to the sequential baseline. MPI Version 1 achieved the best overall performance, reducing execution time from approximately 20.93 seconds in the sequential implementation to approximately 4.14 seconds using 8 MPI processes. The most important problem observed in MPI Version 1 was load imbalance. Even though all processes received approximately the same number of files, some processes required more execution time because certain files contained more computational work than others. The average load imbalance ratio measured for MPI Version 1 using 8 processes was:

```text
1.0633
```

MPI Version 2 was specifically designed to reduce this imbalance problem using a dynamic manager-worker scheduling strategy. Workers dynamically requested new tasks whenever they completed their current workload, producing a much more balanced workload distribution.

The measured average load imbalance ratios for MPI Version 2 were:

```text
p = 2 -> 1.0000
p = 4 -> 1.0005
p = 8 -> 1.0027
```

These results demonstrate that MPI Version 2 successfully reduced the imbalance observed in MPI Version 1 and achieved an almost perfectly balanced workload distribution. However, despite improving load balance, MPI Version 2 did not achieve better overall performance than MPI Version 1. The additional communication and synchronization overhead introduced by the dynamic scheduling strategy outweighed the benefits obtained from improved balancing.

Based on the experimental evidence, MPI Version 1 provided the best tradeoff between execution time and communication overhead for this particular problem and dataset, while MPI Version 2 demonstrated that achieving better workload balance does not necessarily guarantee better overall performance. Overall, the experiments illustrate one of the main challenges in parallel computing: finding an effective balance between workload distribution and communication overhead in order to maximize scalability and performance.
