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
#include <stdio.h>
#include <stdlib.h>
#include <omp.h> 
#include <immintrin.h>
#include <time.h>
#include <mm_malloc.h>

#define Array_Size 1000 //size of each vector
#define Out_Loops 10000000 //outer accuarcy improvemnt loops

int main(){

	double ex_time = 0.0; //time used to track how long the program runs
	double Time_Start = omp_get_wtime(); //start the timer

	//declaring varables
	double*x = (double*)_mm_malloc(Array_Size * sizeof(double),64);
	double*y = (double*)_mm_malloc(Array_Size * sizeof(double),64);
	double*a = (double*)_mm_malloc(Array_Size * sizeof(double),64);
	double*z = (double*)_mm_malloc(Array_Size * sizeof(double),64);

	srand(time(NULL)); //Used to change the seed for random number gen

	//Fill array with random numbers 0 to 1000
	for(int i=0;i<=Array_Size;i++){
		x[i] = ((double)rand()/ RAND_MAX * 1000.00);
		y[i] = ((double)rand()/ RAND_MAX * 1000.00);
		a[i] = ((double)rand()/ RAND_MAX * 1000.00);
		
	}

	printf("-------------------------------------------------\n");

	printf("Data Vector Element: 0\n"); //print the first values to see the op working
	printf("x[i]: %lf\n",x[0]);
	printf("y[i]: %lf\n",y[0]);
	printf("a[i]: %lf\n",a[0]);
	printf("z[i]: %lf\n",z[0]);
	printf("\n");

	printf("Number of Elements per Vector		= %d\n", Array_Size);
	printf("Number of Resolustion Loops		= %d\n", Out_Loops);
	printf("\n");

	//double for loop to run through each 10000 elemants in the array for the number of time of the outer loops
	for(int k = 0; k <= Out_Loops; k++){

		for(int q=0;q<=Array_Size;q++){

			z[q] = (a[q] * x[q]) + y[q];

		}
	}

	double Time_End = omp_get_wtime(); // end the timer
	ex_time += (Time_End - Time_Start); //add the time of each loop to toghther for total time executing

![Benchmark Output -O0](/images/computer_architecture_project_images/VM_Test_O0.jpg)
**Figure 1: Benchmark Output with Compiler Optimization -O0** - This screenshot displays the output of the benchmark test running on an Intel Xeon 6338 processor with compiler optimization set to -O0. The test measures the execution time for the DAXPY algorithm without any optimization, providing a baseline for performance comparison. The output details include processor speed, the arithmetic algorithm tested, and the total elapsed time to complete the benchmark.
