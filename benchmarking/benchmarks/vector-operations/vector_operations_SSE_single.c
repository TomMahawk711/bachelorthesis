#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>
#include <malloc.h>
#include "vector_operations_aux.h"

void calculate_array(float*, float*, float*, int, int, int);

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

	float* a = (float*) memalign(sizeof(float)*4, sizeof(float)*size);
	float* b = (float*) memalign(sizeof(float)*4, sizeof(float)*size);
	float* c = (float*) memalign(sizeof(float)*4, sizeof(float)*size);

	init_array_single_precision(a, size, 0);
	init_array_single_precision(b, size, 1);
	init_array_single_precision(c, size, 2);

	//double start_time = omp_get_wtime();
	calculate_array(a, b, c, size, repetitions, num_threads);
	//double end_time = omp_get_wtime();

    //printf("time: %f seconds\n", end_time - start_time);
	//print_array_single_precision(a, size);
    //check_result_single_precision(a, size);

    free(a);
    free(b);
    free(c);

	return EXIT_SUCCESS;
}

void calculate_array(float* a, float* b, float* c, int size, int repetitions, int num_threads){
    __m128 a_128;
	__m128 b_128;
	__m128 c_128;

    omp_set_num_threads(num_threads);
#pragma omp parallel
	for(int run = 0; run < repetitions; ++run) {
#pragma omp for
		for(int i = 0; i < size; i += 4) {
			a_128 = _mm_load_ps(&a[i]);
			b_128 = _mm_load_ps(&b[i]);
			c_128 = _mm_load_ps(&c[i]);
			a_128 = _mm_add_ps(a_128, _mm_mul_ps(b_128, c_128));
			_mm_store_ps(&a[i], a_128);
		}
	}
}
