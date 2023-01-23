#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>
#include "vector_operations_aux.h"

void calculate_array(double*, double*, double*, int);

int main(int argc, char** argv){

    int const repetitions = 1e6;
    int size = 0;

	if(argc < 2) {
		printf("usage: task3.out <vector_size>\n");
		return EXIT_FAILURE;
	} else {
		size = atol(argv[1]);
	}

	double a[size], b[size], c[size];
	init_array_double_precision(a, size, 0);
	init_array_double_precision(b, size, 1);
	init_array_double_precision(c, size, 2);

	//double start_time = omp_get_wtime();
	calculate_array(a, b, c, size);
	//double end_time = omp_get_wtime();

	//printf("time: %f seconds\n", end_time - start_time);
	//print_array_double_precision(a, size);
    //check_result_double_precision(a, size);

	return EXIT_SUCCESS;
}

void calculate_array(double* a, double* b, double* c, int size){
    __m512d a_512;
	__m512d b_512;
	__m512d c_512;

	for(int run = 0; run < repetitions; ++run) {
		for(int i = 0; i < size; i += 8) {
			a_512 = _mm512_loadu_pd(&a[i]);
			b_512 = _mm512_loadu_pd(&b[i]);
			c_512 = _mm512_loadu_pd(&c[i]);
			a_512 = _mm512_add_pd(a_512, _mm512_mul_pd(b_512, c_512));
			_mm512_storeu_pd(&a[i], a_512);
		}
	}
}
