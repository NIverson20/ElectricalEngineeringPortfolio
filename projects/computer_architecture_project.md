# Computer Organization and Architecture Project: Benchmarking VM Performance

## Project Overview

This project was part of my Computer Organization and Architecture course, where I developed a series of benchmark tests in C to evaluate the performance differences across various virtual machines running on Linux. The goal was to understand how different virtualization technologies impact processing speeds under various computational loads.

## Objectives

- **Develop Benchmark Tests:** Write custom C programs to test computational performance, including CPU-bound and memory-bound operations.
- **Run Tests on Different VMs:** Execute these tests on multiple virtual machines to compare the processing speeds.
- **Analyze Performance:** Collect and analyze data to determine the impact of different virtual environments on performance.

## My Role

- **Program Development:** I wrote multiple benchmark programs in C, designed to test various aspects of computer processing, including arithmetic operations, memory access patterns, and disk I/O.
- **Test Execution:** I ran these programs on several virtual machines configured with different resources and operating systems to gather a broad data set.
- **Data Analysis:** Utilized Linux tools to monitor and record performance metrics, which were then analyzed to draw conclusions about each VM's efficiency and speed.

## Challenges and Solutions

One significant challenge was ensuring that the benchmark tests reliably measured the performance characteristics of each VM without external influences. I addressed this by:
- Standardizing the test environment, ensuring that all background processes were minimized.
- Running multiple iterations of each test to average out any anomalies.

## Results and Impact

The tests revealed noticeable differences in processing speeds between VMs, particularly highlighting how resource allocation and VM configuration can dramatically affect performance. These insights are valuable for optimizing virtual environments in real-world applications, improving both efficiency and cost-effectiveness.

## Gallery

Here are some code snippets and graphs from the project (add images or code blocks as appropriate).

```c
// Example of a benchmark test in C
#include <stdio.h>
#include <time.h>

int main() {
    clock_t start, end;
    double cpu_time_used;

    start = clock();
    // Code to benchmark CPU speed
    end = clock();

    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("CPU Time: %f seconds", cpu_time_used);

    return 0;
}
