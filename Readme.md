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

## Environment

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

The execution environment therefore had access to 12 CPU cores.

<p align="center">
  <img width="977" height="47" alt="cpus_12" src="https://github.com/user-attachments/assets/6febb8a4-a037-47fc-af54-458243640d72" />
</p>

The number of available CPU cores is important because it directly affects the amount of parallelism that MPI implementations can exploit during execution.

---

## Execution Instructions

### Generate Dataset

The dataset generator creates the query file `consulta.txt` and the corpus files used during the experiments.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 python /app/generator.py
```

### Run Sequential Baseline

The sequential implementation processes all files without parallelism and is used as the reference implementation for computing speedup and efficiency.

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 python /app/baseline_secuencial.py
```

### Run MPI Version 1

MPI Version 1 uses static workload distribution based on a round-robin strategy.

```bash
mpirun --allow-run-as-root --oversubscribe -np <number_of_processes> python mpi1.py
```

### Run MPI Version 2

MPI Version 2 uses a dynamic manager-worker scheduling strategy.

```bash
mpirun --allow-run-as-root --oversubscribe -np <number_of_processes> python mpi2.py
```

### Manual Execution Commands Used During the Experiments

#### MPI Version 1 — p = 1

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 mpiexec --allow-run-as-root --oversubscribe -n 1 python /app/mpi1.py
```

#### MPI Version 2 — p = 1

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 mpiexec --allow-run-as-root --oversubscribe -n 1 python /app/mpi2.py
```

### Run Complete Experimental Pipeline

The complete experimental procedure was automated using the provided `run_all.sh` script.

This script:

1. Generates the dataset.
2. Executes the sequential baseline.
3. Executes MPI Version 1.
4. Executes MPI Version 2.
5. Repeats the experiments multiple times.
6. Stores execution logs.
7. Generates a CSV summary file with the execution times.

The experiments were executed with:

```text
p ∈ {1, 2, 4, 8}
```

For each configuration:

```text
3 runs were performed
```

The complete workflow can be executed with:

```bash
docker run --rm -v "${PWD}:/app" augustosalazar/slim-mpi:2 sh /app/run_all.sh
```

---

# 4. Experimental Plan

## a. Sequential Baseline 

The sequential implementation processes all files one by one without using MPI or parallelism.

Its purpose is to validate correctness, provide the reference execution time and compute speedup and efficiency. The baseline implementation reads every file in the dataset and counts the occurrences of each query word.

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

The experiments were executed with:

```text
p ∈ {1, 2, 4, 8}
```

For each configuration:

- 3 runs were performed.
  Execution times were recorded.
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

## Experimental execution records

The following CSV summary contains the execution times collected during the experiments.

<p align="center">
  <img width="240" height="507" alt="Captura de pantalla 2026-05-16 203345" src="https://github.com/user-attachments/assets/0fc26156-d817-4b39-b9ff-2118ac08a7a8" />
</p>

The CSV file stores the execution times collected for every implementation, process configuration, and experimental run. These records were later used to compute the average execution times, speedup, efficiency, and load imbalance ratios presented in this report.

---

## a. Sequential Baseline Timing

The sequential baseline implementation was executed using a single process because it does not use MPI. The execution time obtained for the sequential reference implementation was approximately:

| Program | p | Avg Time (s) |
|---|---|---|
| baseline | 1 | 22.031479 |

This value was later used as the reference baseline for computing speedup and efficiency.

<p align="center">
  <img width="500" height="500" alt="Captura de pantalla 2026-05-16 202348" src="https://github.com/user-attachments/assets/83046680-b927-4c5e-bb8f-2ca4bb057e2c" />
</p>

The execution also produced the global top 10 most frequent words used as the correctness reference for both MPI implementations.

---

### MPI Version 1 — Single Process Execution (p = 1)

Before evaluating scalability with multiple processes, MPI Version 1 was also executed using a single MPI process (`p = 1`). This experiment allowed us to compare the MPI implementation against the sequential baseline while keeping the MPI communication structure active. The following execution logs show the three experimental runs performed for `p = 1`.

<p align="center">
  <img width="850" height="980" alt="mpi1_p1" src="https://github.com/user-attachments/assets/b459302e-1a07-4582-89c2-7601166983d1" />
</p>

The execution times obtained were:

```text
25.944126 s
18.720776 s
15.498512 s
```

The average execution time computed for MPI Version 1 with p = 1 was:

```text
20.054471 s
```

Even with a single process, the MPI implementation performed slightly better than the sequential baseline. This behavior may be influenced by execution variability, cache effects, filesystem buffering, and operating system scheduling.

---

## b. MPI Version 1 Timing Results

MPI Version 1 was experimentally evaluated using the static round-robin distribution strategy.

| Program | p | Avg Time (s) | Speedup | Efficiency | Avg Load Imbalance Ratio |
|---|---|---|---|---|---|
| mpi1 | 1 | 20.054471 | 1.0983 | 1.0983 | N/A |
| mpi1 | 2 | 9.648295 | 2.2835 | 1.1417 | 1.0402 |
| mpi1 | 4 | 6.591308 | 3.3425 | 0.8356 | 1.0457 |
| mpi1 | 8 | 4.225760 | 5.2136 | 0.6517 | 1.1459 |

The results show a significant reduction in execution time as the number of processes increases.

For example:

- Using 2 processes reduced execution time from approximately 20.05 seconds to 9.65 seconds.
- Using 8 processes reduced execution time to approximately 4.23 seconds.

The best execution time was achieved with:

```text
p = 8
```

Obtaining approximately:

```text
4.09 seconds
```

<p align="center">
  <img width="500" height="500" alt="Captura de pantalla 2026-05-16 205530" src="https://github.com/user-attachments/assets/eba0f3d7-e7b5-4239-8263-5d780f38fffe" />
</p>

Although execution time improved considerably, the speedup was not perfectly linear. As the number of processes increased, communication overhead, synchronization costs, and workload imbalance increasingly affected scalability.

---

## c. Load Imbalance Evidence

MPI Version 1 uses static workload distribution, meaning that all files are assigned before execution starts. Even though each process receives approximately the same number of files, this does not guarantee that every process receives the same amount of work. Some files may contain more words, larger text sections, more query matches and higher processing cost.

The following execution log obtained with 8 processes illustrates this behavior:

```text
[rank 0] files=375 local_time=3.545944s
[rank 2] files=375 local_time=4.090355s
```

Even though all processes received the same number of files, their execution times were different. This means that some processes completed their workload earlier and then had to wait until the slowest process finished.

The measured load imbalance ratio for MPI Version 1 was:

```text
Load imbalance ratio = Tmax / Tmin
```
where:

```text
Tmax = execution time of the slowest process
Tmin = execution time of the fastest process
```

```text
Load imbalance ratio = 4.090355 / 3.545944
Load imbalance ratio = 1.1535
```
This value corresponds to the third experimental run using p = 8. The average load imbalance ratio computed across the three runs for p = 8 was:

```text
1.1459
```

The following table summarizes the average load imbalance ratios computed from the three experimental runs for each process configuration.


| MPI Version 1 | Avg Load Imbalance Ratio |
|---|---|
| p = 1 | N/A |
| p = 2 | 1.0402 |
| p = 4 | 1.0457 |
| p = 8 | 1.1459 |

### MPI Version 1 — Load Imbalance Ratio Calculations

#### p = 2

```text
Run 1 = 10.786037 / 10.281152 = 1.0491
Run 2 = 8.989650 / 8.680995 = 1.0356
Run 3 = 9.167715 / 8.850134 = 1.0359

Average = (1.0491 + 1.0356 + 1.0359) / 3
Average = 1.0402
```

#### p = 4

```text
Run 1 = 6.271337 / 6.001084 = 1.0450
Run 2 = 6.106807 / 5.840432 = 1.0456
Run 3 = 7.393910 / 7.064528 = 1.0466

Average = (1.0450 + 1.0456 + 1.0466) / 3
Average = 1.0457
```

#### p = 8

```text
Run 1 = 4.226792 / 3.734578 = 1.1318
Run 2 = 4.357584 / 3.781416 = 1.1524
Run 3 = 4.090355 / 3.545944 = 1.1535

Average = (1.1318 + 1.1524 + 1.1535) / 3
Average = 1.1459
```

A ratio noticeably larger than 1 indicates that the workload distribution was not perfectly balanced. In parallel computing, this situation is known as load imbalance.

When load imbalance occurs some processes stop performing useful work earlier, computational resources become underutilized, and total execution time becomes limited by the slowest process. This negatively affects scalability and overall efficiency.

---

## d. Implementation of MPI Version 2 Correcting the Imbalance with its Timing Results

### MPI Version 2 — Single Process Execution (p = 1)

MPI Version 2 was also executed using a single MPI process (`p = 1`) in order to analyze the overhead introduced by the dynamic scheduling strategy even when no real parallelism is available.

The following execution logs show the three runs performed during the experiment.

<p align="center">
  <img width="900" height="1000" alt="mpi2_p1" src="https://github.com/user-attachments/assets/d010b73c-828c-4c57-aaea-277b0bd9ffbf" />
</p>

The execution times obtained were:

```text
26.724126 s
26.225178 s
20.918884 s
```

The average execution time computed for MPI Version 2 with p = 1 was:

```text
24.622729 s
```

This execution time was slower than both the sequential baseline and MPI Version 1 because the dynamic manager-worker strategy introduced additional communication and scheduling overhead even when only one process was available.

---

### MPI Version 2 Timing Results

MPI Version 2 was evaluated using the dynamic manager-worker scheduling strategy.

| Program | p | Avg Time (s) | Speedup | Efficiency | Avg Load Imbalance Ratio |
|---|---|---|---|---|---|
| mpi2 | 1 | 24.622729 | 0.8947 | 0.8947 | N/A |
| mpi2 | 2 | 14.476575 | 1.5219 | 0.7609 | 1.0000 |
| mpi2 | 4 | 14.100507 | 1.5625 | 0.3906 | 1.0018 |
| mpi2 | 8 | 9.458619 | 2.3292 | 0.2912 | 1.0027 |

The average load imbalance ratio values were computed from the three experimental runs for each process configuration.

The following table summarizes the average load imbalance ratios computed from the three experimental runs for each process configuration.

| MPI Version 2 | Avg Load Imbalance Ratio |
|---|---|
| p = 1 | N/A |
| p = 2 | 1.0000 |
| p = 4 | 1.0018 |
| p = 8 | 1.0027 |

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
Run 1 = 1.0028
Run 2 = 1.0020
Run 3 = 1.0005

Average = (1.0028 + 1.0020 + 1.0005) / 3
Average = 1.0018
```

#### p = 8

```text
Run 1 = 1.0012
Run 2 = 1.0034
Run 3 = 1.0035

Average = (1.0012 + 1.0034 + 1.0035) / 3
Average = 1.0027
```

MPI Version 2 improved workload balance, but its execution time was worse than MPI Version 1. This occurred because the dynamic scheduling strategy introduced additional communication overhead. Workers continuously exchanged messages with rank 0 to request new tasks and send partial results, increasing synchronization and coordination costs. As the number of processes increased, the communication overhead also increased, limiting scalability.

---

### Load Balance Improvement

MPI Version 2 was specifically designed to reduce the imbalance observed in MPI Version 1. Instead of assigning all files statically before execution starts, workers dynamically request new tasks whenever they finish processing their current workload. Additionally, rank 0 also processes files while coordinating workload distribution and collecting partial results. This prevents one processing unit from remaining dedicated exclusively to management tasks.

MPI Version 2 also uses non-blocking probing (`MPI.Iprobe`) to detect completed worker tasks without stopping rank 0 computation. This allows communication and computation to overlap during execution.

The following execution log obtained with 8 processes demonstrates the improved workload balance:

```text
[rank 0] local_time=9.690771s
[rank 1] local_time=9.662283s
[rank 2] local_time=9.656897s
```

The implementation reported:

```text
Load imbalance ratio: 1.0035
```

A value extremely close to 1 indicates that the workload distribution was nearly perfectly balanced.

<p align="center">
  <img width="500" height="500" alt="Captura de pantalla 2026-05-16 210055" src="https://github.com/user-attachments/assets/de4ae7fa-6abd-49ad-952f-8906d74dbc73" />
</p>

Compared to MPI Version 1, the imbalance ratio decreased from:

```text
1.1535 → 1.0035
```

This demonstrates that the dynamic scheduling strategy successfully distributed the workload more evenly across all processes. Even though MPI Version 2 achieved much better workload balance, the communication overhead introduced by the manager-worker strategy outweighed the benefits obtained from improved balancing.

---

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

MPI Version 1 produced a significant improvement compared to the sequential baseline. The sequential implementation required approximately 22.03 seconds to process the dataset, while MPI Version 1 reduced execution time to approximately 4.23 seconds when using 8 processes.

This improvement occurred because the workload was distributed among multiple processes, allowing several files to be processed simultaneously instead of sequentially.

---

## b. Was the observed speedup linear?

Although execution time improved consistently as the number of processes increased, the speedup was not perfectly linear. Ideally, doubling the number of processes would reduce execution time by half. However, real parallel systems rarely behave this way because communication, synchronization, workload coordination, and file I/O operations introduce additional overhead.

For example, MPI Version 1 achieved:

- 2 processes → speedup of 2.2835
- 4 processes → speedup of 3.3425
- 8 processes → speedup of 5.2136

The improvement became progressively smaller as more processes were added. Some efficiency values slightly above 1 may be explained by execution variability, cache effects, operating system scheduling, and measurement noise during short execution intervals.

---

## c. Is there evidence of load imbalance? How was it observed?

MPI Version 1 clearly showed evidence of load imbalance. Even though each process received the same number of files, the local execution times were different:

```text
rank 0 -> 3.545944s
rank 2 -> 4.090355s
```

The average load imbalance ratio for MPI Version 1 using 8 processes was:

```text
1.1459
```

This value confirms that the workload distribution was not perfectly balanced. As a consequence, some processes completed their workload earlier and remained waiting until the slowest process finished. This situation reduced computational resource utilization and negatively affected scalability.

---

## d. Did the second implementation reduce load imbalance?

MPI Version 2 significantly reduced the imbalance observed in MPI Version 1. Workers dynamically requested new tasks whenever they finished processing their current workload, allowing faster processes to continue receiving work instead of remaining inactive. Additionally, rank 0 also processed files locally while coordinating workload distribution and collecting partial results.

The effectiveness of the balancing strategy can be observed in the execution logs:

```text
[rank 0] local_time=9.690771s
[rank 1] local_time=9.662283s
[rank 2] local_time=9.656897s
```

The execution times became almost identical across all processes. The implementation also reported average load imbalance ratios very close to 1:

```text
p = 2 -> 1.0000
p = 4 -> 1.0018
p = 8 -> 1.0027
```

These values indicate that the workload distribution was nearly perfectly balanced.

Compared to MPI Version 1:

```text
MPI1 average imbalance ratio (p = 8) = 1.1459
MPI2 average imbalance ratio (p = 8) ≈ 1.0027
```

This demonstrates that MPI Version 2 successfully reduced the imbalance problem.

---

## e. Did the improved distribution strategy produce a real performance improvement?

Although MPI Version 2 greatly improved workload balance, it did not achieve better execution times than MPI Version 1. MPI Version 1 achieved approximately 4.23 seconds using 8 processes, while MPI Version 2 required approximately 9.46 seconds under the same configuration.

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

# 7. Conclusions

The experimental results demonstrated that both MPI implementations improved execution time compared to the sequential baseline. MPI Version 1 achieved the best overall performance, reducing execution time from approximately 22.03 seconds in the sequential implementation to approximately 4.23 seconds using 8 MPI processes. The most important problem observed in MPI Version 1 was load imbalance. Even though all processes received approximately the same number of files, some processes required more execution time because certain files contained more computational work than others. The average load imbalance ratio measured for MPI Version 1 using 8 processes was:

```text
1.1459
```

MPI Version 2 was specifically designed to reduce this imbalance problem using a dynamic manager-worker scheduling strategy. Workers dynamically requested new tasks whenever they completed their current workload, producing a much more balanced workload distribution.

The measured average load imbalance ratios for MPI Version 2 were:

```text
p = 2 -> 1.0000
p = 4 -> 1.0018
p = 8 -> 1.0027
```

These results demonstrate that MPI Version 2 successfully reduced the imbalance observed in MPI Version 1 and achieved an almost perfectly balanced workload distribution. However, despite improving load balance, MPI Version 2 did not achieve better overall performance than MPI Version 1. The additional communication and synchronization overhead introduced by the dynamic scheduling strategy outweighed the benefits obtained from improved balancing.

Based on the experimental evidence, MPI Version 1 provided the best tradeoff between execution time and communication overhead for this particular problem and dataset, while MPI Version 2 demonstrated that achieving better workload balance does not necessarily guarantee better overall performance. Overall, the experiments illustrate one of the main challenges in parallel computing: finding an effective balance between workload distribution and communication overhead in order to maximize scalability and performance.
