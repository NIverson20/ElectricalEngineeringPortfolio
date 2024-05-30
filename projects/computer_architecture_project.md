# Computer Organization and Architecture Project: Benchmarking VM Performance

## Project Overview

This project, conducted as part of my coursework in Computer Organization and Architecture, involved developing and running benchmark tests in C to assess the processing speeds of different virtual machines (VMs) on a Linux system. The focus was to understand how virtualization impacts performance across various VM configurations.

## Objectives

- **Develop Benchmark Tests:** Implement benchmark programs in C to evaluate the computational performance of VMs, focusing on CPU-bound tasks using the DAXPY algorithm for double precision floating-point operations.
- **Run Tests on Different VMs:** Execute these benchmarks on virtual machines configured with various resource allocations to compare their processing speeds.
- **Analyze Performance:** Collect and analyze data to draw conclusions about the efficiency and performance scalability of VMs under different loads.

## My Role

- **Program Development:** Authored C programs to perform extensive arithmetic operations (specifically DAXPY) and measure their performance across different optimization levels.
- **Test Execution:** Conducted tests on an Intel Xeon 6338 processor under different compiler flags to measure execution times and optimization impacts.
- **Data Analysis:** Analyzed the results to understand the effect of compiler optimizations and CPU clock cycles on arithmetic computation speeds.

## Challenges and Solutions

The challenge was to accurately measure and compare the subtle performance differences between VMs, particularly under varying compiler optimizations. This was addressed by:
- **Standardizing Test Conditions:** Ensuring consistent conditions across all tests to avoid external performance influences.
- **Detailed Metric Analysis:** Utilizing precise performance metrics such as execution time per operation and sustained double-precision operations per second to quantify the differences.

## Results and Impact

- The benchmarks highlighted significant performance improvements with optimization. For example, the `-O2` optimization level showed a nearly 4x speed increase compared to `-O0`, illustrating the potential of compiler optimizations in enhancing computational efficiency.
- The tests also provided insights into the pipeline efficiency and potential data hazards affecting performance, contributing valuable data for optimizing future virtualization setups.

## Gallery

```c
// Sample C code snippet used for benchmarking
#include <stdio.h>
#include <time.h>

int main() {
    double a[1000], x[1000], y[1000], z[1000];
    clock_t start, end;
    double cpu_time_used;
    int i;

    // Initialize arrays
    for (i = 0; i < 1000; i++) {
        a[i] = x[i] = y[i] = 1.0;
    }

    start = clock();
    // DAXPY operation
    for (i = 0; i < 1000; i++) {
        z[i] = a[i] * x[i] + y[i];
    }
    end = clock();

    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken: %f seconds\n", cpu_time_used);

    return 0;
}
```

![Benchmark Output -O0](/images/computer_architecture_images/VM_Test_O0.JPG)

**Figure 1: Benchmark Output with Compiler Optimization -O0** - This screenshot displays the output of the benchmark test running on an Intel Xeon 6338 processor with compiler optimization set to -O0. The test measures the execution time for the DAXPY algorithm without any optimization, providing a baseline for performance comparison. The output details include processor speed, the arithmetic algorithm tested, and the total elapsed time to complete the benchmark.

![Benchmark Output -O2](/images/computer_architecture_images/VM_Test_O2.JPG)

**Figure 2: Benchmark Output with Compiler Optimization -O2** - This screenshot shows the output from the same benchmark test but with compiler optimization set to -O2. Notice the significant reduction in total elapsed time, demonstrating the effectiveness of higher-level optimizations on processing speed. The screenshot also includes detailed metrics such as the number of elements processed, total elapsed time, and execution time per element.

## Full Code

The complete source code for this project is available in this repository. You can view and download the code files using the links below:

- [Client Module Code](/path/to/client.py)
