#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>
#include <malloc.h>
#include "vector_operations_aux.h"

void calculate_array(double*, double*, double*, int, int, int);

int main(int argc, char** argv){

    int const repetitions = 1e6;
    int size = 0;
    int num_threads = 1;

	if(argc < 2) {
		printf("usage: task3.out <vector_size> <num_threads>\n");
		return EXIT_FAILURE;
	} else {
	    num_threads = atol(argv[2]);
		size = atol(argv[1]);
	}

	double* a = (double*) memalign(sizeof(double)*4, sizeof(double)*size);
	double* b = (double*) memalign(sizeof(double)*4, sizeof(double)*size);
	double* c = (double*) memalign(sizeof(double)*4, sizeof(double)*size);

	init_array_double_precision(a, size, 0);
	init_array_double_precision(b, size, 1);
	init_array_double_precision(c, size, 2);

	//double start_time = omp_get_wtime();
	calculate_array(a, b, c, size, repetitions, num_threads);
	//double end_time = omp_get_wtime();

    //printf("time: %f seconds\n", end_time - start_time);
	//print_array_double_precision(a, size);
    //check_result_double_precision(a, size);

    free(a);
    free(b);
    free(c);

	return EXIT_SUCCESS;
}

void calculate_array(double* a, double* b, double* c, int size, int repetitions, int num_threads){
    __m256d a_256;
	__m256d b_256;
	__m256d c_256;

    omp_set_num_threads(num_threads);
#pragma omp parallel
    for(int run = 0; run < repetitions; ++run) {
#pragma omp for
		for(int i = 0; i < size; i += 4) {
			a_256 = _mm256_load_pd(&a[i]);
			b_256 = _mm256_load_pd(&b[i]);
			c_256 = _mm256_load_pd(&c[i]);
			a_256 = _mm256_add_pd(a_256, _mm256_mul_pd(b_256, c_256));
			_mm256_store_pd(&a[i], a_256);
		}
	}
}
