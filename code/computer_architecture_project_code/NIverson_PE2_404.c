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

	printf("\n");
	printf("Data Vectore Element: 0\n"); //print the results of the first operation
	printf("x[i]: %lf\n",x[0]);
	printf("y[i]: %lf\n",y[0]);
	printf("a[i]: %lf\n",a[0]);
	printf("z[i]: %lf\n",z[0]);

	printf("Processor Being Testeted: Intel Xeon 6638\n");

	printf("Processor Clock Freq: 3.20E+09\n");

	printf("Arithmetic Algorithm Testeted: DAXPY Double Precision Floating Point z[i] = (a[i]*x[i]) + y[i]\n");

	printf("Compiler version, and command line option/flag settings: -O2 -fopenmp - march=cascadelake -fno-tree-vectorize\n");

	printf("Number of elements [i] per vector: %d\n",Array_Size);

	printf("Number of outer loops to improve resolution: %d\n",Out_Loops);

	printf("Total Elapsed time to complete benchmark: %.3f\n",ex_time);

	_mm_free(x);
	_mm_free(y);
	_mm_free(z);
	_mm_free(a);

	printf("\n");
	printf("--------------------DONE---------------------\n");
}
